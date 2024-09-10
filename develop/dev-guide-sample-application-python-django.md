---
title: 使用 Django 连接到 TiDB
summary: 了解如何使用 Django 连接到 TiDB。本文提供了使用 Django 与 TiDB 交互的 Python 示例代码片段。
aliases: ['/zh/tidb/dev/dev-guide-sample-application-django']
---

# 使用 Django 连接到 TiDB

TiDB 是一个兼容 MySQL 的数据库。[Django](https://www.djangoproject.com/) 为当前流行的 Python Web 框架之一，它内部实现了一个强大的 ORM (Object Relational Mapper) 系统。

本文档将展示如何使用 TiDB 和 Django 来完成以下任务：

- 配置你的环境。
- 使用 Django 连接到 TiDB 集群。
- 构建并运行你的应用程序。你也可以参考[示例代码片段](#示例代码片段)，完成基本的 CRUD 操作。

> **注意**
>
> 本文档适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和本地部署的 TiDB。

## 前置需求

- 推荐 [Python 3.8](https://www.python.org/downloads/) 及以上版本。
- [Git](https://git-scm.com/downloads)。
- TiDB 集群。如果你还没有 TiDB 集群，可以按照以下方式创建：
    - （推荐方式）参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建你自己的 TiDB Cloud 集群。
    - 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。

## 运行代码并连接到 TiDB

本小节演示如何运行示例应用程序的代码，并连接到 TiDB。

### 第 1 步：克隆示例代码仓库到本地

运行以下命令，将示例代码仓库克隆到本地：

```bash
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### 第 2 步：安装依赖

运行以下命令，安装示例代码所需要的依赖（包括 Django、django-tidb 和 mysqlclient）：

```bash
pip install -r requirements.txt
```

如果你在安装 mysqlclient 时遇到问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)。

#### `django-tidb` 是什么？

`django-tidb` 是一个为 Django 提供的 TiDB 适配器，它解决了 TiDB 与 Django 之间的兼容性问题。

安装 `django-tidb` 时，请选择与你的 Django 版本匹配的版本。例如，如果你使用的是 `django==4.2.*`，则应安装 `django-tidb>=4.2.0,<4.3.0`，其中 minor 版本号不需要完全相同。建议使用最新的 minor 版本。

更多信息，请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 第 3 步：配置连接信息

根据不同的 TiDB 部署方式，使用不同的方法连接到 TiDB 集群。

<SimpleTab>

<div label="TiDB Cloud Serverless">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Cloud Serverless 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

    > **Tip:**
    >
    > 如果你之前已经生成过密码，可以直接使用原密码，或点击 **Reset Password** 重新生成密码。

5. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

6. 复制并粘贴对应连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # e.g. /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值。

7. 保存 `.env` 文件。

</div>

<div label="TiDB Cloud Dedicated">

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面中，选择你的 TiDB Cloud Dedicated 集群，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会出现连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**，并点击 **CA cert** 下载 CA 文件。

    如果你尚未配置 IP 访问列表，请在首次连接前点击 **Configure IP Access List** 或按照[配置 IP 访问列表（英文）](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤进行配置。

    除 **Public** 连接类型外，TiDB Cloud Dedicated 还支持 **Private Endpoint** 和 **VPC Peering** 连接类型。详情请参阅[连接 TiDB Cloud Dedicated 集群（英文）](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

5. 复制并粘贴对应的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # e.g. xxxxxx.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    注意替换 `{}` 中的占位符为连接对话框中获得的值，并配置前面步骤中下载好的证书路径。

6. 保存 `.env` 文件。

</div>

<div label="本地部署 TiDB">

1. 运行以下命令，将 `.env.example` 复制并重命名为 `.env`：

    ```bash
    cp .env.example .env
    ```

2. 复制并粘贴对应 TiDB 的连接字符串至 `.env` 中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    注意替换 `{}` 中的占位符为你的 TiDB 对应的值，并删除 `CA_PATH` 这行。如果你在本机运行 TiDB，默认 Host 地址为 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>

</SimpleTab>

### 第 4 步：初始化数据库

在示例项目根目录执行以下命令，初始化数据库：

```shell
python manage.py migrate
```

```shell
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sample_project, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sample_project.0001_initial... OK
  Applying sessions.0001_initial... OK
```

### 第 5 步：运行示例应用程序

1. 在开发模式下运行示例应用程序：

    ```shell
    python manage.py runserver
    ```

    应用程序默认在 `8000` 端口上运行。如果你想要使用其他端口号，可以在命令后添加端口号，例如：

    ```shell
    python manage.py runserver 8080
    ```

2. 打开浏览器，在地址栏输入 `http://localhost:8000/`，访问示例应用程序，你可以进行以下操作：

    - 创建一个新的 Player
    - 批量创建 Player
    - 查看所有的 Player
    - 更新 Player
    - 删除 Player
    - 在两个 Player 之间交易物品

## 示例代码片段

你可参考以下关键代码片段，完成自己的应用开发。

完整代码及其运行方式，见代码仓库 [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart)。

### 配置数据库连接

打开 `sample_project/settings.py` 文件，添加以下配置：

```python
DATABASES = {
    "default": {
        "ENGINE": "django_tidb",
        "HOST": '${tidb_host}',
        "PORT": '${tidb_port}',
        "USER": '${tidb_user}',
        "PASSWORD": '${tidb_password}',
        "NAME": '${tidb_db_name}',
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = '${ca_path}'
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

在使用该函数时，你需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 以及 `${ca_path}` 替换为你的 TiDB 集群的实际值。

### 声明数据对象

```python
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    coins = models.IntegerField(default=100)
    goods = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

更多信息参考 [Django 模型](https://docs.djangoproject.com/en/dev/topics/db/models/)。

### 插入数据

```python
# 插入单个对象
player = Player.objects.create(name="player1", coins=100, goods=1)

# 批量插入多个对象
Player.objects.bulk_create([
    Player(name="player1", coins=100, goods=1),
    Player(name="player2", coins=200, goods=2),
    Player(name="player3", coins=300, goods=3),
])
```

更多信息参考[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
# 查询单个对象
player = Player.objects.get(name="player1")

# 查询多个对象
filtered_players = Player.objects.filter(name="player1")

# 查询所有对象
all_players = Player.objects.all()
```

更多信息参考[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
# 更新单个对象
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# 批量更新多个对象
Player.objects.filter(coins=100).update(coins=200)
```

更多信息参考[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
# 删除单个对象
player = Player.objects.get(name="player1")
player.delete()

# 批量删除多个对象
Player.objects.filter(coins=100).delete()
```

更多信息参考[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 关于 Django 的更多使用方法，可以参考 [Django 官方文档](https://www.djangoproject.com/)。
- 你可以继续阅读开发者文档，以获取更多关于 TiDB 应用开发的最佳实践。例如：[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)、[SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)等。
- 如果你更倾向于参与课程进行学习，我们也提供专业的 [TiDB 开发者课程](https://cn.pingcap.com/courses-catalog/category/back-end-developer/?utm_source=docs-cn-dev-guide)支持，并在考试后提供相应的[资格认证](https://learn.pingcap.com/learner/certification-center)。

## 需要帮助?

如果在开发的过程中遇到问题，可以在 [AskTUG](https://asktug.com/?utm_source=docs-cn-dev-guide) 上进行提问，寻求帮助。