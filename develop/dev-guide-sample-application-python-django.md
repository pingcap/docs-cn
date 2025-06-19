---
title: 使用 Django 连接 TiDB
summary: 了解如何使用 Django 连接 TiDB。本教程提供使用 Django 操作 TiDB 的 Python 示例代码片段。
---

# 使用 Django 连接 TiDB

TiDB 是一个兼容 MySQL 的数据库，而 [Django](https://www.djangoproject.com) 是一个流行的 Python Web 框架，它包含一个强大的对象关系映射（ORM）库。

在本教程中，您将学习如何使用 TiDB 和 Django 完成以下任务：

- 设置环境。
- 使用 Django 连接到您的 TiDB 集群。
- 构建并运行您的应用程序。您也可以查看基本 CRUD 操作的示例代码片段。

> **注意：**
>
> 本教程适用于 TiDB Cloud Serverless、TiDB Cloud Dedicated 和 TiDB Self-Managed 集群。

## 前提条件

要完成本教程，您需要：

- [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

<CustomContent platform="tidb">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](/production-deployment-using-tiup.md)的说明创建本地集群。

</CustomContent>
<CustomContent platform="tidb-cloud">

**如果您还没有 TiDB 集群，可以按照以下方式创建：**

- （推荐）按照[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md)的说明创建您自己的 TiDB Cloud 集群。
- 按照[部署本地测试 TiDB 集群](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)或[部署生产 TiDB 集群](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)的说明创建本地集群。

</CustomContent>

## 运行示例应用程序连接 TiDB

本节演示如何运行示例应用程序代码并连接到 TiDB。

### 步骤 1：克隆示例应用程序仓库

在终端窗口中运行以下命令来克隆示例代码仓库：

```shell
git clone https://github.com/tidb-samples/tidb-python-django-quickstart.git
cd tidb-python-django-quickstart
```

### 步骤 2：安装依赖

运行以下命令安装示例应用程序所需的包（包括 Django、django-tidb 和 mysqlclient）：

```shell
pip install -r requirements.txt
```

如果您在安装 mysqlclient 时遇到问题，请参考 [mysqlclient 官方文档](https://github.com/PyMySQL/mysqlclient#install)。

#### 什么是 `django-tidb`？

`django-tidb` 是一个用于 Django 的 TiDB 方言，它解决了 TiDB 和 Django 之间的兼容性问题。

安装 `django-tidb` 时，请选择与您的 Django 版本匹配的版本。例如，如果您使用的是 `django==4.2.*`，请安装 `django-tidb==4.2.*`。次要版本号不需要相同。建议使用最新的次要版本。

更多信息，请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 步骤 3：配置连接信息

根据您选择的 TiDB 部署选项连接到您的 TiDB 集群。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 确保连接对话框中的配置与您的操作环境相匹配。

    - **连接类型**设置为 `Public`
    - **分支**设置为 `main`
    - **连接方式**设置为 `General`
    - **操作系统**与您的环境匹配。

    > **提示：**
    >
    > 如果您的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 点击**生成密码**创建一个随机密码。

    > **提示：**
    >
    > 如果您之前已经创建了密码，您可以使用原始密码，也可以点击**重置密码**生成一个新密码。

5. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

6. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # 例如 gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # 例如 xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{ssl_ca}'  # 例如 /etc/ssl/certs/ca-certificates.crt (Debian / Ubuntu / Arch)
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数。

    TiDB Cloud Serverless 需要安全连接。由于 mysqlclient 的 `ssl_mode` 默认为 `PREFERRED`，您不需要手动指定 `CA_PATH`。只需将其留空即可。但如果您有特殊原因需要手动指定 `CA_PATH`，可以参考 [TiDB Cloud Serverless 的 TLS 连接](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-clusters)获取不同操作系统的证书路径。

7. 保存 `.env` 文件。

</div>
<div label="TiDB Cloud Dedicated">

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**，然后点击 **CA 证书**下载 CA 证书。

    如果您尚未配置 IP 访问列表，请点击**配置 IP 访问列表**或按照[配置 IP 访问列表](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)中的步骤在首次连接之前进行配置。

    除了**公共**连接类型外，TiDB Cloud Dedicated 还支持**私有端点**和 **VPC 对等连接**连接类型。更多信息，请参见[连接到您的 TiDB Cloud Dedicated 集群](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)。

4. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

5. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{host}'  # 例如 tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # 例如 root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    请确保将占位符 `{}` 替换为从连接对话框获得的连接参数，并将 `CA_PATH` 配置为在上一步中下载的证书路径。

6. 保存 `.env` 文件。

</div>
<div label="TiDB Self-Managed">

1. 运行以下命令复制 `.env.example` 并将其重命名为 `.env`：

    ```shell
    cp .env.example .env
    ```

2. 将相应的连接字符串复制并粘贴到 `.env` 文件中。示例结果如下：

    ```dotenv
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    请确保将占位符 `{}` 替换为连接参数，并删除 `CA_PATH` 行。如果您在本地运行 TiDB，默认主机地址是 `127.0.0.1`，密码为空。

3. 保存 `.env` 文件。

</div>
</SimpleTab>

### 步骤 4：初始化数据库

在项目的根目录中，运行以下命令初始化数据库：

```shell
python manage.py migrate
```

### 步骤 5：运行示例应用程序

1. 在开发模式下运行应用程序：

    ```shell
    python manage.py runserver
    ```

    应用程序默认在端口 `8000` 上运行。要使用不同的端口，您可以在命令后附加端口号。示例如下：

    ```shell
    python manage.py runserver 8080
    ```

2. 要访问应用程序，请打开浏览器并访问 `http://localhost:8000/`。在示例应用程序中，您可以：

    - 创建新玩家。
    - 批量创建玩家。
    - 查看所有玩家。
    - 更新玩家信息。
    - 删除玩家。
    - 在两个玩家之间交易物品。

## 示例代码片段

您可以参考以下示例代码片段来完成您自己的应用程序开发。

有关完整的示例代码及其运行方法，请查看 [tidb-samples/tidb-python-django-quickstart](https://github.com/tidb-samples/tidb-python-django-quickstart) 仓库。

### 连接到 TiDB

在文件 `sample_project/settings.py` 中，添加以下配置：

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

您需要将 `${tidb_host}`、`${tidb_port}`、`${tidb_user}`、`${tidb_password}`、`${tidb_db_name}` 和 `${ca_path}` 替换为您的 TiDB 集群的实际值。

### 定义数据模型

```python
from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)
    coins = models.IntegerField(default=100)
    goods = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

更多信息，请参见 [Django 模型](https://docs.djangoproject.com/en/dev/topics/db/models/)。

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

更多信息，请参见[插入数据](/develop/dev-guide-insert-data.md)。

### 查询数据

```python
# 获取单个对象
player = Player.objects.get(name="player1")

# 获取多个对象
filtered_players = Player.objects.filter(name="player1")

# 获取所有对象
all_players = Player.objects.all()
```

更多信息，请参见[查询数据](/develop/dev-guide-get-data-from-single-table.md)。

### 更新数据

```python
# 更新单个对象
player = Player.objects.get(name="player1")
player.coins = 200
player.save()

# 更新多个对象
Player.objects.filter(coins=100).update(coins=200)
```

更多信息，请参见[更新数据](/develop/dev-guide-update-data.md)。

### 删除数据

```python
# 删除单个对象
player = Player.objects.get(name="player1")
player.delete()

# 删除多个对象
Player.objects.filter(coins=100).delete()
```

更多信息，请参见[删除数据](/develop/dev-guide-delete-data.md)。

## 下一步

- 从 [Django 的文档](https://www.djangoproject.com/)了解更多 Django 的用法。
- 通过[开发者指南](/develop/dev-guide-overview.md)中的章节学习 TiDB 应用程序开发的最佳实践，例如[插入数据](/develop/dev-guide-insert-data.md)、[更新数据](/develop/dev-guide-update-data.md)、[删除数据](/develop/dev-guide-delete-data.md)、[单表读取](/develop/dev-guide-get-data-from-single-table.md)、[事务](/develop/dev-guide-transaction-overview.md)和 [SQL 性能优化](/develop/dev-guide-optimize-sql-overview.md)。
- 学习专业的 [TiDB 开发者课程](https://www.pingcap.com/education/)，并在通过考试后获得 [TiDB 认证](https://www.pingcap.com/education/certification/)。

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
