---
title: 事务
summary: 了解 TiDB Cloud 的事务概念。
---

# 事务

TiDB 提供完整的分布式事务支持，其模型在 [Google Percolator](https://research.google.com/pubs/pub36726.html) 的基础上进行了一些优化。

## 乐观事务模式

TiDB 的乐观事务模型在提交阶段才检测冲突。如果存在冲突，事务需要重试。但是，如果冲突严重，这种模式的效率会很低，因为重试前的操作都是无效的，需要重新执行。

假设数据库被用作计数器。高并发访问可能会导致严重的冲突，从而导致多次重试甚至超时。因此，在冲突严重的场景下，建议使用悲观事务模式，或者在系统架构层面解决问题，比如将计数器放在 Redis 中。不过，如果访问冲突不是很严重，乐观事务模型的效率还是很高的。

更多信息，请参阅 [TiDB 乐观事务模型](/optimistic-transaction.md)。

## 悲观事务模式

在 TiDB 中，悲观事务模式的行为与 MySQL 几乎相同。事务在执行阶段就会加锁，这样可以避免冲突情况下的重试，确保更高的成功率。通过使用悲观锁定，你还可以使用 `SELECT FOR UPDATE` 提前锁定数据。

但是，如果应用场景的冲突较少，乐观事务模型会有更好的性能表现。

更多信息，请参阅 [TiDB 悲观事务模式](/pessimistic-transaction.md)。

## 事务隔离级别

事务隔离是数据库事务处理的基础之一。隔离是事务的四个关键属性之一（通常称为 [ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)）。

TiDB 实现了快照隔离（Snapshot Isolation，SI）一致性，为了与 MySQL 兼容，将其标识为 `REPEATABLE-READ`。这与 [ANSI 可重复读隔离级别](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read)和 [MySQL 可重复读级别](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)有所不同。

更多信息，请参阅 [TiDB 事务隔离级别](/transaction-isolation-levels.md)。

## 非事务性 DML 语句

非事务性 DML 语句是一个被拆分成多个 SQL 语句（即多个批次）按顺序执行的 DML 语句。它通过牺牲事务的原子性和隔离性来提高批量数据处理的性能和易用性。

通常，内存消耗大的事务需要被拆分成多个 SQL 语句以绕过事务大小限制。非事务性 DML 语句将这个过程集成到 TiDB 内核中以实现相同的效果。通过拆分 SQL 语句来理解非事务性 DML 语句的效果会很有帮助。可以使用 `DRY RUN` 语法来预览拆分后的语句。

更多信息，请参阅[非事务性 DML 语句](/non-transactional-dml.md)。
