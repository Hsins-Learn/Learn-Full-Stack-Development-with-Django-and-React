# Section 08: Payment Gateway Backend

- [Understand the Payment Gateway](#understand-the-payment-gateway)
- [Setup the Simple Server for Braintree](#setup-the-simple-server-for-braintree)
- [Process the Payment from Backend in Django](#process-the-payment-from-backend-in-django)
- [Setup Payment URLs and Debug in Django](#setup-payment-urls-and-debug-in-django)

## Understand the Payment Gateway

We are not bank and we can't actually validate people for all the payments so that we need to use the payment gateway like [Stripe](https://stripe.com/) or [Braintree](https://www.braintreepayments.com/).

Let's discuss the strategy that how Braintree works. The following figures from [Get Started Document](https://developers.braintreepayments.com/start/overview) of Braintree shows how the client, the server and Braintree interact:

<p align="center">
  <img src="https://i.imgur.com/sXPIYDd.png" alt="Braintree: How It Works" weight="400px">
</p>

1. Our front-end requests a client token from our server and initializes the client SDK.
2. Our server generates and sends a client token back to our client using the server SDK.
3. The customer submits payment information, the client SDK communicates that information to Braintree and returns a payment method nonce.
4. Our front-end sends the payment method nonce to our server.
5. Our server code receives the payment method nonce and then uses the server SDK to create a transaction.

<br/>
<div align="right">
  <b><a href="#section-08-payment-gateway-backend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Setup the Simple Server for Braintree

After create the account for using sandbox of Braintree, we should also install the `braintree` package by `pip` or `pipenv`.

```bash
$ pipenv install braintree
```

We don't need to have a model because the modeling is not necessarily in our case. We just need to worry about people will be hitting some routes and we need to run some methods for that. Let's edit the `views.py` of `payment` app by adding following code.

```python
import braintree
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id="MERCHANT_ID",
        public_key="PUBLIC_KEY",
        private_key="PRIVATE_KEY"
    )
)


def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def generate_token(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, Please login again.'})

    return JsonResponse({'clientToken': gateway.client_token.generate(), 'success': True})
```

<br/>
<div align="right">
  <b><a href="#section-08-payment-gateway-backend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Process the Payment from Backend in Django

So far what we have done is we were able to check successfully all the things we wanted to do. Then we have generated the token and send it to the front-end.

<p align="center">
  <img src="https://i.imgur.com/JXGVCiN.png" alt="Braintree: How It Works" weight="400px">
</p>

Consider the figure shown above, we have done the No.1 and No.2 part and the front-end will able to generate the **Nonce**. The Nonce is something like a pack of information that is sent to us from the front-end with the amount that needs to be deducted. Then we can simply add following code to `views.py` in order to pass that information to the server:

```python
@csrf_exempt
def process_payment(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Invalid session, Please login again.'})

    nonce_from_the_client = request.post["paymentMethodNonce"]
    amount_from_the_client = request.post["amount"]

    result = gateway.transaction.sale({
        "amount": amount_from_the_client,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        return JsonResponse({
            "success": result.is_success,
            "transaction": {'id': result.transaction.id, 'amount': result.transaction.amount}
        })
    else:
        return JsonResponse({'error': True, 'success': False})
```

<br/>
<div align="right">
  <b><a href="#section-08-payment-gateway-backend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Setup Payment URLs and Debug in Django

Finally, don't forget to edit the `urls.py` and the `settings.py` for the `payment` app. We don't need viewset for it and the `urls.py` of `payment` app would be:

```python
from django.urls import path, include

from . import views


urlpatterns = [
    path('gettoken/<str:id>/<str:token>',
         views.generate_token, name='token.generate'),
    path('process/<str:id>/<str:token>',
         views.process_payment, name='payment.process'),
]
```

<br/>
<div align="right">
  <b><a href="#section-08-payment-gateway-backend">[ ↥ Back To Top ]</a></b>
</div>
<br/>
