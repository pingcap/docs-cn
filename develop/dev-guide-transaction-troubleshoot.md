---
title: 事务错误处理
summary: 介绍 TiDB 中的事务错误处理办法。
aliases: ['/zh/tidb/dev/transaction-troubleshoot','/zh/tidb/stable/dev-guide-transaction-troubleshoot/','/zh/tidb/dev/dev-guide-transaction-troubleshoot/','/zh/tidbcloud/dev-guide-transaction-troubleshoot/']
---

# 事务错误处理

本章介绍使用事务时可能会遇到的错误和处理办法。

## 死锁

如果应用程序遇到下面错误时，说明遇到了死锁问题：

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

当两个及以上的事务，双方都在等待对方释放已经持有的锁或因为加锁顺序不一致，造成循环等待锁资源，就会出现“死锁”。这里以 [bookshop](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `books` 表为示例演示死锁：

先给 `books` 表中写入 2 条数据：

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

在 TiDB 悲观事务模式下，用 2 个客户端分别执行以下语句，就会遇到死锁：

| 客户端-A                                                   | 客户端-B                                                         |
| ---------------------------------------------------------- | ---------------------------------------------------------------- |
| BEGIN;                                                     |                                                                  |
|                                                            | BEGIN;                                                           |
| UPDATE books SET stock=stock-1 WHERE id=1;                 |                                                                  |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=2;                       |
| UPDATE books SET stock=stock-1 WHERE id=2; -- 执行会被阻塞 |                                                                  |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=1; -- 遇到 Deadlock 错误 |

在客户端-B 遇到死锁错误后，TiDB 会自动 `ROLLBACK` 客户端-B 中的事务，然后客户端-A 中购买 `id=2` 的操作就会执行成功，再执行 `COMMIT` 即可完成购买的事务流程。

### 解决方案 1：避免死锁

为了应用程序有更好的性能，可以通过调整业务逻辑或者 Schema 设计，尽量从应用层面避免死锁。例如上面示例中，如果客户端-B 也和客户端-A 用同样的购买顺序，即都先买 `id=1` 的书，再买 `id=2` 的书，就可以避免死锁了：

| 客户端-A                                   | 客户端-B                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------------------- |
| BEGIN;                                     |                                                                                       |
|                                            | BEGIN;                                                                                |
| UPDATE books SET stock=stock-1 WHERE id=1; |                                                                                       |
|                                            | UPDATE books SET stock=stock-1 WHERE id=1; -- 执行会被阻塞，当事务 A 完成后再继续执行 |
| UPDATE books SET stock=stock-1 WHERE id=2; |                                                                                       |
|                                            | UPDATE books SET stock=stock-1 WHERE id=2;                                            |
| COMMIT;                                    |                                                                                       |
|                                            | COMMIT;                                                                               |

或者直接用 1 条 SQL 购买 2 本书，也能避免死锁，而且执行效率更高：

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解决方案 2：减小事务粒度

如果每次购书都是一个单独的事务，也能避免死锁。但需要权衡的是，事务粒度太小不符合性能上的最佳实践。

### 解决方案 3：使用乐观事务

乐观事务模型下，并不会有死锁问题，但应用端需要加上乐观事务在失败后的重试逻辑，具体重试逻辑见[应用端重试和错误处理](#应用端重试和错误处理)。

### 解决方案 4：重试

正如错误信息中提示的那样，在应用代码中加入重试逻辑即可。具体重试逻辑见[应用端重试和错误处理](#应用端重试和错误处理)。

## 应用端重试和错误处理

尽管 TiDB 尽可能地与 MySQL 兼容，但其分布式系统的性质导致了某些差异，其中之一就是事务模型。

开发者用来与数据库通信的 Adapter 和 ORM 都是为 MySQL 和 Oracle 等传统数据库量身定制的，在这些数据库中，提交很少在默认隔离级别失败，因此不需要重试机制。对于这些客户端，当提交失败时，它们会因错误而中止，因为这在这些数据库中被呈现为罕见的异常。

与 MySQL 等传统数据库不同的是，在 TiDB 中，如果采用乐观事务模型，想要避免提交失败，需要在自己的应用程序的业务逻辑中添加机制来处理相关的异常。

下面的类似 Python 的伪代码展示了如何实现应用程序级的重试。 它不要求您的驱动程序或 ORM 来实现高级重试处理逻辑，因此可以在任何编程语言或环境中使用。

特别是，您的重试逻辑必须：

- 如果失败重试的次数达到 `max_retries` 限制，则抛出错误
- 使用 `try ... catch ...` 语句捕获 SQL 执行异常，当遇到下面这些错误时进行失败重试，遇到其它错误则进行回滚。详细信息请参考：[错误码与故障诊断](https://docs.pingcap.com/tidb/stable/error-codes)。
    - `Error 8002: can not retry select for update statement`：SELECT FOR UPDATE 写入冲突报错。
    - `Error 8022: Error: KV error safe to retry`：事务提交失败报错。
    - `Error 8028: Information schema is changed during the execution of the statement`：表的 Schema 结构因为完成了 DDL 变更，导致事务提交时报错。
    - `Error 9007: Write conflict`：写冲突报错，一般是采用乐观事务模式时，多个事务都对同一行数据进行修改时遇到的写冲突报错。
- 在 try 块结束时使用 COMMIT 提交事务：

```python
while True:
    n++
    if n == max_retries:
        raise("did not succeed within #{n} retries")
    try:
        connection.execute("your sql statement here")
        connection.exec('COMMIT')
        break
    catch error:
        if (error.code != "9007" && error.code != "8028" && error.code != "8002" && error.code != "8022"):
            raise error
        else:
            connection.exec('ROLLBACK')

            # Capture the error types that require application-side retry,
            # wait for a short period of time,
            # and exponentially increase the wait time for each transaction failure
            sleep_ms = int(((1.5 ** n) + rand) * 100)
            sleep(sleep_ms) # make sure your sleep() takes milliseconds
```

> **注意：**
>
> 如果你经常遇到 `Error 9007: Write conflict` 错误，你可能需要进一步评估你的 Schema 设计和数据存取模型，找到冲突的根源并从设计上避免冲突。
> 关于如何定位和解决事务冲突，请参考[TiDB 锁冲突问题处理](/troubleshoot-lock-conflicts.md)。

## 推荐阅读

- [TiDB 锁冲突问题处理](/troubleshoot-lock-conflicts.md)
- [乐观事务模型下写写冲突问题排查](/troubleshoot-write-conflicts.md)
