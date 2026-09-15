---
title: 向量搜索示例
summary: 使用向量嵌入实现语义搜索，以查找相似内容。
---

# 向量搜索示例

本示例演示如何使用 TiDB 和本地嵌入模型构建一个语义搜索应用。它使用向量搜索根据语义查找相似项（而不仅仅是关键字）。

该应用使用 [Ollama](https://ollama.com/download) 在本地生成向量嵌入，使用 [Streamlit](https://streamlit.io/) 构建 Web UI，并使用 [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 的官方 Python SDK）来构建 RAG 流水线。

<p align="center">
  <img width="700" alt="Semantic search with vector embeddings" src="https://docs-download.pingcap.com/media/images/docs/ai/semantic-search-with-vector-embeddings.png" />
  <p align="center"><i>使用向量嵌入的语义搜索</i></p>
</p>

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。
- **Ollama**：从 [Ollama](https://ollama.com/download) 安装。

## 运行方法 {#how-to-run}

### 第 1 步：使用 Ollama 启动嵌入服务 {#step-1-start-the-embedding-service-with-ollama}

拉取嵌入模型：

```bash
ollama pull mxbai-embed-large
```

验证嵌入服务是否正在运行：

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

### 第 2 步：克隆仓库 {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/vector_search/
```

### 第 3 步：安装所需软件包并设置环境 {#step-3-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 第 4 步：设置环境变量 {#step-4-set-environment-variables}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页面。
2. 点击右上角的 **Connect**。此时会显示连接对话框，其中列出了连接参数。
3. 根据连接参数按如下方式设置环境变量：

    ```bash
    cat > .env <<EOF
    TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME={prefix}.root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=pytidb_vector_search
    EOF
    ```

### 第 5 步：运行 Streamlit 应用 {#step-5-run-the-streamlit-app}

```bash
streamlit run app.py
```

打开浏览器并访问 `http://localhost:8501`。

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/vector_search)