---
title: Connect to TiDB with Django
summary: Learn how to connect to TiDB using Django. This tutorial gives Python sample code snippets that work with TiDB using Django.
aliases: ['/tidb/dev/dev-guide-outdated-for-django']
---

# Connect to TiDB with Django

TiDB is a MySQL-compatible database, and [Django](https://www.djangoproject.com) is a popular web framework for Python, which includes a powerful Object Relational Mapper (ORM) library.

In this tutorial, you can learn how to use TiDB and Django to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using Django.
- Build and run your application. Optionally, you can find sample code snippets for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted clusters.

## Prerequisites

To complete this tutorial, you need:

- [Python 3.8 or higher](https://www.python.org/downloads/).
- [Git](https://git-scm.com/downloads).
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including Django, django-tidb, and mysqlclient) for the sample app:

```shell
pip install -r requirements.txt
```

If you encounter installation issues with mysqlclient, refer to the [mysqlclient official documentation](https://github.com/PyMySQL/mysqlclient#install).

#### What is `django-tidb`?

`django-tidb` is a TiDB dialect for Django that resolves compatibility issues between TiDB and Django.

To install `django-tidb`, choose a version that matches your Django version. For example, if you are using `django==4.2.*`, install `django-tidb==4.2.*`. The minor version does not need to be the same. It is recommended to use the latest minor version.

For more information, refer to [django-tidb repository](https://github.com/pingcap/django-tidb).

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click **Create password** to create a random password.

    > **Tip:**
    > 
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

    TiDB Serverless requires a secure connection. Since the `ssl_mode` of mysqlclient defaults to `PREFERRED`, you don't need to manually specify `CA_PATH`. Just leave it empty. But if you have a special reason to specify `CA_PATH` manually, you can refer to the [TLS connections to TiDB Serverless](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters) to get the certificate paths for different operating systems.

7. Save the `.env` file.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

5. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog, and configure `CA_PATH` with the certificate path downloaded in the previous step.

6. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

2. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters, and remove the `CA_PATH` line. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

### Step 4: Initialize the database

In the root directory of the project, run the following command to initialize the database:

```shell
python manage.py migrate
```

### Step 5: Run the sample application

1. Run the application in the development mode:

    ```shell
    python manage.py runserver
    ```

    The application runs on port `8000` by default. To use a different port, you can append the port number to the command. The following is an example:

    ```shell
    python manage.py runserver 8080
    ```

2. To access the application, open your browser and go to `http://localhost:8000/`. In the sample application, you can:

    - Create a new player.
    - Bulk create players.
    - View all players.
    - Update a player.
    - Delete a player.
    - Trade goods between two players.

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart) repository.

### Connect to TiDB

In the file `sample_project/settings.py`, add the following configurations:

```python
DATABASES = {
    "default": {
        "ENGINE": "django_tidb",
        "HOST": ${tidb_host},
        "PORT": ${tidb_port},
        "USER": ${tidb_user},
        "PASSWORD": ${tidb_password},
        "NAME": ${tidb_db_name},
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = ${ca_path}
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

You need to replace `${tidb_host}`, `${tidb_port}`, `${tidb_user}`, `${tidb_password}`, `${tidb_db_name}`, and `${ca_path}` with the actual values of your TiDB cluster.

### Define the data model

```python
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    coins = models.IntegerField(default=100)
    goods = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

For more information, refer to [Django models](https://docs.djangoproject.com/en/dev/topics/db/models/).

### Insert data

```python
# insert a single object
player = Player.objects.create(name="player1", coins=100, goods=1)

# bulk insert multiple objects
Player.objects.bulk_create([
    Player(name="player1", coins=100, goods=1),
    Player(name="player2", coins=200, goods=2),
    Player(name="player3", coins=300, goods=3),
])
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

```python
# get a single object
player = Player.objects.get(name="player1")

# get multiple objects
filtered_players = Player.objects.filter(name="player1")

# get all objects
all_players = Player.objects.all()
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

```python
# update a single object
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# update multiple objects
Player.objects.filter(coins=100).update(coins=200)
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

```python
# delete a single object
player = Player.objects.get(name="player1")
player.delete()

# delete multiple objects
Player.objects.filter(coins=100).delete()
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Next steps

- Learn more usage of Django from [the documentation of Django](https://www.djangoproject.com/).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).
