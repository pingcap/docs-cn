---
title: DROP BINDING
summary: TiDB 数据库中 DROP BINDING 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-drop-binding/']
---

# DROP BINDING

`DROP BINDING` 语句用于逻辑删除指定的 SQL BIND。

## 语法图

**DropBindingStmt:**

![DropBindingStmt](/media/sqlgram/DropBindingStmt.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**SelectStmt**

![SelectStmt](/media/sqlgram/SelectStmt.png)

## 语法说明

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内删除指定的执行计划绑定，在不指定作用域时默认作用域为 SESSION。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [CREATE BINDING](/sql-statements/sql-statement-create-binding.md)
* [SHOW BINDINGS](/sql-statements/sql-statement-show-bindings.md)
