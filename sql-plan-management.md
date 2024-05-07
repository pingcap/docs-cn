---
title: 执行计划管理 (SPM)
---

# 执行计划管理 (SPM)

执行计划管理，又称 SPM (SQL Plan Management)，是通过执行计划绑定，对执行计划进行人为干预的一系列功能，包括执行计划绑定、自动捕获绑定、自动演进绑定等。

## 执行计划绑定 (SQL Binding)

执行计划绑定是 SPM 的基础。在[优化器 Hints](/optimizer-hints.md) 中介绍了可以通过 Hint 的方式选择指定的执行计划，但有时需要在不修改 SQL 语句的情况下干预执行计划的选择。执行计划绑定功能使得可以在不修改 SQL 语句的情况下选择指定的执行计划。

> **注意：**
>
> 要使用执行计划绑定，你需要拥有 `SUPER` 权限。如果在使用过程中系统提示权限不足，可参考[权限管理](/privilege-management.md)补充所需权限。

### 创建绑定

你可以根据 SQL 或者历史执行计划为指定的 SQL 语句创建绑定。

#### 根据 SQL 创建绑定

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING [FOR BindableStmt] USING BindableStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内为 SQL 绑定执行计划。目前，可创建执行计划绑定的 SQL 语句类型 (BindableStmt) 包括：`SELECT`、`DELETE`、`UPDATE` 和带有 `SELECT` 子查询的 `INSERT`/`REPLACE`。使用示例如下：

```sql
CREATE GLOBAL BINDING USING SELECT * /*+ use_index(t1, a) */ FROM t1;
CREATE GLOBAL BINDING FOR SELECT * FROM t1 USING SELECT * /*+ use_index(t1, a) */ FROM t1;
```

> **注意：**
>
> 绑定的优先级高于手工添加的 Hint，即在有绑定的时候执行带有 Hint 的语句时，该语句中控制优化器行为的 Hint 不会生效，但是其他类别的 Hint 仍然能够生效。

其中，有两类特定的语法由于语法冲突不能创建执行计划绑定，例如：

```sql
-- 类型一：使用 `JOIN` 关键字但不通过 `USING` 关键字指定关联列的笛卡尔积
CREATE GLOBAL BINDING for
    SELECT * FROM t t1 JOIN t t2
USING
    SELECT * FROM t t1 JOIN t t2;

-- 类型二：包含了 `USING` 关键字的 `delete` 语句
CREATE GLOBAL BINDING for
    delete FROM t1 USING t1 JOIN t2 ON t1.a = t2.a
USING
    delete FROM t1 USING t1 JOIN t2 ON t1.a = t2.a;
```

可以通过等价的 SQL 改写绕过这个语法冲突的问题。例如，上述两个例子可以改写为：

```sql
-- 类型一的第一种改写：为 `JOIN` 关键字添加 `USING` 子句
CREATE GLOBAL BINDING for
    SELECT * FROM t t1 JOIN t t2 USING (a)
USING
    SELECT * FROM t t1 JOIN t t2 USING (a);

-- 类型一的第二种改写：去掉 `JOIN` 关键字
CREATE GLOBAL BINDING for
    SELECT * FROM t t1, t t2
USING
    SELECT * FROM t t1, t t2;

-- 类型二的改写：去掉 `delete` 语句中的 `USING` 关键字
CREATE GLOBAL BINDING for
    delete t1 FROM t1 JOIN t2 ON t1.a = t2.a
USING
    delete t1 FROM t1 JOIN t2 ON t1.a = t2.a;
```

> **注意：**
>
> 在对带 `SELECT` 子查询的 `INSERT`/`REPLACE` 语句创建执行计划绑定时，需要将想要绑定的优化器 Hints 指定在 `SELECT` 子查询中，而不是 `INSERT`/`REPLACE` 关键字后，不然优化器 Hints 不会生效。

例如：

```sql
-- Hint 能生效的用法
CREATE GLOBAL BINDING for
    INSERT INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1
USING
    INSERT INTO t1 SELECT /*+ use_index(@sel_1 t2, a) */ * FROM t2 WHERE a > 1 AND b = 1;

-- Hint 不能生效的用法
CREATE GLOBAL BINDING for
    INSERT INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1
USING
    INSERT /*+ use_index(@sel_1 t2, a) */ INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1;
```

如果在创建执行计划绑定时不指定作用域，隐式作用域 SESSION 会被使用。TiDB 优化器会将被绑定的 SQL 进行“标准化”处理，然后存储到系统表中。在处理 SQL 查询时，只要“标准化”后的 SQL 和系统表中某个被绑定的 SQL 语句一致，并且系统变量 [`tidb_use_plan_baselines`](/system-variables.md#tidb_use_plan_baselines-从-v40-版本开始引入) 的值为 `on`（其默认值为 `on`），即可使用相应的优化器 Hint。如果存在多个可匹配的执行计划，优化器会从中选择代价最小的一个进行绑定。

`标准化`：把 SQL 中的常量变成变量参数，对空格和换行符等做标准化处理，并对查询引用到的表显式指定数据库。例如：

```sql
SELECT * FROM t WHERE a >    1
-- 以上语句标准化后如下：
SELECT * FROM test . t WHERE a > ?
```

> **注意：**
>
> 在进行标准化的时候，`IN` 表达式中的 `?` 会被标准化为 `...`。
>
> 例如：
>
> ```sql
> SELECT * FROM t WHERE a IN (1)
> SELECT * FROM t WHERE a IN (1,2,3)
> -- 以上语句标准化后如下：
> SELECT * FROM test . t WHERE a IN ( ... )
> SELECT * FROM test . t WHERE a IN ( ... )
> ```
>
> 不同长度的 `IN` 表达式被标准化后，会被识别为同一条语句，因此只需要创建一条绑定，对这些表达式同时生效。
>
> 例如：
>
> ```sql
> CREATE TABLE t (a INT, KEY(a));
> CREATE BINDING FOR SELECT * FROM t WHERE a IN (?) USING SELECT /*+ use_index(t, a) */ * FROM t WHERE a in (?);
> 
> SELECT * FROM t WHERE a IN (1);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
>
> SELECT * FROM t WHERE a IN (1, 2, 3);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
> ```
> 
> 在 v7.4.0 之前版本的 TiDB 集群中创建的绑定可能会包含 `IN (?)`，在升级到 v7.4.0 或更高版本后，这些绑定会被统一修改为 `IN (...)`。
> 
> 例如：
>
> ```sql
> -- 在 v7.3.0 集群上创建绑定
> mysql> CREATE GLOBAL BINDING FOR SELECT * FROM t WHERE a IN (1) USING SELECT /*+ use_index(t, a) */ * FROM t WHERE a IN (1);
> mysql> SHOW GLOBAL BINDINGS;
> +-----------------------------------------------+--------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                  | Bind_sql                                                           | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
> +-----------------------------------------------+--------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ? ) | SELECT /*+ use_index(`t` `a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2023-10-20 14:28:10.093 | 2023-10-20 14:28:10.093 | utf8    | utf8_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-----------------------------------------------+--------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
> 
> -- 升级到 v7.4.0 或更高的版本后
> mysql> SHOW GLOBAL BINDINGS;
> +-------------------------------------------------+--------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                           | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+--------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ... ) | SELECT /*+ use_index(`t` `a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2023-10-20 14:28:10.093 | 2023-10-20 14:28:10.093 | utf8    | utf8_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-------------------------------------------------+--------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
> ```

值得注意的是，如果一条 SQL 语句在 GLOBAL 和 SESSION 作用域内都有与之绑定的执行计划，因为优化器在遇到 SESSION 绑定时会忽略 GLOBAL 绑定的执行计划，该语句在 SESSION 作用域内绑定的执行计划会屏蔽掉语句在 GLOBAL 作用域内绑定的执行计划。

例如：

```sql
-- 创建一个 global binding，指定其使用 sort merge join
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 从该 SQL 的执行计划中可以看到其使用了 global binding 中指定的 sort merge join
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 创建另一个 session binding，指定其使用 hash join
CREATE BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ hash_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 从该 SQL 的执行计划中可以看到其使用了 session binding 中指定的 hash join，而不是 global binding 中指定的 sort merge join
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

第一个 `SELECT` 语句在执行时优化器会通过 GLOBAL 作用域内的绑定为其加上 `sm_join(t1, t2)` hint，`explain` 出的执行计划中最上层的节点为 MergeJoin。而第二个 `SELECT` 语句在执行时优化器则会忽视 GLOBAL 作用域内的绑定而使用 SESSION 作用域内的绑定为该语句加上 `hash_join(t1, t2)` hint，`explain` 出的执行计划中最上层的节点为 HashJoin。

每个标准化的 SQL 只能同时有一个通过 `CREATE BINDING` 创建的绑定。对相同的标准化 SQL 创建多个绑定时，会保留最后一个创建的绑定，之前的所有绑定（创建的和演进出来的）都会被删除。但 session 绑定和 global 绑定仍然允许共存，不受这个逻辑影响。

另外，创建绑定时，TiDB 要求 session 处于某个数据库上下文中，也就是执行过 `use ${database}` 或者客户端连接时指定了数据库。

需要注意的是原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本必须相同，否则创建会失败，例如：

{{< copyable "sql" >}}

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE a > 2;
```

可以创建成功，因为原始 SQL 和绑定 SQL 在参数化以及去掉 Hint 后文本都是 `SELECT * FROM test . t WHERE a > ?`，而

{{< copyable "sql" >}}

```sql
CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2;
```

则不可以创建成功，因为原始 SQL 在经过处理后是 `SELECT * FROM test . t WHERE a > ?`，而绑定 SQL 在经过处理后是 `SELECT * FROM test . t WHERE b > ?`。

> **注意：**
>
> 对于 `PREPARE`/`EXECUTE` 语句组，或者用二进制协议执行的查询，创建执行计划绑定的对象应当是查询语句本身，而不是 `PREPARE`/`EXECUTE` 语句。

#### 根据历史执行计划创建绑定

如需将 SQL 语句的执行计划固定为之前使用过的执行计划，可以使用 `plan_digest` 为该 SQL 语句绑定一个历史的执行计划。相比于使用 SQL 创建绑定的方式，此方式更加简便。

以下为根据历史执行计划创建绑定的注意事项：

- 该功能是根据历史的执行计划生成 hint 而实现的绑定，历史的执行计划来源是 [Statement Summary Tables](/statement-summary-tables.md)，因此在使用此功能之前需开启系统变量 [`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-从-v304-版本开始引入)。
- 对于包含子查询的查询、访问 TiFlash 的查询、3 张表或更多表进行 Join 的查询，自动生成的 hint 不够完备，可能导致无法完全固定住计划，对于这类情况在创建时会产生告警。
- 原执行计划对应 SQL 语句中的 hint 也会被应用在创建的绑定中，如执行 `SELECT /*+ max_execution_time(1000) */ * FROM t` 后，使用其 `plan_digest` 创建的绑定中会带上 `max_execution_time(1000)`。

使用方式:

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST 'plan_digest';
```

该语句使用 `plan_digest` 为 SQL 语句绑定执行计划，在不指定作用域时默认作用域为 SESSION。所创建绑定的适用 SQL、优先级、作用域、生效条件等与[根据 SQL 创建绑定](#根据-sql-创建绑定)相同。

使用此绑定方式时，你需要先从 `statements_summary` 中找到需要绑定的执行计划对应的 `plan_digest`，再通过 `plan_digest` 创建绑定。具体步骤如下：

1. 从 `Statement Summary Tables` 的记录中查找执行计划对应的 `plan_digest`。

    例如:

    ```sql
    CREATE TABLE t(id INT PRIMARY KEY , a INT, KEY(a));
    SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1;
    SELECT * FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE QUERY_SAMPLE_TEXT = 'SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1'\G
    ```

    以下为 `statements_summary` 部分查询结果：

    ```
    SUMMARY_BEGIN_TIME: 2022-12-01 19:00:00
    ...........
          DIGEST_TEXT: select * from `t` where `a` = ?
    ...........
          PLAN_DIGEST: 4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb
                 PLAN:  id                  task        estRows operator info                           actRows execution info                                                                                                                                             memory      disk
                        TableReader_7       root        10      data:Selection_6                        0       time:4.05ms, loops:1, cop_task: {num: 1, max: 598.6µs, proc_keys: 0, rpc_num: 2, rpc_time: 609.8µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}   176 Bytes   N/A
                        └─Selection_6       cop[tikv]   10      eq(test.t.a, 1)                         0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
                          └─TableFullScan_5 cop[tikv]   10000   table:t, keep order:false, stats:pseudo 0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
          BINARY_PLAN: 6QOYCuQDCg1UYWJsZVJlYWRlcl83Ev8BCgtTZWxlY3Rpb25fNhKOAQoPBSJQRnVsbFNjYW5fNSEBAAAAOA0/QSkAAQHwW4jDQDgCQAJKCwoJCgR0ZXN0EgF0Uh5rZWVwIG9yZGVyOmZhbHNlLCBzdGF0czpwc2V1ZG9qInRpa3ZfdGFzazp7dGltZTo1NjAuOMK1cywgbG9vcHM6MH1w////CQMEAXgJCBD///8BIQFzCDhVQw19BAAkBX0QUg9lcSgBfCAudC5hLCAxKWrmYQAYHOi0gc6hBB1hJAFAAVIQZGF0YTo9GgRaFAW4HDQuMDVtcywgCbYcMWKEAWNvcF8F2agge251bTogMSwgbWF4OiA1OTguNsK1cywgcHJvY19rZXlzOiAwLCBycGNfBSkAMgkMBVcQIDYwOS4pEPBDY29wcl9jYWNoZV9oaXRfcmF0aW86IDAuMDAsIGRpc3RzcWxfY29uY3VycmVuY3k6IDE1fXCwAXj///////////8BGAE=
    ```

    可以看到执行计划对应的 `plan_digest` 为 `4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`。

2. 使用 `plan_digest` 创建绑定。

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

创建完毕后可以[查看绑定](#查看绑定)，验证绑定是否生效。

```sql
SHOW BINDINGS\G
```

```
*************************** 1. row ***************************
Original_sql: select * from `test` . `t` where `a` = ?
    Bind_sql: SELECT /*+ use_index(@`sel_1` `test`.`t` ) ignore_index(`t` `a`)*/ * FROM `test`.`t` WHERE `a` = 1
       ...........
  Sql_digest: 6909a1bbce5f64ade0a532d7058dd77b6ad5d5068aee22a531304280de48349f
 Plan_digest:
1 row in set (0.01 sec)

ERROR:
No query specified
```

```sql
SELECT * FROM t WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
```

```
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.00 sec)
```

### 删除绑定

你可以根据 SQL 语句或者 `sql_digest` 删除绑定。

#### 根据 SQL 语句删除绑定

{{< copyable "sql" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

该语句可以在 GLOBAL 或者 SESSION 作用域内删除指定的执行计划绑定，在不指定作用域时默认作用域为 SESSION。

一般来说，SESSION 作用域的绑定主要用于测试或在某些特殊情况下使用。若需要集群中所有的 TiDB 进程都生效，则需要使用 GLOBAL 作用域的绑定。SESSION 作用域对 GLOBAL 作用域绑定的屏蔽效果会持续到该 SESSION 结束。

承接上面关于 SESSION 绑定屏蔽 GLOBAL 绑定的例子，继续执行：

```sql
-- 删除 session 中创建的 binding
DROP session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 重新查看该 SQL 的执行计划
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

在这里 SESSION 作用域内被删除掉的绑定会屏蔽 GLOBAL 作用域内相应的绑定，优化器不会为 `SELECT` 语句添加 `sm_join(t1, t2)` hint，`explain` 给出的执行计划中最上层节点并不被 hint 固定为 MergeJoin，而是由优化器经过代价估算后自主进行选择。

#### 根据 `sql_digest` 删除绑定

除了可以根据 SQL 语句删除对应的绑定以外，也可以根据 `sql_digest` 删除绑定：

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST 'sql_digest';
```

该语句用于在 GLOBAL 或者 SESSION 作用域内删除 `sql_digest` 对应的的执行计划绑定，在不指定作用域时默认作用域为 SESSION。你可以通过[查看绑定](#查看绑定)语句获取 `sql_digest`。

> **注意：**
>
> 执行 `DROP GLOBAL BINDING` 会删除当前 tidb-server 实例缓存中的绑定，并将系统表中对应行的状态修改为 'deleted'。该语句不会直接删除系统表中的记录，因为其他 tidb-server 实例需要读取系统表中的 'deleted' 状态来删除其缓存中对应的绑定。对于这些系统表中状态为 'deleted' 的记录，后台线程每隔 100 个 `bind-info-lease`（默认值为 `3s`，合计 `300s`）会触发一次对 `update_time` 在 10 个 `bind-info-lease` 以前的绑定（确保所有 tidb-server 实例已经读取过这个 'deleted' 状态并更新完缓存）的回收清除操作。

### 变更绑定状态

#### 根据 SQL 语句变更绑定状态

{{< copyable "sql" >}}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

该语句可以在 GLOBAL 作用域内变更指定执行计划的绑定状态，默认作用域为 GLOBAL，该作用域不可更改。

使用时，只能将 `Disabled` 的绑定改为 `Enabled` 状态，或将 `Enabled` 的绑定改为 `Disabled` 状态。如果没有可以改变状态的绑定，则会输出一条内容为 `There are no bindings can be set the status. Please check the SQL text` 的警告。需要注意的是，当绑定被设置成 `Disabled` 状态时，查询语句不会使用该绑定。

#### 根据 `sql_digest` 变更绑定状态

除了可以根据 SQL 语句变更对应的绑定状态以外，也可以根据 `sql_digest` 变更绑定状态：

```sql
SET BINDING [ENABLED | DISABLED] FOR SQL DIGEST 'sql_digest';
```

使用 `sql_digest` 所能变更的绑定状态和生效情况与[根据 SQL 语句变更绑定状态](#根据-sql-语句变更绑定状态)相同。如果没有可以改变状态的绑定，则会输出一条内容为 `can't find any binding for 'sql_digest'` 的警告。

### 查看绑定

{{< copyable "sql" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere];
```

该语句会按照绑定更新时间由新到旧的顺序输出 GLOBAL 或者 SESSION 作用域内的执行计划绑定，在不指定作用域时默认作用域为 SESSION。目前 `SHOW BINDINGS` 会输出 11 列，具体如下：

| 列名 | 说明            |
| -------- | ------------- |
| original_sql  |  参数化后的原始 SQL |
| bind_sql | 带 Hint 的绑定 SQL |
| default_db | 默认数据库名 |
| status | 状态，包括 enabled（可用，从 v6.0 开始取代之前版本的 using 状态）、disabled（不可用）、deleted（已删除）、 invalid（无效）、rejected（演进时被拒绝）和 pending verify（等待演进验证） |
| create_time | 创建时间 |
| update_time | 更新时间 |
| charset | 字符集 |
| collation | 排序规则 |
| source | 创建方式，包括 manual（根据 SQL 创建绑定生成）、history（根据历史执行计划创建绑定生成）、capture（由 TiDB 自动创建生成）和 evolve （由 TiDB 自动演进生成） |
| sql_digest | 归一化后的 SQL 的 digest |
| plan_digest | 执行计划的 digest |

### 排查绑定

绑定的排查通常有两种方式：

- 使用系统变量 [`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-从-v40-版本开始引入) 显示上一条执行语句是否采用 binding 的执行计划。

    {{< copyable "sql" >}}

    ```sql
    -- 创建一个 global binding

    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    SELECT * FROM t;
    SELECT @@[SESSION.]last_plan_from_binding;
    ```

    ```sql
    +--------------------------+
    | @@last_plan_from_binding |
    +--------------------------+
    |                        1 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

- 使用 `explain format = 'verbose'` 语句查看 SQL 语句的查询计划。如果 SQL 语句使用了 binding，可以接着执行 `show warnings` 了解该 SQL 语句使用了哪一条 binding。

    ```sql
    -- 创建一个 global binding

    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    -- 使用 explain format = 'verbose' 语句查看 SQL 的执行计划

    explain format = 'verbose' SELECT * FROM t;

    -- 通过执行 `show warnings` 了解该 SQL 语句使用了哪一条 binding

    show warnings;
    ```

    ```sql
    +-------+------+--------------------------------------------------------------------------+
    | Level | Code | Message                                                                  |
    +-------+------+--------------------------------------------------------------------------+
    | Note  | 1105 | Using the bindSQL: SELECT /*+ USE_INDEX(`t` `idx_a`)*/ * FROM `test`.`t` |
    +-------+------+--------------------------------------------------------------------------+
    1 row in set (0.01 sec)

    ```

### 对绑定进行缓存

每个 TiDB 实例都有一个 LRU (Least Recently Used) Cache 对绑定进行缓存，缓存的容量由系统变量 [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-从-v600-版本开始引入) 进行控制。缓存会影响绑定的使用和查看，因此你只能使用和查看存在于缓存中的绑定。

如需查看绑定的使用情况，可以执行 `SHOW binding_cache status` 语句。该语句无法指定作用域，默认作用域为 GLOBAL。该语句可查看缓存中可用绑定的数量、系统中所有可用绑定的数量、缓存中所有绑定的内存使用量及缓存的内存容量。

{{< copyable "sql" >}}

```sql

SHOW binding_cache status;
```

```sql
+-------------------+-------------------+--------------+--------------+
| bindings_in_cache | bindings_in_table | memory_usage | memory_quota |
+-------------------+-------------------+--------------+--------------+
|                 1 |                 1 | 159 Bytes    | 64 MB        |
+-------------------+-------------------+--------------+--------------+
1 row in set (0.00 sec)
```

## 利用 Statement Summary 表获取需要绑定的查询

[Statement Summary](/statement-summary-tables.md) 的表中存放了近期的 SQL 相关的执行信息，如延迟、执行次数、对应计划等。你可以通过查询 Statement Summary 表得到符合条件查询的 `plan_digest`，然后[根据历史执行计划创建绑定](/sql-plan-management.md#根据历史执行计划创建绑定)。

以下示例查找过去两周执行次数超过 10 次、执行计划不稳定且未被绑定的 `SELECT` 语句，并按照执行次数排序，将执行次数前 100 的查询绑定到对应的查询延迟最低的计划上。

```sql
WITH stmts AS (                                                -- Gets all information
  SELECT * FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY
  UNION ALL
  SELECT * FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY_HISTORY 
),
best_plans AS (
  SELECT plan_digest, `digest`, avg_latency, 
  CONCAT('create global binding from history using plan digest "', plan_digest, '"') as binding_stmt 
  FROM stmts t1
  WHERE avg_latency = (SELECT min(avg_latency) FROM stmts t2   -- The plan with the lowest query latency
                       WHERE t2.`digest` = t1.`digest`)
)

SELECT any_value(digest_text) as query, 
       SUM(exec_count) as exec_count, 
       plan_hint, binding_stmt
FROM stmts, best_plans
WHERE stmts.`digest` = best_plans.`digest`
  AND summary_begin_time > DATE_SUB(NOW(), interval 14 day)    -- Executed in the past 2 weeks
  AND stmt_type = 'Select'                                     -- Only consider select statements
  AND schema_name NOT IN ('INFORMATION_SCHEMA', 'mysql')       -- Not an internal query
  AND plan_in_binding = 0                                      -- No binding yet
GROUP BY stmts.`digest`
  HAVING COUNT(DISTINCT(stmts.plan_digest)) > 1                -- This query is unstable. It has more than 1 plan.
         AND SUM(exec_count) > 10                              -- High-frequency, and has been executed more than 10 times.
ORDER BY SUM(exec_count) DESC LIMIT 100;                       -- Top 100 high-frequency queries.
```

通过一些过滤条件得到满足条件的查询，然后直接运行 `binding_stmt` 列对应的语句即可创建相应的绑定。

```
+---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| query                                       | exec_count | plan_hint                                                                   | binding_stmt                                                                                                            |
+---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
| select * from `t` where `a` = ? and `b` = ? |        401 | use_index(@`sel_1` `test`.`t` `a`), no_order_index(@`sel_1` `test`.`t` `a`) | create global binding from history using plan digest "0d6e97fb1191bbd08dddefa7bd007ec0c422b1416b152662768f43e64a9958a6" |
| select * from `t` where `b` = ? and `c` = ? |        104 | use_index(@`sel_1` `test`.`t` `b`), no_order_index(@`sel_1` `test`.`t` `b`) | create global binding from history using plan digest "80c2aa0aa7e6d3205755823aa8c6165092c8521fb74c06a9204b8d35fc037dd9" |
+---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
```

## 跨数据库绑定执行计划 (Cross-DB Binding)

在创建绑定的 SQL 语句中，TiDB 支持使用通配符 `*` 表示数据库，实现跨数据库绑定。该功能自 v7.6.0 开始引入。要使用跨数据库绑定，首先需要开启 [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-从-v760-版本开始引入) 系统变量。

当数据按数据库 (schema/db) 分类存储，同时各数据库具有相同的对象定义并且运行相似的业务逻辑时，跨数据库执行计划绑定能显著简化执行计划的固定过程。以下是一些常见的使用场景：

* 用户在 TiDB 上运行 SaaS 或 PaaS 类服务，每个租户的数据存储于独立的数据库中，以便数据维护和管理。 
* 用户在单一实例中进行分库操作，并在迁移到 TiDB 后保留了原有的数据库结构，即将原实例中的数据按数据库分类存储。 

在这些场景中，跨数据库绑定能有效缓解由于用户数据和负载的不均衡及其快速变化所引发的 SQL 性能问题。SaaS 服务商可以通过跨数据库绑定，固定大数据量用户业务已验证的执行计划，从而避免因小数据量用户业务快速增长引起的潜在性能问题。

使用跨数据库绑定，只需要在创建绑定的 SQL 语句中将数据库名用 `*` 表示，例如：

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, a) */ * FROM t; -- 创建 GLOBAL 作用域的普通绑定
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, a) */ * FROM *.t; -- 创建 GLOBAL 作用域的跨数据库绑定
SHOW GLOBAL BINDINGS;
```

输出结果示例如下：

```sql
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql               | Bind_sql                                          | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t` | SELECT /*+ use_index(`t` `a`)*/ * FROM `test`.`t` | test       | enabled | 2023-12-29 14:19:01.332 | 2023-12-29 14:19:01.332 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
| select * from `*` . `t`    | SELECT /*+ use_index(`t` `a`)*/ * FROM `*`.`t`    |            | enabled | 2023-12-29 14:19:02.232 | 2023-12-29 14:19:02.232 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
```

在 `SHOW GLOBAL BINDINGS` 的输出结果中，跨数据库绑定的 `Default_db` 为空，且 `Original_sql` 和 `Bind_sql` 字段中的数据库名通过 `*` 表示。这条绑定会对所有 `select * from t` 查询生效，而不限于特定数据库。

对于相同的查询，跨数据绑定与普通绑定可以同时存在，TiDB 匹配的优先级从高到低依次为：SESSION 级别的普通绑定 > SESSION 级别的跨数据库绑定 > GLOBAL 级别的普通绑定 > GLOBAL 级别的跨数据库绑定。

除了创建绑定的 SQL 语句不同，跨数据库绑定的删除和状态变更语句与普通绑定相同。下面是一个详细的使用示例。

1. 创建数据库 `db1` 和 `db2`，并在每个数据库中创建两张表：
  
    ```sql
    CREATE DATABASE db1;
    CREATE TABLE db1.t1 (a INT, KEY(a));
    CREATE TABLE db1.t2 (a INT, KEY(a));
    CREATE DATABASE db2;
    CREATE TABLE db2.t1 (a INT, KEY(a));
    CREATE TABLE db2.t2 (a INT, KEY(a));
    ```

2. 开启跨数据库绑定功能：

    ```sql
    SET tidb_opt_enable_fuzzy_binding=1;
    ```

3. 创建跨数据库绑定：

    ```sql
    CREATE GLOBAL BINDING USING SELECT /*+ use_index(t1, a), use_index(t2, a) */ * FROM *.t1, *.t2;
    ```

4. 执行查询并查看是否使用了绑定：

    ```sql
    SELECT * FROM db1.t1, db1.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    
    SELECT * FROM db2.t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    
    SELECT * FROM db1.t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    USE db1;
    SELECT * FROM t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    ```

5. 查看绑定：

    ```sql
    SHOW GLOBAL BINDINGS;
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    | Original_sql                                 | Bind_sql                                                                                 | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    | select * from ( `*` . `t1` ) join `*` . `t2` | SELECT /*+ use_index(`t1` `a`) use_index(`t2` `a`)*/ * FROM (`*` . `t1`) JOIN `*` . `t2` |            | enabled | 2023-12-29 14:22:28.144 | 2023-12-29 14:22:28.144 | utf8    | utf8_general_ci    | manual | ea8720583e80644b58877663eafb3579700e5f918a748be222c5b741a696daf4 |             |
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    ```

6. 删除绑定：

    ```sql
    DROP GLOBAL BINDING FOR SQL DIGEST 'ea8720583e80644b58877663eafb3579700e5f918a748be222c5b741a696daf4';
    SHOW GLOBAL BINDINGS;
    Empty set (0.00 sec)
    ```

## 自动捕获绑定 (Baseline Capturing)

自动绑定会对符合捕获条件的查询进行捕获，为符合条件的查询生成相应的绑定。通常用于[升级时的计划回退防护](#升级时的计划回退防护)。

Plan Baseline 是一组被允许用于 SQL 语句优化器的可接受计划。在典型的应用场景中，TiDB 仅在验证计划性能良好后才将其添加到 Baseline 中。这些计划包含优化器重新生成执行计划所需的所有信息（例如，SQL 计划标识符、提示集、绑定值、优化器环境）。 

### 使用方式

通过将 `tidb_capture_plan_baselines` 的值设置为 `on`（其默认值为 `off`）可以打开自动捕获绑定功能。

> **注意：**
>
> 自动绑定功能依赖于 [Statement Summary](/statement-summary-tables.md)，因此在使用自动绑定之前需打开 Statement Summary 开关。

开启自动绑定功能后，每隔 `bind-info-lease`（默认值为 `3s`）会遍历一次 Statement Summary 中的历史 SQL 语句，并为至少出现两次的 SQL 语句自动捕获绑定。绑定的执行计划为 Statement Summary 中记录执行这条语句时使用的执行计划。

对于以下几种 SQL 语句，TiDB 不会自动捕获绑定：

- EXPLAIN 和 EXPLAIN ANALYZE 语句；
- TiDB 内部执行的 SQL 语句，比如统计信息自动加载使用的 SELECT 查询；
- 存在 `Enabled` 或 `Disabled` 状态绑定的语句；
- 满足捕获绑定黑名单过滤条件的语句。

> **注意：**
>
> 当前，绑定通过生成一组 Hints 来固定查询语句生成的执行计划，从而确保执行计划不发生变化。对于大多数 OLTP 查询，TiDB 能够保证计划前后一致，如使用相同的索引、相同的 Join 方式（如 HashJoin、IndexJoin）等。但是，受限于当前 Hints 的完善程度，对于一些较为复杂的查询，如两个表以上的 Join 和复杂的 OLAP、MPP 类查询，TiDB 无法保证计划在绑定前后完全一致。

对于 `PREPARE`/`EXECUTE` 语句组，或通过二进制协议执行的查询，TiDB 会为真正的查询（而不是 `PREPARE`/`EXECUTE` 语句）自动捕获绑定。

> **注意：**
>
> 由于 TiDB 存在一些内嵌 SQL 保证一些功能的正确性，所以自动捕获绑定时会默认屏蔽内嵌 SQL。

### 过滤捕获绑定

使用本功能，你可以设置黑名单，将满足黑名单规则的查询排除在捕获范围之外。黑名单支持的过滤维度包括表名、频率和用户名。

#### 使用方式

将过滤规则插入到系统表 `mysql.capture_plan_baselines_blacklist` 中，该过滤规则即刻起会在整个集群范围内生效。

{{< copyable "sql" >}}

```sql
-- 按照表名进行过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.t');

-- 通过通配符来实现按照数据库名和表名进行过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.table_*');
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'db_*.table_*');

-- 按照执行频率进行过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('frequency', '2');

-- 按照用户名进行过滤
INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('user', 'user1');
```

| **维度名称** | **说明**                                                     | 注意事项                                                     |
| :----------- | :----------------------------------------------------------- | ------------------------------------------------------------ |
| table        | 按照表名进行过滤，每个过滤规则均采用 `db.table` 形式，支持通配符。详细规则可以参考[直接使用表名](/table-filter.md#直接使用表名)和[使用通配符](/table-filter.md#使用通配符)。 | 字母大小写不敏感，如果包含非法内容，日志会输出 `[sql-bind] failed to load mysql.capture_plan_baselines_blacklist` 警告。 |
| frequency    | 按照频率进行过滤，默认捕获执行超过一次的语句。可以设置较大值来捕获执行频繁的语句。 | 插入的值小于 1 会被认为是非法值，同时，日志会输出 `[sql-bind] frequency threshold is less than 1, ignore it` 警告。如果插入了多条频率过滤规则，频率最大的值会被用作过滤条件。 |
| user         | 按照用户名进行过滤，黑名单用户名执行的语句不会被捕获。                           | 如果多个用户执行同一条语句，只有当他们的用户名都在黑名单的时候，该语句才不会被捕获。 |

> **注意：**
>
> - 修改黑名单需要数据库的 super privilege 权限。
>
> - 如果黑名单包含了非法的过滤内容时，TiDB 会在日志中输出 `[sql-bind] unknown capture filter type, ignore it` 进行提示。

### 升级时的计划回退防护

当需要升级 TiDB 集群时，你可以利用自动捕获绑定对潜在的计划回退风险进行一定程度的防护，具体流程为：

1. 升级前打开自动捕获。

    > **注意：**
    >
    > 经测试，长期打开自动捕获对集群负载的性能影响很小。尽量长期打开自动捕获，以确保重要的查询（出现过两次及以上）都能被捕获到。

2. 进行 TiDB 集群的升级。在升级完成后，这些通过捕获的绑定会发挥作用，确保在升级后，查询的计划不会改变。
3. 升级完成后，根据情况手动删除绑定。

    - 通过[`SHOW GLOBAL BINDINGS`](#查看绑定)语句检查绑定来源：

        根据输出中的 `Source` 字段对绑定的来源进行区分，确认是通过捕获 (`capture`) 生成还是通过手动创建 (`manual`) 生成。

    - 确定 `capture` 的绑定是否需要保留：

        ```
        -- 查看绑定生效时的计划
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -- 查看绑定不生效时的计划
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;
        ```

        - 如果屏蔽绑定前后，查询得到的计划一致，则可以安全删除此绑定。

        - 如果计划不一样，则可能需要对此计划变化的原因进行排查，如检查统计信息等操作。在这种情况下需要保留此绑定，确保计划不发生变化。

## 自动演进绑定 (Baseline Evolution)

自动演进绑定，在 TiDB 4.0 版本引入，是执行计划管理的重要功能之一。

由于某些数据变更后，原先绑定的执行计划可能是一个不优的计划。为了解决该问题，引入自动演进绑定功能来自动优化已经绑定的执行计划。

另外自动演进绑定还可以一定程度上避免统计信息改动后，对执行计划带来的抖动。

### 使用方式

通过以下语句可以开启自动演进绑定功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

`tidb_evolve_plan_baselines` 的默认值为 `off`。

> **警告：**
>
> - 自动演进功能目前为实验特性，存在未知风险，不建议在生产环境中使用。
>
> - 此变量开关已强制关闭，直到自动演进成为正式功能 GA (Generally Available)。如果你尝试打开开关，会产生报错。如果你已经在生产环境中使用了此功能，请尽快将它禁用。如发现 binding 状态不如预期，请从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。

在打开自动演进功能后，如果优化器选出的最优执行计划不在之前绑定的执行计划之中，会将其记录为待验证的执行计划。每隔 `bind-info-lease`（默认值为 `3s`），会选出一个待验证的执行计划，将其和已经绑定的执行计划中代价最小的比较实际运行时间。如果待验证的运行时间更优的话（目前判断标准是运行时间小于等于已绑定执行计划运行时间的 2/3），会将其标记为可使用的绑定。以下示例描述上述过程。

假如有表 `t` 定义如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

在表 `t` 上进行如下查询：

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

表上满足条件 `a < 100` 的行很少。但由于某些原因，优化器没能选中使用索引 `a` 这个最优执行计划，而是误选了速度慢的全表扫，那么用户首先可以通过如下语句创建一个绑定：

{{< copyable "sql" >}}

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 USING SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
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

## 升级检查 (Upgrade Checklist)

执行计划管理功能 (SPM) 在版本升级过程中可能会出现一些兼容性问题导致升级失败，你需要在版本升级前做一些检查，确保版本顺利升级。

* 当你尝试从 v5.2 以前的版本（即 v4.0、v5.0、v5.1）升级到当前版本，需要注意在升级前检查自动演进的开关 `tidb_evolve_plan_baselines` 是否已经关闭。如果尚未关闭，则需要将其关闭后再进行升级。具体操作如下所示：

    {{< copyable "sql" >}}

    ```sql
    -- 在待升级的版本上检查自动演进的开关 `tidb_evolve_plan_baselines` 是否关闭。

    SELECT @@global.tidb_evolve_plan_baselines;

    -- 如果演进的开关 `tidb_evolve_plan_baselines` 尚未关闭，则需要将其关闭。

    set global tidb_evolve_plan_baselines = off;
    ```

* 当你尝试从 v4.0 版本升级到当前版本，需要注意在升级前检查所有可用绑定对应的查询语句在新版本中是否存在语法错误。如果存在语法错误，则需要删除对应的绑定。

    具体操作如下所示：

    {{< copyable "sql" >}}

    ```sql
    -- 在待升级的版本上检查现有可用绑定对应的查询语句。

    SELECT bind_sql FROM mysql.bind_info WHERE status = 'using';

    -- 将上一条查询得到的结果，在新版本的测试环境中进行验证。

    bind_sql_0;
    bind_sql_1;
    ...

    -- 如果报错信息是语法错误（ERROR 1064 (42000): You have an error in your SQL syntax），则需要删除对应的绑定。
    -- 如果是其他错误，如未找到表，则表示语法兼容，不需要进行额外的处理。
    ```
