## 一、SQL 操作常见问题

#### 1.1.1 TiDB 对哪些 MySQL variables 兼容？

详细可参考[系统变量](/system-variables.md)。

#### 1.1.2 TiDB 是否支持 select for update？

支持，但语义上和 MySQL 有区别，TiDB 是分布式数据库，3.0.8 版本前，采用的乐观锁机制，也就说 select for update 不在事务开启就锁住数据，而是其他事务在提交的时候进行冲突检查，如有冲突，会进行回滚。3.0.8 版本之后，默认采用悲观锁机制，行为和 MySQL 基本一致，SELECT FOR UPDATE 会读取已提交的最新数据，并对读取到的数据加悲观锁。



#### 1.1.3 TiDB 的 codec 能保证 UTF8 的字符串是 memcomparable 的吗？我们的 key 需要支持 UTF8，有什么编码建议吗？

TiDB 字符集默认就是 UTF8 而且目前只支持 UTF8，字符串就是 memcomparable 格式的。

#### 1.1.4 一个事务中的语句数量最大是多少？

一个事务中的语句数量，默认限制最大为 5000 条。

#### 1.1.5 TiDB 中，为什么出现后插入数据的自增 ID 反而小？

TiDB 的自增 ID (`AUTO_INCREMENT`) 只保证自增且唯一，并不保证连续分配。TiDB 目前采用批量分配的方式，所以如果在多台 TiDB 上同时插入数据，分配的自增 ID 会不连续。当多个线程并发往不同的 tidb-server 插入数据的时候，有可能会出现后插入的数据自增 ID 小的情况。此外，TiDB允许给整型类型的字段指定 AUTO_INCREMENT，且一个表只允许一个属性为 `AUTO_INCREMENT` 的字段。详情可参考[CREATE TABLE 语法](/mysql-compatibility.md#自增-id)。


#### 1.1.6 sql_mode 默认除了通过命令 set 修改，配置文件怎么修改？

TiDB 的 sql_mode 与 MySQL 的 sql_mode 设置方法有一些差别，TiDB 不支持配置文件配置设置数据库的 sql\_mode，而只能使用 set 命令去设置，具体方法为：`set @@global.sql_mode = 'STRICT_TRANS_TABLES';`。


#### 1.1.7 用 Sqoop 批量写入 TiDB 数据，虽然配置了 `--batch` 选项，但还是会遇到 `java.sql.BatchUpdateExecption:statement count 5001 exceeds the transaction limitation` 的错误，该如何解决？

- 在 Sqoop 中，`--batch` 是指每个批次提交 100 条 statement，但是默认每个 statement 包含 100 条 SQL 语句，所以此时 100 * 100 = 10000 条 SQL 语句，超出了 TiDB 的事务限制 5000 条，可以增加选项 `-Dsqoop.export.records.per.statement=10` 来解决这个问题，完整的用法如下：

    {{< copyable "shell-regular" >}}

    ```bash
    sqoop export \
        -Dsqoop.export.records.per.statement=10 \
        --connect jdbc:mysql://mysql.example.com/sqoop \
        --username sqoop ${user} \
        --password ${passwd} \
        --table ${tab_name} \
        --export-dir ${dir} \
        --batch
    ```

- 也可以选择增大 tidb 的单个事物语句数量限制，不过这个会导致内存上涨。

#### 1.1.8 TiDB 有像 Oracle 那样的 Flashback Query 功能么，DDL 支持么？

有，也支持 DDL。详细参考 [TiDB 历史数据回溯](/read-historical-data.md)。


#### 1.1.9 Transaction too large 是什么原因，怎么解决？

由于分布式事务要做两阶段提交，并且底层还需要做 Raft 复制，如果一个事务非常大，会使得提交过程非常慢，并且会卡住下面的 Raft 复制流程。为了避免系统出现被卡住的情况，我们对事务的大小做了限制：

- 单个事务包含的 SQL 语句不超过 5000 条（默认）
- 单条 KV entry 不超过 6MB
- KV entry 的总条数不超过 30w
- KV entry 的总大小不超过 100MB

在 Google 的 Cloud Spanner 上面，也有类似的[限制](https://cloud.google.com/spanner/docs/limits)。


#### 1.1.10 TiDB 中删除数据后会立即释放空间吗？

DELETE，TRUNCATE 和 DROP 都不会立即释放空间。对于 TRUNCATE 和 DROP 操作，在达到 TiDB 的 GC (garbage collection) 时间后（默认 10 分钟），TiDB 的 GC 机制会删除数据并释放空间。对于 DELETE 操作 TiDB 的 GC 机制会删除数据，但不会释放空间，而是当后续数据写入 RocksDB 且进行 compact 时对空间重新利用。


#### 1.1.11 TiDB 是否支持 replace into 语法？

支持，但是 load data 不支持 replace into 语法。


#### 1.1.12 数据删除后查询速度为何会变慢？

大量删除数据后，会有很多无用的 key 存在，影响查询效率。可以尝试开启 [Region Merge](https://pingcap.com/docs-cn/v3.0/best-practices/massive-regions-best-practices/#方法五开启-region-merge) 功能，具体看参考[最佳实践](https://pingcap.com/blog-cn/tidb-best-practice/)中的删除数据部分。


#### 1.1.13 对数据做删除操作之后，空间回收比较慢，如何处理？

可以设置并行 GC，加快对空间的回收速度。默认并发为 1，最大可调整为 tikv 实例数量的 50%。可使用 `update mysql.tidb set VARIABLE_VALUE="3" where VARIABLE_NAME="tikv_gc_concurrency";` 命令来调整。

#### 1.1.14 show processlist 是否显示系统进程号？

TiDB 的 `show processlist` 与 MySQL 的 `show processlist` 显示内容基本一样，不会显示系统进程号，而 ID 表示当前的 session ID。其中 TiDB 的 `show processlist` 和 MySQL 的 `show processlist` 区别如下：

1）由于 TiDB 是分布式数据库，tidb-server 实例是无状态的 SQL 解析和执行引擎（详情可参考 [TiDB 整体架构](/overview.md#tidb-整体架构)），用户使用 MySQL 客户端登录的是哪个 tidb-server，`show processlist` 就会显示当前连接的这个 tidb-server 中执行的 session 列表，不是整个集群中运行的全部 session 列表；而 MySQL 是单机数据库，`show processlist` 列出的是当前整个 MySQL 数据库的全部执行 SQL 列表。

2）TiDB 的 `show processlist` 显示内容比起 MySQL 来讲，多了一个当前 session 使用内存的估算值（单位 Byte）。
 
 
## 二、SQL 优化

### 2.1 TiDB 执行计划解读

详细解读 [理解 TiDB 执行计划](/query-execution-plan.md)。

#### 2.1.1 统计信息收集

详细解读 [统计信息](/statistics.md)。

#### 2.1.2 Count 如何加速？

Count 就是暴力扫表，提高并发度能显著的提升速度，修改并发度可以参考 `tidb_distsql_scan_concurrency` 变量，但是也要看 CPU 和 I/O 资源。TiDB 每次查询都要访问 TiKV，在数据量小的情况下，MySQL 都在内存里，TiDB 还需要进行一次网络访问。

提升建议：

- 建议提升硬件配置，可以参考[部署建议](/hardware-and-software-requirements.md)。
- 提升并发度，默认是 10，可以提升到 50 试试，但是一般提升在 2-4 倍之间。
- 测试大数据量的 count。
- 调优 TiKV 配置，可以参考[性能调优](/tune-tikv-performance.md)。

#### 2.1.3 查看当前 DDL 的进度？

通过 `admin show ddl` 查看当前 job 进度。操作如下：

{{< copyable "sql" >}}

```sql
admin show ddl;
```

```
*************************** 1. row ***************************
  SCHEMA_VER: 140
       OWNER: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
RUNNING_JOBS: ID:121, Type:add index, State:running, SchemaState:write reorganization, SchemaID:1, TableID:118, RowCount:77312, ArgLen:0, start time: 2018-12-05 16:26:10.652 +0800 CST, Err:<nil>, ErrCount:0, SnapshotVersion:404749908941733890
     SELF_ID: 1a1c4174-0fcd-4ba0-add9-12d08c4077dc
```

从上面操作结果可知，当前正在处理的是 `add index` 操作。且从 `RUNNING_JOBS` 列的 `RowCount` 字段可以知道当前 `add index` 操作已经添加了 77312 行索引。

#### 2.1.4 如何查看 DDL job？

可以使用 `admin show ddl` 语句查看正在运行的 DDL 作业。

- `admin show ddl jobs`：用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。
- `admin show ddl job queries 'job_id' [, 'job_id'] ...`：用于显示 `job_id` 对应的 DDL 任务的原始 SQL 语句。此 `job_id` 只搜索正在执行中的任务以及 DDL 历史作业队列中的最近十条结果。

#### 2.1.5 TiDB 是否支持基于 COST 的优化（CBO），如果支持，实现到什么程度？

是的，TiDB 使用的基于成本的优化器（CBO），我们有一个小组单独会对代价模型、统计信息持续优化，除此之外，我们支持 hash join、soft merge 等关联算法。

#### 2.1.6 如何确定某张表是否需要做 analyze ？

可以通过 `show stats_healthy` 来查看 Healthy 字段，一般小于等于 60 的表需要做 analyze。

#### 2.1.7 SQL 的执行计划展开成了树，ID 的序号有什么规律吗？这棵树的执行顺序会是怎么样的？

ID 没什么规律，只要是唯一就行，不过生成的时候，是有一个计数器，生成一个 plan 就加一，执行的顺序和序号无关，整个执行计划是一颗树，执行时从根节点开始，不断地向上返回数据。执行计划的理解，请参考[理解 TiDB 执行计划](/query-execution-plan.md)。

#### 2.1.8 TiDB 执行计划中，task cop 在一个 root 下，这个是并行的么？

目前 TiDB 的计算任务隶属于两种不同的 task：cop task 和 root task。cop task 是指被下推到 KV 端分布式执行的计算任务，root task 是指在 TiDB 端单点执行的计算任务。一般来讲 root task 的输入数据是来自于 cop task 的；但是 root task 在处理数据的时候，TiKV 上的 cop task 也可以同时处理数据，等待 TiDB 的 root task 拉取，所以从这个观点上来看，他们是并行的；但是存在数据上下游关系；在执行的过程中，某些时间段其实也是并行的，第一个 cop task 在处理 [100, 200] 的数据，第二个 cop task 在处理 [1, 100] 的数据。执行计划的理解，请参考[理解 TiDB 执行计划](/query-execution-plan.md)。 



## 三、数据库优化

### 3.1 TiDB

#### 3.1.1 TiDB 参数及调整

详情参考 [TiDB 配置参数](/command-line-flags-for-tidb-configuration.md)。

#### 3.1.2 如何打散热点

TiDB 中以 Region 分片来管理数据库，通常来讲，TiDB 的热点指的是 Region 的读写访问热点。而 TiDB 中对于 PK 非整数或没有 PK 的表，可以通过设置 `SHARD_ROW_ID_BITS` 来适度分解 Region 分片，以达到打散 Region 热点的效果。详情可参考官网 [TiDB 专用系统变量和语法](/tidb-specific-system-variables.md#shard_row_id_bits)中 `SHARD_ROW_ID_BITS` 的介绍。

### 3.2 TiKV

#### 3.2.1 TiKV 性能参数调优

详情参考 [TiKV 性能参数调优](/tune-tikv-performance.md)。
 
