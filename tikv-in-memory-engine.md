---
title: TiKV MVCC 内存引擎
summary: 了解内存引擎的适用场景和工作原理，使用内存引擎加速多版本记录查询。
---

# TiKV MVCC 内存引擎

TiKV MVCC 内存引擎 (In-Memory Engine, IME) 主要用于加速需要扫描大量 MVCC 历史版本的查询，即[查询扫描的总共版本数量 (`total_keys`) 远大于处理的版本数量 (`processed_keys`)](/analyze-slow-queries.md#过期-mvcc-版本和-key-过多)。

TiKV MVCC 内存引擎适用于以下场景：

- 业务需要查询频繁更新或删除的记录。
- 业务需要调整 [`tidb_gc_life_time`](/garbage-collection-configuration.md#gc-配置)，使 TiDB 保留较长时间的历史版本（比如 24 小时）。

## 工作原理

TiKV MVCC 内存引擎在内存中缓存最近写入的 MVCC 版本，并实现独立于 TiDB 的 MVCC GC 机制，使其可快速 GC 内存中的 MVCC 记录，从而减少查询时扫描版本的个数，以达到降低请求延时和减少 CPU 开销的效果。

下图为 TiKV 如何组织 MVCC 版本的示意图：

![IME 通过缓存近期的版本以减少 CPU 开销](/media/tikv-ime-data-organization.png)

以上示意图中共有 2 行记录，每行记录各有 9 个 MVCC 版本。在开启内存引擎和未开启内存引擎的情况下，行为对比如下：

- 左侧（未开启内存引擎）：表中记录按主键升序保存在 RocksDB 中，相同行的 MVCC 版本紧邻在一起。
- 右侧（开启了内存引擎）：RocksDB 中的数据与左侧一致，同时内存引擎缓存了 2 行记录最新的 2 个 MVCC 版本。
- 当 TiKV 处理一个范围为 `[k1, k2]`，开始时间戳为 `8` 的扫描请求时：
    - 左侧未开启内存引擎时需要处理 11 个 MVCC 版本。
    - 右侧开启内存引擎时只需处理 4 个 MVCC 版本，因此减少了请求延时和 CPU 消耗。
- 当 TiKV 处理一个范围为 `[k1, k2]`，开始时间戳为 `7` 的扫描请求时：
    - 由于右侧缺少需要读取的历史版本，因此内存引擎缓存失效，回退到读取 RocksDB 中的数据。

## 使用方式

如果要开启 TiKV MVCC 内存引擎 (IME) 功能，需要调整 [TiKV 配置](/tikv-configuration-file.md#in-memory-engine-从-v850-版本开始引入)并重启 TiKV。以下是配置说明：

```toml
[in-memory-engine]
# 该参数为内存引擎功能的开关，默认为 false，调整为 true 即可开启。
enable = false

# 该参数控制内存引擎可使用的内存大小。默认值为系统内存的 10%，同时最大值为 5 GiB，
# 可通过手动调整配置以使用更多内存。
# 注意：当内存引擎开启后，block-cache.capacity 会减少 10%。
capacity = "5GiB"

# 该参数控制内存引擎 GC 缓存 MVCC 的版本的时间间隔。
# 默认为 3 分钟，代表每 3 分钟 GC 一次缓存的 MVCC 版本。
# 调小该参数可加快 GC 频率，减少 MVCC 记录，但会增加 GC CPU 的消耗和增加内存引擎失效的概率。
gc-run-interval = "3m"

# 该参数控制内存引擎选取加载 Region 时 MVCC 读放大的阈值。
# 默认为 10，表示在某个 Region 中读一行记录需要处理的 MVCC 版本数量超过 10 个时，将有可能会被加载到内存引擎中。
mvcc-amplification-threshold = 10
```

> **注意：**
>
> + 内存引擎默认关闭，并且从关闭状态修改为开启状态后，需要重启 TiKV。
> + 除 `enable` 之外，其他配置都可以动态调整。

### 自动加载

开启内存引擎之后，TiKV 会根据 Region 的读流量和 MVCC 放大程度，选择要自动加载的 Region。具体流程如下：

1. Region 按照最近时间段的 `next` (RocksDB Iterator next API) 和 `prev` (RocksDB Iterator prev API) 次数进行排序。
2. 使用 `mvcc-amplification-threshold` 配置项对 Region 进行过滤，该配置项的默认值为 `10`。MVCC amplification 衡量读放大程度，计算公式为 (`next` + `prev`) / `processed_keys`）。
3. 载入前 N 个 MVCC 放大严重的 Region，其中 N 基于内存估算而来。

内存引擎也会定期驱逐 Region。具体流程如下：

1. 内存引擎会驱逐那些读流量过小或者 MVCC 放大程度过低的 Region。
2. 如果内存使用达到了 `capacity` 的 90%，并且有新的 Region 需要被载入，那么内存引擎会根据读取流量来筛选 Region 并进行驱逐。

## 兼容性

+ [BR](/br/br-use-overview.md)：内存引擎与 BR 可同时使用，但 BR restore 会驱逐内存引擎中涉及恢复的 Region，BR restore 完成后，如果对应 Region 还是热点，则会被内存引擎自动加载。
+ [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：内存引擎与 TiDB Lightning 可同时使用，但 TiDB Lightning 的物理导入模式会驱逐内存引擎中涉及恢复的 Region，TiDB Lightning 使用物理导入模式完成导入数据后，如果对应 Region 还是热点，则会被内存引擎自动加载。
+ [Follower Read](/develop/dev-guide-use-follower-read.md) 与 [Stale Read](/develop/dev-guide-use-stale-read.md)：内存引擎可与这两个特性同时开启，但内存引擎只能加速 Leader 上的 coprocessor 请求，无法加速 Follower Read 和 Stale Read。
+ [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)：内存引擎与 Flashback 可同时使用，但 Flashback 会导致内存引擎缓存失效。Flashback 完成后，内存引擎会自动加载热点 Region。

## FAQ

### 内存引擎能否减少写入延时，提高写入吞吐？

不能。内存引擎只能加速扫描了大量 MVCC 版本的读请求。

### 如何判断内存引擎是否能改善我的场景？

可以通过执行以下 SQL 语句查看是否存在 `Total_keys` 远大于 `Process_keys` 的慢查询：

```sql
SELECT
    Time,
    DB,
    Index_names,
    Process_keys,
    Total_keys,
    CONCAT(
        LEFT(REGEXP_REPLACE(Query, '\\s+', ' '), 20),
        '...',
        RIGHT(REGEXP_REPLACE(Query, '\\s+', ' '), 10)
    ) as Query,
    Query_time,
    Cop_time,
    Process_time
FROM
    INFORMATION_SCHEMA.SLOW_QUERY
WHERE
    Is_internal = 0
    AND Cop_time > 1
    AND Process_keys > 0
    AND Total_keys / Process_keys >= 10
    AND Time >= NOW() - INTERVAL 10 MINUTE
ORDER BY Total_keys DESC
LIMIT 5;
```

示例：

以下结果显示 `db1.tbl1` 表上存在 MVCC 放大严重的查询，TiKV 在处理 1358517 个 MVCC 版本后，仅返回了 2 个版本。

```
+----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
| Time                       | DB  | Index_names       | Process_keys | Total_keys | Query                             | Query_time         | Cop_time           | Process_time       |
+----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
| 2024-11-18 11:56:10.303228 | db1 | [tbl1:some_index] |            2 |    1358517 |  SELECT * FROM tbl1 ... LIMIT 1 ; | 1.2581352350000001 |         1.25651062 |        1.251837479 |
| 2024-11-18 11:56:11.556257 | db1 | [tbl1:some_index] |            2 |    1358231 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.252694002 |        1.251129038 |        1.240532546 |
| 2024-11-18 12:00:10.553331 | db1 | [tbl1:some_index] |            2 |    1342914 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.473941872 | 1.4720495900000001 | 1.3666103170000001 |
| 2024-11-18 12:01:52.122548 | db1 | [tbl1:some_index] |            2 |    1128064 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.058942591 |        1.056853228 |        1.023483875 |
| 2024-11-18 12:01:52.107951 | db1 | [tbl1:some_index] |            2 |    1128064 |  SELECT * FROM tbl1 ... LIMIT 1 ; |        1.044847031 |        1.042546122 |        0.934768555 |
+----------------------------+-----+-------------------+--------------+------------+-----------------------------------+--------------------+--------------------+--------------------+
5 rows in set (1.26 sec)
```

### 如何判断 TiKV MVCC 内存引擎是否开启？

你可以使用 [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) 语句查看 TiKV 配置：

```sql
SHOW CONFIG WHERE Type='tikv' AND Name LIKE 'in-memory-engine\.%';
```

```
+------+-----------------+-----------------------------------------------+---------+
| Type | Instance        | Name                                          | Value   |
+------+-----------------+-----------------------------------------------+---------+
| tikv | 127.0.0.1:20160 | in-memory-engine.capacity                     | 5GiB    |
| tikv | 127.0.0.1:20160 | in-memory-engine.cross-check-interval         | 0s      |
| tikv | 127.0.0.1:20160 | in-memory-engine.enable                       | true    |
| tikv | 127.0.0.1:20160 | in-memory-engine.evict-threshold              | 4920MiB |
| tikv | 127.0.0.1:20160 | in-memory-engine.gc-run-interval              | 3m      |
| tikv | 127.0.0.1:20160 | in-memory-engine.load-evict-interval          | 5m      |
| tikv | 127.0.0.1:20160 | in-memory-engine.mvcc-amplification-threshold | 10      |
| tikv | 127.0.0.1:20160 | in-memory-engine.stop-load-threshold          | 4208MiB |
+------+-----------------+-----------------------------------------------+---------+
8 rows in set (0.00 sec)
```

### 如何监控 TiKV MVCC 内存引擎？

你可以查看 [TiKV-Details 面板](/grafana-tikv-dashboard.md) 的 **In Memory Engine** 部分。