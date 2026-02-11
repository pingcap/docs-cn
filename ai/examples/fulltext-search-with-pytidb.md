---
title: 全文搜索示例
summary: 使用 TiDB 全文搜索执行传统文本搜索。
---

# 全文搜索示例

本示例演示如何使用 TiDB 全文搜索构建一个支持多语言的电商产品搜索应用。该应用的用户可以使用其偏好的语言，通过关键字搜索产品。

<p align="center">
  <img width="700" alt="E-commerce product search with full-text search" src="https://docs-download.pingcap.com/media/images/docs/ai/e-commerce-product-search-with-full-text-search.png" />
  <p align="center"><i>基于全文搜索的电商产品搜索</i></p>
</p>

## 前置条件

在开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。

## 运行方法

### 步骤 1. 克隆 `pytidb` 仓库

[`pytidb`](https://github.com/pingcap/pytidb) 是官方的 TiDB Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/fulltext_search/
```

### 步骤 2. 安装所需依赖并设置环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 3. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。
3. 根据连接参数设置环境变量，如下所示：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=pytidb_fulltext_demo
EOF
```

### 步骤 4. 运行 Streamlit 应用

```bash
streamlit run app.py
```

在浏览器中访问 `http://localhost:8501`。

## 相关资源

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/fulltext_search)