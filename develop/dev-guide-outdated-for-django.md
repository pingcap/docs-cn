---
title: App Development for Django
summary: Learn how to build a simple Python application using TiDB and Django.
---

# App Development for Django

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple Python application based on TiDB and Django. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

## Step 1. Start a TiDB cluster

Start a pseudo TiDB cluster on your local storage:

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

The above command starts a temporary and single-node cluster with mock TiKV. The cluster listens on the port `$LOCAL_PORT`. After the cluster is stopped, any changes already made to the database are not persisted.

> **Note:**
>
> To deploy a "real" TiDB cluster for production, see the following guides:
>
> + [Deploy TiDB using TiUP for On-Premises](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> + [Deploy TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> You can also [use TiDB Cloud](https://pingcap.com/products/tidbcloud/), a fully-managed Database-as-a-Service (DBaaS), which offers free trial.

## Step 2. Create a database

1. In the SQL shell, create the `django` database that your application will use:

    {{< copyable "sql" >}}

    ```sql
    CREATE DATABASE django;
    ```

2. Create a SQL user for your application:

    {{< copyable "sql" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    Take note of the username and password. You will use them in your application code when initializing the project.

3. Grant necessary permissions to the SQL user you have just created:

    {{< copyable "sql" >}}

    ```sql
    GRANT ALL ON django.* TO <username>;
    ```

## Step 3. Set virtual environments and initialize the project

1. Use [Poetry](https://python-poetry.org/docs/), a dependency and package manager in Python, to set virtual environments and initialize the project.

    Poetry can isolate system dependencies from other dependencies and avoid dependency pollution. Use the following command to install Poetry.

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2. Initialize the development environment using Poetry:

    {{< copyable "" >}}

    ```bash
    poetry init --no-interaction --dependency django
    poetry run django-admin startproject tidb_example

    mv pyproject.toml ./tidb_example
    cd tidb_example

    poetry add django-tidb

    poetry shell
    ```

3. Modify the configuration file. The configuration in `tidb_example/settings.py` is as follows.

    {{< copyable "" >}}

    ```python
    USE_TZ = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    ```

    Modify the configuration above as follows. This is used for connection to TiDB.

    {{< copyable "" >}}

    ```python
    USE_TZ = False

    DATABASES = {
        'default': {
            'ENGINE': 'django_tidb',
            'NAME': 'django',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': 4000,
        },
    }

    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
    ```

## Step 4. Write the application logic

After you have configured the application's database connection, you can start building out the application. To write the application logic, you need to build the models, build the controller, and define the URL routes.

1. Build models that are defined in a file called `models.py`. You can copy the sample code below and paste it into a new file.

    {{< copyable "" >}}

    ```python
    from django.db import models

    class Orders(models.Model):
        id = models.AutoField(primary_key=True)
        username = models.CharField(max_length=250)
        price = models.FloatField()
    ```

2. Build class-based views in a file called `views.py`. You can copy the sample code below and paste it into a new file.

    {{< copyable "" >}}

    ```python
    from django.http import JsonResponse, HttpResponse
    from django.utils.decorators import method_decorator
    from django.views.generic import View
    from django.views.decorators.csrf import csrf_exempt
    from django.db import Error, OperationalError
    from django.db.transaction import atomic
    from functools import wraps
    import json
    import sys
    import time

    from .models import *

    def retry_on_exception(view, num_retries=3, on_failure=HttpResponse(status=500), delay_=0.5, backoff_=1.5):
        @wraps(view)
        def retry(*args, **kwargs):
            delay = delay_
            for i in range(num_retries):
                try:
                    return view(*args, **kwargs)
                except Exception as e:
                    return on_failure
        return retry


    class PingView(View):
        def get(self, request, *args, **kwargs):
            return HttpResponse("python/django", status=200)


    @method_decorator(csrf_exempt, name='dispatch')
    class OrderView(View):
        def get(self, request, id=None, *args, **kwargs):
            if id is None:
                orders = list(Orders.objects.values())
            else:
                orders = list(Orders.objects.filter(id=id).values())
            return JsonResponse(orders, safe=False)


        @retry_on_exception
        @atomic
        def post(self, request, *args, **kwargs):
            form_data = json.loads(request.body.decode())
            username = form_data['username']
            price = form_data['price']
            c = Orders(username=username, price=price)
            c.save()
            return HttpResponse(status=200)

        @retry_on_exception
        @atomic
        def delete(self, request, id=None, *args, **kwargs):
            if id is None:
                return HttpResponse(status=404)
            Orders.objects.filter(id=id).delete()
            return HttpResponse(status=200)
    ```

3. Define URL routes in a file called `urls.py`. The `django-admin` command-line tool has generated this file when you create the Django project, so the file should already exist in `tidb_example/tidb_example`. You can copy the sample code below and paste it into the existing `urls.py` file.

    {{< copyable "" >}}

    ```python
    from django.contrib import admin
    from django.urls import path
    from django.conf.urls import url

    from .views import OrderView, PingView

    urlpatterns = [
        path('admin/', admin.site.urls),

        url('ping/', PingView.as_view()),

        url('order/', OrderView.as_view(), name='order'),
        url('order/<int:id>/', OrderView.as_view(), name='order'),
    ]
    ```

## Step 5. Set up and run the Django application

In the top `tidb_example` directory, use the [`manage.py`](https://docs.djangoproject.com/en/3.1/ref/django-admin/) script to create [Django migrations](https://docs.djangoproject.com/en/3.1/topics/migrations/) that initialize the database for the application:

{{< copyable "" >}}

```bash
python manage.py makemigrations tidb_example
python manage.py migrate tidb_example
python manage.py migrate
```

Then start the application:

{{< copyable "" >}}

```python
python3 manage.py runserver 0.0.0.0:8000
```

To test the application by inserting some example data, run the following commands:

{{< copyable "" >}}

```bash
curl --request POST '127.0.0.1:8000/order/' \
--data-raw '{
    "uid": 1,
    "price": 3.12
}'

curl --request PATCH '127.0.0.1:8000/order/' --data-raw '{ "oid": 1, "price": 312 }'

curl --request GET '127.0.0.1:8000/order/' --data-raw '{ "oid": 1 }'
```

To verify whether the data insertion is successful, open the terminal with the SQL shell to check:

{{< copyable "" >}}

```sql
MySQL root@127.0.0.1:(none)> select * from django.tidb_example_orders;
+-----+-----+-------+
| oid | uid | price |
+-----+-----+-------+
| 1   | 1   | 312.0 |
+-----+-----+-------+
1 row in set
Time: 0.008s
```

The result above shows that the data insertion is successful. Then you can delete the inserted data:

{{< copyable "" >}}

```bash
curl --request DELETE '127.0.0.1:8000/order/' --data-raw '{ "oid": 1 }'
```
