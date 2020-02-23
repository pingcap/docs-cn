---
title: TiDB 内存控制文档
category: how-to
aliases: ['/docs-cn/sql/tidb-memory-control/']
---

# TiDB 内存控制文档

目前 TiDB 已经能够做到追踪单条 SQL 查询过程中的内存使用情况，当内存使用超过一定阈值后也能采取一些操作来预防 OOM 或者排查 OOM 原因。在 TiDB 的配置文件中，我们可以使用如下配置来控制内存使用超阈值时 TiDB 的行为：

{{< copyable "" >}}

```
# Valid options: ["log", "cancel"]
oom-action = "log"
```

- 如果上面的配置项使用的是 "log"，那么当一条 SQL 的内存使用超过一定阈值（由 session 变量 `tidb_mem_quota_query` 来控制）后，TiDB 会在 log 文件中打印一条 LOG，然后这条 SQL 继续执行，之后如果发生了 OOM 可以在 LOG 中找到对应的 SQL。
- 如果上面的配置项使用的是 "cancel"，那么当一条 SQL 的内存使用超过一定阈值后，TiDB 会立即中断这条 SQL 的执行并给客户端返回一个 error，error 信息中会详细写明这条 SQL 执行过程中各个占用内存比较多的物理执行算子的内存使用情况。

## 如何配置一条 SQL 执行过程中的内存使用阈值

可以在配置文件中设置每个 Query 默认的 Memory Quota，例如将其设置为 32GB：

{{< copyable "" >}}

```
mem-quota-query = 34359738368
```

此外还可通过如下几个 session 变量来控制一条 Query 中的内存使用，大多数用户只需要设置 `tidb_mem_quota_query` 即可，其他变量是高级配置，大多数用户不需要关心：

| 变量名                            | 作用                                              | 单位  | 默认值    |
|-----------------------------------|---------------------------------------------------|-------|-----------|
| tidb_mem_quota_query              | 配置整条 SQL 的内存使用阈值                       | Byte  | 32 << 30  |
| tidb_mem_quota_hashjoin           | 配置 Hash Join 的内存使用阈值                     | Byte  | 32 << 30  |
| tidb_mem_quota_mergejoin          | 配置 Merge Join 的内存使用阈值                    | Byte  | 32 << 30  |
| tidb_mem_quota_sort               | 配置 Sort 的内存使用阈值                          | Byte  | 32 << 30  |
| tidb_mem_quota_topn               | 配置 TopN 的内存使用阈值                          | Byte  | 32 << 30  |
| tidb_mem_quota_indexlookupreader  | 配置 Index Lookup Reader 的内存使用阈值           | Byte  | 32 << 30  |
| tidb_mem_quota_indexlookupjoin    | 配置 Index Lookup Join 的内存使用阈值             | Byte  | 32 << 30  |
| tidb_mem_quota_nestedloopapply    | 配置 Nested Loop Apply 的内存使用阈值             | Byte  | 32 << 30  |

几个使用例子：

配置整条 SQL 的内存使用阈值为 8GB：

{{< copyable "sql" >}}

```sql
set @@tidb_mem_quota_query = 8 << 30;
```

配置整条 SQL 的内存使用阈值为 8MB：

{{< copyable "sql" >}}

```sql
set @@tidb_mem_quota_query = 8 << 20;
```

配置整条 SQL 的内存使用阈值为 8KB：

{{< copyable "sql" >}}

```sql
set @@tidb_mem_quota_query = 8 << 10;
```