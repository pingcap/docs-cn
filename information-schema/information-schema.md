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



## COLLATIONS 表

`COLLATIONS` 表提供了 `CHARACTER_SETS` 表中字符集对应的排序规则列表。TiDB 当前仅支持二进制排序规则，包含该表仅为兼容 MySQL。

{{< copyable "sql" >}}

```sql
SELECT * FROM collations WHERE character_set_name='utf8mb4';
```

```sql
+------------------------+--------------------+------+------------+-------------+---------+
| COLLATION_NAME         | CHARACTER_SET_NAME | ID   | IS_DEFAULT | IS_COMPILED | SORTLEN |
+------------------------+--------------------+------+------------+-------------+---------+
| utf8mb4_general_ci     | utf8mb4            |   45 | Yes        | Yes         |       1 |
| utf8mb4_bin            | utf8mb4            |   46 |            | Yes         |       1 |
| utf8mb4_unicode_ci     | utf8mb4            |  224 |            | Yes         |       1 |
| utf8mb4_icelandic_ci   | utf8mb4            |  225 |            | Yes         |       1 |
| utf8mb4_latvian_ci     | utf8mb4            |  226 |            | Yes         |       1 |
| utf8mb4_romanian_ci    | utf8mb4            |  227 |            | Yes         |       1 |
| utf8mb4_slovenian_ci   | utf8mb4            |  228 |            | Yes         |       1 |
| utf8mb4_polish_ci      | utf8mb4            |  229 |            | Yes         |       1 |
| utf8mb4_estonian_ci    | utf8mb4            |  230 |            | Yes         |       1 |
| utf8mb4_spanish_ci     | utf8mb4            |  231 |            | Yes         |       1 |
| utf8mb4_swedish_ci     | utf8mb4            |  232 |            | Yes         |       1 |
| utf8mb4_turkish_ci     | utf8mb4            |  233 |            | Yes         |       1 |
| utf8mb4_czech_ci       | utf8mb4            |  234 |            | Yes         |       1 |
| utf8mb4_danish_ci      | utf8mb4            |  235 |            | Yes         |       1 |
| utf8mb4_lithuanian_ci  | utf8mb4            |  236 |            | Yes         |       1 |
| utf8mb4_slovak_ci      | utf8mb4            |  237 |            | Yes         |       1 |
| utf8mb4_spanish2_ci    | utf8mb4            |  238 |            | Yes         |       1 |
| utf8mb4_roman_ci       | utf8mb4            |  239 |            | Yes         |       1 |
| utf8mb4_persian_ci     | utf8mb4            |  240 |            | Yes         |       1 |
| utf8mb4_esperanto_ci   | utf8mb4            |  241 |            | Yes         |       1 |
| utf8mb4_hungarian_ci   | utf8mb4            |  242 |            | Yes         |       1 |
| utf8mb4_sinhala_ci     | utf8mb4            |  243 |            | Yes         |       1 |
| utf8mb4_german2_ci     | utf8mb4            |  244 |            | Yes         |       1 |
| utf8mb4_croatian_ci    | utf8mb4            |  245 |            | Yes         |       1 |
| utf8mb4_unicode_520_ci | utf8mb4            |  246 |            | Yes         |       1 |
| utf8mb4_vietnamese_ci  | utf8mb4            |  247 |            | Yes         |       1 |
+------------------------+--------------------+------+------------+-------------+---------+
26 rows in set (0.00 sec)
```

`COLLATION` 表中列的含义如下：

* `COLLATION_NAME`：排序规则名称
* `CHARACTER_SET_NAME`：排序规则所属的字符集名称
* `ID`：排序规则的 ID
* `IS_DEFAULT`：该排序规则是否是所属字符集的默认排序规则
* `IS_COMPILED`：字符集是否编译到服务器中
* `SORTLEN`：排序规则在对字符进行排序时，所分配内存的最小长度

## COLLATION_CHARACTER_SET_APPLICABILITY 表

`COLLATION_CHARACTER_SET_APPLICABILITY` 表将排序规则映射至适用的字符集名称。和 `COLLATIONS` 表一样，包含此表也是为了兼容 MySQL。

{{< copyable "sql" >}}

```sql
SELECT * FROM collation_character_set_applicability WHERE character_set_name='utf8mb4';
```

```sql
+----------------+--------------------+
| COLLATION_NAME | CHARACTER_SET_NAME |
+----------------+--------------------+
| utf8mb4_bin    | utf8mb4            |
+----------------+--------------------+
```

`COLLATION_CHARACTER_SET_APPLICABILITY` 表中列的含义如下：

* `COLLATION_NAME`：排序规则名称
* `CHARACTER_SET_NAME`：排序规则所属的字符集名称

## COLUMNS 表

`COLUMNS` 表提供了表的所有列的信息。

{{< copyable "sql" >}}

```sql
CREATE TABLE test.t1 (a int);
```

```
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.columns WHERE table_schema='test' AND TABLE_NAME='t1';
```

```
*************************** 1. row ***************************
           TABLE_CATALOG: def
            TABLE_SCHEMA: test
              TABLE_NAME: t1
             COLUMN_NAME: a
        ORDINAL_POSITION: 1
          COLUMN_DEFAULT: NULL
             IS_NULLABLE: YES
               DATA_TYPE: int
CHARACTER_MAXIMUM_LENGTH: NULL
  CHARACTER_OCTET_LENGTH: NULL
       NUMERIC_PRECISION: 11
           NUMERIC_SCALE: 0
      DATETIME_PRECISION: NULL
      CHARACTER_SET_NAME: NULL
          COLLATION_NAME: NULL
             COLUMN_TYPE: int(11)
              COLUMN_KEY:
                   EXTRA:
              PRIVILEGES: select,insert,update,references
          COLUMN_COMMENT:
   GENERATION_EXPRESSION:
1 row in set (0.01 sec)
```

`COLUMNS` 表中列的含义如下：

* `TABLE_CATALOG`：包含列的表所属的目录的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：包含列的表所属的数据库的名称。
* `TABLE_NAME`：包含列的表的名称。
* `COLUMN_NAME`：列的名称。
* `ORDINAL_POSITION`：表中列的位置。
* `COLUMN_DEFAULT`：列的默认值。如果列的显式默认值为 `NULL`，或者列定义中不包含 `default` 子句，则此值为 `NULL`。
* `IS_NULLABLE`：列的可空性。如果列中可以存储空值，则该值为 `YES`，则为 `NO`。
* `DATA_TYPE`：列数据类型。
* `CHARACTER_MAXIMUM_LENGTH`：对于字符串列，以字符为单位的最大长度。
* `CHARACTER_OCTET_LENGTH`：对于字符串列，以字节为单位的最大长度。
* `NUMERIC_PRECISION`：对于数字列，为数字精度。
* `NUMERIC_SCALE`：对于数字列，为数字刻度。
* `DATETIME_PRECISION`：对于时间列，小数秒精度。
* `CHARACTER_SET_NAME`：对于字符串列，字符集名称。
* `COLLATION_NAME`：对于字符串列，排序规则名称。
* `COLUMN_TYPE`：列类型。
* `COLUMN_KEY`：该列是否被索引。具体显示如下:
    * 如果此值为空，则该列要么未被索引，要么被索引且是多列非唯一索引中的第二列。
    * 如果此值是`PRI`，则该列是主键，或者是多列主键中的一列。
    * 如果此值是`UNI`，则该列是唯一索引的第一列。
    * 如果此值是`MUL`，则该列是非唯一索引的第一列，在该列中允许给定值的多次出现。
* `EXTRA`：关于给定列的任何附加信息。
* `PRIVILEGES`：当前用户对该列拥有的权限。目前在 TiDB 中，此值为定值，一直为 `select,insert,update,references`。
* `COLUMN_COMMENT`：列定义中包含的注释。
* `GENERATION_EXPRESSION`：对于生成的列，显示用于计算列值的表达式。对于未生成的列为空。

对应的 `SHOW` 语句如下：

{{< copyable "sql" >}}

```sql
SHOW COLUMNS FROM t1 FROM test;
```

```sql
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```

## ENGINES 表

`ENGINES` 表提供了关于存储引擎的信息。从和 MySQL 兼容性上考虑，TiDB 会一直将 InnoDB 描述为唯一支持的引擎。此外，`ENGINES` 表中其它列值也都是定值。

{{< copyable "sql" >}}

```sql
SELECT * FROM engines;
```

```
*************************** 1. row ***************************
      ENGINE: InnoDB
     SUPPORT: DEFAULT
     COMMENT: Supports transactions, row-level locking, and foreign keys
TRANSACTIONS: YES
          XA: YES
  SAVEPOINTS: YES
1 row in set (0.00 sec)
```

`ENGINES` 表中列的含义如下：

* `ENGINE`：存储引擎的名称。
* `SUPPORT`：服务器对存储引擎的支持级别，在 TiDB 中此值一直是 `DEFAULT`。
* `COMMENT`：存储引擎的简要描述。
* `TRANSACTIONS`：存储引擎是否支持事务。
* `XA`：存储引擎是否支持 XA 事务。
* `SAVEPOINTS`：存储引擎是否支持 `savepoints`。

## KEY_COLUMN_USAGE 表

`KEY_COLUMN_USAGE` 表描述了列的键约束，比如主键约束。

{{< copyable "sql" >}}

```sql
SELECT * FROM key_column_usage WHERE table_schema='mysql' and table_name='user';
```

```
*************************** 1. row ***************************
           CONSTRAINT_CATALOG: def
            CONSTRAINT_SCHEMA: mysql
              CONSTRAINT_NAME: PRIMARY
                TABLE_CATALOG: def
                 TABLE_SCHEMA: mysql
                   TABLE_NAME: user
                  COLUMN_NAME: Host
             ORDINAL_POSITION: 1
POSITION_IN_UNIQUE_CONSTRAINT: NULL
      REFERENCED_TABLE_SCHEMA: NULL
        REFERENCED_TABLE_NAME: NULL
       REFERENCED_COLUMN_NAME: NULL
*************************** 2. row ***************************
           CONSTRAINT_CATALOG: def
            CONSTRAINT_SCHEMA: mysql
              CONSTRAINT_NAME: PRIMARY
                TABLE_CATALOG: def
                 TABLE_SCHEMA: mysql
                   TABLE_NAME: user
                  COLUMN_NAME: User
             ORDINAL_POSITION: 2
POSITION_IN_UNIQUE_CONSTRAINT: NULL
      REFERENCED_TABLE_SCHEMA: NULL
        REFERENCED_TABLE_NAME: NULL
       REFERENCED_COLUMN_NAME: NULL
2 rows in set (0.00 sec)
```

`KEY_COLUMN_USAGE` 表中列的含义如下：

* `CONSTRAINT_CATALOG`：约束所属的目录的名称。该值始终为 `def`。
* `CONSTRAINT_SCHEMA`：约束所属的数据库的名称。
* `CONSTRAINT_NAME`：约束名称。
* `TABLE_CATALOG`：表所属目录的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：表所属的架构数据库的名称。
* `TABLE_NAME`：具有约束的表的名称。
* `COLUMN_NAME`：具有约束的列的名称。
* `ORDINAL_POSITION`：列在约束中的位置，而不是列在表中的位置。列位置从 1 开始编号。
* `POSITION_IN_UNIQUE_CONSTRAINT`：唯一约束和主键约束为空。对于外键约束，此列是被引用的表的键的序号位置。
* `REFERENCED_TABLE_SCHEMA`：约束引用的数据库的名称。目前在 TiDB 中，除了外键约束，其它约束此列的值都为 `nil`。
* `REFERENCED_TABLE_NAME`：约束引用的表的名称。目前在 TiDB 中，除了外键约束，其它约束此列的值都为 `nil`。
* `REFERENCED_COLUMN_NAME`：约束引用的列的名称。目前在 TiDB 中，除了外键约束，其它约束此列的值都为 `nil`。

## PROCESSLIST 表

`PROCESSLIST` 和 `show processlist` 的功能一样，都是查看当前正在处理的请求。

`PROCESSLIST` 表会比 `show processlist` 多一个 `MEM` 列，`MEM` 是指正在处理的请求已使用的内存，单位是 byte。

```sql
+----+------+------+--------------------+---------+------+-------+---------------------------+-----+
| ID | USER | HOST | DB                 | COMMAND | TIME | STATE | INFO                      | MEM |
+----+------+------+--------------------+---------+------+-------+---------------------------+-----+
| 1  | root | ::1  | INFORMATION_SCHEMA | Query   | 0    | 2     | select * from PROCESSLIST | 0   |
+----+------+------+--------------------+---------+------+-------+---------------------------+-----+
```

`PROCESSLIST` 表各列的含义如下：

* ID：客户连接 ID。
* USER：执行当前 PROCESS 的用户名。
* HOST：客户连接的地址。
* DB：当前连接的默认数据库名。
* COMMAND：当前 PROCESS 执行的命令类型。
* TIME：当前 PROCESS 的已经执行的时间，单位是秒。
* STATE：当前连接的状态。
* INFO：正在处理的请求语句。
* MEM：正在处理的请求已使用的内存，单位是 byte。

## CLUSTER_PROCESSLIST

`CLUSTER_PROCESSLIST` 是 `PROCESSLIST` 对应的集群系统表，用于查询集群中所有 TiDB 节点的 `PROCESSLIST` 信息。`CLUSTER_PROCESSLIST` 表结构上比 `PROCESSLIST` 多一列 `INSTANCE`，表示该行数据来自的 TiDB 节点地址。

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.cluster_processlist;
```

```sql
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

## SCHEMATA 表

`SCHEMATA` 表提供了关于数据库的信息。表中的数据与 `SHOW DATABASES` 语句的执行结果等价。

{{< copyable "sql" >}}

```sql
SELECT * FROM schemata;
```

```sql
+--------------+--------------------+----------------------------+------------------------+----------+
| CATALOG_NAME | SCHEMA_NAME        | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH |
+--------------+--------------------+----------------------------+------------------------+----------+
| def          | INFORMATION_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | mynewdb            | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | mysql              | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | PERFORMANCE_SCHEMA | utf8mb4                    | utf8mb4_bin            | NULL     |
| def          | test               | utf8mb4                    | utf8mb4_bin            | NULL     |
+--------------+--------------------+----------------------------+------------------------+----------+
5 rows in set (0.00 sec)
```

`SCHEMATA` 表各列字段含义如下：

* CATALOG_NAME：数据库归属的目录名，该列值永远为 `def`。
* SCHEMA_NAME：数据库的名字。
* DEFAULT_CHARACTER_SET_NAME：数据库的默认字符集。
* DEFAULT_COLLATION_NAME：数据库的默认 collation。
* SQL_PATH：该项值永远为 `NULL`。

## SESSION_VARIABLES 表

`SESSION_VARIABLES` 表提供了关于 session 变量的信息。表中的数据跟 `SHOW SESSION VARIABLES` 语句执行结果类似。

{{< copyable "sql" >}}

```sql
SELECT * FROM session_variables LIMIT 10;
```

```sql
+----------------------------------+----------------------+
| VARIABLE_NAME                    | VARIABLE_VALUE       |
+----------------------------------+----------------------+
| max_write_lock_count             | 18446744073709551615 |
| server_id_bits                   | 32                   |
| net_read_timeout                 | 30                   |
| innodb_online_alter_log_max_size | 134217728            |
| innodb_optimize_fulltext_only    | OFF                  |
| max_join_size                    | 18446744073709551615 |
| innodb_read_io_threads           | 4                    |
| session_track_gtids              | OFF                  |
| have_ssl                         | DISABLED             |
| max_binlog_cache_size            | 18446744073709547520 |
+----------------------------------+----------------------+
10 rows in set (0.00 sec)
```

`SESSION_VARIABLES` 表各列字段含义如下：

* `VARIABLE_NAME`：数据库中 session 级变量的名称。
* `VARIABLE_VALUE`：数据库中对应该 session 变量名的具体值。

## SLOW_QUERY 表

`SLOW_QUERY` 表中提供了当前节点的慢查询相关的信息，其内容通过解析当前节点的 TiDB 慢查询日志而来，列名和慢日志中的字段名是一一对应。关于如何使用该表调查和改善慢查询请参考[慢查询日志文档](/identify-slow-queries.md)。

{{< copyable "sql" >}}

```sql
desc information_schema.slow_query;
```

```sql
+---------------------------+---------------------+------+-----+---------+-------+
| Field                     | Type                | Null | Key | Default | Extra |
+---------------------------+---------------------+------+-----+---------+-------+
| Time                      | timestamp unsigned  | YES  |     | <null>  |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |     | <null>  |       |
| User                      | varchar(64)         | YES  |     | <null>  |       |
| Host                      | varchar(64)         | YES  |     | <null>  |       |
| Conn_ID                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Query_time                | double unsigned     | YES  |     | <null>  |       |
| Parse_time                | double unsigned     | YES  |     | <null>  |       |
| Compile_time              | double unsigned     | YES  |     | <null>  |       |
| Prewrite_time             | double unsigned     | YES  |     | <null>  |       |
| Wait_prewrite_binlog_time | double unsigned     | YES  |     | <null>  |       |
| Commit_time               | double unsigned     | YES  |     | <null>  |       |
| Get_commit_ts_time        | double unsigned     | YES  |     | <null>  |       |
| Commit_backoff_time       | double unsigned     | YES  |     | <null>  |       |
| Backoff_types             | varchar(64)         | YES  |     | <null>  |       |
| Resolve_lock_time         | double unsigned     | YES  |     | <null>  |       |
| Local_latch_wait_time     | double unsigned     | YES  |     | <null>  |       |
| Write_keys                | bigint(22) unsigned | YES  |     | <null>  |       |
| Write_size                | bigint(22) unsigned | YES  |     | <null>  |       |
| Prewrite_region           | bigint(22) unsigned | YES  |     | <null>  |       |
| Txn_retry                 | bigint(22) unsigned | YES  |     | <null>  |       |
| Process_time              | double unsigned     | YES  |     | <null>  |       |
| Wait_time                 | double unsigned     | YES  |     | <null>  |       |
| Backoff_time              | double unsigned     | YES  |     | <null>  |       |
| LockKeys_time             | double unsigned     | YES  |     | <null>  |       |
| Request_count             | bigint(20) unsigned | YES  |     | <null>  |       |
| Total_keys                | bigint(20) unsigned | YES  |     | <null>  |       |
| Process_keys              | bigint(20) unsigned | YES  |     | <null>  |       |
| DB                        | varchar(64)         | YES  |     | <null>  |       |
| Index_names               | varchar(100)        | YES  |     | <null>  |       |
| Is_internal               | tinyint(1) unsigned | YES  |     | <null>  |       |
| Digest                    | varchar(64)         | YES  |     | <null>  |       |
| Stats                     | varchar(512)        | YES  |     | <null>  |       |
| Cop_proc_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_addr             | varchar(64)         | YES  |     | <null>  |       |
| Cop_wait_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_addr             | varchar(64)         | YES  |     | <null>  |       |
| Mem_max                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Succ                      | tinyint(1) unsigned | YES  |     | <null>  |       |
| Plan_from_cache           | tinyint(1)          | YES  |     | <null>  |       |
| Plan                      | longblob unsigned   | YES  |     | <null>  |       |
| Plan_digest               | varchar(128)        | YES  |     | <null>  |       |
| Prev_stmt                 | longblob unsigned   | YES  |     | <null>  |       |
| Query                     | longblob unsigned   | YES  |     | <null>  |       |
+---------------------------+---------------------+------+-----+---------+-------+
```

## CLUSTER_SLOW_QUERY 表

`CLUSTER_SLOW_QUERY` 表中提供了集群所有节点的慢查询相关的信息，其内容通过解析 TiDB 慢查询日志而来，该表使用上和 [`SLOW_QUERY`](#slow_query-表) 一样，表结构上比 `SLOW_QUERY` 多一列 `INSTANCE`，表示该行慢查询信息来自的 TiDB 节点地址。关于如何使用该表调查和改善慢查询请参考[慢查询日志文档](/identify-slow-queries.md)。

{{< copyable "sql" >}}

```sql
desc information_schema.cluster_slow_query;
```

```sql
+---------------------------+---------------------+------+-----+---------+-------+
| Field                     | Type                | Null | Key | Default | Extra |
+---------------------------+---------------------+------+-----+---------+-------+
| INSTANCE                  | varchar(64)         | YES  |     | <null>  |       |
| Time                      | timestamp unsigned  | YES  |     | <null>  |       |
| Txn_start_ts              | bigint(20) unsigned | YES  |     | <null>  |       |
| User                      | varchar(64)         | YES  |     | <null>  |       |
| Host                      | varchar(64)         | YES  |     | <null>  |       |
| Conn_ID                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Query_time                | double unsigned     | YES  |     | <null>  |       |
| Parse_time                | double unsigned     | YES  |     | <null>  |       |
| Compile_time              | double unsigned     | YES  |     | <null>  |       |
| Prewrite_time             | double unsigned     | YES  |     | <null>  |       |
| Wait_prewrite_binlog_time | double unsigned     | YES  |     | <null>  |       |
| Commit_time               | double unsigned     | YES  |     | <null>  |       |
| Get_commit_ts_time        | double unsigned     | YES  |     | <null>  |       |
| Commit_backoff_time       | double unsigned     | YES  |     | <null>  |       |
| Backoff_types             | varchar(64)         | YES  |     | <null>  |       |
| Resolve_lock_time         | double unsigned     | YES  |     | <null>  |       |
| Local_latch_wait_time     | double unsigned     | YES  |     | <null>  |       |
| Write_keys                | bigint(22) unsigned | YES  |     | <null>  |       |
| Write_size                | bigint(22) unsigned | YES  |     | <null>  |       |
| Prewrite_region           | bigint(22) unsigned | YES  |     | <null>  |       |
| Txn_retry                 | bigint(22) unsigned | YES  |     | <null>  |       |
| Process_time              | double unsigned     | YES  |     | <null>  |       |
| Wait_time                 | double unsigned     | YES  |     | <null>  |       |
| Backoff_time              | double unsigned     | YES  |     | <null>  |       |
| LockKeys_time             | double unsigned     | YES  |     | <null>  |       |
| Request_count             | bigint(20) unsigned | YES  |     | <null>  |       |
| Total_keys                | bigint(20) unsigned | YES  |     | <null>  |       |
| Process_keys              | bigint(20) unsigned | YES  |     | <null>  |       |
| DB                        | varchar(64)         | YES  |     | <null>  |       |
| Index_names               | varchar(100)        | YES  |     | <null>  |       |
| Is_internal               | tinyint(1) unsigned | YES  |     | <null>  |       |
| Digest                    | varchar(64)         | YES  |     | <null>  |       |
| Stats                     | varchar(512)        | YES  |     | <null>  |       |
| Cop_proc_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_proc_addr             | varchar(64)         | YES  |     | <null>  |       |
| Cop_wait_avg              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_p90              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_max              | double unsigned     | YES  |     | <null>  |       |
| Cop_wait_addr             | varchar(64)         | YES  |     | <null>  |       |
| Mem_max                   | bigint(20) unsigned | YES  |     | <null>  |       |
| Succ                      | tinyint(1) unsigned | YES  |     | <null>  |       |
| Plan_from_cache           | tinyint(1)          | YES  |     | <null>  |       |
| Plan                      | longblob unsigned   | YES  |     | <null>  |       |
| Plan_digest               | varchar(128)        | YES  |     | <null>  |       |
| Prev_stmt                 | longblob unsigned   | YES  |     | <null>  |       |
| Query                     | longblob unsigned   | YES  |     | <null>  |       |
+---------------------------+---------------------+------+-----+---------+-------+
```

查询集群系统表时，TiDB 也会将相关计算下推给其他节点执行，而不是把所有节点的数据都取回来，可以查看执行计划如下：

{{< copyable "sql" >}}

```sql
desc select count(*) from information_schema.cluster_slow_query where user = 'u1';
```

```sql
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

{{< copyable "sql" >}}

```sql
select /*+ AGG_TO_COP() */ count(*) from information_schema.cluster_slow_query group by user;
```

## STATISTICS 表

`STATISTICS` 表提供了关于表索引的信息。

{{< copyable "sql" >}}

```sql
desc statistics;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| TABLE_CATALOG | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
| NON_UNIQUE    | varchar(1)    | YES  |      | NULL    |       |
| INDEX_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME    | varchar(64)   | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(2)     | YES  |      | NULL    |       | 
| COLUMN_NAME   | varchar(21)   | YES  |      | NULL    |       |
| COLLATION     | varchar(1)    | YES  |      | NULL    |       |
| CARDINALITY   | bigint(21)    | YES  |      | NULL    |       |
| SUB_PART      | bigint(3)     | YES  |      | NULL    |       |
| PACKED        | varchar(10)   | YES  |      | NULL    |       |
| NULLABLE      | varchar(3)    | YES  |      | NULL    |       |
| INDEX_TYPE    | varchar(16)   | YES  |      | NULL    |       | 
| COMMENT       | varchar(16)   | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(1024) | YES  |      | NULL    |       |
| IS_VISIBLE    | varchar(3)    | YES  |      | NULL    |       |
| Expression    | varchar(64)   | YES  |      | NULL    |       | 
+---------------+---------------+------+------+---------+-------+
```

下列语句是等价的：

{{< copyable "sql" >}}

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'
```

{{< copyable "sql" >}}

```sql
SHOW INDEX
  FROM tbl_name
  FROM db_name
```

## TABLES 表

`TABLES` 表提供了数据库里面关于表的信息。

{{< copyable "sql" >}}

```sql
SELECT * FROM tables WHERE table_schema='mysql' AND table_name='user';
```

```
*************************** 1. row ***************************
            TABLE_CATALOG: def
             TABLE_SCHEMA: mysql
               TABLE_NAME: user
               TABLE_TYPE: BASE TABLE
                   ENGINE: InnoDB
                  VERSION: 10
               ROW_FORMAT: Compact
               TABLE_ROWS: 0
           AVG_ROW_LENGTH: 0
              DATA_LENGTH: 0
          MAX_DATA_LENGTH: 0
             INDEX_LENGTH: 0
                DATA_FREE: 0
           AUTO_INCREMENT: 0
              CREATE_TIME: 2019-03-29 09:17:27
              UPDATE_TIME: NULL
               CHECK_TIME: NULL
          TABLE_COLLATION: utf8mb4_bin
                 CHECKSUM: NULL
           CREATE_OPTIONS:
            TABLE_COMMENT:
            TIDB_TABLE_ID: 5
TIDB_ROW_ID_SHARDING_INFO: NULL
1 row in set (0.00 sec)
```

以下操作是等价的：

{{< copyable "sql" >}}

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']
```

{{< copyable "sql" >}}

```sql
SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES` 表各列字段含义如下：

* `TABLE_CATALOG`：表所属的目录的名称。该值始终为 `def`。
* `TABLE_SCHEMA`：表所属数据库的名称。
* `TABLE_NAME`：表的名称。
* `TABLE_TYPE`：表的类型。
* `ENGINE`：存储引擎类型。该值暂为 ‘InnoDB’。
* `VERSION`：版本，默认值为 10。
* `ROW_FORMAT`：行格式。该值暂为 ‘Compact’。
* `TABLE_ROWS`：统计信息中该表所存的行数。
* `AVG_ROW_LENGTH`：该表中所存数据的平均行长度。平均行长度 = DATA_LENGTH / 统计信息中的行数。
* `DATA_LENGTH`：数据长度。数据长度 = 统计信息中的行数 × 元组各列存储长度和，这里尚未考虑 TiKV 的副本数。
* `MAX_DATA_LENGTH`：最大数据长度。该值暂为 0，表示没有最大数据长度的限制。
* `INDEX_LENGTH`：索引长度。索引长度 = 统计信息中的行数 × 索引元组各列长度和，这里尚未考虑 TiKV 的副本数。
* `DATA_FREE`：空间碎片。该值暂为 0。
* `AUTO_INCREMENT`：该表中自增主键自动增量的当前值。
* `CREATE_TIME`：该表的创建时间。
* `UPDATE_TIME`：该表的更新时间。
* `CHECK_TIME`：该表的检查时间。
* `TABLE_COLLATION`：该表的字符校验编码集。
* `CHECKSUM`：校验和。
* `CREATE_OPTIONS`：创建选项。
* `TABLE_COMMENT`：表的注释、备注。

表中的信息大部分定义自 MySQL，此外有两列是 TiDB 新增的：

* `TIDB_TABLE_ID`：标识表的内部 ID，该 ID 在一个 TiDB 集群内部唯一。
* `TIDB_ROW_ID_SHARDING_INFO`：标识表的 Sharding 类型，可能的值为：
    - `"NOT_SHARDED"`：表未被 Shard。
    - `"NOT_SHARDED(PK_IS_HANDLE)"`：一个定义了整型主键的表未被 Shard。
    - `"PK_AUTO_RANDOM_BITS={bit_number}"`：一个定义了整型主键的表由于定义了 `AUTO_RANDOM` 而被 Shard。
    - `"SHARD_BITS={bit_number}"`：表使用 `SHARD_ROW_ID_BITS={bit_number}` 进行了 Shard。
    - NULL：表属于系统表或 View，无法被 Shard。

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
