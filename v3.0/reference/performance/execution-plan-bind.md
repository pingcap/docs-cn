---
title: Execution Plan Binding
summary: Learn about execution plan binding operations in TiDB.
category: reference
---

# Execution Plan Binding

The [Optimizer Hints](/v3.0/reference/performance/optimizer-hints.md) document introduces how to select a specific execution plan using Hint. However, sometimes you need to interfere with execution selection without modifying SQL statements. Execution Plan Binding provides a set of functionalities to do this.

## Syntax

### Create binding

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt
```

This statement binds SQL execution plans at the GLOBAL or SESSION level. The default scope is SESSION. The bound SQL statement is parameterized and stored in the system table. When a SQL query is processed, the corresponding optimizer hint is available as long as the parameterized SQL statement and a bound one in the system table are consistent.

`Parameterization` is a process that converts a constant in SQL to a variable parameter, with standardized processing on the spaces and line breaks in the SQL statement, for example,

{{< copyable "sql" >}}

```sql
select * from t where a >    1
-- parameterized:
select * from t where a > ？
```

> **Note:**
>
> The text must be the same before and after parameterization and hint removal for both the original SQL statement and the bound statement, or the binding will fail. Take the following examples:
>
> - This binding can be created successfully because the texts before and after parameterization and hint removal are the same: `select * from t where a > ?`
>
>     ```sql
>     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
>     ```
>
> - This binding will fail because the original SQL statement is processed as `select * from t where a > ?`, while the bound SQL statement is processed differently as `select * from t where b > ?`.
>
>     ```sql
>     CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
>     ```

### Remove binding

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt
```

This statement removes a specified execution plan binding at the GLOBAL or SESSION level. The default scope is SESSION.

### View binding

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

This statement outputs the execution plan bindings at the GLOBAL or SESSION level. The default scope is SESSION. Currently `SHOW BINDINGS` outputs eight columns, as shown below:

| Column Name | Note  |
| :-------- | :------------- |
| original_sql  |  Original SQL statement after parameterization |
| bind_sql | Bound SQL statement with hints |
| default_db | Default database |
| status | Status including Using, Deleted, and Invalid |
| create_time | Creating time |
| update_time | Updating time |
| charset | Character set |
| collation | Ordering rule |
