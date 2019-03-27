from datetime import datetime
from django.db import models
from django.contrib import messages

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from ebdjango import settings
from .stripe_api import NewStripeSDK
# Create your models here.
class PaymentTransaction(models.Model):
    date_created = models.DateTimeField(
        _('created'),auto_now_add=True,db_index=True)
    date_updated = models.DateTimeField(
        _('updated'), auto_now=True, db_index=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    messages = models.TextField(max_length=2000)
    txn_id = models.CharField(max_length=50)
    status = models.CharField(
        _('Status'), max_length=15, blank=True, null=True)
    _data = models.TextField(
        blank=True, null=True
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2,default=0)
    def __str__(self):
        return '**%s'% self.txn_id or 'None'

class PaymentToken(models.Model):
    date_created = models.DateTimeField( _('created'), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField( _('updated'), auto_now=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token =  models.CharField(max_length=50)
    last_4_digits = models.CharField(max_length=50, default='1111')
    email = models.EmailField(max_length=50, default='demo')
    name = models.CharField(max_length=50, default='demo')

    def __str__(self):
        return '**%s'% self.token[::-4] or 'None'



class SubscriptionPlan(models.Model):
    date_created = models.DateTimeField( _('created'), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField( _('updated'), auto_now=True, db_index=True)
    name = models.CharField(max_length=255, default='demo')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # interval = models.CharField(max_length=255, choices=CATEGORIES, default="month")
    stripe_plan_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '**%s'% self.name or 'None'

class Subscription(models.Model):
    date_created = models.DateTimeField( _('created'), auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField( _('updated'), auto_now=True, db_index=True)
    name = models.CharField(max_length=255, default='demo')
    token = models.ForeignKey(PaymentToken, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return '**%s'% self.name or 'None'


@receiver(post_delete, sender=PaymentToken, dispatch_uid="delete_stripe_customer")
def delete_stripe_customer(sender, instance, **kwargs):
    #print(instance.token,'delete====================',kwargs)
    res = NewStripeSDK.delete_customer(instance.token)
    #print(instance,'delete====================',res)
    if res.get('error'):
        raise Exception(res.get('error'))



@receiver(post_save, sender=SubscriptionPlan, dispatch_uid="create_stripe_subscription_plan")
def create_stripe_subscription_plan(sender, instance, **kwargs):

    if kwargs['created']:
        res = NewStripeSDK.create_plan(instance.amount, instance.name)
        #print(instance,'create====================',res)
        if res.get('error'):
            raise Exception(res.get('error'))
        else:
            post_save.disconnect(create_stripe_subscription_plan, sender=SubscriptionPlan)
            instance.stripe_plan_id = res.get('data').id
            instance.save()
            post_save.connect(create_stripe_subscription_plan, sender=SubscriptionPlan)
        #print(instance,'create====================',res)


@receiver(post_delete, sender=SubscriptionPlan, dispatch_uid="delete_stripe_subscription_plan")
def delete_stripe_subscription_plan(sender, instance, **kwargs):
    #print(instance.stripe_plan_id,'delete====================',kwargs)
    res = NewStripeSDK.delete_plan(instance.stripe_plan_id)
    #print(instance,'delete====================',res)
    if res.get('error'):
        raise Exception(res.get('error'))



@receiver(post_save, sender=Subscription, dispatch_uid="create_stripe_subscription")
def create_stripe_subscription(sender, instance, **kwargs):
    if kwargs['created']:
        res = NewStripeSDK.create_subscription(instance.token.token, instance.plan.stripe_plan_id)
        #print(instance,'create====================',res)
        if res.get('error'):
            raise Exception(res.get('error'))
        else:
            post_save.disconnect(create_stripe_subscription, sender=SubscriptionPlan)
            instance.stripe_subscription_id = res.get('data').id
            instance.save()
            post_save.connect(create_stripe_subscription, sender=SubscriptionPlan)
        #print(instance,'create====================',res)



@receiver(post_delete, sender=Subscription, dispatch_uid="delete_stripe_subscription")
def delete_stripe_subscription(sender, instance, **kwargs):
    #print(instance.stripe_subscription_id,'delete====================',kwargs)
    res = NewStripeSDK.delete_subscription(instance.stripe_subscription_id)
    #print(instance,'delete====================',res)
    if res.get('error'):
        raise Exception(res.get('error'))

