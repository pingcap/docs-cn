---
title: TiDB Lightning 冲突数据检测
summary: 介绍了 TIDB Lighting 如何处理导入过程中遇到的冲突数据。
---

# 冲突数据检测

冲突数据，即两条或两条以上的记录存在 PK/UK 列数据重复的情况。当数据源中的记录存在冲突数据，将导致该表真实总行数和使用唯一索引查询的总行数不一致的情况。在 v5.3 版本之后，lightning 开始支持冲突数据检测，在不同的导入模式中均可进行配置。

## Local-backend 模式

当使用 local-backend 模式进行数据导入时，可以在 lightning 配置文件中的 duplicate-detection 选项进行配置。一共有三种检测模式：

### none

lightning 默认的配置为 none，即 lightning 不会开启冲突检测，如果存在冲突数据时（PK/UK 列重复），则会导致该表真实总行数和使用唯一索引查询的总行数不一致的情况，并且 checksum 验证无法通过（checksum mismatched remote vs local），从而造成 lightning 报错退出。但 lightning 仍会将全部数据写入到 TiDB 中。

```log
Error: [Lighting:Restore:ErrChecksumMismatch]checksum mismatched remote vs local => (checksum: 16695241788915789231 vs 12854679390123074615) (total_kvs: 5 vs 6) (total_bytes:402 vs 465)
tidb lightning encountered error: [Lighting:Restore:ErrChecksumMismatch]checksum mismatched remote vs local => (checksum: 16695241788915789231 vs 12854679390123074615) (total_kvs: 5 vs 6) (total_bytes:402 vs 465)
```

假设一张表`order_line`的表结构如下：

```sql
CREATE TABLE IF NOT EXISTS `order_line` (
  `ol_o_id` int(11) NOT NULL,
  `ol_d_id` int(11) NOT NULL,
  `ol_w_id` int(11) NOT NULL,
  `ol_number` int(11) NOT NULL,
  `ol_i_id` int(11) NOT NULL,
  `ol_supply_w_id` int(11) DEFAULT NULL,
  `ol_delivery_d` datetime DEFAULT NULL,
  `ol_quantity` int(11) DEFAULT NULL,
  `ol_amount` decimal(6,2) DEFAULT NULL,
  `ol_dist_info` char(24) DEFAULT NULL,
  PRIMARY KEY (`ol_w_id`,`ol_d_id`,`ol_o_id`,`ol_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

使用 `select * from order_line` 进行全表扫描查询数据可得：

```
 ol_o_id | ol_d_id | ol_w_id | ol_number | ol_i_id | ol_supply_w_id | ol_delivery_d | ol_quantity | ol_amount |       ol_dist_info       
---------+---------+---------+-----------+---------+----------------+---------------+-------------+-----------+--------------------------
    2677 |      10 |      10 |        11 |   75656 |             10 |               |           5 | 5831.97   | HT5DN3EVb6kWTd4L37bsbogj 
    2677 |      10 |      10 |        11 |   75656 |             10 |               |           6 | 6666.66   | HT5DN3EVb6kWTd4L37bsbogj 
(2 rows)
```

当我们在 TiDB 中查询主键时，该索引已创建。

```
 Table    | Non_unique | Key_name | Seq_in_index | Column_name | Collation | Cardinality | Sub_part | Packed | Null | Index_type | Comment | Index_comment | Visible | Expression | Clustered 
------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------
 order_line |          0 | PRIMARY  |            1 | ol_w_id     | A         |           0 |          |        |      | BTREE      |         |               | YES     |            | NO 
 order_line |          0 | PRIMARY  |            2 | ol_d_id     | A         |           0 |          |        |      | BTREE      |         |               | YES     |            | NO 
 order_line |          0 | PRIMARY  |            3 | ol_o_id     | A         |           0 |          |        |      | BTREE      |         |               | YES     |            | NO 
 order_line |          0 | PRIMARY  |            4 | ol_number   | A         |           0 |          |        |      | BTREE      |         |               | YES     |            | NO 
(4 rows)
```

如果使用 `select * from order_line where (ol_o_id, ol_d_id, ol_w_id, ol_number) = (2677, 10, 10, 11)` 以主键查询数据，返回数据如下：

```
 ol_o_id | ol_d_id | ol_w_id | ol_number | ol_i_id | ol_supply_w_id | ol_delivery_d | ol_quantity | ol_amount | ol_dist_info
------------+------------+----------+--------------+-------------+-----------+-------------+----------+--------+------+------------+---------+---------------+---------+------------+-----------
 2677 |      10 |      10 |        11 |   75656 |             10 |               |           5 | 5831.97   | HT5DN3EVb6kWTd4L37bsbogj 
(1 row)
```

与实际情况并不一致，仅返回了以主键查找数据时符合条件的第一条数据。

### record

仅将冲突数据添加到目的 TiDB 中的 `lightning_task_info.conflict_error_v1` 表中。该表结构如下：

```sql
CREATE TABLE 'conflict_error_v1' (
  'task_id'     bigint NOT NULL,
  'create_time' datetime(6) NOT NULL DEFAULT now(6),
  'table_name'  varchar(261) NOT NULL,
  'index_name'  varchar(128) NOT NULL,
  'key_data'    text NOT NULL,
  'row_data'   text NOT NULL,
  'raw_key'     mediumblob NOT NULL,
  'raw_value'   mediumblob NOT NULL,
  'raw_handle'  mediumblob NOT NULL,
  'raw_row'     mediumblob NOT NULL,
  KEY (task_id, table_name)
);
```

record 模式会保留所有数据，并跳过 checksum 环节，因此 lightning 不会报错。你可以根据`lightning_task_info.conflict_error_v1` 表中记录的信息手动处理这些冲突数据。注意，该方法要求目的 TiKV 的版本为 v5.2.0 或更新版本。如果版本过低，则会启用 none 模式。

与 `none` 模式相同，假设一张表中有且仅有两条冲突数据，使用 record 模式导入该表后，TiDB 中全表扫描查询数据和主键查询数据返回的结果不相符，后者只会返回符合该查询条件的第一条数据。

### remove

和 record 模式类似，会将冲突数据添加到 `lightning_task_info.conflict_error_v1` 表中并跳过 checksum，但 remove 模式下 lightning 还会将所有冲突数据从 TiDB 中删除。 如果若干条数据发生冲突，这些冲突数据均不会被保留在 TiDB 中，但可以在 `lightning_task_info.conflict_error_v1` 表中查询。

以上面的 `order_line` 表为例，若在导入过程中检测到冲突数据，在 none 和 remove 模式下均可以查询 `lightning_task_info.conflict_error_v1` 表得到以下内容：

```
mysql> select table_name,index_name,key_data,row_data from conflict_error_v1;
+---------------------+------------+----------+-----------------------------------------------------------------------------+
|  table_name         | index_name | key_data | row_data                                                                    |
+---------------------+------------+----------+-----------------------------------------------------------------------------+
| `tpcc`.`order_line` | PRIMARY    | 2 | (2677, 10, 10, 11, 75656, 10, NULL, 5, 5831.97, "HT5DN3EVb6kWTd4L37bsbogj") |
| `tpcc`.`order_line` | PRIMARY    | 3 | (2677, 10, 10, 11, 75656, 10, NULL, 6, 6666.66, "HT5DN3EVb6kWTd4L37bsbogj") |
+---------------------+------------+----------------------------------------------------------------------------------------+
```

当用 `select * from order_line` 查询该表数据时，record 模式下 TiDB 存有包括冲突数据在内的所有数据：

```
 ol_o_id | ol_d_id | ol_w_id | ol_number | ol_i_id | ol_supply_w_id | ol_delivery_d | ol_quantity | ol_amount | ol_dist_info       
---------+---------+---------+-----------+---------+----------------+---------------+-------------+-----------+--------------------------
    2676 |      10 |      13 |        12 |   75658 |             11 |               |           5 | 5831.97   | HT5DN3EVb6kWTd4L37bsbogj 
    2677 |      10 |      10 |        11 |   75656 |             10 |               |           5 | 5831.97   | HT5DN3EVb6kWTd4L37bsbogj 
    2677 |      10 |      10 |        11 |   75656 |             10 |               |           6 | 6666.66   | HT5DN3EVb6kWTd4L37bsbogj 
(3 rows)
```

而 remove 模式下 TiDB 仅保留了非冲突数据，冲突数据会被全部移除：

```
 ol_o_id | ol_d_id | ol_w_id | ol_number | ol_i_id | ol_supply_w_id | ol_delivery_d | ol_quantity | ol_amount | ol_dist_info       
---------+---------+---------+-----------+---------+----------------+---------------+-------------+-----------+--------------------------
    2676 |      10 |      13 |        12 |   75658 |             11 |               |           5 | 5831.97   | HT5DN3EVb6kWTd4L37bsbogj 
(1 rows)
```

## tidb-backend 模式

tidb-backend 模式通过直接执行 SQL 语句导入数据，该模式的冲突检测可由配置文件中的 on-duplicate 进行选择。一共有三种模式:

### replace

在 replace 模式下，遇到冲突数据时，会执行 `REPLACE INTO …`，该 SQL 语句会将数据库中的冲突数据替换为当前的冲突数据。

### ignore

在 ignore 模式下会执行 `INSERT IGNORE INTO …`，如果插入的数据与 TiDB 中的数据发生冲突，该 SQL 语句会忽略该插入指令，也就是说，保留 TiDB 中的数据并忽略当前的冲突数据。

### error

在 error 模式下，则直接执行 `INSERT INTO …`，遇到冲突数据插入时 lightning 会在导入过程中直接报错，并中止导入。查询TiDB 可发现，含有冲突数据的表只导入了表结构，表中无数据存在，但在有冲突数据的表之前导入的表已正常写入数据到 TiDB 中。

```log
Error: restore table `test`.`order_line` failed: Error 1062: Duplicate entry '10-10-2677-11' for key 'PRIMARY'
tidb lightning encountered error:  restore table `test`.`order_line` failed: Error 1062: Duplicate entry '10-10-2677-11' for key 'PRIMARY'
```

在 tidb-backend 模式中，由于执行的 SQL 语句的特性，三种配置下 TiDB 中均不会存在冲突数据。