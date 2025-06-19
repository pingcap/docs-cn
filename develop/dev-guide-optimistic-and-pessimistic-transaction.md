---
title: 乐观事务和悲观事务
summary: 了解 TiDB 中的乐观事务和悲观事务。
---

# 乐观事务和悲观事务

[乐观事务](/optimistic-transaction.md)模型直接提交事务，并在发生冲突时回滚。相比之下，[悲观事务](/pessimistic-transaction.md)模型会在实际提交事务之前尝试锁定需要修改的资源，只有在确保事务可以成功执行后才开始提交。

乐观事务模型适用于冲突率较低的场景，因为直接提交有较高的成功概率。但一旦发生事务冲突，回滚的成本相对较高。

悲观事务模型的优点是对于冲突率较高的场景，提前锁定的成本低于事后回滚的成本。而且，它可以解决多个并发事务由于冲突而无法提交的问题。然而，在冲突率较低的场景中，悲观事务模型的效率不如乐观事务模型。

悲观事务模型在应用程序端更直观且更容易实现。乐观事务模型需要复杂的应用程序端重试机制。

以下是一个[书店](/develop/dev-guide-bookshop-schema-design.md)的示例。它使用购买书籍的例子来展示乐观和悲观事务的优缺点。购买书籍的过程主要包括以下几个步骤：

1. 更新库存数量
2. 创建订单
3. 支付

这些操作必须要么全部成功，要么全部失败。你必须确保在并发事务的情况下不会发生超卖。

## 悲观事务

以下代码使用两个线程来模拟两个用户在悲观事务模式下购买同一本书的过程。书店里还剩 10 本书。Bob 买 6 本，Alice 买 4 本。他们几乎同时完成订单。最终，库存中的所有书籍都售罄。

<SimpleTab groupId="language">

<div label="Java" value="java">

因为你使用多个线程来模拟多个用户同时插入数据的情况，所以需要使用线程安全的连接对象。这里使用 Java 流行的连接池 [HikariCP](https://github.com/brettwooldridge/HikariCP) 进行演示。

</div>

<div label="Golang" value="golang">

Golang 中的 `sql.DB` 是并发安全的，所以不需要导入第三方包。

为了适配 TiDB 事务，根据以下代码编写工具包 [util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)：

```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

</div>

<div label="Python" value="python">

为了确保线程安全，你可以使用 mysqlclient 驱动程序打开多个不在线程之间共享的连接。

</div>

</SimpleTab>

### 编写悲观事务示例
