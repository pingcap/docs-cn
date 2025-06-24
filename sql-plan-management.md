---
title: SQL 执行计划管理 (SPM)
summary: 了解 TiDB 中的 SQL 执行计划管理。
---

# SQL 执行计划管理 (SPM)

SQL 执行计划管理是一组用于手动干预 SQL 执行计划的功能。这些功能包括 SQL 绑定、基线捕获和基线演进。

## SQL 绑定

SQL 绑定是 SPM 的基础。[优化器提示](/optimizer-hints.md)文档介绍了如何使用提示选择特定的执行计划。但是，有时您需要在不修改 SQL 语句的情况下干预执行计划的选择。通过 SQL 绑定，您可以在不修改 SQL 语句的情况下选择指定的执行计划。

<CustomContent platform="tidb">

> **注意：**
>
> 要使用 SQL 绑定，您需要具有 `SUPER` 权限。如果 TiDB 提示您没有足够的权限，请参见[权限管理](/privilege-management.md)添加所需的权限。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 要使用 SQL 绑定，您需要具有 `SUPER` 权限。如果 TiDB 提示您没有足够的权限，请参见[权限管理](https://docs.pingcap.com/tidb/stable/privilege-management)添加所需的权限。

</CustomContent>

### 创建绑定

您可以根据 SQL 语句或历史执行计划为 SQL 语句创建绑定。

#### 根据 SQL 语句创建绑定

{{< copyable "sql" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING [FOR BindableStmt] USING BindableStmt;
```

此语句在 GLOBAL 或 SESSION 级别绑定 SQL 执行计划。目前，TiDB 支持的可绑定 SQL 语句（BindableStmt）包括 `SELECT`、`DELETE`、`UPDATE` 和带有 `SELECT` 子查询的 `INSERT` / `REPLACE`。以下是一个示例：

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
CREATE GLOBAL BINDING FOR SELECT * FROM orders USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
```

> **注意：**
>
> 绑定的优先级高于手动添加的提示。因此，当您执行包含提示的语句而存在相应绑定时，控制优化器行为的提示不会生效。但是，其他类型的提示仍然有效。

具体来说，由于语法冲突，以下两类语句无法绑定执行计划。在创建绑定时会报语法错误。请参见以下示例：

```sql
-- 第一类：使用 `JOIN` 关键字且不使用 `USING` 关键字指定关联列获取笛卡尔积的语句。
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1 JOIN orders o2
USING
    SELECT * FROM orders o1 JOIN orders o2;

-- 第二类：包含 `USING` 关键字的 `DELETE` 语句。
CREATE GLOBAL BINDING for
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id
USING
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id;
```

您可以通过使用等效语句来绕过语法冲突。例如，您可以按以下方式重写上述语句：

```sql
-- 第一类语句的重写：删除 `JOIN` 关键字，用逗号替代。
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1, orders o2
USING
    SELECT * FROM orders o1, orders o2;

-- 第二类语句的重写：从 `DELETE` 语句中删除 `USING` 关键字。
CREATE GLOBAL BINDING for
    DELETE users FROM users JOIN orders ON users.id = orders.user_id
USING
    DELETE users FROM users JOIN orders ON users.id = orders.user_id;
```

> **注意：**
>
> 为带有 `SELECT` 子查询的 `INSERT` / `REPLACE` 语句创建执行计划绑定时，需要在 `SELECT` 子查询中指定要绑定的优化器提示，而不是在 `INSERT` / `REPLACE` 关键字后指定。否则，优化器提示不会按预期生效。

以下是两个示例：

```sql
-- 以下语句中的提示会生效。
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT INTO orders SELECT /*+ use_index(@sel_1 pre_orders, idx_created) */ * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);

-- 以下语句中的提示不会生效。
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT /*+ use_index(@sel_1 pre_orders, idx_created) */ INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);
```

如果在创建执行计划绑定时未指定作用域，默认作用域为 SESSION。TiDB 优化器会对绑定的 SQL 语句进行规范化处理，并将其存储在系统表中。在处理 SQL 查询时，如果规范化后的语句与系统表中的某个绑定 SQL 语句匹配，并且系统变量 `tidb_use_plan_baselines` 设置为 `on`（默认值为 `on`），TiDB 就会为该语句使用相应的优化器提示。如果有多个可匹配的执行计划，优化器会选择成本最低的一个进行绑定。

`规范化`是一个将 SQL 语句中的常量转换为变量参数，并显式指定查询中引用的表的数据库，同时对 SQL 语句中的空格和换行进行标准化处理的过程。请参见以下示例：

```sql
SELECT * FROM users WHERE balance >    100
-- 规范化后的语句如下：
SELECT * FROM bookshop . users WHERE balance > ?
```

> **注意：**
>
> 在规范化过程中，`IN` 谓词中的 `?` 被规范化为 `...`。
>
> 例如：
>
> ```sql
> SELECT * FROM books WHERE type IN ('Novel')
> SELECT * FROM books WHERE type IN ('Novel','Life','Education')
> -- 规范化后的语句如下：
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> ```
>
> 规范化后，不同长度的 `IN` 谓词被识别为相同的语句，因此您只需要创建一个适用于所有这些谓词的绑定。
>
> 例如：
>
> ```sql
> CREATE TABLE t (a INT, KEY(a));
> CREATE BINDING FOR SELECT * FROM t WHERE a IN (?) USING SELECT /*+ use_index(t, idx_a) */ * FROM t WHERE a in (?);
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
> 在 v7.4.0 之前版本的 TiDB 集群中创建的绑定可能包含 `IN (?)`。升级到 v7.4.0 或更高版本后，这些绑定将被修改为 `IN (...)`。
>
> 例如：
>
> ```sql
> -- 在 v7.3.0 上创建绑定
> mysql> CREATE GLOBAL BINDING FOR SELECT * FROM t WHERE a IN (1) USING SELECT /*+ use_index(t, idx_a) */ * FROM t WHERE a IN (1);
> mysql> SHOW GLOBAL BINDINGS;
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                  | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ? ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:39:02.695 | 2024-09-03 15:39:02.695 | utf8mb4 | utf8mb4_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
>
> -- 升级到 v7.4.0 或更高版本后
> mysql> SHOW GLOBAL BINDINGS;
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ... ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:35:59.861 | 2024-09-03 15:35:59.861 | utf8mb4 | utf8mb4_general_ci | manual | da38bf216db4a53e1a1e01c79ffa42306419442ad7238480bb7ac510723c8bdf |             |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> ```

当一个 SQL 语句在 GLOBAL 和 SESSION 作用域都有绑定的执行计划时，由于优化器在遇到 SESSION 绑定时会忽略 GLOBAL 作用域中的绑定执行计划，因此该语句在 SESSION 作用域中的绑定执行计划会屏蔽 GLOBAL 作用域中的执行计划。

例如：

```sql
--  创建一个 GLOBAL 绑定，并在此绑定中指定使用 `sort merge join`。
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 此 SQL 语句的执行计划使用 GLOBAL 绑定中指定的 `sort merge join`。
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- 创建另一个 SESSION 绑定，并在此绑定中指定使用 `hash join`。
CREATE BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ hash_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- 在此语句的执行计划中，使用的是 SESSION 绑定中指定的 `hash join`，而不是 GLOBAL 绑定中指定的 `sort merge join`。
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

当第一个 `SELECT` 语句被执行时，优化器通过 GLOBAL 作用域中的绑定为语句添加 `sm_join(t1, t2)` 提示。`explain` 结果中的执行计划顶部节点是 MergeJoin。当第二个 `SELECT` 语句被执行时，优化器使用 SESSION 作用域中的绑定而不是 GLOBAL 作用域中的绑定，并为语句添加 `hash_join(t1, t2)` 提示。`explain` 结果中的执行计划顶部节点是 HashJoin。

每个规范化的 SQL 语句在同一时间只能有一个使用 `CREATE BINDING` 创建的绑定。当为同一个规范化的 SQL 语句创建多个绑定时，保留最后创建的绑定，所有之前的绑定（创建的和演进的）都被标记为已删除。但是会话绑定和全局绑定可以共存，不受此逻辑影响。

此外，在创建绑定时，TiDB 要求会话处于数据库上下文中，这意味着在客户端连接时指定了数据库或执行了 `use ${database}`。

原始 SQL 语句和绑定语句在规范化和移除提示后必须具有相同的文本，否则绑定将失败。请参见以下示例：

- 此绑定可以成功创建，因为参数化和移除提示后的文本相同：`SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

- 此绑定将失败，因为原始 SQL 语句处理为 `SELECT * FROM test . t WHERE a > ?`，而绑定 SQL 语句处理为 `SELECT * FROM test . t WHERE b > ?`。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **注意：**
>
> 对于 `PREPARE` / `EXECUTE` 语句和使用二进制协议执行的查询，您需要为实际的查询语句创建执行计划绑定，而不是为 `PREPARE` / `EXECUTE` 语句创建绑定。
