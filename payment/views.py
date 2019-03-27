import os
import datetime
import logging
import stripe
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from ebdjango import settings

from .models import User, PaymentToken, Subscription, SubscriptionPlan
from .forms import CardForm
from .stripe_api import NewStripeSDK

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def soon():
    soon = datetime.date.today() + datetime.timedelta(days=30)
    return {'month': soon.month, 'year': soon.year}


@login_required
def card_edit(request):
    uid = request.session.get('user')
    if uid is None:
        return HttpResponseRedirect('/')
    user = User.objects.get(pk=uid)
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid() and user.payment_token_id:
            payment_token_id = user.payment_token_id
            customer = stripe.Customer.retrieve(payment_token_id.token)
            customer.card = form.cleaned_data['stripe_token']
            customer.save()
            payment_token_id.last_4_digits = form.cleaned_data['last_4_digits']
            payment_token_id.token = customer.id
            payment_token_id.save()
    form = CardForm()
    return render(request, 'payment/edit.html',
                  {
                      'form': form,
                      'publishable': settings.STRIPE_PUBLIC_KEY,
                      'soon': soon(),
                      'months': range(1, 13),
                      'years': range(2018, 2036)
                  }
                  )


@login_required
def card_delete(request, pk):
    data = request.GET

    obj = get_object_or_404(PaymentToken, pk=pk)
    obj.delete()
    return card_register(request)


@login_required
def card_register(request):
    user = request.user
    customer = None
    error = None
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            res = NewStripeSDK.create_customer(form.cleaned_data['email'], form.cleaned_data['stripe_token'])
            customer = res.get('data')
            error = res.get('error')
            if customer:
                token = PaymentToken(
                    last_4_digits=form.cleaned_data['last_4_digits'],
                    token=customer.id,
                    user=user,
                    email=form.cleaned_data['email'],
                    name=form.cleaned_data['name'],
                )
                token.save()
    tokens = PaymentToken.objects.filter(user=user)
    form = CardForm()
    return render(request, 'payment/register.html',
                  {'form': form, 'months': range(1, 13), 'active_tokens': tokens, 'server_error': error,
                   'publishable': settings.STRIPE_PUBLIC_KEY,
                   'soon': soon(), 'user': user, 'years': range(2019, 2036)})


@login_required
def subscription(request):
    user = request.user
    subscription = Subscription.objects.filter(user=user)

    if subscription:
        user.subscription.delete()
        return redirect('accounts:view_profile')
    tokens = PaymentToken.objects.filter(user=user)
    subscription_plan = SubscriptionPlan.objects.first()
    if not tokens.count():
        return card_register(request)

    subscription = Subscription.objects.create(
        name='Task of the day membership for user: %s' % user,
        token=tokens[0],
        plan=subscription_plan,
        user=user,
    )
    print(subscription.stripe_subscription_id)
    return redirect('accounts:view_profile')
