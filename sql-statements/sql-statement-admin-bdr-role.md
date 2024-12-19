---
title: ADMIN [SET|SHOW|UNSET] BDR ROLE
summary: TiDB 数据库中 ADMIN [SET|SHOW|UNSET] BDR ROLE 的使用概况。
---

# ADMIN [SET|SHOW|UNSET] BDR ROLE

- `ADMIN SET BDR ROLE` 可以设置该集群的 BDR role。现在 TiDB 集群可以设置 `PRIMARY`、`SECONDARY` 两种 BDR role。关于 BDR role 的详细信息可参考 [TiCDC 双向复制的 DDL 同步](/ticdc/ticdc-bidirectional-replication.md#ddl-同步)。
- `ADMIN SHOW BDR ROLE` 可以显示该集群的 BDR role。
- `ADMIN UNSET BDR ROLE` 可以撤销之前设置的 BDR role。

## 语法图

```ebnf+diagram
AdminShowBDRRoleStmt ::=
    'ADMIN' 'SHOW' 'BDR' 'ROLE'

AdminSetBDRRoleStmt ::=
    'ADMIN' 'SET' 'BDR' 'ROLE' ('PRIMARY' | 'SECONDARY')

AdminUnsetBDRRoleStmt ::=
    'ADMIN' 'UNSET' 'BDR' 'ROLE'
```

## 示例

TiDB 集群默认没有 BDR role。运行以下命令显示集群的 BDR 角色。

```sql
ADMIN SHOW BDR ROLE;
```

```sql
+----------+
| BDR_ROLE |
+----------+
|          |
+----------+
1 row in set (0.01 sec)
```

执行以下命令可以将 BDR role 设置为 `PRIMARY`。

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

撤销之前的设置。

```sql
ADMIN UNSET BDR ROLE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
|          |
+----------+
1 row in set (0.01 sec)
```

## MySQL 兼容性

`ADMIN [SET|SHOW|UNSET] BDR ROLE` 语句是 TiDB 对 MySQL 语法的扩展。
