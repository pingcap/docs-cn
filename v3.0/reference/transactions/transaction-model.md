---
title: 事务模型
category: reference
aliases: ['/docs-cn/sql/transaction-model/']
---

# 事务模型

TiDB 使用乐观事务模型，在执行 `UPDATE`、`INSERT`、`DELETE` 等语句时，只有在提交过程中，执行 `UPDATE`，`INSERT`，`DELETE` 等语句时才会检查写写冲突，而不是像 MySQL 一样使用行锁来避免写写冲突。类似的，诸如 `GET_LOCK()` 和 `RELEASE_LOCK()` 等函数以及 `SELECT .. FOR UPDATE` 之类的语句在 TiDB 和 MySQL 中的执行方式并不相同。所以业务端在执行 SQL 语句后，需要注意检查 `COMMIT` 的返回值，即使执行时没有出错，`COMMIT` 的时候也可能会出错。

## 与 MySQL 行为及性能对比

### 事务重试

执行失败的事务默认**不会**自动重试，因为这会导致更新丢失。可通过配置 `tidb_disable_txn_auto_retry = off` 开启该项功能。

## 大事务

由于 TiDB 分布式两阶段提交的要求，修改数据的大事务可能会出现一些问题。因此，TiDB 特意对事务大小设置了一些限制以减少这种影响：

* 单个事务包含的 SQL 语句不超过 5000 条（默认）
* 每个键值对不超过 6MB
* 键值对的总数不超过 300,000
* 键值对的总大小不超过 100MB

## 小事务

由于 TiDB 中的每个事务都需要跟 PD leader 进行两次 round trip，TiDB 中的小事务相比于 MySQL 中的小事务延迟更高。以如下的 query 为例，用显式事务代替 `auto_commit`，可优化该 query 的性能。

```sql
# 使用 auto_commit 的原始版本
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;

# 优化后的版本
START TRANSACTION;
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
COMMIT;
```

### 单线程或时延敏感型 workload

由于 TiDB 中的 workload 是分布式的，TiDB 中单线程或时延敏感型 workload 的性能相比于单实例部署的 MySQL 较低。这与 TiDB 中的小事务延迟较高的情況类似。

### Load data

* 语法：

    ```sql
    LOAD DATA LOCAL INFILE 'file_name' INTO TABLE table_name
        {FIELDS | COLUMNS} TERMINATED BY 'string' ENCLOSED BY 'char' ESCAPED BY 'char'
        LINES STARTING BY 'string' TERMINATED BY 'string'
        IGNORE n LINES
        (col_name ...);
    ```

    其中 ESCAPED BY 目前只支持 '/\/\'。

* 事务的处理：

    TiDB 在执行 `LOAD DATA` 操作时，默认将每 2 万行记录作为一个事务进行持久化存储。如果一次 `LOAD DATA` 操作插入的数据超过 2 万行，那么会分为多个事务进行提交。如果某个事务出错，这个事务会提交失败，但它前面的事务仍然会提交成功，在这种情况下，一次 `LOAD DATA` 操作会有部分数据插入成功，部分数据插入失败。而 MySQL 中会将一次 `LOAD DATA` 操作视为一个事务，如果其中发生失败情况，将会导致整个 `LOAD DATA` 操作失败。

    > **注意：**
    >
    > `LOAD DATA` 在 TiDB 中默认会拆分事务后分批提交，这种拆分事务提交的方式是以打破事务的原子性和隔离性为代价的，使用该特性时，使用者需要保证没有其他对正在处理的表的**任何**操作，并且在出现报错时，需要及时**人工介入，检查数据的一致性和完整性**。不建议在生产环境中使用。
