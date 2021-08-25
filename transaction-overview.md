---
title: TiDB 事务概览
summary: 了解 TiDB 中的事务。
---

# TiDB 事务概览

TiDB 支持分布式事务，提供[乐观事务](/optimistic-transaction.md)与[悲观事务](/pessimistic-transaction.md)两种事务模型。TiDB 3.0.8 及以后版本，TiDB 默认采用悲观事务模型。

本文主要介绍涉及事务的常用语句、显式/隐式事务、事务的隔离级别和惰性检查，以及事务大小的限制。

常用的变量包括 [`autocommit`](#自动提交)、[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)、[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 以及 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)。

> **注意：**
>
> 变量 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 和 [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 仅适用于乐观事务，不适用于悲观事务。

## 常用事务语句

### 开启事务

要显式地开启一个新事务，既可以使用 [`BEGIN`](/sql-statements/sql-statement-begin.md) 语句，也可以使用 [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) 语句，两者效果相同。

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

如果执行以上语句时，当前 Session 正处于一个事务的中间过程，那么系统会先自动提交当前事务，再开启一个新的事务。

> **注意：**
>
> 与 MySQL 不同的是，TiDB 在执行完上述语句后即会获取当前数据库快照，而 MySQL 的 `BEGIN` 和 `START TRANSACTION` 是在开启事务后的第一个从 InnoDB 读数据的 `SELECT` 语句（非 `SELECT FOR UPDATE`）后获取快照，`START TRANSACTION WITH CONSISTENT SNAPSHOT` 是语句执行时获取快照。因此，TiDB 中的 `BEGIN`、`START TRANSACTION` 和 `START TRANSACTION WITH CONSISTENT SNAPSHOT` 都等效为 MySQL 中的 `START TRANSACTION WITH CONSISTENT SNAPSHOT`。

### 提交事务

[`COMMIT`](/sql-statements/sql-statement-commit.md) 语句用于提交 TiDB 在当前事务中进行的所有修改。

语法：

{{< copyable "sql" >}}

```sql
COMMIT;
```

> **建议：**
>
> 启用[乐观事务](/optimistic-transaction.md)前，请确保应用程序可正确处理 `COMMIT` 语句可能返回的错误。如果不确定应用程序将会如何处理，建议改为使用[悲观事务](/pessimistic-transaction.md)。

### 回滚事务

[`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句用于回滚并撤销当前事务的所有修改。

语法：

{{< copyable "sql" >}}

```sql
ROLLBACK;
```

如果客户端连接中止或关闭，也会自动回滚该事务。

## 自动提交

为满足 MySQL 兼容性的要求，在默认情况下，TiDB 将在执行语句后立即进行 _autocommit_（自动提交）。

举例：

```sql
mysql> CREATE TABLE t1 (
    ->  id INT NOT NULL PRIMARY KEY auto_increment,
    ->  pad1 VARCHAR(100)
    -> );
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

以上示例中，`ROLLBACK` 语句没产生任何效果。由于 `INSERT` 语句是在自动提交的情况下执行的，等同于以下单语句事务：

```sql
START TRANSACTION;
INSERT INTO t1 VALUES (1, 'test');
COMMIT;
```

如果已显式地启动事务，则不适用自动提交。以下示例，`ROLLBACK` 语句成功撤回了 `INSERT` 语句：

```sql
mysql> CREATE TABLE t2 (
    ->  id INT NOT NULL PRIMARY KEY auto_increment,
    ->  pad1 VARCHAR(100)
    -> );
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

[`autocommit`](/system-variables.md#autocommit) 是一个系统变量，可以基于 Session 或 Global 进行[修改](/sql-statements/sql-statement-set-variable.md)。

举例：

{{< copyable "sql" >}}

```sql
SET autocommit = 0;
```

{{< copyable "sql" >}}

```sql
SET GLOBAL autocommit = 0;
```

## 显式事务和隐式事务

> **注意：**
>
> 有些语句是隐式提交的。例如，执行 `[BEGIN|START TRANCATION]` 语句时，TiDB 会隐式提交上一个事务，并开启一个新的事务以满足 MySQL 兼容性的需求。详情参见 [implicit commit](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)。

TiDB 可以显式地使用事务（通过 `[BEGIN|START TRANSACTION]`/`COMMIT` 语句定义事务的开始和结束）或者隐式地使用事务 (`SET autocommit = 1`)。

在自动提交状态下，使用 `[BEGIN|START TRANSACTION]` 语句会显式地开启一个事务，同时也会禁用自动提交，使隐式事务变成显式事务。直到执行 `COMMIT` 或 `ROLLBACK` 语句时才会恢复到此前默认的自动提交状态。

对于 DDL 语句，会自动提交并且不能回滚。如果运行 DDL 的时候，正在一个事务的中间过程中，会先自动提交当前事务，再执行 DDL。

## 惰性检查

执行 DML 语句时，乐观事务默认不会检查[主键约束](/constraints.md#主键约束)或[唯一约束](/constraints.md#唯一约束)，而是在 `COMMIT` 事务时进行这些检查。

举例：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
BEGIN OPTIMISTIC;
INSERT INTO t1 VALUES (1); -- MySQL 返回错误；TiDB 返回成功。
INSERT INTO t1 VALUES (2);
COMMIT; -- MySQL 提交成功；TiDB 返回错误，事务回滚。
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

mysql> COMMIT; -- MySQL 提交成功；TiDB 返回错误，事务回滚。
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
mysql> SELECT * FROM t1; -- MySQL 返回 1 2；TiDB 返回 1。
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

惰性检查优化通过批处理约束检查并减少网络通信来提升性能。可以通过设置 [`tidb_constraint_check_in_place = TRUE`](/system-variables.md#tidb_constraint_check_in_place) 禁用该行为。

> **注意：**
>
> + 本优化仅适用于乐观事务。
> + 本优化仅对普通的 `INSERT` 语句生效，对 `INSERT IGNORE` 和 `INSERT ON DUPLICATE KEY UPDATE` 不会生效。

## 语句回滚

TiDB 支持语句执行失败后的原子性回滚。如果语句报错，则所做的修改将不会生效。该事务将保持打开状态，并且在发出 `COMMIT` 或 `ROLLBACK` 语句之前可以进行其他修改。

{{< copyable "sql" >}}

```sql
CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
BEGIN;
INSERT INTO test VALUES (1);
INSERT INTO tset VALUES (2);  -- tset 拼写错误，使该语句执行出错。
INSERT INTO test VALUES (1),(2);  -- 违反 PRIMARY KEY 约束，语句不生效。
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

mysql> INSERT INTO tset VALUES (2);  -- tset 拼写错误，使该语句执行出错。
ERROR 1146 (42S02): Table 'test.tset' doesn't exist
mysql> INSERT INTO test VALUES (1),(2);  -- 违反 PRIMARY KEY 约束，语句不生效。
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
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

以上例子中，`INSERT` 语句执行失败之后，事务保持打开状态。最后的 `INSERT` 语句执行成功，并且提交了修改。

## 事务限制

由于底层存储引擎的限制，TiDB 要求单行不超过 6 MB。可以将一行的所有列根据类型转换为字节数并加和来估算单行大小。

TiDB 同时支持乐观事务与悲观事务，其中乐观事务是悲观事务的基础。由于乐观事务是先将修改缓存在私有内存中，因此，TiDB 对于单个事务的容量做了限制。

TiDB 中，单个事务的总大小默认不超过 100 MB，这个默认值可以通过配置文件中的配置项 `txn-total-size-limit` 进行修改，最大支持 10 GB。实际的单个事务大小限制还取决于服务器剩余可用内存的大小，执行事务时 TiDB 进程的内存消耗大约是事务大小的 6 倍以上。

在 4.0 以前的版本，TiDB 限制了单个事务的键值对的总数量不超过 30 万条，从 4.0 版本起 TiDB 取消了这项限制。

> **注意：**
>
> 通常，用户会开启 TiDB Binlog 将数据向下游进行同步。某些场景下，用户会使用消息中间件来消费同步到下游的 binlog，例如 Kafka。
>
> 以 Kafka 为例，Kafka 的单条消息处理能力的上限是 1 GB。因此，当把 `txn-total-size-limit` 设置为 1 GB 以上时，可能出现事务在 TiDB 中执行成功，但下游 Kafka 报错的情况。为避免这种情况出现，请用户根据最终消费者的限制来决定 `txn-total-size-limit` 的实际大小。例如：下游使用了 Kafka，则 `txn-total-size-limit` 不应超过 1 GB。

## 因果一致性事务

> **注意：**
>
> 因果一致性事务只在启用 Async Commit 特性和一阶段提交特性时生效。关于这两个特性的启用情况，请参见 [`tidb_enable_async_commit` 系统变量介绍](/system-variables.md#tidb_enable_async_commit-从-v50-版本开始引入)和 [`tidb_enable_1pc` 系统变量介绍](/system-variables.md#tidb_enable_1pc-从-v50-版本开始引入)。

TiDB 支持开启因果一致性的事务。因果一致性的事务在提交时无需向 PD 获取时间戳，所以提交延迟更低。开启因果一致性事务的语法为：

{{< copyable "sql" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

默认情况下，TiDB 保证线性一致性。在线性一致性的情况下，如果事务 2 在事务 1 提交完成后提交，逻辑上事务 2 就应该在事务 1 后发生。

因果一致性弱于线性一致性。在因果一致性的情况下，只有事务 1 和事务 2 加锁或写入的数据有交集时（即事务 1 和事务 2 存在数据库可知的因果关系时），才能保证事务的提交顺序与事务的发生顺序保持一致。目前暂不支持传入数据库外部的因果关系。

采用因果一致性的两个事务有以下特性：

+ [有潜在因果关系的事务之间的逻辑顺序与物理提交顺序一致](#有潜在因果关系的事务之间的逻辑顺序与物理提交顺序一致)
+ [无因果关系的事务之间的逻辑顺序与物理提交顺序不保证一致](#无因果关系的事务之间的逻辑顺序与物理提交顺序不保证一致)
+ [不加锁的读取不产生因果关系](#不加锁的读取不产生因果关系)

### 有潜在因果关系的事务之间的逻辑顺序与物理提交顺序一致

假设事务 1 和事务 2 都采用因果一致性，并先后执行如下语句：

| 事务 1 | 事务 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE | |
| UPDATE t set v = $(x + 1) WHERE id = 2 | |
| COMMIT | |
| | UPDATE t SET v = 2 WHERE id = 1 |
| | COMMIT |

上面的例子中，事务 1 对 `id = 1` 的记录加了锁，事务 2 的事务对 `id = 1` 的记录进行了修改，所以事务 1 和事务 2 有潜在的因果关系。所以即使用因果一致性开启事务，只要事务 2 在事务 1 提交成功后才提交，逻辑上事务 2 就必定比事务 1 晚发生。因此，不存在某个事务读到了事务 2 对 `id = 1` 记录的修改，但却没有读到事务 1 对 `id = 2` 记录的修改的情况。

### 无因果关系的事务之间的逻辑顺序与物理提交顺序不保证一致

假设 `id = 1` 和 `id = 2` 的记录最初值都为 0，事务 1 和事务 2 都采用因果一致性，并先后执行如下语句：

| 事务 1 | 事务 2 | 事务 3 |
|-------|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | |
| UPDATE t set v = 3 WHERE id = 2 | | |
| | UPDATE t SET v = 2 WHERE id = 1 | |
| | | BEGIN |
| COMMIT | | |
| | COMMIT | |
| | | SELECT v FROM t WHERE id IN (1, 2) |

在本例中，事务 1 不读取 `id = 1` 的记录。此时事务 1 和事务 2 没有数据库可知的因果关系。如果使用因果一致性开启事务，即使物理时间上事务 2 在事务 1 提交完成后才开始提交，TiDB 也不保证逻辑上事务 2 比事务 1 晚发生。

此时如果有一个事务 3 在事务 1 提交前开启，并在事务 2 提交后读取 `id = 1` 和 `id = 2` 的记录，事务 3 可能读到 `id = 1` 的值为 2 但是 `id = 2` 的值为 0。

### 不加锁的读取不产生因果关系

假设事务 1 和事务 2 都采用因果一致性，并先后执行如下语句：

| 事务 1 | 事务 2 |
|-------|-------|
| START TRANSACTION WITH CAUSAL CONSISTENCY ONLY | START TRANSACTION WITH CAUSAL CONSISTENCY ONLY |
| | UPDATE t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1 | |
| UPDATE t set v = 3 WHERE id = 2 | |
| | COMMIT |
| COMMIT | |

如本例所示，不加锁的读取不产生因果关系。事务 1 和事务 2 产生了写偏斜的异常，如果他们有业务上的因果关系，则是不合理的。所以本例中，使用因果一致性的事务 1 和事务 2 没有确定的逻辑顺序。
