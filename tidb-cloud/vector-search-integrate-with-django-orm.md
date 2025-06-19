---
title: 将 TiDB Vector Search 与 Django ORM 集成
summary: 了解如何将 TiDB Vector Search 与 Django ORM 集成以存储嵌入向量并执行语义搜索。
---

# 将 TiDB Vector Search 与 Django ORM 集成

本教程将指导您如何使用 [Django](https://www.djangoproject.com/) ORM 与 [TiDB Vector Search](/tidb-cloud/vector-search-overview.md) 交互，存储嵌入向量并执行向量搜索查询。

> **注意**
>
> TiDB Vector Search 仅适用于 TiDB Self-Managed（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

## 前提条件

完成本教程需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果您还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)的说明创建您自己的 TiDB Cloud 集群。

## 运行示例应用

您可以通过以下步骤快速了解如何将 TiDB Vector Search 与 Django ORM 集成。

### 步骤 1. 克隆代码仓库

将 `tidb-vector-python` 代码仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 步骤 2. 创建虚拟环境

为您的项目创建虚拟环境：

```bash
cd tidb-vector-python/examples/orm-django-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 步骤 3. 安装所需依赖

安装示例项目所需的依赖：

```bash
pip install -r requirements.txt
```

或者，您可以为您的项目安装以下包：

```bash
pip install Django django-tidb mysqlclient numpy python-dotenv
```

如果在安装 mysqlclient 时遇到问题，请参考 mysqlclient 官方文档。

#### 什么是 `django-tidb`

`django-tidb` 是 Django 的 TiDB 方言，它增强了 Django ORM 以支持 TiDB 特定功能（例如 TiDB Vector Search）并解决了 TiDB 和 Django 之间的兼容性问题。

安装 `django-tidb` 时，请选择与您的 Django 版本匹配的版本。例如，如果您使用的是 `django==4.2.*`，请安装 `django-tidb==4.2.*`。次要版本不需要相同。建议使用最新的次要版本。

更多信息，请参考 [django-tidb 代码仓库](https://github.com/pingcap/django-tidb)。

### 步骤 4. 配置环境变量

1. 导航到 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的 **Connect**。将显示连接对话框。

3. 确保连接对话框中的配置与您的操作环境匹配。

   - **Connection Type** 设置为 `Public`
   - **Branch** 设置为 `main`
   - **Connect With** 设置为 `General`
   - **Operating System** 与您的环境匹配。

   > **提示：**
   >
   > 如果您的程序在 Windows Subsystem for Linux (WSL) 中运行，请切换到相应的 Linux 发行版。

4. 从连接对话框复制连接参数。

   > **提示：**
   >
   > 如果您还没有设置密码，请点击 **Generate Password** 生成随机密码。

5. 在 Python 项目的根目录下创建一个 `.env` 文件，并将连接参数粘贴到相应的环境变量中。

   - `TIDB_HOST`：TiDB 集群的主机地址。
   - `TIDB_PORT`：TiDB 集群的端口。
   - `TIDB_USERNAME`：连接 TiDB 集群的用户名。
   - `TIDB_PASSWORD`：连接 TiDB 集群的密码。
   - `TIDB_DATABASE`：要连接的数据库名称。
   - `TIDB_CA_PATH`：根证书文件的路径。

   以下是 macOS 的示例：

   ```dotenv
   TIDB_HOST=gateway01.****.prod.aws.tidbcloud.com
   TIDB_PORT=4000
   TIDB_USERNAME=********.root
   TIDB_PASSWORD=********
   TIDB_DATABASE=test
   TIDB_CA_PATH=/etc/ssl/cert.pem
   ```

### 步骤 5. 运行示例

迁移数据库架构：

```bash
python manage.py migrate
```

运行 Django 开发服务器：

```bash
python manage.py runserver
```

在浏览器中访问 `http://127.0.0.1:8000` 试用示例应用。以下是可用的 API 路径：

| API 路径                                | 描述                           |
| --------------------------------------- | ------------------------------ |
| `POST: /insert_documents`               | 插入带有嵌入向量的文档。      |
| `GET: /get_nearest_neighbors_documents` | 获取 3 个最近邻文档。         |
| `GET: /get_documents_within_distance`   | 获取指定距离范围内的文档。    |

## 示例代码片段

您可以参考以下示例代码片段来完成您自己的应用程序开发。

### 连接到 TiDB 集群

在文件 `sample_project/settings.py` 中，添加以下配置：

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

您可以在项目根目录下创建一个 `.env` 文件，并使用 TiDB 集群的实际值设置环境变量 `TIDB_HOST`、`TIDB_PORT`、`TIDB_USERNAME`、`TIDB_PASSWORD`、`TIDB_DATABASE` 和 `TIDB_CA_PATH`。

### 创建向量表

#### 定义向量列

`tidb-django` 提供了一个 `VectorField` 用于在表中存储向量嵌入。

创建一个包含名为 `embedding` 的列的表，用于存储 3 维向量。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

### 存储带有嵌入向量的文档

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### 搜索最近邻文档

TiDB Vector 支持以下距离函数：

- `L1Distance`
- `L2Distance`
- `CosineDistance`
- `NegativeInnerProduct`

基于余弦距离函数搜索与查询向量 `[1, 2, 3]` 语义最接近的前 3 个文档。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 搜索指定距离范围内的文档

搜索与查询向量 `[1, 2, 3]` 的余弦距离小于 0.2 的文档。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
