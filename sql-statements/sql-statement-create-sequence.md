---
title: CREATE SEQUENCE
summary: TiDB 数据库中 CREATE SEQUENCE 的使用概述。
---

# CREATE SEQUENCE

`CREATE SEQUENCE` 语句在 TiDB 中创建序列对象。序列是与表和 `View` 对象同级的数据库对象。序列用于以自定义方式生成序列化的 ID。

## 语法图

```ebnf+diagram
CreateSequenceStmt ::=
    'CREATE' 'SEQUENCE' IfNotExists TableName CreateSequenceOptionListOpt

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
|   'COMMENT' '='? stringLit
|   'NOMINVALUE'
|   'NO' ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' | 'CYCLE' )
|   'NOMAXVALUE'
|   'NOCACHE'
|   'CYCLE'
|   'NOCYCLE'
```

## 语法

{{< copyable "sql" >}}

```sql
CREATE [TEMPORARY] SEQUENCE [IF NOT EXISTS] sequence_name
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
| `TEMPORARY` | `false` | TiDB 目前不支持 `TEMPORARY` 选项，仅提供语法兼容。 |
| `INCREMENT` | `1` | 指定序列的增量。其正值或负值可以控制序列的增长方向。 |
| `MINVALUE` | `1` 或 `-9223372036854775807` | 指定序列的最小值。当 `INCREMENT` > `0` 时，默认值为 `1`。当 `INCREMENT` < `0` 时，默认值为 `-9223372036854775807`。 |
| `MAXVALUE` | `9223372036854775806` 或 `-1` | 指定序列的最大值。当 `INCREMENT` > `0` 时，默认值为 `9223372036854775806`。当 `INCREMENT` < `0` 时，默认值为 `-1`。 |
| `START` | `MINVALUE` 或 `MAXVALUE`| 指定序列的初始值。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |
| `CACHE` | `1000` | 指定序列在 TiDB 中的本地缓存大小。 |
| `CYCLE` | `NO CYCLE` | 指定序列是否从最小值重新开始（或递减序列的最大值）。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |

## `SEQUENCE` 函数

你可以通过以下表达式函数控制序列：

+ `NEXTVAL` 或 `NEXT VALUE FOR`

    本质上，两者都是 `NEXTVAL()` 函数，用于获取序列对象的下一个有效值。`NEXTVAL()` 函数的参数是序列的 `identifier`。

+ `LASTVAL`

    此函数获取此会话中最后使用的值。如果该值不存在，则使用 `NULL`。此函数的参数是序列的 `identifier`。

+ `SETVAL`

    此函数设置序列当前值的进程。此函数的第一个参数是序列的 `identifier`；第二个参数是 `num`。

> **注意：**
>
> 在 TiDB 的序列实现中，`SETVAL` 函数不能更改此序列的初始进程或循环进程。此函数仅根据此进程返回下一个有效值。

## 示例

+ 使用默认参数创建序列对象：

    {{< copyable "sql" >}}

    ```sql
    CREATE SEQUENCE seq;
    ```

    ```
    Query OK, 0 rows affected (0.06 sec)
    ```

+ 使用 `NEXTVAL()` 函数获取序列对象的下一个值：

    {{< copyable "sql" >}}

    ```sql
    SELECT NEXTVAL(seq);
    ```

    ```
    +--------------+
    | NEXTVAL(seq) |
    +--------------+
    |            1 |
    +--------------+
    1 row in set (0.02 sec)
    ```

+ 使用 `LASTVAL()` 函数获取此会话中序列对象最后一次调用生成的值：

    {{< copyable "sql" >}}

    ```sql
    SELECT LASTVAL(seq);
    ```

    ```
    +--------------+
    | LASTVAL(seq) |
    +--------------+
    |            1 |
    +--------------+
    1 row in set (0.02 sec)
    ```

+ 使用 `SETVAL()` 函数设置序列对象的当前值（或当前位置）：

    {{< copyable "sql" >}}

    ```sql
    SELECT SETVAL(seq, 10);
    ```

    ```
    +-----------------+
    | SETVAL(seq, 10) |
    +-----------------+
    |              10 |
    +-----------------+
    1 row in set (0.01 sec)
    ```

+ 你也可以使用 `next value for` 语法获取序列的下一个值：

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

+ 使用自定义默认参数创建序列对象：

    {{< copyable "sql" >}}

    ```sql
    CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

+ 当序列对象在此会话中未被使用时，`LASTVAL()` 函数返回 `NULL` 值。

    {{< copyable "sql" >}}

    ```sql
    SELECT LASTVAL(seq2);
    ```

    ```
    +---------------+
    | LASTVAL(seq2) |
    +---------------+
    |          NULL |
    +---------------+
    1 row in set (0.01 sec)
    ```

+ 序列对象的 `NEXTVAL()` 函数的第一个有效值是 `START` 参数的值。

    {{< copyable "sql" >}}

    ```sql
    SELECT NEXTVAL(seq2);
    ```

    ```
    +---------------+
    | NEXTVAL(seq2) |
    +---------------+
    |             3 |
    +---------------+
    1 row in set (0.00 sec)
    ```

+ 虽然 `SETVAL()` 函数可以更改序列对象的当前值，但它不能更改下一个值的算术进程规则。

    {{< copyable "sql" >}}

    ```sql
    SELECT SETVAL(seq2, 6);
    ```

    ```
    +-----------------+
    | SETVAL(seq2, 6) |
    +-----------------+
    |               6 |
    +-----------------+
    1 row in set (0.00 sec)
    ```

+ 当你使用 `NEXTVAL()` 获取下一个值时，下一个值将遵循序列定义的算术进程规则。

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

+ 你可以使用序列的下一个值作为列的默认值，如下例所示。

    {{< copyable "sql" >}}

    ```sql
    CREATE table t(a int default next value for seq2);
    ```

    ```
    Query OK, 0 rows affected (0.02 sec)
    ```

+ 在下面的示例中，未指定值，因此使用 `seq2` 的默认值。

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

+ 在下面的示例中，未指定值，因此使用 `seq2` 的默认值。但是 `seq2` 的下一个值不在上面示例中定义的范围内（`CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;`），因此返回错误。

    {{< copyable "sql" >}}

    ```sql
    INSERT into t values();
    ```

    ```
    ERROR 4135 (HY000): Sequence 'test.seq2' has run out
    ```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。其实现参考了 MariaDB 中可用的序列。

除了 `SETVAL` 函数外，所有其他函数都具有与 MariaDB 相同的_进程_。这里的"进程"意味着序列中的数字遵循序列定义的某个算术进程规则。虽然你可以使用 `SETVAL` 设置序列的当前值，但序列的后续值仍然遵循原始进程规则。

例如：

```
1, 3, 5, ...            // 序列从 1 开始，每次增加 2。
select SETVAL(seq, 6)   // 将序列的当前值设置为 6。
7, 9, 11, ...           // 后续值仍然遵循进程规则。
```

在 `CYCLE` 模式下，序列在第一轮中的初始值是 `START` 参数的值，在后续轮次中的初始值是 `MinValue`（`INCREMENT` > 0）或 `MaxValue`（`INCREMENT` < 0）的值。

## 另请参阅

* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
* [序列函数](/functions-and-operators/sequence-functions.md)
