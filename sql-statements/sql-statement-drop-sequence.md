---
title: DROP SEQUENCE
summary: TiDB 数据库中 DROP SEQUENCE 的使用概况。
category: reference
aliases: ['/docs-cn/dev/reference/sql/statements/drop-sequence/']
---

# DROP SEQUENCE

`DROP SEQUENCE` 语句用于删除序列对象。

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

MySQL 暂无序列选项。TiDB 序列借鉴自 MariaDB。`SETVAL` 函数的步调是 TiDB 特有的，其他函数的步调与 MariaDB 保持一致。

## 另请参阅

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
