---
title: 聚簇索引
summary: 了解 TiDB 中的聚簇索引。
---

# 聚簇索引

聚簇索引是 TiDB 在 5.0.0-rc 版本中引入的实验性特性。本文档通过多个示例来说明该特性对 TiDB 查询性能的影响。如需启用此特性及查看详细操作指南，参见 [`tidb_enable_clustered_index` 系统变量介绍](/system-variables.md#tidb_enable_clustered_index-从-v500-rc-版本开始引入)。

通过使用聚簇索引，TiDB 可以更好地组织数据表，从而提高某些查询的性能。有些数据库管理系统也将聚簇索引称为“索引组织表” (index-organized tables)。

TiDB 仅支持根据表的`主键`来进行聚簇操作。聚簇索引启用时，`主键`和`聚簇索引`两个术语在一些情况下可互换使用。`主键`指的是约束（一种逻辑属性），而`聚簇索引`描述的是数据存储的物理实现。

## TiDB v5.0 前支持部分主键作为聚簇索引

在 v5.0 之前，TiDB 对聚簇索引的支持有限，需要同时满足以下条件才能启用：

- 数据表设置了主键
- 主键的数据类型为 `INTEGER` 或 `BIGINT`
- 主键只有一列

当其中任一条件不满足时，TiDB 会创建一个隐藏的 64 位 `handle` 值，以组织该数据表。与非聚簇索引相比，使用聚簇索引一步就能完成表查询，效率更高。下面的例子对比了两张数据表的 `EXPLAIN` 语句输出结果，其中一张表支持使用聚簇索引，而另一张不支持：

```sql
CREATE TABLE always_clusters_in_all_versions (
 id BIGINT NOT NULL PRIMARY KEY auto_increment,
 b CHAR(100),
 INDEX(b)
);

CREATE TABLE does_not_cluster_by_default (
 guid CHAR(32) NOT NULL PRIMARY KEY,
 b CHAR(100),
 INDEX(b)
);

INSERT INTO always_clusters_in_all_versions VALUES (1, 'aaa'), (2, 'bbb');
INSERT INTO does_not_cluster_by_default VALUES ('02dd050a978756da0aff6b1d1d7c8aef', 'aaa'), ('35bfbc09cb3c93d8ef032642521ac042', 'bbb');

EXPLAIN SELECT * FROM always_clusters_in_all_versions WHERE id = 1;
EXPLAIN SELECT * FROM does_not_cluster_by_default WHERE guid = '02dd050a978756da0aff6b1d1d7c8aef';
```

```sql
Query OK, 0 rows affected (0.09 sec)

Query OK, 0 rows affected (0.10 sec)

Records: 2  Duplicates: 0  Warnings: 0

Records: 2  Duplicates: 0  Warnings: 0

+-------------+---------+------+---------------------------------------+---------------+
| id          | estRows | task | access object                         | operator info |
+-------------+---------+------+---------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:always_clusters_in_all_versions | handle:1      |
+-------------+---------+------+---------------------------------------+---------------+
1 row in set (0.00 sec)

+-------------+---------+------+--------------------------------------------------------+---------------+
| id          | estRows | task | access object                                          | operator info |
+-------------+---------+------+--------------------------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:does_not_cluster_by_default, index:PRIMARY(guid) |               |
+-------------+---------+------+--------------------------------------------------------+---------------+
1 row in set (0.00 sec)
```

以上两个 `EXPLAIN` 语句输出结果类似，但在第二个例子中，TiDB 需要首先读取 `guid` 列上的主键索引，才能获得 `handle` 的值。

而在下面的例子中，由于 `does_not_cluster_by_default.b` 这列并不是主键，查询效率差异体现得更为明显。TiDB 必须进行额外的扫表操作 (`└─TableFullScan_5`) 才能将 `handle` 的值转变为 `guid` 的主键值。示例如下：

```sql
EXPLAIN SELECT id FROM always_clusters_in_all_versions WHERE b = 'aaaa';
EXPLAIN SELECT guid FROM does_not_cluster_by_default WHERE b = 'aaaa';
```

```sql
+--------------------------+---------+-----------+---------------------------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                                     | operator info                                         |
+--------------------------+---------+-----------+---------------------------------------------------+-------------------------------------------------------+
| Projection_4             | 0.00    | root      |                                                   | test.always_clusters_in_all_versions.id               |
| └─IndexReader_6          | 0.00    | root      |                                                   | index:IndexRangeScan_5                                |
|   └─IndexRangeScan_5     | 0.00    | cop[tikv] | table:always_clusters_in_all_versions, index:b(b) | range:["aaaa","aaaa"], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+---------------------------------------------------+-------------------------------------------------------+
3 rows in set (0.01 sec)

+---------------------------+---------+-----------+-----------------------------------+------------------------------------------------+
| id                        | estRows | task      | access object                     | operator info                                  |
+---------------------------+---------+-----------+-----------------------------------+------------------------------------------------+
| Projection_4              | 0.00    | root      |                                   | test.does_not_cluster_by_default.guid          |
| └─TableReader_7           | 0.00    | root      |                                   | data:Selection_6                               |
|   └─Selection_6           | 0.00    | cop[tikv] |                                   | eq(test.does_not_cluster_by_default.b, "aaaa") |
|     └─TableFullScan_5     | 2.00    | cop[tikv] | table:does_not_cluster_by_default | keep order:false, stats:pseudo                 |
+---------------------------+---------+-----------+-----------------------------------+------------------------------------------------+
4 rows in set (0.00 sec)
```

## TiDB v5.0 起支持任意主键作为聚簇索引

从 v5.0 开始，TiDB 全面支持使用任意主键作为聚簇索引。下方示例沿用了上一节的数据表例子，但开启了聚簇索引特性，并列出相应的 `EXPLAIN` 语句输出结果：

```sql
SET tidb_enable_clustered_index = 1;
CREATE TABLE will_now_cluster (
 guid CHAR(32) NOT NULL PRIMARY KEY,
 b CHAR(100),
 INDEX(b)
);

INSERT INTO will_now_cluster VALUES (1, 'aaa'), (2, 'bbb');
INSERT INTO will_now_cluster VALUES ('02dd050a978756da0aff6b1d1d7c8aef', 'aaa'), ('35bfbc09cb3c93d8ef032642521ac042', 'bbb');

EXPLAIN SELECT * FROM will_now_cluster WHERE guid = '02dd050a978756da0aff6b1d1d7c8aef';
EXPLAIN SELECT guid FROM will_now_cluster WHERE b = 'aaaa';
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.11 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------+---------+------+-------------------------------------------------------+---------------+
| id          | estRows | task | access object                                         | operator info |
+-------------+---------+------+-------------------------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:will_now_cluster, clustered index:PRIMARY(guid) |               |
+-------------+---------+------+-------------------------------------------------------+---------------+
1 row in set (0.00 sec)

+--------------------------+---------+-----------+------------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                      | operator info                                         |
+--------------------------+---------+-----------+------------------------------------+-------------------------------------------------------+
| Projection_4             | 10.00   | root      |                                    | test.will_now_cluster.guid                            |
| └─IndexReader_6          | 10.00   | root      |                                    | index:IndexRangeScan_5                                |
|   └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:will_now_cluster, index:b(b) | range:["aaaa","aaaa"], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+------------------------------------+-------------------------------------------------------+
3 rows in set (0.00 sec)
```

TiDB 同样支持用复合主键进行聚簇操作：

```sql
SET tidb_enable_clustered_index = 1;
CREATE TABLE composite_primary_key (
 key_a INT NOT NULL,
 key_b INT NOT NULL,
 b CHAR(100),
 PRIMARY KEY (key_a, key_b)
);

INSERT INTO composite_primary_key VALUES (1, 1, 'aaa'), (2, 2, 'bbb');
EXPLAIN SELECT * FROM composite_primary_key WHERE key_a = 1 AND key_b = 2;
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 0 rows affected (0.09 sec)

Query OK, 2 rows affected (0.02 sec)
Records: 2  Duplicates: 0  Warnings: 0

+-------------+---------+------+--------------------------------------------------------------------+---------------+
| id          | estRows | task | access object                                                      | operator info |
+-------------+---------+------+--------------------------------------------------------------------+---------------+
| Point_Get_1 | 1.00    | root | table:composite_primary_key, clustered index:PRIMARY(key_a, key_b) |               |
+-------------+---------+------+--------------------------------------------------------------------+---------------+
1 row in set (0.00 sec)
```

在 MySQL 中，InnoDB 存储引擎默认会使用任意主键作为聚簇索引，此处行为与之一致。

## 存储需求

启用聚簇索引后，主键替代 64 位的 `handle` 值成为表中每行数据的内部指针，所以对存储空间的需求可能会上升，尤其当表中包含很多二级索引时。以下表为例：

```sql
CREATE TABLE t1 (
 guid CHAR(32) NOT NULL PRIMARY KEY,
 b BIGINT,
 INDEX(b)
);
```

因为 `guid` 的指针的数据类型为 `char(32)`，所以 `b` 列的每一个索引都大约需要 `8 + 32 = 40` 个字节的存储空间（一个数据类型为 `BIGINT` 的数据需要 8 个字节来存储）。而在非聚簇索引的数据表中，只需要 `8 + 8 = 16` 个字节。不过，具体的存储需求在数据经过压缩后可能会有所差异。
