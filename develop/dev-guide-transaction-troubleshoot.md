---
title: Handle Transaction Errors
summary: Learn about how to handle transaction errors, such as deadlocks and application retry errors.
---

# Handle Transaction Errors

This document introduces how to handle transaction errors, such as deadlocks and application retry errors.

## Deadlocks

The following error in your application indicates a deadlock issue:

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

A deadlock occurs when two or more transactions are waiting for each other to release the lock they already hold, or the inconsistent lock order results in a loop waiting for the lock resources.

The following is an example of a deadlock using the table `books` in the [`bookshop`](/develop/dev-guide-bookshop-schema-design.md) database:

First, insert 2 rows into the table `books`:

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

In TiDB pessimistic transaction mode, if two clients execute the following statements respectively, a deadlock will occur:

| Client-A                                                      | Client-B                                                            |
| --------------------------------------------------------------| --------------------------------------------------------------------|
| BEGIN;                                                        |                                                                     |
|                                                               | BEGIN;                                                              |
| UPDATE books SET stock=stock-1 WHERE id=1;                    |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=2;                          |
| UPDATE books SET stock=stock-1 WHERE id=2; -- execution will be blocked |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=1; -- a deadlock error occurs |

After client-B encounters a deadlock error, TiDB automatically rolls back the transaction in client-B. Updating `id=2` in client-A will be executed successfully. You can then run `COMMIT` to finish the transaction.

### Solution 1: avoid deadlocks

To get better performance, you can avoid deadlocks at the application level by adjusting the business logic or schema design. In the example above, if client-B also uses the same update order as client-A, that is, they update books with `id=1` first, and then update books with `id=2`. The deadlock can then be avoided:

| Client-A                                                    | Client-B                                                         |
| ---------------------------------------------------------- | ----------------------------------------------------------------|
| BEGIN;                                                     |                                                                 |
|                                                            | BEGIN;                                                          |
| UPDATE books SET stock=stock-1 WHERE id=1;                 |                                                                 |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=1;  -- will be blocked  |
| UPDATE books SET stock=stock-1 WHERE id=2;                 |                                                                 |
| COMMIT;                                                    |                                                                 |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=2;                      |
|                                                            | COMMIT;                                                         |

Alternatively, you can update 2 books with 1 SQL statement, which can also avoid the deadlock and execute more efficiently:

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### Solution 2: reduce transaction granularity

If you only update 1 book in each transaction, you can also avoid deadlocks. However, the trade-off is that too small transaction granularity may affect performance.

### Solution 3: use optimistic transactions

There are no deadlocks in the optimistic transaction model. But in your application, you need to add the optimistic transaction retry logic in case of failure. For details, see [Application retry and error handling](#application-retry-and-error-handling).

### Solution 4: retry

Add the retry logic in the application as suggested in the error message. For details, see [Application retry and error handling](#application-retry-and-error-handling).

## Application retry and error handling

Although TiDB is as compatible as possible with MySQL, the nature of its distributed system leads to certain differences. One of them is the transaction model.

The Adapters and ORMs that developers use to connect with databases are tailored for traditional databases such as MySQL and Oracle. In these databases, transactions rarely fail to commit at the default isolation level, so retry mechanisms are not required. When a transaction fails to commit, these clients abort due to an error, as it is treated as an exception in these databases.

Different from traditional databases such as MySQL, in TiDB, if you use the optimistic transaction model and want to avoid commit failure, you need to add a mechanism to handle related exceptions in your applications.

The following Python pseudocode shows how to implement application-level retries. It does not require your driver or ORM to implement advanced retry logic. It can be used in any programming language or environment.

Your retry logic must follow the following rules:

- Throws an error if the number of failed retries reaches the `max_retries` limit.
- Use `try ... catch ...` to catch SQL execution exceptions. Retry when encountering the following errors. Roll back when encountering other errors.
    - `Error 8002: can not retry select for update statement`: SELECT FOR UPDATE write conflict error
    - `Error 8022: Error: KV error safe to retry`: transaction commit failed error.
    - `Error 8028: Information schema is changed during the execution of the statement`: Table schema has been changed by DDL operation, resulting in an error in the transaction commit.
    - `Error 9007: Write conflict`: Write conflict error, usually caused by multiple transactions modifying the same row of data when the optimistic transaction mode is used.
- `COMMIT` the transaction at the end of the try block.

<CustomContent platform="tidb">

For more information about error codes, see [Error Codes and Troubleshooting](/error-codes.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

For more information about error codes, see [Error Codes and Troubleshooting](https://docs.pingcap.com/tidb/stable/error-codes).

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

> **Note:**
>
> If you frequently encounter `Error 9007: Write conflict`, you may need to check your schema design and the data access patterns of your workload to find the root cause of the conflict and try to avoid conflicts by a better design.

<CustomContent platform="tidb">

For information about how to troubleshoot and resolve transaction conflicts, see [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

For information about how to troubleshoot and resolve transaction conflicts, see [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts).

</CustomContent>

## See also

<CustomContent platform="tidb">

- [Troubleshoot Write Conflicts in Optimistic Transactions](/troubleshoot-write-conflicts.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Troubleshoot Write Conflicts in Optimistic Transactions](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)

</CustomContent>