---
title: SHOW MASKING POLICIES
summary: TiDB 数据库中 SHOW MASKING POLICIES 的使用概况。
---

# SHOW MASKING POLICIES

`SHOW MASKING POLICIES` 语句用于查看指定表上定义的脱敏策略信息。

## 所需权限

查看脱敏策略需要拥有目标表的 `ALTER MASKING POLICY` 权限。

## 语法图

```ebnf+diagram
ShowMaskingPoliciesStmt ::=
    'SHOW' 'MASKING' 'POLICIES' 'FOR' TableName WhereClauseOptional

TableName ::=
    Identifier ('.' Identifier)?

WhereClauseOptional ::=
    ( 'WHERE' Expression )?
```

## 示例

创建脱敏策略后，使用 `SHOW MASKING POLICIES` 查看策略信息：

{{< copyable "sql" >}}

```sql
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  ssn VARCHAR(20),
  salary DECIMAL(10,2)
);

CREATE MASKING POLICY p_mask_ssn
  ON employees(ssn)
  AS MASK_FULL(ssn) ENABLE;

CREATE MASKING POLICY p_mask_salary
  ON employees(salary)
  AS MASK_NULL(salary) ENABLE;

SHOW MASKING POLICIES FOR employees;
```

```
Query OK, 0 rows affected (0.10 sec)

Query OK, 0 rows affected (0.08 sec)

Query OK, 0 rows affected (0.08 sec)

+----------------+---------+--------+-----------------+-----------+
| PolicyName     | Column  | Status | Expression      | Restrict  |
+----------------+---------+--------+-----------------+-----------+
| p_mask_ssn     | ssn     | ENABLE | MASK_FULL(ssn)  | NONE      |
| p_mask_salary  | salary  | ENABLE | MASK_NULL(salary) | NONE    |
+----------------+---------+--------+-----------------+-----------+
2 rows in set (0.01 sec)
```

### 使用 WHERE 子句过滤

{{< copyable "sql" >}}

```sql
SHOW MASKING POLICIES FOR employees WHERE Status = 'ENABLE';
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展，在 MySQL 中不存在。

## 另请参阅

* [CREATE MASKING POLICY](/sql-statements/sql-statement-create-masking-policy.md)
* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)