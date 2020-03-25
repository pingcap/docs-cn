---
title: CLUSTER_LOG
category: reference
---

# CLUSTER_LOG

集群日志表 `CLUSTER_LOG` 表主要用于集群日志查询，通过将查询条件下推到各个节点，降低日志查询对集群的影响，**性能影响小于 grep 命令**。

{{< copyable "sql" >}}

```sql
desc cluster_log;
```

```
+----------+---------------------------+------+------+---------+-------+
| Field    | Type                      | Null | Key  | Default | Extra |
+----------+---------------------------+------+------+---------+-------+
| TIME     | varchar(32)               | YES  |      | NULL    |       |
| TYPE     | varchar(64)               | YES  |      | NULL    |       |
| INSTANCE | varchar(64)               | YES  |      | NULL    |       |
| LEVEL    | varchar(8)                | YES  |      | NULL    |       |
| MESSAGE  | var_string(1024) unsigned | YES  |      | NULL    |       |
+----------+---------------------------+------+------+---------+-------+
5 rows in set (0.00 sec)
```

字段解释：

* TIME：日志打印时间。
* TYPE：对应节点信息表 `information_schema.cluster_info` 中的 TYPE 字段，可取值为 `tidb`，`pd` 或 `tikv`。
* INSTANCE：对应于节点信息表 `information_schema.cluster_info` 中的 INSTANCE 字段。
* LEVEL：日志级别。
* MESSAGE：日志内容。

> **注意事项：**
>日志表的所有字段都会下推到对应节点执行，所以为了降低使用集群日志表的开销，需尽可能地指定更多的条件，比如 select * from cluter_log where instance='tikv-1' 只会在 tikv-1 执行日志搜索。
>message 字段支持 like 和 regexp 正则表达式，对应的 pattern 会编译为 regexp，同时指定多个 message 条件，相当于 grep 命令的 pipeline 形式，例如：select * from cluster_log where message like 'coprocessor%' and message regexp '.*slow.*' 相当于在集群所有节点执行 grep 'coprocessor' xxx.log | grep -E '.*slow.*'。

在TiDB 4.0 之前要获取集群的日志需要逐个登录各个节点汇总日志。TiDB 4.0 有了集群日志表后，可以更高效地提供一个全局时间有序的日志搜索结果，对于全链路事件跟踪提供便利的手段，比如按照某一个 region id 搜索日志，可以查询该 region 生命周期的所有日志，类似的通过慢日志的 txn id 搜索全链路日志，可以查询该事务在各个节点扫描的 key 数量以及流量等信息。
