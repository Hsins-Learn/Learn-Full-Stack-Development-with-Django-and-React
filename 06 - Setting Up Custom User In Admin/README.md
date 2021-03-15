# Section 06: Setting Up Custom User in Admin

- [Custom User Model in Admin](#custom-user-model-in-admin)
- [Custom User Serialization in Django](#custom-user-serialization-in-django)
- [Custom User Sign-In in Django](#custom-user-sign-in-in-django)
- [Classic Super Admin Issue in Django](#classic-super-admin-issue-in-django)

## Custom User Model in Admin

Django provides us the default authentication and we have use it creating the super admin. The same mechanism can be used for the regular authentication for any other user as well but we have the challenge to separate login for admins and regular users.

The workflow would be:

1. People will send us data in the JSON format.
2. Server need to extract that information and register the user into the database.

Of course, the first step we're going to do is creating the models based on existing model. According to the [document](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project), we can customize by creating a `CustomUser` class inherit the `AbstractUser` in `models.py` of the `user` app:

```python
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=254, unique=True)

    # The field is already there, we have to make it as None because we're not
    # gogin to be sign in of the user based on the username
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    # Django doesn't work wih token based so obviously the fields need to be
    # stored.
    session_token = models.CharField(max_length=10, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Note that we set the `username` to be `None` because we're not going to be sign-in of the user based on the `username` and set the `USERNAME_FIELD` to be `email` field.

<br/>
<div align="right">
  <b><a href="#section-06-setting-up-custom-user-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Custom User Serialization in Django

We need to write our own serializers of custom users in the `serializers.py` in the `user` app or Django would use the default User serializer.

```python
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import authentication_classes, permission_classes

from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # the instance is going to be interacting with the model and will be
        # saving it based on that
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)

        instance.save()
        return instance

    class Meta:
        model = CustomUser
        # this is the point where we can add our extra parameter that we want to
        # be handled with the databases
        extra_kwargs = {'password': {'write_only': True}}
        fields = ('name', 'email', 'password', 'phone',
                  'gender', 'is_active', 'is_stuff', 'is_superuser')
```

<br/>
<div align="right">
  <b><a href="#section-06-setting-up-custom-user-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Custom User Sign-In in Django

```python
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
```

```python
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api/', include('api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

<br/>
<div align="right">
  <b><a href="#section-06-setting-up-custom-user-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Classic Super Admin Issue in Django

The only issue right now is a classic issue of Django, where once we do customization of our user model, then creating a super user is a challenge. There's a simple solution to create such a migrate Python file in the `api` app:

```python
from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(name="hsins",
                          email="hsinspeng@gmail.com",
                          is_stuff=True,
                          is_superuser=True,
                          phone="123456789",
                          gender="Male"
                          )
        user.set_password("admin1234")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data)
    ]
```

And then make migrations by follow commands:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br/>
<div align="right">
  <b><a href="#section-06-setting-up-custom-user-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>