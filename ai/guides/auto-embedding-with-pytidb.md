---
title: Auto Embedding 示例
summary: 使用内置嵌入模型为你的文本数据自动生成向量嵌入。
---

# Auto Embedding 示例

本示例展示了如何结合 [Auto Embedding](/ai/integrations/vector-search-auto-embedding-overview.md) 功能与 [pytidb](https://github.com/pingcap/pytidb) 客户端使用。

1. 使用 `pytidb` 客户端连接到 TiDB。
2. 定义一个表，并配置带有自动生成向量功能的 VectorField。
3. 插入纯文本数据：系统会在后台自动填充向量嵌入。
4. 使用自然语言查询执行向量搜索：系统会透明地生成向量嵌入。

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。

## 运行方式 {#how-to-run}

### 第 1 步：克隆 `pytidb` 仓库 {#step-1-clone-the-pytidb-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/auto_embedding/
```

### 第 2 步：安装所需依赖包 {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 第 3 步：设置环境变量 {#step-3-set-environment-variables}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框，其中列出了连接参数。
3. 根据连接参数按如下方式设置环境变量：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test

# Using TiDB Cloud Free embedding model by default, which does not require setting up any API key
EMBEDDING_PROVIDER=tidbcloud_free
EOF
```

### 第 4 步：运行示例 {#step-4-run-the-demo}

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

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/auto_embedding)