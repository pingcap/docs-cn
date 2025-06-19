---
title: 处理事务错误
summary: 了解如何处理事务错误，例如死锁和应用程序重试错误。
---

# 处理事务错误

本文档介绍如何处理事务错误，例如死锁和应用程序重试错误。

## 死锁

应用程序中出现以下错误表示存在死锁问题：

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

当两个或多个事务互相等待对方释放已持有的锁，或者不一致的锁顺序导致循环等待锁资源时，就会发生死锁。

以下是使用 [`bookshop`](/develop/dev-guide-bookshop-schema-design.md) 数据库中的 `books` 表的死锁示例：

首先，向 `books` 表中插入 2 行数据：

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

在 TiDB 悲观事务模式下，如果两个客户端分别执行以下语句，将会发生死锁：

| 客户端 A                                                      | 客户端 B                                                            |
| --------------------------------------------------------------| --------------------------------------------------------------------|
| BEGIN;                                                        |                                                                     |
|                                                               | BEGIN;                                                              |
| UPDATE books SET stock=stock-1 WHERE id=1;                    |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=2;                          |
| UPDATE books SET stock=stock-1 WHERE id=2; -- 执行将被阻塞 |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=1; -- 发生死锁错误 |

当客户端 B 遇到死锁错误时，TiDB 会自动回滚客户端 B 的事务。客户端 A 中更新 `id=2` 的操作将成功执行。然后你可以运行 `COMMIT` 完成事务。

### 解决方案 1：避免死锁

为了获得更好的性能，你可以通过调整业务逻辑或架构设计在应用程序层面避免死锁。在上面的示例中，如果客户端 B 也使用与客户端 A 相同的更新顺序，即先更新 `id=1` 的图书，然后更新 `id=2` 的图书，就可以避免死锁：

| 客户端 A                                                    | 客户端 B                                                         |
| ---------------------------------------------------------- | ----------------------------------------------------------------|
| BEGIN;                                                     |                                                                 |
|                                                            | BEGIN;                                                          |
| UPDATE books SET stock=stock-1 WHERE id=1;                 |                                                                 |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=1;  -- 将被阻塞  |
| UPDATE books SET stock=stock-1 WHERE id=2;                 |                                                                 |
| COMMIT;                                                    |                                                                 |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=2;                      |
|                                                            | COMMIT;                                                         |

或者，你可以使用 1 条 SQL 语句更新 2 本书，这样也可以避免死锁并且执行效率更高：

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### 解决方案 2：减小事务粒度

如果你在每个事务中只更新 1 本书，也可以避免死锁。但是，过小的事务粒度可能会影响性能。

### 解决方案 3：使用乐观事务

在乐观事务模型中不会出现死锁。但是在你的应用程序中，你需要添加乐观事务重试逻辑以防失败。详情请参阅[应用程序重试和错误处理](#应用程序重试和错误处理)。

### 解决方案 4：重试

按照错误消息的建议在应用程序中添加重试逻辑。详情请参阅[应用程序重试和错误处理](#应用程序重试和错误处理)。

## 应用程序重试和错误处理

尽管 TiDB 尽可能与 MySQL 兼容，但其分布式系统的特性导致某些差异。其中之一就是事务模型。

开发人员用来连接数据库的适配器和 ORM 是为 MySQL 和 Oracle 等传统数据库量身定制的。在这些数据库中，事务在默认隔离级别下很少提交失败，因此不需要重试机制。当事务提交失败时，这些客户端会因错误而中止，因为这在这些数据库中被视为异常情况。

与 MySQL 等传统数据库不同，在 TiDB 中，如果你使用乐观事务模型并希望避免提交失败，你需要在应用程序中添加处理相关异常的机制。

以下 Python 伪代码展示了如何实现应用程序级重试。它不需要你的驱动程序或 ORM 实现高级重试逻辑。它可以在任何编程语言或环境中使用。

你的重试逻辑必须遵循以下规则：

- 如果失败重试次数达到 `max_retries` 限制，则抛出错误。
- 使用 `try ... catch ...` 捕获 SQL 执行异常。遇到以下错误时重试。遇到其他错误时回滚。
    - `Error 8002: can not retry select for update statement`：SELECT FOR UPDATE 写冲突错误
    - `Error 8022: Error: KV error safe to retry`：事务提交失败错误。
    - `Error 8028: Information schema is changed during the execution of the statement`：表架构已被 DDL 操作更改，导致事务提交出错。
    - `Error 9007: Write conflict`：写冲突错误，通常在使用乐观事务模式时由多个事务修改同一行数据导致。
- 在 try 块的末尾 `COMMIT` 事务。

<CustomContent platform="tidb">

有关错误代码的更多信息，请参阅[错误码与故障诊断](/error-codes.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

有关错误代码的更多信息，请参阅[错误码与故障诊断](https://docs.pingcap.com/tidb/stable/error-codes)。

</CustomContent>

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
> 如果你经常遇到 `Error 9007: Write conflict`，你可能需要检查你的架构设计和工作负载的数据访问模式，找出冲突的根本原因，并尝试通过更好的设计来避免冲突。

<CustomContent platform="tidb">

有关如何排查和解决事务冲突的信息，请参阅[排查锁冲突](/troubleshoot-lock-conflicts.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

有关如何排查和解决事务冲突的信息，请参阅[排查锁冲突](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)。

</CustomContent>

## 另请参阅

<CustomContent platform="tidb">

- [排查乐观事务中的写入冲突](/troubleshoot-write-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [排查乐观事务中的写入冲突](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
