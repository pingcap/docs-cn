---
title: 使用 TiFlash
aliases: ['/docs-cn/stable/tiflash/use-tiflash/','/docs-cn/v4.0/tiflash/use-tiflash/','/docs-cn/stable/reference/tiflash/use-tiflash/','/docs-cn/v4.0/reference/tiflash/use-tiflash/']
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

* 如果集群版本 \< v4.0.6，若先对表创建 TiFlash 副本，再使用 TiDB Lightning 导入数据，会导致数据导入失败。需要在使用 TiDB Lightning 成功导入数据至表后，再对相应的表创建 TiFlash 副本。

* 如果集群版本以及 TiDB Lightning 版本均 \>= v4.0.6，无论一个表是否已经创建 TiFlash 副本，你均可以使用 TiDB Lightning 导入数据至该表。但注意此情况会导致 TiDB Lightning 导入数据耗费的时间延长，具体取决于 TiDB Lightning 部署机器的网卡带宽、TiFlash 节点的 CPU 及磁盘负载、TiFlash 副本数等因素。

* 不推荐同步 1000 张以上的表，这会降低 PD 的调度性能。这个限制将在后续版本去除。

## 查看表同步进度

可通过如下 SQL 语句查看特定表（通过 WHERE 语句指定，去掉 WHERE 语句则查看所有表）的 TiFlash 副本的状态：

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>'
```

查询结果中：

* AVAILABLE 字段表示该表的 TiFlash 副本是否可用。1 代表可用，0 代表不可用。副本状态为可用之后就不再改变，如果通过 DDL 命令修改副本数则会重新计算同步进度。
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

需要注意的是，如果表仅有单个 TiFlash 副本且相关节点无法服务，智能选择模式下的查询会不断重试，需要指定 Engine 或者手工 Hint 来读取 TiKV 副本。

### Engine 隔离

Engine 隔离是通过配置变量来指定所有的查询均使用指定 engine 的副本，可选 engine 为 "tikv"、"tidb" 和 "tiflash"（其中 "tidb" 表示 TiDB 内部的内存表区，主要用于存储一些 TiDB 系统表，用户不能主动使用），分别有 2 个配置级别：

1. TiDB 实例级别，即 INSTANCE 级别。在 TiDB 的配置文件添加如下配置项：

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **实例级别的默认配置为 `["tikv", "tidb", "tiflash"]`。**

2. 会话级别，即 SESSION 级别。设置语句：

    {{< copyable "sql" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "逗号分隔的 engine list";
    ```

    或者

    {{< copyable "sql" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "逗号分隔的 engine list";
    ```

    **会话级别的默认配置继承自 TiDB 实例级别的配置。**

最终的 engine 配置为会话级别配置，即会话级别配置会覆盖实例级别配置。比如实例级别配置了 "tikv"，而会话级别配置了 "tiflash"，则会读取 TiFlash 副本。当 engine 配置为 "tikv, tiflash"，即可以同时读取 TiKV 和 TiFlash 副本，优化器会自动选择。

> **注意：**
>
> 由于 [TiDB Dashboard](/dashboard/dashboard-intro.md) 等组件需要读取一些存储于 TiDB 内存表区的系统表，因此建议实例级别 engine 配置中始终加入 "tidb" engine。

如果查询中的表没有对应 engine 的副本，比如配置了 engine 为 "tiflash" 而该表没有 TiFlash 副本，则查询会报该表不存在该 engine 副本的错。

### 手工 Hint

手工 Hint 可以在满足 engine 隔离的前提下，强制 TiDB 对于某张或某几张表使用指定的副本，使用方法为：

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

如果在查询语句中对表设置了别名，在 Hint 语句中必须使用别名才能使 Hint 生效。比如：

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

其中 `tiflash[]` 是提示优化器读取 TiFlash 副本，亦可以根据需要使用 `tikv[]` 来提示优化器读取 TiKV 副本。更多关于该 Hint 语句的语法可以参考 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)。

如果 Hint 指定的表在指定的引擎上不存在副本，则 Hint 会被忽略，并产生 warning。另外 Hint 必须在满足 engine 隔离的前提下才会生效，如果 Hint 中指定的引擎不在 engine 隔离列表中，Hint 同样会被忽略，并产生 warning。

> **注意：**
>
> MySQL 命令行客户端在 5.7.7 版本之前默认清除了 Optimizer Hints。如果需要在这些早期版本的客户端中使用 `Hint` 语法，需要在启动客户端时加上 `--comments` 选项，例如 `mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

### 三种方式之间关系的总结

上述三种读取 TiFlash 副本的方式中，Engine 隔离规定了总的可使用副本 engine 的范围，手工 Hint 可以在该范围内进一步实现语句级别及表级别的细粒度的 engine 指定，最终由 CBO 在指定的 engine 范围内根据代价估算最终选取某个 engine 上的副本。

> **注意：**
>
> TiDB 4.0.3 版本之前，在非只读 SQL 语句中（比如 `INSERT INTO ... SELECT`、`SELECT ... FOR UPDATE`、`UPDATE ...`、`DELETE ...`）读取 TiFlash，行为是未定义。TiDB 4.0.3 以及后续的版本，TiDB 内部会对非只读 SQL 语句忽略 TiFlash 副本以保证数据写入、更新、删除的正确性。对应的，如果使用了[智能选择](#智能选择)的方式，TiDB 会自动选择非 TiFlash 副本；如果使用了 [Engine 隔离](#engine-隔离)的方式指定**仅**读取 TiFlash 副本，则查询会报错；而如果使用了[手工 Hint](#手工-hint) 的方式，则 Hint 会被忽略。

## 使用 TiSpark 读取 TiFlash

TiSpark 目前提供类似 TiDB 中 engine 隔离的方式读取 TiFlash，方式是通过配置参数 `spark.tispark.isolation_read_engines`。参数值默认为 `tikv,tiflash`，表示根据 CBO 自动选择从 TiFlash 或从 TiKV 读取数据。如果将该参数值设置成 `tiflash`，表示强制从 TiFlash 读取数据。

> **注意：**
>
> 设为 `true` 时，所有查询的表都会只读取 TiFlash 副本，设为 `false` 则只读取 TiKV 副本。设为 `true` 时，要求查询所用到的表都必须已创建了 TiFlash 副本，对于未创建 TiFlash 副本的表的查询会报错。

可以使用以下任意一种方式进行设置：

1. 在 `spark-defaults.conf` 文件中添加：

    ```
    spark.tispark.isolation_read_engines tiflash
    ```

2. 在启动 Spark shell 或 Thrift server 时，启动命令中添加 `--conf spark.tispark.isolation_read_engines=tiflash`

3. Spark shell 中实时设置：`spark.conf.set("spark.tispark.isolation_read_engines", "tiflash")`

4. Thrift server 通过 beeline 连接后实时设置：`set spark.tispark.isolation_read_engines=tiflash`

## TiFlash 支持的计算下推

> **注意：**
>
> TiDB 4.0.2 版本之前，TiFlash 不支持 TiDB 新排序规则框架，所以在 TiDB 开启[新框架下的排序规则支持](/character-set-and-collation.md#新框架下的排序规则支持)后不支持任何表达式的下推，TiDB 4.0.2 以及后续的版本取消了这个限制。

TiFlash 支持谓词、聚合下推计算以及表连接，下推的计算可以帮助 TiDB 进行分布式加速。暂不支持的计算类型是 `Full Outer Join` 和 `DISTINCT COUNT`，会在后续版本逐步优化。

目前下推连接 (`Join`) 的功能需要通过以下会话变量开启（暂不支持 `Full Outer Join`）：

```
set @@session.tidb_opt_broadcast_join=1
```

目前 TiFlash 支持了有限的常用表达式下推，支持下推的表达式包括：

```
+, -, /, *, >=, <=, =, !=, <, >, ifnull, isnull, bitor, in, bitand, or, and, like, not, case when, month, substr, timestampdiff, date_format, from_unixtime, json_length, if, bitneg, bitxor, 
round without fraction, cast(int as decimal), date_add(datetime, int), min, max, sum, count, avg, approx_count_distinct
```

目前 TiFlash 不支持下推的情况包括：

- 所有包含 Time 类型的表达式均不能下推
- 在聚合函数或者 WHERE 条件中包含了不在上述列表中的表达式，聚合或者相关的谓词过滤均不能下推

如查询遇到不支持的下推计算，则需要依赖 TiDB 完成剩余计算，可能会很大程度影响 TiFlash 加速效果。对于暂不支持的表达式，将会在后续陆续加入支持，也可以联系官方沟通。
