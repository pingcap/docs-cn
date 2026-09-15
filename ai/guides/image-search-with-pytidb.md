---
title: 图像搜索示例
summary: 使用多模态嵌入构建一个支持文搜图和图搜图的图像搜索应用。
---

# 图像搜索示例

本示例展示了如何结合 TiDB 向量搜索能力与多模态嵌入模型来构建图像搜索应用。

只需几行代码，你就可以创建一个同时理解文本和图像的搜索系统。

- **文搜图**：使用自然语言描述你想要的内容来查找宠物照片，例如“毛茸茸的橘猫”
- **图搜图**：上传一张照片，根据品种、颜色、姿态等查找视觉上相似的宠物

<p align="center">
  <img width="700" alt="PyTiDB Image Search Demo" src="https://docs-download.pingcap.com/media/images/docs/ai/pet-image-search-via-multimodal-embeddings.png" />
  <p align="center"><i>通过多模态嵌入进行宠物图像搜索</i></p>
</p>

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **一个 {{{ .starter }}} 实例**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 {{{ .starter }}} 实例。
- **Jina AI API key**：你可以从 [Jina AI Embeddings](https://jina.ai/embeddings/) 获取一个免费的 API key。

## 运行方式 {#how-to-run}

### 第 1 步：克隆 `pytidb` 仓库 {#step-1-clone-the-pytidb-repository}

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/image_search/
```

### 第 2 步：安装所需软件包 {#step-2-install-the-required-packages}

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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

JINA_AI_API_KEY={your-jina-ai-api-key}
EOF
```

### 第 4 步：下载并解压数据集 {#step-4-download-and-extract-the-dataset}

本演示使用 [Oxford Pets dataset](https://www.robots.ox.ac.uk/~vgg/data/pets/) 将宠物图像加载到数据库中以供搜索。

*适用于 Linux/MacOS：*

```bash
# Download the dataset
curl -L -o oxford_pets.tar.gz "https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz"

# Extract the dataset
mkdir -p oxford_pets
tar -xzf oxford_pets.tar.gz -C oxford_pets
```

### 第 5 步：运行应用 {#step-5-run-the-app}

```bash
streamlit run app.py
```

打开浏览器并访问 `http://localhost:8501`。

### 第 6 步：加载数据 {#step-6-load-data}

在示例应用中，你可以点击 **Load Sample Data** 按钮，将一些示例数据加载到数据库中。

如果你想加载 Oxford Pets dataset 中的全部数据，请点击 **Load All Data** 按钮。

### 第 7 步：执行搜索 {#step-7-search}

1. 在侧边栏中选择 **Search type**。
2. 输入你要查找的宠物的文本描述，或者上传一张狗或猫的照片。
3. 点击 **Search** 按钮。

## 相关资源 {#related-resources}

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/image_search)