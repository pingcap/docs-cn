---
title: 事务
summary: 了解 TiDB 中的事务。
---

# 事务

TiDB 支持使用[悲观](/pessimistic-transaction.md)或[乐观](/optimistic-transaction.md)事务模式的分布式事务。从 TiDB 3.0.8 开始，TiDB 默认使用悲观事务模式。

本文档介绍常用的事务相关语句、显式和隐式事务、隔离级别、约束的延迟检查以及事务大小。

常用变量包括 [`autocommit`](#autocommit)、[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)、[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 和 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)。

> **注意：**
>
> [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 和 [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 变量仅适用于乐观事务，不适用于悲观事务。

## 常用语句

### 开始事务

语句 [`BEGIN`](/sql-statements/sql-statement-begin.md) 和 [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) 可以互换使用，用于显式开始新事务。

语法：

{{< copyable "sql" >}}

```sql
BEGIN;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

如果在执行这些语句时当前会话正在进行事务，TiDB 会在开始新事务之前自动提交当前事务。

> **注意：**
>
> 与 MySQL 不同，TiDB 在执行上述语句后立即获取当前数据库的快照。MySQL 的 `BEGIN` 和 `START TRANSACTION` 在事务开始后执行第一个读取 InnoDB 数据的 `SELECT` 语句（不是 `SELECT FOR UPDATE`）时才获取快照。`START TRANSACTION WITH CONSISTENT SNAPSHOT` 在执行语句时获取快照。因此，在 MySQL 中，`BEGIN`、`START TRANSACTION` 和 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 等同于 MySQL 中的 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。

### 提交事务

语句 [`COMMIT`](/sql-statements/sql-statement-commit.md) 指示 TiDB 应用当前事务中的所有更改。

语法：

{{< copyable "sql" >}}

```sql
COMMIT;
```

> **提示：**
>
> 在启用[乐观事务](/optimistic-transaction.md)之前，请确保您的应用程序正确处理 `COMMIT` 语句可能返回错误的情况。如果您不确定应用程序如何处理这种情况，建议使用默认的[悲观事务](/pessimistic-transaction.md)。

### 回滚事务

语句 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 回滚并取消当前事务中的所有更改。

语法：

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

如果客户端连接中断或关闭，事务也会自动回滚。

## 自动提交

为了保持与 MySQL 的兼容性，TiDB 默认会在语句执行后立即_自动提交_。

例如：

```sql
mysql> CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     pad1 VARCHAR(100)
    );
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
+----+------+
| id | pad1 |
+----+------+
|  1 | test |
+----+------+
1 row in set (0.00 sec)
```

在上面的例子中，`ROLLBACK` 语句没有效果。这是因为 `INSERT` 语句是在自动提交模式下执行的。也就是说，它相当于以下单语句事务：

```sql
START TRANSACTION;
INSERT INTO t1 VALUES (1, 'test');
COMMIT;
```

如果已经显式开始了事务，则不会应用自动提交。在下面的例子中，`ROLLBACK` 语句成功撤销了 `INSERT` 语句：

```sql
mysql> CREATE TABLE t2 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     pad1 VARCHAR(100)
    );
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t2 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

[`autocommit`](/system-variables.md#autocommit) 系统变量可以在全局或会话级别[进行更改](/sql-statements/sql-statement-set-variable.md)。

例如：

{{< copyable "sql" >}}

```sql
SET autocommit = 0;
```

{{< copyable "sql" >}}

```sql
SET GLOBAL autocommit = 0;
```

## 显式和隐式事务

> **注意：**
>
> 某些语句会隐式提交。例如，执行 `[BEGIN|START TRANSACTION]` 会隐式提交最后一个事务并开始新事务。这种行为是为了保持与 MySQL 的兼容性。更多详细信息，请参考[隐式提交](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。

TiDB 支持显式事务（使用 `[BEGIN|START TRANSACTION]` 和 `COMMIT` 定义事务的开始和结束）和隐式事务（`SET autocommit = 1`）。

如果将 `autocommit` 的值设置为 `1` 并通过 `[BEGIN|START TRANSACTION]` 语句开始新事务，则在 `COMMIT` 或 `ROLLBACK` 之前自动提交被禁用，使事务成为显式事务。

对于 DDL 语句，事务会自动提交且不支持回滚。如果在当前会话正在进行事务时运行 DDL 语句，则在当前事务提交后执行 DDL 语句。

## 约束的延迟检查

默认情况下，乐观事务在执行 DML 语句时不会检查[主键](/constraints.md#primary-key)或[唯一约束](/constraints.md#unique-key)。这些检查会在事务 `COMMIT` 时执行。

例如：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
BEGIN OPTIMISTIC;
INSERT INTO t1 VALUES (1); -- MySQL 返回错误；TiDB 返回成功。
INSERT INTO t1 VALUES (2);
COMMIT; -- MySQL 成功提交；TiDB 返回错误并回滚事务。
SELECT * FROM t1; -- MySQL 返回 1 2；TiDB 返回 1。
```

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> BEGIN OPTIMISTIC;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1); -- MySQL 返回错误；TiDB 返回成功。
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (2);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT; -- MySQL 成功提交；TiDB 返回错误并回滚事务。
ERROR 1062 (23000): Duplicate entry '1' for key 't1.PRIMARY'
mysql> SELECT * FROM t1; -- MySQL 返回 1 2；TiDB 返回 1。
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

延迟检查优化通过批量约束检查和减少网络通信来提高性能。可以通过设置 [`tidb_constraint_check_in_place=ON`](/system-variables.md#tidb_constraint_check_in_place) 来禁用此行为。

> **注意：**
>
> + 此优化仅适用于乐观事务。
> + 此优化不适用于 `INSERT IGNORE` 和 `INSERT ON DUPLICATE KEY UPDATE`，仅适用于普通的 `INSERT` 语句。

## 语句回滚

TiDB 支持语句执行失败后的原子回滚。如果语句导致错误，其所做的更改将不会生效。事务将保持打开状态，可以在发出 `COMMIT` 或 `ROLLBACK` 语句之前进行其他更改。

{{< copyable "sql" >}}

```sql
CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
BEGIN;
INSERT INTO test VALUES (1);
INSERT INTO tset VALUES (2);  -- 语句不生效，因为 "test" 被错误拼写为 "tset"。
INSERT INTO test VALUES (1),(2);  -- 整个语句不生效，因为违反了主键约束
INSERT INTO test VALUES (3);
COMMIT;
SELECT * FROM test;
```

```sql
mysql> CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.09 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO test VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO tset VALUES (2);  -- 语句不生效，因为 "test" 被错误拼写为 "tset"。
ERROR 1146 (42S02): Table 'test.tset' doesn't exist
mysql> INSERT INTO test VALUES (1),(2);  -- 整个语句不生效，因为违反了主键约束
ERROR 1062 (23000): Duplicate entry '1' for key 'test.PRIMARY'
mysql> INSERT INTO test VALUES (3);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM test;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

在上面的例子中，失败的 `INSERT` 语句后事务仍然保持打开状态。最后的插入语句成功执行，并且更改被提交。

## 事务大小限制

由于底层存储引擎的限制，TiDB 要求单行不能超过 6 MB。单行的大小是根据其所有列的数据类型将其转换为字节并求和来估算的。

TiDB 支持乐观和悲观事务，而乐观事务是悲观事务的基础。因为乐观事务首先将更改缓存在私有内存中，TiDB 限制了单个事务的大小。

默认情况下，TiDB 将单个事务的总大小限制为不超过 100 MB。你可以通过配置文件中的 `txn-total-size-limit` 修改此默认值。`txn-total-size-limit` 的最大值为 1 TB。单个事务的大小限制还取决于服务器中剩余可用内存的大小。这是因为在执行事务时，TiDB 进程的内存使用量会随事务大小增加而增加，最多可达到事务大小的两到三倍或更多。

TiDB 之前限制单个事务的键值对总数为 300,000。这个限制在 TiDB v4.0 中被移除。

> **注意：**
>
> 通常，TiDB Binlog 会被启用以将数据复制到下游。在某些场景中，会使用 Kafka 等消息中间件来消费复制到下游的 binlog。
>
> 以 Kafka 为例，Kafka 的单条消息处理能力上限为 1 GB。因此，当 `txn-total-size-limit` 设置为超过 1 GB 时，可能会出现事务在 TiDB 中成功执行，但下游 Kafka 报错的情况。为避免这种情况，你需要根据最终消费者的限制来决定 `txn-total-size-limit` 的实际值。例如，如果下游使用 Kafka，则 `txn-total-size-limit` 不能超过 1 GB。

## 因果一致性

> **注意：**
>
> 因果一致性事务仅在启用异步提交和一阶段提交特性时生效。有关这两个特性的详细信息，请参见 [`tidb_enable_async_commit`](/system-variables.md#tidb_enable_async_commit-new-in-v50) 和 [`tidb_enable_1pc`](/system-variables.md#tidb_enable_1pc-new-in-v50)。

TiDB 支持为事务启用因果一致性。启用因果一致性的事务在提交时不需要从 PD 获取时间戳，具有更低的提交延迟。启用因果一致性的语法如下：

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

默认情况下，TiDB 保证线性一致性。在线性一致性的情况下，如果事务 2 在事务 1 提交后提交，从逻辑上讲，事务 2 应该发生在事务 1 之后。因果一致性比线性一致性更弱。在因果一致性的情况下，只有当事务 1 和事务 2 锁定或写入的数据有交集时，即两个事务具有数据库已知的因果关系时，才能保证两个事务的提交顺序和发生顺序一致。目前，TiDB 不支持传入外部因果关系。

启用因果一致性的两个事务具有以下特征：

+ [具有潜在因果关系的事务具有一致的逻辑顺序和物理提交顺序](#具有潜在因果关系的事务具有一致的逻辑顺序和物理提交顺序)
+ [没有因果关系的事务不保证一致的逻辑顺序和物理提交顺序](#没有因果关系的事务不保证一致的逻辑顺序和物理提交顺序)
+ [不带锁的读取不会创建因果关系](#不带锁的读取不会创建因果关系)

### 具有潜在因果关系的事务具有一致的逻辑顺序和物理提交顺序

假设事务 1 和事务 2 都采用因果一致性，并执行以下语句：

| 事务 1 | 事务 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE | |
| UPDATE t set v = $(x + 1) WHERE id = 2 | |
| COMMIT | |
| | UPDATE t SET v = 2 WHERE id = 1 |
| | COMMIT |

在上面的例子中，事务 1 锁定了 `id = 1` 记录，事务 2 修改了 `id = 1` 记录。因此，事务 1 和事务 2 具有潜在的因果关系。即使启用了因果一致性，只要事务 2 在事务 1 成功提交后提交，从逻辑上讲，事务 2 必须发生在事务 1 之后。因此，不可能出现事务读取到事务 2 对 `id = 1` 记录的修改，但没有读取到事务 1 对 `id = 2` 记录的修改的情况。

### 没有因果关系的事务不保证一致的逻辑顺序和物理提交顺序

假设 `id = 1` 和 `id = 2` 的初始值都是 `0`。假设事务 1 和事务 2 都采用因果一致性，并执行以下语句：

| 事务 1 | 事务 2 | 事务 3 |
|-------|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | |
| UPDATE t set v = 3 WHERE id = 2 | | |
| | UPDATE t SET v = 2 WHERE id = 1 | |
| | | BEGIN |
| COMMIT | | |
| | COMMIT | |
| | | SELECT v FROM t WHERE id IN (1, 2) |

在上面的例子中，事务 1 没有读取 `id = 1` 记录，所以事务 1 和事务 2 没有数据库已知的因果关系。当事务启用因果一致性时，即使事务 2 在物理时间顺序上在事务 1 提交后提交，TiDB 也不保证事务 2 在逻辑上发生在事务 1 之后。

如果事务 3 在事务 1 提交之前开始，并且在事务 2 提交后读取 `id = 1` 和 `id = 2` 记录，事务 3 可能会读取到 `id = 1` 的值为 `2` 但 `id = 2` 的值为 `0`。

### 不带锁的读取不会创建因果关系

假设事务 1 和事务 2 都采用因果一致性，并执行以下语句：

| 事务 1 | 事务 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| | UPDATE t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1 | |
| UPDATE t set v = 3 WHERE id = 2 | |
| | COMMIT |
| COMMIT | |

在上面的例子中，不带锁的读取不会创建因果关系。事务 1 和事务 2 已经创建了写偏差。在这种情况下，如果两个事务仍然具有因果关系，那将是不合理的。因此，启用因果一致性的两个事务没有确定的逻辑顺序。
