import json
import random
import re

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.backends import UserModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import CustomUser
from .serializers import UserSerializer


def generate_session_toke(length=10):
    return ''.join(random.SystemRandom().choice([chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]) for _ in range(length))


@csrf_exempt
def signin(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'Send a post request with valid parameter only'})

    username = request.POST['email']
    password = request.POST['password']

    if not re.match("^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", username):
        return JsonResponse({'error': 'Enter a valid email'})

    if len(password) < 3:
        return JsonResponse({'error': 'Password needs to be at least of 3 chars'})

    UserModel = get_user_model()

    try:
        user = UserModel.objects.get(email=username)

        if user.check_password(password):
            user_dict = UserModel.objects.filter(
                email=username).values().first()
            user_dict.pop('password')

            if user.session_token != "0":
                user.sesson_token = "0"
                user.save
                return JsonResponse({'error': 'Previous session exists'})

            token = generate_session_toke
            user.session_token = token
            user.save()
            login(request, user)
            return JsonResponse({'token': token, 'user': user_dict})

        else:
            return JsonResponse({'error': 'Invalid password'})

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid Email'})


def signout(request, id):
    logout(request)

    UserModel = get_user_model

    try:
        user = UserModel.objects.get(pk=id)
        user.session_toke = "0"
        user.save()

    except UserModel.DoesNotExist:
        return JsonResponse({'error': 'Invalid user ID'})

    return JsonResponse({'success': 'Logout success'})


class UserViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {'create': [AllowAny]}

    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self]]

        except KeyError:
            return [permission() for permission in self.permission_classes]
