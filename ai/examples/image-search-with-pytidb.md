---
title: 图像搜索示例
summary: 使用多模态嵌入构建一个支持文本到图像和图像到图像搜索的图像搜索应用。
---

# 图像搜索示例

本示例展示了如何通过结合 TiDB 向量搜索能力与多模态嵌入模型，构建一个图像搜索应用。

只需几行代码，你就可以创建一个能够理解文本和图像的搜索系统。

- **Text-to-image search**：通过自然语言描述（如 “fluffy orange cat”）查找宠物照片
- **Image-to-image search**：上传一张照片，根据品种、颜色、姿势等查找视觉上相似的宠物

<p align="center">
  <img width="700" alt="PyTiDB Image Search Demo" src="https://docs-download.pingcap.com/media/images/docs/ai/pet-image-search-via-multimodal-embeddings.png" />
  <p align="center"><i>通过多模态嵌入进行宠物图像搜索</i></p>
</p>

## 前置条件

在开始之前，请确保你已具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。
- **Jina AI API key**：你可以从 [Jina AI Embeddings](https://jina.ai/embeddings/) 免费获取 API key。

## 运行方法

### 步骤 1. 克隆 `pytidb` 仓库

[`pytidb`](https://github.com/pingcap/pytidb) 是 TiDB 的官方 Python SDK，旨在帮助开发者高效构建 AI 应用。

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/image_search/
```

### 步骤 2. 安装所需依赖包

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r reqs.txt
```

### 步骤 3. 设置环境变量

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，进入 [**Clusters**](https://tidbcloud.com/clusters) 页面，然后点击目标集群名称进入其概览页面。
2. 点击右上角的 **Connect**。此时会弹出连接对话框，显示连接参数。
3. 根据连接参数设置环境变量，如下所示：

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

### 步骤 4. 下载并解压数据集

本演示使用 [Oxford Pets 数据集](https://www.robots.ox.ac.uk/~vgg/data/pets/) 将宠物图片加载到数据库中进行搜索。

*对于 Linux/MacOS：*

```bash
# 下载数据集
curl -L -o oxford_pets.tar.gz "https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz"

# 解压数据集
mkdir -p oxford_pets
tar -xzf oxford_pets.tar.gz -C oxford_pets
```

### 步骤 5. 运行应用

```bash
streamlit run app.py
```

在浏览器中访问 `http://localhost:8501`。

### 步骤 6. 加载数据

在示例应用中，你可以点击 **Load Sample Data** 按钮，将部分示例数据加载到数据库中。

如果你想加载 Oxford Pets 数据集中的全部数据，可以点击 **Load All Data** 按钮。

### 步骤 7. 搜索

1. 在侧边栏选择 **Search type**。
2. 输入你想查找的宠物的文本描述，或上传一张狗或猫的照片。
3. 点击 **Search** 按钮。

## 相关资源

- **Source Code**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/image_search)