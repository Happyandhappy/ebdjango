from functools import update_wrapper , wraps
from django.utils.decorators import available_attrs
from django.http import HttpResponseRedirect
from .models import PaymentToken
from django.urls import reverse_lazy, reverse


def requiresCard(failed_url=reverse_lazy('card_register')):
    def decorator(view_function):
        def _wrapped_view(request,*args,**kwargs):
            tokens = PaymentToken.objects.filter(user=request.user)
            token_exist = tokens.count()
            if tokens.exists():
                return view_function(request,*args,**kwargs)
            return HttpResponseRedirect(failed_url)
        return wraps(view_function,assigned=available_attrs(view_function))(_wrapped_view)
    return decorator
