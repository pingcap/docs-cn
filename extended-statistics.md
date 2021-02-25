---
title: 扩展统计信息简介
summary: 扩展统计信息用于优化包含相关列的查询
---

# 扩展统计信息简介

[统计信息简介](/statistics.md)章节中提到的统计信息，包括直方图和 Count-Min Sketch 等，都是常规统计信息。在每次手动或自动收集统计信息时，对应表的这些常规信息都会被收集。与常规统计信息相对的另一类统计信息是扩展统计信息，只对特定场景下的优化器估算有作用。

由于只在特定场景有益，扩展统计信息在默认手动或自动 `ANALYZE` 时不会被收集，避免增加收集统计信息的开销。如果想要收集扩展统计信息，需要先通过 SQL 命令进行“注册”，然后在下一次手动或自动 `ANALYZE` 时，TiDB 会在常规统计信息基础上额外收集这些注册过的扩展统计信息。

## 扩展统计信息注册

如果要对想收集的扩展统计信息进行注册，可使用 `ALTER TABLE ADD STATS_EXTENDED` SQL 语句，其语法如下：

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

该语句表示想要在指定表的指定列组合上收集指定类型的扩展统计信息，并为其命名。

- `table_name` 表示想要收集扩展统计信息的表。
- `stats_name` 在每张表内需要服从唯一性约束。
- `stats_type` 表示扩展统计信息的类型，目前只支持 `correlation` 这一种取值。
- `column_name` 可以为两个或多个，取决于 `stats_type` 的值。如果 `stats_type` 是 `correlation` 类型，`column_name` 必须为两个。

执行这条注册语句会在系统表 `mysql.stats_extended` 中插入一条记录，该表包含的列为：

| 列名 | 说明 |
| -------- | ------------- |
| `name` |  扩展统计信息名，通过注册语句中的 `stats_name` 指定 |
| `type` | 扩展统计信息的类型 |
| `table_id` | 表的 id |
| `column_ids` | 列的 id，格式如 `[1,2]` |
| `stats` | 扩展统计信息的值，注册时这列为空 |
| `version` | 这条扩展统计信息的版本 |
| `status` | 这条扩展统计信息的状态，刚注册时该列值为 0，表示“未收集”状态 |

在对某张表做 `ANALYZE` 时，如果 `mysql.stats_extended` 中存在对应该表 id 的记录，该类型的扩展统计信息会被收集，并记录到 `stats` 这一列里。相应地，`status` 列会被更新为 `1`（表示“已收集”状态），`version` 列的值会被调大。

## 扩展统计信息类型

### 顺序相关性 (correlation)

目前唯一支持的扩展统计信息类型是顺序相关性。以如下注册语句为例：

{{< copyable "sql" >}}

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

在执行该语句后的下一次 `ANALYZE` 时，TiDB 会计算 `t` 表上 `col1` 和 `col2` 值在顺序上的[皮尔逊相关系数](https://zh.wikipedia.org/wiki/%E7%9A%AE%E5%B0%94%E9%80%8A%E7%A7%AF%E7%9F%A9%E7%9B%B8%E5%85%B3%E7%B3%BB%E6%95%B0)，并将结果值记录到 `mysql.stats_extended` 的 `stats` 列。

该值主要用作提升以下场景中优化器的索引决策：

对于定义如下的表 `t`：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

假设 `t` 表的 `col1` 和 `col2` 上的值都按行顺序服从单调递增的约束，即 `col1` 和 `col2` 的值在顺序上严格相关（correlation 值为 1）：

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

对于以上查询，优化器对于 `t` 表的访问方式有两个选择：一是用 `col1` 的索引按 `col1 > 1` 做过滤，再对结果按 `col2` 的值求 Top 1；二是对 `col2` 的索引按序扫描，直到遇到一条满足 `col1 > 1` 条件的记录后结束扫描。前者的代价通过常规统计信息可以作出较准的估算，而后者的代价取决于在按 `col2` 顺序扫描时，什么时候可以遇到满足过滤条件的记录。一般地，优化器只能假设 `col1` 和 `col2` 之间是独立不相关的，然后用 LIMIT 的行数 1 除以 `col1 > 1` 的选择率作为需要按 `col2` 顺序扫描的行数。这个估算在该两列的独立不相关假设失效时会带来较大的误差，导致最后优化器选错索引。

有了顺序相关性的扩展统计信息后，优化器可以更准确地估算上述选择二中需要扫描的行数。由于 `col1` 和 `col2` 在顺序上严格相关，优化器会将上述选择二的行数估算等价转化为：

{{< copyable "sql" >}}

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

这个过滤条件的行数估算再加上 1，后者可以通过直方图获得较准确的估算，从而避免了使用不恰当的独立不相关假设。

当列之间的相关系数的绝对值低于系统变量 `tidb_opt_correlation_threshold` 时（默认值为 0.9），优化器会认为相关性不够从而依然使用独立不相关假设，但会对估算的行数启发式地调大，相关性绝对值越高，调大越多，系统变量 `tidb_opt_correlation_exp_factor` 越大，调大也越多。

## 扩展统计信息收集

如上所述，在注册后，扩展统计信息会在对表的 `ANALYZE` 时被收集（只对索引的 `ANALYZE` 不会收集），不管是手动还是自动触发的。值得注意的是，增量 `ANALYZE` 或者当 `tidb_enable_fast_analyze` 为 `true` 时，扩展统计信息不会被收集。

## 扩展统计信息缓存

为了提高优化器访问扩展统计信息的效率，每个 TiDB 实例会维护一份扩展统计信息的缓存，并定期加载 `mysql.stats_extended` 表以保证缓存和表数据的一致。TiDB 对 `mysql.stats_extended` 的每一行记录维护了一个 `version` 列，每次修改行时需要增大 `version` 列的值，使得每次加载 `mysql.stats_extended` 时可以只增量加载相对于上次被更新过的行，减少系统的开销。但由于系统存在多个 TiDB 实例，增量加载会引入一个问题：当某个 TiDB 实例从 `mysql.stats_extended` 中删除一行时，这个删除操作不能被其他 TiDB 实例感知并应用到其缓存中，进而导致多实例之间缓存不一致，以及缓存和表数据的不一致。

为了解决这个问题，TiDB 为用户提供了专门删除扩展统计信息的 SQL 接口：

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

这条语句会将 `mysql.stats_extended` 中相应记录的 `status` 列值修改为 2（表示“已删除”状态），而不是将其从表中直接删除。其他 TiDB 实例会增量读取到这个更新操作，并删除各自缓存中的记录，使得缓存保持一致。在后续的统计信息 Garbage Collection 过程中，TiDB 才会将这些被标记为“删除”状态的记录真正从表中删除，以避免 `mysql.stats_extended` 的无限增长。

不推荐直接操作 `mysql.stats_extended` 表数据，否则可能会导致扩展统计信息缓存不一致。但为了应对可能发生的误操作，TiDB 提供了以下 SQL 语句，用于强制将当前 TiDB 实例的扩展统计信息缓存丢弃并重新对 `mysql.stats_extended` 做一次全量加载：

{{< copyable "sql" >}}

```sql
ADMIN RELOAD STATS_EXTENDED;
```

## 扩展统计信息导入导出

[统计信息简介](/statistics.md)章节中提到的常规统计信息导入导出同样适用于扩展统计信息，导出的扩展统计信息和常规统计信息在同一个 json 文件中。

## 控制开关

通过以下语句可以开启扩展统计信息功能：

{{< copyable "sql" >}}

```sql
set global tidb_enable_extended_stats = on;
```

`tidb_enable_extended_stats` 的默认值为 `off`。

> **注意：**
>
> 设置 global 系统变量在当前 session 并不会生效，只会在新创建的 session 生效。可以将 global 关键字替换为 session 使当前 session 开启扩展统计信息功能。
