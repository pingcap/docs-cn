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

该语句可以在全局或者 SESSION 作用域内创建执行计划绑定。原始 SQL 会被参数化后存储下来，后续查询语句只需和原始 SQL 在参数化后一致即可使用在绑定 SQL 上添加的 Hint。

需要注意的是原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本必须相同，否则创建会失败。

### 删除绑定

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt
```

该语句可以在全局或者 SESSION 作用域内删除指定的执行计划绑定。

### 查看绑定

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

该语句会输出全局或者 SESSION 作用域内的执行计划绑定。目前 `SHOW BINDINGS` 会输出 8 列，具体如下：

| 语法元素 | 说明            |
| -------- | ------------- |
| original_sql  |  参数化后的原始 SQL |
| bind_sql | 带 Hint 的绑定 SQL |
| default_db | 默认数据库名 |
| status | 状态，包括正在使用和已删除 |
| create_time | 创建时间 |
| update_time | 更新时间 |
| charset | 字符集 |
| collation | 排序规则 |
