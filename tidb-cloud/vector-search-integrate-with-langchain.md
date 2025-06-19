---
title: 将向量搜索与 LangChain 集成
summary: 了解如何将 TiDB Cloud 中的向量搜索与 LangChain 集成。
---

# 将向量搜索与 LangChain 集成

本教程演示如何将 TiDB Cloud 中的[向量搜索](/tidb-cloud/vector-search-overview.md)功能与 [LangChain](https://python.langchain.com/) 集成。

> **注意**
>
> TiDB 向量搜索仅适用于 TiDB 自管理版本（TiDB >= v8.4）和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)。它不适用于 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)。

> **提示**
>
> 你可以在 Jupyter Notebook 上查看完整的[示例代码](https://github.com/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb)，或直接在 [Colab](https://colab.research.google.com/github/langchain-ai/langchain/blob/master/docs/docs/integrations/vectorstores/tidb_vector.ipynb) 在线环境中运行示例代码。

## 前提条件

要完成本教程，你需要：

- 安装 [Python 3.8 或更高版本](https://www.python.org/downloads/)。
- 安装 [Jupyter Notebook](https://jupyter.org/install)。
- 安装 [Git](https://git-scm.com/downloads)。
- 一个 TiDB Cloud Serverless 集群。如果你还没有，请按照[创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md)创建自己的 TiDB Cloud 集群。

## 开始使用

本节提供将 TiDB 向量搜索与 LangChain 集成以执行语义搜索的分步说明。

### 步骤 1. 创建新的 Jupyter Notebook 文件

在你选择的目录中，创建一个名为 `integrate_with_langchain.ipynb` 的新 Jupyter Notebook 文件：

```shell
touch integrate_with_langchain.ipynb
```

### 步骤 2. 安装所需依赖

在你的项目目录中，运行以下命令安装所需的包：

```shell
!pip install langchain langchain-community
!pip install langchain-openai
!pip install pymysql
!pip install tidb-vector
```

在 Jupyter Notebook 中打开 `integrate_with_langchain.ipynb` 文件，然后添加以下代码以导入所需的包：

```python
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import TiDBVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
```

### 步骤 3. 设置环境

按照以下步骤获取集群连接字符串并配置环境变量：

1. 导航到[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击目标集群的名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个连接对话框。

3. 确保连接对话框中的配置与你的操作环境匹配。

   - **连接类型**设置为 `Public`。
   - **分支**设置为 `main`。
   - **连接方式**设置为 `SQLAlchemy`。
   - **操作系统**与你的环境匹配。

4. 点击 **PyMySQL** 标签并复制连接字符串。

   > **提示：**
   >
   > 如果你还没有设置密码，请点击**生成密码**生成一个随机密码。

5. 配置环境变量。

   本文使用 [OpenAI](https://platform.openai.com/docs/introduction) 作为嵌入模型提供者。在此步骤中，你需要提供从上一步获取的连接字符串和你的 [OpenAI API 密钥](https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key)。

   要配置环境变量，运行以下代码。系统会提示你输入连接字符串和 OpenAI API 密钥：

   ```python
   # 使用 getpass 在终端中安全地提示输入环境变量。
   import getpass
   import os

   # 从 TiDB Cloud 控制台复制你的连接字符串。
   # 连接字符串格式："mysql+pymysql://<USER>:<PASSWORD>@<HOST>:4000/<DB>?ssl_ca=/etc/ssl/cert.pem&ssl_verify_cert=true&ssl_verify_identity=true"
   tidb_connection_string = getpass.getpass("TiDB Connection String:")
   os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI API Key:")
   ```

### 步骤 4. 加载示例文档

#### 步骤 4.1 下载示例文档

在你的项目目录中，创建一个名为 `data/how_to/` 的目录，并从 [langchain-ai/langchain](https://github.com/langchain-ai/langchain) GitHub 仓库下载示例文档 [`state_of_the_union.txt`](https://github.com/langchain-ai/langchain/blob/master/docs/docs/how_to/state_of_the_union.txt)。

```shell
!mkdir -p 'data/how_to/'
!wget 'https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/docs/how_to/state_of_the_union.txt' -O 'data/how_to/state_of_the_union.txt'
```

#### 步骤 4.2 加载并拆分文档

从 `data/how_to/state_of_the_union.txt` 加载示例文档，并使用 `CharacterTextSplitter` 将其拆分为每个约 1,000 个字符的块。

```python
loader = TextLoader("data/how_to/state_of_the_union.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
```

### 步骤 5. 嵌入并存储文档向量

TiDB 向量存储支持余弦距离（`cosine`）和欧几里得距离（`l2`）来衡量向量之间的相似度。默认策略是余弦距离。

以下代码在 TiDB 中创建一个名为 `embedded_documents` 的表，该表针对向量搜索进行了优化。

```python
embeddings = OpenAIEmbeddings()
vector_store = TiDBVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    table_name="embedded_documents",
    connection_string=tidb_connection_string,
    distance_strategy="cosine",  # 默认值，另一个选项是 "l2"
)
```

执行成功后，你可以直接在 TiDB 数据库中查看和访问 `embedded_documents` 表。

### 步骤 6. 执行向量搜索

此步骤演示如何从文档 `state_of_the_union.txt` 中查询 "What did the president say about Ketanji Brown Jackson"。

```python
query = "What did the president say about Ketanji Brown Jackson"
```

#### 选项 1：使用 `similarity_search_with_score()`

`similarity_search_with_score()` 方法计算文档和查询之间的向量空间距离。这个距离作为相似度分数，由所选的 `distance_strategy` 决定。该方法返回得分最低的前 `k` 个文档。较低的分数表示文档与你的查询在含义上更相似。

```python
docs_with_score = vector_store.similarity_search_with_score(query, k=3)
for doc, score in docs_with_score:
   print("-" * 80)
   print("Score: ", score)
   print(doc.page_content)
   print("-" * 80)
```

<details>
   <summary><b>预期输出</b></summary>

```plain
--------------------------------------------------------------------------------
Score:  0.18472413652518527
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you're at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I'd like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.21757513022785557
A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she's been nominated, she's received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.

And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.

We can do both. At our border, we've installed new technology like cutting-edge scanners to better detect drug smuggling.

We've set up joint patrols with Mexico and Guatemala to catch more human traffickers.

We're putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.

We're securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.22676987253721725
And for our LGBTQ+ Americans, let's finally get the bipartisan Equality Act to my desk. The onslaught of state laws targeting transgender Americans and their families is wrong.

As I said last year, especially to our younger transgender Americans, I will always have your back as your President, so you can be yourself and reach your God-given potential.

While it often appears that we never agree, that isn't true. I signed 80 bipartisan bills into law last year. From preventing government shutdowns to protecting Asian-Americans from still-too-common hate crimes to reforming military justice.

And soon, we'll strengthen the Violence Against Women Act that I first wrote three decades ago. It is important for us to show the nation that we can come together and do big things.

So tonight I'm offering a Unity Agenda for the Nation. Four big things we can do together.

First, beat the opioid epidemic.
--------------------------------------------------------------------------------
```

</details>

#### 选项 2：使用 `similarity_search_with_relevance_scores()`

`similarity_search_with_relevance_scores()` 方法返回相关性得分最高的前 `k` 个文档。较高的分数表示文档与你的查询之间的相似度更高。

```python
docs_with_relevance_score = vector_store.similarity_search_with_relevance_scores(query, k=2)
for doc, score in docs_with_relevance_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

<details>
   <summary><b>预期输出</b></summary>

```plain
--------------------------------------------------------------------------------
Score:  0.8152758634748147
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you're at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I'd like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Score:  0.7824248697721444
A former top litigator in private practice. A former federal public defender. And from a family of public school educators and police officers. A consensus builder. Since she's been nominated, she's received a broad range of support—from the Fraternal Order of Police to former judges appointed by Democrats and Republicans.

And if we are to advance liberty and justice, we need to secure the Border and fix the immigration system.

We can do both. At our border, we've installed new technology like cutting-edge scanners to better detect drug smuggling.

We've set up joint patrols with Mexico and Guatemala to catch more human traffickers.

We're putting in place dedicated immigration judges so families fleeing persecution and violence can have their cases heard faster.

We're securing commitments and supporting partners in South and Central America to host more refugees and secure their own borders.
--------------------------------------------------------------------------------
```

</details>

### 用作检索器

在 Langchain 中，[检索器](https://python.langchain.com/v0.2/docs/concepts/#retrievers)是一个接口，它响应非结构化查询检索文档，提供比向量存储更多的功能。以下代码演示如何将 TiDB 向量存储用作检索器。

```python
retriever = vector_store.as_retriever(
   search_type="similarity_score_threshold",
   search_kwargs={"k": 3, "score_threshold": 0.8},
)
docs_retrieved = retriever.invoke(query)
for doc in docs_retrieved:
   print("-" * 80)
   print(doc.page_content)
   print("-" * 80)
```

预期输出如下：

```
--------------------------------------------------------------------------------
Tonight. I call on the Senate to: Pass the Freedom to Vote Act. Pass the John Lewis Voting Rights Act. And while you're at it, pass the Disclose Act so Americans can know who is funding our elections.

Tonight, I'd like to honor someone who has dedicated his life to serve this country: Justice Stephen Breyer—an Army veteran, Constitutional scholar, and retiring Justice of the United States Supreme Court. Justice Breyer, thank you for your service.

One of the most serious constitutional responsibilities a President has is nominating someone to serve on the United States Supreme Court.

And I did that 4 days ago, when I nominated Circuit Court of Appeals Judge Ketanji Brown Jackson. One of our nation's top legal minds, who will continue Justice Breyer's legacy of excellence.
--------------------------------------------------------------------------------
```

### 移除向量存储

要移除现有的 TiDB 向量存储，使用 `drop_vectorstore()` 方法：

```python
vector_store.drop_vectorstore()
```

## 使用元数据过滤器搜索

要优化搜索，你可以使用元数据过滤器来检索与应用的过滤器匹配的特定最近邻结果。

### 支持的元数据类型

TiDB 向量存储中的每个文档都可以与元数据配对，元数据以 JSON 对象中的键值对形式构建。键始终是字符串，而值可以是以下任何类型：

- 字符串
- 数字：整数或浮点数
- 布尔值：`true` 或 `false`

例如，以下是一个有效的元数据负载：

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

### 元数据过滤器语法

可用的过滤器包括：

- `$or`：选择匹配任一指定条件的向量。
- `$and`：选择匹配所有指定条件的向量。
- `$eq`：等于指定值。
- `$ne`：不等于指定值。
- `$gt`：大于指定值。
- `$gte`：大于或等于指定值。
- `$lt`：小于指定值。
- `$lte`：小于或等于指定值。
- `$in`：在指定的值数组中。
- `$nin`：不在指定的值数组中。

如果文档的元数据如下：

```json
{
  "page": 12,
  "book_title": "Siddhartha"
}
```

以下元数据过滤器可以匹配此文档：

```json
{ "page": 12 }
```

```json
{ "page": { "$eq": 12 } }
```

```json
{
  "page": {
    "$in": [11, 12, 13]
  }
}
```

```json
{ "page": { "$nin": [13] } }
```

```json
{ "page": { "$lt": 11 } }
```

```json
{
  "$or": [{ "page": 11 }, { "page": 12 }],
  "$and": [{ "page": 12 }, { "page": 13 }]
}
```

在元数据过滤器中，TiDB 将每个键值对视为单独的过滤器子句，并使用 `AND` 逻辑运算符组合这些子句。

### 示例

以下示例向 `TiDBVectorStore` 添加两个文档，并为每个文档添加一个 `title` 字段作为元数据：

```python
vector_store.add_texts(
    texts=[
        "TiDB Vector offers advanced, high-speed vector processing capabilities, enhancing AI workflows with efficient data handling and analytics support.",
        "TiDB Vector, starting as low as $10 per month for basic usage",
    ],
    metadatas=[
        {"title": "TiDB Vector functionality"},
        {"title": "TiDB Vector Pricing"},
    ],
)
```

预期输出如下：

```plain
[UUID('c782cb02-8eec-45be-a31f-fdb78914f0a7'),
 UUID('08dcd2ba-9f16-4f29-a9b7-18141f8edae3')]
```

使用元数据过滤器执行相似度搜索：

```python
docs_with_score = vector_store.similarity_search_with_score(
    "Introduction to TiDB Vector", filter={"title": "TiDB Vector functionality"}, k=4
)
for doc, score in docs_with_score:
    print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)
```

预期输出如下：

```plain
--------------------------------------------------------------------------------
Score:  0.12761409169211535
TiDB Vector offers advanced, high-speed vector processing capabilities, enhancing AI workflows with efficient data handling and analytics support.
--------------------------------------------------------------------------------
```

## 高级用法示例：旅行代理

本节演示将向量搜索与 Langchain 集成用于旅行代理的用例。目标是为客户创建个性化的旅行报告，帮助他们找到具有特定设施（如干净的休息室和素食选项）的机场。

该过程包括两个主要步骤：

1. 对机场评论进行语义搜索，以识别匹配所需设施的机场代码。
2. 执行 SQL 查询，将这些代码与路线信息合并，突出显示符合用户偏好的航空公司和目的地。

### 准备数据

首先，创建一个表来存储机场路线数据：

```python
# 创建一个表来存储航班计划数据。
vector_store.tidb_vector_client.execute(
    """CREATE TABLE airplan_routes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        airport_code VARCHAR(10),
        airline_code VARCHAR(10),
        destination_code VARCHAR(10),
        route_details TEXT,
        duration TIME,
        frequency INT,
        airplane_type VARCHAR(50),
        price DECIMAL(10, 2),
        layover TEXT
    );"""
)

# 向 airplan_routes 和向量表插入一些示例数据。
vector_store.tidb_vector_client.execute(
    """INSERT INTO airplan_routes (
        airport_code,
        airline_code,
        destination_code,
        route_details,
        duration,
        frequency,
        airplane_type,
        price,
        layover
    ) VALUES
    ('JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', '06:00:00', 5, 'Boeing 777', 299.99, 'None'),
    ('LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', '04:00:00', 3, 'Airbus A320', 149.99, 'None'),
    ('EFGH', 'UA', 'SEA', 'Daily flights from SFO to SEA.', '02:30:00', 7, 'Boeing 737', 129.99, 'None');
    """
)
vector_store.add_texts(
    texts=[
        "Clean lounges and excellent vegetarian dining options. Highly recommended.",
        "Comfortable seating in lounge areas and diverse food selections, including vegetarian.",
        "Small airport with basic facilities.",
    ],
    metadatas=[
        {"airport_code": "JFK"},
        {"airport_code": "LAX"},
        {"airport_code": "EFGH"},
    ],
)
```

预期输出如下：

```plain
[UUID('6dab390f-acd9-4c7d-b252-616606fbc89b'),
 UUID('9e811801-0e6b-4893-8886-60f4fb67ce69'),
 UUID('f426747c-0f7b-4c62-97ed-3eeb7c8dd76e')]
```

### 执行语义搜索

以下代码搜索具有干净设施和素食选项的机场：

```python
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 3, "score_threshold": 0.85},
)
semantic_query = "Could you recommend a US airport with clean lounges and good vegetarian dining options?"
reviews = retriever.invoke(semantic_query)
for r in reviews:
    print("-" * 80)
    print(r.page_content)
    print(r.metadata)
    print("-" * 80)
```

预期输出如下：

```plain
--------------------------------------------------------------------------------
Clean lounges and excellent vegetarian dining options. Highly recommended.
{'airport_code': 'JFK'}
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
Comfortable seating in lounge areas and diverse food selections, including vegetarian.
{'airport_code': 'LAX'}
--------------------------------------------------------------------------------
```

### 检索详细的机场信息

从搜索结果中提取机场代码并查询数据库以获取详细的路线信息：

```python
# 从元数据中提取机场代码
airport_codes = [review.metadata["airport_code"] for review in reviews]

# 执行查询以获取机场详细信息
search_query = "SELECT * FROM airplan_routes WHERE airport_code IN :codes"
params = {"codes": tuple(airport_codes)}

airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

预期输出如下：

```plain
[(1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None'),
 (2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None')]
```

### 简化流程

或者，你可以使用单个 SQL 查询简化整个流程：

```python
search_query = f"""
    SELECT
        VEC_Cosine_Distance(se.embedding, :query_vector) as distance,
        ar.*,
        se.document as airport_review
    FROM
        airplan_routes ar
    JOIN
        {TABLE_NAME} se ON ar.airport_code = JSON_UNQUOTE(JSON_EXTRACT(se.meta, '$.airport_code'))
    ORDER BY distance ASC
    LIMIT 5;
"""
query_vector = embeddings.embed_query(semantic_query)
params = {"query_vector": str(query_vector)}
airport_details = vector_store.tidb_vector_client.execute(search_query, params)
airport_details.get("result")
```

预期输出如下：

```plain
[(0.1219207353407008, 1, 'JFK', 'DL', 'LAX', 'Non-stop from JFK to LAX.', datetime.timedelta(seconds=21600), 5, 'Boeing 777', Decimal('299.99'), 'None', 'Clean lounges and excellent vegetarian dining options. Highly recommended.'),
 (0.14613754359804654, 2, 'LAX', 'AA', 'ORD', 'Direct LAX to ORD route.', datetime.timedelta(seconds=14400), 3, 'Airbus A320', Decimal('149.99'), 'None', 'Comfortable seating in lounge areas and diverse food selections, including vegetarian.'),
 (0.19840519342700513, 3, 'EFGH', 'UA', 'SEA', 'Daily flights from SFO to SEA.', datetime.timedelta(seconds=9000), 7, 'Boeing 737', Decimal('129.99'), 'None', 'Small airport with basic facilities.')]
```

### 清理数据

最后，通过删除创建的表来清理资源：

```python
vector_store.tidb_vector_client.execute("DROP TABLE airplan_routes")
```

预期输出如下：

```plain
{'success': True, 'result': 0, 'error': None}
```

## 另请参阅

- [向量数据类型](/tidb-cloud/vector-search-data-types.md)
- [向量搜索索引](/tidb-cloud/vector-search-index.md)
