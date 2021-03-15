# Section 07: Getting Orders in Admin Django

- [Creating Model for Orders in Django](#creating-model-for-orders-in-django)
- [Add Serialization for Orders](#add-serialization-for-orders)
- [User Authentication and Order Placement in Django](#user-authentication-and-order-placement-in-django)
- [URL for Order and Auth Token in Django](#url-for-order-and-auth-token-in-django)

## Creating Model for Orders in Django

Obviously, the operations of order would include the `CustomUser` and `Product` class. Let's create the `Order` class in the `models.py` of `order` app.

```python
from django.db import models
from api.user.models import CustomUser
from api.product.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    product_names = models.CharField(max_length=500)
    total_products = models.CharField(max_length=500, default=0)
    transaction_id = models.CharField(max_length=150, default=0)
    total_amount = models.CharField(max_length=50, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

<br/>
<div align="right">
  <b><a href="#section-07-getting-orders-in-admin-django">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Add Serialization for Orders

The implementation of order serializer is as same as the others. Add `serializers.py` in the `order` app folder with following code:

```python
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('user')
```

<br/>
<div align="right">
  <b><a href="#section-07-getting-orders-in-admin-django">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## User Authentication and Order Placement in Django

There are two main objective in the views:

- Validate the user, whether the user is signed-in or not. Because we want to allow the purchase only for the signed-in user.
- When the authenticated user makes the payment, the page should be redirected to another URL.

```python
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


def validate_user_session(id, token):
    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(pk=id)
        if user.session_toke == token:
            return True
        return False
    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse({'error': 'Please re-login', 'code': '1'})

    if request.method == 'Post':
        user_id = id
        transaction_id = request.POST['transcation_id']
        amount = request.POST['amount']
        products = request.POST['products']

        total_products = len(products.split(',')[:-1])

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'})

        order = Order(user=user, product_names=products,
                      total_products=total_products, transaction_id=transaction_id, total_amount=amount)
        order.save()

        return JsonResponse({'success': True, 'error': False, 'msg': 'Order placed Successfully'})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('name')
    serializer_class = OrderSerializer
```

<br/>
<div align="right">
  <b><a href="#section-07-getting-orders-in-admin-django">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## URL for Order and Auth Token in Django

We are working on the custom token that we have generated but the Django REST Framework provide us a way of generating their own token as well. We can implement that part by refering to this [article](https://simpleisbetterthancomplex.com/tutorial/2018/11/22/how-to-implement-token-authentication-using-django-rest-framework.html). Just edit the `urls.py` in `api` app folder:

```python
from django.urls import path, include
from rest_framework.authtoken import views
from .views import home


urlpatterns = [
    path('', home, name='api.home'),
    path('category/', include('api.category.urls')),
    path('product/', include('api.product.urls')),
    path('user/', include('api.user.urls')),
    path('order/', include('api.order.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
]
```

<br/>
<div align="right">
  <b><a href="#section-07-getting-orders-in-admin-django">[ ↥ Back To Top ]</a></b>
</div>
<br/>