---
title: 使用 Django 构建 TiDB 应用程序
summary: 给出一个 Django 构建 TiDB 应用程序示例。
aliases: ['/zh/tidb/dev/dev-guide-sample-application-django']
---

<!-- markdownlint-disable MD029 -->

# 使用 Django 构建 TiDB 应用程序

本文档将展示如何使用 [Django](https://www.djangoproject.com/) 构建一个 TiDB Web 应用程序。使用 [django-tidb](https://github.com/pingcap/django-tidb) 模块作为数据访问能力的框架。示例应用程序的代码可从 [Github](https://github.com/pingcap-inc/tidb-example-python) 下载。

这是一个较为完整的构建 Restful API 的示例应用程序，展示了一个使用 TiDB 作为数据库的通用 Django 后端服务。该示例设计了以下过程，用于还原一个现实场景：

这是一个关于游戏的例子，每个玩家有两个属性：金币数 `coins` 和货物数 `goods`。且每个玩家都拥有一个字段 `id`，作为玩家的唯一标识。玩家在金币数和货物数充足的情况下，可以自由地交易。

你可以以此示例为基础，构建自己的应用程序。

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

**使用 TiDB Serverless 集群**

详细步骤，请参考：[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)。

**使用本地集群**

详细步骤，请参考：[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)。

## 第 2 步：安装 Python

请在你的计算机上下载并安装 **Python**。本文的示例使用 [Django 3.2.16](https://docs.djangoproject.com/zh-hans/3.2/) 版本。根据 [Django 文档](https://docs.djangoproject.com/zh-hans/3.2/faq/install/#what-python-version-can-i-use-with-django)，Django 3.2.16 版本支持 Python 3.6、3.7、3.8、3.9 和 3.10 版本，推荐使用 Python 3.10 版本。

## 第 3 步：获取应用程序代码

> **建议：**
>
> 如果你希望得到一个与本示例相同依赖的空白程序，而无需示例代码，可参考[创建相同依赖空白程序（可选）](#创建相同依赖空白程序可选)一节。

请下载或克隆示例代码库 [pingcap-inc/tidb-example-python](https://github.com/pingcap-inc/tidb-example-python)，并进入到目录 `django_example` 中。

## 第 4 步：运行应用程序

接下来运行应用程序代码，将会生成一个 Web 应用程序。你可以使用 `python manage.py migrate` 命令，要求 Django 在数据库 `django` 中创建一个表 `player`。如果你向应用程序的 Restful API 发送请求，这些请求将会在 TiDB 集群上运行[数据库事务](/develop/dev-guide-transaction-overview.md)。

如果你想了解有关此应用程序的代码的详细信息，可参阅[实现细节](#实现细节)部分。

### 第 4 步第 1 部分：TiDB Cloud 更改参数

若你使用了 TiDB Serverless 集群，此处需使用系统本地的 CA 证书，并将证书路径记为 `<ca_path>` 以供后续指代。你可以参考 [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system) 文档获取你所使用的操作系统的 CA 证书位置。

更改 `example_project/settings.py` 中的 `DATABASES` 参数：

```python
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
```

若你设定的密码为 `123456`，而且从 TiDB Serverless 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

下面以 macOS 为例，应将参数更改为：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tidb',
        'NAME': 'django',
        'USER': '2aEp24QWEDLqRFs.root',
        'PASSWORD': '123456',
        'HOST': 'xxx.tidbcloud.com',
        'PORT': 4000,
        'OPTIONS': {
            'ssl': {
                "ca": "<ca_path>"
            },
        },
    },
}
```

### 第 4 步第 2 部分：运行

1. 打开终端，进入 `tidb-example-python` 代码示例目录：

    ```bash
    cd <path>/tidb-example-python
    ```

2. 安装项目依赖并进入 `django_example` 目录：

    ```bash
    pip install -r requirement.txt
    cd django_example
    ```

3. 运行数据模型迁移：

    > **注意：**
    >
    > - 此步骤假定已经存在 `django` 数据库。
    > - 若未创建 `django` 数据库，可通过 `CREATE DATABASE django` 语句进行创建。关于创建数据库语句的详细信息，参考 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md#create-database)。
    > - 数据库名称 `NAME` 可在 `example_project/settings.py` 的 `DATABASES` 属性中更改。

    这将在你连接的数据库内生成 Django 所需的相应数据表。

    ```bash
    python manage.py migrate
    ```

4. 运行应用程序：

    ```bash
    python manage.py runserver
    ```

### 第 4 步第 3 部分：输出

输出的最后部分应如下所示：

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
December 12, 2022 - 08:21:50
Django version 3.2.16, using settings 'example_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

如果你想了解有关此应用程序的代码的详细信息，可参阅[实现细节](#实现细节)部分。

## 第 5 步：HTTP 请求

在运行应用程序后，你可以通过访问根地址 `http://localhost:8000` 向后端程序发送 HTTP 请求。下面将给出一些示例请求来演示如何使用该服务。

<SimpleTab groupId="request">

<div label="使用 Postman（推荐）" value="postman">

1. 将配置文件 [`Player.postman_collection.json`](https://raw.githubusercontent.com/pingcap-inc/tidb-example-python/main/django_example/Player.postman_collection.json) 导入 [Postman](https://www.postman.com/)。

2. 导入后 **Collections** > **Player** 如图所示：

    ![postman import](/media/develop/postman_player_import.png)

3. 发送请求：

    - 增加玩家

        点击 **Create** 标签，点击 **Send** 按钮，发送 `POST` 形式的 `http://localhost:8000/player/` 请求。返回值为增加的玩家个数，预期为 1。

    - 使用 ID 获取玩家信息

        点击 **GetByID** 标签，点击 **Send** 按钮，发送 `GET` 形式的 `http://localhost:8000/player/1` 请求。返回值为 ID 为 1 的玩家信息。

    - 使用 Limit 批量获取玩家信息

        点击 **GetByLimit** 标签，点击 **Send** 按钮，发送 `GET` 形式的 `http://localhost:8000/player/limit/3` 请求。返回值为最多 3 个玩家的信息列表。

    - 获取玩家个数

        点击 **Count** 标签，点击 **Send** 按钮，发送 `GET` 形式的 `http://localhost:8000/player/count` 请求。返回值为玩家个数。

    - 玩家交易

        点击 **Trade** 标签，点击 **Send** 按钮，发送 `POST` 形式的 `http://localhost:8000/player/trade` 请求。请求参数为售卖玩家 ID `sellID`、购买玩家 ID `buyID`、购买货物数量 `amount` 以及购买消耗金币数 `price`。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功。并且由于[数据库事务](/develop/dev-guide-transaction-overview.md)保证，不会有玩家的金币或货物丢失的情况。

</div>

<div label="使用 curl" value="curl">

下面使用 curl 请求服务端。

- 增加玩家

    使用 `POST` 方法向 `/player` 端点发送请求来增加玩家，例如：

    ```shell
    curl --location --request POST 'http://localhost:8000/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
    ```

    这里使用 JSON 作为信息的载荷。表示需要创建一个金币数 `coins` 为 100，货物数 `goods` 为 20 的玩家。返回值为创建的玩家信息：

    ```
    create 1 players.
    ```

- 使用 ID 获取玩家信息

    使用 `GET` 方法向 `/player` 端点发送请求来获取玩家信息。此外，还需要在路径上给出玩家的 ID 参数，即 `/player/{id}`。例如，在请求 ID 为 1 的玩家时：

    ```shell
    curl --location --request GET 'http://localhost:8000/player/1'
    ```

    返回值为 ID 为 1 的玩家的信息：

    ```json
    {
    "coins": 200,
    "goods": 10,
    "id": 1
    }
    ```

- 使用 Limit 批量获取玩家信息

    使用 `GET` 方法向 `/player/limit` 端点发送请求来获取玩家信息。此外，还需要在路径上给出限制查询的玩家信息的总数，即 `/player/limit/{limit}`。例如，在请求最多 3 个玩家的信息时：

    ```shell
    curl --location --request GET 'http://localhost:8000/player/limit/3'
    ```

    返回值为玩家信息的列表：

    ```json
    [
    {
        "coins": 200,
        "goods": 10,
        "id": 1
    },
    {
        "coins": 0,
        "goods": 30,
        "id": 2
    },
    {
        "coins": 100,
        "goods": 20,
        "id": 3
    }
    ]
    ```

- 获取玩家个数

    使用 `GET` 方法向 `/player/count` 端点发送请求来获取玩家个数：

    ```shell
    curl --location --request GET 'http://localhost:8000/player/count'
    ```

    返回值为玩家个数：

    ```
    4
    ```

- 玩家交易

    使用 `POST` 方法向 `/player/trade` 端点发送请求来发起玩家间的交易，例如：

    ```shell
    curl --location --request POST 'http://localhost:8000/player/trade' \
    --header 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'sellID=1' \
    --data-urlencode 'buyID=2' \
    --data-urlencode 'amount=10' \
    --data-urlencode 'price=100'
    ```

    这里使用 Form Data 作为信息的载荷。表示售卖玩家 ID `sellID` 为 1、购买玩家 ID `buyID` 为 2、购买货物数量 `amount` 为 10、购买消耗金币数 `price` 为 100。

    返回值为交易是否成功：

    ```
    true
    ```

    当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功。并且由于[数据库事务](/develop/dev-guide-transaction-overview.md)保证，不会有玩家的金币或货物丢失的情况。

</div>

<div label="使用 Shell 脚本" value="shell">

为方便测试，你可以使用 [`request.sh`](https://github.com/pingcap-inc/tidb-example-python/blob/main/django_example/request.sh) 脚本依次发送以下请求：

1. 循环创建 10 名玩家
2. 获取 ID 为 1 的玩家信息
3. 获取至多 3 名玩家信息列表
4. 获取玩家总数
5. ID 为 1 的玩家作为售出方，ID 为 2 的玩家作为购买方，购买 10 个货物，耗费 100 金币

使用 `./request.sh` 命令运行此脚本，运行结果如下所示：

```shell
> ./request.sh
loop to create 10 players:
create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.create 1 players.

get player 1:
{"id": 1, "coins": 100, "goods": 20}

get players by limit 3:
[{"id": 1, "coins": 100, "goods": 20}, {"id": 2, "coins": 100, "goods": 20}, {"id": 3, "coins": 100, "goods": 20}]

get players count:
10

trade by two players:
trade successful
```

</div>

</SimpleTab>

## 实现细节

本小节介绍示例应用程序项目中的组件。

### 总览

本示例项目的目录树大致如下所示：

```
.
├── example_project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── player
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── manage.py
```

其中：

- 每一个文件夹中的 `__init__.py` 文件声明了该文件夹是一个 Python 包。
- `manage.py` 为 Django 自动生成的用于管理项目的脚本。
- `example_project` 包含项目级别的代码：

    - `settings.py` 声明了项目的配置，如数据库地址、密码、使用的数据库方言等。
    - `urls.py` 配置了项目的根路由。

- `player` 是项目中提供对 `Player` 数据模型管理、数据查询的包，这在 Django 中被称为应用。你可以使用 `python manage.py startapp player` 来创建一个空白的 `player` 应用。

    - `models.py` 定义了 `Player` 数据模型。
    - `migrations` 是一组数据模型迁移脚本。你可以使用 `python manage.py makemigrations player` 命令自动分析 `models.py` 文件中定义的数据对象，并生成迁移脚本。
    - `urls.py` 定义了应用的路由。
    - `views.py` 提供了应用的逻辑代码。

> **注意：**
>
> 由于 Django 的设计采用了可插拔模式，因此，你需要在创建应用后，在项目中进行注册。在本示例中，注册过程就是在 `example_project/settings.py` 文件中，在 `INSTALLED_APPS` 对象内添加 `'player.apps.PlayerConfig'` 条目。你可以参考示例代码 [`settings.py`](https://github.com/pingcap-inc/tidb-example-python/blob/main/django_example/example_project/settings.py#L33-L41) 以获得更多信息。

### 项目配置

本节将简要介绍 `example_project` 包内 `settings.py` 的重要配置。这个文件包含了 Django 项目的配置，声明了项目包含的应用、中间件、连接的数据库等信息。你可以通过[创建相同依赖空白程序](#创建相同依赖空白程序可选)这一节来了解此配置文件的生成流程，也可直接在项目中使用 `settings.py` 文件。关于 Django 配置的更多信息，参考 [Django 配置](https://docs.djangoproject.com/zh-hans/3.2/topics/settings/)文档。

```python
...

# Application definition

INSTALLED_APPS = [
    'player.apps.PlayerConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

...

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

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

...
```

其中：

- `INSTALLED_APPS`：启用的应用全限定名称列表。
- `MIDDLEWARE`：启用的中间件列表。由于本示例无需 `CsrfViewMiddleware` 中间件，因此其被注释。
- `DATABASES`：数据库配置。其中，`ENGINE` 一项被配置为 `django_tidb`，这遵循了 [django-tidb](https://github.com/pingcap/django-tidb) 的配置要求。

### 根路由

在 `example_project` 包中的 `urls.py` 文件中编写了根路由：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('player/', include('player.urls')),
    path('admin/', admin.site.urls),
]
```

在上面的示例中，根路由将 `player/` 路径指向 `player.urls`。即，`player` 包下的 `urls.py` 将负责处理所有以 `player/` 开头的 URL 请求。关于更多 Django URL 调度器的信息，请参考 [Django URL 调度器](https://docs.djangoproject.com/zh-hans/3.2/topics/http/urls/)文档。

### player 应用

`player` 应用实现了对 `Player` 对象的数据模型迁移、对象持久化、接口实现等功能。

#### 数据模型

`models.py` 文件内包含 `Player` 数据模型，这个模型对应了数据库的一张表。

```python
from django.db import models

# Create your models here.


class Player(models.Model):
    id = models.AutoField(primary_key=True)
    coins = models.IntegerField()
    goods = models.IntegerField()

    objects = models.Manager()

    class Meta:
        db_table = "player"

    def as_dict(self):
        return {
            "id": self.id,
            "coins": self.coins,
            "goods": self.goods,
        }
```

在上面的示例中，数据模型中有一个子类 `Meta`，这些子类给了 Django 额外的信息，用以指定数据模型的元信息。其中，`db_table` 声明此数据模型对应的表名为 `player`。关于模型元信息的全部选项可查看 [Django 模型 Meta 选项](https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/)文档。

此外，数据模型中定义了 `id`、`coins` 及 `goods` 三个属性：

- `id`：`models.AutoField(primary_key=True)` 表示其为一个自动递增的主键。
- `coins`：`models.IntegerField()` 表示其为一个 Integer 类型的字段。
- `goods`：`models.IntegerField()` 表示其为一个 Integer 类型的字段。

关于数据模型的详细信息，可查看 [Django 模型](https://docs.djangoproject.com/zh-hans/3.2/topics/db/models/)文档。

#### 数据模型迁移

Django 以 Python 数据模型定义代码为依赖，对数据库模型进行迁移。因此，它会生成一系列数据库模型迁移脚本，用于解决代码与数据库之间的差异。在 `models.py` 中定义完 `Player` 数据模型后，你可以使用 `python manage.py makemigrations player` 生成迁移脚本。在本文示例中，`migrations` 包内的 `0001_initial.py` 就是自动生成的迁移脚本。

```python
# Generated by Django 3.2.16 on 2022-11-16 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('coins', models.IntegerField()),
                ('goods', models.IntegerField()),
            ],
            options={
                'db_table': 'player',
            },
        ),
    ]
```

你可以使用 `python manage.py sqlmigrate ...` 来预览迁移脚本最终将运行的 SQL 语句。这将极大地减少迁移脚本运行你意料之外的 SQL 语句的可能性。在生成迁移脚本后，推荐至少使用一次此命令预览并仔细检查生成的 SQL 语句。在本示例中，你可以运行 `python manage.py sqlmigrate player 0001`，其输出为可读的 SQL 语句，有助于开发者对语句进行审核：

```sql
--
-- Create model Player
--
CREATE TABLE `player` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `coins` integer NOT NULL, `goods` integer NOT NULL);
```

生成迁移脚本后，你可以使用 `python manage.py migrate` 实施数据迁移。此命令拥有幂等性，其运行后将在数据库内保存一条运行记录以完成幂等保证。因此，你可以多次运行此命令，而无需担心重复运行 SQL 语句。

#### 应用路由

在[根路由](#根路由)一节中，示例程序将 `player/` 路径指向了 `player.urls`。本节将展开叙述 `player` 包下的 `urls.py` 应用路由：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.create, name='create'),
    path('count', views.count, name='count'),
    path('limit/<int:limit>', views.limit_list, name='limit_list'),
    path('<int:player_id>', views.get_by_id, name='get_by_id'),
    path('trade', views.trade, name='trade'),
]
```

应用路由注册了 5 个路径：

- `''`：被指向了 `views.create` 函数。
- `'count'`：被指向了 `views.count` 函数。
- `'limit/<int:limit>'`：被指向了 `views.limit_list` 函数。此处路径包含一个 `<int:limit>` 路径变量，其中：

    - `int` 是指这个参数其将被验证是否为 `int` 类型。
    - `limit` 是指此参数的值将被映射至名为 `limit` 的函数入参中。

- `'<int:player_id>'`：被指向了 `views.get_by_id` 函数，此处路径包含一个 `<int:player_id>` 路径变量。
- `'trade'`：被指向了 `views.trade` 函数。

此外，应用路由是根路由转发而来的，因此将在 URL 匹配时包含根路由配置的路径。如上面示例所示，根路由配置为 `player/` 转发至此应用路由，那么，应用路由中的：

- `''` 在实际的请求中为 `http(s)://<host>(:<port>)/player`。
- `'count'` 在实际的请求中为 `http(s)://<host>(:<port>)/player/count`。
- `'limit/<int:limit>'` 以 `limit` 为 `3` 为例，在实际的请求中为 `http(s)://<host>(:<port>)/player/limit/3`。

#### 逻辑实现

逻辑实现代码，在 `player` 包下的 `views.py` 内，这在 Django 中被称为视图。关于 Django 视图的更多信息，参考 [Django 视图](https://docs.djangoproject.com/zh-hans/3.2/topics/http/views/)文档。

```python
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import *
from .models import Player
import json


@require_POST
def create(request):
    dict_players = json.loads(request.body.decode('utf-8'))
    players = list(map(
        lambda p: Player(
            coins=p['coins'],
            goods=p['goods']
        ), dict_players))
    result = Player.objects.bulk_create(objs=players)
    return HttpResponse(f'create {len(result)} players.')


@require_GET
def count(request):
    return HttpResponse(Player.objects.count())


@require_GET
def limit_list(request, limit: int = 0):
    if limit == 0:
        return HttpResponse("")
    players = set(Player.objects.all()[:limit])
    dict_players = list(map(lambda p: p.as_dict(), players))
    return JsonResponse(dict_players, safe=False)


@require_GET
def get_by_id(request, player_id: int):
    result = get_object_or_404(Player, pk=player_id).as_dict()
    return JsonResponse(result)


@require_POST
@transaction.atomic
def trade(request):
    sell_id, buy_id, amount, price = int(request.POST['sellID']), int(request.POST['buyID']), \
                                     int(request.POST['amount']), int(request.POST['price'])
    sell_player = Player.objects.select_for_update().get(id=sell_id)
    if sell_player.goods < amount:
        raise Exception(f'sell player {sell_player.id} goods not enough')

    buy_player = Player.objects.select_for_update().get(id=buy_id)
    if buy_player.coins < price:
        raise Exception(f'buy player {buy_player.id} coins not enough')

    Player.objects.filter(id=sell_id).update(goods=F('goods') - amount, coins=F('coins') + price)
    Player.objects.filter(id=buy_id).update(goods=F('goods') + amount, coins=F('coins') - price)

    return HttpResponse("trade successful")
```

下面将逐一解释代码中的重点部分：

- 装饰器：

    - `@require_GET`：代表此函数仅接受 `GET` 类型的 HTTP 请求。
    - `@require_POST`：代表此函数仅接受 `POST` 类型的 HTTP 请求。
    - `@transaction.atomic`：代表此函数内的所有数据库操作将被包含于同一个事务中运行。关于在 Django 中使用事务的更多信息，可参考 [Django 数据库事务](https://docs.djangoproject.com/zh-hans/3.2/topics/db/transactions/)文档。关于 TiDB 中事物的详细信息，可参考 [TiDB 事务概览](/develop/dev-guide-transaction-overview.md)。

- `create` 函数：

    - 获取 `request` 对象中 `body` 的 Payload，并用 `utf-8` 解码：

        ```python
        dict_players = json.loads(request.body.decode('utf-8'))
        ```

    - 使用 lambda 中的 `map` 函数，将 dict 类型的 `dict_players` 对象转换为 `Player` 数据模型的列表：

        ```python
        players = list(map(
            lambda p: Player(
                coins=p['coins'],
                goods=p['goods']
            ), dict_players))
        ```

    - 调用 `Player` 数据模型的 `bulk_create` 函数，批量添加 `players` 列表，并返回添加的数据条目：

        ```python
        result = Player.objects.bulk_create(objs=players)
        return HttpResponse(f'create {len(result)} players.')
        ```

- `count` 函数：调用 `Player` 数据模型的 `count` 函数，并返回所有的数据条目。
- `limit_list` 函数：

    - 短路逻辑，`limit` 为 `0` 时不发送数据库请求：

        ```python
        if limit == 0:
            return HttpResponse("")
        ```

    - 调用 `Player` 数据模型的 `all` 函数，并使用切片操作符获取前 `limit` 个数据。需要注意的是，Django 不是获取所有数据并在内存中切分前 `limit` 个数据，而是在使用时请求数据库的前 `limit` 个数据。这是由于 Django 重写了切片操作符，并且 QuerySet 对象是**惰性**的。这意味着对一个未执行的 QuerySet 进行切片，将继续返回一个未执行的 QuerySet，直到你第一次真正的请求 QuerySet 内的数据。例如此处使用 `set` 函数对其进行迭代并返回整个集合。关于 Django QuerySet 的更多信息，你可以参考 [Django QuerySet API](https://docs.djangoproject.com/zh-hans/3.2/ref/models/querysets/) 文档。

        ```python
        players = set(Player.objects.all()[:limit])
        ```

    - 将返回的 `Player` 数据模型的列表，转为对象为 dict 的列表，并使用 `JsonResponse` 输出。

        ```python
        dict_players = list(map(lambda p: p.as_dict(), players))
        return JsonResponse(dict_players, safe=False)
        ```

- `get_by_id` 函数：

    - 使用 `get_object_or_404` 语法糖传入 `player_id`，并将 `Player` 对象转为 dict。如数据不存在，将由此函数返回 `404` 状态码：

        ```python
        result = get_object_or_404(Player, pk=player_id).as_dict()
        ```

    - 使用 `JsonResponse` 返回数据：

        ```python
        return JsonResponse(result)
        ```

- `trade` 函数：

    - 从 `POST` Payload 中接收 Form 形式的数据：

        ```python
        sell_id, buy_id, amount, price = int(request.POST['sellID']), int(request.POST['buyID']), \
                                        int(request.POST['amount']), int(request.POST['price'])
        ```

    - 调用 `Player` 数据模型的 `select_for_update` 函数对卖家和买家的数据进行加锁，并检查卖家的货物数量和买家的货币数量是否足够。该函数使用了 `@transaction.atomic` 装饰器，任意异常都会导致事务回滚。可以利用这个机制，在任意检查失败的时候，抛出异常，由 Django 进行事务回滚。

        ```python
        sell_player = Player.objects.select_for_update().get(id=sell_id)
        if sell_player.goods < amount:
            raise Exception(f'sell player {sell_player.id} goods not enough')

        buy_player = Player.objects.select_for_update().get(id=buy_id)
        if buy_player.coins < price:
            raise Exception(f'buy player {buy_player.id} coins not enough')
        ```

    - 更新卖家与买家的数据。由于这里使用了 `@transaction.atomic` 装饰器，任何异常都将由 Django 回滚事务。因此，请不要在此处使用 `try-except` 语句进行异常处理。如果一定需要处理，请在 except 块中将异常继续抛向上层，以防止因 Django 误认为函数运行正常而提交事务，导致数据错误。

        ```python
        Player.objects.filter(id=sell_id).update(goods=F('goods') - amount, coins=F('coins') + price)
        Player.objects.filter(id=buy_id).update(goods=F('goods') + amount, coins=F('coins') - price)
        ```

    - 返回交易成功字符串，因为其他情况将导致异常抛出返回：

        ```python
        return HttpResponse("trade successful")
        ```

## 创建相同依赖空白程序（可选）

本程序使用 Django Admin CLI [django-admin](https://django-admin-cli.readthedocs.io/en/stable/index.html) 构建。你可以安装并使用 `django-admin` 来快速完成 Django 项目的初始化。如果需要快速获得与示例程序 `django_example` 相同的可运行空白应用程序，可以按照以下步骤操作：

1. 初始化 Django 项目 `copy_django_example`：

    ```bash
    pip install -r requirement.txt
    django-admin startproject copy_django_example
    cd copy_django_example
    ```

2. 更改 `DATABASES` 配置：

    1. 打开 `copy_django_example/settings.py` 配置文件
    2. 将 `DATABASES` 部分从指向本地 SQLite 的配置更改为 TiDB 集群的信息：

        ```python
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

    3. 由于本示例不需要跨域校验，因此你需要注释或删除 `MIDDLEWARE` 中的 `CsrfViewMiddleware`。修改后的 `MIDDLEWARE` 为：

        ```python
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            # 'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        ```

至此，你已经完成了一个空白的应用程序，此应用程序与示例应用程序的依赖完全相同。如果需要进一步了解 Django 的使用方法，参考：

- [Django 文档](https://docs.djangoproject.com/zh-hans/3.2/)
- [Django 入门教程](https://docs.djangoproject.com/zh-hans/3.2/intro/tutorial01/)