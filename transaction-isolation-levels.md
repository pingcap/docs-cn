---
title: TiDB 事务隔离级别
summary: 了解 TiDB 中的事务隔离级别。
---

# TiDB 事务隔离级别

<CustomContent platform="tidb">

事务隔离是数据库事务处理的基础之一。隔离是事务的四个关键特性之一（通常称为 [ACID](/glossary.md#acid)）。

</CustomContent>

<CustomContent platform="tidb-cloud">

事务隔离是数据库事务处理的基础之一。隔离是事务的四个关键特性之一（通常称为 [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)）。

</CustomContent>

SQL-92 标准定义了四个事务隔离级别：读未提交（Read Uncommitted）、读已提交（Read Committed）、可重复读（Repeatable Read）和串行化（Serializable）。详情请参见下表：

| 隔离级别  | 脏写   | 脏读 | 不可重复读     | 幻读 |
| :----------- | :------------ | :------------- | :----------| :-------- |
| READ UNCOMMITTED | 不可能 | 可能     | 可能     | 可能     |
| READ COMMITTED   | 不可能 | 不可能 | 可能     | 可能     |
| REPEATABLE READ  | 不可能 | 不可能 | 不可能 | 可能     |
| SERIALIZABLE     | 不可能 | 不可能 | 不可能 | 不可能 |

TiDB 实现了快照隔离（Snapshot Isolation，SI）一致性，为了与 MySQL 兼容，它将其标识为 `REPEATABLE-READ`。这与 [ANSI 可重复读隔离级别](#tidb-与-ansi-可重复读的区别)和 [MySQL 可重复读级别](#tidb-与-mysql-可重复读的区别)有所不同。

> **注意：**
>
> 从 TiDB v3.0 开始，事务的自动重试默认关闭。不建议开启自动重试，因为这可能会**破坏事务隔离级别**。详情请参考[事务重试](/optimistic-transaction.md#自动重试)。
>
> 从 TiDB v3.0.8 开始，新创建的 TiDB 集群默认使用[悲观事务模式](/pessimistic-transaction.md)。当前读（`for update` 读）是**不可重复读**。详情请参考[悲观事务模式](/pessimistic-transaction.md)。

## 可重复读隔离级别

可重复读隔离级别只能看到事务开始之前已经提交的数据，并且在事务执行期间不会看到未提交的数据或并发事务提交的更改。但是，事务语句可以看到其自身事务中之前执行的更新的效果，即使这些更新尚未提交。

对于在不同节点上运行的事务，其开始和提交顺序取决于从 PD 获取时间戳的顺序。

可重复读隔离级别的事务不能同时更新同一行。在提交时，如果事务发现该行在事务开始后已被另一个事务更新，则该事务会回滚。例如：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- 在悲观事务中，后执行的 `update` 语句会等待锁，直到持有锁的事务提交或回滚并释放行锁。
commit;                         |
                                |               commit; -- 事务提交失败并回滚。悲观事务可以成功提交。
```

### TiDB 与 ANSI 可重复读的区别

TiDB 中的可重复读隔离级别与 ANSI 可重复读隔离级别虽然名称相同，但实际上是不同的。根据 [A Critique of ANSI SQL Isolation Levels](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf) 论文中描述的标准，TiDB 实现的是快照隔离级别。这种隔离级别不允许严格幻读（A3），但允许宽松幻读（P3）和写偏斜。相比之下，ANSI 可重复读隔离级别允许幻读但不允许写偏斜。

### TiDB 与 MySQL 可重复读的区别

TiDB 中的可重复读隔离级别与 MySQL 中的不同。MySQL 的可重复读隔离级别在更新时不检查当前版本是否可见，这意味着即使在事务开始后该行已被更新，它仍然可以继续更新。相比之下，如果在事务开始后该行已被更新，TiDB 乐观事务会回滚并重试。在 TiDB 的乐观并发控制中，事务重试可能会失败，导致事务最终失败，而在 TiDB 的悲观并发控制和 MySQL 中，更新事务可以成功。

## 读已提交隔离级别

从 TiDB v4.0.0-beta 开始，TiDB 支持读已提交隔离级别。

由于历史原因，当前主流数据库的读已提交隔离级别本质上是 [Oracle 定义的一致性读隔离级别](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)。为了适应这种情况，TiDB 悲观事务中的读已提交隔离级别本质上也是一致性读行为。

> **注意：**
>
> 读已提交隔离级别仅在[悲观事务模式](/pessimistic-transaction.md)下生效。在[乐观事务模式](/optimistic-transaction.md)下，设置事务隔离级别为读已提交不会生效，事务仍然使用可重复读隔离级别。

从 v6.0.0 开始，TiDB 支持使用 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) 系统变量来优化在读写冲突较少场景下的时间戳获取。启用该变量后，TiDB 在执行 `SELECT` 时会尝试使用之前有效的时间戳来读取数据。该变量的初始值为事务的 `start_ts`。

- 如果 TiDB 在读取过程中没有遇到任何数据更新，则向客户端返回结果，`SELECT` 语句执行成功。
- 如果 TiDB 在读取过程中遇到数据更新：
    - 如果 TiDB 还未向客户端发送结果，TiDB 会尝试获取新的时间戳并重试该语句。
    - 如果 TiDB 已经向客户端发送了部分数据，TiDB 会向客户端报错。每次向客户端发送的数据量由 [`tidb_init_chunk_size`](/system-variables.md#tidb_init_chunk_size) 和 [`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size) 控制。

在使用 `READ-COMMITTED` 隔离级别、`SELECT` 语句较多且读写冲突较少的场景下，启用该变量可以避免获取全局时间戳的延迟和开销。

从 v6.3.0 开始，TiDB 支持通过启用系统变量 [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630) 来优化在点写冲突较少场景下的时间戳获取。启用该变量后，在执行点写语句时，TiDB 会尝试使用当前事务的有效时间戳来读取和锁定数据。TiDB 将以与启用 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600) 相同的方式读取数据。

目前，适用的点写语句类型包括 `UPDATE`、`DELETE` 和 `SELECT ...... FOR UPDATE`。点写语句指使用主键或唯一键作为过滤条件且最终执行算子包含 `POINT-GET` 的写语句。目前这三种点写语句有一个共同点：它们首先根据键值进行点查询，如果键存在则锁定该键，如果键不存在则返回空集。

- 如果点写语句的整个读取过程没有遇到更新的数据版本，TiDB 继续使用当前事务的时间戳来锁定数据。
    - 如果在获取锁的过程中由于时间戳过旧而发生写冲突，TiDB 会通过获取最新的全局时间戳来重试获取锁的过程。
    - 如果在获取锁的过程中没有发生写冲突或其他错误，则锁获取成功。
- 如果在读取过程中遇到更新的数据版本，TiDB 会尝试获取新的时间戳并重试该语句。

在 `READ-COMMITTED` 隔离级别下，点写语句较多但点写冲突较少的事务中，启用该变量可以避免获取全局时间戳的延迟和开销。

## TiDB 与 MySQL 读已提交的区别

MySQL 的读已提交隔离级别在大多数情况下符合一致性读特性。也有例外情况，比如[半一致性读](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)。TiDB 不支持这种特殊行为。

## 查看和修改事务隔离级别

你可以按如下方式查看和修改事务隔离级别。

查看当前会话的事务隔离级别：

```sql
SHOW VARIABLES LIKE 'transaction_isolation';
```

修改当前会话的事务隔离级别：

```sql
SET SESSION transaction_isolation = 'READ-COMMITTED';
```

有关配置和使用事务隔离级别的更多信息，请参见以下文档：

- [系统变量 `transaction_isolation`](/system-variables.md#transaction_isolation)
- [隔离级别](/pessimistic-transaction.md#隔离级别)
- [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)
