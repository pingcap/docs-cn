---
title: 向量搜索
summary: 了解如何在你的应用中使用向量搜索。
---

# 向量搜索

向量搜索利用语义相似性，帮助你找到最相关的记录，即使你的查询没有明确包含所有关键字。

> **注意：**
>
> 有关向量搜索的完整示例，请参见 [向量搜索示例](/ai/examples/vector-search-with-pytidb.md)。

## 基本用法

本节展示了如何通过几个简单步骤在你的应用中使用向量搜索。在开始之前，你需要先[连接到数据库](/ai/guides/connect.md)。

### 步骤 1. 创建包含向量字段的表

<SimpleTab groupId="language">
<div label="Python" value="python">

你可以使用 `client.create_table()` 创建表，并用 `VectorField` 定义向量字段。

以下示例创建了一个包含四个列的 `documents` 表：

- `id`：表的主键。
- `text`：文档的文本内容。
- `text_vec`：文本内容的向量嵌入。
- `meta`：文档的元信息，是一个 JSON 对象。

```python hl_lines="9"
from pytidb.schema import TableModel, Field, VectorField
from pytidb.datatype import TEXT, JSON

class Document(TableModel):
    __tablename__ = "documents"

    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = VectorField(dimensions=3)
    meta: dict = Field(sa_type=JSON, default_factory=dict)

table = client.create_table(schema=Document, if_exists="overwrite")
```

`VectorField` 类接受以下参数：

- `dimensions`：向量的维度。指定后，该字段只能存储具有该精确维度的向量。
- `index`：是否为该向量字段创建[向量索引](https://docs.pingcap.com/tidbcloud/vector-search-index/)。默认为 `True`。
- `distance_metric`：用于向量索引的距离度量。支持的取值：
    - `DistanceMetric.COSINE`（默认）：余弦距离度量，适合衡量文本相似性
    - `DistanceMetric.L2`：L2 距离度量，适合衡量整体差异

</div>
<div label="SQL" value="sql">

使用 `CREATE TABLE` 语句创建表，并用 `VECTOR` 类型定义向量列。

```sql hl_lines="4 5"
CREATE TABLE documents (
    id INT PRIMARY KEY,
    text TEXT,
    text_vec VECTOR(3),
    VECTOR INDEX `vec_idx_text_vec`((VEC_COSINE_DISTANCE(`text_vec`)))
);
```

在本示例中：

- `text_vec` 列被定义为 `VECTOR(3)`，因此存储在该列的向量必须为 3 维。
- 使用 `VEC_COSINE_DISTANCE` 函数创建了向量索引，以优化向量搜索性能。

TiDB 支持两种用于向量索引的距离函数：

- `VEC_COSINE_DISTANCE`：计算两个向量的余弦距离
- `VEC_L2_DISTANCE`：计算两个向量的 L2 距离（欧氏距离）

</div>
</SimpleTab>

### 步骤 2. 向表中插入向量数据

为了演示，向表中插入一些文本及其对应的嵌入向量。

以下示例插入了三条文档记录，每条都带有一个简单的 3 维向量嵌入：

- `dog` 的向量嵌入为 `[1, 2, 1]`
- `fish` 的向量嵌入为 `[1, 2, 4]`
- `tree` 的向量嵌入为 `[1, 0, 0]`

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
table.bulk_insert([
    Document(text="dog", text_vec=[1,2,1], meta={"category": "animal"}),
    Document(text="fish", text_vec=[1,2,4], meta={"category": "animal"}),
    Document(text="tree", text_vec=[1,0,0], meta={"category": "plant"}),
])
```

</div>
<div label="SQL" value="sql">

```sql
INSERT INTO documents (id, text, text_vec, meta)
VALUES
    (1, 'dog', '[1,2,1]', '{"category": "animal"}'),
    (2, 'fish', '[1,2,4]', '{"category": "animal"}'),
    (3, 'tree', '[1,0,0]', '{"category": "plant"}');
```

> **注意：**
>
> 在实际应用中，嵌入通常由[嵌入模型](/ai/concepts/vector-search-overview.md#embedding-model)生成。

为方便起见，pytidb 提供了 Auto Embedding 功能，可以在插入、修改或查询时自动为你的文本字段生成向量嵌入，无需手动处理。

详细信息请参见 [Auto Embedding](/ai/guides/auto-embedding.md) 指南。

</div>
</SimpleTab>

### 步骤 3. 执行向量搜索

向量搜索使用向量距离度量来衡量向量之间的相似性和相关性。距离越近，记录越相关。要在表中查找最相关的文档，你需要指定一个查询向量。

以下示例假设查询为 `A swimming animal`，其向量嵌入为 `[1, 2, 3]`。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.search()` 方法执行向量搜索。默认使用 `search_mode="vector"`。

```python
table.search([1, 2, 3]).limit(3).to_list()
```

```python title="执行结果"
[
    {"id": 2, "text": "fish", "text_vec": [1,2,4], "_distance": 0.00853986601633272},
    {"id": 1, "text": "dog", "text_vec": [1,2,1], "_distance": 0.12712843905603044},
    {"id": 3, "text": "tree", "text_vec": [1,0,0], "_distance": 0.7327387580875756},
]
```

结果显示，最相关的文档是 `fish`，其距离为 `0.00853986601633272`。

</div>
<div label="SQL" value="sql">

在 `SELECT` 语句中使用 `ORDER BY <distance_function>(<column_name>, <query_vector>) LIMIT <n>` 子句，可以获取查询向量的 n 个最近邻。

以下示例使用 `vec_cosine_distance` 函数计算 `text_vec` 列中存储的向量与提供的查询向量 `[1, 2, 3]` 之间的余弦距离。

```sql
SELECT id, text, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
FROM documents
ORDER BY distance
LIMIT 3;
```

```plain title="执行结果"
+----+----------+---------------------+
| id | text     | distance            |
+----+----------+---------------------+
|  2 | fish     | 0.00853986601633272 |
|  1 | dog      | 0.12712843905603044 |
|  3 | tree     |  0.7327387580875756 |
+----+----------+---------------------+
3 rows in set (0.15 sec)
```

结果显示，最相关的文档是 `fish`，其距离为 `0.00853986601633272`。

</div>
</SimpleTab>

## 距离度量

距离度量用于衡量一对向量之间的相似性。目前，TiDB 支持以下距离度量：

<SimpleTab groupId="language">
<div label="Python" value="python">

`table.search()` API 支持以下距离度量：

| 度量名称                  | 描述                                                                 | 最佳应用场景 |
|--------------------------|---------------------------------------------------------------------|--------------|
| `DistanceMetric.COSINE`  | 计算两个向量的余弦距离（默认）。衡量向量之间的夹角。                | 文本嵌入、语义搜索 |
| `DistanceMetric.L2`      | 计算两个向量的 L2 距离（欧氏距离）。衡量直线距离。                  | 图像特征     |

要更改向量搜索使用的距离度量，可使用 `.distance_metric()` 方法。

**示例：使用 L2 距离度量**

```python
from pytidb.schema import DistanceMetric

results = (
    table.search([1, 2, 3])
        .distance_metric(DistanceMetric.L2)
        .limit(10)
        .to_list()
)
```

</div>
<div label="SQL" value="sql">

在 SQL 中，你可以在查询中直接使用以下内置函数计算向量距离：

| 函数名称                                                                                                                        | 描述                                         |
|--------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------|
| [`VEC_L2_DISTANCE`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_l2_distance)                  | 计算两个向量的 L2 距离（欧氏距离）           |
| [`VEC_COSINE_DISTANCE`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_cosine_distance)          | 计算两个向量的余弦距离                       |
| [`VEC_NEGATIVE_INNER_PRODUCT`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_negative_inner_product) | 计算两个向量的内积的相反数                   |
| [`VEC_L1_DISTANCE`](https://docs.pingcap.com/tidbcloud/vector-search-functions-and-operators/#vec_l1_distance)                  | 计算两个向量的 L1 距离（曼哈顿距离）         |

</div>
</SimpleTab>

## 距离阈值

`table.search()` API 允许你设置距离阈值，以控制返回结果的相似性。通过指定该阈值，你可以排除不够相似的向量，仅返回满足相关性标准的结果。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `.distance_threshold()` 方法为搜索结果设置最大距离。只有距离小于该阈值的记录才会被返回。

**示例：仅返回距离小于 0.5 的文档**

```python
results = table.search([1, 2, 3]).distance_threshold(0.5).limit(10).to_list()
```

</div>
<div label="SQL" value="sql">

在 SQL 中，使用带有距离函数的 `HAVING` 子句按距离过滤结果：

**示例：仅返回距离小于 0.1 的文档**

```sql
SELECT id, text, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
FROM documents
HAVING distance < 0.1
ORDER BY distance
LIMIT 10;
```

</div>
</SimpleTab>

## 距离范围

`table.search()` API 还支持指定距离范围，以进一步细化结果。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `.distance_range()` 方法同时设置最小和最大距离值。只有距离在该范围内的记录才会被返回。

**示例：仅返回距离在 0.01 到 0.05 之间的文档**

```python
results = table.search([1, 2, 3]).distance_range(0.01, 0.05).limit(10).to_list()
```

</div>
<div label="SQL" value="sql">

在 SQL 中，可在 `HAVING` 子句中使用 `BETWEEN` 或其他比较运算符指定距离范围：

**示例：仅返回距离在 0.01 到 0.05 之间的文档**

```sql
SELECT id, text, vec_l2_distance(text_vec, '[1,2,3]') AS distance
FROM documents
HAVING distance BETWEEN 0.01 AND 0.05
ORDER BY distance
LIMIT 10;
```

</div>
</SimpleTab>

## 元信息过滤 {#metadata-filtering}

作为关系型数据库，TiDB 支持丰富的 [SQL 运算符](https://docs.pingcap.com/tidbcloud/operators/)，并允许灵活组合过滤条件。

在 TiDB 中进行向量搜索时，你可以对标量字段（如整数型和字符串）或 JSON 字段进行元信息过滤。

通常，向量搜索结合元信息过滤有两种模式：

- **后过滤**：TiDB 首先在整个向量空间中执行向量搜索，获取 top-k 候选，然后对候选集应用过滤条件。向量搜索阶段通常会使用向量索引以提升性能。
- **预过滤**：TiDB 在向量搜索前先应用过滤条件。如果过滤条件选择性高，且被过滤字段有标量索引，该模式可以减少搜索空间并提升性能。

### 后过滤

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `.filter()` 方法和过滤字典为向量搜索添加过滤条件。

默认情况下，`table.search()` API 使用后过滤模式，以最大化向量索引的搜索性能。

**示例：向量搜索结合后过滤**

```python
results = (
    table.search([1, 2, 3])
        # `meta` 是 JSON 字段，其值为类似 {"category": "animal"} 的 JSON 对象
        .filter({"meta.category": "animal"})
        .num_candidate(50)
        .limit(10)
        .to_list()
)
```

> **注意：**
>
> 使用向量索引时，如果最终的 `limit` 很小，结果的准确性可能会降低。你可以通过 `.num_candidate()` 方法控制向量搜索阶段从向量索引中获取多少候选，而不改变 `limit` 参数。

> 较大的 `num_candidate` 值通常可以提升召回率，但可能降低查询性能。请根据你的数据集和准确性需求调整该值。

</div>
<div label="SQL" value="sql">

目前，向量索引仅在严格的 ANN（近似最近邻）查询中生效，例如：

```sql
SELECT * FROM <table> ORDER BY <distance_func>(<column>) LIMIT <n>
```

换句话说，不能在同一个查询中同时使用 `WHERE` 子句和向量索引。

如果你需要将向量搜索与其他过滤条件结合，可以采用后过滤模式。在该模式下，ANN 查询会被拆分为两部分：

- 内层查询使用向量索引执行向量搜索。
- 外层查询应用 `WHERE` 条件过滤结果。

```sql hl_lines="8"
SELECT *
FROM (
    SELECT id, text, meta, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
    FROM documents
    ORDER BY distance
    LIMIT 50
) candidates
WHERE meta->>'$.category' = 'animal'
ORDER BY distance
LIMIT 10;
```

> **注意：**
>
> 后过滤模式可能导致结果为空。例如，内层查询搜索到 top 50 最相似的记录，但这些记录都不满足 `WHERE` 条件。
>
> 为避免这种情况，可以适当增大**内层查询**的 `LIMIT`（如 50），以提升过滤后返回足够有效结果的概率。

有关支持的 SQL 运算符，请参见 TiDB Cloud 文档中的 [运算符](https://docs.pingcap.com/tidbcloud/operators/)。

</div>
</SimpleTab>

### 预过滤

<SimpleTab groupId="language">
<div label="Python" value="python">

要启用预过滤，在 `.filter()` 方法中设置 `prefilter=True`。

**示例：向量搜索结合预过滤**

```python
results = (
    table.search([1, 2, 3])
        .filter({"meta.category": "animal"}, prefilter=True)
        .limit(10)
        .to_list()
)
```

有关支持的过滤运算符，请参见 [过滤](/ai/guides/filtering.md)。

</div>
<div label="SQL" value="sql">

在 SQL 中，可在 `WHERE` 子句中使用 `->>` 运算符或 `JSON_EXTRACT` 访问 JSON 字段：

```sql
SELECT id, text, meta, vec_cosine_distance(text_vec, '[1,2,3]') AS distance
FROM documents
WHERE meta->>'$.category' = 'animal'
ORDER BY distance
LIMIT 10;
```

有关支持的 SQL 运算符，请参见 TiDB Cloud 文档中的 [运算符](https://docs.pingcap.com/tidbcloud/operators/)。

</div>
</SimpleTab>

## 多向量字段

TiDB 支持在单个表中定义多个向量列，便于存储和搜索不同类型的向量嵌入。

例如，你可以在同一张表中同时存储文本嵌入和图像嵌入，方便管理多模态数据。

<SimpleTab groupId="language">
<div label="Python" value="python">

你可以在 schema 中定义多个向量字段，并通过 `.vector_column()` 方法指定要搜索的向量字段。

**示例：指定搜索的向量字段**

```python hl_lines="6 8 17"
# 创建包含多个向量字段的表
class RichTextDocument(TableModel):
    __tablename__ = "rich_text_documents"
    id: int = Field(primary_key=True)
    text: str = Field(sa_type=TEXT)
    text_vec: list[float] = VectorField(dimensions=3)
    image_url: str
    image_vec: list[float] = VectorField(dimensions=3)

table = client.create_table(schema=RichTextDocument, if_exists="overwrite")

# 插入示例数据 ...

# 使用图像向量字段进行搜索
results = (
    table.search([1, 2, 3])
        .vector_column("image_vec")
        .distance_metric(DistanceMetric.COSINE)
        .limit(10)
        .to_list()
)
```

</div>
<div label="SQL" value="sql">

你可以在表中创建多个向量列，并使用合适的距离函数进行搜索：

```sql
-- 创建包含多个向量字段的表
CREATE TABLE rich_text_documents (
    id BIGINT PRIMARY KEY,
    text TEXT,
    text_vec VECTOR(3),
    image_url VARCHAR(255),
    image_vec VECTOR(3)
);

-- 插入示例数据 ...

-- 使用文本向量进行搜索
SELECT id, image_url, vec_l2_distance(image_vec, '[4,5,6]') AS image_distance
FROM rich_text_documents
ORDER BY image_distance
LIMIT 10;
```

</div>
</SimpleTab>

## 输出搜索结果

`table.search()` API 支持将搜索结果转换为多种常见数据处理格式：

### 作为 SQLAlchemy 结果行

如需处理原始 SQLAlchemy 结果行，可使用：

```python
table.search([1, 2, 3]).limit(10).to_rows()
```

### 作为 Python 字典列表

如需在 Python 中便于操作，可将结果转换为字典列表：

```python
table.search([1, 2, 3]).limit(10).to_list()
```

### 作为 pandas DataFrame

如需以用户友好的表格方式展示结果（尤其适用于 Jupyter notebook），可转换为 pandas DataFrame：

```python
table.search([1, 2, 3]).limit(10).to_pandas()
```

### 作为 Pydantic 模型实例列表

`TableModel` 类也可作为 Pydantic 模型用于表示数据实体。如需以 Pydantic 模型实例处理结果，可使用：

```python
table.search([1, 2, 3]).limit(10).to_pydantic()
```