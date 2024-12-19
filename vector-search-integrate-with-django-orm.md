---
title: 在 Django ORM 中使用 TiDB 向量搜索
summary: 了解如何在 Django ORM 中通过 TiDB 向量搜索功能存储向量并执行语义搜索。
---

# 在 Django ORM 中使用 TiDB 向量搜索

本文档将展示如何使用 [Django](https://www.djangoproject.com/) ORM 与 [TiDB 向量搜索](/vector-search-overview.md)进行交互，以及如何存储向量和执行向量搜索查询。

> **警告：**
>
> 向量搜索目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 前置需求

为了能够顺利完成本文中的操作，你需要提前：

- 在你的机器上安装 [Python 3.8](https://www.python.org/downloads/) 或更高版本
- 在你的机器上安装 [Git](https://git-scm.com/downloads)
- 准备一个 TiDB 集群

如果你还没有 TiDB 集群，可以按照以下任一种方式创建：

- 参考[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)，创建本地集群。
- 参考[创建 TiDB Cloud Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-cloud-serverless-集群)，创建 TiDB Cloud 集群。

## 运行示例应用程序

你可以通过以下步骤快速了解如何在 Django ORM 中使用 TiDB 向量搜索。

### 第 1 步：克隆示例代码仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第 2 步：创建虚拟环境

为你的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-django-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 第 3 步：安装所需的依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

你也可以直接为项目安装以下依赖项：

```bash
pip install Django django-tidb mysqlclient numpy python-dotenv
```

如果遇到 mysqlclient 安装问题，请参阅 mysqlclient 官方文档。

#### 什么是 `django-tidb`?

`django-tidb` 是一个为 Django 提供的 TiDB 适配器。通过该适配器，Django ORM 实现了对 TiDB 特有的功能（如，向量搜索）的支持，并解决了 TiDB 和 Django 之间的兼容性问题。

安装 `django-tidb` 时，选择与你的 Django 版本匹配的版本。例如，如果你使用的是 `django==4.2.*`，则应安装 `django-tidb==4.2.*`，其中 minor 版本号不需要完全相同。建议使用最新的 minor 版本。

更多信息，请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 第 4 步：配置环境变量

根据 TiDB 集群的部署方式不同，选择对应的环境变量配置方式。

<SimpleTab>

<div label="本地部署 TiDB">

对于本地部署的 TiDB，请在 Python 项目的根目录下新建一个 `.env` 文件，将以下内容复制到 `.env` 文件中，并根据集群的连接参数修改环境变量值为 TiDB 实际对应的值：

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

如果你在本机运行 TiDB，`TIDB_HOST` 默认为 `127.0.0.1`。`TIDB_PASSWORD` 初始密码为空，若你是第一次启动集群，则无需带上此字段。

以下为各参数的解释：

- `TIDB_HOST`：TiDB 集群的主机号。
- `TIDB_PORT`：TiDB 集群的端口号。
- `TIDB_USERNAME`：连接 TiDB 集群的用户名。
- `TIDB_PASSWORD`：连接 TiDB 集群的密码。
- `TIDB_DATABASE`：要连接的数据库名称。

</div>

<div label="TiDB Cloud Serverless">

对于 TiDB Cloud Serverless 集群，请按照以下步骤获取集群的连接字符串，然后配置环境变量：

1. 在 TiDB Cloud 的 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，单击你的 TiDB Cloud Serverless 集群名，进入集群的 **Overview** 页面。

2. 点击右上角的 **Connect** 按钮，将会弹出连接对话框。

3. 确认对话框中的配置和你的运行环境一致。

    - **Connection Type** 为 `Public`。
    - **Branch** 选择 `main`。
    - **Connect With** 选择 `General`。
    - **Operating System** 为你的运行环境。

    > **Tip:**
    >
    > 如果你的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换为对应的 Linux 发行版。

4. 从连接对话框中复制连接参数。

    > **Tip:**
    >
    > 如果你还没有设置密码，点击 **Generate Password** 生成一个随机密码。

5. 在 Python 项目的根目录下新建一个 `.env` 文件，并将连接参数粘贴到相应的环境变量中。

    - `TIDB_HOST`：TiDB 集群的主机号。
    - `TIDB_PORT`：TiDB 集群的端口号。
    - `TIDB_USERNAME`：连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`：连接 TiDB 集群的密码。
    - `TIDB_DATABASE`：要连接的数据库名称。
    - `TIDB_CA_PATH`：根证书文件的路径。

    以下为 macOS 的示例：

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

</div>

</SimpleTab>

### 第 5 步：运行示例应用程序

迁移数据库模式：

```bash
python manage.py migrate
```

运行 Django 开发服务器：

```bash
python manage.py runserver
```

打开浏览器，访问 `http://127.0.0.1:8000` 查看该示例程序的可视化界面。以下为该程序可用的 API 路径：

| API 路径                                | 描述                              |
| --------------------------------------- | ---------------------------------------- |
| `POST: /insert_documents`               | 插入含有向量的 `document`。        |
| `GET: /get_nearest_neighbors_documents` | 获取距离最近的 3 个 `document`。    |
| `GET: /get_documents_within_distance`   | 获取处于给定距离内的所有 `document`。 |

## 示例代码片段

你可以参考以下示例代码片段来完成自己的应用程序开发。

### 连接到 TiDB 集群

打开 `sample_project/settings.py` 文件，添加以下配置：

```python
dotenv.load_dotenv()

DATABASES = {
    "default": {
        # https://github.com/pingcap/django-tidb
        "ENGINE": "django_tidb",
        "HOST": os.environ.get("TIDB_HOST", "127.0.0.1"),
        "PORT": int(os.environ.get("TIDB_PORT", 4000)),
        "USER": os.environ.get("TIDB_USERNAME", "root"),
        "PASSWORD": os.environ.get("TIDB_PASSWORD", ""),
        "NAME": os.environ.get("TIDB_DATABASE", "test"),
        "OPTIONS": {
            "charset": "utf8mb4",
        },
    }
}

TIDB_CA_PATH = os.environ.get("TIDB_CA_PATH", "")
if TIDB_CA_PATH:
    DATABASES["default"]["OPTIONS"]["ssl_mode"] = "VERIFY_IDENTITY"
    DATABASES["default"]["OPTIONS"]["ssl"] = {
        "ca": TIDB_CA_PATH,
    }
```

你可以在项目的根目录下创建一个 `.env` 文件，在文件中添加环境变量 `TIDB_HOST`、`TIDB_PORT`、`TIDB_USERNAME`、`TIDB_PASSWORD`、`TIDB_DATABASE` 和 `TIDB_CA_PATH`，并根据你的 TiDB 集群的实际值来设置这些变量的值。

### 创建向量表

#### 定义向量列

`tidb-django` 提供了一个 `VectorField`，可以在表中用来表示和存储向量类型。

创建一个表，其中包含一个向量数据类型的 `embedding` 列，用于存储三维向量。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

### 存储包含向量的 `document`

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### 搜索近邻向量

TiDB 向量支持以下距离函数：

- `L1Distance`
- `L2Distance`
- `CosineDistance`
- `NegativeInnerProduct`

可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 语义最接近的前 3 个 `document`。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 搜索一定距离内的向量

可以选择使用余弦距离 (`CosineDistance`) 函数，查询与向量 `[1, 2, 3]` 的余弦距离小于 0.2 的向量。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## 另请参阅

- [向量数据类型](/vector-search-data-types.md)
- [向量搜索索引](/vector-search-index.md)