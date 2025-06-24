</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：String
- 默认值：`""`
- 该变量用于控制优化器的一些内部行为。
- 优化器的行为可能会因用户场景或 SQL 语句而异。此变量提供了对优化器更细粒度的控制，有助于防止因优化器行为变化导致升级后的性能回退。
- 更详细的介绍请参见[优化器修复控制](/optimizer-fix-controls.md)。

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">从 v6.3.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 该变量用于控制整个会话中的公共表表达式（CTE）是否内联。默认值为 `OFF`，表示默认不强制内联 CTE。但是，您仍然可以通过指定 `MERGE()` hint 来内联 CTE。如果将变量设置为 `ON`，则此会话中的所有 CTE（递归 CTE 除外）都将被强制内联。

### tidb_opt_advanced_join_hint <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 该变量用于控制连接方法 hint（如 [`HASH_JOIN()` hint](/optimizer-hints.md#hash_joint1_name--tl_name-) 和 [`MERGE_JOIN()` hint](/optimizer-hints.md#merge_joint1_name--tl_name-)）是否影响连接重排优化过程，包括 [`LEADING()` hint](/optimizer-hints.md#leadingt1_name--tl_name-) 的使用。默认值为 `ON`，表示不影响。如果设置为 `OFF`，在同时使用连接方法 hint 和 `LEADING()` hint 的某些场景下可能会出现冲突。

> **注意：**
>
> v7.0.0 之前版本的行为与将此变量设置为 `OFF` 一致。为了保证向前兼容性，当您从早期版本升级到 v7.0.0 或更高版本的集群时，此变量会被设置为 `OFF`。为了获得更灵活的 hint 行为，强烈建议在确保不会出现性能回退的情况下将此变量切换为 `ON`。

### tidb_opt_insubq_to_join_and_agg

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 该变量用于设置是否启用将子查询转换为连接和聚合的优化规则。
- 例如，启用此优化规则后，子查询转换如下：

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    子查询转换为连接如下：

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    如果 `t1` 的 `aa` 列被限制为 `unique` 且 `not null`，则可以使用以下语句，无需聚合：

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 该变量用于控制 TiDB 连接重排算法的选择。当参与连接重排的节点数大于此阈值时，TiDB 选择贪心算法，当小于此阈值时，TiDB 选择动态规划算法。
- 目前，对于 OLTP 查询，建议保持默认值。对于 OLAP 查询，建议将变量值设置为 10~15，以在 OLAP 场景中获得更好的连接顺序。

### tidb_opt_limit_push_down_threshold

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`100`
- 范围：`[0, 2147483647]`
- 该变量用于设置决定是否将 Limit 或 TopN 算子下推到 TiKV 的阈值。
- 如果 Limit 或 TopN 算子的值小于或等于此阈值，这些算子将被强制下推到 TiKV。此变量解决了由于错误估算导致 Limit 或 TopN 算子无法部分下推到 TiKV 的问题。

### tidb_opt_memory_factor

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 范围：`[0, 2147483647]`
- 默认值：`0.001`
- 表示 TiDB 存储一行数据的内存成本。此变量在[成本模型](/cost-model.md)内部使用，**不建议**修改其值。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">从 v5.1.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 当变量值为 `ON` 时，左连接运算符始终使用内表作为构建侧，右连接运算符始终使用外表作为构建侧。如果将值设置为 `OFF`，外连接运算符可以使用表的任一侧作为构建侧。

### tidb_opt_network_factor

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 范围：`[0, 2147483647]`
- 默认值：`1.0`
- 表示通过网络传输 1 字节数据的网络成本。此变量在[成本模型](/cost-model.md)内部使用，**不建议**修改其值。

### tidb_opt_objective <span class="version-mark">从 v7.4.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：枚举
- 默认值：`moderate`
- 可选值：`moderate`，`determinate`
- 该变量控制优化器的目标。`moderate` 保持 TiDB v7.4.0 之前版本的默认行为，优化器尝试使用更多信息生成更好的执行计划。`determinate` 模式倾向于更保守，使执行计划更稳定。
- 实时统计信息是基于 DML 语句自动更新的总行数和修改行数。当此变量设置为 `moderate`（默认）时，TiDB 基于实时统计信息生成执行计划。当此变量设置为 `determinate` 时，TiDB 不使用实时统计信息生成执行计划，这将使执行计划更稳定。
- 对于长期稳定的 OLTP 工作负载，或者如果用户确定现有执行计划，建议使用 `determinate` 模式以减少意外执行计划变更的可能性。此外，您可以使用 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) 防止统计信息被修改，进一步稳定执行计划。

### tidb_opt_ordering_index_selectivity_ratio <span class="version-mark">从 v8.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 集群持久化：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 默认值：`-1`
- 范围：`[-1, 1]`
