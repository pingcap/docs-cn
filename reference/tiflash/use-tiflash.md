---
title: 使用 TiFlash
category: reference
---

# 使用 TiFlash

TiFlash 部署完成后并不会自动同步数据，而需要手动指定需要同步的表。

用户可以使用 TiDB 或者 TiSpark 读取 TiFlash，TiDB 适合用于中等规模的 OLAP 计算，而 TiSpark 适合大规模的 OLAP 计算，用户可以根据自己的场景和使用习惯自行选择。具体参见：

- [使用 TiDB 读取 TiFlash](#使用-tidb-读取-tiflash)
- [使用 TiSpark 读取 TiFlash](#使用-tispark-读取-tiflash)

## 按表构建 TiFlash 副本

TiFlash 接入 TiKV 集群后，默认不会开始同步数据。可通过 MySQL 客户端向 TiDB 发送 DDL 命令来为特定的表建立 TiFlash 副本：

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count
```

该命令的参数说明如下：

- count 表示副本数，0 表示删除。

对于相同表的多次 DDL 命令，仅保证最后一次能生效。例如下面给出的操作 `tpch50` 表的两条 DDL 命令中，只有第二条删除副本的命令能生效：

为表建立 2 个副本：

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2
```

删除副本：

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0
```

注意事项：

* 假设有一张表 t 已经通过上述的 DDL 语句同步到 TiFlash，则通过以下语句创建的表也会自动同步到 TiFlash：

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE table_name like t
    ```

* 目前版本里，若先对表创建 TiFlash 副本，再使用 TiDB Lightning 导入数据，会导致数据导入失败。需要在使用 TiDB Lightning 成功导入数据至表后，再对相应的表创建 TiFlash 副本。

* 不推荐同步 1000 张以上的表，这会降低 PD 的调度性能。这个限制将在后续版本去除。

* TiFlash 中保留了数据库 system，用户不能为 TiDB 中名字为 system 数据库下的表创建 TiFlash 副本。如果强行创建，结果行为未定义（暂时性限制）。

## 查看表同步进度

可通过如下 SQL 语句查看特定表（通过 WHERE 语句指定，去掉 WHERE 语句则查看所有表）的 TiFlash 副本的状态：

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>'
```

查询结果中：

* AVAILABLE 字段表示该表的 TiFlash 副本是否可用。1 代表可用，0 代表不可用。
* PROGRESS 字段代表同步进度，在 0.0~1.0 之间，1 代表至少 1 个副本已经完成同步。

## 使用 TiDB 读取 TiFlash

TiDB 提供三种读取 TiFlash 副本的方式。如果添加了 TiFlash 副本，而没有做任何 engine 的配置，则默认使用 CBO 方式。

### 智能选择

对于创建了 TiFlash 副本的表，TiDB 优化器会自动根据代价估算选择是否使用 TiFlash 副本。具体有没有选择 TiFlash 副本，可以通过 `desc` 或 `explain analyze` 语句查看，例如：

{{< copyable "sql" >}}

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` 表示该任务会发送至 TiFlash 进行处理。如果没有选择 TiFlash 副本，可尝试通过 `analyze table` 语句更新统计信息后，再查看 `explain analyze` 结果。

### Engine 隔离

Engine 隔离是通过配置变量来指定所有的查询均使用指定 engine 的副本，可选 engine 为 tikv 和 tiflash，分别有 2 个配置级别：

1. 会话级别，即 SESSION 级别。设置语句：

    {{< copyable "sql" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "逗号分隔的 engine list";
    ```

    或者

    {{< copyable "sql" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "逗号分隔的 engine list";
    ```

    会话级别的默认配置继承自 TiDB 实例级别的配置，见 2。

2. TiDB 实例级别，即 INSTANCE 级别，和会话级别配置是交集关系。比如实例级别配置了 "tikv, tiflash"，而会话级别配置了 "tikv"，则只会读取 TiKV。

    在 TiDB 的配置文件添加如下配置项：

    ```
    [isolation-read]
    engines = ["tikv", "tiflash"]
    ```

    实例级别的默认配置为 `["tikv", "tiflash"]`。

当 engine 配置为 "tikv, tiflash"，即可以同时读取 TiKV 和 TiFlash 副本，优化器会自动选择。指定了 engine 后，对于查询中的表没有对应 engine 副本的情况（因为 TiKV 副本是必定存在的，因此只有配置了 engine 为 tiflash 而 TiFlash 副本不存在这一种情况），查询会报该表不存在该 engine 副本的错。

### 手工 Hint

手工 Hint 可以强制 TiDB 对于某张或某几张表使用 TiFlash 副本，其优先级低于 engine 隔离，如果 Hint 中指定的引擎不在 engine 列表中，会返回 warning，使用方法为：

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

Engine 隔离的优先级高于 CBO 与 Hint，Hint 优先级高于代价估算，即代价估算仅会选取指定 engine 的副本。

## 使用 TiSpark 读取 TiFlash

TiSpark 目前提供类似 TiDB 中 engine 隔离的方式读取 TiFlash，方式是通过配置参数 `spark.tispark.use.tiflash` 为 `true`（或 `false`）。

> **注意：**
>
> 设为 `true` 时，所有查询的表都会只读取 TiFlash 副本，设为 `false` 则只读取 TiKV 副本。设为 `true` 时，要求查询所用到的表都必须已创建了 TiFlash 副本，对于未创建 TiFlash 副本的表的查询会报错。

可以使用以下任意一种方式进行设置：

1. 在 `spark-defaults.conf` 文件中添加：

    ```
    spark.tispark.use.tiflash true
    ```

2. 在启动 Spark shell 或 Thrift server 时，启动命令中添加 `--conf spark.tispark.use.tiflash=true`

3. Spark shell 中实时设置：`spark.conf.set("spark.tispark.use.tiflash", true)`

4. Thrift server 通过 beeline 连接后实时设置：`set spark.tispark.use.tiflash=true`

## TiFlash 支持的计算下推

TiFlash 主要支持谓词、聚合下推计算，下推的计算可以帮助 TiDB 进行分布式加速。暂不支持的计算类型主要是表连接和 DISTINCT COUNT，会在后续版本逐步优化。

目前 TiFlash 支持了有限的常用表达式下推，想了解具体下推的表达式，请参考[该文件](https://github.com/pingcap/tidb/blob/release-3.1/expression/expression.go#L409)。

例如在聚合函数或者 WHERE 条件中包含了不在上述列表中的表达式，聚合或者相关的谓词过滤会无法进行下推。

如查询遇到不支持的下推计算，则需要依赖 TiDB 完成剩余计算，可能会很大程度影响 TiFlash 加速效果。对于暂不支持的表达式，将会在后续陆续加入支持，也可以联系官方沟通。
