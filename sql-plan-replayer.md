---
title: 使用 PLAN REPLAYER 保存和恢复集群现场信息
summary: 了解如何使用 PLAN REPLAY 命令保存和恢复集群现场信息。
---

# 使用 PLAN REPLAYER 保存和恢复集群现场信息

用户在定位排查 TiDB 集群问题时，经常需要提供系统和查询计划相关的信息。为了帮助用户更方便地获取相关信息，更高效地排查集群问题，TiDB 在 v5.3.0 中引入了 `PLAN REPLAYER` 命令，用于“一键”保存和恢复现场问题的相关信息，提升查询计划问题诊断的效率，同时方便将问题归档管理。

`PLAN REPLAYER` 主要功能如下：

- 导出排查现场 TiDB 集群的相关信息，导出为 ZIP 格式的文件用于保存。
- 在任意 TiDB 集群上导入另一 TiDB 集群现场信息的 ZIP 文件。

## 使用 `PLAN REPLAYER` 导出集群信息

你可以使用 `PLAN REPLAYER` 来保存 TiDB 集群的现场信息。导出接口如下：

{{< copyable "sql" >}}

```sql
PLAN REPLAYER DUMP EXPLAIN [ANALYZE] sql-statement;
```

TiDB 根据 `sql-statement` 整理出以下集群现场信息：

- TiDB 版本信息
- TiDB 配置信息
- TiDB Session 系统变量
- TiDB 执行计划绑定信息（SQL Binding）
- `sql-statement` 中所包含的表结构
- `sql-statement` 中所包含表的统计信息
- `EXPLAIN [ANALYZE] sql-statement` 的结果
- 优化器进行查询优化的一些内部步骤的记录

> **注意：**
>
> `PLAN REPLAYER` **不会**导出表中数据

### `PLAN REPLAYER` 导出示例

{{< copyable "sql" >}}

```sql
use test;
create table t(a int, b int);
insert into t values(1,1), (2, 2), (3, 3);
analyze table t;

plan replayer dump explain select * from t;
```

`PLAN REPLAYER DUMP` 会将以上信息打包整理成 `ZIP` 文件，并返回文件标识作为执行结果。

> **注意：**
>
> `ZIP` 文件最多会在 TiDB 集群中保存一个小时，超时后 TiDB 会将其删除。

```sql
MySQL [test]> plan replayer dump explain select * from t;
```

```sql
+------------------------------------------------------------------+
| Dump_link                                                        |
+------------------------------------------------------------------+
| replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip |
+------------------------------------------------------------------+
1 row in set (0.015 sec)
```

你同样可以通过 [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_last_plan_replayer_token-从-v630-版本开始引入) 这个会话变量来获取上一次 `PLAN REPLAYER dump` 执行的结果。

```sql
SELECT @@tidb_last_plan_replayer_token;
```

```sql
| @@tidb_last_plan_replayer_token                           |
+-----------------------------------------------------------+
| replayer_Fdamsm3C7ZiPJ-LQqgVjkA==_1663304195885090000.zip |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

对于多条 SQL 的情况，你可以通过文件的方式来获取 plan replayer dump 的结果，多条 SQL 语句在文件中以 `;` 进行分隔。

```sql
plan replayer dump explain 'sqls.txt';
```

```sql
SELECT @@tidb_last_plan_replayer_token;
```

```sql
+-----------------------------------------------------------+
| @@tidb_last_plan_replayer_token                           |
+-----------------------------------------------------------+
| replayer_LEDKg8sb-K0u24QesiH8ig==_1663226556509182000.zip |
+-----------------------------------------------------------+
1 row in set (0.00 sec)
```

因为 MySQL Client 无法下载文件，所以需要通过 TiDB HTTP 接口和文件标识下载文件：

{{< copyable "shell-regular" >}}

```shell
http://${tidb-server-ip}:${tidb-server-status-port}/plan_replayer/dump/${file_token}
```

其中，`${tidb-server-ip}:${tidb-server-status-port}` 是集群中任意 TiDB server 的地址。示例如下：

{{< copyable "shell-regular" >}}

```shell
curl http://127.0.0.1:10080/plan_replayer/dump/replayer_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip > plan_replayer.zip
```

## 使用 `PLAN REPLAYER` 导入集群信息

> **警告：**
>
> `PLAN REPLAYER` 在一个 TiDB 集群上导入另一集群的现场信息，会修改导入集群的 TiDB Session 系统变量、执行计划绑定信息、表结构和统计信息。

有 `PLAN REPLAYER` 导出的 `ZIP` 文件后，用户便可以通过 `PLAN REPLAYER` 导入接口在任意 TiDB 集群上恢复另一集群地现场信息。语法如下：

{{< copyable "sql" >}}

```sql
PLAN REPLAYER LOAD 'file_name';
```

以上语句中，`file_name` 为要导入的 `ZIP` 文件名。

示例如下：

{{< copyable "sql" >}}

```sql
PLAN REPLAYER LOAD 'plan_replayer.zip';
```

导入完毕后，该 TiDB 集群就载入了所需要的表结构、统计信息等其他影响构造 Plan 所需要的信息。你可以通过以下方式查看执行计划以及验证统计信息:

```sql
mysql> desc t;
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
| b     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
2 rows in set (0.01 sec)

mysql> explain select * from t where a = 1 or b =1;
+-------------------------+---------+-----------+---------------+--------------------------------------+
| id                      | estRows | task      | access object | operator info                        |
+-------------------------+---------+-----------+---------------+--------------------------------------+
| TableReader_7           | 0.01    | root      |               | data:Selection_6                     |
| └─Selection_6           | 0.01    | cop[tikv] |               | or(eq(test.t.a, 1), eq(test.t.b, 1)) |
|   └─TableFullScan_5     | 6.00    | cop[tikv] | table:t       | keep order:false, stats:pseudo       |
+-------------------------+---------+-----------+---------------+--------------------------------------+
3 rows in set (0.00 sec)

mysql> show stats_meta;
+---------+------------+----------------+---------------------+--------------+-----------+
| Db_name | Table_name | Partition_name | Update_time         | Modify_count | Row_count |
+---------+------------+----------------+---------------------+--------------+-----------+
| test    | t          |                | 2022-08-26 15:52:07 |            3 |         6 |
+---------+------------+----------------+---------------------+--------------+-----------+
1 row in set (0.04 sec)
```

加载并还原所需现场后，即可在该现场诊断和改进执行计划。

## 使用 `PLAN REPLAYER CAPTURE` 抓取目标计划

在用户定位 TiDB 执行计划的部分场景中，目标 SQL 语句与目标计划可能仅在查询中偶尔出现，无法使用 `PLAN REPLAYER` 直接抓取。此时你可以使用 `PLAN REPLAYER CAPTURE` 来帮助定向抓取目标 SQL 语句与目标计划的优化器信息。

`PLAN REPLAYER CAPTURE` 主要功能如下：

- 在 TiDB 集群内部提前注册目标 SQL 语句与执行计划的 Digest，并开始匹配目标查询。
- 当目标查询匹配成功时，直接抓取其优化器相关信息，导出为 ZIP 格式的文件用于保存。
- 针对匹配到的每组 SQL 和执行计划，信息只抓取一次。
- 通过系统表显示正在进行的匹配任务，以及生成的文件。
- 定时清理历史文件。

### 开启 `PLAN REPLAYER CAPTURE`

`PLAN REPLAYER CAPTURE` 功能通过系统变量 [`tidb_enable_plan_replayer_capture`](/system-variables.md#tidb_enable_plan_replayer_capture) 控制。要开启 `PLAN REPLAYER CAPTURE`，将变量值设为 `ON`。

### 使用 `PLAN REPLAYER CAPTURE` 功能

你可以通过以下方式向 TiDB 集群注册目标 SQL 语句和计划的 Digest:

```sql
PLAN REPLAYER CAPTURE 'sql_digest' 'plan_digest';
```

当你的目标 SQL 语句对应多种执行计划，且你想抓取所有执行计划时，你可以通过以下 SQL 语句一键注册:

```sql
PLAN REPLAYER CAPTURE 'sql_digest' '*';
```

### 查看 `PLAN REPLAYER CAPTURE` 抓取任务

你可以通过以下方式查看集群中目前正在工作的 `PLAN REPLAYER CAPTURE` 的抓取任务:

```sql
mysql> PLAN PLAYER CAPTURE 'example_sql' 'example_plan';
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
+-------------+--------------+---------------------+
| sql_digest  | plan_digest  | update_time         |
+-------------+--------------+---------------------+
| example_sql | example_plan | 2023-01-28 11:58:22 |
+-------------+--------------+---------------------+
1 row in set (0.01 sec)
```

### 查看 `PLAN REPLAYER CAPTURE` 抓取结果

当 `PLAN REPLAYER CAPTURE` 成功抓取到结果后，可以通过以下 SQL 语句查看用于下载的文件标识:

```sql
mysql> SELECT * FROM mysql.plan_replayer_status;
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
| sql_digest                                                       | plan_digest                                                      | origin_sql | token                                                     | update_time         | fail_reason | instance        |
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
| 086e3fbd2732f7671c17f299d4320689deeeb87ba031240e1e598a0ca14f808c | 042de2a6652a6d20afc629ff90b8507b7587a1c7e1eb122c3e0b808b1d80cc02 |            | replayer_Utah4nkz2sIEzkks7tIRog==_1668746293523179156.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
| b5b38322b7be560edb04f33f15b15a885e7c6209a22b56b0804622e397199b54 | 1770efeb3f91936e095f0344b629562bf1b204f6e46439b7d8f842319297c3b5 |            | replayer_Z2mUXNHDjU_WBmGdWQqifw==_1668746293560115314.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
| 96d00c0b3f08795fe94e2d712fa1078ab7809faf4e81d198f276c0dede818cf9 | 8892f74ac2a42c2c6b6152352bc491b5c07c73ac3ed66487b2c990909bae83e8 |            | replayer_RZcRHJB7BaCccxFfOIAhWg==_1668746293578282450.zip | 2022-11-18 12:38:13 | NULL        | 172.16.4.4:4022 |
+------------------------------------------------------------------+------------------------------------------------------------------+------------+-----------------------------------------------------------+---------------------+-------------+-----------------+
3 rows in set (0.00 sec)
```

下载 `PLAN REPLAYER CAPTURE` 的文件方法与 `PLAN REPLAYER` 相同，请参考 [`PLAN REPLAYER` 导出示例](#plan-replayer-导出示例)。

> **注意：**
>
> `PLAN REPLAYER CAPTURE` 的结果文件最多会在 TiDB 集群中保存一周，超时后 TiDB 会将其删除。

### 移除 `PLAN REPLAYER CAPTURE` 抓取任务

不再需要某个 `PLAN REPLAYER CAPTURE` 抓取任务后，你可以通过 `PLAN REPLAYER CAPTURE REMOVE` 语句将其移除。示例如下：

```sql
mysql> PLAN REPLAYER CAPTURE '077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0' '4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| sql_digest                                                       | plan_digest                                                      | update_time         |
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
| 077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0 | 4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce | 2024-05-21 11:26:10 |
+------------------------------------------------------------------+------------------------------------------------------------------+---------------------+
1 row in set (0.01 sec)

mysql> PLAN REPLAYER CAPTURE REMOVE '077a87a576e42360c95530ccdac7a1771c4efba17619e26be50a4cfd967204a0' '4838af52c1e07fc8694761ad193d16a689b2128bc5ced9d13beb31ae27b370ce';
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM mysql.plan_replayer_task;
Empty set (0.01 sec)
```

## 使用 `PLAN REPLAYER CONTINUOUS CAPTURE`

开启 `PLAN REPLAYER CONTINUOUS CAPTURE` 功能后，TiDB 将以 SQL DIGEST 和 PLAN DIGEST 为维度异步地将业务 SQL 语句以 `PLAN REPLAYER` 的方式进行记录，对于相同 DIGEST 的 SQL 语句与执行计划，`PLAN REPLAYER CONTINUOUS CAPTURE` 不会重复记录。

### 开启 `PLAN REPLAYER CONTINUOUS CAPTURE`

`PLAN REPLAYER CONTINUOUS CAPTURE` 功能通过系统变量 [`tidb_enable_plan_replayer_continuous_capture`](/system-variables.md#tidb_enable_plan_replayer_continuous_capture-从-v700-版本开始引入) 控制。要开启 `PLAN REPLAYER CONTINUOUS CAPTURE`，将变量值设为 `ON`。

### 查看 `PLAN REPLAYER CONTINUOUS CAPTURE` 抓取结果

查看 `PLAN REPLAYER CONTINUOUS CAPTURE` 抓取结果的方法同[查看 `PLAN REPLAYER CAPTURE` 抓取结果](#查看-plan-replayer-capture-抓取结果)。
