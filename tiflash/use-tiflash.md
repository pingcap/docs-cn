---
title: 使用 TiFlash
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

* v5.1 版本及后续版本将不再支持设置系统表的 replica。在集群升级前，需要清除相关系统表的 replica，否则升级到较高版本后将无法再修改系统表的 replica 设置。

### 查看表同步进度

可通过如下 SQL 语句查看特定表（通过 WHERE 语句指定，去掉 WHERE 语句则查看所有表）的 TiFlash 副本的状态：

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>'
```

查询结果中：

* AVAILABLE 字段表示该表的 TiFlash 副本是否可用。1 代表可用，0 代表不可用。副本状态为可用之后就不再改变，如果通过 DDL 命令修改副本数则会重新计算同步进度。
* PROGRESS 字段代表同步进度，在 0.0~1.0 之间，1 代表至少 1 个副本已经完成同步。

### 可用区设置

如果在配置副本时为了考虑容灾，需要将 TiFlash 的不同数据副本分布在多个数据中心，则可以按如下步骤进行配置：

1. 在集群配置文件中为 TiFlash 节点指定 label. 

    ```
    tiflash_servers:
      - host: 172.16.5.81
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.82
        config:
          flash.proxy.labels: zone=z1
      - host: 172.16.5.85
        config:
          flash.proxy.labels: zone=z2
    ```

2. 启动集群后，在创建副本时为副本调度指定 label，语法如下：

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels
    ```

    例如：

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3. 此时 pd 就会根据设置的 label 进行调度，将表 t 的两个副本分别调度到两个可用区中。我们可以通过监控或 pd-ctl 来验证这一点：

    ```sh
    > tiup ctl:<version> pd -u<pd-host>:<pd-port> store

        ...

        "address": "172.16.5.82:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 4,

        ...

        "address": "172.16.5.81:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 5,

        ...

        "address": "172.16.5.85:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z2" }
        ],
        "region_count": 9,

        ...
    ```

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

TiFlash 支持部分算子的下推，支持的算子如下：

* TableScan：该算子从表中读取数据
* Selection：该算子对数据进行过滤
* HashAgg：该算子基于 [Hash Aggregation](/explain-aggregation.md#hash-aggregation) 算法对数据进行聚合运算
* StreamAgg：该算子基于 [Stream Aggregation](/explain-aggregation.md#stream-aggregation) 算法对数据进行聚合运算。StreamAgg 仅支持不带 `GROUP BY` 条件的列。
* TopN：该算子对数据求 TopN 运算
* Limit：该算子对数据进行 limit 运算
* Project：该算子对数据进行投影运算
* HashJoin（带等值 Join 条件）：该算子基于 [Hash Join](/explain-joins.md#hash-join) 算法对数据进行连接运算，但有以下使用条件：
    * 只有在 [MPP 模式](#使用-mpp-模式)下才能被下推
    * 不支持下推 `Full Outer Join`
* HashJoin（不带等值 Join 条件，即 Cartesian Join）：该算子实现了 Cartesian Join，但有以下使用条件：
    * 只有在 [MPP 模式](#使用-mpp-模式)下才能被下推
    * 只有在 Broadcast Join 中才支持 Cartesian Join

在 TiDB 中，算子之间会呈现树型组织结构。一个算子能下推到 TiFlash 的前提条件，是该算子的所有子算子都能下推到 TiFlash。因为大部分算子都包含有表达式计算，当且仅当一个算子所包含的所有表达式均支持下推到 TiFlash 时，该算子才有可能下推给 TiFlash。目前 TiFlash 支持下推的表达式包括：

* 数学函数：`+, -, /, *, %, >=, <=, =, !=, <, >, round(int), round(double), round(decimal), abs, floor(int), ceil(int), ceiling(int), sqrt, log, log2, log10, ln, exp, pow, sign, radians, degrees, conv, crc32`
* 逻辑函数：`and, or, not, case when, if, ifnull, isnull, in, like, coalesce`
* 位运算：`bitand, bitor, bigneg, bitxor`
* 字符串函数：`substr, char_length, replace, concat, concat_ws, left, right, ascii, length, trim, position`
* 日期函数：`date_format, timestampdiff, from_unixtime, unix_timestamp(int), unix_timestamp(decimal), str_to_date(date), str_to_date(datetime), datediff, year, month, day, extract(datetime), date`
* JSON 函数：`json_length`
* 转换函数：`cast(int as double), cast(int as decimal), cast(int as string), cast(int as time), cast(double as int), cast(double as decimal), cast(double as string), cast(double as time), cast(string as int), cast(string as double), cast(string as decimal), cast(string as time), cast(decimal as int), cast(decimal as string), cast(decimal as time), cast(time as int), cast(time as decimal), cast(time as string)`
* 聚合函数：`min, max, sum, count, avg, approx_count_distinct`
* 其他函数：`inetntoa, inetaton, inet6ntoa, inet6aton`

另外，所有包含 Time/Bit/Set/Enum/Geometry 类型的表达式均不能下推到 TiFlash。

如查询遇到不支持的下推计算，则需要依赖 TiDB 完成剩余计算，可能会很大程度影响 TiFlash 加速效果。对于暂不支持的算子/表达式，将会在后续版本中陆续支持。

## 使用 MPP 模式

TiFlash 支持 MPP 模式的查询执行，即在计算中引入跨节点的数据交换（data shuffle 过程）。TiDB 默认由优化器自动选择是否使用 MPP 模式，你可以通过修改变量 [`tidb_allow_mpp`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入) 和 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 的值来更改选择策略。

### 控制是否选择 MPP 模式

变量 `tidb_allow_mpp` 控制 TiDB 能否选择 MPP 模式执行查询。变量 `tidb_enforce_mpp` 控制是否忽略优化器代价估算，强制使用 TiFlash 的 MPP 模式执行查询。

这两个变量所有取值对应的结果如下：

|                        | tidb_allow_mpp=off | tidb_allow_mpp=on（默认）              |
| ---------------------- | -------------------- | -------------------------------- |
| tidb_enforce_mpp=off（默认） | 不使用 MPP 模式。  | 优化器根据代价估算选择。（默认） |
| tidb_enforce_mpp=on  | 不使用 MPP 模式。  | TiDB 无视代价估算，选择 MPP 模式。      |

例如，如果你不想使用 MPP 模式，可以通过以下语句来设置：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=0;
```

如果想要通过优化器代价估算来智能选择是否使用 MPP（默认情况），可以通过如下语句来设置：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=0;
```

如果想要 TiDB 忽略优化器的代价估算，强制使用 MPP，可以通过如下语句来设置：

{{< copyable "sql" >}}

```sql
set @@session.tidb_allow_mpp=1;
set @@session.tidb_enforce_mpp=1;
```

Session 变量 `tidb_enforce_mpp` 的初始值等于这台 tidb-server 实例的 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置项值（默认为 `false`）。在一个 TiDB 集群中，如果有若干台 tidb-server 实例只执行分析型查询，要确保它们能够选中 MPP 模式，你可以将它们的 [`enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置值修改为 `true`.

> **注意：**
>
> `tidb_enforce_mpp=1` 在生效时，TiDB 优化器会忽略代价估算选择 MPP 模式。但如果存在其它不支持 MPP 的因素，例如没有 TiFlash 副本、TiFlash 副本同步未完成、语句中含有 MPP 模式不支持的算子或函数等，那么 TiDB 仍然不会选择 MPP 模式。
> 
> 如果由于代价估算之外的原因导致 TiDB 优化器无法选择 MPP，在你使用 `EXPLAIN` 语句查看执行计划时，会返回警告说明原因，例如：
> 
> {{< copyable "sql" >}}
> 
> ```sql
> set @@session.tidb_enforce_mpp=1;
> create table t(a int);
> explain select count(*) from t; 
> show warnings;
> ```
> 
> ```
> +---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
> +---------+------+-----------------------------------------------------------------------------+
> | Warning | 1105 | MPP mode may be blocked because there aren't tiflash replicas of table `t`. |
> +---------+------+-----------------------------------------------------------------------------+
> ```

### MPP 模式的算法支持

MPP 模式目前支持的物理算法有：Broadcast Hash Join、Shuffled Hash Join、 Shuffled Hash Aggregation、Union All、 TopN 和 Limit。算法的选择由优化器自动判断。通过 `EXPLAIN` 语句可以查看具体的查询执行计划。如果 `EXPLAIN` 语句的结果中出现 ExchangeSender 和 ExchangeReceiver 算子，表明 MPP 已生效。

以 TPC-H 测试集中的表结构为例：

```sql
mysql> explain select count(*) from customer c join nation n on c.c_nationkey=n.n_nationkey;
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| id                                       | estRows    | task              | access object | operator info                                                              |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
| HashAgg_23                               | 1.00       | root              |               | funcs:count(Column#16)->Column#15                                          |
| └─TableReader_25                         | 1.00       | root              |               | data:ExchangeSender_24                                                     |
|   └─ExchangeSender_24                    | 1.00       | batchCop[tiflash] |               | ExchangeType: PassThrough                                                  |
|     └─HashAgg_12                         | 1.00       | batchCop[tiflash] |               | funcs:count(1)->Column#16                                                  |
|       └─HashJoin_17                      | 3000000.00 | batchCop[tiflash] |               | inner join, equal:[eq(tpch.nation.n_nationkey, tpch.customer.c_nationkey)] |
|         ├─ExchangeReceiver_21(Build)     | 25.00      | batchCop[tiflash] |               |                                                                            |
|         │ └─ExchangeSender_20            | 25.00      | batchCop[tiflash] |               | ExchangeType: Broadcast                                                    |
|         │   └─TableFullScan_18           | 25.00      | batchCop[tiflash] | table:n       | keep order:false                                                           |
|         └─TableFullScan_22(Probe)        | 3000000.00 | batchCop[tiflash] | table:c       | keep order:false                                                           |
+------------------------------------------+------------+-------------------+---------------+----------------------------------------------------------------------------+
9 rows in set (0.00 sec)
```

在执行计划中，出现了 `ExchangeReceiver` 和 `ExchangeSender` 算子。该执行计划表示 `nation` 表读取完毕后，经过 `ExchangeSender` 算子广播到各个节点中，与 `customer` 表先后进行 `HashJoin` 和 `HashAgg` 操作，再将结果返回至 TiDB 中。

TiFlash 提供了两个全局/会话变量决定是否选择 Broadcast Hash Join，分别为：

- [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为 bytes。如果表大小（字节数）小于该值，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。
- [`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-从-v50-版本开始引入)，单位为行数。如果 join 的对象为子查询，优化器无法估计子查询结果集大小，在这种情况下通过结果集行数判断。如果子查询的行数估计值小于该变量，则选择 Broadcast Hash Join 算法。否则选择 Shuffled Hash Join 算法。

## 注意事项

TiFlash 目前尚不支持的一些功能，与原生 TiDB 可能存在不兼容的问题，具体如下：

* TiFlash 计算层：
    * 不支持检查溢出的数值。例如将两个 `BIGINT` 类型的最大值相加 `9223372036854775807 + 9223372036854775807`，该计算在 TiDB 中预期的行为是返回错误 `ERROR 1690 (22003): BIGINT value is out of range`，但如果该计算在 TiFlash 中进行，则会得到溢出的结果 `-2` 且无报错。
    * 不支持窗口函数。
    * 不支持从 TiKV 读取数据。
    * 目前 TiFlash 中的 `sum` 函数不支持传入字符串类型的参数，但 TiDB 在编译时无法检测出这种情况。所以当执行类似于 `select sum(string_col) from t` 的语句时，TiFlash 会报错 `[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`。要避免这类报错，需要手动把 SQL 改写成 `select sum(cast(string_col as double)) from t`。
    * TiFlash 目前的 Decimal 除法计算和 TiDB 存在不兼容的情况。例如在进行 Decimal 相除的时候，TiFlash 会始终按照编译时推断出来的类型进行计算，而 TiDB 则在计算过程中采用精度高于编译时推断出来的类型。这导致在一些带有 Decimal 除法的 SQL 语句在 TiDB + TiKV 上的执行结果会和 TiDB + TiFlash 上的执行结果不一样，示例如下：

        ```sql
        mysql> create table t (a decimal(3,0), b decimal(10, 0));
        Query OK, 0 rows affected (0.07 sec)

        mysql> insert into t values (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)

        mysql> alter table t set tiflash replica 1;
        Query OK, 0 rows affected (0.07 sec)

        mysql> set session tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)

        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)

        mysql> set session tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)

        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        Empty set (0.01 sec)
        ```

        以上示例中，在 TiDB 和 TiFlash 中，`a/b` 在编译期推导出来的类型都为 `Decimal(7,4)`，而在 `Decimal(7,4)` 的约束下，`a/b` 返回的结果应该为 `0.0000`。但是在 TiDB 中，`a/b` 运行期的精度比 `Decimal(7,4)` 高，所以原表中的数据没有被 `where a/b` 过滤掉。而在 TiFlash 中 `a/b` 在运行期也是采用 `Decimal(7,4)` 作为结果类型，所以原表中的数据被 `where a/b` 过滤掉了。
