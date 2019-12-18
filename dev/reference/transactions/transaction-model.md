---
title: 事务模型
category: reference
---

# 事务模型

TiDB 默认使用乐观事务模型。也就是说，在执行 `UPDATE`、`INSERT`、`DELETE` 等语句时，只有在提交过程中才会检查写写冲突，而不是像 MySQL 一样使用行锁来避免写写冲突。类似的，诸如 `GET_LOCK()` 和 `RELEASE_LOCK()` 等函数以及 `SELECT .. FOR UPDATE` 之类的语句在 TiDB 和 MySQL 中的执行方式并不相同。所以业务端在执行 SQL 语句后，需要注意检查 `COMMIT` 的返回值，即使执行时没有出错，`COMMIT` 的时候也可能会出错。

## 事务限制

由于 TiDB 分布式两阶段提交的要求，修改数据的大事务可能会出现一些问题。因此，TiDB 特意对事务大小设置了一些限制以减少这种影响：

* 单个事务包含的 SQL 语句不超过 5000 条（默认）
* 每个键值对不超过 6MB
* 键值对的总大小不超过 100MB

## 基于事务模型的优化实践

由于 TiDB 中的每个事务都需要跟 PD leader 进行两次 round trip，TiDB 中的事务相比于 MySQL 中的事务延迟更高。以如下的 query 为例，用显式事务代替 `autocommit`，可优化该 query 的性能。

使用 `autocommit` 的原始版本：

{{< copyable "sql" >}}

```sql
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
```

优化后的版本：

{{< copyable "sql" >}}

```sql
START TRANSACTION;
UPDATE my_table SET a='new_value' WHERE id = 1;
UPDATE my_table SET a='newer_value' WHERE id = 2;
UPDATE my_table SET a='newest_value' WHERE id = 3;
COMMIT;
```

> **注意：**
>
> 由于 TiDB 中的资源是分布式的，TiDB 中单线程 workload 可能不会很好地利用分布式资源，因此性能相比于单实例部署的 MySQL 较低。这与 TiDB 中的事务延迟较高的情況类似。
