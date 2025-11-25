---
title: 性能调优最佳实践
summary: 介绍使用 TiDB 的性能调优最佳实践。
aliases: ['/zh/tidb/dev/optimize-sql-best-practices']
---

# 性能调优最佳实践

本章将介绍在使用 TiDB 数据库的一些最佳实践。

## DML 最佳实践

以下将介绍使用 TiDB 的 DML 时所涉及到的最佳实践。

### 使用单个语句多行数据操作

当需要修改多行数据时，推荐使用单个 SQL 多行数据的语句：

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

不推荐使用多个 SQL 单行数据的语句：

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### 使用 PREPARE

当需要多次执行某个 SQL 语句时，推荐使用 `PREPARE` 语句，可以避免重复解析 SQL 语法的开销。

<SimpleTab>
<div label="Golang">

在 Golang 中使用 `PREPARE` 语句：

```go
func BatchInsert(db *sql.DB) error {
  stmt, err := db.Prepare("INSERT INTO t (id) VALUES (?), (?), (?), (?), (?)")
  if err != nil {
    return err
  }
  for i := 0; i < 1000; i += 5 {
    values := []interface{}{i, i + 1, i + 2, i + 3, i + 4}
    _, err = stmt.Exec(values...)
    if err != nil {
      return err
    }
  }
  return nil
}
```

</div>

<div label="Java">

在 Java 中使用 `PREPARE` 语句：

```java
public void batchInsert(Connection connection) throws SQLException {
  PreparedStatement statement = connection.prepareStatement(
      "INSERT INTO `t` (`id`) VALUES (?), (?), (?), (?), (?)");
  for (int i = 0; i < 1000; i ++) {
    statement.setInt(i % 5 + 1, i);

    if (i % 5 == 4) {
      statement.executeUpdate();
    }
  }
}
```

</div>

<div label="Python">

在 Python 中使用 `PREPARE` 语句时，并不需要显式指定。在你使用参数化查询时，mysqlclient 等 Driver 将自动转用执行计划。

</div>
</SimpleTab>

注意不要重复执行 `PREPARE` 语句，否则并不能提高执行效率。

### 避免查询不必要的信息

如非必要，不要总是用 `SELECT *` 返回所以列的数据，下面查询是低效的：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

应该仅查询需要的列信息，例如：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 使用批量删除

当需要删除大量的数据，推荐使用批量删除，见[批量删除](/develop/dev-guide-delete-data.md#批量删除)

### 使用批量更新

当需要更新大量的数据时，推荐使用批量更新，见[批量更新](/develop/dev-guide-update-data.md#批量更新)

### 使用 TRUNCATE 语句代替 DELETE 全表数据

当需要删除一个表的所有数据时，推荐使用 `TRUNCATE` 语句：

```sql
TRUNCATE TABLE t;
```

不推荐使用 `DELETE` 全表数据：

```sql
DELETE FROM t;
```

## DDL 最佳实践

以下将介绍使用 TiDB 的 DDL 时所涉及到的最佳实践。

### 主键选择的最佳实践

见[选择主键时应遵守的规则](/develop/dev-guide-create-table.md#选择主键时应遵守的规则)。

## 索引的最佳实践

见[索引的最佳实践](/develop/dev-guide-index-best-practice.md)。

### 添加索引性能最佳实践

TiDB 支持在线添加索引操作，可通过 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 或 [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md) 完成索引添加操作。添加索引不会阻塞表中的数据读写。可以通过修改下面的系统变量来调整 DDL 操作 `re-organize` 阶段的并行度与回填索引的单批数量大小：

- [tidb_ddl_reorg_worker_cnt](/system-variables.md#tidb_ddl_reorg_worker_cnt)
- [tidb_ddl_reorg_batch_size](/system-variables.md#tidb_ddl_reorg_batch_size)

为了减少对在线业务的影响，添加索引的默认速度会比较保守。当添加索引的目标列仅涉及查询负载，或者与线上负载不直接相关时，可以适当调大上述变量来加速添加索引：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

当添加索引操作的目标列被频繁更新（包含 `UPDATE`、`INSERT` 和 `DELETE`）时，调大上述配置会造成较为频繁的写冲突，使得在线负载较大；同时添加索引操作也可能由于不断地重试，需要很长的时间才能完成。此时建议调小上述配置来避免和在线业务的写冲突：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## 事务冲突

关于如何定位和解决事务冲突，请参考[TiDB 锁冲突问题处理](/troubleshoot-lock-conflicts.md)。

## Java 数据库应用开发最佳实践

[开发 Java 应用使用 TiDB 的最佳实践](https://tidb.net/blog/ae01003e)。

### 推荐阅读

- [TiDB 最佳实践系列（一）高并发写入常见热点问题及规避方法](https://tidb.net/blog/09d47cf8)。
