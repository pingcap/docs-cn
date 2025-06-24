---
title: SHOW PLUGINS
summary: TiDB 数据库中 SHOW PLUGINS 的使用概述。
---

# SHOW PLUGINS

`SHOW PLUGINS` 显示在 TiDB 中安装的所有插件，包括每个插件的状态和版本信息。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法

```ebnf+diagram
ShowPluginsStmt ::=
    "SHOW" "PLUGINS" ShowLikeOrWhere?
```

## 示例

```sql
SHOW PLUGINS;
```

```
+-------+--------------+-------+-----------------------------+---------+---------+
| Name  | Status       | Type  | Library                     | License | Version |
+-------+--------------+-------+-----------------------------+---------+---------+
| audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
+-------+--------------+-------+-----------------------------+---------+---------+
1 row in set (0.000 sec)
```

```sql
SHOW PLUGINS LIKE 'a%';
```

```
+-------+--------------+-------+-----------------------------+---------+---------+
| Name  | Status       | Type  | Library                     | License | Version |
+-------+--------------+-------+-----------------------------+---------+---------+
| audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
+-------+--------------+-------+-----------------------------+---------+---------+
1 row in set (0.000 sec)
```

## MySQL 兼容性

TiDB 中的 `SHOW PLUGINS` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

- [`ADMIN PLUGINS`](/sql-statements/sql-statement-admin.md#admin-plugins-related-statement)
