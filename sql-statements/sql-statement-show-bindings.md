---
title: SHOW BINDINGS
summary: TiDB 数据库中 SHOW BINDINGS 的使用概况。
---

# SHOW BINDINGS

`SHOW BINDINGS` 语句用于显示所有创建过的 SQL BIND 的相关信息。

## 语法图

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

**GlobalScope:**

![GlobalScope](/media/sqlgram/GlobalScope.png)

**ShowLikeOrWhereOpt**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 语法说明

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhereOpt];
```

该语句会输出 GLOBAL 或者 SESSION 作用域内的执行计划绑定，在不指定作用域时默认作用域为 SESSION。目前 `SHOW BINDINGS` 会输出 8 列，具体如下：

| 列名 | 说明            |
| -------- | ------------- |
| original_sql  |  参数化后的原始 SQL |
| bind_sql | 带 Hint 的绑定 SQL |
| default_db | 默认数据库名 |
| status | 状态，包括 using（正在使用）、deleted（已删除）、 invalid（无效）、rejected（演进时被拒绝）和 pending verify（等待演进验证） |
| create_time | 创建时间 |
| update_time | 更新时间 |
| charset | 字符集 |
| collation | 排序规则 |
| source | 创建方式，包括 manual （由 `create [global] binding` 生成）、capture（由 tidb 自动创建生成）和 evolve （由 tidb 自动演进生成） |

## 另请参阅

* [CREATE BINDING](/sql-statements/sql-statement-create-binding.md)
* [DROP BINDING](/sql-statements/sql-statement-drop-binding.md)
