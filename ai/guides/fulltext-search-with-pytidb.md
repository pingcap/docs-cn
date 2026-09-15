---
title: 全文搜索示例
summary: 使用 TiDB 全文搜索执行传统文本搜索。
---

# 全文搜索示例

本示例演示如何使用支持多语言的 TiDB 全文搜索来构建一个电商商品搜索应用。该应用的用户可以使用自己偏好的语言，通过关键字搜索商品。

<p align="center">
  <img width="700" alt="E-commerce product search with full-text search" src="https://docs-download.pingcap.com/media/images/docs/ai/e-commerce-product-search-with-full-text-search.png" />
  <p align="center"><i>使用全文搜索的电商商品搜索</i></p>
</p>

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。

## 运行方式 {#how-to-run}

### 步骤 1. 克隆 `pytidb` 仓库 {#step-1-clone-the-pytidb-repository}

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/
```

### 步骤 2. 安装所需软件包并设置环境 {#step-2-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 3. 设置环境变量 {#step-3-set-environment-variables}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框，其中列出了连接参数。
3. 根据连接参数按如下方式设置环境变量：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_fulltext_demo
EOF
```

### 步骤 4. 运行 Streamlit 应用 {#step-4-run-the-streamlit-app}

```bash
streamlit run app.py
```

打开浏览器并访问 `http://localhost:8501`。

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/fulltext_search)