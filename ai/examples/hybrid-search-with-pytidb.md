---
title: 混合搜索示例
summary: 结合向量搜索和全文搜索，获得更全面的结果。
---

# 混合搜索示例

本演示展示了如何结合向量搜索和全文搜索，以提升在文档集上的搜索质量。

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/ai/tidb-hybrid-search-demo.png" alt="TiDB Hybrid Search Demo" width="700"/>
    <p align="center"><i>TiDB Hybrid Search Demo</i></p>
</p>

## 前置条件

在开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。
- **OpenAI API key**：从 [OpenAI](https://platform.openai.com/api-keys) 获取 OpenAI API key。

> **注意**
>
> 目前，全文搜索仅在以下产品选项和区域中可用：
>
> - TiDB Cloud Starter：法兰克福（`eu-central-1`）、新加坡（`ap-southeast-1`）

## 如何运行

### 步骤 1. 克隆 `pytidb` 仓库

[pytidb](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/hybrid_search
```

### 步骤 2. 安装所需包并设置环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 3. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框，显示连接参数。
3. 根据连接参数设置环境变量，如下所示：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_hybrid_demo
OPENAI_API_KEY=<your-openai-api-key>
EOF
```

### 步骤 4. 运行演示

### 选项 1. 运行 Streamlit 应用

如果你希望通过 Web UI 查看演示，可以运行以下命令：

```bash
streamlit run app.py
```

在浏览器中访问 `http://localhost:8501`。

### 选项 2. 运行演示脚本

如果你希望通过脚本查看演示，可以运行以下命令：

```bash
python example.py
```

预期输出：

```
=== CONNECT TO TIDB ===
Connected to TiDB.

=== CREATE TABLE ===
Table created.

=== INSERT SAMPLE DATA ===
Inserted 3 rows.

=== PERFORM HYBRID SEARCH ===
Search results:
[
    {
        "_distance": 0.4740166257687124,
        "_match_score": 1.6804268,
        "_score": 0.03278688524590164,
        "id": 60013,
        "text": "TiDB is a distributed database that supports OLTP, OLAP, HTAP and AI workloads."
    },
    {
        "_distance": 0.6428459116216618,
        "_match_score": 0.78427225,
        "_score": 0.03200204813108039,
        "id": 60015,
        "text": "LlamaIndex is a Python library for building AI-powered applications."
    },
    {
        "_distance": 0.641581407158715,
        "_match_score": null,
        "_score": 0.016129032258064516,
        "id": 60014,
        "text": "PyTiDB is a Python library for developers to connect to TiDB."
    }
]
```

## 相关资源

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)