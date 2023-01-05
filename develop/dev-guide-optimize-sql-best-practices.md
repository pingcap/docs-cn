---
title: Performance Tuning Best Practices
summary: Introduces the best practices for tuning TiDB performance.
---

# Performance Tuning Best Practices

This document introduces some best practices for using TiDB databases.

## DML best practices

This section describes the best practices involved when you use DML with TiDB.

### Use multi-row statements

When you need to modify multiple rows of table, it is recommended to use multi-row statements:

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

It is not recommended to use multiple single-row statements:

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### Use `PREPARE`

When you need to execute a SQL statement for multiple times, it is recommended to use the `PREPARE` statement to avoid the overhead of repeatedly parsing the SQL syntax.

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

Do not execute the `PREPARE` statement repeatedly. Otherwise, the execution efficiency cannot be improved.

### Only query the columns you need

If you do not need data from all columns, do not use `SELECT *` to return all columns data. The following query is inefficient:

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

You should only query the columns you need. For example:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### Use bulk delete

When you delete a large amount of data, it is recommended to use [bulk delete](/develop/dev-guide-delete-data.md#bulk-delete).

### Use bulk update

When you update a large amount of data, it is recommended to use [bulk update](/develop/dev-guide-update-data.md#bulk-update).

### Use `TRUNCATE` instead of `DELETE` for full table data

When you need to delete all data from a table, it is recommended to use the `TRUNCATE` statement:

```sql
TRUNCATE TABLE t;
```

It is not recommended to use `DELETE` for full table data:

```sql
DELETE FROM t;
```

## DDL best practices

This section describes the best practices involved when using TiDB's DDL.

### Primary key best practices

See the [rules to follow when selecting the primary key](/develop/dev-guide-create-table.md#guidelines-to-follow-when-selecting-primary-key).

## Index best practices

See [Index Best Practices](/develop/dev-guide-index-best-practice.md).

### Add index best practices

TiDB supports the online index add operation. You can use [ADD INDEX](/sql-statements/sql-statement-add-index.md) or [CREATE INDEX](/sql-statements/sql-statement-create-index.md) statement to add an index. It does not block data reads and writes in the table. You can adjust the concurrency and the batch size during the `re-organize` phase of the index add operation by modifying the following system variables:

* [`tidb_ddl_reorg_worker_cnt`](/system-variables.md#tidb_ddl_reorg_worker_cnt)
* [`tidb_ddl_reorg_batch_size`](/system-variables.md#tidb_ddl_reorg_batch_size)

To reduce the impact on the online application, the default speed of add index operation is slow. When the target column of add index operation only involves read load or is not directly related to online workload, you can appropriately increase the value of the above variables to speed up the add index operation:

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

When the target column of the add index operation is updated frequently (including `UPDATE`, `INSERT` and `DELETE`), increasing the above variables causes more write conflicts, which impacts the online workload. Accordingly, the add index operation might take a long time to complete due to constant retries. In this case, it is recommended to decrease the value of the above variables to avoid write conflicts with the online application:

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## Transaction conflicts

<CustomContent platform="tidb">

For how to locate and resolve transaction conflicts, see [Troubleshoot Lock Conflicts](/troubleshoot-lock-conflicts.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

For how to locate and resolve transaction conflicts, see [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts).

</CustomContent>

## Best practices for developing Java applications with TiDB

<CustomContent platform="tidb">

See [Best Practices for Developing Java Applications with TiDB](/best-practices/java-app-best-practices.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Best Practices for Developing Java Applications with TiDB](https://docs.pingcap.com/tidb/stable/java-app-best-practices).

</CustomContent>

### See also

<CustomContent platform="tidb">

- [Highly Concurrent Write Best Practices](/best-practices/high-concurrency-best-practices.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [Highly Concurrent Write Best Practices](https://docs.pingcap.com/tidb/stable/high-concurrency-best-practices)

</CustomContent>
