---
title: 使用 Django 构建 TiDB 应用程序
summary: 给出一个 Django 构建 TiDB 应用程序示例。
---

<!-- markdownlint-disable MD029 -->

# 使用 Django 构建 TiDB 应用程序

本教程向你展示如何使用 TiDB 构建 [Django](https://www.djangoproject.com/) Web 应用程序。使用 [django-tidb](https://github.com/pingcap/django-tidb) 模块作为数据访问能力的框架。此示例应用程序的代码仓库可在 [Github](https://github.com/pingcap-inc/tidb-example-python) 下载。

这是一个较为完整的构建 Restful API 的示例应用程序，展示了一个使用 **TiDB** 作为数据库的通用 **Django** 后端服务。设计了以下过程，用于还原一个现实场景：

这是一个关于游戏的例子，每个玩家有两个属性：金币数 `coins` 和货物数 `goods`。且每个玩家都拥有一个字段 `id`，作为玩家的唯一标识。玩家在金币数和货物数充足的情况下，可以自由的交易。

你可以以此示例为基础，构建自己的应用程序。

> **建议：**
>
> 在[云原生开发环境](/develop/dev-guide-playground-gitpod.md)中尝试 Django 构建 TiDB 应用程序。
> 预配置完成的环境，自动启动 TiDB 集群，获取和运行代码，只需要一个链接。
>
> [现在就试试](https://gitpod.io/#/https://github.com/pingcap-inc/tidb-example-python)

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

### 使用 TiDB Cloud Serverless Tier 集群

[创建 Serverless Tier 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-serverless-tier-集群)

### 使用本地集群

此处将简要叙述启动一个测试集群的过程，若需查看正式环境集群部署，或查看更详细的部署内容，请查阅[本地启动 TiDB](/quick-start-with-tidb.md)。

**部署本地测试集群**

适用场景：利用本地 macOS 或者单机 Linux 环境快速部署 TiDB 测试集群，体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行

1. 下载并安装 TiUP。

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 声明全局环境变量。

    > **注意：**
    >
    > TiUP 安装完成后会提示对应 profile 文件的绝对路径。在执行以下 source 命令前，需要根据 profile 文件的实际位置修改命令。

    ```shell
    source .bash_profile
    ```

3. 在当前 session 执行以下命令启动集群。

    - 直接执行`tiup playground` 命令会运行最新版本的 TiDB 集群，其中 TiDB、TiKV、PD 和 TiFlash 实例各 1 个：

        ```shell
        tiup playground
        ```

    - 也可以指定 TiDB 版本以及各组件实例个数，命令类似于：

        ```shell
        tiup playground v5.4.0 --db 2 --pd 3 --kv 3
        ```

    上述命令会在本地下载并启动某个版本的集群（例如 v5.4.0）。最新版本可以通过执行`tiup list tidb` 来查看。运行结果将显示集群的访问方式：

    ```
    CLUSTER START SUCCESSFULLY, Enjoy it ^-^
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4001 -u root -p (no password)
    To connect TiDB: mysql --comments --host 127.0.0.1 --port 4000 -u root -p (no password)
    To view the dashboard: http://127.0.0.1:2379/dashboard
    PD client endpoints: [127.0.0.1:2379 127.0.0.1:2382 127.0.0.1:2384]
    To view the Prometheus: http://127.0.0.1:9090
    To view the Grafana: http://127.0.0.1:3000
    ```

> **注意：**
>
> - 支持 v5.2.0 及以上版本的 TiDB 在 Apple M1 芯片的机器上运行 `tiup playground`。
> - 以这种方式执行的 playground，在结束部署测试后 TiUP 会清理掉原集群数据，重新执行该命令后会得到一个全新的集群。
> - 若希望持久化数据，可以执行 TiUP 的 `--tag` 参数：`tiup --tag <your-tag> playground ...`，详情参考 [TiUP 参考手册](/tiup/tiup-reference.md#-t---tag-string)。

## 第 2 步：安装 Python

请在你的计算机上下载并安装 **Python**。我们将使用 **[Django 3.2.16](https://github.com/pingcap-inc/tidb-example-python/blob/main/requirement.txt#L2)** 版本完成此示例，依照 [Django 文档](https://docs.djangoproject.com/en/4.1/faq/install/#what-python-version-can-i-use-with-django)，其在 3.2.16 版本中支持版本为 **3.6, 3.7, 3.8, 3.9, 3.10 (added in 3.2.9)** 的 Python 环境，推荐使用 Python 3.10 版本 。

## 第 3 步：获取应用程序代码

请下载或克隆[示例代码库](https://github.com/pingcap-inc/tidb-example-python)，并进入到目录`django_example`中。

### 创建相同依赖空白程序（可选）

本程序使用 **django-admin** 构建。你可以安装并使用这个 CLI 工具来快速完成 Django 项目的初始化。如你需要快速得到一个与 **django_example** 示例程序相同依赖的可运行空白应用程序，你可以跟随如下步骤：

1. 初始化

    ```bash
    pip install -r requirement.txt
    django-admin startproject copy_django_example
    cd copy_django_example
    ```

2. 更改配置

    1. 请进入当前文件夹内 `copy_django_example/settings.py`.
    2. 请更改 `DATABASES` 部分内容：

        从原本指向本地的 SQLite 的配置：

        ```python
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
        ```

        更改为：

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

    3. 此外，我们不需要跨域校验，请将 `MIDDLEWARE` 中的 `CsrfViewMiddleware` 进行注释或删除：

        即，将：

        ```python
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]
        ```

        改为：

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

至此，你已经完成了一个空白的应用程序，此应用程序与示例应用程序的依赖完全相同。其他关于 Django 的使用方法，可参考：

- [Django 文档（中文版）](https://docs.djangoproject.com/zh-hans/3.2/)
- [Django 入门 Tutorial（中文版）](https://docs.djangoproject.com/zh-hans/3.2/intro/tutorial01/)

## 第 4 步：运行应用程序

此处对应用程序代码进行运行，将产生一个 Web 应用程序。你可以在使用 `python manage.py migrate` 命令，要求 Django 创建一个在数据库 `django` 内的表 `player`。如果你想应用程序的 Restful API 进行请求，这些请求将会在 TiDB 集群上运行[数据库事务](/develop/dev-guide-transaction-overview.md)。

如果你想了解有关此应用程序的代码的详细信息，可参阅本教程下方的[实现细节](#实现细节)。

### 第 4 步第 1 部分：TiDB Cloud 更改参数

若你使用 TiDB Cloud Serverless Tier 集群，更改 `settings.py`（位于 `example_project` 内）关于 `DATABASES` 的参数：

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

若你设定的密码为 `123456`，而且从 TiDB Cloud Serverless Tier 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

另外，由于 TiDB Cloud Serverless Tier 需要使用 SSL 连接。因此，CA 证书路径是必要的。你可以在 [Where is the CA root path on my system?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system) 一节中得到建议。

此处将以 MacOS 为例，应将参数更改为：

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
                "ca": "/etc/ssl/cert.pem"
            },
        },
    },
}
```

### 第 4 步第 2 部分：运行

打开终端，确保你已经进入 tidb-example-python 目录，若还未在此目录，请使用命令进入：

```shell
cd <path>/tidb-example-python
```

#### 安装依赖并进入目录

```bash
pip install -r requirement.txt
cd django_example
```

#### 运行数据模型迁移

> **提示：**
>
> - 此步骤假定已经存在 `django` 数据库。
> - 若未创建此数据库，可通过 `CREATE DATABASE django` 语句进行创建，可在 [CREATE DATABASE](/sql-statements/sql-statement-create-database.md#create-database) 页面获取更多关于创建数据库语句的信息。
> - 数据库名 `NAME` 可在 `settings.py`（位于 `example_project` 内）的 `DATABASES` 属性中更改。

这将在你连接的数据库内生成 Django 所需的相应数据表。

```bash
python3 manage.py migrate
```

#### 运行应用程序

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

如果你想了解有关此应用程序的代码的详细信息，可参阅本教程下方的[实现细节](#实现细节)。

## 第 5 步：HTTP 请求

服务完成运行后，即可使用 HTTP 接口请求后端程序。`http://localhost:8000` 是服务提供根地址。此处使用一系列的 HTTP 请求来演示如何使用该服务。

### 第 6 步第 1 部分：使用 Postman 请求(推荐)

你可下载[此配置文件](https://raw.githubusercontent.com/pingcap-inc/tidb-example-python/main/django_example/Player.postman_collection.json)到本地，并导入 [Postman](https://www.postman.com/)，导入后如图所示：

![postman import](/media/develop/IMG_20220402-003303222.png)

#### 增加玩家

点击 **Create** 标签，点击 **Send** 按钮，发送 Post 形式的 `http://localhost:8000/player/` 请求。返回值为增加的玩家个数信息，预期为 1。

#### 使用 ID 获取玩家信息

点击 **GetByID** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/1` 请求。返回值为 ID 为 1 的玩家信息。

#### 使用 Limit 批量获取玩家信息

点击 **GetByLimit** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/limit/3` 请求。返回值为最多 3 个玩家的信息列表。

#### 获取玩家个数

点击 **Count** 标签，点击 **Send** 按钮，发送 Get 形式的 `http://localhost:8000/player/count` 请求。返回值为玩家个数。

#### 玩家交易

点击 **Trade** 标签，点击 **Send** 按钮，发送 Post 形式的 `http://localhost:8000/player/trade` 请求，请求参数为售卖玩家 ID `sellID`、购买玩家 ID `buyID`、购买货物数量 `amount`、购买消耗金币数 `price`。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功，且由于[数据库事务](/develop/dev-guide-transaction-overview.md)保证，不会有玩家的金币或货物丢失的情况。

### 第 6 步第 2 部分：使用 curl 请求

当然，你也可以直接使用 curl 进行请求。

#### 增加玩家

使用 **Post** 方法请求 `/player` 端点请求来增加玩家，即：

```shell
curl --location --request POST 'http://localhost:8000/player/' --header 'Content-Type: application/json' --data-raw '[{"coins":100,"goods":20}]'
```

这里使用 JSON 作为信息的载荷。表示需要创建一个金币数 `coins` 为 100，货物数 `goods` 为 20 的玩家。返回值为创建的玩家信息。

```json
create 1 players.
```

#### 使用 ID 获取玩家信息

使用 **Get** 方法请求 `/player` 端点请求来获取玩家信息，额外的需要在路径上给出玩家的 `id` 参数，即 `/player/{id}` ，例如在请求 `id` 为 1 的玩家时：

```shell
curl --location --request GET 'http://localhost:8000/player/1'
```

返回值为玩家的信息：

```json
{
  "coins": 200,
  "goods": 10,
  "id": 1
}
```

#### 使用 Limit 批量获取玩家信息

使用 **Get** 方法请求 `/player/limit` 端点请求来获取玩家信息，额外的需要在路径上给出限制查询的玩家信息的总数，即 `/player/limit/{limit}` ，例如在请求最多 3 个玩家的信息时：

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

#### 获取玩家个数

使用 **Get** 方法请求 `/player/count` 端点请求来获取玩家个数：

```shell
curl --location --request GET 'http://localhost:8000/player/count'
```

返回值为玩家个数

```json
4
```

#### 玩家交易

使用 **Post** 方法请求 `/player/trade` 端点请求来发起玩家间的交易，即：

```shell
curl --location --request POST 'http://localhost:8000/player/trade' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'sellID=1' \
  --data-urlencode 'buyID=2' \
  --data-urlencode 'amount=10' \
  --data-urlencode 'price=100'
```

这里使用 **Form Data** 作为信息的载荷。表示售卖玩家 ID `sellID` 为 1、购买玩家 ID `buyID` 为 2、购买货物数量 `amount` 为 10、购买消耗金币数 `price` 为 100。返回值为交易是否成功。当出现售卖玩家货物不足、购买玩家金币不足或数据库错误时，交易将不成功，且由于[数据库事务](/develop/dev-guide-transaction-overview.md)保证，不会有玩家的金币或货物丢失的情况。

```json
true
```

### 第 6 步第 3 部分：使用 Shell 脚本请求

这里已经将请求过程编写为 [Shell](https://github.com/pingcap-inc/tidb-example-java/blob/main/spring-jpa-hibernate/request.sh) 脚本，以方便大家的测试，脚本将会做以下操作：

1. 循环创建 10 名玩家
2. 获取 `id` 为 1 的玩家信息
3. 获取至多 3 名玩家信息列表
4. 获取玩家总数
5. `id` 为 1 的玩家作为售出方，id 为 2 的玩家作为购买方，购买 10 个货物，耗费 100 金币

你可以使用 `./request.sh` 命令运行此脚本，结果应如下所示：

```
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

## 实现细节

本小节介绍示例应用程序项目中的组件。

### 总览

本示例项目的大致目录树如下所示：

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

- 所有的 `__init__.py` 声明此文件夹是一个 Python 包。
- `manage.py` 为 Django 自动生成的对项目进行管理的脚本。
- `example_project` 包含项目级别的代码。

    - `settings.py` 内声明了项目的配置，如数据库地址、密码、使用的数据库方言等。
    - `urls.py` 配置了项目的根路由。

- `player` 是项目中提供对 `Player` 数据模型管理、数据查询的包，这在 Django 中被叫做应用。你可以使用 `python manage.py startapp player` 来创建一个空白的 `player` 应用。

    - `models.py` 是定义 `Player` 数据模型的 Python 脚本。
    - `migrations` 包内是一组数据模型迁移脚本。可使用 `python manage.py makemigrations player` 命令自动分析 `models.py` 内定义的数据对象，并生成迁移脚本。
    - `urls.py` 定义了此应用的路由。
    - `views.py` 内提供了逻辑代码。

> **提示：**
>
> 另外值得一提的是，由于 Django 的任意对象都被设计为可插拔模式。因此，你需要在创建应用后，在项目中进行注册。在此例中，注册的过程即在 `example_project` 包的 `settings.py` 文件中，在 `INSTALLED_APPS` 对象内，添加 `'player.apps.PlayerConfig'` 条目即可。你可以参考[示例代码](https://github.com/pingcap-inc/tidb-example-python/blob/main/django_example/example_project/settings.py#L33-L41)以获得更多信息。

### 项目配置

本节将简要介绍 `example_project` 包内 `settings.py` 的重点配置。文件内为 Django 项目配置，声明了项目包含的应用、中间件，连接的数据库等信息，你可以通过[创建相同依赖空白程序](#创建相同依赖空白程序可选) 这一节来复刻此配置文件的生成流程，当然，也可直接复制此文件至你的项目来使用。你可访问 [Django 配置](https://docs.djangoproject.com/zh-hans/3.2/topics/settings/)文档以获取更多信息。

其中：

- `INSTALLED_APPS` : 启用的应用全限定名称列表。
- `MIDDLEWARE` : 启用的中间件列表，由于此处无需 `CsrfViewMiddleware` 中间件，因此其被注释。
- `DATABASES` : 数据库配置，其中，`ENGINE` 一项被配置为 `django_tidb`。这遵循了 [django-tidb](https://github.com/pingcap/django-tidb) 的配置要求。

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

### 根路由

根路由被编写在 `example_project` 包中的 `urls.py`：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('player/', include('player.urls')),
    path('admin/', admin.site.urls),
]
```

根路由十分简单，将 `player/` 路径指向了 `player.urls`。即 `player` 包下的 `urls.py` 将接管 `player/*` 的 URL 映射。你可以访问 [Django URL调度器](https://docs.djangoproject.com/zh-hans/3.2/topics/http/urls/)文档来获取更多信息。

### player 应用

`player` 应用内，实现了对 `Player` 对象的数据模型迁移、对象持久化、接口实现等功能。

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

这里可以看到，数据模型中拥有一个子类 `Meta`，这些子类给了 Django 额外的信息，用以指定数据模型的元信息。其中，`db_table` 声明此数据模型对应的表名为 `player`。模型的元信息的全部选项可查看 [Django 模型 Meta 选项](https://docs.djangoproject.com/zh-hans/3.2/ref/models/options/)文档。

此外，数据模型中定义了 `id`, `coins` 及 `goods` 三个属性。其中：

- `id`: `models.AutoField(primary_key=True)` 表示其为一个自动递增的主键。
- `coins`: `models.IntegerField()` 表示其为一个 Integer 类型的字段。
- `goods`: `models.IntegerField()` 表示其为一个 Integer 类型的字段。

更多关于数据模型的信息，可查看 [Django 模型](https://docs.djangoproject.com/zh-hans/3.2/topics/db/models/)文档。

#### 数据模型迁移

Django 的设计思路是以 Python 数据模型定义代码为依赖，对数据库模型进行迁移。因此，其将生成一系列的数据库模型迁移脚本，用以抹平代码与数据库之间的差异。在 `models.py` 中定义完毕 `Player` 数据模型后，你可以运行 `python manage.py makemigrations player` 用以完成迁移脚本的生成。此例中，`migrations` 包内的 `0001_initial.py` 即为自动生成的迁移脚本。

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

你可以使用命令 `python manage.py sqlmigrate ...` 来预览这个迁移脚本最终将运行的 SQL 语句。这将极大地减少迁移脚本运行你意料之外的 SQL 语句的可能性。我们推荐在生成迁移脚本后，请至少使用一次此命令预览并仔细检查生成的 SQL 语句。此例中，你可运行 `python manage.py sqlmigrate player 0001`，其输出为：

```sql
--
-- Create model Player
--
CREATE TABLE `player` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `coins` integer NOT NULL, `goods` integer NOT NULL);
```

其输出被设计为人类可读的模式，这非常便于开发者进行审核。

生成迁移脚本后，你可使用 `python manage.py migrate` 实施数据迁移。此命令拥有幂等性，其运行后将在数据库内保存一条运行记录以完成幂等保证。因此，你可以多次运行此命令，而无需担心重复运行 SQL 语句。

#### 应用路由

在[根路由](#根路由)一节中，我们将 `player/` 路径指向了 `player.urls`。本节将展开叙述 `player` 包下的 `urls.py` 应用路由：

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

- `''`: 被指向了 `views.create` 函数。
- `'count'`: 被指向了 `views.count` 函数。
- `'limit/<int:limit>'`: 被指向了 `views.limit_list` 函数。此处路径包含一个 `<int:limit>` 路径变量，其中：

    - `int` 是指这个参数其将被验证是否为 `int` 类型
    - `limit` 是指此参数的值将被映射至名为 `limit` 的函数入参中

- `'<int:player_id>'`: 被指向了 `views.get_by_id` 函数，此处路径包含一个 `<int:player_id>` 路径变量。
- `'trade'`: 被指向了 `views.trade` 函数。

另外，值得一提的是，此处的应用路由是根路由转发而来的，因此将在 URL 匹配时包含跟路由配置的路径。如此例中所示，根路由配置为 `player/` 转发至此应用路由，那么，应用路由中的：

- `''` 在实际的请求中，为 `http(s)://<host>(:<port>)/player`。
- `'count'` 在实际的请求中，为 `http(s)://<host>(:<port>)/player/count`。
- `'limit/<int:limit>'` 以 `limit` 为 `3` 为例，在实际的请求中为 `http(s)://<host>(:<port>)/player/limit/3`。

#### 逻辑实现

逻辑实现代码，在 `player` 包下的 `views.py` 内，其中包含了项目实现逻辑。这在 Django 中被称为视图，可参考 [Django 视图](https://docs.djangoproject.com/zh-hans/3.2/topics/http/views/)文档来获取更多信息。

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
    if limit is 0:
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

下方将逐一解释代码中的重点部分：

- 装饰器：

    - `@require_GET`: 代表此函数仅接受 `GET` 类型的 HTTP 请求。
    - `@require_POST`: 代表此函数仅接受 `POST` 类型的 HTTP 请求。
    - `@transaction.atomic`: 代表此函数内的所有数据库操作将被包含于同一个事务中运行。可查看 [Django 数据库事务](https://docs.djangoproject.com/zh-hans/3.2/topics/db/transactions/)文档查看关于如何在 Django 中使用事务。同时，也可以查看 [TiDB 事务概览](/develop/dev-guide-transaction-overview.md)文档来查看 TiDB 中的事务行为。

- `create` 函数：

    - 获取 `request` 对象中的 `body` 的 payload，并用 `utf-8` 解码

        ```python
        dict_players = json.loads(request.body.decode('utf-8'))
        ```

    - 使用 lambda 中的 `map` 函数，将 dict 类型的 `dict_players` 对象转换为 `Player` 数据模型的 list。

        ```python
        players = list(map(
            lambda p: Player(
                coins=p['coins'],
                goods=p['goods']
            ), dict_players))
        ```

    - 调用 `Player` 数据模型的 `bulk_create` 函数。批量添加整个 `players` list。并且返回添加的数据条目。

        ```python
        result = Player.objects.bulk_create(objs=players)
        return HttpResponse(f'create {len(result)} players.')
        ```

- `count` 函数，调用 `Player` 数据模型的 `count` 函数，并返回。
- `limit_list` 函数：

    - 短路逻辑，`limit` 为 0 时将不做数据库请求。

        ```python
        if limit is 0:
            return HttpResponse("")
        ```

    - 调用 `Player` 数据模型的 `all` 函数，并仅获取 前`limit` 个数据。注意此处 Django 并不会获取所有数据并在内存中切分前 `limit` 个数据。而是在使用时再请求数据库的前 `limit` 个数据。这是由于 Django 重写了切片操作符，并且 QuerySet 对象是**惰性**的。这意味着对一个未执行的 QuerySet 进行切片，将继续返回一个未执行的 QuerySet。直到你第一次真正的请求 QuerySet 内的数据，例如此处使用 `set` 函数对其进行迭代并返回整个 set。你可以参考 [Django QuerySet API 参考](https://docs.djangoproject.com/zh-hans/3.2/ref/models/querysets/)文档来获取更多信息。

        ```python
        players = set(Player.objects.all()[:limit])
        ```

    - 将返回的 `Player` 数据模型的列表，转为对象为 dict 的 list，并使用 `JsonResponse` 输出。

        ```python
        dict_players = list(map(lambda p: p.as_dict(), players))
        return JsonResponse(dict_players, safe=False)
        ```

- `get_by_id` 函数：

    - 使用 `get_object_or_404` 语法糖，将 `player_id` 传入。如数据不存在，将由此函数返回 404 状态码。随后将 `Player` 对象转为 dict。

        ```python
        result = get_object_or_404(Player, pk=player_id).as_dict()
        ```

    - 使用 `JsonResponse` 返回数据。

        ```python
        return JsonResponse(result)
        ```

- `trade` 函数：

    - 从 Post Payload 中，接收 Form 形式的数据

        ```python
        sell_id, buy_id, amount, price = int(request.POST['sellID']), int(request.POST['buyID']), \
                                        int(request.POST['amount']), int(request.POST['price'])
        ```

    - 调用 `Player` 数据模型的 `select_for_update` 函数，检查数据，并对此数据进行加锁操作，留待后续更新使用。由于此函数使用了 `@transaction.atomic` 装饰器，任意的异常都会导致事务回滚，可以利用这个机制，在任意检查失败的时候，抛出异常，由 Django 进行事务回滚。此处需检查两项：

        - 卖家的货物数是否足够。
        - 买家的货币数是否足够。

        ```python
        sell_player = Player.objects.select_for_update().get(id=sell_id)
        if sell_player.goods < amount:
            raise Exception(f'sell player {sell_player.id} goods not enough')

        buy_player = Player.objects.select_for_update().get(id=buy_id)
        if buy_player.coins < price:
            raise Exception(f'buy player {buy_player.id} coins not enough')
        ```

    - 逐一对卖家与买家的数据进行更新。此处更新有任何异常都将由 Django 回滚事务。因此，请不要在此处手动使用 `try-except` 语法进行异常处理。如果一定需要处理，请在 except 块中将异常继续抛向上层，以防 Django 误以为函数运行正常，提交事务后，导致错误的数据出现。

        ```python
        Player.objects.filter(id=sell_id).update(goods=F('goods') - amount, coins=F('coins') + price)
        Player.objects.filter(id=buy_id).update(goods=F('goods') + amount, coins=F('coins') - price)
        ```

    - 返回成功字符串，因为其他情况将导致异常抛出返回。

        ```python
        return HttpResponse("trade successful")
        ```
