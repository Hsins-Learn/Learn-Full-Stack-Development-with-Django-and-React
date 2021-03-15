# Section 02: Installation for Backend

- [Python and Virtual Environment](#python-and-virtual-environment)
- [Setup The Django](#setup-the-django)

## Python and Virtual Environment

There are multiple ways how we can have virtual environments and one of the easiest way is `pipenv`. It creates a new file `Pipfile` which contains information for the dependencies of the project, and supersedes the requirements.txt file used in most Python projects.

```bash
# install the pipenv
$ pip install pipenv

# create a virtual environment for project
$ pipenv shell

# install packages
$ pipenv install Django==3.0.8
```

<br/>
<div align="right">
  <b><a href="#section-02-installation-for-backend">[ ↥ Back To Top ]</a></b>
</div>
<br/>

## Setup The Django

```bash
# create new django project
$ django-admin startproject ecom

# move anything that we have created into the database
$ python manage.py makemigrations
$ python manage.py migrate

# create the super user
$ python manage.py createsuperuser

# run the server
$ python manage.py runserver
```

<br/>
<div align="right">
  <b><a href="#section-02-installation-for-backend">[ ↥ Back To Top ]</a></b>
</div>
<br/>
