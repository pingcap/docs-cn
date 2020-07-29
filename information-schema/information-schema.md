---
title: Information Schema
aliases: ['/docs-cn/dev/reference/system-databases/information-schema/','/docs-cn/dev/reference/system-databases/information-schema/','/docs-cn/dev/system-tables/system-table-information-schema/','/zh/tidb/dev/system-table-information-schema/']]
---

# Information Schema

Information Schema 提供了一种查看系统元数据的 ANSI 标准方法。除了包含与 MySQL 兼容的表外，TiDB 还提供了许多自定义的 `INFORMATION_SCHEMA` 表。

许多 `INFORMATION_SCHEMA` 表都有相应的 `SHOW` 命令。查询 `INFORMATION_SCHEMA` 的好处是可以在表之间进行 `join` 操作。

## 与 MySQL 兼容的表

| 表名                                                                                    | 描述                 |
|-----------------------------------------------------------------------------------------|-----------------------------|
| [`CHARACTER_SETS`](/information-schema/information-schema-character-sets.md)            | 提供 TiDB 支持的字符集列表。 |
| [`COLLATIONS`](/information-schema/information-schema-collations.md)                    | 提供 TiDB 支持的排序规则列表。 |
| [`COLLATION_CHARACTER_SET_APPLICABILITY`](/information-schema/information-schema-collation-character-set-applicability.md) | 说明哪些排序规则适用于哪些字符集。 |
| [`COLUMNS`](/information-schema/information-schema-columns.md)                          | 提供所有表中列的列表。 |
| `COLUMN_PRIVILEGES`                                                                     | TiDB 未实现，返回零行。 |
| `COLUMN_STATISTICS`                                                                     | TiDB 未实现，返回零行。 |
| [`ENGINES`](/information-schema/information-schema-engines.md)                          | 提供支持的存储引擎列表。 |
| `EVENTS`                                                                                | TiDB 未实现，返回零行。 |
| `FILES`                                                                                 | TiDB 未实现，返回零行。 |
| `GLOBAL_STATUS`                                                                         | TiDB 未实现，返回零行。 |
| `GLOBAL_VARIABLES`                                                                      | TiDB 未实现，返回零行。 |
| [`KEY_COLUMN_USAGE`](/information-schema/information-schema-key-column-usage.md)        | 描述列的键约束，例如主键约束。|
| `OPTIMIZER_TRACE`                                                                       | TiDB 未实现，返回零行。 |
| `PARAMETERS`                                                                            | TiDB 未实现，返回零行。 |
| [`PARTITIONS`](/information-schema/information-schema-partitions.md)                    | 提供表分区的列表。 |
| `PLUGINS`                                                                               | TiDB 未实现，返回零行。 |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md)                  | 提供与 `SHOW PROCESSLIST` 命令类似的信息。 |
| `PROFILING`                                                                             | TiDB 未实现，返回零行。 |
| `REFERENTIAL_CONSTRAINTS`                                                               | TiDB 未实现，返回零行。 |
| `ROUTINES`                                                                              | TiDB 未实现，返回零行。 |
| [`SCHEMATA`](/information-schema/information-schema-schemata.md)                        | 提供与 `SHOW DATABASES` 命令类似的信息。 |
| `SCHEMA_PRIVILEGES`                                                                     | TiDB 未实现，返回零行。 |
| `SESSION_STATUS`                                                                        | TiDB 未实现，返回零行。 |
| [`SESSION_VARIABLES`](/information-schema/information-schema-session-variables.md)      | 提供与 `SHOW SESSION VARIABLES` 命令类似的功能。|
| [`STATISTICS`](/information-schema/information-schema-statistics.md)                    | 提供有关表索引的信息。 |
| [`TABLES`](/information-schema/information-schema-tables.md)                            | 提供当前用户可见的表的列表。 类似于 `SHOW TABLES`。 |
| `TABLESPACES`                                                                           | TiDB 未实现，返回零行。 |
| [`TABLE_CONSTRAINTS`](/information-schema/information-schema-table-constraints.md)      | 提供有关主键、唯一索引和外键的信息。 |
| `TABLE_PRIVILEGES`                                                                      | TiDB 未实现，返回零行。 |
| `TRIGGERS`                                                                              | TiDB 未实现，返回零行。 |
| [`USER_PRIVILEGES`](/information-schema/information-schema-user-privileges.md)          | 汇总与当前用户相关的权限。 |
| [`VIEWS`](/information-schema/information-schema-views.md)                              | 提供当前用户可见的视图列表。类似于 `SHOW FULL TABLES WHERE table_type = 'VIEW'`。 |

## TiDB 中的扩展表

| 表名                                                                                    | 描述 |
|-----------------------------------------------------------------------------------------|-------------|
| [`ANALYZE_STATUS`](/information-schema/information-schema-analyze-status.md)            | 提供有关收集统计信息的任务的信息。 |
| [`CLUSTER_CONFIG`](/information-schema/information-schema-cluster-config.md)            | 提供有关整个 TiDB 集群的配置设置的详细信息。 |
| [`CLUSTER_HARDWARE`](/information-schema/information-schema-cluster-info.md)            | 提供在每个 TiDB 组件上发现的底层物理硬件的详细信息。 |
| [`CLUSTER_INFO`](/information-schema/information-schema-cluster-info.md)                | 提供当前集群拓扑的详细信息。 |
| [`CLUSTER_LOAD`](/information-schema/information-schema-cluster-load.md)                | 提供集群中 TiDB 服务器的当前负载信息。 |
| [`CLUSTER_LOG`](/information-schema/information-schema-cluster-log.md)                  | 提供整个 TiDB 集群的日志。 |
| `CLUSTER_PROCESSLIST`                                                                   | 提供 `PROCESSLIST` 表的集群级别的视图。 |
| `CLUSTER_SLOW_QUERY`                                                                    | 提供 `SLOW_QUERY` 表的集群级别的视图。 |
| `CLUSTER_STATEMENTS_SUMMARY`                                                            | 提供 `STATEMENTS_SUMMARY` 表的集群级别的视图。 |
| `CLUSTER_STATEMENTS_SUMMARY_HISTORY`                                                    | 提供 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 表的集群级别的视图。 |
| [`CLUSTER_SYSTEMINFO`](/information-schema/information-schema-cluster-systeminfo.md)    | 提供集群中服务器的内核参数配置的详细信息。 |
| [`DDL_JOBS`](/information-schema/information-schema-ddl-jobs.md)                        | 提供与 `ADMIN SHOW DDL JOBS` 类似的输出。 |
| [`INSPECTION_RESULT`](/information-schema/information-schema-inspection-result.md)      | 触发内部诊断检查。 |
| [`INSPECTION_RULES`](/information-schema/information-schema-inspection-rules.md)        | 进行的内部诊断检查的列表。 |
| [`INSPECTION_SUMMARY`](/information-schema/information-schema-inspection-summary.md)    | 重要监视指标的摘要报告。 |
| [`METRICS_SUMMARY`](/information-schema/information-schema-metrics-summary.md)          | 从 Prometheus 获取的指标的摘要。 |
| `METRICS_SUMMARY_BY_LABEL`                                                              | 参见 `METRICS_SUMMARY` 表。 |
| [`METRICS_TABLES`](/information-schema/information-schema-metrics-tables.md)            | 为 `METRICS_SCHEMA` 中的表提供 PromQL 定义。 |
| [`SEQUENCES`](/information-schema/information-schema-sequences.md)                      | 描述了基于 MariaDB 实现的 TiDB 序列。 |
| [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)                    | 提供当前 TiDB 服务器上慢查询的信息。 |
| [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)                                    | 类似于 MySQL 中的 performance_schema 语句摘要。 |
| [`STATEMENTS_SUMMARY_HISTORY`](/statement-summary-tables.md)                            | 类似于 MySQL 中的 performance_schema 语句摘要历史。 |
| [`TABLE_STORAGE_STATS`](/information-schema/information-schema-table-storage-stats.md)  | 提供存储的表的大小的详细信息。 |
| [`TIDB_HOT_REGIONS`](/information-schema/information-schema-tidb-hot-regions.md)        | 提供有关哪些 Region 访问次数最多的统计信息。|
| [`TIDB_INDEXES`](/information-schema/information-schema-tidb-indexes.md)                | 提供有关 TiDB 表的索引信息。 |
| [`TIDB_SERVERS_INFO`](/information-schema/information-schema-tidb-servers-info.md)      | 提供 TiDB 服务器的列表 |
| [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)          | 提供有关 TiFlash 副本的详细信息。 |
| [`TIKV_REGION_PEERS`](/information-schema/information-schema-tikv-region-peers.md)      | 提供 Region 存储位置的详细信息。 |
| [`TIKV_REGION_STATUS`](/information-schema/information-schema-tikv-region-status.md)    | 提供 Region 的统计信息。 |
| [`TIKV_STORE_STATUS`](/information-schema/information-schema-tikv-store-status.md)      | 提供 TiKV 服务器的基本信息。 |

## TABLE_CONSTRAINTS 表

`TABLE_CONSTRAINTS` 表记录了表的约束信息。

{{< copyable "sql" >}}

```sql
SELECT * FROM table_constraints WHERE constraint_type='UNIQUE';
```

```
*************************** 1. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: name
      TABLE_SCHEMA: mysql
        TABLE_NAME: help_topic
   CONSTRAINT_TYPE: UNIQUE
*************************** 2. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: tbl
      TABLE_SCHEMA: mysql
        TABLE_NAME: stats_meta
   CONSTRAINT_TYPE: UNIQUE
*************************** 3. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: tbl
      TABLE_SCHEMA: mysql
        TABLE_NAME: stats_histograms
   CONSTRAINT_TYPE: UNIQUE
*************************** 4. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: tbl
      TABLE_SCHEMA: mysql
        TABLE_NAME: stats_buckets
   CONSTRAINT_TYPE: UNIQUE
*************************** 5. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: delete_range_index
      TABLE_SCHEMA: mysql
        TABLE_NAME: gc_delete_range
   CONSTRAINT_TYPE: UNIQUE
*************************** 6. row ***************************
CONSTRAINT_CATALOG: def
 CONSTRAINT_SCHEMA: mysql
   CONSTRAINT_NAME: delete_range_done_index
      TABLE_SCHEMA: mysql
        TABLE_NAME: gc_delete_range_done
   CONSTRAINT_TYPE: UNIQUE
```

其中：

* `CONSTRAINT_TYPE` 的取值可以是 `UNIQUE`，`PRIMARY KEY`，或者 `FOREIGN KEY`。
* `UNIQUE` 和 `PRIMARY KEY` 信息与 `SHOW INDEX` 语句的执行结果类似。

## TIDB_HOT_REGIONS 表

`TIDB_HOT_REGIONS` 表提供了关于热点 REGION 的相关信息。

{{< copyable "sql" >}}

```sql
desc TIDB_HOT_REGIONS;
```

```sql
+----------------+---------------------+------+-----+---------+-------+
| Field          | Type                | Null | Key | Default | Extra |
+----------------+---------------------+------+-----+---------+-------+
| TABLE_ID       | bigint(21) unsigned | YES  |     | <null>  |       |
| INDEX_ID       | bigint(21) unsigned | YES  |     | <null>  |       |
| DB_NAME        | varchar(64)         | YES  |     | <null>  |       |
| TABLE_NAME     | varchar(64)         | YES  |     | <null>  |       |
| INDEX_NAME     | varchar(64)         | YES  |     | <null>  |       |
| TYPE           | varchar(64)         | YES  |     | <null>  |       |
| MAX_HOT_DEGREE | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_COUNT   | bigint(21) unsigned | YES  |     | <null>  |       |
| FLOW_BYTES     | bigint(21) unsigned | YES  |     | <null>  |       |
+----------------+---------------------+------+-----+---------+-------+
```

`TIDB_HOT_REGIONS` 表各列字段含义如下：

* TABLE_ID：热点 region 所在表的 ID。
* INDEX_ID：热点 region 所在索引的 ID。
* DB_NAME：热点 region 所在数据库对象的数据库名。
* TABLE_NAME：热点 region 所在表的名称。
* INDEX_NAME：热点 region 所在索引的名称。
* REGION_ID：热点 region 的 ID。
* TYPE：热点 region 的类型。
* MAX_HOT_DEGREE：该 region 的最大热度。
* REGION_COUNT：所在 instance 的 region 数量。
* FLOW_BYTES：该 region 内读写的字节数量。

## TIDB_INDEXES 表

`TIDB_INDEXES` 记录了所有表中的 INDEX 信息。

{{< copyable "sql" >}}

```sql
desc TIDB_INDEXES;
```

```sql
+---------------+---------------------+------+-----+---------+-------+
| Field         | Type                | Null | Key | Default | Extra |
+---------------+---------------------+------+-----+---------+-------+
| TABLE_SCHEMA  | varchar(64)         | YES  |     | <null>  |       |
| TABLE_NAME    | varchar(64)         | YES  |     | <null>  |       |
| NON_UNIQUE    | bigint(21) unsigned | YES  |     | <null>  |       |
| KEY_NAME      | varchar(64)         | YES  |     | <null>  |       |
| SEQ_IN_INDEX  | bigint(21) unsigned | YES  |     | <null>  |       |
| COLUMN_NAME   | varchar(64)         | YES  |     | <null>  |       |
| SUB_PART      | bigint(21) unsigned | YES  |     | <null>  |       |
| INDEX_COMMENT | varchar(2048)       | YES  |     | <null>  |       |
| INDEX_ID      | bigint(21) unsigned | YES  |     | <null>  |       |
+---------------+---------------------+------+-----+---------+-------+
```

`TIDB_INDEXES` 表中列的含义如下：

* `TABLE_SCHEMA`：索引所在表的所属数据库的名称。
* `TABLE_NAME`：索引所在表的名称。
* `NON_UNIQUE`：如果索引是唯一的，则为 `0`，否则为 `1`。
* `KEY_NAME`：索引的名称。如果索引是主键，则名称为 `PRIMARY`。
* `SEQ_IN_INDEX`：索引中列的顺序编号，从 `1` 开始。
* `COLUMN_NAME`：索引所在的列名。
* `SUB_PART`：索引前缀长度。如果列是部分被索引，则该值为被索引的字符数量，否则为 `NULL`。
* `INDEX_COMMENT`：创建索引时以 `COMMENT` 标注的注释。
* `INDEX_ID`：索引的 ID。

## TIKV_REGION_PEERS 表

`TIKV_REGION_PEERS` 表提供了所有 REGION 的 peer 信息。

{{< copyable "sql" >}}

```sql
desc TIKV_REGION_PEERS;
```

```sql
+--------------+---------------------+------+-----+---------+-------+
| Field        | Type                | Null | Key | Default | Extra |
+--------------+---------------------+------+-----+---------+-------+
| REGION_ID    | bigint(21) unsigned | YES  |     | <null>  |       |
| PEER_ID      | bigint(21) unsigned | YES  |     | <null>  |       |
| STORE_ID     | bigint(21) unsigned | YES  |     | <null>  |       |
| IS_LEARNER   | tinyint(1) unsigned | YES  |     | <null>  |       |
| IS_LEADER    | tinyint(1) unsigned | YES  |     | <null>  |       |
| STATUS       | varchar(10)         | YES  |     | <null>  |       |
| DOWN_SECONDS | bigint(21) unsigned | YES  |     | <null>  |       |
+--------------+---------------------+------+-----+---------+-------+
```

`TIKV_REGION_PEERS` 表各列含义如下：

* REGION_ID：REGION 的 ID。
* PEER_ID：REGION 中对应的副本 PEER 的 ID。
* STORE_ID：REGION 所在 TiKV Store 的 ID。
* IS_LEARNER：PEER 是否是 LEARNER。
* IS_LEADER：PEER 是否是 LEADER。
* STATUS：PEER 的状态，一共有 3 种状态：
    * PENDING：暂时不可用状态。
    * DOWN：下线转态，该 PEER 不再提供服务。
    * NORMAL: 正常状态。
* DOWN_SECONDS：处于下线状态的时间，单位是秒。

## TIKV_REGION_STATUS 表

`TIKV_REGION_STATUS` 表提供了所有 REGION 的状态信息。

{{< copyable "sql" >}}

```sql
desc TIKV_REGION_STATUS;
```

```sql
+---------------------------+-------------+------+------+---------+-------+
| Field                     | Type        | Null | Key  | Default | Extra |
+---------------------------+-------------+------+------+---------+-------+
| REGION_ID                 | bigint(21)  | YES  |      | NULL    |       |
| START_KEY                 | text        | YES  |      | NULL    |       |
| END_KEY                   | text        | YES  |      | NULL    |       |
| TABLE_ID                  | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME                   | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME                | varchar(64) | YES  |      | NULL    |       |
| IS_INDEX                  | tinyint(1)  | NO   |      | 0       |       |
| INDEX_ID                  | bigint(21)  | YES  |      | NULL    |       |
| INDEX_NAME                | varchar(64) | YES  |      | NULL    |       |
| EPOCH_CONF_VER            | bigint(21)  | YES  |      | NULL    |       |
| EPOCH_VERSION             | bigint(21)  | YES  |      | NULL    |       |
| WRITTEN_BYTES             | bigint(21)  | YES  |      | NULL    |       |
| READ_BYTES                | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_SIZE          | bigint(21)  | YES  |      | NULL    |       |
| APPROXIMATE_KEYS          | bigint(21)  | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATE   | varchar(64) | YES  |      | NULL    |       |
| REPLICATIONSTATUS_STATEID | bigint(21)  | YES  |      | NULL    |       |
+---------------------------+-------------+------+------+---------+-------+
```

`TIKV_REGION_STATUS` 表中列的含义如下：

* `REGION_ID`：Region 的 ID。
* `START_KEY`：Region 的起始 key 的值。
* `END_KEY`：Region 的末尾 key 的值。
* `TABLE_ID`：Region 所属的表的 ID。
* `DB_NAME`：`TABLE_ID` 所属的数据库的名称。
* `TABLE_NAME`：Region 所属的表的名称。
* `IS_INDEX`：Region 数据是否是索引，0 代表不是索引，1 代表是索引。如果当前 Region 同时包含表数据和索引数据，会有多行记录，`IS_INDEX` 分别是 0 和 1。
* `INDEX_ID`：Region 所属的索引的 ID。如果 `IS_INDEX` 为 0，这一列的值就为 NULL。
* `INDEX_NAME`：Region 所属的索引的名称。如果 `IS_INDEX` 为 0，这一列的值就为 NULL。
* `EPOCH_CONF_VER`：Region 的配置的版本号，在增加或减少 peer 时版本号会递增。
* `EPOCH_VERSION`：Region 的当前版本号，在分裂或合并时版本号会递增。
* `WRITTEN_BYTES`：已经往 Region 写入的数据量 (bytes)。
* `READ_BYTES`：已经从 Region 读取的数据量 (bytes)。
* `APPROXIMATE_SIZE`：Region 的近似数据量 (MB)。
* `APPROXIMATE_KEYS`：Region 中 key 的近似数量。
* `REPLICATIONSTATUS_STATE`：Region 当前的同步状态，可能为 `UNKNOWN` / `SIMPLE_MAJORITY` / `INTEGRITY_OVER_LABEL` 其中一种状态。
* `REPLICATIONSTATUS_STATEID`：`REPLICATIONSTATUS_STATE` 对应的标识符。

## TIKV_STORE_STATUS 表

`TIKV_STORE_STATUS` 表提供了所有 TiKV Store 的状态信息。

{{< copyable "sql" >}}

```sql
desc TIKV_STORE_STATUS;
```

```sql
+-------------------+---------------------+------+-----+---------+-------+
| Field             | Type                | Null | Key | Default | Extra |
+-------------------+---------------------+------+-----+---------+-------+
| STORE_ID          | bigint(21) unsigned | YES  |     | <null>  |       |
| ADDRESS           | varchar(64)         | YES  |     | <null>  |       |
| STORE_STATE       | bigint(21) unsigned | YES  |     | <null>  |       |
| STORE_STATE_NAME  | varchar(64)         | YES  |     | <null>  |       |
| LABEL             | json unsigned       | YES  |     | <null>  |       |
| VERSION           | varchar(64)         | YES  |     | <null>  |       |
| CAPACITY          | varchar(64)         | YES  |     | <null>  |       |
| AVAILABLE         | varchar(64)         | YES  |     | <null>  |       |
| LEADER_COUNT      | bigint(21) unsigned | YES  |     | <null>  |       |
| LEADER_WEIGHT     | bigint(21) unsigned | YES  |     | <null>  |       |
| LEADER_SCORE      | bigint(21) unsigned | YES  |     | <null>  |       |
| LEADER_SIZE       | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_COUNT      | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_WEIGHT     | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_SCORE      | bigint(21) unsigned | YES  |     | <null>  |       |
| REGION_SIZE       | bigint(21) unsigned | YES  |     | <null>  |       |
| START_TS          | datetime unsigned   | YES  |     | <null>  |       |
| LAST_HEARTBEAT_TS | datetime unsigned   | YES  |     | <null>  |       |
| UPTIME            | varchar(64)         | YES  |     | <null>  |       |
+-------------------+---------------------+------+-----+---------+-------+
```

`TIKV_STORE_STATUS` 表中列的含义如下：

* `STORE_ID`：Store 的 ID。
* `ADDRESS`：Store 的地址。
* `STORE_STATE`：Store 状态的标识符，与 `STORE_STATE_NAME` 相对应。
* `STORE_STATE_NAME`：Store 状态的名字，为 `Up` / `Offline` / `Tombstone` 中的一种。
* `LABEL`：给 Store 设置的标签。
* `VERSION`：Store 的版本号。
* `CAPACITY`：Store 的存储容量。
* `AVAILABLE`：Store 的剩余存储空间。
* `LEADER_COUNT`：Store 上的 leader 的数量。
* `LEADER_WEIGHT`：Store 的 leader 权重。
* `LEADER_SCORE`：Store 的 leader 评分。
* `LEADER_SIZE`：Store 上的所有 leader 的近似总数据量 (MB)。
* `REGION_COUNT`：Store 上的 Region 总数。
* `REGION_WEIGHT`：Store 的 Region 权重。
* `REGION_SCORE`：Store 的 Region 评分。
* `REGION_SIZE`：Store 上的所有 Region 的近似总数据量 (MB)。
* `START_TS`：Store 启动时的时间戳。
* `LAST_HEARTBEAT_TS`：Store 上次发出心跳的时间戳。
* `UPTIME`：Store 启动以来的总时间。

## USER_PRIVILEGES 表

`USER_PRIVILEGES` 表提供了关于全局权限的信息。该表的数据根据 `mysql.user` 系统表生成。

{{< copyable "sql" >}}

```sql
desc USER_PRIVILEGES;
```

```sql
+----------------|--------------|------|------|---------|-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------|--------------|------|------|---------|-------+
| GRANTEE        | varchar(81)  | YES  |      | NULL    |       |
| TABLE_CATALOG  | varchar(512) | YES  |      | NULL    |       |
| PRIVILEGE_TYPE | varchar(64)  | YES  |      | NULL    |       |
| IS_GRANTABLE   | varchar(3)   | YES  |      | NULL    |       |
+----------------|--------------|------|------|---------|-------+
4 rows in set (0.00 sec)
```

`USER_PRIVILEGES` 表中列的含义如下：

* `GRANTEE`：被授权的用户名称，格式为 `'user_name'@'host_name'`。
* `TABLE_CATALOG`：表所属的目录的名称。该值始终为 `def`。
* `PRIVILEGE_TYPE`：被授权的权限类型，每行只列一个权限。
* `IS_GRANTABLE`：如果用户有 `GRANT OPTION` 的权限，则为 `YES`，否则为 `NO`。

## VIEWS 表

`VIEWS` 表提供了关于 SQL 视图的信息。

{{< copyable "sql" >}}

```sql
create view test.v1 as select 1;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
select * from views;
```

```
*************************** 1. row ***************************
       TABLE_CATALOG: def
        TABLE_SCHEMA: test
          TABLE_NAME: v1
     VIEW_DEFINITION: select 1
        CHECK_OPTION: CASCADED
        IS_UPDATABLE: NO
             DEFINER: root@127.0.0.1
       SECURITY_TYPE: DEFINER
CHARACTER_SET_CLIENT: utf8
COLLATION_CONNECTION: utf8_general_ci
1 row in set (0.00 sec)
```

`VIEWS` 表中列的含义如下：

* `TABLE_CATALOG`：视图所属的目录的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：视图所属的数据库的名称。
* `TABLE_NAME`：视图名称。
* `VIEW_DEFINITION`：视图的定义，由创建视图时 `SELECT` 部分的语句组成。
* `CHECK_OPTION`：`CHECK_OPTION` 的值。取值为 `NONE`、 `CASCADE` 或 `LOCAL`。
* `IS_UPDATABLE`：`UPDATE`/`INSERT`/`DELETE` 是否对该视图可用。在 TiDB，始终为 `NO`。 
* `DEFINER`：视图的创建者用户名称，格式为 `'user_name'@'host_name'`。
* `SECURITY_TYPE`：`SQL SECURITY` 的值，取值为 `DEFINER` 或 `INVOKER`。
* `CHARACTER_SET_CLIENT`：在视图创建时 session 变量 `character_set_client` 的值。
* `COLLATION_CONNECTION`：在视图创建时 session 变量 `collation_connection` 的值。

## SQL 诊断相关的表

* [`information_schema.cluster_info`](/system-tables/system-table-cluster-info.md)
* [`information_schema.cluster_config`](/system-tables/system-table-cluster-config.md)
* [`information_schema.cluster_hardware`](/system-tables/system-table-cluster-hardware.md)
* [`information_schema.cluster_load`](/system-tables/system-table-cluster-load.md)
* [`information_schema.cluster_systeminfo`](/system-tables/system-table-cluster-systeminfo.md)
* [`information_schema.cluster_log`](/system-tables/system-table-cluster-log.md)
* [`information_schema.metrics_tables`](/system-tables/system-table-metrics-tables.md)
* [`information_schema.metrics_summary`](/system-tables/system-table-metrics-summary.md)
* [`information_schema.metrics_summary_by_label`](/system-tables/system-table-metrics-summary.md)
* [`information_schema.inspection_result`](/system-tables/system-table-inspection-result.md)
* [`information_schema.inspection_summary`](/system-tables/system-table-inspection-summary.md)

## 不支持的 Information Schema 表

TiDB 包含以下 `INFORMATION_SCHEMA` 表，但仅会返回空行：

* `COLUMN_PRIVILEGES`
* `EVENTS`
* `FILES`
* `GLOBAL_STATUS`
* `GLOBAL_VARIABLES`
* `OPTIMIZER_TRACE`
* `PARAMETERS`
* `PARTITIONS`
* `PLUGINS`
* `PROFILING`
* `REFERENTIAL_CONSTRAINTS`
* `ROUTINES`
* `SCHEMA_PRIVILEGES`
* `SESSION_STATUS`
* `TABLESPACES`
* `TABLE_PRIVILEGES`
* `TRIGGERS`
