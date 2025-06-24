---
title: ALTER SEQUENCE
summary: TiDB 数据库中 ALTER SEQUENCE 的使用概述。
---

# ALTER SEQUENCE

`ALTER SEQUENCE` 语句用于修改 TiDB 中的序列对象。序列是与 `Table` 和 `View` 对象同级的数据库对象。序列用于以自定义方式生成序列化的 ID。

## 语法概要

```ebnf+diagram
CreateSequenceStmt ::=
    'ALTER' 'SEQUENCE' TableName CreateSequenceOptionListOpt

TableName ::=
    Identifier ('.' Identifier)?

CreateSequenceOptionListOpt ::=
    SequenceOption*

SequenceOptionList ::=
    SequenceOption

SequenceOption ::=
    ( 'INCREMENT' ( '='? | 'BY' ) | 'START' ( '='? | 'WITH' ) | ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' ) '='? ) SignedNum
|   'COMMENT' '='? stringLit
|   'NOMINVALUE'
|   'NO' ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' | 'CYCLE' )
|   'NOMAXVALUE'
|   'NOCACHE'
|   'CYCLE'
|   'NOCYCLE'
|   'RESTART' ( ( '='? | 'WITH' ) SignedNum )?
```

## 语法

```sql
ALTER SEQUENCE sequence_name
    [ INCREMENT [ BY | = ] increment ]
    [ MINVALUE [=] minvalue | NO MINVALUE | NOMINVALUE ]
    [ MAXVALUE [=] maxvalue | NO MAXVALUE | NOMAXVALUE ]
    [ START [ WITH | = ] start ]
    [ CACHE [=] cache | NOCACHE | NO CACHE]
    [ CYCLE | NOCYCLE | NO CYCLE]
    [table_options]
```

## 参数

|参数 | 默认值 | 描述 |
| :-- | :-- | :--|
| `INCREMENT` | `1` | 指定序列的增量。其正值或负值可以控制序列的增长方向。 |
| `MINVALUE` | `1` 或 `-9223372036854775807` | 指定序列的最小值。当 `INCREMENT` > `0` 时，默认值为 `1`。当 `INCREMENT` < `0` 时，默认值为 `-9223372036854775807`。 |
| `MAXVALUE` | `9223372036854775806` 或 `-1` | 指定序列的最大值。当 `INCREMENT` > `0` 时，默认值为 `9223372036854775806`。当 `INCREMENT` < `0` 时，默认值为 `-1`。 |
| `START` | `MINVALUE` 或 `MAXVALUE` | 指定序列的初始值。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |
| `CACHE` | `1000` | 指定 TiDB 中序列的本地缓存大小。 |
| `CYCLE` | `NO CYCLE` | 指定序列是否从最小值重新开始（或降序序列的最大值）。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |

> **注意：**
>
> 更改 `START` 值不会影响生成的值，直到你执行 `ALTER SEQUENCE ... RESTART`。

## `SEQUENCE` 函数

你可以通过以下表达式函数控制序列：

+ `NEXTVAL` 或 `NEXT VALUE FOR`

    本质上，两者都是 `NEXTVAL()` 函数，用于获取序列对象的下一个有效值。`NEXTVAL()` 函数的参数是序列的 `identifier`。

+ `LASTVAL`

    此函数获取此会话的最后使用值。如果该值不存在，则使用 `NULL`。此函数的参数是序列的 `identifier`。

+ `SETVAL`

    此函数设置序列当前值的进程。此函数的第一个参数是序列的 `identifier`；第二个参数是 `num`。

> **注意：**
>
> 在 TiDB 的序列实现中，`SETVAL` 函数不能更改此序列的初始进程或循环进程。此函数仅根据此进程返回下一个有效值。

## 示例

创建一个名为 `s1` 的序列：

```sql
CREATE SEQUENCE s1;
```

```
Query OK, 0 rows affected (0.15 sec)
```

通过执行以下 SQL 语句两次从序列中获取接下来的两个值：

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|           1 |
+-------------+
1 row in set (0.01 sec)
```

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|           2 |
+-------------+
1 row in set (0.00 sec)
```

将序列的增量更改为 `2`：

```sql
ALTER SEQUENCE s1 INCREMENT=2;
```

```
Query OK, 0 rows affected (0.18 sec)
```

现在，再次从序列中获取接下来的两个值：

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|        1001 |
+-------------+
1 row in set (0.02 sec)
```

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|        1003 |
+-------------+
1 row in set (0.00 sec)
```

从输出可以看出，在执行 `ALTER SEQUENCE` 语句后，值现在每次增加 2。

你还可以更改序列的其他参数。例如，你可以按如下方式更改序列的 `MAXVALUE`：

```sql
CREATE SEQUENCE s2 MAXVALUE=10;
```

```
Query OK, 0 rows affected (0.17 sec)
```

```sql
ALTER SEQUENCE s2 MAXVALUE=100;
```

```
Query OK, 0 rows affected (0.15 sec)
```

```sql
SHOW CREATE SEQUENCE s2\G
```

```
*************************** 1. row ***************************
       Sequence: s2
Create Sequence: CREATE SEQUENCE `s2` start with 1 minvalue 1 maxvalue 100 increment by 1 cache 1000 nocycle ENGINE=InnoDB
1 row in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 扩展。其实现是基于 MariaDB 中可用的序列。

除了 `SETVAL` 函数外，所有其他函数都具有与 MariaDB 相同的_进程_。这里的"进程"意味着序列中的数字遵循由序列定义的某个算术进程规则。虽然你可以使用 `SETVAL` 设置序列的当前值，但序列的后续值仍然遵循原始进程规则。

例如：

```
1, 3, 5, ...            // 序列从 1 开始，每次增加 2。
SELECT SETVAL(seq, 6)   // 将序列的当前值设置为 6。
7, 9, 11, ...           // 后续值仍然遵循进程规则。
```

在 `CYCLE` 模式下，序列在第一轮中的初始值是 `START` 参数的值，在后续轮次中的初始值是 `MinValue`（`INCREMENT` > 0）或 `MaxValue`（`INCREMENT` < 0）的值。

## 另请参阅

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
* [序列函数](/functions-and-operators/sequence-functions.md)
