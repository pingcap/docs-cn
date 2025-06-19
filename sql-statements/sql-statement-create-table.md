---
title: CREATE TABLE | TiDB SQL 语句参考
summary: TiDB 数据库中 CREATE TABLE 的使用概览。
---

# CREATE TABLE

此语句在当前选择的数据库中创建一个新表。它的行为类似于 MySQL 中的 `CREATE TABLE` 语句。

## 语法

```ebnf+diagram
CreateTableStmt ::=
    'CREATE' OptTemporary 'TABLE' IfNotExists TableName ( TableElementListOpt CreateTableOptionListOpt PartitionOpt DuplicateOpt AsOpt CreateTableSelectOpt | LikeTableWithOrWithoutParen ) OnCommitOpt

OptTemporary ::=
    ( 'TEMPORARY' | ('GLOBAL' 'TEMPORARY') )?

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

TableName ::=
    Identifier ('.' Identifier)?

TableElementListOpt ::=
    ( '(' TableElementList ')' )?

TableElementList ::=
    TableElement ( ',' TableElement )*

TableElement ::=
    ColumnDef
|   Constraint

ColumnDef ::=
    ColumnName ( Type | 'SERIAL' ) ColumnOptionListOpt

ColumnOptionListOpt ::=
    ColumnOption*

ColumnOptionList ::=
    ColumnOption*

ColumnOption ::=
    'NOT'? 'NULL'
|   'AUTO_INCREMENT'
|   PrimaryOpt 'KEY'
|   'UNIQUE' 'KEY'?
|   'DEFAULT' DefaultValueExpr
|   'SERIAL' 'DEFAULT' 'VALUE'
|   'ON' 'UPDATE' NowSymOptionFraction
|   'COMMENT' stringLit
|   ConstraintKeywordOpt 'CHECK' '(' Expression ')' EnforcedOrNotOrNotNullOpt
|   GeneratedAlways 'AS' '(' Expression ')' VirtualOrStored
|   ReferDef
|   'COLLATE' CollationName
|   'COLUMN_FORMAT' ColumnFormat
|   'STORAGE' StorageMedia
|   'AUTO_RANDOM' OptFieldLen

Constraint ::=
    IndexDef
|   ForeignKeyDef

IndexDef ::=
    ( 'INDEX' | 'KEY' ) IndexName? '(' KeyPartList ')' IndexOption?

KeyPartList ::=
    KeyPart ( ',' KeyPart )*

KeyPart ::=
    ColumnName ( '(' Length ')')? ( 'ASC' | 'DESC' )?
|   '(' Expression ')' ( 'ASC' | 'DESC' )?

IndexOption ::=
    'COMMENT' String
|   ( 'VISIBLE' | 'INVISIBLE' )
|   ('USING' | 'TYPE') ('BTREE' | 'RTREE' | 'HASH')

ForeignKeyDef
         ::= ( 'CONSTRAINT' Identifier )? 'FOREIGN' 'KEY'
             Identifier? '(' ColumnName ( ',' ColumnName )* ')'
             'REFERENCES' TableName '(' ColumnName ( ',' ColumnName )* ')'
             ( 'ON' 'DELETE' ReferenceOption )?
             ( 'ON' 'UPDATE' ReferenceOption )?

ReferenceOption
         ::= 'RESTRICT'
           | 'CASCADE'
           | 'SET' 'NULL'
           | 'SET' 'DEFAULT'
           | 'NO' 'ACTION'

CreateTableOptionListOpt ::=
    TableOptionList?

PartitionOpt ::=
    ( 'PARTITION' 'BY' PartitionMethod PartitionNumOpt SubPartitionOpt PartitionDefinitionListOpt )?

DuplicateOpt ::=
    ( 'IGNORE' | 'REPLACE' )?

TableOptionList ::=
    TableOption ( ','? TableOption )*

TableOption ::=
    PartDefOption
|   DefaultKwdOpt ( CharsetKw EqOpt CharsetName | 'COLLATE' EqOpt CollationName )
|   ( 'AUTO_INCREMENT' | 'AUTO_ID_CACHE' | 'AUTO_RANDOM_BASE' | 'AVG_ROW_LENGTH' | 'CHECKSUM' | 'TABLE_CHECKSUM' | 'KEY_BLOCK_SIZE' | 'DELAY_KEY_WRITE' | 'SHARD_ROW_ID_BITS' | 'PRE_SPLIT_REGIONS' ) EqOpt LengthNum
|   ( 'CONNECTION' | 'PASSWORD' | 'COMPRESSION' ) EqOpt stringLit
|   RowFormat
|   ( 'STATS_PERSISTENT' | 'PACK_KEYS' ) EqOpt StatsPersistentVal
|   ( 'STATS_AUTO_RECALC' | 'STATS_SAMPLE_PAGES' ) EqOpt ( LengthNum | 'DEFAULT' )
|   'STORAGE' ( 'MEMORY' | 'DISK' )
|   'SECONDARY_ENGINE' EqOpt ( 'NULL' | StringName )
|   'UNION' EqOpt '(' TableNameListOpt ')'
|   'ENCRYPTION' EqOpt EncryptionOpt
|    'TTL' EqOpt TimeColumnName '+' 'INTERVAL' Expression TimeUnit (TTLEnable EqOpt ( 'ON' | 'OFF' ))? (TTLJobInterval EqOpt stringLit)?
|   PlacementPolicyOption

OnCommitOpt ::=
    ('ON' 'COMMIT' 'DELETE' 'ROWS')?

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"

DefaultValueExpr ::=
    NowSymOptionFractionParentheses
|   SignedLiteral
|   NextValueForSequenceParentheses
|   BuiltinFunction

BuiltinFunction ::=
    '(' BuiltinFunction ')'
|   identifier '(' ')'
|   identifier '(' ExpressionList ')'
|   "REPLACE" '(' ExpressionList ')'

NowSymOptionFractionParentheses ::=
    '(' NowSymOptionFractionParentheses ')'
|   NowSymOptionFraction

NowSymOptionFraction ::=
    NowSym
|   NowSymFunc '(' ')'
|   NowSymFunc '(' NUM ')'
|   CurdateSym '(' ')'
|   "CURRENT_DATE"

NextValueForSequenceParentheses ::=
    '(' NextValueForSequenceParentheses ')'
|   NextValueForSequence

NextValueForSequence ::=
    "NEXT" "VALUE" forKwd TableName
|   "NEXTVAL" '(' TableName ')'
```

支持以下 *table_options*。其他选项如 `AVG_ROW_LENGTH`、`CHECKSUM`、`COMPRESSION`、`CONNECTION`、`DELAY_KEY_WRITE`、`ENGINE`、`KEY_BLOCK_SIZE`、`MAX_ROWS`、`MIN_ROWS`、`ROW_FORMAT` 和 `STATS_PERSISTENT` 会被解析但忽略。

| 选项 | 描述 | 示例 |
| ---------- | ---------- | ------- |
| `AUTO_INCREMENT` | 自增字段的初始值 | `AUTO_INCREMENT` = 5 |
| [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)| 设置隐式 `_tidb_rowid` 分片的位数 |`SHARD_ROW_ID_BITS` = 4|
|`PRE_SPLIT_REGIONS`| 在创建表时预先切分 `2^(PRE_SPLIT_REGIONS)` 个 Region |`PRE_SPLIT_REGIONS` = 4|
|`AUTO_ID_CACHE`| 设置 TiDB 实例中的自动 ID 缓存大小。默认情况下，TiDB 会根据自动 ID 的分配速度自动调整此大小 |`AUTO_ID_CACHE` = 200 |
|`AUTO_RANDOM_BASE`| 设置 auto_random 的初始增量部分值。此选项可以被视为内部接口的一部分。用户可以忽略此参数 |`AUTO_RANDOM_BASE` = 0|
| `CHARACTER SET` | 指定表的[字符集](/character-set-and-collation.md) | `CHARACTER SET` =  'utf8mb4' |
| `COMMENT` | 注释信息 | `COMMENT` = 'comment info' |

<CustomContent platform="tidb">

> **注意：**
>
> `split-table` 配置选项默认启用。启用时，为每个新创建的表创建单独的 Region。详情请参见 [TiDB 配置文件](/tidb-configuration-file.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> TiDB 为每个新创建的表创建单独的 Region。

</CustomContent>

## 示例

创建一个简单的表并插入一行：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a int);
DESC t1;
SHOW CREATE TABLE t1\G
INSERT INTO t1 (a) VALUES (1);
SELECT * FROM t1;
```

```
mysql> drop table if exists t1;
Query OK, 0 rows affected (0.23 sec)

mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.09 sec)

mysql> DESC t1;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.00 sec)

mysql> INSERT INTO t1 (a) VALUES (1);
Query OK, 1 row affected (0.03 sec)

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

如果表存在则删除，如果表不存在则有条件地创建表：

{{< copyable "sql" >}}

```sql
DROP TABLE IF EXISTS t1;
CREATE TABLE IF NOT EXISTS t1 (
 id BIGINT NOT NULL PRIMARY KEY auto_increment,
 b VARCHAR(200) NOT NULL
);
DESC t1;
```

```sql
mysql> DROP TABLE IF EXISTS t1;
Query OK, 0 rows affected (0.22 sec)

mysql> CREATE TABLE IF NOT EXISTS t1 (
         id BIGINT NOT NULL PRIMARY KEY auto_increment,
         b VARCHAR(200) NOT NULL
        );
Query OK, 0 rows affected (0.08 sec)

mysql> DESC t1;
+-------+--------------+------+------+---------+----------------+
| Field | Type         | Null | Key  | Default | Extra          |
+-------+--------------+------+------+---------+----------------+
| id    | bigint(20)   | NO   | PRI  | NULL    | auto_increment |
| b     | varchar(200) | NO   |      | NULL    |                |
+-------+--------------+------+------+---------+----------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* 支持除空间类型外的所有数据类型。
* TiDB 在语法上接受 `HASH`、`BTREE` 和 `RTREE` 等索引类型以与 MySQL 兼容，但会忽略它们。
* TiDB 支持解析 `FULLTEXT` 语法，但不支持使用 `FULLTEXT` 索引。

<CustomContent platform="tidb">

* 为了兼容性，`index_col_name` 属性支持长度选项，默认最大长度限制为 3072 字节。可以通过 `max-index-length` 配置选项更改长度限制。详情请参见 [TiDB 配置文件](/tidb-configuration-file.md#max-index-length)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* 为了兼容性，`index_col_name` 属性支持长度选项，最大长度限制为 3072 字节。

</CustomContent>

* `index_col_name` 中的 `[ASC | DESC]` 目前会被解析但忽略（与 MySQL 5.7 兼容的行为）。
* `COMMENT` 属性不支持 `WITH PARSER` 选项。
* TiDB 默认支持单个表中的 1017 列，最多支持 4096 列。InnoDB 中对应的限制是 1017 列，MySQL 的硬限制是 4096 列。详情请参见 [TiDB 限制](/tidb-limitations.md)。
* TiDB 支持 `HASH`、`RANGE`、`LIST` 和 `KEY` [分区类型](/partitioned-table.md#分区类型)。对于不支持的分区类型，TiDB 返回 `Warning: Unsupported partition type %s, treat as normal table`，其中 `%s` 是具体的不支持的分区类型。

## 另请参阅

* [数据类型](/data-type-overview.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [CREATE TABLE LIKE](/sql-statements/sql-statement-create-table-like.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
