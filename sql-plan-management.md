---
title: 执行计划管理 (SPM)
aliases: ['/docs-cn/dev/sql-plan-management/','/docs-cn/dev/reference/performance/execution-plan-bind/','/docs-cn/dev/execution-plan-binding/']
---

# 执行计划管理 (SPM)

执行计划管理，又称 SPM (SQL Plan Management)，是通过执行计划绑定，对执行计划进行人为干预的一系列功能，包括执行计划绑定、自动捕获绑定、自动演进绑定等。

## 执行计划绑定 (SQL Binding)

执行计划绑定是 SPM 的基础。在[优化器 Hints](/optimizer-hints.md) 中介绍了可以通过 Hint 的方式选择指定的执行计划，但有时需要在不修改 SQL 语句的情况下干预执行计划的选择。执行计划绑定功能使得可以在不修改 SQL 语句的情况下选择指定的执行计划。

### 创建绑定

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内为 SQL 绑定执行计划。目前支持的可创建执行计划绑定的 SQL 类型 (BindableStmt) 包括：`SELECT`，`DELETE`，`UPDATE` 和带有 `SELECT` 子查询的 `INSERT`/`REPLACE`。

其中，有两类特定的语法由于语法冲突不能创建执行计划绑定，例如：

```sql
-- 类型一：使用 `join` 关键字但不通过 `using` 关键字指定关联列的笛卡尔积
create global binding for
    select * from t t1 join t t2
using
    select * from t t1 join t t2;

-- 类型二：包含了 `using` 关键字的 `delete` 语句
create global binding for
    delete from t1 using t1 join t2 on t1.a = t2.a
using
    delete from t1 using t1 join t2 on t1.a = t2.a;
```

可以通过等价的 SQL 改写绕过这个语法冲突的问题。例如，上述两个例子可以改写为：

```sql
-- 类型一的第一种改写：为 `join` 关键字添加 `using` 子句
create global binding for
    select * from t t1 join t t2 using (a)
using
    select * from t t1 join t t2 using (a);

-- 类型一的第二种改写：去掉 `join` 关键字
create global binding for
    select * from t t1, t t2
using
    select * from t t1, t t2;

-- 类型二的改写：去掉 `delete` 语句中的 `using` 关键字
create global binding for
    delete t1 from t1 join t2 on t1.a = t2.a
using
    delete t1 from t1 join t2 on t1.a = t2.a;
```

> **注意：**
>
> 在对带 `SELECT` 子查询的 `INSERT`/`REPLACE` 语句创建执行计划绑定时，需要将想要绑定的优化器 Hints 指定在 `SELECT` 子查询中，而不是 `INSERT`/`REPLACE` 关键字后，不然优化器 Hints 不会生效。

例如：

```sql
-- Hint 能生效的用法
create global binding for
    insert into t1 select * from t2 where a > 1 and b = 1
using
    insert into t1 select /*+ use_index(@sel_1 t2, a) */ * from t2 where a > 1 and b = 1;

-- Hint 不能生效的用法
create global binding for
    insert into t1 select * from t2 where a > 1 and b = 1
using
    insert /*+ use_index(@sel_1 t2, a) */ into t1 select * from t2 where a > 1 and b = 1;
```

如果在创建执行计划绑定时不指定作用域，隐式作用域 SESSION 会被使用。TiDB 优化器会将被绑定的 SQL 进行“标准化”处理，然后存储到系统表中。在处理 SQL 查询时，只要“标准化”后的 SQL 和系统表中某个被绑定的 SQL 语句一致，并且系统变量 `tidb_use_plan_baselines` 的值为 `on`（其默认值为 `on`），即可使用相应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会从中选择代价最小的一个进行绑定。

`标准化`：把 SQL 中的常量变成变量参数，对空格和换行符等做标准化处理，并对查询引用到的表显式指定数据库。例如：

```sql
select * from t where a >    1
-- 标准化后：
select * from test . t where a > ?
```

值得注意的是，如果一条 SQL 语句在 GLOBAL 和 SESSION 作用域内都有与之绑定的执行计划，因为优化器在遇到 SESSION 绑定时会忽略 GLOBAL 绑定的执行计划，该语句在 SESSION 作用域内绑定的执行计划会屏蔽掉语句在 GLOBAL 作用域内绑定的执行计划。

例如：

```sql
-- 创建一个 global binding，指定其使用 sort merge join
create global binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ merge_join(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- 从该 SQL 的执行计划中可以看到其使用了 global binding 中指定的 sort merge join
explain select * from t1, t2 where t1.id = t2.id;

-- 创建另一个 session binding，指定其使用 hash join
create binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ hash_join(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- 从该 SQL 的执行计划中可以看到其使用了 session binding 中指定的 hash join，而不是 global binding 中指定的 sort merge join
explain select * from t1, t2 where t1.id = t2.id;
```

第一个 `select` 语句在执行时优化器会通过 GLOBAL 作用域内的绑定为其加上 `sm_join(t1, t2)` hint，`explain` 出的执行计划中最上层的节点为 MergeJoin。而第二个 `select` 语句在执行时优化器则会忽视 GLOBAL 作用域内的绑定而使用 SESSION 作用域内的绑定为该语句加上 `hash_join(t1, t2)` hint，`explain` 出的执行计划中最上层的节点为 HashJoin。

每个标准化的 SQL 只能同时有一个通过 `CREATE BINDING` 创建的绑定。对相同的标准化 SQL 创建多个绑定时，会保留最后一个创建的绑定，之前的所有绑定（创建的和演进出来的）都会被删除。但 session 绑定和 global 绑定仍然允许共存，不受这个逻辑影响。

另外，创建绑定时，TiDB 要求 session 处于某个数据库上下文中，也就是执行过 `use ${database}` 或者客户端连接时指定了数据库。

需要注意的是原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本必须相同，否则创建会失败，例如：

{{< copyable "sql" >}}

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE a > 2;
```

可以创建成功，因为原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本都是 `select * from test . t where a > ?`，而

{{< copyable "sql" >}}

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2;
```

则不可以创建成功，因为原始 SQL 在经过处理后是 `select * from test . t where a > ?`，而绑定 SQL 在经过处理后是 `select * from test . t where b > ?`。

> **注意：**
>
> 对于 `PREPARE`/`EXECUTE` 语句组，或者用二进制协议执行的查询，创建执行计划绑定的对象应当是查询语句本身，而不是 `PREPARE`/`EXECUTE` 语句。

### 删除绑定

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
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

在这里 SESSION 作用域内被删除掉的绑定会屏蔽 GLOBAL 作用域内相应的绑定，优化器不会为 `select` 语句添加 `sm_join(t1, t2)` hint，`explain` 给出的执行计划中最上层节点并不被 hint 固定为 MergeJoin，而是由优化器经过代价估算后自主进行选择。

> **注意：**
>
> 执行 `DROP GLOBAL BINDING` 会删除当前 tidb-server 实例缓存中的绑定，并将系统表中对应行的状态修改为 'deleted'。该语句不会直接删除系统表中的记录，因为其他 tidb-server 实例需要读取系统表中的 'deleted' 状态来删除其缓存中对应的绑定。对于这些系统表中状态为 'deleted' 的记录，后台线程每隔 100 个 `bind-info-lease`（默认值为 `3s`，合计 `300s`）会触发一次对 `update_time` 在 10 个 `bind-info-lease` 以前的绑定（确保所有 tidb-server 实例已经读取过这个 'deleted' 状态并更新完缓存）的回收清除操作。

### 查看绑定

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere];
```

该语句会按照绑定更新时间由新到旧的顺序输出 GLOBAL 或者 SESSION 作用域内的执行计划绑定，在不指定作用域时默认作用域为 SESSION。目前 `SHOW BINDINGS` 会输出 8 列，具体如下：

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

### 排查绑定

{{< copyable "sql" >}}

```sql
SELECT [SESSION] @@last_plan_from_binding;
```

该语句使用系统变量 [last_plan_from_binding](https://docs.pingcap.com/zh/tidb/stable/system-variables#last_plan_from_binding-%E4%BB%8E-v40-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) 显示上一条执行的语句所使用的执行计划是否来自 binding 的执行计划。

另外，当使用 `explain format = 'verbose'`  语句查看一条 SQL 语句的查询计划时，如果该 SQL 语句使用了 binding，`explain` 语句会输出 warning 警告。此时可以通过查看 warning 了解该 SQL 语句使用了哪一条 binding。

```
-- 创建一个 global binding
create global binding for
    select * from t
using
    select * from t;

-- 使用 explain format = 'verbose' 
语句查看 SQL 的执行计划，通过查看 warning 信息确认查询所使用的 binding
explain format = 'verbose' select * from t;
show warnings;
```

## 自动捕获绑定 (Baseline Capturing)

通过将 `tidb_capture_plan_baselines` 的值设置为 `on`（其默认值为 `off`）可以打开自动捕获绑定功能。

> **注意：**
>
> 自动绑定功能依赖于 [Statement Summary](/statement-summary-tables.md)，因此在使用自动绑定之前需打开 Statement Summary 开关。

开启自动绑定功能后，每隔 `bind-info-lease`（默认值为 `3s`）会遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动捕获绑定。绑定的执行计划为 Statement Summary 中记录执行这条语句时使用的执行计划。

对于以下几种 SQL 语句，TiDB 不会自动捕获绑定：

- EXPLAIN 和 EXPLAIN ANALYZE 语句；
- TiDB 内部执行的 SQL 语句，比如统计信息自动加载使用的 SELECT 查询；
- 存在手动创建的执行计划绑定的 SQL 语句；

对于 `PREPARE`/`EXECUTE` 语句组，或通过二进制协议执行的查询，TiDB 会为真正的查询（而不是 `PREPARE`/`EXECUTE` 语句）自动捕获绑定。

> **注意：**
>
> 由于 TiDB 存在一些内嵌 SQL 保证一些功能的正确性，所以自动捕获绑定时会默认屏蔽内嵌 SQL。

## 自动演进绑定 (Baseline Evolution)

自动演进绑定，在 TiDB 4.0 版本引入，是执行计划管理的重要功能之一。

由于某些数据变更后，原先绑定的执行计划可能是一个不优的计划。为了解决该问题，引入自动演进绑定功能来自动优化已经绑定的执行计划。

另外自动演进绑定还可以一定程度上避免统计信息改动后，对执行计划带来的抖动。

### 使用方式

通过以下语句可以开启自动演进绑定功能：

{{< copyable "sql" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

`tidb_evolve_plan_baselines` 的默认值为 `off`。

> **注意：**
>
> 自动演进功能目前为实验特性，存在未知风险并需要继续优化，不建议在生产环境中使用。此开关将被禁用直到该功能到达 GA (Generally Available) 状态，如果尝试打开开关，会产生报错。如果你已经在生产环境中使用了此功能，请尽快将它关闭，如发现 Binding 状态不如预期，请与 PingCAP 的技术支持联系获取相关支持。

在打开自动演进功能后，如果优化器选出的最优执行计划不在之前绑定的执行计划之中，会将其记录为待验证的执行计划。每隔 `bind-info-lease`（默认值为 `3s`），会选出一个待验证的执行计划，将其和已经绑定的执行计划中代价最小的比较实际运行时间。如果待验证的运行时间更优的话（目前判断标准是运行时间小于等于已绑定执行计划运行时间的 2/3），会将其标记为可使用的绑定。以下示例描述上述过程。

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

为了减少自动演进对集群的影响，可以通过设置 `tidb_evolve_plan_task_max_time` 来限制每个执行计划运行的最长时间，其默认值为 `600s`。实际在验证执行计划时，计划的最长运行时间还会被限制为不超过已验证执行计划的运行时间的两倍；通过 `tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time` 可以限制运行演进任务的时间窗口，默认值分别为 `00:00 +0000` 和 `23:59 +0000`。

### 注意事项

由于自动演进绑定会自动地创建新的绑定，当查询的环境发生变动时，自动创建的绑定可能会有多种行为的选择。这里列出一些注意事项：

+ 自动演进只会对存在至少一个 global 绑定的标准化 SQL 进行演进。

+ 由于创建新的绑定会删除之前所有绑定（对于一条标准化 SQL），自动演进的绑定也会在手动重新创建绑定后被删除。

+ 所有和计算过程相关的 hint，在演进时都会被保留。计算过程相关的 hint 有如下几种：

    | Hint | 说明            |
    | :-------- | :------------- |
    | memory_quota |  查询过程最多可以使用多少内存 |
    | use_toja | 优化器是否考虑把子查询转化为 join |
    | use_cascades | 是否使用 cascades 优化器 |
    | no_index_merge | 优化器是否考虑将 index merge 作为一个读表选项 |
    | read_consistent_replica | 是否强制读表时使用 follower read |
    | max_execution_time | 查询过程最多消耗多少时间 |

+ `read_from_storage` 是一个非常特别的 hint，因为它指定了读表时选择从 TiKV 读还是从 TiFlash 读。由于 TiDB 提供隔离读的功能，当隔离条件变化时，这个 hint 对演进出来的执行计划影响很大，所以当最初创建的绑定中存在这个 hint，TiDB 会无视其所有演进的绑定。
