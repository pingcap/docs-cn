---
title: CREATE BINDING
summary: TiDB 数据库中 CREATE BINDING 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-create-binding/']
---

# CREATE BINDING

`CREATE BINDING` 语句用于在 TiDB 上创建新 SQL BIND。

## 语法图

**CreateBindingStmt:**

![CreateBindingStmt](/media/sqlgram/CreateBindingStmt.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**SelectStmt**

![SelectStmt](/media/sqlgram/SelectStmt.png)

****

## 语法说明

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内为 SQL 绑定执行计划。在不指定作用域时，隐式作用域为 SESSION。

被绑定的 SQL 会被参数化后存储到系统表中。在处理 SQL 查询时，只要参数化后的 SQL 和系统表中某个被绑定的 SQL 语句一致，并且系统变量 `tidb_use_plan_baselines` 的值为 `on`（其默认值为 `on`），即可使用相应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会从中选择代价最小的一个进行绑定。

## 另请参阅

* [DROP BINDING](/sql-statements/sql-statement-drop-binding.md)
* [SHOW BINDINGS](/sql-statements/sql-statement-show-bindings.md)
