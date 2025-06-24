---
title: EXPLAIN 使用视图的语句
summary: 了解 TiDB 中 `EXPLAIN` 语句返回的执行计划信息。
---

# EXPLAIN 使用视图的语句

`EXPLAIN` 显示[视图](/views.md)引用的表和索引，而不是视图本身的名称。这是因为视图只是虚拟表，本身不存储任何数据。视图的定义和语句的其余部分在 SQL 优化期间会合并在一起。

<CustomContent platform="tidb">

从 [bikeshare 示例数据库](/import-example-data.md)中，你可以看到以下两个查询的执行方式类似：

</CustomContent>

<CustomContent platform="tidb-cloud">

从 [bikeshare 示例数据库](/tidb-cloud/import-sample-data.md)中，你可以看到以下两个查询的执行方式类似：

</CustomContent>

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (duration);
CREATE OR REPLACE VIEW long_trips AS SELECT * FROM trips WHERE duration > 3600;
EXPLAIN SELECT * FROM long_trips;
EXPLAIN SELECT * FROM trips WHERE duration > 3600;
```

```sql
Query OK, 0 rows affected (2 min 10.11 sec)

Query OK, 0 rows affected (0.13 sec)

+--------------------------------+------------+-----------+---------------------------------------+-------------------------------------+
| id                             | estRows    | task      | access object                         | operator info                       |
+--------------------------------+------------+-----------+---------------------------------------+-------------------------------------+
| IndexLookUp_12                 | 6372547.67 | root      |                                       |                                     |
| ├─IndexRangeScan_10(Build)     | 6372547.67 | cop[tikv] | table:trips, index:duration(duration) | range:(3600,+inf], keep order:false |
| └─TableRowIDScan_11(Probe)     | 6372547.67 | cop[tikv] | table:trips                           | keep order:false                    |
+--------------------------------+------------+-----------+---------------------------------------+-------------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+-----------+-----------+---------------------------------------+-------------------------------------+
| id                            | estRows   | task      | access object                         | operator info                       |
+-------------------------------+-----------+-----------+---------------------------------------+-------------------------------------+
| IndexLookUp_10                | 833219.37 | root      |                                       |                                     |
| ├─IndexRangeScan_8(Build)     | 833219.37 | cop[tikv] | table:trips, index:duration(duration) | range:(3600,+inf], keep order:false |
| └─TableRowIDScan_9(Probe)     | 833219.37 | cop[tikv] | table:trips                           | keep order:false                    |
+-------------------------------+-----------+-----------+---------------------------------------+-------------------------------------+
3 rows in set (0.00 sec)
```

类似地，视图中的谓词会下推到基表：

{{< copyable "sql" >}}

```sql
EXPLAIN SELECT * FROM long_trips WHERE bike_number = 'W00950';
EXPLAIN SELECT * FROM trips WHERE bike_number = 'W00950';
```

```sql
+--------------------------------+---------+-----------+---------------------------------------+---------------------------------------------------+
| id                             | estRows | task      | access object                         | operator info                                     |
+--------------------------------+---------+-----------+---------------------------------------+---------------------------------------------------+
| IndexLookUp_14                 | 3.33    | root      |                                       |                                                   |
| ├─IndexRangeScan_11(Build)     | 3333.33 | cop[tikv] | table:trips, index:duration(duration) | range:(3600,+inf], keep order:false, stats:pseudo |
| └─Selection_13(Probe)          | 3.33    | cop[tikv] |                                       | eq(bikeshare.trips.bike_number, "W00950")         |
|   └─TableRowIDScan_12          | 3333.33 | cop[tikv] | table:trips                           | keep order:false, stats:pseudo                    |
+--------------------------------+---------+-----------+---------------------------------------+---------------------------------------------------+
4 rows in set (0.00 sec)

+-------------------------+-------------+-----------+---------------+-------------------------------------------+
| id                      | estRows     | task      | access object | operator info                             |
+-------------------------+-------------+-----------+---------------+-------------------------------------------+
| TableReader_7           | 43.00       | root      |               | data:Selection_6                          |
| └─Selection_6           | 43.00       | cop[tikv] |               | eq(bikeshare.trips.bike_number, "W00950") |
|   └─TableFullScan_5     | 19117643.00 | cop[tikv] | table:trips   | keep order:false                          |
+-------------------------+-------------+-----------+---------------+-------------------------------------------+
3 rows in set (0.00 sec)
```

在上面的第一个语句中，你可以看到索引用于满足视图定义，然后在 TiDB 读取表行时应用 `bike_number = 'W00950'`。在第二个语句中，没有索引可以满足该语句，因此使用了 `TableFullScan`。

TiDB 会使用同时满足视图定义和语句本身的索引。考虑以下复合索引：

{{< copyable "sql" >}}

```sql
ALTER TABLE trips ADD INDEX (bike_number, duration);
EXPLAIN SELECT * FROM long_trips WHERE bike_number = 'W00950';
EXPLAIN SELECT * FROM trips WHERE bike_number = 'W00950';
```

```sql
Query OK, 0 rows affected (2 min 31.20 sec)

+--------------------------------+----------+-----------+-------------------------------------------------------+-------------------------------------------------------+
| id                             | estRows  | task      | access object                                         | operator info                                         |
+--------------------------------+----------+-----------+-------------------------------------------------------+-------------------------------------------------------+
| IndexLookUp_13                 | 63725.48 | root      |                                                       |                                                       |
| ├─IndexRangeScan_11(Build)     | 63725.48 | cop[tikv] | table:trips, index:bike_number(bike_number, duration) | range:("W00950" 3600,"W00950" +inf], keep order:false |
| └─TableRowIDScan_12(Probe)     | 63725.48 | cop[tikv] | table:trips                                           | keep order:false                                      |
+--------------------------------+----------+-----------+-------------------------------------------------------+-------------------------------------------------------+
3 rows in set (0.00 sec)

+-------------------------------+----------+-----------+-------------------------------------------------------+---------------------------------------------+
| id                            | estRows  | task      | access object                                         | operator info                               |
+-------------------------------+----------+-----------+-------------------------------------------------------+---------------------------------------------+
| IndexLookUp_10                | 19117.64 | root      |                                                       |                                             |
| ├─IndexRangeScan_8(Build)     | 19117.64 | cop[tikv] | table:trips, index:bike_number(bike_number, duration) | range:["W00950","W00950"], keep order:false |
| └─TableRowIDScan_9(Probe)     | 19117.64 | cop[tikv] | table:trips                                           | keep order:false                            |
+-------------------------------+----------+-----------+-------------------------------------------------------+---------------------------------------------+
3 rows in set (0.00 sec)
```

在第一个语句中，TiDB 能够使用复合索引 `(bike_number, duration)` 的两个部分。在第二个语句中，只使用了索引 `(bike_number, duration)` 的第一部分 `bike_number`。
