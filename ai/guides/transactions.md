---
title: 事务
summary: 了解如何在你的应用中使用事务。
---

# 事务

TiDB 支持 ACID 事务，以确保数据一致性和可靠性。

## 基本用法

```python
with client.session() as session:
    initial_total_balance = session.query("SELECT SUM(balance) FROM players").scalar()

    # Transfer 10 coins from player 1 to player 2
    session.execute("UPDATE players SET balance = balance - 10 WHERE id = 1")
    session.execute("UPDATE players SET balance = balance + 10 WHERE id = 2")

    session.commit()
    # or session.rollback()

    final_total_balance = session.query("SELECT SUM(balance) FROM players").scalar()
    assert final_total_balance == initial_total_balance
```

## 另请参阅

- [TiDB Developer Guide - Transactions](/develop/dev-guide-transaction-overview.md)
- [TiDB Documentation - SQL Reference - Transactions](/transaction-overview.md)