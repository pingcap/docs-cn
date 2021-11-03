---
title: 临时表
aliases: ['/docs-cn/dev/temporary-table/']
---

# 临时表

本文介绍 TiDB 的临时表。

TiDB 从 v5.3.0 开始支持临时表。区别于普通表，临时表主要解决了业务中间计算结果的临时存储问题，避免了频繁的建表、删表操作，提升易用性。

## 临时表类型

TiDB 的临时表分为本地临时表和全局临时表：

- 本地临时表的表定义只对当前会话可见，表内数据对当前会话可见，适用于暂存会话内的中间数据。
- 全局临时表的表定义对整个 TiDB 集群可见，表内数据只对当前事务可见，适用于暂存事务内的中间数据。

## 本地临时表

本地临时表的语义与 MySQL 临时表一致，它有以下特性：

- 本地临时表的表定义不持久化，只在创建该表的会话内可见，其他会话无法访问该本地临时表
- 不同会话可以创建同名的本地临时表，各会话只会读写该会话内创建的本地临时表
- 本地临时表的数据对会话内的所有事务可见
- 在会话结束后，该会话创建的本地临时表会自动删除
- 本地临时表可以与普通表同名，此时在 DDL 和 DML 语句中，普通表被隐藏，直到本地临时表被删除

不同于 MySQL，TiDB 本地临时表都是外部表，SQL 语句不会创建内部临时表。

### 示例

假设已存在普通表 `users`:

{{< copyable "sql" >}}

```sql
CREATE TABLE users (
    id BIGINT,
    name VARCHAR(100),
    PRIMARY KEY(id)
);
```

在会话 A 中创建本地临时表 `users`，不会有名字冲突。会话 A 访问 `users` 时，访问的是本地临时表 `users`。

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

在会话 B 中创建本地临时表 `users`，也不会有名字冲突。会话 B 内访问 `users` 时，访问的是会话 B 内创建的 `users` 的数据。

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

TiDB 本地临时表的以下特性与限制与 MySQL 一致：

- 创建、删除本地临时表时，不会自动提交当前事务
- 删除本地临时表所在的 schema 后，临时表不会被删除，仍然可以读写
- 创建本地临时表需要 `CREATE TEMPORARY TABLES` 权限，随后对该表的所有操作不需要权限
- 本地临时表不支持 foreign key 和 partition table
- 不支持基于本地临时表创建视图

TiDB 本地临时表与 MySQL 临时表有以下方面不兼容：

- TiDB 本地临时表不支持 `ALTER TABLE`
- TiDB 本地临时表忽略 `ENGINE` 表选项，始终在 TiDB 内存中暂存临时表数据，并且有 [内存限制](/temporary-table.md#内存限制)
- 当声明存储引擎为 `MEMORY` 时，TiDB 本地临时表没有 `MEMORY` 存储引擎的限制
- 当声明存储引擎为 `INNODB` 或 `MYISAM` 时，TiDB 本地临时表忽略 InnoDB 临时表特有的系统变量
- MySQL 不允许在同一条 SQL 中多次引用同一张临时表，而 TiDB 本地临时表没有该限制
- TiDB 中的系统表 `information_schema.INNODB_TEMP_TABLE_INFO` 不显示本地临时表
- TiDB 没有内部临时表，MySQL 针对内部临时表的系统变量对 TiDB 不生效

## 全局临时表

全局临时表是 TiDB 的扩展功能，它有以下特性：

- 全局临时表的表定义会持久化，对所有会话可见
- 全局临时表的数据只对当前的事务内可见，事务结束后数据自动清空
- 全局临时表不能与普通表同名

### 示例

会话 A 中创建全局临时表 `users`：

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

事务结束后数据自动被清空：

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

会话 A 创建了 `users` 后，会话 B 也可以读写该表：

{{< copyable "sql" >}}

```sql
SELECT * FROM users;
```

```
Empty set (0.00 sec)
```

注意，如果事务是自动提交的，插入的数据在 SQL 结束后被自动清空，导致后续 SQL 查找不到结果。因此应该使用非自动提交的事务读写全局临时表。

## 临时表的约束和限制

### 内存限制

无论定义表时声明的 `EGNINE` 是哪种存储引擎，本地临时表和全局临时表的数据都只暂存在 TiDB 实例的内存中，不持久化。

为了避免 OOM，用户可通过系统变量 [`tidb_tmp_table_max_size`](/system-variables.md#tidb_tmp_table_max_size-从-v53-版本开始引入) 限制每张临时表的大小，当临时表大小超过限制后报错。`tidb_tmp_table_max_size` 的默认值是 `64MB`。

例如调整 `tidb_tmp_table_max_size` 为 `256MB`：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_tmp_table_max_size=268435456;
```

### 与其他功能的兼容性

以下是本地临时表和全局临时表都不支持的功能：

- 不支持 `AUTO_RANDOM` 列
- 不支持 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS` 表选项
- 不支持 partition table
- 不支持 `SPLIT REGION` 语句
- 不支持 `ADMIN CHECK TABLE` 和 `ADMIN CHECKSUM TABLE` 语句
- 不支持 `FLASHBACK TABLE` 和 `RECOVER TABLE` 语句
- 不支持以临时表为源表执行 `CREATE TABLE LIKE` 语句
- 不支持 stale read
- 不支持 foreign key
- 不支持 SQL binding
- 不支持添加 TiFlash 副本
- 不支持在临时表上创建视图
- 不支持 placement rules
- 包含临时表的执行计划不会被 prepared plan cache 缓存

以下是只有本地临时表不支持的功能：

- 不支持通过系统变量 `tidb_snapshot` 读取历史数据

## 生态工具支持

本地临时表只对当前会话可见，因此本地临时表不会被生态工具导出、备份、同步。

全局临时表的表定义全局可见，因此全局临时表的表定义会被生态工具导出、备份、同步，但不导出数据。

> **注意：**
>
> - TiCDC 必须使用 v5.3.0 及以上版本同步，否则下游集群的表定义错误
> - BR 必须使用 v5.3.0 及以上版本备份，否则备份后的表定义错误
> - 导入的集群、恢复后的集群、同步的下游集群需要支持全局临时表，否则报错

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [CREATE TABLE LIKE](/sql-statements/sql-statement-create-table-like.md)
* [DROP TABLE](/sql-statements/sql-statement-drop-table.md)
