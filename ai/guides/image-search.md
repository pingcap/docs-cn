---
title: 图像搜索
summary: 了解如何在你的应用中使用图像搜索。
---

# 图像搜索

**图像搜索** 通过比较图像的视觉内容（而不仅仅是文本或元信息）来帮助你查找相似的镜像。该功能适用于电商、内容审核、数字资产管理，以及任何需要基于外观搜索或去重镜像的场景。

TiDB 通过 **向量搜索** 实现图像搜索。借助 Auto Embedding，你可以使用多模态嵌入模型，从镜像 URL、PIL 镜像或关键字文本生成镜像嵌入。TiDB 随后可以在扩展下搜索相似的向量。

> **注意：**
>
> 有关图像搜索的完整示例，请参见 [Image Search Example](/ai/examples/image-search-with-pytidb.md)。

## 基本用法

### 第 1 步. 定义嵌入函数

要生成镜像嵌入，你需要一个支持镜像输入的嵌入模型。

演示中，你可以使用 Jina AI 的多模态嵌入模型。

前往 [Jina AI](https://jina.ai/embeddings) 创建 API key，然后按如下方式初始化嵌入函数：

```python hl_lines="7"
from pytidb.embeddings import EmbeddingFunction

image_embed = EmbeddingFunction(
    # Or another provider/model that supports multimodal input
    model_name="jina_ai/jina-embedding-v4",
    api_key="{your-jina-api-key}",
    multimodal=True,
)
```

### 第 2 步. 创建表和向量字段

使用 `VectorField()` 定义用于存储镜像嵌入的向量字段。通过设置 `source_field` 参数，指定存储镜像 URL 的字段。

```python
from pytidb.schema import TableModel, Field

class ImageItem(TableModel):
    __tablename__ = "image_items"
    id: int = Field(primary_key=True)
    image_uri: str = Field()
    image_vec: list[float] = image_embed.VectorField(
        source_field="image_uri"
    )

table = client.create_table(schema=ImageItem, if_exists="overwrite")
```

### 第 3 步. 插入镜像数据

当你插入数据时，`image_vec` 字段会自动用从 `image_uri` 生成的嵌入进行填充。

```python
table.bulk_insert([
    ImageItem(image_uri="https://example.com/image1.jpg"),
    ImageItem(image_uri="https://example.com/image2.jpg"),
    ImageItem(image_uri="https://example.com/image3.jpg"),
])
```

### 第 4 步. 执行图像搜索

图像搜索是一种向量搜索。借助 Auto Embedding，你可以直接提供镜像 URL、PIL 镜像或关键字文本，每种输入都会被转换为嵌入用于相似性匹配。

#### 选项 1：通过镜像 URL 搜索

通过提供镜像 URL 搜索相似镜像：

```python
results = table.search("https://example.com/query.jpg").limit(3).to_list()
```

客户端会将镜像 URL 转换为向量。TiDB 随后通过比较向量返回最相似的镜像。

#### 选项 2：通过 PIL 镜像搜索

你也可以通过提供镜像文件或字节流来搜索相似镜像：

```python
from PIL import Image

image = Image.open("/path/to/query.jpg")

results = table.search(image).limit(3).to_list()
```

客户端会在发送给嵌入模型前，将 PIL 镜像对象转换为 Base64 字符串。

#### 选项 3：通过关键字文本搜索

你还可以通过提供关键字文本来搜索相似镜像。

例如，如果你在处理宠物镜像数据集，可以通过 “orange tabby cat” 或 “golden retriever puppy” 等关键字来查找相似镜像。

```python
results = table.search("orange tabby cat").limit(3).to_list()
```

然后，多模态嵌入模型会将关键字文本转换为能够表达其语义含义的嵌入，TiDB 会执行向量搜索，查找嵌入与该关键字嵌入最相似的镜像。

## 另请参阅

- [Auto Embedding 指南](/ai/guides/auto-embedding.md)
- [向量搜索指南](/ai/concepts/vector-search-overview.md)
- [Image Search Example](/ai/examples/image-search-with-pytidb.md)
