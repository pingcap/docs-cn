---
title: CREATE TABLE
summary: TiDB 数据库中 CREATE TABLE 的使用概况
aliases: ['/docs-cn/v2.1/sql-statements/sql-statement-create-table/','/docs-cn/v2.1/reference/sql/statements/create-table/']
---

# CREATE TABLE

`CREATE TABLE` 语句用于在当前所选数据库中创建新表，与 MySQL 中 `CREATE TABLE` 语句的行为类似。另可参阅单独的 `CREATE TABLE LIKE` 文档。

## 语法图

**CreateTableStmt:**

![CreateTableStmt](/media/sqlgram/CreateTableStmt.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**TableElementListOpt:**

![TableElementListOpt](/media/sqlgram/TableElementListOpt.png)

**TableElement:**

![TableElement](/media/sqlgram/TableElement.png)

**PartitionOpt:**

![PartitionOpt](/media/sqlgram/PartitionOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnName:**

![ColumnName](/media/sqlgram/ColumnName.png)

**Type:**

![Type](/media/sqlgram/Type.png)

**ColumnOptionListOpt:**

![ColumnOptionListOpt](/media/sqlgram/ColumnOptionListOpt.png)

**TableOptionListOpt:**

![TableOptionListOpt](/media/sqlgram/TableOptionListOpt.png)

TiDB 支持以下 `table_option`。TiDB 会解析并忽略其他 `table_option` 参数，例如 `AVG_ROW_LENGTH`、`CHECKSUM`、`COMPRESSION`、`CONNECTION`、`DELAY_KEY_WRITE`、`ENGINE`、`KEY_BLOCK_SIZE`、`MAX_ROWS`、`MIN_ROWS`、`ROW_FORMAT` 和 `STATS_PERSISTENT`。

| 参数           |含义                                  |举例                      |
|----------------|--------------------------------------|----------------------------|
|`AUTO_INCREMENT`|自增字段初始值                        |`AUTO_INCREMENT` = 5|
| `SHARD_ROW_ID_BITS` |用来设置隐式 _tidb_rowid 的分片数量的 bit 位数 |`SHARD_ROW_ID_BITS` = 4|
|`PRE_SPLIT_REGIONS`|用来在建表时预先均匀切分 `2^(PRE_SPLIT_REGIONS)` 个 Region |`PRE_SPLIT_REGIONS` = 4|
|`CHARACTER SET` |指定该表的字符串编码。目前支持 UTF8MB4| `CHARACTER SET` =  'utf8mb4'|
|`COLLATE`       |指定该表所使用的字符集排序规则        | `COLLATE` = 'utf8mb4_bin'|
|`COMMENT`       |注释信息                              | `COMMENT` = 'comment info'|

> **注意：**
>
> 在 TiDB 2.1 版本中，`SHARD_ROW_ID_BITS`、`PRE_SPLIT_REGIONS` 和 `COLLATE` 这三个功能都是从 2.1.13 版本（包括 2.1.13）开始支持的。

## 示例

创建一张简单表并插入一行数据：

```sql
CREATE TABLE t1 (a int);
DESC t1;
SHOW CREATE TABLE t1\G
INSERT INTO t1 (a) VALUES (1);
SELECT * FROM t1;
```

```sql
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

删除一张表。如果该表不存在，就建一张表：

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
    ->  id BIGINT NOT NULL PRIMARY KEY auto_increment,
    ->  b VARCHAR(200) NOT NULL
    -> );
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

* TiDB 不支持 `CREATE TEMPORARY TABLE` 语法。
* 支持除空间类型以外的所有数据类型。
* 不支持 `FULLTEXT`，`HASH` 和 `SPATIAL` 索引。
* 为了与 MySQL 兼容，TiDB 会解析但忽略 `index_col_name` 属性的 `[ASC | DESC]` 索引排序选项。
* `COMMENT` 属性最多支持 1024 个字符，不支持 `WITH PARSER` 选项。
* TiDB 在单个表中最多支持 512 列。InnoDB 中相应的数量限制为 1017，MySQL 中的硬限制为 4096。
* TiDB 会解析并忽略 `CHECK` 约束，与 MySQL 5.7 相兼容。详情参阅 [`CHECK` 约束](/constraints.md#check-约束)。
* TiDB 会解析并存储外键约束，但不会在 DML 语句中强制对外键进行约束检查。详情[外键约束](/constraints.md#外键约束)。

## 另请参阅

* [数据类型](/data-type-overview.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
* [CREATE TABLE LIKE](/sql-statements/sql-statement-create-table-like.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
