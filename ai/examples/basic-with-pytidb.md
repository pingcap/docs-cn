---
title: 增删改查基本操作
summary: 学习使用 `pytidb` 进行数据库连接、建表和数据操作等基础操作。
---

# 增删改查基本操作

本示例演示了如何使用 [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 官方 Python SDK）进行基本的 CRUD（创建、读取、修改、删除）操作。

1. 使用 `pytidb` 客户端连接 TiDB。
2. 创建包含文本、向量和 JSON 列的表。
3. 对数据执行基本的 CRUD 操作。

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上免费创建 TiDB 集群。

## 运行方法

### 步骤 1. 克隆 `pytidb` 仓库

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/basic/
```

### 步骤 2. 安装所需依赖包

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 3. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 点击右上角的 **Connect**，会弹出连接对话框，显示连接参数。
3. 根据连接参数设置环境变量，如下所示：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test
EOF
```

### 步骤 4. 运行示例

```bash
python main.py
```

*预期输出：*

```plain
=== CREATE TABLE ===
Table created

=== TRUNCATE TABLE ===
Table truncated

=== CREATE ===
Created 3 items

=== READ ===
ID: 1, Content: TiDB is a distributed SQL database, Metadata: {'category': 'database'}
ID: 2, Content: GPT-4 is a large language model, Metadata: {'category': 'llm'}
ID: 3, Content: LlamaIndex is a Python library for building AI-powered applications, Metadata: {'category': 'rag'}

=== UPDATE ===
Updated item #1
After update - ID: 1, Content: TiDB Cloud Starter is a fully-managed, auto-scaling cloud database service, Metadata: {'category': 'dbass'}

=== DELETE ===
Deleted item #2

=== FINAL STATE ===
ID: 1, Content: TiDB Cloud Starter is a fully-managed, auto-scaling cloud database service, Metadata: {'category': 'dbass'}
ID: 3, Content: LlamaIndex is a Python library for building AI-powered applications, Metadata: {'category': 'rag'}

=== COUNT ROWS ===
Number of rows: 2

=== DROP TABLE ===
Table dropped

Basic CRUD operations completed!
```

## 相关资源

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/basic)