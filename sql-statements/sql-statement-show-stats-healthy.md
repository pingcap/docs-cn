---
title: SHOW STATS_HEALTHY
summary: TiDB 数据库中 SHOW STATS_HEALTHY 的使用概述。
---

# SHOW STATS_HEALTHY

`SHOW STATS_HEALTHY` 语句显示统计信息被认为准确程度的估计值。健康度百分比较低的表可能会生成次优的查询执行计划。

可以通过运行 [`ANALYZE`](/sql-statements/sql-statement-analyze-table.md) 语句来提高表的健康度。当健康度低于 [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) 阈值时，`ANALYZE` 会自动运行。

目前，`SHOW STATS_HEALTHY` 语句返回以下列：

| 列名 | 描述 |
| -------- | ------------- |
| `Db_name` | 数据库名称 |
| `Table_name` | 表名 |
| `Partition_name` | 分区名称 |
| `Healthy` | 介于 0 和 100 之间的健康度百分比 |

## 语法

```ebnf+diagram
ShowStatsHealthyStmt ::=
    "SHOW" "STATS_HEALTHY" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

加载示例数据并运行 `ANALYZE`：

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad VARBINARY(255),
 INDEX(b)
);

INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(255) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 100000;
SELECT SLEEP(1);
ANALYZE TABLE t1;
SHOW STATS_HEALTHY; # 应该是 100% 健康
```

```sql
...
mysql> SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |     100 |
+---------+------------+----------------+---------+
1 row in set (0.00 sec)
```

执行批量更新，删除大约 30% 的记录。检查统计信息的健康度：

```sql
DELETE FROM t1 WHERE id BETWEEN 101010 AND 201010; # 删除大约 30% 的记录
SHOW STATS_HEALTHY; 
```

```sql
mysql> SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |      50 |
+---------+------------+----------------+---------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)
