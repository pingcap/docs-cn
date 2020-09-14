---
title: SHOW STATS_HEALTHY
summary: TiDB 数据库中 SHOW STATS_HEALTHY 的使用概况。
---

# SHOW STATS_HEALTHY

`SHOW STATS_HEALTHY` 语句可以预估统计信息的准确度，也就是健康度。健康度低的表可能会生成次优查询执行计划。

可以通过执行 `ANALYZE` 表命令来改善表的健康度。当表的健康度下降到低于 [`tidb_auto_analyze_ratio`](/system-variables.md#tidb_auto_analyze_ratio) 时，则会自动执行 `ANALYZE` 命令。

## 语法图

**ShowStmt**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 示例

加载示例数据并运行 `ANALYZE` 命令：

{{< copyable "sql" >}}

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
SHOW STATS_HEALTHY; # should be 100% healthy
```

{{< copyable "sql" >}}

```sql
SHOW STATS_HEALTHY;
```

```sql
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |     100 |
+---------+------------+----------------+---------+
1 row in set (0.00 sec)
```

执行批量更新来删除大约 30% 的记录，然后检查统计信息的健康度：

{{< copyable "sql" >}}

```sql
DELETE FROM t1 WHERE id BETWEEN 101010 AND 201010; # delete about 30% of records
SHOW STATS_HEALTHY;
```

```sql
SHOW STATS_HEALTHY;
+---------+------------+----------------+---------+
| Db_name | Table_name | Partition_name | Healthy |
+---------+------------+----------------+---------+
| test    | t1         |                |      50 |
+---------+------------+----------------+---------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW STATS_HEALTHY` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ANALYZE](/sql-statements/sql-statement-analyze-table.md)
* [统计信息简介](/statistics.md)