---
title: RAG 示例
summary: 构建一个结合文档检索与语言生成的 RAG 应用。
---

# RAG 示例

本示例演示如何使用 [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 官方 Python SDK）构建一个最小化的 RAG 应用。

该应用使用 [Ollama](https://ollama.com/download) 在本地生成向量嵌入，使用 [Streamlit](https://streamlit.io/) 构建 Web UI，并使用 `pytidb` 搭建 RAG 流水线。

<p align="center">
  <img src="https://docs-download.pingcap.com/media/images/docs/ai/rag-application-built-with-pytidb.png" alt="RAG application built with PyTiDB" width="600" />
  <p align="center"><i>使用 PyTiDB 构建的 RAG 应用</i></p>
</p>

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。
- **Ollama**：从 [Ollama](https://ollama.com/download) 安装。

## 运行方法 {#how-to-run}

### 第 1 步：准备推理 API {#step-1-prepare-the-inference-api}

使用 Ollama CLI 拉取向量嵌入模型和 LLM 模型：

```bash
ollama pull mxbai-embed-large
ollama pull gemma3:4b
ollama run gemma3:4b
```

验证 `/embed` 和 `/generate` 端点是否正在运行：

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

### 第 2 步：克隆仓库 {#step-2-clone-the-repository}

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/rag/
```

### 第 3 步：安装所需软件包并设置环境 {#step-3-install-the-required-packages-and-set-up-the-environment}

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 第 4 步：设置环境变量 {#step-4-set-environment-variables}

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 实例的名称，进入其实例概览页。
2. 点击右上角的 **Connect**。此时会显示连接对话框，其中列出了连接参数。
3. 根据连接参数按如下方式设置环境变量：

```bash
cat > .env <<EOF
TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
TIDB_PORT=4000
TIDB_USERNAME={prefix}.root
TIDB_PASSWORD={password}
TIDB_DATABASE=test
EOF
```

### 第 5 步：运行 Streamlit 应用 {#step-5-run-the-streamlit-app}

```bash
streamlit run main.py
```

打开浏览器并访问 `http://localhost:8501`。

## 故障排查 {#troubleshooting}

### `502 Bad Gateway` 错误 {#502-bad-gateway-error}

尝试禁用全局代理设置。

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/rag)