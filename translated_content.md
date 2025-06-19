- 第五个示例同样使用 `1.0`，但在 `a` 上添加了谓词，限制了最坏情况下的扫描范围。这是因为 `WHERE a <= 9000` 匹配索引，大约有 9,000 行数据符合条件。由于 `b` 上的过滤谓词不在索引中，所有这些大约 9,000 行数据都需要被扫描，才能找到符合 `b <= 9000` 的行。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE a <= 9000 AND b <= 9000 ORDER BY a LIMIT 1;
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | id                                 | estRows | task      | access object         | operator info                      |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | Limit_12                           | 1.00    | root      |                       | offset:0, count:1                  |
    | └─Projection_22                    | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c       |
    |   └─IndexLookUp_21                 | 1.00    | root      |                       |                                    |
    |     ├─IndexRangeScan_18(Build)     | 9074.99 | cop[tikv] | table:t, index:ia(a)  | range:[-inf,9000], keep order:true |
    |     └─Selection_20(Probe)          | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)                 |
    |       └─TableRowIDScan_19          | 9074.99 | cop[tikv] | table:t               | keep order:false                   |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    ```

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">从 v7.0.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 默认值：`0`
- 取值范围：`[0, 1]`
- 该变量用于控制优化器在 SQL 语句中同时存在 `ORDER BY` 和 `LIMIT` 子句以及过滤条件时如何选择索引。
- 对于这类查询，优化器会考虑选择相应的索引来满足 `ORDER BY` 和 `LIMIT` 子句（即使该索引不满足任何过滤条件）。但是，由于数据分布的复杂性，优化器在这种情况下可能会选择次优的索引。
- 该变量表示一个阈值。当存在可以满足过滤条件的索引，且其选择率估计值低于此阈值时，优化器将避免选择用于满足 `ORDER BY` 和 `LIMIT` 的索引，而是优先选择满足过滤条件的索引。
- 例如，当变量设置为 `0` 时，优化器保持其默认行为；当设置为 `1` 时，优化器始终优先选择满足过滤条件的索引，避免选择同时满足 `ORDER BY` 和 `LIMIT` 子句的索引。
- 在以下示例中，表 `t` 总共有 1,000,000 行数据。使用列 `b` 上的索引时，其估计行数约为 8,748，因此其选择率估计值约为 0.0087。默认情况下，优化器选择列 `a` 上的索引。但在将此变量设置为 0.01 后，由于列 `b` 上索引的选择率（0.0087）小于 0.01，优化器选择了列 `b` 上的索引。

```sql
> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+-----------------------------------+---------+-----------+----------------------+--------------------+
| id                                | estRows | task      | access object        | operator info      |
+-----------------------------------+---------+-----------+----------------------+--------------------+
| Limit_12                          | 1.00    | root      |                      | offset:0, count:1  |
| └─Projection_25                   | 1.00    | root      |                      | test.t.a, test.t.b |
|   └─IndexLookUp_24                | 1.00    | root      |                      |                    |
|     ├─IndexFullScan_21(Build)     | 114.30  | cop[tikv] | table:t, index:ia(a) | keep order:true    |
|     └─Selection_23(Probe)         | 1.00    | cop[tikv] |                      | le(test.t.b, 9000) |
|       └─TableRowIDScan_22         | 114.30  | cop[tikv] | table:t              | keep order:false   |
+-----------------------------------+---------+-----------+----------------------+--------------------+

> SET SESSION tidb_opt_ordering_index_selectivity_threshold = 0.01;

> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| id                               | estRows | task      | access object        | operator info                       |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| TopN_9                           | 1.00    | root      |                      | test.t.a, offset:0, count:1         |
| └─IndexLookUp_20                 | 1.00    | root      |                      |                                     |
|   ├─IndexRangeScan_17(Build)     | 8748.62 | cop[tikv] | table:t, index:ib(b) | range:[-inf,9000], keep order:false |
|   └─TopN_19(Probe)               | 1.00    | cop[tikv] |                      | test.t.a, offset:0, count:1         |
|     └─TableRowIDScan_18          | 8748.62 | cop[tikv] | table:t              | keep order:false                    |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
```

### tidb_opt_prefer_range_scan <span class="version-mark">从 v5.0 版本开始引入</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 将此变量的值设置为 `ON` 后，优化器将始终优先选择范围扫描而不是全表扫描。
- 在以下示例中，在启用 `tidb_opt_prefer_range_scan` 之前，TiDB 优化器执行全表扫描。启用 `tidb_opt_prefer_range_scan` 后，优化器选择索引范围扫描。

```sql
explain select * from t where age=5;
+-------------------------+------------+-----------+---------------+-------------------+
| id                      | estRows    | task      | access object | operator info     |
+-------------------------+------------+-----------+---------------+-------------------+
| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |
| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |
|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |
+-------------------------+------------+-----------+---------------+-------------------+
3 rows in set (0.00 sec)

set session tidb_opt_prefer_range_scan = 1;

explain select * from t where age=5;
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| id                            | estRows    | task      | access object               | operator info                 |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |
| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |
