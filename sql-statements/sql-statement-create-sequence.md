---
title: CREATE SEQUENCE
summary: CREATE SEQUENCE 在 TiDB 中的使用概况
---

# CREATE SEQUENCE

`CREATE SEQUENCE` 语句用于在 TiDB 中创建序列对象。序列是一种与表、视图对象平级的数据库对象，用于生成自定义的序列化 ID。

## 语法图

```ebnf+diagram
CreateSequenceStmt ::=
    'CREATE' 'SEQUENCE' IfNotExists TableName CreateSequenceOptionListOpt CreateTableOptionListOpt

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

TableName ::=
    Identifier ('.' Identifier)?

CreateSequenceOptionListOpt ::=
    SequenceOption*

SequenceOptionList ::=
    SequenceOption

SequenceOption ::=
    ( 'INCREMENT' ( '='? | 'BY' ) | 'START' ( '='? | 'WITH' ) | ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' ) '='? ) SignedNum
|   'NOMINVALUE'
|   'NO' ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' | 'CYCLE' )
|   'NOMAXVALUE'
|   'NOCACHE'
|   'CYCLE'
|   'NOCYCLE'
```

## 语法说明

{{< copyable "sql" >}}

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

|参数 | 默认值 | 描述 |
| :-- | :-- | :--|
| `TEMPORARY` | `false` | TiDB 暂时不支持 `TEMPORARY` 选项，仅在语法上做兼容。|
| `INCREMENT` | `1` | 指定序列的步长。其正负值可以控制序列的增长方向。|
| `MINVALUE` | `1` 或 `-9223372036854775807` | 指定序列的最小值。当 `INCREMENT` > `0` 时，默认值为 `1`；当 `INCREMENT` < `0` 时，默认值为 `-9223372036854775807`。|
| `MAXVALUE` | `9223372036854775806` 或 `-1` | 指定序列的最大值。当 `INCREMENT` > `0` 时，默认值为 `9223372036854775806`；当 `INCREMENT` < `0` 时，默认值为 `-1`。|
| `START` | `MINVALUE` 或 `MAXVALUE` | 指定序列的初始值。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`; 当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。|
| `CACHE` | `1000` | 指定每个 TiDB 本地缓存序列的大小。|
| `CYCLE` | `NO CYCLE` | 指定序列用完之后是否要循环使用。在 `CYCLE` 的情况下，当 `INCREMENT` > `0` 时，序列用完后的后续起始值为 `MINVALUE`；当 `INCREMENT` < `0` 时，序列用完后的后续起始值为 `MAXVALUE`。|
| `ORDER` | `NO ORDER` | TiDB 暂时不支持 `ORDER` 选项，仅在语法上做兼容。|

## `SEQUENCE` 函数

主要通过表达式函数来操纵序列的使用。

+ `NEXTVAL` 或 `NEXT VALUE FOR`

    本质上都是 `nextval()` 函数，获取序列对象的下一个有效值，其参数为序列的 `identifier`。

+ `LASTVAL`

    `lastval()` 函数，用于获取本会话上一个使用过的值。如果没有值，则为 `NULL`，其参数为序列的 `identifier`。

+ `SETVAL`

    `setval()` 函数，用于设置序列的增长。其第一参数为序列的 `identifier`，第二个参数为 `num`。

> **注意：**
>
> 在 TiDB 序列的实现中，`SETVAL` 函数并不能改变序列增长的初始步调或循环步调。在 `SETVAL` 之后只会返回符合步调规律的下一个有效的序列值。

## 示例

+ 创建一个默认参数的序列对象。

    {{< copyable "sql" >}}

    ```sql
    CREATE SEQUENCE seq;
    ```

    ```
    Query OK, 0 rows affected (0.06 sec)
    ```

+ 使用 `nextval()` 函数获取序列对象的下一个值。

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

+ 使用 `lastval()` 函数获取本会话上一次调用序列对象所产生的值。

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

+ 使用 `setval()` 函数设置序列对象当前值的位置。

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

+ 也可使用 `next value for` 语法获取序列的下一个值。

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

+ 创建一个默认自定义参数的序列对象。

    {{< copyable "sql" >}}

    ```sql
    CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

+ 当本会话还未使用过序列对象时，`lastval()` 函数返回 NULL 值。

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

+ 序列对象 `nextval()` 的第一个有效值为 `start` 值。

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

+ 使用 `setval()` 虽然可以改变序列对象当前值的位置，但是无法改变下一个值的等差规律。

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

+ 使用 `nextval()` 下一个值获取时，会遵循序列定义的等差规律。

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

+ 可以将序列的下一个值作为列的默认值来使用。

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE t(a int default next value for seq2);
    ```

    ```
    Query OK, 0 rows affected (0.02 sec)
    ```

+ 下列示例中，因为没有指定值，会直接获取 `seq2` 的默认值来使用。

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

+ 下列示例中，因为没有指定值，会直接获取 `seq2` 的默认值来使用。由于 `seq2` 的下一个值超过了上述示例 (`CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;`) 的定义范围，所以会显示报错。

    {{< copyable "sql" >}}

    ```sql
    INSERT into t values();
    ```

    ```
    ERROR 4135 (HY000): Sequence 'test.seq2' has run out
    ```

## MySQL 兼容性

该语句是 TiDB 的扩展，序列的实现借鉴自 MariaDB。

除了 `SETVAL` 函数外，其他函数的“步调 (progressions)” 与 MariaDB 一致。这里的步调是指，序列中的数在定义之后会产生一定的等差关系。`SETVAL` 虽然可以将序列的当前值进行移动设置，但是后续出现的值仍会遵循原有的等差关系。

示例如下：

```
1, 3, 5, ...            // 序列遵循起始为 1、步长为 2 的等差关系。
select setval(seq, 6)   // 设置序列的当前值为 6。
7, 9, 11, ...           // 后续产生值仍会遵循这个等差关系。
```

在 `CYCLE` 模式下，序列的起始值第一轮为 `start`，后续轮次将会是 `MinValue` (increment > 0) 或 `MaxValue` (increment < 0)。

## 另请参阅

* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
