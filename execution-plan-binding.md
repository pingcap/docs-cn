---
title: 执行计划绑定
category: reference
aliases: ['/docs-cn/dev/reference/performance/execution-plan-bind/']
---

# 执行计划绑定

在[优化器 Hints](/optimizer-hints.md) 中介绍了可以通过 Hint 的方式选择指定的执行计划，但有的时候需要在不修改 SQL 语句的情况下干预执行计划的选择。执行计划绑定提供了一系列功能使得可以在不修改 SQL 语句的情况下选择指定的执行计划。

## 语法

### 创建绑定

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR SelectStmt USING SelectStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内为 SQL 绑定执行计划。在不指定作用域时，隐式作用域为 SESSION。被绑定的 SQL 会被参数化后存储到系统表中。在处理 SQL 查询时，只要参数化后的 SQL 和系统表中某个被绑定的 SQL 语句一致，并且系统变量 `tidb_use_plan_baselines` 的值为 `on`（其默认值为 `on`），即可使用相应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会从中选择代价最小的一个进行绑定。

值得注意的是当一条 SQL 语句在 GLOBAL 和 SESSION 作用域内都有与之绑定的执行计划时，因为优化器在遇到 SESSION 绑定时会将 GLOBAL 绑定的执行计划丢弃，该语句在 SESSION 作用域内绑定的执行计划会屏蔽掉语句在 GLOBAL 作用域内绑定的执行计划。

例如：

```sql
--  创建一个 global binding，指定其使用 sort merge join
create global binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ TIDB_SMJ(t1, t2) */ * from t1, t2 where t1.id = t2.id;
    
-- 从该 SQL 的执行计划中可以看到其使用了 global binding 中指定的 sort merge join
explain select * from t1, t2 where t1.id = t2.id;

-- 创建另一个 session binding，指定其使用 hash join
create binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ TIDB_HJ(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- 从该 SQL 的执行计划中可以看到其使用了 session binding 中指定的 hash join，而不是 global binding 中指定的 sort merge join
explain select * from t1, t2 where t1.id = t2.id;
```

第一个 `select` 语句在执行时优化器会通过 GLOBAL 作用域内的绑定为其加上 `TIDB_SMJ(t1, t2)` hint，`explain` 出的执行计划中最上层的节点为 MergeJoin。而第二个 `select` 语句在执行时优化器则会忽视 GLOBAL 作用域内的绑定而使用 SESSION 作用域内的绑定为该语句加上 `TIDB_HJ(t1, t2)` hint，`explain` 出的执行计划中最上层的节点为 HashJoin。

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

一般来说，SESSION 作用域的绑定主要用于测试或在某些特殊情况下使用。若需要集群中所有的 TiDB 进程都生效，则需要使用 GLOBAL 作用域的绑定。SESSION 作用域对 GLOBAL 作用域绑定的屏蔽效果会持续到该 SESSION 结束。

承接上面关于 SESSION 绑定屏蔽 GLOBAL 绑定的例子，继续执行：

```sql
-- 删除 session 中创建的 binding
drop session binding for select * from t1, t2 where t1.id = t2.id;

-- 重新查看该 SQL 的执行计划
explain select * from t1,t2 where t1.id = t2.id;
```

在这里 SESSION 作用域内被删除掉的绑定会屏蔽 GLOBAL 作用域内相应的绑定，优化器不会为 `select` 语句添加 `TIDB_SMJ(t1, t2)` hint，`explain` 给出的执行计划中最上层节点并不被 hint 固定为 MergeJoin，而是由优化器经过代价估算后自主进行选择。

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
> 自动绑定功能依赖于 [Statement Summary](/statement-summary-tables.md)，因此在使用自动绑定之前需打开 Statement Summary 开关。

开启自动绑定功能后，每隔 `bind-info-lease`（默认值为 `3s`）会遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动创建绑定。

### 自动演进绑定

随着数据的变更，有可能原先绑定的执行计划已经不是最优的了，自动演进绑定功能可以自动优化已经绑定的执行计划。通过以下语句可以开启自动演进绑定功能：

{{< copyable "sql" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

`tidb_evolve_plan_baselines` 的默认值为 `off`。

> **注意：**
>
> 设置 global 系统变量在当前 session 并不会生效，只会在新创建的 session 生效。可以将 global 关键字替换为 session 使当前 session 开启演进功能。

在打开自动演进功能后，如果优化器选出的最优执行计划不在之前绑定的执行计划之中，会将其记录为待验证的执行计划。每隔 `bind-info-lease`（默认值为 `3s`），会选出一个待验证的执行计划，将其和已经绑定的执行计划中代价最小的比较实际运行时间。如果待验证的运行时间更优的话，会将其标记为可使用的绑定。以下示例描述上述过程。

假如有表 `t` 定义如下：

{{< copyable "sql" >}}

```sql
create table t(a int, b int, key(a), key(b));
```

在表 `t` 上进行如下查询：

{{< copyable "sql" >}}

```sql
select * from t where a < 100 and b < 100;
```

表上满足条件 `a < 100` 的行很少。但由于某些原因，优化器没能选中使用索引 `a` 这个最优执行计划，而是误选了速度慢的全表扫，那么用户首先可以通过如下语句创建一个绑定：

{{< copyable "sql" >}}

```sql
create global binding for select * from t where a < 100 and b < 100 using select * from t use index(a) where a < 100 and b < 100;
```

当以上查询语句再次执行时，优化器会在刚创建绑定的干预下选择使用索引 `a`，进而降低查询时间。

假如随着在表中进行插入和修改，表中满足条件 `a < 100` 的行变得越来越多，而满足条件 `b < 100` 的行变得越来越少，这时再在绑定的干预下使用索引 `a` 可能就不是最优了。

绑定的演进可以解决这类问题。当优化器感知到表数据变化后，会对这条查询生成使用索引 `b` 的执行计划。但由于绑定的存在，这个执行计划不会被采纳和执行，不过它会被存在后台的演进列表里。在演进过程中，如果它被验证为执行时间明显低于使用索引 `a` 的执行时间（即当前绑定的执行计划），那么索引 `b` 会被加入到可用的绑定列表中。在此之后，当这条查询再次被执行时，优化器首先生成使用索引 `b` 的执行计划，并确认它在绑定列表中，所以会采纳它并执行，进而可以在数据变化后降低这条查询的执行时间。

为了减少自动演进对集群的影响，可以通过 `tidb_evolve_plan_task_max_time` 来限制每个执行计划运行的最长时间，其默认值为 `600s`；通过 `tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time` 可以限制运行演进任务的时间窗口，默认值分别为 `00:00 +0000` 和 `23:59 +0000`。
