# Section 04: Setting Up Categories in Admin

- [Setting up Category Models and Admin](#setting-up-category-models-and-admin)
- [Serialize the Data from Database in Django](#serialize-the-data-from-database-in-django)
- [Category API Routing and Views in Django](#category-api-routing-and-views-in-django)
- [Testing with Postman for Category in Django](#testing-with-postman-for-category-in-django)

## Setting up Category Models and Admin

A Model is the single, definitive source of information about our data in Django. Each model is just a Python class that subclasses `django.db.models.Model`. Let's create the models in the `models.py` of `category` app:

```python
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

If we want to manipulate our data in the admin panel, we should register the `Category` class in the `admin.py` file after creating our `Category` class.

```python
from django.contrib import admin
from .models import Category


# Register your models here.
admin.site.register(Category)
```

Don't forget to do migration and adding apps to `INSTALLED_APPS` in `setting.py` before running our server, both of them are common problems that happend to all the Django Creators. By the way, the name of the `category` should be exactly the same with `name` inside `apps.py` file.

<br/>
<div align="right">
  <b><a href="#section-04-setting-up-categories-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Serialize the Data from Database in Django

Migrations are necessary whenever we create a new model and register that model. And once the migration files are there by running `python manage.py makemigrations`, we simply have to make the migrations by running `python manage.py migrate`.

The other thing we need to get started on our Web API is to provide a way of serializing and deserializing the instances into representations such as json. We can do this by declaring serializers that work very similar to Django's forms in the `serializers.py` file of `category` app:

```python
from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'description')

```

<br/>
<div align="right">
  <b><a href="#section-04-setting-up-categories-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Category API Routing and Views in Django

Let's see how to write some the views using our the `CategorySerializer` class.

```python
from rest_framework import viewsets

from .serializers import CategorySerializer
from .models import Category


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
```

In order to enable the `CategoryViewSet`, we need to add routes to `urls.py` of `category` app.

```python
from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

<br/>
<div align="right">
  <b><a href="#section-04-setting-up-categories-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Testing with Postman for Category in Django

[Postman](https://www.postman.com/) is such a great tool for every developers to test the APIs.


<br/>
<div align="right">
  <b><a href="#section-04-setting-up-categories-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>