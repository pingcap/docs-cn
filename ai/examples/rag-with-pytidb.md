---
title: RAG 示例
summary: 构建一个结合文档搜索与语言生成的 RAG 应用。
---

# RAG 示例

本示例演示如何使用 [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 官方 Python SDK）构建一个最小化的 RAG 应用。

该应用使用 [Ollama](https://ollama.com/download) 进行本地嵌入生成，使用 [Streamlit](https://streamlit.io/) 构建 Web UI，并通过 `pytidb` 搭建 RAG 流水线。

<p align="center">
  <img src="https://docs-download.pingcap.com/media/images/docs/ai/rag-application-built-with-pytidb.png" alt="RAG application built with PyTiDB" width="600" />
  <p align="center"><i>基于 PyTiDB 构建的 RAG 应用</i></p>
</p>

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。
- **Ollama**：从 [Ollama](https://ollama.com/download) 安装。

## 运行方法

### 步骤 1. 准备推理 API

使用 Ollama CLI 拉取 embedding 和 LLM 镜像：

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:4b
ollama run gemma3:4b
```

验证 `/embed` 和 `/generate` 接口是否已启动：

```bash
curl http://localhost:11434/api/embed -d '{
  "model": "mxbai-embed-large",
  "input": "Llamas are members of the camelid family"
}'
```

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:4b",
  "prompt": "Hello, Who are you?"
}'
```

### 步骤 2. 克隆仓库

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/rag/
```

### 步骤 3. 安装所需依赖并设置环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 步骤 4. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称，进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。
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

### 步骤 5. 运行 Streamlit 应用

```bash
streamlit run main.py
```

打开浏览器并访问 `http://localhost:8501`。

## 故障排查

### `502 Bad Gateway` 错误

尝试关闭你的全局代理设置。

## 相关资源

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/rag)