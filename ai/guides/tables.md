---
title: 使用表
summary: 了解如何在 TiDB 中使用表。
---

# 使用表

TiDB 使用表来组织和存储相关数据集合。它提供了灵活的 schema 定义能力，因此你可以根据具体需求设计表结构。

一个表可以包含多个不同数据类型的列。支持的数据类型包括文本、数字、向量、二进制数据（`BLOB`）、JSON 等。

本文档展示了如何使用 [`pytidb`](https://github.com/pingcap/pytidb) 操作表。

`pytidb` 是 TiDB 官方的 Python SDK，旨在帮助开发者高效构建 AI 应用。

> **注意：**
>
> 完整的可运行示例请参见我们仓库中的 [basic example](https://github.com/pingcap/pytidb/tree/main/examples/basic)。

## 创建表

### 使用 TableModel

`pytidb` 提供了一个 `TableModel` class，用于表示表的 schema。该 class 兼容 [Pydantic model](https://docs.pydantic.dev/latest/concepts/models/)，可以让你以声明式方式定义表。

在以下示例中，你将创建一个名为 `items` 的表，包含以下列：

- `id`：主键列，整数型
- `content`：文本类型列
- `embedding`：3 维向量类型列
- `meta`：JSON 类型列

<SimpleTab groupId="language">
<div label="Python" value="python">

在你使用 `pytidb` [连接数据库](/ai/guides/connect.md) 并获取 `client` instance 后，可以通过 `create_table` method 创建表。

```python hl_lines="12"
from pytidb.schema import TableModel, Field, VectorField
from pytidb.datatype import TEXT, JSON

class Item(TableModel):
    __tablename__ = "items"

    id: int = Field(primary_key=True)
    content: str = Field(sa_type=TEXT)
    embedding: list[float] = VectorField(dimensions=3)
    meta: dict = Field(sa_type=JSON, default_factory=dict)

table = client.create_table(schema=Item, if_exists="overwrite")
```

`create_table` method 接受以下参数：

- `schema`：定义表结构的 `TableModel` class。
- `if_exists`：表创建模式。
    - `raise`（默认）：如果表不存在则创建；如果已存在则抛出错误。
    - `skip`：如果表不存在则创建；如果已存在则不做任何操作。
    - `overwrite`：删除已存在的表并新建。这适用于**测试和开发**，不建议在生产环境中使用。

表创建完成后，你可以使用 `table` 对象进行数据插入、修改、删除和查询。

</div>
<div label="SQL" value="sql">

使用 `CREATE TABLE` 语句创建表。

```sql
CREATE TABLE items (
    id INT PRIMARY KEY,
    content TEXT,
    embedding VECTOR(3),
    meta JSON
);
```

</div>
</SimpleTab>

## 向表中添加数据

### 使用 TableModel

你可以使用 `TableModel` instance 表示一行数据并插入到表中。

插入单条记录：

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.insert()` method 向表中插入单条记录。

```python
table.insert(
    Item(
        id=1,
        content="TiDB is a distributed SQL database",
        embedding=[0.1, 0.2, 0.3],
        meta={"category": "database"},
    )
)
```

</div>
<div label="SQL" value="sql">

使用 `INSERT INTO` 语句向表中插入单条记录。

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES (1, 'TiDB is a distributed SQL database', '[0.1, 0.2, 0.3]', '{"category": "database"}');
```

</div>
</SimpleTab>

插入多条记录：

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.bulk_insert()` method 向表中插入多条记录。

```python
table.bulk_insert([
    Item(
        id=2,
        content="GPT-4 is a large language model",
        embedding=[0.4, 0.5, 0.6],
        meta={"category": "llm"},
    ),
    Item(
        id=3,
        content="LlamaIndex is a Python library for building AI-powered applications",
        embedding=[0.7, 0.8, 0.9],
        meta={"category": "rag"},
    ),
])
```

</div>
<div label="SQL" value="sql">

使用 `INSERT INTO` 语句向表中插入多条记录。

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES
    (2, 'GPT-4 is a large language model', '[0.4, 0.5, 0.6]', '{"category": "llm"}'),
    (3, 'LlamaIndex is a Python library for building AI-powered applications', '[0.7, 0.8, 0.9]', '{"category": "rag"}');
```

</div>
</SimpleTab>

### 使用 Dict

你也可以使用 `dict` 表示行并插入到表中。这种方式更灵活，无需定义 `TableModel` 即可插入数据。

插入单条记录：

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.insert()` method 并传入字典，向表中插入单条记录。

```python
table.insert({
    "id": 1,
    "content": "TiDB is a distributed SQL database",
    "embedding": [0.1, 0.2, 0.3],
    "meta": {"category": "database"},
})
```

</div>
<div label="SQL" value="sql">

使用 `INSERT INTO` 语句向表中插入单条记录。

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES (1, 'TiDB is a distributed SQL database', '[0.1, 0.2, 0.3]', '{"category": "database"}');
```

</div>
</SimpleTab>

## 保存数据到表

`save` method 提供了一种便捷方式来插入或更新单行数据。对于一行数据，如果主键在表中不存在，则插入为新行；如果记录已存在，则覆盖整行数据。

> **注意：**
>
> 如果记录 ID 已存在于表中，`table.save()` 会覆盖整个记录。如需只修改部分字段，请使用 `table.update()`。

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.save()` method 将单条记录保存到表中。

**示例：保存新记录**

```python
saved_record = table.save(
    Item(
        id=4,
        content="Vector databases enable AI applications",
        embedding=[1.0, 1.1, 1.2],
        meta={"category": "vector-db"},
    )
)
```

**示例：保存已存在的记录（覆盖整行）**

```python
# 这将覆盖 id=1 的整行记录
updated_record = table.save(
    Item(
        id=1,  # 已存在的 ID
        content="Updated content for TiDB",
        embedding=[0.2, 0.3, 0.4],
        meta={"category": "updated"},
    )
)
```

</div>
<div label="SQL" value="sql">

使用 `INSERT ... ON DUPLICATE KEY UPDATE` 语句保存记录。

**示例：保存新记录或已存在则更新**

```sql
INSERT INTO items(id, content, embedding, meta)
VALUES (4, 'Vector databases enable AI applications', '[1.0, 1.1, 1.2]', '{"category": "vector-db"}')
ON DUPLICATE KEY UPDATE
    content = VALUES(content),
    embedding = VALUES(embedding),
    meta = VALUES(meta;
```

</div>
</SimpleTab>

## 从表中查询数据

要从表中获取记录：

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.query()` method 从表中查询记录。

**示例：获取前 10 条记录**

```python
result = table.query(limit=10).to_list()
```

</div>
<div label="SQL" value="sql">

使用 `SELECT` 语句从表中查询记录。

**示例：获取前 10 条记录**

```sql
SELECT * FROM items LIMIT 10;
```

</div>
</SimpleTab>

根据查询条件获取记录：

<SimpleTab groupId="language">
<div label="Python" value="python">

将 `filters` 参数传递给 `table.query()` method。

```python
result = table.query(
    filters={"meta.category": "database"},
    limit=10
).to_list()
```

</div>
<div label="SQL" value="sql">

使用 `WHERE` 子句过滤记录。

**示例：获取 category 为 "database" 的 10 条记录**

```sql
SELECT * FROM items WHERE meta->>'$.category' = 'database' LIMIT 10;
```

</div>
</SimpleTab>

完整的过滤操作及示例请参考 [Filtering](/ai/guides/filtering.md) 指南。

## 修改表中数据

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.update()` method 结合 [filters](/ai/guides/filtering.md) 修改记录。

**示例：修改 `id` 等于 1 的记录**

```python
table.update(
    values={
        "content": "TiDB Cloud Starter is a fully managed, auto-scaling cloud database service",
        "embedding": [0.1, 0.2, 0.4],
        "meta": {"category": "dbaas"},
    },
    filters={
        "id": 1
    },
)
```

</div>
<div label="SQL" value="sql">

使用 `UPDATE` 语句结合 [filters](/ai/guides/filtering.md) 修改记录。

**示例：修改 `id` 等于 1 的记录**

```sql
UPDATE items
SET
    content = 'TiDB Cloud Starter is a fully managed, auto-scaling cloud database service',
    embedding = '[0.1, 0.2, 0.4]',
    meta = '{"category": "dbaas"}'
WHERE
    id = 1;
```

</div>
</SimpleTab>

## 从表中删除数据

<SimpleTab groupId="language">
<div label="Python" value="python">

使用 `table.delete()` method 结合 [filters](/ai/guides/filtering.md) 删除记录。

**示例：删除 `id` 等于 2 的记录**

```python
table.delete(
    filters={
        "id": 2
    }
)
```

</div>
<div label="SQL" value="sql">

使用 `DELETE` 语句结合 [filters](/ai/guides/filtering.md) 删除记录。

**示例：删除 `id` 等于 2 的记录**

```sql
DELETE FROM items WHERE id = 2;
```

</div>
</SimpleTab>

## 清空表

<SimpleTab groupId="language">
<div label="Python" value="python">

如需删除表中所有数据但保留表结构，可使用 `table.truncate()` method。

```python
table.truncate()
```

你可以通过验证表中行数为 0 来确认表已被清空。

```python
table.rows()
```

</div>
<div label="SQL" value="sql">

如需删除表中所有数据但保留表结构，可使用 `TRUNCATE TABLE` 语句。

```sql
TRUNCATE TABLE items;
```

你可以通过验证表中行数为 0 来确认表已被清空。

```sql
SELECT COUNT(*) FROM items;
```

</div>
</SimpleTab>

## 删除表

<SimpleTab groupId="language">
<div label="Python" value="python">

如需永久从数据库中删除表，可使用 `client.drop_table()` method。

```python
client.drop_table("items")
```

你可以通过以下方式验证表已从数据库中移除：

```python
client.table_names()
```

</div>
<div label="SQL" value="sql">

如需永久从数据库中删除表，可使用 `DROP TABLE` 语句。

```sql
DROP TABLE items;
```

你可以通过以下方式验证表已从数据库中移除：

```sql
SHOW TABLES;
```

</div>
</SimpleTab>