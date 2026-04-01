---
title: 向量搜索示例
summary: 使用向量嵌入实现语义搜索，查找相似内容。
---

# 向量搜索示例

本示例演示如何使用 TiDB 和本地嵌入模型构建语义搜索应用。它通过向量搜索，根据含义（而不仅仅是关键字）查找相似项。

该应用使用 [Ollama](https://ollama.com/download) 进行本地嵌入生成，使用 [Streamlit](https://streamlit.io/) 构建 Web UI，并使用 [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 官方 Python SDK）搭建 RAG 流程。

<p align="center">
  <img width="700" alt="Semantic search with vector embeddings" src="https://docs-download.pingcap.com/media/images/docs/ai/semantic-search-with-vector-embeddings.png" />
  <p align="center"><i>基于向量嵌入的语义搜索</i></p>
</p>

## 前置条件

在开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建免费的 TiDB 集群。
- **Ollama**：从 [Ollama](https://ollama.com/download) 安装。

## 运行方法

### 步骤 1. 使用 Ollama 启动嵌入服务

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

### 步骤 2. 克隆仓库

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/vector_search/
```

### 步骤 3. 安装所需依赖并配置环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 4. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。会弹出连接对话框，显示连接参数。
3. 根据连接参数设置环境变量，如下所示：

    ```bash
    cat > .env <<EOF
    TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME={prefix}.root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=pytidb_vector_search
    EOF
    ```

### 步骤 5. 运行 Streamlit 应用

```bash
streamlit run app.py
```

在浏览器中访问 `http://localhost:8501`。

## 相关资源

- **源代码**：[在 GitHub 查看](https://github.com/pingcap/pytidb/tree/main/examples/vector_search)