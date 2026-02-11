---
title: Auto Embedding 示例
summary: 使用内置嵌入模型为你的文本数据自动生成嵌入向量。
---

# Auto Embedding 示例

本示例展示如何通过 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 功能，结合 [pytidb](https://github.com/pingcap/pytidb) client 使用 Auto Embedding。

1. 使用 `pytidb` client 连接 TiDB。
2. 定义一个配置了 Auto Embedding 的 VectorField 的表。
3. 插入纯文本数据：嵌入向量会在后台自动填充。
4. 使用自然语言查询进行向量搜索：嵌入向量会透明地生成。

## 前置条件

在开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。

## 运行方法

### 步骤 1. 克隆 `pytidb` 仓库

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/auto_embedding/
```

### 步骤 2. 安装所需依赖包

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 3. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框，显示连接参数。
3. 根据连接参数如下设置环境变量：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test

# 默认使用 TiDB Cloud 免费嵌入模型，无需设置任何 API key
EMBEDDING_PROVIDER=tidbcloud_free
EOF
```

### 步骤 4. 运行示例

```bash
python main.py
```

**预期输出：**

```plain
=== Define embedding function ===
Embedding function (model id: tidbcloud_free/amazon/titan-embed-text-v2) defined

=== Define table schema ===
Table created

=== Truncate table ===
Table truncated

=== Insert sample data ===
Inserted 3 chunks

=== Perform vector search ===
id: 1, text: TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads., distance: 0.30373281240458805
id: 2, text: PyTiDB is a Python library for developers to connect to TiDB., distance: 0.422506501973434
id: 3, text: LlamaIndex is a Python library for building AI-powered applications., distance: 0.5267239638442787
```

## 相关资源

- **源代码**：[在 GitHub 查看](https://github.com/pingcap/pytidb/tree/main/examples/auto_embedding)