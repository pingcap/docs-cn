---
title: ALTER SEQUENCE
summary: 介绍 ALTER SEQUENCE 在 TiDB 中的使用概况。
---

# ALTER SEQUENCE

`ALTER SEQUENCE` 语句用于在 TiDB 中修改序列对象。序列是一种与 `Table` 和 `View` 对象平级的数据库对象，用于生成自定义的序列化 ID。

## 语法图

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

## 语法说明

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

## 参数说明

|参数 | 默认值 | 描述 |
| :-- | :-- | :--|
| `INCREMENT` | `1` | 指定序列的步长。其正负值可以控制序列的增长方向。|
| `MINVALUE` | `1` 或 `-9223372036854775807` | 指定序列的最小值。当 `INCREMENT` > `0` 时，默认值为 `1`；当 `INCREMENT` < `0` 时，默认值为 `-9223372036854775807`。|
| `MAXVALUE` | `9223372036854775806` 或 `-1` | 指定序列的最大值。当 `INCREMENT` > `0` 时，默认值为 `9223372036854775806`；当 `INCREMENT` < `0` 时，默认值为 `-1`。|
| `START` | `MINVALUE` 或 `MAXVALUE` | 指定序列的初始值。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`; 当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |
| `CACHE` | `1000` | 指定每个 TiDB 本地缓存序列的大小。|
| `CYCLE` | `NO CYCLE` | 指定序列用完之后是否要循环使用。在 `CYCLE` 的情况下，当 `INCREMENT` > `0` 时，序列用完后的后续起始值为 `MINVALUE`；当 `INCREMENT` < `0` 时，序列用完后的后续起始值为 `MAXVALUE`。|

> **注意：**
>
> 在执行 `ALTER SEQUENCE ... RESTART` 之前，更改 `START` 值不会影响生成的值。

## `SEQUENCE` 函数

主要通过表达式函数来操纵序列的使用。

+ `NEXTVAL` 或 `NEXT VALUE FOR`

    本质上都是 `NEXTVAL()` 函数，获取序列对象的下一个有效值，其参数为序列的 `identifier`。

+ `LASTVAL`

    `LASTVAL()` 函数，用于获取本会话上一个使用过的值。如果没有值，则为 `NULL`，其参数为序列的 `identifier`。

+ `SETVAL`

    `SETVAL()` 函数，用于设置序列的增长。其第一参数为序列的 `identifier`，第二个参数为 `num`。

> **注意：**
>
> 在 TiDB 序列的实现中，`SETVAL` 函数并不能改变序列增长的初始步调或循环步调。在 `SETVAL` 之后只会返回符合步调规律的下一个有效的序列值。

## 示例

创建一个名为 `s1` 的序列：

```sql
CREATE SEQUENCE s1;
```

```
Query OK, 0 rows affected (0.15 sec)
```

执行以下 SQL 语句两次，获取该序列接下来的两个值：

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

将该序列的步长更改为 `2`：

```sql
ALTER SEQUENCE s1 INCREMENT=2;
```

```
Query OK, 0 rows affected (0.18 sec)
```

此时，再次获取该序列接下来的两个值：

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

从以上输出中可以看到，在执行了 `ALTER SEQUENCE` 语句后，数值的增幅为 `2`。

你还可以更改序列的其他参数。例如，可以按照以下方式更改序列的 `MAXVALUE`：

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

该语句是 TiDB 的扩展，序列的实现借鉴自 MariaDB。

除了 `SETVAL` 函数外，其他函数的“步调 (progressions)” 与 MariaDB 一致。这里的步调是指，序列中的数在定义之后会产生一定的等差关系。`SETVAL` 虽然可以将序列的当前值进行移动设置，但是后续出现的值仍会遵循原有的等差关系。

示例如下：

```
1, 3, 5, ...            // 序列遵循起始为 1、步长为 2 的等差关系。
SELECT SETVAL(seq, 6)   // 设置序列的当前值为 6。
7, 9, 11, ...           // 后续产生值仍会遵循这个等差关系。
```

在 `CYCLE` 模式下，序列的起始值第一轮为 `START`，后续轮次将会是 `MinValue` (INCREMENT > 0) 或 `MaxValue` (INCREMENT < 0)。

## 另请参阅

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
* [Sequence Functions](/functions-and-operators/sequence-functions.md)
