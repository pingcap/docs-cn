---
title: 原始查询
summary: 学习如何在你的应用程序中使用原始查询。
---

# 原始查询

本指南介绍如何在你的应用程序中运行原始 SQL 查询。

## 使用原始 SQL 操作数据

使用 `客户端.执行()` 方法来执行 `INSERT`、`UPDATE`、`DELETE` 以及其他数据操作语句。

```python
client.execute("INSERT INTO chunks(text, user_id) VALUES ('sample text', 5)")
```

### SQL 注入防护

`执行()` 和 `查询()` 方法都支持 **参数化 SQL** 功能，这有助于你在构建动态 SQL 语句时避免 [SQL 注入](https://en.wikipedia.org/wiki/SQL_injection)。

```python
client.execute(
    "INSERT INTO chunks(text, user_id) VALUES (:text, :user_id)",
    {
        "text": "sample text",
        "user_id": 6,
    },
)
```

## 使用原始 SQL 查询数据

使用 `客户端.查询()` 方法来执行 `SELECT`、`SHOW` 以及其他查询语句。

### 输出查询结果

`客户端.查询()` 方法会返回一个 `SQLQueryResult` 实例，并带有一些辅助方法：

- `to_pydantic()`
- `to_list()`
- `to_pandas()`
- `to_rows()`
- `scalar()`

#### 作为 Pydantic 模型

`to_pydantic()` 方法会返回一个 Pydantic 模型列表。

```python
client.query("SELECT id, text, user_id FROM chunks").to_pydantic()
```

#### 作为 SQLAlchemy 结果行

`to_rows()` 方法会返回一个元组列表，每个元组代表一行数据。

```python
client.query("SHOW TABLES;").to_rows()
```

#### 作为字典列表

`to_list()` 方法会将查询结果转换为字典列表。

```python
client.query(
    "SELECT id, text, user_id FROM chunks WHERE user_id = :user_id",
    {
        "user_id": 3
    }
).to_list()
```

#### 作为 pandas DataFrame

`to_pandas()` 方法会将查询结果转换为 `pandas.DataFrame`，在 notebook 中以更易读的格式展示：

```python
client.query("SELECT id, text, user_id FROM chunks").to_pandas()
```

#### 作为标量值

`scalar()` 方法会返回结果集第一行的第一列。

```python
client.query("SELECT COUNT(*) FROM chunks;").scalar()
```