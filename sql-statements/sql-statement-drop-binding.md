---
title: DROP BINDING
summary: Use of DROP BINDING in TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-drop-binding/']
---

# DROP BINDING

The `DROP BINDING` statement is used to drop a SQL bind on TiDB.

## Synopsis

**DropBindingStmt:**

![DropBindingStmt](/media/sqlgram/DropBindingStmt.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**SelectStmt**

![SelectStmt](/media/sqlgram/SelectStmt.png)

## Syntax description

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt;
```

This statement removes a specified execution plan binding at the GLOBAL or SESSION level. The default scope is SESSION.

## See also

* [CREATE BINDING](/sql-statements/sql-statement-create-binding.md)
* [SHOW BINDINGS](/sql-statements/sql-statement-show-bindings.md)
