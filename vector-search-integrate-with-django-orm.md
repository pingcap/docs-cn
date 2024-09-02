---
title: TiDB 向量搜索与 Django ORM 相集成
summary: 了解如何将 TiDB 向量搜索与 Django ORM 集成，以存储嵌入并执行语义搜索。
---

# TiDB 向量搜索与 Django ORM 结合

本教程将指导您如何使用 [Django](https://www.djangoproject.com/) ORM 与 TiDB 向量搜索进行交互、存储嵌入和执行向量搜索查询。

## 准备

要实现本部分的内容，需要确保安装以下内容：

- [Python 3.8 or higher](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads) 
- TiDB serverless集群。如果没有，请按照[使用 TiDB Serverless 构建 TiDB 集群](/develop/dev-guide-build-cluster-in-cloud.md)创建自己的 TiDB 集群。

## 运行示例应用程序

您可以通过以下步骤快速了解如何将 TiDB 向量搜索与 Django ORM 集成。

### 步骤 1. clone仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-django-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需的依赖项

安装示例项目所需的依赖项：

```bash
pip install -r requirements.txt
```

您可以为现有项目安装以下软件包：

```bash
pip install Django django-tidb mysqlclient numpy python-dotenv
```

如果遇到 mysqlclient 安装问题，请参阅 mysqlclient 官方文档。

#### 什么是 `django-tidb`?

`django-tidb`使用django框架提供了与tidb交互的示例，它实现了 Django ORM 以支持 TiDB 特有的功能（例如，向量搜索），并解决了 TiDB 和 Django 之间的兼容性问题。

要安装 `django-tidb`，请选择与 Django 版本相匹配的版本。例如，如果使用的是 `django==4.2.*`, 则安装 `django-tidb===4.2.*`。次版本号不必相同。建议使用最新的次版本。

更多信息，请参阅 [django-tidb repository](https://github.com/pingcap/django-tidb)。

### 步骤 4. 配置环境变量

1. 导航至 [** 群集**](https://tidbcloud.com/console/clusters) 页面，然后单击目标群集的名称进入其概览页面。

2. 单击右上角的**连接**。此时将显示连接对话框。

3. 确保连接对话框中的配置符合您的运行环境。

    - **Endpoint Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与环境相匹配

    > **Tip:**
    >
    > 如果程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 从连接对话框中复制连接参数。

    > **Tip:**
    >
    > 如果尚未设置密码，请单击**生成密码**生成一个随机密码。

5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接参数粘贴到相应的环境变量中。

    - `TIDB_HOST`: TiDB 集群的主机。
    - `TIDB_PORT`: TiDB 集群的端口。
    - `TIDB_USERNAME`: 连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`: 连接 TiDB 集群的密码。
    - `TIDB_DATABASE`: 要连接的数据库名称。
    - `TIDB_CA_PATH`: 根证书文件的路径。

    以下是 MacOS 的示例：

    ```dotenv
    TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME=********.root
    TIDB_PASSWORD=********
    TIDB_DATABASE=test
    TIDB_CA_PATH=/etc/ssl/cert.pem
    ```

### Step 5. 运行demo

迁移数据库模式：

```bash
python manage.py migrate
```

运行 Django 开发服务器：

```bash
python manage.py runserver
```

打开浏览器，访问 `http://127.0.0.1:8000` 尝试演示应用程序。以下是可用的 API 路径：

| API Path                                | Description                              |
| --------------------------------------- | ---------------------------------------- |
| `POST: /insert_documents`               | Insert documents with embeddings.        |
| `GET: /get_nearest_neighbors_documents` | Get the 3-nearest neighbor documents.    |
| `GET: /get_documents_within_distance`   | Get documents within a certain distance. |

## 示例代码片段

您可以参考以下示例代码片段来完成自己的应用程序开发。

### 连接到 TiDB 集群

在文件 `sample_project/settings.py` 中添加以下配置：

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

你可以在项目根目录下创建一个 `.env` 文件，并使用 TiDB 集群的实际值设置环境变量 `TIDB_HOST`、`TIDB_PORT`、`TIDB_USERNAME`、`TIDB_PASSWORD`、`TIDB_DATABASE` 和 `TIDB_CA_PATH`。

### 创建向量表

#### 定义向量列

`tidb-django` 提供了一个 `VectorField` 来在表中存储向量嵌入。

创建一个表格，其中有一列名为 `embedding`，用于存储三维向量。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

#### 用索引定义优化的向量列

定义三维向量列，并使用[向量搜索索引](/vector-search-index.md) （HNSW 索引）对其进行优化。

```python
class DocumentWithIndex(models.Model):
   content = models.TextField()
   # Note:
   #   - Using comment to add hnsw index is a temporary solution. In the future it will use `CREATE INDEX` syntax.
   #   - Currently the HNSW index cannot be changed after the table has been created.
   #   - Only Django >= 4.2 supports `db_comment`.
   embedding = VectorField(dimensions=3, db_comment="hnsw(distance=cosine)")
```

TiDB 将使用该索引来加速基于余弦距离函数的向量搜索查询。

### 存储向量

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

根据余弦距离函数，搜索与查询向量“[1, 2, 3]”语义最接近的前 3 个内容。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 搜索一定距离内的向量

搜索与查询向量“[1, 2, 3]”的余弦距离小于 0.2 的向量。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## See also

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)