---
title: 事务限制
---

# 事务限制

## 1. 隔离级别

TiDB 支持的隔离级别是 RC（Read Committed）与 SI（Snapshot Isolation），其中 SI 与 RR（Repeatable Read）隔离级别基本等价。

![隔离级别](/media/develop/transaction_isolation_level.png)

## 2. SI 可以克服幻读

TiDB 的 SI 隔离级别可以克服幻读异常（Phantom Reads），但 ANSI/ISO SQL 标准 中的 RR 不能。

所谓幻读是指：事务 A 首先根据条件查询得到 n 条记录，然后事务 B 改变了这 n 条记录之外的 m 条记录或者增添了 m 条符合事务 A 查询条件的记录，导致事务 A 再次发起请求时发现有 n+m 条符合条件记录，就产生了幻读。

例如：系统管理员 A 将数据库中所有学生的成绩从具体分数改为 ABCDE 等级，但是系统管理员 B 就在这个时候插入了一条具体分数的记录，当系统管理员 A 改结束后发现还有一条记录没有改过来，就好像发生了幻觉一样，这就叫幻读。

## 3. SI 不能克服写偏斜

TiDB 的 SI 隔离级别不能克服写偏斜异常（Write Skew），需要使用 Select for update 语法来克服写偏斜异常。

写偏斜异常是指两个并发的事务读取了不同但相关的记录，接着这两个事务各自更新了自己读到的数据，并最终都提交了事务，如果这些相关的记录之间存在着不能被多个事务并发修改的约束，那么最终结果将是违反约束的。

例如：值班表有两列，姓名以及值班状态，0 代表不值班，1 代表值班

| **姓名** | **值班状态** |
| -------- | ------------ |
| 张三     | 0            |
| 李四     | 0            |
| 王五     | 0            |

有这样一个事务，它的逻辑是判断当前无人值班，则分配一个值班人。当该程序顺序执行时，只会分配一个值班人。但当它并行执行时，就可能出现多人同时为值班状态的错误，造成这个错误的原因就是写偏斜。

## 4. 不支持 savepoint 和嵌套事务

Spring 支持的 PROPAGATION_NESTED 传播行为会启动一个嵌套的事务，它是当前事务之上独立启动的一个子事务。嵌套事务开始时会记录一个savepoint ，如果嵌套事务执行失败，事务将会回滚到 savepoint 的状态。嵌套事务是外层事务的一部分，它将会在外层事务提交时一起被提交。下面案例展示了savepoint 机制：

```sql
mysql> BEGIN;
mysql> INSERT INTO T2 VALUES(100);
mysql> SAVEPOINT svp1;
mysql> INSERT INTO T2 VALUES(200);
mysql> ROLLBACK TO SAVEPOINT svp1;
mysql> RELEASE SAVEPOINT svp1;
mysql> COMMIT;
mysql> SELECT * FROM T2;
+------+
|  ID   |
+------+
|  100 |
+------+
```

TiDB 不支持 savepoint 机制，因此也不支持 PROPAGATION_NESTED 传播行为。基于 Java Spring 框架的应用如果使用了 PROPAGATION_NESTED 传播行为，需要在应用端做出调整，将嵌套事务的逻辑移除。

## 5. 大事务限制

基本原则是要限制事务的大小。TiDB 对单个事务的大小有限制，这层限制是在 KV 层面。反映在 SQL 层面的话，简单来说一行数据会映射为一个 KV entry，每多一个索引，也会增加一个 KV entry。所以这个限制反映在 SQL 层面是：

- 最大单行记录容量为 120MB（TiDB v5.0 及更高的版本可通过 tidb-server 配置项 `performance.txn-entry-size-limit` 调整，低于 TiDB v5.0 的版本支持的单行容量为 6MB）
- 支持的最大单个事务容量为 10GB（TiDB v4.0 及更高版本可通过 tidb-server 配置项 `performance.txn-total-size-limit` 调整，低于 TiDB v4.0的版本支持的最大单个事务容量为 100MB）

另外注意，无论是大小限制还是行数限制，还要考虑事务执行过程中，TiDB 做编码以及事务额外 Key 的开销。在使用的时候，为了使性能达到最优，建议每 100 ～ 500 行写入一个事务。

## 6. 自动提交的 SELECT FOR UPDATE 语句不会等锁

自动提交下的 select for update 目前不会加锁。效果如下图所示：
![TiDB中的情况](/media/develop/autocommit_selectforupdate_nowaitlock.png)

这是已知的与 MySQL 不兼容的地方。

可以通过使用显式的 `begin;commit;` 解决该问题。
