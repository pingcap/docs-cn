---
title: UPDATE | TiDB SQL 语句参考
summary: TiDB 数据库中 UPDATE 的使用概述。
---

# UPDATE

`UPDATE` 语句用于修改指定表中的数据。

## 语法图

```ebnf+diagram
UpdateStmt ::=
    "UPDATE" UpdateOption
(   TableRef "SET" Assignment ("," Assignment)* WhereClause? OrderBy? Limit?
|   TableRefs "SET" Assignment ("," Assignment)* WhereClause?
)

UpdateOption ::=
    OptimizerHints? ("LOW_PRIORITY" | "HIGH_PRIORITY" | "DELAYED")? "IGNORE"?

TableRef ::=
    ( TableFactor | JoinTable )

TableRefs ::=
    EscapedTableRef ("," EscapedTableRef)*
```

> **注意：**
>
> 从 v6.6.0 开始，TiDB 支持[资源控制](/tidb-resource-control.md)。你可以使用此功能在不同的资源组中以不同的优先级执行 SQL 语句。通过为这些资源组配置适当的配额和优先级，你可以更好地控制不同优先级 SQL 语句的调度。当启用资源控制时，语句优先级（`LOW_PRIORITY` 和 `HIGH_PRIORITY`）将不再生效。建议你使用[资源控制](/tidb-resource-control.md)来管理不同 SQL 语句的资源使用。

## 示例

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)

mysql> UPDATE t1 SET c1=5 WHERE c1=3;
Query OK, 1 row affected (0.01 sec)
Rows matched: 1  Changed: 1  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  5 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL 兼容性

TiDB 在计算表达式时始终使用列的原始值。例如：

```sql
CREATE TABLE t (a int, b int);
INSERT INTO t VALUES (1,2);
UPDATE t SET a = a+1,b=a;
```

在 MySQL 中，列 `b` 被更新为 2，因为它被设置为 `a` 的值，而 `a` 的值（1）在同一语句中被更新为 `a+1`（即 2）。

TiDB 遵循更标准的 SQL 行为，将 `b` 更新为 1。

## 另请参阅

* [INSERT](/sql-statements/sql-statement-insert.md)
* [SELECT](/sql-statements/sql-statement-select.md)
* [DELETE](/sql-statements/sql-statement-delete.md)
* [REPLACE](/sql-statements/sql-statement-replace.md)
