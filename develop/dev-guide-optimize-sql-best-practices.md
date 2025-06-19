---
title: 性能调优最佳实践
summary: 介绍 TiDB 性能调优的最佳实践。
---

# 性能调优最佳实践

本文介绍使用 TiDB 数据库的一些最佳实践。

## DML 最佳实践

本节介绍在使用 TiDB 的 DML 时涉及的最佳实践。

### 使用多行语句

当你需要修改表的多行数据时，建议使用多行语句：

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

不建议使用多个单行语句：

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### 使用 `PREPARE`

当你需要多次执行同一个 SQL 语句时，建议使用 `PREPARE` 语句以避免重复解析 SQL 语法的开销。

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

不要重复执行 `PREPARE` 语句。否则，执行效率无法得到提升。

### 只查询需要的列

如果你不需要所有列的数据，不要使用 `SELECT *` 返回所有列数据。以下查询效率不高：

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

你应该只查询需要的列。例如：

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### 使用批量删除

当你删除大量数据时，建议使用[批量删除](/develop/dev-guide-delete-data.md#bulk-delete)。

### 使用批量更新

当你更新大量数据时，建议使用[批量更新](/develop/dev-guide-update-data.md#bulk-update)。

### 使用 `TRUNCATE` 而不是 `DELETE` 删除全表数据

当你需要删除表中的所有数据时，建议使用 `TRUNCATE` 语句：

```sql
TRUNCATE TABLE t;
```

不建议使用 `DELETE` 删除全表数据：

```sql
DELETE FROM t;
```

## DDL 最佳实践

本节介绍使用 TiDB 的 DDL 时涉及的最佳实践。

### 主键最佳实践

请参阅[选择主键时需要遵循的规则](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key)。

## 索引最佳实践

请参阅[索引的最佳实践](/develop/dev-guide-index-best-practice.md)。

### 添加索引最佳实践

TiDB 支持在线添加索引操作。你可以使用 [ADD INDEX](/sql-statements/sql-statement-add-index.md) 或 [CREATE INDEX](/sql-statements/sql-statement-create-index.md) 语句添加索引。这不会阻塞表中的数据读写。你可以通过修改以下系统变量来调整索引添加操作的 `re-organize` 阶段的并发度和批量大小：

* [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
* [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

为了减少对在线应用的影响，添加索引操作的默认速度较慢。当添加索引操作的目标列只涉及读取负载或与在线工作负载没有直接关系时，你可以适当增加上述变量的值来加快添加索引操作：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

当添加索引操作的目标列经常被更新（包括 `UPDATE`、`INSERT` 和 `DELETE`）时，增加上述变量会导致更多的写入冲突，这会影响在线工作负载。相应地，由于不断重试，添加索引操作可能需要很长时间才能完成。在这种情况下，建议减小上述变量的值以避免与在线应用发生写入冲突：

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## 事务冲突

<CustomContent platform="tidb">

关于如何定位和解决事务冲突，请参阅[故障诊断：锁冲突](/troubleshoot-lock-conflicts.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

关于如何定位和解决事务冲突，请参阅[故障诊断：锁冲突](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)。

</CustomContent>

## 使用 TiDB 开发 Java 应用程序的最佳实践

<CustomContent platform="tidb">

请参阅[使用 TiDB 开发 Java 应用程序的最佳实践](/best-practices/java-app-best-practices.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

请参阅[使用 TiDB 开发 Java 应用程序的最佳实践](https://docs.pingcap.com/tidb/stable/java-app-best-practices)。

</CustomContent>

### 另请参阅

<CustomContent platform="tidb">

- [高并发写入最佳实践](/best-practices/high-concurrency-best-practices.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [高并发写入最佳实践](https://docs.pingcap.com/tidb/stable/high-concurrency-best-practices)

</CustomContent>

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
