---
title: 混合搜索示例
summary: 结合向量搜索和全文搜索，以获得更全面的结果。
---

# 混合搜索示例

本示例演示了如何结合向量搜索和全文搜索，以提升文档集合上的检索质量。

<p align="center">
    <img src="https://docs-download.pingcap.com/media/images/docs/ai/tidb-hybrid-search-demo.png" alt="TiDB Hybrid Search Demo" width="700"/>
    <p align="center"><i>TiDB 混合搜索演示</i></p>
</p>

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。
- **OpenAI API key**：从 [OpenAI](https://platform.openai.com/api-keys) 获取 OpenAI API key。

> **注意**
>
> 当前，全文搜索仅在以下产品选项和 Region 中可用：
>
> - TiDB Cloud Starter：Frankfurt (`eu-central-1`)、Singapore (`ap-southeast-1`)

## 运行方式 {#how-to-run}

### 第 1 步：克隆 `pytidb` 仓库 {#step-1-clone-the-pytidb-repository}

[pytidb](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/hybrid_search
```

### 第 2 步：安装所需软件包并设置环境 {#step-2-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 第 3 步：设置环境变量 {#step-3-set-environment-variables}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页。
2. 点击右上角的 **Connect**。系统会显示连接对话框，其中列出了连接参数。
3. 根据连接参数按如下方式设置环境变量：

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

### 第 4 步：运行示例 {#step-4-run-the-demo}

### 选项 1：运行 Streamlit 应用 {#option-1-run-the-streamlit-app}

如果你想通过 Web UI 查看该示例，可以运行以下命令：

```bash
streamlit run app.py
```

打开浏览器并访问 `http://localhost:8501`。

### 选项 2：运行示例脚本 {#option-2-run-the-demo-script}

如果你想通过脚本查看该示例，可以运行以下命令：

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

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/hybrid_search)