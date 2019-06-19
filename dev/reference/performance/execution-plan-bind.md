---
title: 执行计划绑定
category: reference
aliases: ['/docs-cn/sql/execution-plan-bind/']
---

# 执行计划绑定

在[优化器 Hints](/dev/reference/performance/optimizer-hints.md) 中介绍了可以通过 Hint 的方式选择指定的执行计划，但有的时候需要在不修改 SQL 语句的情况下干预执行计划的选择。执行计划绑定提供了一系列功能使得可以在不修改 SQL 语句的情况下选择指定的执行计划。

## 语法

### 创建绑定

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt
```

该语句可以在 GLOBAL 或者 SESSION 作用域内为 SQL 绑定执行计划。在不指定作用域时，隐式作用域为 SESSION。被绑定的 SQL 会被参数化后存储到系统表中。在处理 SQL 查询时，只要参数化后的 SQL 和系统表中某个被绑定的 SQL 一致即可使用相应的优化器 Hint。

`参数化`：把 SQL 中的常量变成变量参数，并对 SQL 中的空格和换行符等做标准化处理。例如：

```sql
select * from t where a >    1
-- 参数化后：
select * from t where a > ？
```

需要注意的是原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本必须相同，否则创建会失败，例如：

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE a > 2
```

可以创建成功，因为原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本都是 `select * from t where a > ?`，而

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
```

则不可以创建成功，因为原始 SQL 在经过处理后是 `select * from t where a > ?`，而绑定 SQL 在经过处理后是 `select * from t where b > ?`。

### 删除绑定

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt
```

该语句可以在 GLOBAL 或者 SESSION 作用域内删除指定的执行计划绑定，在不指定作用域时默认作用域为 SESSION。

### 查看绑定

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

该语句会输出 GLOBAL 或者 SESSION 作用域内的执行计划绑定，在不指定作用域时默认作用域为 SESSION。目前 `SHOW BINDINGS` 会输出 8 列，具体如下：

| 列名 | 说明            |
| -------- | ------------- |
| original_sql  |  参数化后的原始 SQL |
| bind_sql | 带 Hint 的绑定 SQL |
| default_db | 默认数据库名 |
| status | 状态，包括 using（正在使用）、deleted（已删除）和 invalid（无效）|
| create_time | 创建时间 |
| update_time | 更新时间 |
| charset | 字符集 |
| collation | 排序规则 |
