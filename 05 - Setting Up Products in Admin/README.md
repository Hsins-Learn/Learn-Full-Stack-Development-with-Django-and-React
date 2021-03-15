# Section 05: Setting Up Products in Admin

- [Add Model for Product in Django](#add-model-for-product-in-django)
- [Image Serialization and Product Views in Django](#image-serialization-and-product-views-in-django)
- [Setting up URL for Products in Django](#setting-up-url-for-products-in-django)

## Add Model for Product in Django

We're going to use `ImageField` and it needs the [Pillow](https://python-pillow.org/) as part of the dependencies. Install the Pillow package first by following commands:

```bash
$ pipenv install Pillow
```

The stuffs here are almost as same as the `models.py` of `category` app but the one thing that different. We need a **foreign key** of the category.

```python
from django.db import models
from django.db.models.fields import CharField
from api.category.models import Category


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.CharField(max_length=50)
    stock = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True, blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

Moreover, don't forget to register `product` to admin panel and add it to `INSTALLED_APPS` in the `settings.py`. Then make the migrations before running server.

<br/>
<div align="right">
  <b><a href="#section-05-setting-up-products-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Image Serialization and Product Views in Django

When we're going to implement the serialization of the Product class, what happens is that it doesn't provide an absolute URL in Django. However, we can modify the serializer to return the absolute URL of images by using a custom `serializers.SerializerMethodField`.

```python
from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    image = serializers.ImageField(
        max_length=None, allow_empty_file=False, allow_null=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'image', 'category')
```

Then create the `ProductViewSet` in `views.py` of `product` app:

```python
from rest_framework import viewsets

from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
```

<br/>
<div align="right">
  <b><a href="#section-05-setting-up-products-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Setting up URL for Products in Django

After create the serializers and views, don't forget to add it to the `urls.py` of `product` app.

```python
from rest_framework import routers
from django.urls import path, include

from . import views

router = routers.DefaultRouter()
router.register(r'', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls))
]
```

<br/>
<div align="right">
  <b><a href="#section-05-setting-up-products-in-admin">[ ↥ Back To Top ]</a></b>
</div>
<br/>
