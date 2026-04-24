---
title: 连接 TiDB
summary: 学习如何使用 `pytidb` 客户端连接到 TiDB 数据库。
---

# 连接 TiDB

本指南介绍如何使用 `pytidb` 客户端连接到 TiDB 数据库。

## 安装依赖项

[`pytidb`](https://github.com/pingcap/pytidb) 是一个基于 [SQLAlchemy](https://sqlalchemy.org/) 构建的 Python 客户端。它提供了一系列高级 API，帮助你存储和搜索向量嵌入，无需编写原始 SQL。

要安装 Python 客户端，请运行以下命令：

```bash
pip install pytidb
```

## 使用连接参数进行连接

请根据你的 TiDB 部署类型选择相应步骤：

<SimpleTab>
<div label="TiDB Cloud Starter">

你可以[创建一个 TiDB Cloud Starter 集群](https://tidbcloud.com/free-trial/)，然后按照以下步骤在 Web 控制台获取连接参数：

1. 进入 [Clusters 页面](https://tidbcloud.com/clusters)，点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。
3. 将连接参数复制到你的代码或环境变量中。

示例代码：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="{gateway-region}.prod.aws.tidbcloud.com",
    port=4000,
    username="{prefix}.root",
    password="{password}",
    database="test",
)
```

> **注意：**
>
> 对于 TiDB Cloud Starter，当使用公共端点时，[连接数据库必须使用 TLS](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/)。`pytidb` 客户端会**自动**为 TiDB Cloud Starter 集群启用 TLS。

</div>
<div label="TiDB 自托管">

按照 [TiDB 快速上手](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb/#deploy-a-local-test-cluster) 部署一个 TiDB 集群用于测试。

示例代码：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    host="{tidb_server_host}",
    port=4000,
    username="root",
    password="{password}",
    database="test",
)
```

> **注意：**
>
> 如果你使用 `tiup playground` 部署 TiDB 集群进行测试，默认主机为 `127.0.0.1`，默认密码为空。

</div>
</SimpleTab>

连接成功后，你可以使用 `db` 对象进行表操作、数据查询等。

## 使用连接字符串进行连接

如果你更喜欢使用连接字符串（数据库 URL），可以根据你的部署类型参考以下格式：

<SimpleTab>
<div label="TiDB Cloud Starter">

你可以[创建一个 TiDB Cloud Starter 集群](https://tidbcloud.com/free-trial/)，然后按照以下步骤在 Web 控制台获取连接参数：

1. 进入 [Clusters 页面](https://tidbcloud.com/clusters)，点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。
3. 复制连接参数，并按以下格式构建连接字符串：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?ssl_verify_cert=true&ssl_verify_identity=true",
)
```

> **注意：**
>
> 对于 TiDB Cloud Starter，当使用公共端点时，[连接数据库必须使用 TLS](https://docs.pingcap.com/tidbcloud/secure-connections-to-starter-clusters/)，因此需要在连接字符串中设置 `ssl_verify_cert=true&ssl_verify_identity=true`。

</div>
<div label="TiDB 自托管">

你可以按照以下格式构建连接字符串：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient.connect(
    database_url="mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
)
```

> **注意：**
>
> 如果你使用 `tiup playground` 部署 TiDB 集群进行测试，连接字符串为：
>
> ```
> mysql+pymysql://root:@127.0.0.1:4000/test
> ```

</div>
</SimpleTab>

## 使用 SQLAlchemy 数据库引擎连接

如果你的应用已经有 SQLAlchemy 数据库引擎，可以通过 `db_engine` 参数复用：

```python title="main.py"
from pytidb import TiDBClient

db = TiDBClient(db_engine=db_engine)
```

## 后续步骤

连接到 TiDB 数据库后，你可以参考以下指南，学习如何操作你的数据：

- [表操作](/ai/guides/tables.md)：学习如何在 TiDB 中定义和管理表。
- [向量搜索](/ai/guides/vector-search.md)：使用向量嵌入进行语义搜索。
- [全文搜索](/ai/guides/vector-search-full-text-search-python.md)：通过关键字搜索文档。
- [混合搜索](/ai/guides/vector-search-hybrid-search.md)：结合向量和全文搜索，获得更相关的结果。