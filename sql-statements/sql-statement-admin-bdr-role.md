---
title: ADMIN [SET|SHOW] BDR ROLE
summary: TiDB 数据库中 ADMIN [SET|SHOW] BDR ROLE 的使用概况。
---

# ADMIN [SET|SHOW] BDR ROLE

- `ADMIN SET BDR ROLE` 可以设置该集群的 BDR role。现在 TiDB 集群可以设置 `PRIMARY`、`SECONDAR` 和 `LOCAL_ONLY`（默认）三种 BDR role。关于 BDR role 的详细信息可参考 [TiCDC 双向复制的 DDL 同步小节](../ticdc/ticdc-bidirectional-replication.md#ddl-同步)。
- `ADMIN SHOW BDR ROLE` 可以显示该集群的 BDR role。

> **警告：**
>
> 在当前版本中，双向复制的 DDL 同步为实验特性，不建议在生产环境中使用。

## 语法图

```ebnf+diagram
AdminShowBDRRoleStmt ::=
    'ADMIN' 'SHOW' 'BDR' 'ROLE'

AdminSetBDRRoleStmt ::=
    'ADMIN' 'SET' 'BDR' 'ROLE' ('PRIMARY' | 'SECONDARY' | 'LOCAL_ONLY')
```

## 示例

TiDB 集群的默认 BDR role 是 `LOCAL_ONLY`。

{{< copyable "sql" >}}

```sql
mysql> admin show bdr role;
+------------+
| BDR_ROLE   |
+------------+
| local_only |
+------------+
1 row in set (0.01 sec)
```

把 BDR role 设置为 `PRIMARY`。

{{< copyable "sql" >}}

```sql
mysql> admin set bdr role primary;
Query OK, 0 rows affected (0.01 sec)

mysql> admin show bdr role;
+----------+
| BDR_ROLE |
+----------+
| primary  |
+----------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`ADMIN [SET|SHOW] BDR ROLE` 语句是 TiDB 对 MySQL 语法的扩展。

