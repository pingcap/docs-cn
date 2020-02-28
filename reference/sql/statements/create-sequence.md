---
title: CREATE SEQUENCE
summary: CREATE SEQUENCE 在 TiDB 中的使用概况
category: reference
---

# CREATE SEQUENCE

`CREATE SEQUENCE` 语句用于在 TiDB 中创建 SEQUENCE 对象。SEQUENCE 是一种与表、视图对象平级的数据库对象，用于进行自定义的序列化 id 生成。

## 语法图

**CreateSequenceStmt:**

![CreateSequenceStmt](/media/sqlgram/CreateSequenceStmt.png)

**OptTemporary:**

![OptTemporary](/media/sqlgram/OptTemporary.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**CreateSequenceOptionListOpt:**

![CreateSequenceOptionListOpt](/media/sqlgram/CreateSequenceOptionListOpt.png)

**SequenceOption:**

![SequenceOption](/media/sqlgram/SequenceOption.png)

**CreateTableOptionListOpt:**

![CreateTableOptionListOpt](/media/sqlgram/CreateTableOptionListOpt.png)

## 语法说明

```
CREATE [TEMPORARY] SEQUENCE [IF NOT EXISTS] sequence_name
    [ INCREMENT [ BY | = ] increment ]
    [ MINVALUE [=] minvalue | NO MINVALUE | NOMINVALUE ]
    [ MAXVALUE [=] maxvalue | NO MAXVALUE | NOMAXVALUE ]
    [ START [ WITH | = ] start ]
    [ CACHE [=] cache | NOCACHE | NO CACHE]
    [ CYCLE | NOCYCLE | NO CYCLE]
    [ ORDER | NOORDER | NO ORDER]
    [table_options]
```

## 参数说明

参数 | 默认值 | 描述  
 -|-|-
INCREMENT | 1 | 指定序列的步长，其正负值可以控制 SEQUENCE 的增长方向。
MINVALUE | 1 / -9223372036854775807 | 指定序列的最小值，当 INCREMENT > 0 时，默认值为 1；当 INCREMENT < 0 时，默认值为 -9223372036854775807。
MAXVALUE | 9223372036854775806 / -1 | 指定序列的最大值，当 INCREMENT > 0 时，默认值为 9223372036854775806；当 INCREMENT < 0 时，默认值为 -1。
START | MINVALUE / MAXVALUE | 指定序列的初始值，当 INCREMENT > 0 时，默认值为 MINVALUE; 当 INCREMENT < 0 时，默认值为 MAXVALUE。
CACHE | 1000 | 指定每个 TiDB 本地缓存序列的大小，默认值为 1000。
CYCLE | false | 指定序列用完之后的是否循环使用。在 CYCLE 的情况下，当 INCREMENT > 0 时，默认值为 MINVALUE；当 INCREMENT < 0 时，默认值为 MAXVALUE。

## SEQUENCE 函数

SEQUENCE 的使用主要通过表达式函数来操纵

**NEXTVAL / NEXT VALUE FOR**

本质上都是 nextval() 函数, 获取 SEQUENCE 对象的下一个有效值，其参数为 SEQUENCE 序列的 identifier。

**LASTVAL**

lastval() 函数，用于获取本会话上一个使用过的值，如果没有则为 NULL, 其参数为 SEQUENCE 序列的 identifier。

**SETVAL**

setval() 函数，用于设置序列的增长，其第一参数为 SEQUENCE 序列的 identifier，第二个参数为 num。

> 注意：在 TiDB SEQUENCE 的实现中，setval 函数并不能改变序列增长的初始步调/循环步调，在 setval 之后只会返回符合步调规律的下一个有效的序列值。

## 示例

{{< copyable "sql" >}}

```sql
CREATE SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.06 sec)
```

{{< copyable "sql" >}}

```sql
SELECT nextval(seq);
```

```
+--------------+
| nextval(seq) |
+--------------+
|            1 |
+--------------+
1 row in set (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SELECT lastval(seq);
```

```
+--------------+
| lastval(seq) |
+--------------+
|            1 |
+--------------+
1 row in set (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SELECT setval(seq, 10);
```

```
+-----------------+
| setval(seq, 10) |
+-----------------+
|              10 |
+-----------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT next value for seq;
```

```
+--------------------+
| next value for seq |
+--------------------+
|                 11 |
+--------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT lastval(seq2);
```

```
+---------------+
| lastval(seq2) |
+---------------+
|          NULL |
+---------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT nextval(seq2);
```

```
+---------------+
| nextval(seq2) |
+---------------+
|             3 |
+---------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT setval(seq2, 6);
```

```
+-----------------+
| setval(seq2, 6) |
+-----------------+
|               6 |
+-----------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT next value for seq2;
```

```
+---------------------+
| next value for seq2 |
+---------------------+
|                   7 |
+---------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CRATE table t(a int default next value for seq2);
```

```
Query OK, 0 rows affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
INSERT into t values();
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * from t;
```

```
+------+
| a    |
+------+
|    9 |
+------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT into t values();
```

```
ERROR 4135 (HY000): Sequence 'test.seq2' has run out
```

## MySQL 兼容性

* MySQL 暂无 SEQUENCE 选项。TiDB Sequence 借鉴自 MariaDB，但是 setval 会保持原有的步调。

## 另请参阅

* [DROP SEQUENCE](/reference/sql/statements/drop-sequence.md)
* [SHOW CREATE SEQUENCE](/reference/sql/statements/show-create-sequence.md)
