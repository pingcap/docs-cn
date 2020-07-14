---
title: SHOW BINDINGS
summary: Use of SHOW BINDINGS binding in TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-bindings/']
---

# SHOW BINDINGS

The `SHOW BINDINGS` statement is used to display information about all created SQL bindings.

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## Syntax description

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhereOpt];
```

This statement outputs the execution plan bindings at the GLOBAL or SESSION level. The default scope is SESSION. Currently `SHOW BINDINGS` outputs eight columns, as shown below:

| Column Name | Description |
| :-------- | :------------- |
| original_sql  |  Original SQL statement after parameterization |
| bind_sql | Bound SQL statement with hints |
| default_db | Default database |
| status | Status including 'Using', 'Deleted', 'Invalid', 'Rejected', and 'Pending verification'|
| create_time | Created time |
| update_time | Updated time |
| charset | Character set |
| collation | Sorting rule |
| source | The way in which a binding is created, including `manual` (created by the `create [global] binding` SQL statement), `capture` (captured automatically by TiDB), and `evolve` (evolved automatically by TiDB) |

## See also

* [CREATE BINDING](/sql-statements/sql-statement-create-binding.md)
* [DROP BINDING](/sql-statements/sql-statement-drop-binding.md)
