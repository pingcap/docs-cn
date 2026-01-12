---
title: 外键约束
summary: TiDB 数据库中外键约束的使用概况。
---

# 外键约束

外键允许跨表交叉引用相关数据，外键约束则可以保证相关数据的一致性。从 v6.6.0 开始，TiDB 支持外键以及外键约束功能。从 v8.5.0 开始，该功能成为正式功能。

> **警告：**
>
> 外键功能通常用于强制执行[参照完整性](https://zh.wikipedia.org/wiki/%E5%8F%82%E7%85%A7%E5%AE%8C%E6%95%B4%E6%80%A7)约束检查。使用该功能可能会导致性能下降，在将其应用于性能敏感的场景前，建议先进行全面测试。

外键是在子表中定义的，语法如下：

```ebnf+diagram
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
```

## 命名

外键的命名遵循以下规则：

- 如果在 `CONSTRAINT identifier` 语句中指定了名称，则使用该名称。
- 如果 `CONSTRAINT identifier` 语句未指定名称，但在 `FOREIGN KEY identifier` 语句中指定了名称，则使用 `FOREIGN KEY identifier` 定义的名称。
- 如果 `CONSTRAINT identifier` 和 `FOREIGN KEY identifier` 语句都没有指定名称，则会自动生成一个名称，例如 `fk_1`、`fk_2`、`fk_3` 等。
- 外键名称必须在当前表中唯一，否则创建时会报错 `ERROR 1826: Duplicate foreign key constraint name 'fk'`。

## 限制

创建外键时需要满足以下条件：

- 父表和子表都不能是临时表。
- 用户需要对父表有 `REFERENCES` 权限。
- 外键中的列和引用的父表中的列必须是相同的数据类型，并具有相同的大小、精度、长度、字符集 (charset) 和排序规则 (collation)。
- 外键中的列不能引用自身。
- 外键中的列和引用的父表中的列必须有相同的索引，并且索引中的列顺序必须与外键的列顺序一样，这样才能在执行外键约束检查时使用索引来避免全表扫描。

    - 如果父表中没有对应的外键索引，则会报错 `ERROR 1822: Failed to add the foreign key constraint. Missing index for constraint 'fk' in the referenced table 't'`。
    - 如果子表中没有对应的外键索引，则会自动创建一个索引，索引名和外键名一样。

- 不支持在 `BLOB` 和 `TEXT` 类型的列上创建外键。
- 不支持在分区表上创建外键。
- 不支持在虚拟生成列 (`VIRTUAL GENERATED COLUMNS`) 上创建外键。

## 引用操作

当 `UPDATE` 或 `DELETE` 操作影响父表中的外键值时，其在子表中相匹配的外键值取决于外键定义中 `ON UPDATE` 和 `ON DELETE` 定义的引用操作，引用操作包括：

- `CASCADE`：当 `UPDATE` 或 `DELETE` 父表中的行数据时，自动级联更新或删除子表中的匹配行数据。级联操作会用深度优先方式执行。
- `SET NULL`：当 `UPDATE` 或 `DELETE` 父表中的行数据时，自动将子表中匹配的外键列数据设置为 `NULL`。
- `RESTRICT`：如果子表中存在外键匹配的行数据，则拒绝 `UPDATE` 或 `DELETE` 父表的操作。
- `NO ACTION`：行为和 `RESTRICT` 一样。
- `SET DEFAULT`：行为和 `RESTRICT` 一样。

如果父表中没有匹配的外键值，则拒绝 `INSERT` 或 `UPDATE` 子表的操作。

如果外键定义中没有指定 `ON DELETE` 或者 `ON UPDATE`，则默认的行为是 `NO ACTION`。

如果外键是定义在 `STORED GENERATED COLUMN` 上的，则不支持使用 `CASCADE`、`SET NULL` 和 `SET DEFAULT` 引用操作。

## 外键使用示例

下面的示例通过单列外键关联父表和子表：

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT,
    INDEX idx_pid (pid),
    FOREIGN KEY (pid) REFERENCES parent(id) ON DELETE CASCADE
);
```

下面是一个更复杂的示例，其中 `product_order` 表有两个外键分别引用其他两个表。一个外键引用 `product` 表中的两列索引。另一个引用 `customer` 表中的单列索引：

```sql
CREATE TABLE product (
    category INT NOT NULL,
    id INT NOT NULL,
    price DECIMAL(20,10),
    PRIMARY KEY(category, id)
);

CREATE TABLE customer (
    id INT KEY
);

CREATE TABLE product_order (
    id INT NOT NULL AUTO_INCREMENT,
    product_category INT NOT NULL,
    product_id INT NOT NULL,
    customer_id INT NOT NULL,

    PRIMARY KEY(id),
    INDEX (product_category, product_id),
    INDEX (customer_id),

    FOREIGN KEY (product_category, product_id)
      REFERENCES product(category, id)
      ON UPDATE CASCADE ON DELETE RESTRICT,

    FOREIGN KEY (customer_id)
      REFERENCES customer(id)
);
```

## 新增外键约束

可以使用下面 `ALTER TABLE` 语句来新增一个外键约束：

```sql
ALTER TABLE table_name
    ADD [CONSTRAINT [identifier]] FOREIGN KEY
    [identifier] (col_name, ...)
    REFERENCES tbl_name (col_name,...)
    [ON DELETE reference_option]
    [ON UPDATE reference_option]
```

外键可以是自引用的，即引用同一个表。使用 `ALTER TABLE` 向表添加外键约束时，请先在外键引用父表的列上创建索引。

## 删除外键约束

可以使用下面 `ALTER TABLE` 语句来删除一个外键约束：

```sql
ALTER TABLE table_name DROP FOREIGN KEY fk_identifier;
```

如果外键约束在创建时定义了名称，则可以引用该名称来删除外键约束。否则，只能引用自动生成的约束名称进行删除。你可以使用 `SHOW CREATE TABLE` 查看外键名称：

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

## 外键约束检查

TiDB 支持是否开启外键约束检查，由系统变量 [`foreign_key_checks`](/system-variables.md#foreign_key_checks) 控制，其默认值是 `ON`，即开启外键约束检查，它有 `GLOBAL` 和 `SESSION` 两种作用域。在一般的操作中保持该变量开启可以保证外键引用关系的完整性。

关闭外键约束检查的作用如下：

- 当删除一个被外键引用的父表时，只有关闭外键约束检查时才能删除成功。
- 当给数据库导入数据时，创建表的顺序可能和外键依赖顺序不一样而导致创建表报错，只有关闭外键约束检查时才能创建表成功，另外，导入数据时关闭外键约束检查也能加快导数据的速度。
- 当给数据库导入数据时，先导入子表的数据会报错，只有关闭外键约束检查，才能确保顺利导入子表数据。
- 执行有关外键的 `ALTER TABLE` 操作时，关闭外键约束检查才能执行成功。

当关闭关键约束检查时，不会执行外键约束检查以及引用操作，但以下场景除外：

- 如果执行 `ALTER TABLE` 会导致外键定义不正确，则依然会执行报错。
- 删除外键所需的索引时，需要先删除外键，否则删除外键会执行报错。
- 创建外键时，如果不符合外键的条件或限制，则依然会执行报错。

## 锁

在 `INSERT` 或者 `UPDATE` 子表时，外键约束会检查父表中是否存在对应的外键值，并对父表中的该行数据上锁，避免该外键值被其他操作删除，导致破坏外键约束。这里的上锁行为等同于对父表中外键值所在行做 `SELECT FOR UPDATE` 操作。

因为 TiDB 目前暂不支持 `LOCK IN SHARE MODE`，所以，在并发写入子表场景，如果引用的外键值大部分都一样，可能会有比较严重的锁冲突。建议在大批量写入子表数据时，关闭 [`foreign_key_checks`](/system-variables.md#foreign_key_checks)。

## 外键的定义和元信息

你可以使用 [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) 语句查看外键的定义：

```sql
mysql> SHOW CREATE TABLE child\G
*************************** 1. row ***************************
       Table: child
Create Table: CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

你可以使用以下任一系统表获取有关外键的信息：

- [`INFORMATION_SCHEMA.KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)
- [`INFORMATION_SCHEMA.TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)
- [`INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS`](/information-schema/information-schema-referential-constraints.md)

下面提供了查询示例：

从 `INFORMATION_SCHEMA.KEY_COLUMN_USAGE` 系统表中获取有关的外键信息：

```sql
mysql> SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA IS NOT NULL;
+--------------+---------------+------------------+-----------------+
| TABLE_SCHEMA | TABLE_NAME    | COLUMN_NAME      | CONSTRAINT_NAME |
+--------------+---------------+------------------+-----------------+
| test         | child         | pid              | fk_1            |
| test         | product_order | product_category | fk_1            |
| test         | product_order | product_id       | fk_1            |
| test         | product_order | customer_id      | fk_2            |
+--------------+---------------+------------------+-----------------+
```

从 `INFORMATION_SCHEMA.TABLE_CONSTRAINTS` 系统表中获取有关的外键信息：

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE='FOREIGN KEY'\G
***************************[ 1. row ]***************************
CONSTRAINT_CATALOG | def
CONSTRAINT_SCHEMA  | test
CONSTRAINT_NAME    | fk_1
TABLE_SCHEMA       | test
TABLE_NAME         | child
CONSTRAINT_TYPE    | FOREIGN KEY
```

从 `INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS` 系统表中获取有关的外键信息：

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS\G
***************************[ 1. row ]***************************
CONSTRAINT_CATALOG        | def
CONSTRAINT_SCHEMA         | test
CONSTRAINT_NAME           | fk_1
UNIQUE_CONSTRAINT_CATALOG | def
UNIQUE_CONSTRAINT_SCHEMA  | test
UNIQUE_CONSTRAINT_NAME    | PRIMARY
MATCH_OPTION              | NONE
UPDATE_RULE               | NO ACTION
DELETE_RULE               | CASCADE
TABLE_NAME                | child
REFERENCED_TABLE_NAME     | parent
```

## 查看带有外键的执行计划

你可以使用 `EXPLAIN` 语句查看执行计划。`Foreign_Key_Check` 算子是执行 DML 语句时，执行外键约束检查的算子。

```sql
mysql> explain insert into child values (1,1);
+-----------------------+---------+------+---------------+-------------------------------+
| id                    | estRows | task | access object | operator info                 |
+-----------------------+---------+------+---------------+-------------------------------+
| Insert_1              | N/A     | root |               | N/A                           |
| └─Foreign_Key_Check_3 | 0.00    | root | table:parent  | foreign_key:fk_1, check_exist |
+-----------------------+---------+------+---------------+-------------------------------+
```

你可以使用 `EXPLAIN ANALYZE` 语句查看外键引用行为的执行。`Foreign_Key_Cascade` 算子是执行 DML 语句时，执行外键引用行为的算子。

```sql
mysql> explain analyze delete from parent where id = 1;
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| id                               | estRows | actRows | task      | access object                   | execution info                                                                                                                                                                               | operator info                               | memory    | disk |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
| Delete_2                         | N/A     | 0       | root      |                                 | time:117.3µs, loops:1                                                                                                                                                                        | N/A                                         | 380 Bytes | N/A  |
| ├─Point_Get_1                    | 1.00    | 1       | root      | table:parent                    | time:63.6µs, loops:2, Get:{num_rpc:1, total_time:29.9µs}                                                                                                                                     | handle:1                                    | N/A       | N/A  |
| └─Foreign_Key_Cascade_3          | 0.00    | 0       | root      | table:child, index:idx_pid      | total:1.28ms, foreign_keys:1                                                                                                                                                                 | foreign_key:fk_1, on_delete:CASCADE         | N/A       | N/A  |
|   └─Delete_7                     | N/A     | 0       | root      |                                 | time:904.8µs, loops:1                                                                                                                                                                        | N/A                                         | 1.11 KB   | N/A  |
|     └─IndexLookUp_11             | 10.00   | 1       | root      |                                 | time:869.5µs, loops:2, index_task: {total_time: 371.1µs, fetch_handle: 357.3µs, build: 1.25µs, wait: 12.5µs}, table_task: {total_time: 382.6µs, num: 1, concurrency: 5}                      |                                             | 9.13 KB   | N/A  |
|       ├─IndexRangeScan_9(Build)  | 10.00   | 1       | cop[tikv] | table:child, index:idx_pid(pid) | time:351.2µs, loops:3, cop_task: {num: 1, max: 282.3µs, proc_keys: 0, rpc_num: 1, rpc_time: 263µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:220.2µs, loops:0}   | range:[1,1], keep order:false, stats:pseudo | N/A       | N/A  |
|       └─TableRowIDScan_10(Probe) | 10.00   | 1       | cop[tikv] | table:child                     | time:223.9µs, loops:2, cop_task: {num: 1, max: 168.8µs, proc_keys: 0, rpc_num: 1, rpc_time: 154.5µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}, tikv_task:{time:145.6µs, loops:0} | keep order:false, stats:pseudo              | N/A       | N/A  |
+----------------------------------+---------+---------+-----------+---------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------+-----------+------+
```

## 兼容性

### TiDB 版本间兼容性

TiDB 在 v6.6.0 之前已经支持创建外键的语法，但创建的外键并不生效。如果将之前创建的 TiDB 集群升级到 v6.6.0 及之后的版本，之前创建的外键依然是不生效的，可以先删除不生效的外键后再创建外键使外键约束生效。只有在 v6.6.0 及之后版本中新创建的外键才生效。你可以使用 `SHOW CREATE TABLE` 语句查看外键是否生效，不生效的外键会有一条 `/* FOREIGN KEY INVALID */` 注释。

```sql
mysql> SHOW CREATE TABLE child\G
***************************[ 1. row ]***************************
Table        | child
Create Table | CREATE TABLE `child` (
  `id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  KEY `idx_pid` (`pid`),
  CONSTRAINT `fk_1` FOREIGN KEY (`pid`) REFERENCES `test`.`parent` (`id`) ON DELETE CASCADE /* FOREIGN KEY INVALID */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### 与 TiDB 工具的兼容性

- [DM](/dm/dm-overview.md) 不兼容外键功能。DM 在同步数据到下游 TiDB 时，会显式关闭下游 TiDB 的 [`foreign_key_checks`](/system-variables.md#foreign_key_checks)，所以由外键产生的级联操作不会从上游同步到下游，这会导致上下游数据不一致。
- [TiCDC](/ticdc/ticdc-overview.md) v6.6.0 兼容外键功能。旧版本的 TiCDC 在同步带外键的表时，可能会报错，建议使用 v6.6.0 之前版本 TiCDC 时先关闭下游 TiDB 集群的 `foreign_key_checks`。
- [BR](/br/backup-and-restore-overview.md) v6.6.0 兼容外键功能。之前版本的 BR 在恢复带外键的表到 v6.6.0 及之后版本的集群时，可能会报错，建议先关闭下游 TiDB 集群的 `foreign_key_checks` 后再恢复集群。
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 导入数据到 TiDB 前，如果目标表使用了外键，建议先关闭 TiDB 集群的 `foreign_key_checks`。对于 v6.6.0 之前的版本，关闭该系统变量也不会生效，你需要为下游数据库用户添加 `REFERENCES` 权限，或者提前手动在下游数据库中创建好目标表，以确保顺利导入数据。
- [Dumpling](/dumpling-overview.md) 兼容外键功能。
- [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 在对比上下游数据时，如果上下游数据库的版本不一样，且下游 TiDB 中存在[不生效的外键](#tidb-版本间兼容性)，则 sync-diff-inspector 可能会报上下游表结构不一致的错误。因为 TiDB v6.6.0 会对表结构中不生效的外键添加一条 `/* FOREIGN KEY INVALID */` 注释。

### 与 MySQL 的兼容性

创建外键未指定名称时，TiDB 自动生成的外键名称和 MySQL 不一样。例如 TiDB 生成的外键名称为 `fk_1`、`fk_2`、`fk_3` 等，MySQL 生成的外键名称为 `table_name_ibfk_1`、 `table_name_ibfk_2`、`table_name_ibfk_3` 等。

MySQL 和 TiDB 均能解析但会忽略以内联 `REFERENCES` 的方式定义的外键。只有当 `REFERENCES` 作为 `FOREIGN KEY` 定义的一部分时，才会进行检查和执行。下面的示例在定义外键约束时只使用了 `REFERENCES`：

```sql
CREATE TABLE parent (
    id INT KEY
);

CREATE TABLE child (
    id INT,
    pid INT REFERENCES parent(id)
);

SHOW CREATE TABLE child;
```

输出结果显示 `child` 表不包含任何外键：

```sql
+-------+-------------------------------------------------------------+
| Table | Create Table                                                |
+-------+-------------------------------------------------------------+
| child | CREATE TABLE `child` (                                      |
|       |   `id` int DEFAULT NULL,                                |
|       |   `pid` int DEFAULT NULL                                |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+-------------------------------------------------------------+
```
