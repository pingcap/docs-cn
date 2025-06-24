---
title: LOAD STATS
summary: TiDB 数据库中 LOAD STATS 的使用概览。
---

# LOAD STATS

`LOAD STATS` 语句用于将统计信息加载到 TiDB 中。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法图

```ebnf+diagram
LoadStatsStmt ::=
    'LOAD' 'STATS' stringLit
```

## 示例

你可以访问地址 `http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}` 来下载 TiDB 实例的统计信息。

你也可以使用 `LOAD STATS ${stats_path}` 来加载特定的统计信息文件。

`${stats_path}` 可以是绝对路径或相对路径。如果使用相对路径，则从启动 `tidb-server` 的路径开始查找相应的文件。以下是一个示例：

{{< copyable "sql" >}}

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [统计信息](/statistics.md)
