# Section 03: Getting Structure Ready

- [The Cross-Origin Requests](#the-cross-origin-requests)
- [The Django REST Framework](#the-django-rest-framework)
- [Store Images in Django](#store-images-in-django)
- [Setting Django API Structure](#setting-django-api-structure)
- [Handling API Route](#handling-api-route)

## The Cross-Origin Requests

The first packages we should install would be the [`django-cors headers`](https://github.com/adamchainz/django-cors-headers) because we're going to allow the resources to be accessed on other domains. It adds [Cross-Origin Resource Sharing (CORS)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) headers to responses and allows in-browser requests to our Django application from other origins.

```bash
# install django-cors-headers
$ pipenv install django-cors-headers
```

After install the package, we should edit the `setting.py` file:

1. Add `'corsheaders'` to `INSTALLED_APPS`.
2. Add `'corsheaders.middleware.CorsMiddleware'` to `MIDDLEWARE`.
3. Set `ALLOWED_HOSTS` to be `['*']`. Because we want all the hosts to be allowed to interact an app.
4. Set `CORS_ORIGIN_ALLOW_ALL` to be `True`.

<br/>
<div align="right">
  <b><a href="#section-03-getting-structure-ready">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## The Django REST Framework

The second package should be installed would be [`djangorestframework`](https://github.com/encode/django-rest-framework) because we are going to use the django server as an API server and expose the RESTful API for React front-end.

```bash
# install django-rest-framework
$ pipenv install djangorestframework
```

After install the package, we should edit the `setting.py` file:

1. Add `'rest_framework'` to `INSTALLED_APPS`. The `rest_framework` is going to be required for throwing up the JSON format for product categories, orders and so on.
2. Add `'rest_framework.authtoken'` to `INSTALLED_APPS`. The `'rest_framework.authtoken'` is going to be required so that customers signup can be created.
3. Setup `REST_FRAMEWORK`. Just paste the code shown below:
    ```python
    REST_FRAMEWORK = {
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ]
    }
    ```

After doing so, we can edit the `urls.py` file and add the routes:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls'))
]
```

<br/>
<div align="right">
  <b><a href="#section-03-getting-structure-ready">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Store Images in Django

There are a couple of ways and couple of strategies that we can follow while holding up images, audios and videos. We're going to create a folder `media` to keep the images and insert the following code to `settings.py` (be careful to add slash `/` after the path):

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Don't forget to add the path to `urls.py`:

```python
...
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    ...
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

<br/>
<div align="right">
  <b><a href="#section-03-getting-structure-ready">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Setting Django API Structure

It's a better approach to create another app which will be `API` to be interacted, transferred or received instead of serving APIs in the `ecom` app.

```bash
# create another app
$ django-admin startapp api
```

Then we're going to create `category`, `order`, `payment`, `product` and `user` inside the app `api`.

```bash
# don't forget to move into the directory of api
$ cd api

# create apps inside api
$ django-admin startapp category
$ django-admin startapp order
$ django-admin startapp payment
$ django-admin startapp product
$ django-admin startapp user
```

<br/>
<div align="right">
  <b><a href="#section-03-getting-structure-ready">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Handling API Route

Remember that any installed app needs to be taken up in `INSTALLED_APPS` in `settings.py`. Then we need to edit the `urls.py` in `ecom` folder:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api/', include('api.urls'))
]
```

Notice that we include the `urls` inside the `api` so that we should create the `urls.py` in the `api` folder:

```python
from django.urls import path, include
from rest_framework.authtoken import views
from .views import home


urlpatterns = [
    path('', home, name='api.home'),
]
```

Notice that the `home` is from `views.py` in the `api` folder:

```python
from django.http import JsonResponse


# Create your views here.
def home(request):
    return JsonResponse({'info': 'Django React Course', 'name': 'hitech'})
```

<br/>
<div align="right">
  <b><a href="#section-03-getting-structure-ready">[ ↥ Back To Top ]</a></b>
</div>
<br/>