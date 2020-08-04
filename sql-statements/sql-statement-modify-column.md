---
title: MODIFY COLUMN
summary: TiDB 数据库中 MODIFY COLUMN 的使用概况。
aliases: ['/docs-cn/stable/sql-statements/sql-statement-modify-column/','/docs-cn/v4.0/sql-statements/sql-statement-modify-column/','/docs-cn/stable/reference/sql/statements/modify-column/']
---

# MODIFY COLUMN

`ALTER TABLE .. MODIFY COLUMN` 语句用于修改已有表上的列，包括列的数据类型和属性。若要同时重命名，可改用 [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) 语句。

## 语法图

**AlterTableStmt:**

![AlterTableStmt](/media/sqlgram/AlterTableStmt.png)

**AlterTableSpec:**

![AlterTableSpec](/media/sqlgram/AlterTableSpec.png)

**ColumnKeywordOpt:**

![ColumnKeywordOpt](/media/sqlgram/ColumnKeywordOpt.png)

**ColumnDef:**

![ColumnDef](/media/sqlgram/ColumnDef.png)

**ColumnPosition:**

![ColumnPosition](/media/sqlgram/ColumnPosition.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (id int not null primary key AUTO_INCREMENT, col1 INT);
```

```
Query OK, 0 rows affected (0.11 sec)
```

{{< copyable "sql" >}}

```sql
INSERT INTO t1 (col1) VALUES (1),(2),(3),(4),(5);
```

```
Query OK, 5 rows affected (0.02 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

{{< copyable "sql" >}}

```sql
ALTER TABLE t1 MODIFY col1 BIGINT;
```

```
Query OK, 0 rows affected (0.09 sec)
```

{{< copyable "sql" >}}

```sql
SHOW CREATE TABLE t1\G;
```

```
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `col1` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=30001
1 row in set (0.00 sec)
```

## MySQL 兼容性

* 不支持在单个 `ALTER TABLE` 语句修改多个列，例如：

    ```sql
    ALTER TABLE t1 MODIFY col1 BIGINT, MODIFY id BIGINT NOT NULL;
    ERROR 1105 (HY000): Unsupported multi schema change
    ```

* 不支持有损变更，以及部分数据类型的更改（包括整数改为字符串或 BLOB 格式等）。例如：

    ```sql
    CREATE TABLE t1 (col1 BIGINT);
    ALTER TABLE t1 MODIFY col1 INT;
    ERROR 8200 (HY000): Unsupported modify column length 11 is less than origin 20
    ```

* 不支持修改 decimal 类型的精度。例如：

    ```sql
    CREATE TABLE t (a DECIMAL(5, 3));
    ALTER TABLE t MODIFY COLUMN a DECIMAL(6, 3);
    ERROR 8200 (HY000): Unsupported modify column: can't change decimal column precision
    ```

## 另请参阅

* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
* [ADD COLUMN](/sql-statements/sql-statement-add-column.md)
* [DROP COLUMN](/sql-statements/sql-statement-drop-column.md)
* [CHANGE COLUMN](/sql-statements/sql-statement-change-column.md)
