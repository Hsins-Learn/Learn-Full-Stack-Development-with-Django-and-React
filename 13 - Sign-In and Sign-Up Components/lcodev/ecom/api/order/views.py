from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from .models import Order
from .serializers import OrderSerializer


# Create your views here.
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
