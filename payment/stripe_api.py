import stripe
import logging
from ebdjango import settings
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from contextlib import contextmanager
from ebdjango import settings
@contextmanager
def handle_error():
    result = dict(data=None, error=None)
    
    try:
        yield
    except stripe.error.StripeError as e:
        body = e.json_body.get('error')
        logging.info("==%r=="%(body))
        error  = '%r'%body.get('message', {})
        result['error'] = error 
        return result
    except Exception as e:
        result['error'] = '%s'%e 
        return result

def get_decorator():
    def decorator(func):
        def new_func(*args, **kwargs):
            result = dict(data=None, error=None)
            stripe.api_key = settings.STRIPE_SECRET_KEY
            try:
                return func(*args, **kwargs)
            except stripe.error.StripeError as e:
                print(e)
                body = e.json_body.get('error')
                logging.info("==%r=="%(body))
                error  = '%r'%body.get('message', {})
                result['error'] = error
            except stripe.error.AuthenticationError as e:
                result['error'] = '%s'%e 
            except Exception as e:
                result['error'] = '%s'%e 
            return result
        return new_func

    return decorator


class NewStripeSDK(object):
    
    @staticmethod
    @get_decorator()
    def create_customer(email, stripe_token):
        customer = stripe.Customer.create(
          description = email,
          source = stripe_token,
          email = email,
        )
        logging.info("==%r=="%(customer.to_dict()))
        return dict(data=customer, error=None)
       
    @staticmethod
    @get_decorator()
    def delete_customer(plan_id):
        res = stripe.Customer.retrieve(plan_id)
        res.delete()
        return dict(data=res, error=None)

    @staticmethod
    @get_decorator()
    def create_plan(amount, name, interval="month"):
        res = stripe.Plan.create(
          amount=amount,
          interval="month",
          product={
            "name": name
          },
          currency="usd",
        )
        return dict(data=res, error=None)

    @staticmethod
    @get_decorator()
    def delete_plan(plan_id):
        res = stripe.Plan.retrieve(plan_id)
        res.delete()
        return dict(data=res, error=None)


    @staticmethod
    @get_decorator()
    def create_subscription(customer, plan):
        res = stripe.Subscription.create(
          customer=customer,
          items=[
            {
              "plan": plan,
            },
          ]
        )
        return dict(data=res, error=None)

    @staticmethod
    @get_decorator()
    def delete_subscription(plan_id):
        res = stripe.Subscription.retrieve(plan_id)
        res.delete()
        return dict(data=res, error=None)
