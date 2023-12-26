---
title: ADMIN [SET|SHOW] BDR ROLE
summary: TiDB 数据库中 ADMIN [SET|SHOW] BDR ROLE 的使用概况。
---

# ADMIN [SET|SHOW] BDR ROLE

- `ADMIN SET BDR ROLE` 可以设置该集群的 BDR role。现在 TiDB 集群可以设置 `PRIMARY`、`SECONDARY` 和 `LOCAL_ONLY`（默认）三种 BDR role。关于 BDR role 的详细信息可参考 [TiCDC 双向复制的 DDL 同步小节](../ticdc/ticdc-bidirectional-replication.md#ddl-同步)。
- `ADMIN SHOW BDR ROLE` 可以显示该集群的 BDR role。

> **警告：**
>
> 双向复制的 DDL 同步目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

## 语法图

```ebnf+diagram
AdminShowBDRRoleStmt ::=
    'ADMIN' 'SHOW' 'BDR' 'ROLE'

AdminSetBDRRoleStmt ::=
    'ADMIN' 'SET' 'BDR' 'ROLE' ('PRIMARY' | 'SECONDARY' | 'LOCAL_ONLY')
```

## 示例

TiDB 集群的默认 BDR role 是 `LOCAL_ONLY`。

```sql
ADMIN SHOW BDR ROLE;
```

```sql
+------------+
| BDR_ROLE   |
+------------+
| local_only |
+------------+
1 row in set (0.01 sec)
```

把 BDR role 设置为 `PRIMARY`。

```sql
ADMIN SET BDR ROLE PRIMARY;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
| primary  |
+----------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`ADMIN [SET|SHOW] BDR ROLE` 语句是 TiDB 对 MySQL 语法的扩展。
