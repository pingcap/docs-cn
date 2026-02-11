---
title: 将 TiDB 向量搜索集成到 Django ORM
summary: 学习如何将 TiDB 向量搜索集成到 Django ORM，用于存储嵌入向量并执行语义搜索。
aliases: ['/zh/tidb/stable/vector-search-integrate-with-django-orm/','/zh/tidb/dev/vector-search-integrate-with-django-orm/','/zh/tidbcloud/vector-search-integrate-with-django-orm/']
---

# 将 TiDB 向量搜索集成到 Django ORM

本教程将指导你如何使用 [Django](https://www.djangoproject.com/) ORM 与 [TiDB 向量搜索](/ai/concepts/vector-search-overview.md) 进行交互，存储嵌入向量，并执行向量搜索查询。

> **注意：**
>
> - 向量搜索功能目前为 Beta 版本，可能会在没有提前通知的情况下发生变更。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 向量搜索功能适用于 [TiDB 自托管](/overview.md)、[TiDB Cloud Starter](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#starter)、[TiDB Cloud Essential](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#essential) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier/#tidb-cloud-dedicated)。对于 TiDB 自托管和 TiDB Cloud Dedicated，TiDB 版本需为 v8.4.0 或更高（推荐 v8.5.0 或更高）。

## 前置条件

完成本教程，你需要：

- 已安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 已安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB 集群。

**如果你还没有 TiDB 集群，可以按如下方式创建：**

- （推荐）参考 [创建 TiDB Cloud Starter 集群](/develop/dev-guide-build-cluster-in-cloud.md) 创建属于你自己的 TiDB Cloud 集群。
- 参考 [部署本地测试 TiDB 集群](/quick-start-with-tidb.md#deploy-a-local-test-cluster) 或 [部署生产环境 TiDB 集群](/production-deployment-using-tiup.md) 创建本地集群。

## 运行示例应用

你可以按照以下步骤快速学习如何将 TiDB 向量搜索集成到 Django ORM。

### 第 1 步：克隆仓库

将 `tidb-vector-python` 仓库克隆到本地：

```shell
git clone https://github.com/pingcap/tidb-vector-python.git
```

### 第 2 步：创建虚拟环境

为你的项目创建一个虚拟环境：

```bash
cd tidb-vector-python/examples/orm-django-quickstart
python3 -m venv .venv
source .venv/bin/activate
```

### 第 3 步：安装所需依赖

为示例项目安装所需依赖：

```bash
pip install -r requirements.txt
```

或者，你也可以为你的项目单独安装以下包：

```bash
pip install Django django-tidb mysqlclient numpy python-dotenv
```

如果在安装 mysqlclient 时遇到问题，请参考 mysqlclient 官方文档。

#### 什么是 `django-tidb`？

`django-tidb` 是 Django 的 TiDB 方言，增强了 Django ORM 对 TiDB 特性的支持（例如向量搜索），并解决了 TiDB 与 Django 之间的兼容性问题。

安装 `django-tidb` 时，请选择与你的 Django 版本相匹配的版本。例如，如果你使用的是 `django==4.2.*`，则安装 `django-tidb==4.2.*`。小版本号无需完全一致，建议使用最新的小版本。

更多信息请参考 [django-tidb 仓库](https://github.com/pingcap/django-tidb)。

### 第 4 步：配置环境变量

根据你选择的 TiDB 部署方式，配置环境变量。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

对于 TiDB Cloud Starter 集群，按如下步骤获取集群连接字符串并配置环境变量：

1. 进入 [**Clusters**](https://tidbcloud.com/console/clusters) 页面，点击目标集群名称进入集群概览页。

2. 点击右上角的 **Connect**，弹出连接对话框。

3. 确保连接对话框中的配置与你的运行环境一致。

    - **Connection Type** 设置为 `Public`
    - **Branch** 设置为 `main`
    - **Connect With** 设置为 `General`
    - **Operating System** 与你的环境一致

    > **提示：**
    >
    > 如果你的程序运行在 Windows Subsystem for Linux (WSL) 中，请切换到对应的 Linux 发行版。

4. 从连接对话框中复制连接参数。

    > **提示：**
    >
    > 如果你还未设置密码，可点击 **Generate Password** 生成随机密码。

5. 在你的 Python 项目根目录下创建 `.env` 文件，并将连接参数粘贴到对应的环境变量中。

    - `TIDB_HOST`：TiDB 集群的主机。
    - `TIDB_PORT`：TiDB 集群的端口。
    - `TIDB_USERNAME`：连接 TiDB 集群的用户名。
    - `TIDB_PASSWORD`：连接 TiDB 集群的密码。
    - `TIDB_DATABASE`：要连接的数据库名。
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

</div>
<div label="TiDB 自托管" value="tidb">

对于 TiDB 自建集群，在你的 Python 项目根目录下创建 `.env` 文件。将以下内容复制到 `.env` 文件中，并根据你的 TiDB 集群连接参数修改环境变量的值：

```dotenv
TIDB_HOST=127.0.0.1
TIDB_PORT=4000
TIDB_USERNAME=root
TIDB_PASSWORD=
TIDB_DATABASE=test
```

如果你在本地运行 TiDB，`TIDB_HOST` 默认为 `127.0.0.1`。初始 `TIDB_PASSWORD` 为空，因此如果是首次启动集群，可以省略该字段。

各参数说明如下：

- `TIDB_HOST`：TiDB 集群的主机。
- `TIDB_PORT`：TiDB 集群的端口。
- `TIDB_USERNAME`：连接 TiDB 集群的用户名。
- `TIDB_PASSWORD`：连接 TiDB 集群的密码。
- `TIDB_DATABASE`：要连接的数据库名。

</div>

</SimpleTab>

### 第 5 步：运行示例

迁移数据库 schema：

```bash
python manage.py migrate
```

运行 Django 开发服务器：

```bash
python manage.py runserver
```

在浏览器中访问 `http://127.0.0.1:8000` 体验示例应用。可用的 API 路径如下：

| API Path                                | 说明                                   |
| --------------------------------------- | -------------------------------------- |
| `POST: /insert_documents`               | 插入带有嵌入向量的文档。               |
| `GET: /get_nearest_neighbors_documents` | 获取 3 个最近邻文档。                  |
| `GET: /get_documents_within_distance`   | 获取距离在指定范围内的文档。           |

## 示例代码片段

你可以参考以下示例代码片段，完成你自己的应用开发。

### 连接 TiDB 集群

在 `sample_project/settings.py` 文件中添加如下配置：

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

你可以在项目根目录下创建 `.env` 文件，并将 `TIDB_HOST`、`TIDB_PORT`、`TIDB_USERNAME`、`TIDB_PASSWORD`、`TIDB_DATABASE` 和 `TIDB_CA_PATH` 等环境变量设置为你实际的 TiDB 集群参数。

### 创建向量表

#### 定义向量列

`tidb-django` 提供了 `VectorField`，用于在表中存储向量嵌入。

创建一个包含名为 `embedding` 的 3 维向量列的表。

```python
class Document(models.Model):
   content = models.TextField()
   embedding = VectorField(dimensions=3)
```

### 存储带嵌入向量的文档

```python
Document.objects.create(content="dog", embedding=[1, 2, 1])
Document.objects.create(content="fish", embedding=[1, 2, 4])
Document.objects.create(content="tree", embedding=[1, 0, 0])
```

### 搜索最近邻文档

TiDB 向量搜索支持以下距离函数：

- `L1Distance`
- `L2Distance`
- `CosineDistance`
- `NegativeInnerProduct`

基于余弦距离函数，搜索与查询向量 `[1, 2, 3]` 语义最接近的前 3 个文档。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).order_by('distance')[:3]
```

### 搜索距离在指定范围内的文档

搜索与查询向量 `[1, 2, 3]` 余弦距离小于 0.2 的文档。

```python
results = Document.objects.annotate(
   distance=CosineDistance('embedding', [1, 2, 3])
).filter(distance__lt=0.2).order_by('distance')[:3]
```

## 另请参阅

- [向量数据类型](/ai/reference/vector-search-data-types.md)
- [向量搜索索引](/ai/reference/vector-search-index.md)
