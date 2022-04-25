---
title: 性能调优最佳实践
---

# 性能调优最佳实践

本节将介绍在使用 TiDB 数据库的一些最佳实践。

## DML 最佳实践

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

当需要删除大量的数据，推荐使用批量删除，见[批量删除](/develop/delete-data.md#批量删除)

### 使用批量更新

当需要更新大量的数据时，推荐使用批量更新，见[批量更新](/develop/update-data.md#批量更新)

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

### 主键选择的最佳实践

见 [主键选择的最佳实践](create-table.md####主键选择的最佳实践)

## 索引的最佳实践

见 [索引的最佳实践](index-best-practice.md)

### ADD INDEX 性能最佳实践

TiDB 支持在线 `ADD INDEX` 操作，不会阻塞表中的数据读写。`ADD INDEX` 的速度可以通过修改下面的系统变量来调整：

- [tidb_ddl_reorg_worker_cnt](https://docs.pingcap.com/zh/tidb/stable/system-variables#tidb_ddl_reorg_worker_cnt)
- [tidb_ddl_reorg_batch_size](https://docs.pingcap.com/zh/tidb/stable/system-variables#tidb_ddl_reorg_batch_size)

为了减少对在线业务的影响，`ADD INDEX` 的默认速度会比较保守。当 `ADD INDEX` 的目标列仅涉及查询负载，或者与线上负载不直接相关时，可以适当调大上述变量来加速 `ADD INDEX`：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

当 `ADD INDEX` 的目标列被频繁更新（包含 `UPDATE`、`INSERT` 和 `DELETE`）时，调大上述配置会造成较为频繁的写冲突，使得在线负载较大；同时 `ADD INDEX` 也可能由于不断地重试，需要很长的时间才能完成。此时建议调小上述配置来避免和在线业务的写冲突：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## 事务冲突

关于如何定位和解决事务冲突，请参考[TiDB 锁冲突问题处理](https://docs.pingcap.com/zh/tidb/stable/troubleshoot-lock-conflicts)。

## 授权最佳实践

// TODO

## Java 数据库应用开发最佳实践

[TiDB 最佳实践系列（五）Java 数据库应用开发指南](https://pingcap.com/zh/blog/best-practice-java)

### 推荐阅读

- [TiDB 最佳实践系列（一）高并发写入常见热点问题及规避方法](https://pingcap.com/zh/blog/tidb-in-high-concurrency-scenarios)
