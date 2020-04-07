---
title: 执行计划绑定
category: reference
---

# 执行计划绑定

在[优化器 Hints](/reference/performance/optimizer-hints.md) 中介绍了可以通过 Hint 的方式选择指定的执行计划，但有的时候需要在不修改 SQL 语句的情况下干预执行计划的选择。执行计划绑定提供了一系列功能使得可以在不修改 SQL 语句的情况下选择指定的执行计划。

## 语法

### 创建绑定

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内为 SQL 绑定执行计划。在不指定作用域时，隐式作用域为 SESSION。被绑定的 SQL 会被参数化后存储到系统表中。在处理 SQL 查询时，只要参数化后的 SQL 和系统表中某个被绑定的 SQL 语句一致，并且系统变量 `tidb_use_plan_baselines` 的值为 `on`（其默认值为 `on`），即可使用相应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会从中选择代价最小的一个进行绑定。

`参数化`：把 SQL 中的常量变成变量参数，并对 SQL 中的空格和换行符等做标准化处理。例如：

```sql
select * from t where a >    1
-- 参数化后：
select * from t where a > ？
```

需要注意的是原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本必须相同，否则创建会失败，例如：

{{< copyable "sql" >}}

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE a > 2;
```

可以创建成功，因为原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本都是 `select * from t where a > ?`，而

{{< copyable "sql" >}}

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2;
```

则不可以创建成功，因为原始 SQL 在经过处理后是 `select * from t where a > ?`，而绑定 SQL 在经过处理后是 `select * from t where b > ?`。

### 删除绑定

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR SelectStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内删除指定的执行计划绑定，在不指定作用域时默认作用域为 SESSION。

### 查看绑定

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere];
```

该语句会输出 GLOBAL 或者 SESSION 作用域内的执行计划绑定，在不指定作用域时默认作用域为 SESSION。目前 `SHOW BINDINGS` 会输出 8 列，具体如下：

| 列名 | 说明            |
| -------- | ------------- |
| original_sql  |  参数化后的原始 SQL |
| bind_sql | 带 Hint 的绑定 SQL |
| default_db | 默认数据库名 |
| status | 状态，包括 using（正在使用）、deleted（已删除）和 invalid（无效） |
| create_time | 创建时间 |
| update_time | 更新时间 |
| charset | 字符集 |
| collation | 排序规则 |

### 自动创建绑定

通过将 `tidb_capture_plan_baselines` 的值设置为 `on`（其默认值为 `off`）可以打开自动创建绑定功能。

> **注意：**
>
> 自动绑定功能依赖于 [Statement Summary](/reference/performance/statement-summary.md)，因此在使用自动绑定之前需打开 Statement Summary 开关。

开启自动绑定功能后，每隔 `bind-info-lease`（默认值为 `3s`）会遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动创建绑定。

### 自动演进绑定

随着数据的变更，有可能原先绑定的执行计划已经不是最优的了，自动演进绑定功能可以自动优化已经绑定的执行计划。

{{< copyable "sql" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

`tidb_evolve_plan_baselines` 的默认值为 `off`。

在打开自动演进功能后，如果优化器选出的最优执行计划不在之前绑定的执行计划之中，会将其记录为待验证的执行计划。每隔 `bind-info-lease`（默认值为 `3s`），会选出一个待验证的执行计划，将其和已经绑定的执行计划中代价最小的比较实际运行时间。如果待验证的运行时间更优的话，会将其标记为可使用的绑定。

为了减少自动演进对集群的影响，可以通过 `tidb_evolve_plan_task_max_time` 来限制每个执行计划运行的最长时间，其默认值为 `600s`；通过 `tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time` 可以限制运行演进任务的时间窗口，默认值分别为 `00:00 +0000` 和 `23:59 +0000`。
