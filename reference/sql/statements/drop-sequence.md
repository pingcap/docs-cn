---
title: DROP SEQUENCE
summary: TiDB 数据库中 DROP SEQUENCE 的使用概况。
category: reference
---

# DROP SEQUENCE

`DROP SEQUENCE` 语句用于删除 SEQUENCE 对象。

## 语法图

**DropSequenceStmt:**

![DropSequenceStmt](/media/sqlgram/DropSequenceStmt.png)

**OptTemporary:**

![OptTemporary](/media/sqlgram/OptTemporary.png)

**IfExists:**

![IfExists](/media/sqlgram/IfExists.png)

**TableNameList:**

![TableNameList](/media/sqlgram/TableNameList.png)

## 示例

{{< copyable "sql" >}}

```sql
DROP SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "sql" >}}

```sql
DROP SEQUENCE seq, seq2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

## MySQL 兼容性

* MySQL 暂无 SEQUENCE 选项。TiDB Sequence 借鉴自 MariaDB，但是 setval 会保持原有的步调。

## 另请参阅

* [CREATE SEQUENCE](/reference/sql/statements/create-sequence.md)
* [SHOW CREATE SEQUENCE](/reference/sql/statements/show-create-sequence.md)
