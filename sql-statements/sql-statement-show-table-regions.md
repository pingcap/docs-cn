---
title: SHOW TABLE REGIONS
summary: 了解如何在 TiDB 中使用 SHOW TABLE REGIONS。
---

# SHOW TABLE REGIONS

`SHOW TABLE REGIONS` 语句用于显示 TiDB 中表的 Region 信息。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];
SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

## 语法图

```ebnf+diagram
ShowTableRegionStmt ::=
    "SHOW" "TABLE" TableName PartitionNameList? ("INDEX" IndexName)? "REGIONS" ("WHERE" Expression)?

TableName ::=
    (SchemaName ".")? Identifier
```

执行 `SHOW TABLE REGIONS` 返回以下列：

* `REGION_ID`：Region ID。
* `START_KEY`：Region 的起始键。
* `END_KEY`：Region 的结束键。
* `LEADER_ID`：Region 的 Leader ID。
* `LEADER_STORE_ID`：Region leader 所在的 store（TiKV）的 ID。
* `PEERS`：所有 Region 副本的 ID。
* `SCATTERING`：Region 是否正在调度。`1` 表示是。
* `WRITTEN_BYTES`：一个心跳周期内估计写入该 Region 的数据量，单位为字节。
* `READ_BYTES`：一个心跳周期内估计从该 Region 读取的数据量，单位为字节。
* `APPROXIMATE_SIZE(MB)`：该 Region 中数据量的估计值，单位为兆字节（MB）。
* `APPROXIMATE_KEYS`：该 Region 中 Key 的估计数量。

<CustomContent platform="tidb">

* `SCHEDULING_CONSTRAINTS`：与 Region 所属的表或分区相关联的[放置规则设置](/placement-rules-in-sql.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* `SCHEDULING_CONSTRAINTS`：与 Region 所属的表或分区相关联的放置规则设置。

</CustomContent>

* `SCHEDULING_STATE`：具有放置规则的 Region 的调度状态。

> **注意：**
>
> `WRITTEN_BYTES`、`READ_BYTES`、`APPROXIMATE_SIZE(MB)`、`APPROXIMATE_KEYS` 的值不是准确数据。它们是 PD 根据从 Region 收到的心跳信息估算的数据。

## 示例

创建一个包含足够数据以填充几个 Region 的示例表：

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad1 VARBINARY(1024),
 pad2 VARBINARY(1024),
 pad3 VARBINARY(1024)
);
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
SELECT SLEEP(5);
SHOW TABLE t1 REGIONS;
```

输出应该显示表被分割成多个 Region。`REGION_ID`、`START_KEY` 和 `END_KEY` 可能不完全匹配：

```sql
...
mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |                        |                  |
|        96 | t_75_r_31717 | t_75_r_63434 |        97 |               1 | 97    |          0 |             0 |          0 |                   97 |                0 |                        |                  |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |     269323514 |   66346110 |                  245 |           162020 |                        |                  |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
3 rows in set (0.00 sec)
```

在上面的输出中，`START_KEY` 为 `t_75_r_31717` 和 `END_KEY` 为 `t_75_r_63434` 表示主键在 `31717` 和 `63434` 之间的数据存储在这个 Region 中。前缀 `t_75_` 表示这是一个表（`t`）的 Region，该表的内部表 ID 为 `75`。`START_KEY` 或 `END_KEY` 的空值分别表示负无穷或正无穷。

TiDB 会根据需要自动重新平衡 Region。对于手动重新平衡，使用 `SPLIT TABLE REGION` 语句：

```sql
mysql> SPLIT TABLE t1 BETWEEN (31717) AND (63434) REGIONS 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  1 |                    1 |
+--------------------+----------------------+
1 row in set (42.34 sec)

mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |                        |                  |
|        98 | t_75_r_31717 | t_75_r_47575 |        99 |               1 | 99    |          0 |          1325 |          0 |                   53 |            12052 |                        |                  |
|        96 | t_75_r_47575 | t_75_r_63434 |        97 |               1 | 97    |          0 |          1526 |          0 |                   48 |                0 |                        |                  |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |             0 |   55752049 |                   60 |                0 |                        |                  |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
4 rows in set (0.00 sec)
```

上面的输出显示 Region 96 被分割，创建了一个新的 Region 98。表中的其他 Region 不受分割操作的影响。这可以通过输出统计信息确认：

* `TOTAL_SPLIT_REGION` 表示新分割的 Region 数量。在此示例中，数量为 1。
* `SCATTER_FINISH_RATIO` 表示新分割的 Region 成功分散的比率。`1.0` 表示所有 Region 都已分散。

更详细的示例：

```sql
mysql> SHOW TABLE t REGIONS;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 102       | t_43_r       | t_43_r_20000 | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 106       | t_43_r_20000 | t_43_r_40000 | 120       | 7               | 107, 108, 120 | 0          | 23            | 0          | 1                    | 0                |                        |                  |
| 110       | t_43_r_40000 | t_43_r_60000 | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 114       | t_43_r_60000 | t_43_r_80000 | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |                        |                  |
| 3         | t_43_r_80000 |              | 93        | 8               | 5, 73, 93     | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 98        | t_43_        | t_43_r       | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
6 rows in set
```

在上面的示例中：

* 表 t 对应六个 Region。在这些 Region 中，`102`、`106`、`110`、`114` 和 `3` 存储行数据，`98` 存储索引数据。
* 对于 Region `102` 的 `START_KEY` 和 `END_KEY`，`t_43` 表示表前缀和 ID。`_r` 是表 t 中记录数据的前缀。`_i` 是索引数据的前缀。
* 在 Region `102` 中，`START_KEY` 和 `END_KEY` 表示存储了范围 `[-inf, 20000)` 内的记录数据。同样，也可以计算出 Region（`106`、`110`、`114`、`3`）中数据存储的范围。
* Region `98` 存储索引数据。表 t 的索引数据的起始键是 `t_43_i`，它在 Region `98` 的范围内。

要检查 store 1 中对应表 t 的 Region，使用 `WHERE` 子句：

```sql
test> SHOW TABLE t REGIONS WHERE leader_store_id =1;
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS        | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 98        | t_43_     | t_43_r  | 99        | 1               | 99, 100, 101 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+-----------+---------+-----------+-----------------+--------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
```

使用 `SPLIT TABLE REGION` 将索引数据分割成 Region。在下面的示例中，表 t 的索引数据 `name` 在范围 `[a,z]` 内被分割成两个 Region。

```sql
test> SPLIT TABLE t INDEX name BETWEEN ("a") AND ("z") REGIONS 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

现在表 t 对应七个 Region。其中五个（`102`、`106`、`110`、`114`、`3`）存储表 t 的记录数据，另外两个（`135`、`98`）存储索引数据 `name`。

```sql
test> SHOW TABLE t REGIONS;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| 102       | t_43_r                      | t_43_r_20000                | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 106       | t_43_r_20000                | t_43_r_40000                | 120       | 7               | 108, 120, 126 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 110       | t_43_r_40000                | t_43_r_60000                | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 114       | t_43_r_60000                | t_43_r_80000                | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |                        |                  |
| 3         | t_43_r_80000                |                             | 93        | 8               | 73, 93, 128   | 0          | 0             | 0          | 1                    | 0                |                        |                  |
| 135       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 139       | 2               | 138, 139, 140 | 0          | 35            | 0          | 1                    | 0                |                        |                  |
| 98        | t_43_i_1_016d80000000000000 | t_43_r                      | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |                        |                  |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
7 rows in set
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [SPLIT REGION](/sql-statements/sql-statement-split-region.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
