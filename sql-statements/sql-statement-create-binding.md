---
title: CREATE BINDING
summary: Use of CREATE BINDING in TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-create-binding/']
---

# CREATE BINDING

The `CREATE BINDING` statement is used to create a new SQL bind on TiDB.

## Synopsis

**CreateBindingStmt:**

![CreateBindingStmt](/media/sqlgram/CreateBindingStmt.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**SelectStmt**

![SelectStmt](/media/sqlgram/SelectStmt.png)

****

## Syntax description 

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt;
```

This statement binds SQL execution plans at the GLOBAL or SESSION scope. The default scope is SESSION.

The bound SQL statement is parameterized and stored in the system table. When a SQL query is processed, as long as the parameterized SQL statement and a bound one in the system table are consistent and the system variable `tidb_use_plan_baselines` is set to `on` (`on` by default), the corresponding optimizer hint is available. If multiple execution plans are available, the optimizer chooses to bind the plan with the least cost.

## See also

* [DROP BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW BINDINGS](/sql-statements/sql-statement-show-bindings.md)
