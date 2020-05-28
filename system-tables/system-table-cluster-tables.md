---
title: CLUSTER TABLES
category: reference
aliases: ['/docs-cn/dev/reference/system-databases/cluster-tables/']
---

# CLUSTER TABLES

TiDB 有些系统表只包含单个 TiDB 节点的数据，如果想查询集群所有节点的系统表数据，可以使用 TiDB 4.0 新增的集群系统表。

| 单节点系统表                 | 集群系统表                         |
| -------------------------- | ---------------------------------- |
| PROCESSLIST                | CLUSTER_PROCESSLIST                |
| SLOW_QUERY                 | CLUSTER_SLOW_QUERY                 |
| STATEMENTS_SUMMARY         | CLUSTER_STATEMENTS_SUMMARY         |
| STATEMENTS_SUMMARY_HISTORY | CLUSTER_STATEMENTS_SUMMARY_HISTORY |

如上表中，集群系统表的表名是 `CLUSTER_` 前缀加上对应的单节点系统表名。在表结构上，集群系统表多一个 `INSTANCE` 列，表示该行数据来自的 TiDB 节点地址。

## 示例

集群系统表使用上和单节点系统表并无差异，以下以 `CLUSTER_PROCESSLIST` 作为示例。

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| INSTANCE        | ID  | USER | HOST     | DB   | COMMAND | TIME | STATE      | INFO                                                 | MEM | TxnStart                               |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
| 10.0.1.22:10080 | 150 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077223) |
| 10.0.1.22:10080 | 138 | root | 10.0.1.1 | test | Query   | 0    | autocommit | SELECT * FROM information_schema.cluster_processlist | 0   | 05-28 03:54:21.230(416976223923077220) |
| 10.0.1.22:10080 | 151 | u1   | 10.0.1.1 | test | Query   | 0    | autocommit | select count(*) from usertable                       | 372 | 05-28 03:54:21.230(416976223923077224) |
| 10.0.1.21:10080 | 15  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077222) |
| 10.0.1.21:10080 | 14  | u2   | 10.0.1.1 | test | Query   | 0    | autocommit | select max(field0) from usertable                    | 496 | 05-28 03:54:21.230(416976223923077225) |
+-----------------+-----+------+----------+------+---------+------+------------+------------------------------------------------------+-----+----------------------------------------+
```

以上查询的是集群中所有 TiDB 节点正在执行的请求，其中 `INSTANCE` 表示的是对应 TiDB 服务的 `STATUS_ADDRESS`。

## 集群系统表的实现

查询集群系统表时，TiDB 也会将相关计算下推给其他节点执行，而不是把所有节点的数据都取回来，可以查下相应的执行计划，示例如下：

{{< copyable "sql" >}}

```sql
desc select count(*) from information_schema.cluster_slow_query where user = 'u1';
```

```
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| id                       | estRows  | task      | access object            | operator info                                        |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
| StreamAgg_20             | 1.00     | root      |                          | funcs:count(Column#53)->Column#51                    |
| └─TableReader_21         | 1.00     | root      |                          | data:StreamAgg_9                                     |
|   └─StreamAgg_9          | 1.00     | cop[tidb] |                          | funcs:count(1)->Column#53                            |
|     └─Selection_19       | 10.00    | cop[tidb] |                          | eq(information_schema.cluster_slow_query.user, "u1") |
|       └─TableFullScan_18 | 10000.00 | cop[tidb] | table:CLUSTER_SLOW_QUERY | keep order:false, stats:pseudo                       |
+--------------------------+----------+-----------+--------------------------+------------------------------------------------------+
```

上面执行计划表示，会将 `user = u1` 条件下推给其他的 （`cop`） TiDB 节点执行，也会把聚合算子下推（即图中的 `StreamAgg` 算子）。

目前由于没有对系统表收集统计信息，所以有时会导致某些聚合算子不能下推，导致执行较慢，用户可以通过手动指定聚合下推的 SQL HINT 来将聚合算子下推，示例如下：

```sql
select /*+ AGG_TO_COP() */ count(*) from information_schema.cluster_slow_query group by user;
```
