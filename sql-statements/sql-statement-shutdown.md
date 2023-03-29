---
title: SHUTDOWN
summary: TiDB 数据库中 SHUTDOWN 的使用概况。
---

# SHUTDOWN

`SHUTDOWN` 语句用于在 TiDB 中执行停机操作。执行 `SHUTDOWN` 语句需要用户拥有 `SHUTDOWN privilege`。

## 语法图

**Statement:**

![Statement](/media/sqlgram/ShutdownStmt.png)

## 示例

{{< copyable "sql" >}}

```sql
SHUTDOWN;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

> **注意：**
>
> 由于 TiDB 是分布式数据库，因此 TiDB 中的停机操作停止的是客户端连接的 TiDB 实例，而不是整个 TiDB 集群。

`SHUTDOWN` 语句与 MySQL 不完全兼容。如发现任何其他兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。
