---
title: 临时表
summary: 了解 TiDB 中的临时表功能，以及如何使用临时表存储应用程序的中间数据，从而减少表管理开销并提高性能。
---

# 临时表

临时表功能在 TiDB v5.3.0 中引入。此功能解决了临时存储应用程序中间结果的问题，使你不必频繁创建和删除表。你可以将中间计算数据存储在临时表中。当不再需要中间数据时，TiDB 会自动清理和回收临时表。这避免了用户应用程序过于复杂，减少了表管理开销，并提高了性能。

本文介绍临时表的使用场景和类型，提供使用示例和如何限制临时表内存使用的说明，并解释与其他 TiDB 功能的兼容性限制。

## 使用场景

你可以在以下场景中使用 TiDB 临时表：

- 缓存应用程序的中间临时数据。计算完成后，数据被转储到普通表中，临时表自动释放。
- 在短时间内对相同数据执行多个 DML 操作。例如，在电子商务购物车应用中，添加、修改和删除产品，完成支付，并删除购物车信息。
- 快速批量导入中间临时数据以提高临时数据导入的性能。
- 批量更新数据。将数据批量导入数据库中的临时表，修改数据后将数据导出到文件。

## 临时表类型

TiDB 中的临时表分为两种类型：本地临时表和全局临时表。

- 对于本地临时表，表定义和表中的数据仅对当前会话可见。这种类型适合临时存储会话中的中间数据。
- 对于全局临时表，表定义对整个 TiDB 集群可见，而表中的数据仅对当前事务可见。这种类型适合临时存储事务中的中间数据。

## 本地临时表

TiDB 中本地临时表的语义与 MySQL 临时表一致。特点如下：

- 本地临时表的表定义不是持久的。本地临时表仅对创建该表的会话可见，其他会话无法访问该表。
- 你可以在不同的会话中创建同名的本地临时表，每个会话只能读取和写入在该会话中创建的本地临时表。
- 本地临时表的数据对会话中的所有事务可见。
- 会话结束后，在该会话中创建的本地临时表会自动删除。
- 本地临时表可以与普通表同名。在这种情况下，在 DDL 和 DML 语句中，普通表会被隐藏，直到本地临时表被删除。

要创建本地临时表，你可以使用 `CREATE TEMPORARY TABLE` 语句。要删除本地临时表，你可以使用 `DROP TABLE` 或 `DROP TEMPORARY TABLE` 语句。

与 MySQL 不同，TiDB 中的本地临时表都是外部表，在执行 SQL 语句时不会自动创建内部临时表。

### 本地临时表使用示例

> **注意：**
>
> - 在 TiDB 中使用临时表之前，请注意[与其他 TiDB 功能的兼容性限制](#与其他-tidb-功能的兼容性限制)和[与 MySQL 临时表的兼容性](#与-mysql-临时表的兼容性)。
> - 如果你在早于 TiDB v5.3.0 的集群上创建了本地临时表，这些表实际上是普通表，并且在集群升级到 TiDB v5.3.0 或更高版本后仍被视为普通表。

假设有一个普通表 `users`：

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

在会话 A 中，创建本地临时表 `users` 不会与普通表 `users` 冲突。当会话 A 访问 `users` 表时，它访问的是本地临时表 `users`。

{{< copyable "sql" >}}

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

如果你向 `users` 插入数据，数据会插入到会话 A 中的本地临时表 `users`。

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

在会话 B 中，创建本地临时表 `users` 不会与普通表 `users` 或会话 A 中的本地临时表 `users` 冲突。当会话 B 访问 `users` 表时，它访问的是会话 B 中的本地临时表 `users`。

{{< copyable "sql" >}}

```sql
CREATE TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
);
```

```
Query OK, 0 rows affected (0.01 sec)
```

如果你向 `users` 插入数据，数据会插入到会话 B 中的本地临时表 `users`。

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'James', 'NewYork');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+---------+
| id   | name  | city    |
+------+-------+---------+
| 1001 | James | NewYork |
+------+-------+---------+
1 row in set (0.00 sec)
```

### 与 MySQL 临时表的兼容性

TiDB 本地临时表与 MySQL 临时表具有以下相同的特性和限制：

- 创建或删除本地临时表时，当前事务不会自动提交。
- 删除本地临时表所在的 schema 后，临时表不会被删除，仍然可读可写。
- 创建本地临时表需要 `CREATE TEMPORARY TABLES` 权限。对表的所有后续操作不需要任何权限。
- 本地临时表不支持外键和分区表。
- 不支持基于本地临时表创建视图。
- `SHOW [FULL] TABLES` 不显示本地临时表。

TiDB 本地临时表与 MySQL 临时表在以下方面不兼容：

- TiDB 本地临时表不支持 `ALTER TABLE`。
- TiDB 本地临时表忽略 `ENGINE` 表选项，始终使用 TiDB 内存存储临时表数据，并有[内存限制](#限制临时表的内存使用)。
- 当声明 `MEMORY` 作为存储引擎时，TiDB 本地临时表不受 `MEMORY` 存储引擎的限制。
- 当声明 `INNODB` 或 `MYISAM` 作为存储引擎时，TiDB 本地临时表忽略 InnoDB 临时表特有的系统变量。
- MySQL 不允许在同一个 SQL 语句中多次引用同一个临时表。TiDB 本地临时表没有这个限制。
- MySQL 中显示临时表的系统表 `information_schema.INNODB_TEMP_TABLE_INFO` 在 TiDB 中不存在。目前，TiDB 没有显示本地临时表的系统表。
- TiDB 没有内部临时表。MySQL 中用于内部临时表的系统变量对 TiDB 不起作用。

## 全局临时表

全局临时表是 TiDB 的扩展功能。特点如下：

- 全局临时表的表定义是持久的，对所有会话可见。
- 全局临时表的数据仅在当前事务中可见。事务结束时，数据会自动清除。
- 全局临时表不能与普通表同名。

要创建全局临时表，你可以使用以 `ON COMMIT DELETE ROWS` 结尾的 `CREATE GLOBAL TEMPORARY TABLE` 语句。要删除全局临时表，你可以使用 `DROP TABLE` 或 `DROP GLOBAL TEMPORARY TABLE` 语句。

### 全局临时表使用示例

> **注意：**
>
> - 在 TiDB 中使用临时表之前，请注意[与其他 TiDB 功能的兼容性限制](#与其他-tidb-功能的兼容性限制)。
> - 如果你在 TiDB v5.3.0 或更高版本的集群上创建了全局临时表，当集群降级到早于 v5.3.0 的版本时，这些表会被作为普通表处理。在这种情况下，会发生数据错误。

在会话 A 中创建全局临时表 `users`：

{{< copyable "sql" >}}

```sql
CREATE GLOBAL TEMPORARY TABLE users (
    id BIGINT,
    name VARCHAR(100),
    city VARCHAR(50),
    PRIMARY KEY(id)
) ON COMMIT DELETE ROWS;
```

```
Query OK, 0 rows affected (0.01 sec)
```

写入 `users` 的数据对当前事务可见：

{{< copyable "sql" >}}

```sql
BEGIN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO users(id, name, city) VALUES(1001, 'Davis', 'LosAngeles');
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
+------+-------+------------+
| id   | name  | city       |
+------+-------+------------+
| 1001 | Davis | LosAngeles |
+------+-------+------------+
1 row in set (0.00 sec)
```

事务结束后，数据会自动清除：

{{< copyable "sql" >}}

```sql
COMMIT;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

在会话 A 中创建 `users` 后，会话 B 也可以读取和写入 `users` 表：

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

> **注意：**
>
> 如果事务自动提交，SQL 语句执行后，插入的数据会自动清除，后续的 SQL 执行无法使用这些数据。因此，你应该使用非自动提交事务来读取和写入全局临时表。

## 限制临时表的内存使用

无论在定义表时声明哪种存储引擎作为 `ENGINE`，本地临时表和全局临时表的数据都只存储在 TiDB 实例的内存中。这些数据不会持久化。

为了避免内存溢出，你可以使用 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-new-in-v530) 系统变量来限制每个临时表的大小。一旦临时表大于 `tidb_tmp_table_max_size` 阈值，TiDB 就会报错。`tidb_tmp_table_max_size` 的默认值是 `64MB`。

例如，将临时表的最大大小设置为 `256MB`：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

## 与其他 TiDB 功能的兼容性限制

TiDB 中的本地临时表和全局临时表与以下 TiDB 功能**不**兼容：

- `AUTO_RANDOM` 列
- `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 表选项
- 分区表
- `SPLIT REGION` 语句
- `ADMIN CHECK TABLE` 和 `ADMIN CHECKSUM TABLE` 语句
- `FLASHBACK TABLE` 和 `RECOVER TABLE` 语句
- 基于临时表执行 `CREATE TABLE LIKE` 语句
- Stale Read
- 外键
- SQL 绑定
- TiFlash 副本
- 在临时表上创建视图
- Placement Rules
- 涉及临时表的执行计划不会被 `prepare plan cache` 缓存。

TiDB 中的本地临时表**不**支持以下功能：

- 使用 `tidb_snapshot` 系统变量读取历史数据。

## TiDB 迁移工具支持

本地临时表不会被 TiDB 迁移工具导出、备份或复制，因为这些表仅对当前会话可见。

全局临时表会被 TiDB 迁移工具导出、备份和复制，因为表定义是全局可见的。注意，表上的数据不会被导出。

> **注意：**
>
> - 使用 TiCDC 复制临时表需要 TiCDC v5.3.0 或更高版本。否则，下游表的表定义会出错。
> - 使用 BR 备份临时表需要 BR v5.3.0 或更高版本。否则，备份的临时表的表定义会出错。
> - 导出集群、数据恢复后的集群和复制的下游集群都应该支持全局临时表。否则，会报错。

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE TABLE LIKE](/sql-statements/sql-statement-create-table-like.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
