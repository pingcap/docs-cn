---
title: 多表连接
summary: 学习如何在你的应用中使用多表连接。
---

# 多表连接

作为一个关系型数据库，TiDB 允许你在同一个数据库中以不同结构（例如，`chunks`、`documents`、`users`、`chats`）存储多样化的数据。你还可以使用连接操作，将来自多个表的数据组合在一起，执行复杂的查询。

## 基本用法

### 第 1 步：创建表并插入示例数据

<SimpleTab groupId="language">
<div label="Python" value="python">

假设你已经使用 `TiDBClient` [连接到 TiDB](/ai/guides/connect.md)：

创建一个 `documents` 表并插入一些示例数据：

```python
from pytidb import Session
from pytidb.schema import TableModel, Field
from pytidb.sql import select

class Document(TableModel):
    __tablename__ = "documents"
    id: int = Field(primary_key=True)
    title: str = Field(max_length=255)

client.create_table(schema=Document, if_exists="overwrite")
client.table("documents").truncate()
client.table("documents").bulk_insert([
    Document(id=1, title="The Power of Positive Thinking"),
    Document(id=2, title="The Happiness Advantage"),
    Document(id=3, title="The Art of Happiness"),
])
```

创建一个 `chunks` 表并插入一些示例数据：

```python
class Chunk(TableModel):
    __tablename__ = "chunks"
    id: int = Field(primary_key=True)
    text: str = Field(max_length=255)
    document_id: int = Field(foreign_key="documents.id")

client.create_table(schema=Chunk, if_exists="overwrite")
client.table("chunks").truncate()
client.table("chunks").bulk_insert([
    Chunk(id=1, text="Positive thinking can change your life", document_id=1),
    Chunk(id=2, text="Happiness leads to success", document_id=2),
    Chunk(id=3, text="Finding joy in everyday moments", document_id=3),
])
```

</div>
<div label="SQL" value="sql">

创建一个 `documents` 表并插入一些示例数据：

```sql
CREATE TABLE documents (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL
);

INSERT INTO documents (id, title) VALUES
    (1, 'The Power of Positive Thinking'),
    (2, 'The Happiness Advantage'),
    (3, 'The Art of Happiness');
```

创建一个 `chunks` 表并插入一些示例数据：

```sql
CREATE TABLE chunks (
    id INT PRIMARY KEY,
    text VARCHAR(255) NOT NULL,
    document_id INT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

INSERT INTO chunks (id, text, document_id) VALUES
    (1, 'Positive thinking can change your life', 1),
    (2, 'Happiness leads to success', 2),
    (3, 'Finding joy in everyday moments', 3);
```

</div>
</SimpleTab>

### 第 2 步：执行连接查询

<SimpleTab groupId="language">
<div label="Python" value="python">

```python
with Session(client.db_engine) as db_session:
    query = (
        select(Chunk)
        .join(Document, Chunk.document_id == Document.id)
        .where(Document.title == "The Power of Positive Thinking")
    )
    chunks = db_session.exec(query).all()

[(c.id, c.text, c.document_id) for c in chunks]
```

</div>
<div label="SQL" value="sql">

执行连接查询，将 `chunks` 和 `documents` 表中的数据组合在一起：

```sql
SELECT c.id, c.text, c.document_id
FROM chunks c
JOIN documents d ON c.document_id = d.id
WHERE d.title = 'The Power of Positive Thinking';
```

</div>
</SimpleTab>