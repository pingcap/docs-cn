---
title: TiDB 8.4.0 Release Notes
summary: 了解 TiDB 8.4.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.4.0 Release Notes

发版日期：2024 年 11 月 11 日

TiDB 版本：8.4.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.4/quick-start-with-tidb) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.4.0-DMR#version-list)

在 8.4.0 版本中，你可以获得以下关键特性：

<table>
<thead>
  <tr>
    <th>分类</th>
    <th>功能/增强</th>
    <th>描述</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td rowspan="4">可扩展性和性能</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/system-variables#tidb_enable_instance_plan_cache-从-v840-版本开始引入">实例级执行计划缓存</a>（实验特性）</td>
    <td>实例级执行计划缓存允许同一个 TiDB 实例的所有会话共享执行计划缓存。与现有的会话级执行计划缓存相比，实例级执行计划缓存能够在内存中缓存更多执行计划，减少 SQL 编译时间，从而降低 SQL 整体运行时间，提升 OLTP 的性能和吞吐，同时更好地控制内存使用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/partitioned-table#全局索引">分区表全局索引成为正式功能</a></td>
    <td>全局索引可以有效提高检索非分区列的效率，并且消除了唯一键必须包含分区键的限制。该功能扩展了 TiDB 分区表的使用场景，避免了数据迁移过程中的一些应用修改工作。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/system-variables#tidb_tso_client_rpc_mode-从-v840-版本开始引入">TiDB 并行获取 TSO</a></td>
    <td>在高并发场景下，并行获取 TSO 能够有效降低等待获取 TSO 的时间，提升集群的吞吐。</td>
  </tr>
  <tr>
    <td>提升<a href="https://docs.pingcap.com/zh/tidb/v8.4/cached-tables#缓存表">缓存表</a>的查询性能</td>
    <td>优化了缓存表索引扫描的查询性能，部分场景可提升 5.4 倍。在需要对小表进行高速查询的场景下，利用缓存表可大幅提升整体性能。</td>
  </tr>
  <tr>
    <td rowspan="4">稳定性与高可用</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/tidb-resource-control#query_limit-参数说明">Runaway Queries 支持更多触发条件，并能够切换资源组</a></td>
    <td>Runaway Queries 提供了有效的手段来降低突发的 SQL 性能问题对系统产生的影响。v8.4.0 中新增 Coprocessor 处理的 Key 的数量 (<code>PROCESSED_KEYS</code>) 和 Request Unit (<code>RU</code>) 作为识别条件，并可以将识别到的查询置入指定资源组，对 Runaway Queries 进行更精确的识别与控制。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/tidb-resource-control#background-参数说明">支持为资源管控的后台任务设置资源使用上限</a></td>
    <td>为资源管控的后台任务设置百分比上限，针对不同业务系统的需求，控制后台任务的消耗，从而将后台任务的消耗限制在一个很低的水平，保证在线业务的服务质量。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/tiproxy-traffic-replay">TiProxy 流量捕获和回放</a>（实验特性）</td>
    <td>在进行集群升级、迁移或部署变更等重要操作之前，使用 TiProxy 捕获 TiDB 生产集群的真实负载，并在测试的目标集群中重现该工作负载，从而验证性能，确保变更成功。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/system-variables#tidb_auto_analyze_concurrency-从-v840-版本开始引入">自动统计信息收集任务支持并发</a></td>
    <td>使用系统变量 <code>tidb_auto_analyze_concurrency</code> 控制单个自动统计信息收集任务内部的并发度，TiDB 会根据节点规模和硬件规格自动确定扫描任务的并发度。该功能通过充分利用系统资源，提高统计信息收集效率，从而减少手动调优，并确保集群性能稳定。</td>
  </tr>
  <tr>
    <td rowspan="1">SQL</td>
    <td>支持<a href="https://docs.pingcap.com/zh/tidb/v8.4/vector-search-overview">向量搜索功能</a>（实验特性）</td>
    <td>向量搜索是一种基于数据语义的搜索方法，可以提供更相关的搜索结果。作为 AI 和大语言模型 (LLM) 的核心功能之一，向量搜索可用于检索增强生成 (Retrieval-Augmented Generation, RAG)、语义搜索、推荐系统等多种场景。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理和可观测性</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/information-schema-processlist">在内存表中显示 TiKV 和 TiDB 的 CPU 时间</a></td>
    <td>将 CPU 时间合入系统表中展示，与会话或 SQL 的其他指标并列，方便你从多角度对高 CPU 消耗的操作进行观测，提升诊断效率。尤其适用于诊断实例 CPU 飙升或集群读写热点等场景。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/top-sql#使用-top-sql">按表或数据库维度聚合 TiKV 消耗的 CPU 时间</a></td>
    <td>当热点问题不是由个别 SQL 语句引起时，利用 Top SQL 中按表或者数据库聚合的 CPU 时间，能够协助用户快速发现造成热点的表或者应用程序，从而大大提升热点问题和 CPU 消耗问题的诊断效率。</td>
  </tr>
  <tr>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/backup-and-restore-storages#鉴权">支持对开启了 IMDSv2 服务的 TiKV 实例做备份</a></td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">目前 AWS EC2 的默认元数据服务是 IMDSv2</a>。TiDB 支持从开启了 IMDSv2 的 TiKV 实例中备份数据，协助你更好地在公有云服务中运行 TiDB 集群。</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td><a href="https://docs.pingcap.com/zh/tidb/v8.4/br-pitr-manual#加密日志备份数据">日志备份数据支持客户端加密</a>（实验特性）</td>
    <td>在上传日志备份到备份存储之前，你可以对日志备份数据进行加密，确保数据在存储和传输过程中的安全性。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 性能

* 新增 TSO 请求的并行批处理模式，降低获取 TSO 的延迟 [#54960](https://github.com/pingcap/tidb/issues/54960) [#8432](https://github.com/tikv/pd/issues/8432) @[MyonKeminta](https://github.com/MyonKeminta)

    在 v8.4.0 之前，TiDB 向 PD 请求 [TSO](/tso.md) 时会将一段时间内的请求汇总起来并以串行的方式进行批处理，以减少 RPC (Remote Procedure Call) 请求数量，从而降低 PD 负载。对于延迟敏感的场景，这种串行模式的性能并不理想。

    在 v8.4.0 中，TiDB 新增 TSO 请求的并行批处理模式，并提供不同的并发能力。并行模式可以降低获取 TSO 的延迟，但可能会增加 PD 的负载。你可以通过 [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 变量设定获取 TSO 的 RPC 模式。

    更多信息，请参考[用户文档](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入)。

* 优化 TiDB Hash Join 算子的执行效率（实验特性）[#55153](https://github.com/pingcap/tidb/issues/55153) [#53127](https://github.com/pingcap/tidb/issues/53127) @[windtalker](https://github.com/windtalker) @[xzhangxian1008](https://github.com/xzhangxian1008) @[XuHuaiyu](https://github.com/XuHuaiyu) @[wshwsh12](https://github.com/wshwsh12)

    在 v8.4.0 中，TiDB 对 Hash Join 算子的实现方法进行了优化，以提升其执行效率。目前，优化版的 Hash Join 仅对 Inner Join 和 Outer Join 操作生效，且默认关闭。如需开启优化版的 Hash Join，可以将系统变量 [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入) 设置为 `optimized`。

    更多信息，请参考[用户文档](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入)。

* 支持下推以下日期函数到 TiKV [#56297](https://github.com/pingcap/tidb/issues/56297) [#17529](https://github.com/tikv/tikv/issues/17529) @[gengliqi](https://github.com/gengliqi)

    * `DATE_ADD()`
    * `DATE_SUB()`
    * `ADDDATE()`
    * `SUBDATE()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 支持实例级执行计划缓存（实验特性）[#54057](https://github.com/pingcap/tidb/issues/54057) @[qw4990](https://github.com/qw4990)

    实例级执行计划缓存允许同一个 TiDB 实例上的所有会话共享执行计划缓存。该功能可以大幅降低 TiDB 的查询响应时间，提升集群吞吐，减少执行计划突变的可能性，并保持集群性能的稳定。相比会话级执行计划缓存，实例级执行计划缓存具有以下优势：

    - 消除冗余，在相同的内存消耗下缓存更多执行计划。
    - 在实例上分配固定大小的内存区域，更有效地限制内存使用。

  在 v8.4.0 中，实例级执行计划缓存仅支持对查询的执行计划进行缓存，且默认关闭。你可以通过系统变量 [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入) 开启该功能，并通过系统变量 [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-从-v840-版本开始引入) 设置其最大内存使用量。开启该功能之前，请关闭会话级别的 [Prepare 语句执行计划缓存](/sql-prepared-plan-cache.md)和[非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)。

    更多信息，请参考[用户文档](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入)。

* TiDB Lightning 的逻辑导入模式支持预处理语句和客户端语句缓存 [#54850](https://github.com/pingcap/tidb/issues/54850) @[dbsid](https://github.com/dbsid)

    通过开启配置项 `logical-import-prep-stmt`，TiDB Lightning 逻辑导入模式中执行的 SQL 语句将通过使用预处理语句和客户端语句缓存，降低 TiDB SQL 解析和编译的成本，提升 SQL 执行效率，并有更大机会命中执行计划缓存，提升逻辑导入的速度。

    更多信息，请参考[用户文档](/tidb-lightning/tidb-lightning-configuration.md)。

* 分区表的全局索引成为正式功能 (GA) [#45133](https://github.com/pingcap/tidb/issues/45133) @[mjonss](https://github.com/mjonss) @[Defined2014](https://github.com/Defined2014) @[jiyfhust](https://github.com/jiyfhust) @[L-maple](https://github.com/L-maple)

    之前版本的分区表，因为不支持全局索引有较多的限制，比如唯一键必须包含分区表达式中用到的所有列，如果查询条件不带分区键，查询时会扫描所有分区，导致性能较差。从 v7.6.0 开始，引入了系统变量 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) 用于开启全局索引特性，但该功能当时处于开发中，不够完善，不建议开启。

    从 v8.3.0 开始，全局索引作为实验特性正式发布。你可通过关键字 `GLOBAL` 为分区表显式创建一个全局索引，从而去除分区表唯一键必须包含分区表达式中用到的所有列的限制，满足灵活的业务需求。同时基于全局索引也提升了非分区列的查询性能。

    在 v8.4.0 中，全局索引成为正式功能 (GA)。你无需再设置系统变量 [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) 开启全局索引特性，可以直接使用关键字 `GLOBAL` 创建全局索引。从 v8.4.0 开始，该系统变量被废弃，并总是设置为 `ON`。

    更多信息，请参考[用户文档](/partitioned-table.md#全局索引)。

* 优化缓存表在部分场景下的查询性能 [#43249](https://github.com/pingcap/tidb/issues/43249) @[tiancaiamao](https://github.com/tiancaiamao)

    优化缓存表的查询性能，在使用 `IndexLookup` 执行 `SELECT ... LIMIT 1` 时，性能最高提升 5.4 倍。同时，提升 `IndexLookupReader` 在全表扫描和主键查询场景下的性能。

### 稳定性

* 超出预期的查询 (Runaway Queries) 新增处理行数和 Request Unit 作为阈值 [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp)

    从 v8.4.0 开始， TiDB 可以依据处理行数 (`PROCESSED_KEYS`) 和 Request Unit (`RU`) 定义超出预期的查询。和执行时间 (`EXEC_ELAPSED`) 相比，新增阈值能够更准确地定义查询的资源消耗，避免整体性能下降时发生识别偏差。

    支持同时设置多个条件，满足任意条件即识别为 `Runaway Queries`。

    可以观测 [Statement Summary Tables](/statement-summary-tables.md) 中的几个对应字段 (`RESOURCE_GROUP`、`MAX_REQUEST_UNIT_WRITE`、`MAX_REQUEST_UNIT_READ`、`MAX_PROCESSED_KEYS`)，根据历史执行情况决定条件值的大小。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* 超出预期的查询 (Runaway Queries) 支持切换资源组 [#54434](https://github.com/pingcap/tidb/issues/54434) @[JmPotato](https://github.com/JmPotato)

    v8.4.0 新增支持将 Runaway Queries 切换到指定资源组。在降低优先级 (COOLDOWN) 仍旧无法有效降低资源消耗的情况下，你可以创建一个[资源组 (Resource Group)](/tidb-resource-control.md#创建资源组)并限制其资源上限，通过配置参数 `SWITCH_GROUP` 指定将识别到的查询切换到该资源组中，会话的后续查询仍在原资源组中执行。切换资源组的行为能够更精确地限制资源使用，对 Runaway Queries 的资源消耗做更加严格的控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#query_limit-参数说明)。

* 支持使用系统变量 `tidb_scatter_region` 设置集群级别的 Region 打散策略 [#55184](https://github.com/pingcap/tidb/issues/55184) @[D3Hunter](https://github.com/D3Hunter)

    在 v8.4.0 之前，系统变量 `tidb_scatter_region` 仅支持设置为开启或者关闭。开启后，建表时会使用表级别打散策略。在批量快速建表，且表的数量达到几十万张后，该策略会导致 Region 集中分布在其中几个 TiKV 节点，导致这些 TiKV 节点 OOM。

    从 v8.4.0 开始，该系统变量改为字符串类型，且新增支持集群级别的打散策略，避免上述场景下导致 TiKV OOM 的问题。

    更多信息，请参考[用户文档](/system-variables.md#tidb_scatter_region)。

* 支持为资源管控的后台任务设置资源上限 [#56019](https://github.com/pingcap/tidb/issues/56019) @[glorv](https://github.com/glorv)

    TiDB 资源管控能够识别并降低后台任务的运行优先级。在部分场景下，即使有空闲资源，用户也希望后台任务消耗能够控制在很低的水平。从 v8.4.0 开始，你可以使用参数 `UTILIZATION_LIMIT` 为资源管控的后台任务设置最大可以使用的资源百分比，每个节点把所有后台任务的使用量控制在这个百分比以下。该功能可以让你精细控制后台任务的资源占用，进一步提升集群稳定性。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理后台任务)。

* 优化资源组资源分配策略 [#50831](https://github.com/pingcap/tidb/issues/50831) @[nolouch](https://github.com/nolouch)

    TiDB 在 v8.4.0 部分调整了资源分配策略，更好地满足用户对资源管控的预期。

    - 控制大查询在运行时的资源分配，避免超出资源组限额。配合 Runaway Queries 的 `COOLDOWN` 动作，识别并降低大查询并发度，降低瞬时资源消耗。
    - 调整默认的优先级调度策略。当不同优先级的任务同时运行时，高优先级的任务获得更多资源。

### 高可用

* TiProxy 支持流量回放功能（实验特性）[#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832)

    从 TiProxy v1.3.0 开始，你可以使用 `tiproxyctl` 连接 TiProxy 实例，捕获 TiDB 生产集群中的访问流量，并在测试集群中按照指定的速率回放这些流量。通过该功能，你可以在测试环境中重现生产集群的实际工作负载，从而验证所有 SQL 的执行结果和性能表现。

    流量回放适用于以下场景：

    - TiDB 版本升级前验证
    - 执行变更前影响评估
    - TiDB 扩缩容前性能验证
    - 集群性能上限测试

  更多信息，请参考[用户文档](/tiproxy/tiproxy-traffic-replay.md)。

### SQL 功能

* 支持向量搜索功能（实验特性）[#54245](https://github.com/pingcap/tidb/issues/54245) [#17290](https://github.com/tikv/tikv/issues/17290) [#9032](https://github.com/pingcap/tiflash/issues/9032) @[breezewish](https://github.com/breezewish) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[EricZequan](https://github.com/EricZequan) @[zimulala](https://github.com/zimulala) @[JaySon-Huang](https://github.com/JaySon-Huang) @[winoros](https://github.com/winoros) @[wk989898](https://github.com/wk989898)

    向量搜索是一种基于数据语义的搜索方法，可以提供更相关的搜索结果。作为 AI 和大语言模型 (LLM) 的核心功能之一，向量搜索可用于检索增强生成 (Retrieval-Augmented Generation, RAG)、语义搜索、推荐系统等多种场景。

    从 v8.4.0 开始，TiDB 支持[向量数据类型](/vector-search/vector-search-data-types.md)和[向量搜索索引](/vector-search/vector-search-index.md)，具备强大的向量搜索能力。TiDB 的向量数据类型最多可支持 16383 维度，并支持多种[距离函数](/vector-search/vector-search-functions-and-operators.md#向量函数)，包括 L2 距离（欧式距离）、余弦距离、负内积和 L1 距离（曼哈顿距离）。

    在使用时，你只需要创建包含向量数据类型的表，并插入向量数据，即可执行向量搜索查询，也可进行向量数据与传统关系数据的混合查询。

    此外，你可以创建并利用[向量搜索索引](/vector-search/vector-search-index.md)来提升向量搜索的性能。需要注意的是，TiDB 的向量搜索索引依赖于 TiFlash。在使用向量搜索索引之前，需要确保 TiDB 集群中已部署 TiFlash 节点。

    更多信息，请参考[用户文档](/vector-search/vector-search-overview.md)。

### 数据库管理

* 日志备份数据支持客户端加密（实验特性）[#55834](https://github.com/pingcap/tidb/issues/55834) @[Tristan1900](https://github.com/Tristan1900)

    在之前的版本中，仅快照备份数据支持客户端加密。从 v8.4.0 起，日志备份数据也支持客户端加密。在上传日志备份到备份存储之前，你可以选择以下方式之一对日志备份数据进行加密，从而确保备份数据的安全性：

    - 使用自定义的固定密钥加密
    - 使用本地磁盘的主密钥加密
    - 使用 KMS（密钥管理服务）的主密钥加密

  更多信息，请参考[用户文档](/br/br-pitr-manual.md#加密日志备份数据)。

* BR 降低了从云存储服务系统恢复数据的权限要求 [#55870](https://github.com/pingcap/tidb/issues/55870) @[Leavrth](https://github.com/Leavrth)

    在 v8.4.0 之前，BR 在恢复过程中会将恢复进度的检查点信息写入到备份存储系统。当恢复过程出现中断时，这些检查点使中断的恢复操作能够快速恢复。从 v8.4.0 开始，BR 将恢复检查点信息写入到目标 TiDB 集群中。这意味着 BR 在恢复时只需要具备对备份目录的读取权限。

    更多信息，请参考[用户文档](/br/backup-and-restore-storages.md#鉴权)。

### 可观测性

* 在系统表中显示 TiDB 和 TiKV 消耗的 CPU 时间 [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87)

    [TiDB Dashboard](/dashboard/dashboard-intro.md) 的 [Top SQL 页面](/dashboard/top-sql.md)能够展示 CPU 消耗高的 SQL 语句。从 v8.4.0 开始，TiDB 将 CPU 时间消耗信息加入系统表展示，与会话或 SQL 的其他指标并列，方便你从多角度对高 CPU 消耗的操作进行观测。在实例 CPU 飙升或集群读写热点的场景下，这些信息能够协助你快速发现问题的原因。

    - [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 增加 `AVG_TIDB_CPU_TIME` 和 `AVG_TIKV_CPU_TIME`，显示单个 SQL 语句在历史上消耗 CPU 的平均时间。
    - [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 增加 `TIDB_CPU` 和 `TIKV_CPU`，显示会话当前正在执行 SQL 的累计 CPU 时间消耗。
    - [慢日志](/analyze-slow-queries.md)中增加字段 `Tidb_cpu_time` 和 `Tikv_cpu_time`，显示被捕捉到的 SQL 语句消耗 CPU 的时间。

  其中，TiKV 的 CPU 时间默认显示。采集 TiDB 的 CPU 时间会引入额外开销（约 8%），因此仅在开启 [Top SQL 特性](/dashboard/top-sql.md)时，TiDB 的 CPU 时间才会显示为实际值，否则始终显示为 `0`。

    更多信息，请参考 [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 和 [`INFORMATION_SCHEMA.SLOW_QUERY`](/information-schema/information-schema-slow-query.md)。

* Top SQL 支持按表或数据库维度查看 CPU 时间的聚合结果 [#55540](https://github.com/pingcap/tidb/issues/55540) @[nolouch](https://github.com/nolouch)

    在 v8.4.0 之前，[Top SQL](/dashboard/top-sql.md) 以 SQL 为单位来聚合 CPU 时间。如果 CPU 时间不是由少数几个 SQL 贡献，按 SQL 聚合并不能有效发现问题。从 v8.4.0 开始，你可以选择 **By TABLE** 或者 **By DB** 聚合 CPU 时间。在多系统融合的场景下，新的聚合方式能够更有效地识别来自某个特定系统的负载变化，提升问题诊断的效率。

    更多信息，请参考[用户文档](/dashboard/top-sql.md#使用-top-sql)。

### 安全

* BR 支持 AWS IMDSv2 [#16443](https://github.com/tikv/tikv/issues/16443) @[pingyu](https://github.com/pingyu)

    在 Amazon EC2 上部署 TiDB 时，BR 支持 AWS 的 Instance Metadata Service Version 2 (IMDSv2)。你可以在 EC2 实例上进行相关配置，使 BR 可以使用与实例关联的 IAM 角色以适当的权限访问 Amazon S3。

    更多信息，请参考[用户文档](/br/backup-and-restore-storages.md#鉴权)。

### 数据迁移

* TiCDC Claim-Check 支持仅发送 Kafka 消息的 `value` 部分到外部存储 [#11396](https://github.com/pingcap/tiflow/issues/11396) @[3AceShowHand](https://github.com/3AceShowHand)

    在 v8.4.0 之前，如果开启了 Claim-Check 功能 （将 `large-message-handle-option` 设置为 `claim-check`），TiCDC 在处理大型消息时会将 `key` 和 `value` 都进行编码并存储在外部存储系统中。

    从 v8.4.0 开始，TiCDC 支持仅将 Kafka 消息的 `value` 部分发送到外部存储，该功能仅适用于非 Open Protocol 协议。你可以通过设置 `claim-check-raw-value` 参数控制是否开启该功能。

    更多信息，请参考[用户文档](/ticdc/ticdc-sink-to-kafka.md#只发送-value-部分到外部存储)。

* TiCDC 引入 Checksum V2 算法校验 Update 或 Delete 事件中 Old Value 数据 [#10969](https://github.com/pingcap/tiflow/issues/10969) @[3AceShowHand](https://github.com/3AceShowHand)

    从 v8.4.0 开始，TiDB 和 TiCDC 引入 Checksum V2 算法，解决了 Checksum V1 在执行 `ADD COLUMN` 或 `DROP COLUMN` 后无法正确校验 Update 或 Delete 事件中 Old Value 数据的问题。对于 v8.4.0 及之后新创建的集群，或从之前版本升级到 v8.4.0 的集群，启用单行数据 Checksum 正确性校验功能后，TiDB 默认使用 Checksum V2 算法进行 Checksum 计算和校验。TiCDC 支持同时处理 V1 和 V2 两种 Checksum。该变更仅影响 TiDB 和 TiCDC 内部实现，不影响下游 Kafka consumer 的 Checksum 计算校验方法。

    更多信息，请参考[用户文档](/ticdc/ticdc-integrity-check.md)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.3.0 升级至当前版本 (v8.4.0) 所需兼容性变更信息。如果从 v8.2.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 系统变量

| 变量名 | 修改类型 | 描述 |
|--------|------------------------------|------|
| `log_bin` | 删除 | 从 v8.4.0 开始，[TiDB Binlog](https://docs.pingcap.com/zh/tidb/v8.3/tidb-binlog-overview) 被移除。该变量表示是否使用 TiDB Binlog，从 v8.4.0 开始被删除。|
| `sql_log_bin` | 删除 | 从 v8.4.0 开始，[TiDB Binlog](https://docs.pingcap.com/zh/tidb/v8.3/tidb-binlog-overview) 被移除。该变量表示是否将更改写入 TiDB Binlog，从 v8.4.0 开始被删除。|
| [`tidb_enable_global_index`](/system-variables.md#tidb_enable_global_index-从-v760-版本开始引入) | 废弃 | 从 v8.4.0 开始，该变量被废弃。其值将固定为默认值 `ON`，即默认启用[全局索引](/partitioned-table.md#全局索引)。你只需在执行 `CREATE TABLE` 或 `ALTER TABLE` 时给对应的列加上关键字 `GLOBAL` 即可创建全局索引。|
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-从-v50-版本开始引入) | 废弃 | 从 v8.4.0 开始，该变量被废弃。其值将固定为默认值 `ON`，即默认启用 [List 分区](/partitioned-table.md#list-分区)。|
| [`tidb_enable_table_partition`](/system-variables.md#tidb_enable_table_partition) | 废弃 |  从 v8.4.0 开始，该变量被废弃。其值将固定为默认值 `ON`，即默认启用[分区表](/partitioned-table.md)。|
| [`tidb_analyze_partition_concurrency`](/system-variables.md#tidb_analyze_partition_concurrency) | 修改 | 取值范围从 `[1, 18446744073709551615]` 修改为 `[1, 128]`。|
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-从-v700-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`。从 v8.4.0 开始，当内表上有 `Selection`、`Projection` 或 `Aggregation` 算子时，默认支持 Index Join。 |
| [`tidb_opt_prefer_range_scan`](/system-variables.md#tidb_opt_prefer_range_scan-从-v50-版本开始引入) | 修改 | 默认值从 `OFF` 修改为 `ON`。对于没有统计信息的表（伪统计信息）或空表（零统计信息），优化器将优先选择区间扫描而不是全表扫描。|
| [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) | 修改 | 在 v8.4.0 之前，该变量为布尔型，仅支持开启或关闭，且开启后新建表的 Region 只支持表级别打散。从 v8.4.0 开始，增加 `SESSION` 作用域，类型由布尔型变更为枚举型，默认值由原来的 `OFF` 变更为空，表示不打散表 Region，并增加了可选值 `TABLE` 和 `GLOBAL`。支持集群级别的打散策略，避免快速批量建表时由于 Region 分布不均匀导致 TiKV OOM 的问题。|
| [`tidb_schema_cache_size`](/system-variables.md#tidb_schema_cache_size-从-v800-版本开始引入) | 修改 | 默认值从 `0` 修改为 `536870912`（即 512 MiB），表示默认开启该功能，且最小值允许设置为 `67108864`（即 64 MiB）。|
| [`tidb_auto_analyze_concurrency`](/system-variables.md#tidb_auto_analyze_concurrency-从-v840-版本开始引入)| 新增 | 设置单个自动统计信息收集任务内部的并发度。在 v8.4.0 之前，该并发度固定为 `1`。你可以根据集群资源情况提高该并发度，从而加快统计信息收集任务的执行速度。|
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入)| 新增 | 控制是否开启 Instance Plan Cache 功能。|
| [`tidb_enable_stats_owner`](/system-variables.md#tidb_enable_stats_owner-从-v840-版本开始引入)| 新增 | 设置该 TiDB 实例是否可以运行统计信息自动更新任务。|
| [`tidb_hash_join_version`](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入) | 新增 | 控制 TiDB 是否使用 Hash Join 算子的优化版。默认值为 `legacy`，表示不使用优化版。如果设置为 `optimized`，TiDB 在执行 Hash Join 算子时将使用其优化版，以提升 Hash Join 性能。|
| [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-从-v840-版本开始引入) | 新增 | 设置 Instance Plan Cache 的最大内存使用量。|
| [`tidb_instance_plan_cache_reserved_percentage`](/system-variables.md#tidb_instance_plan_cache_reserved_percentage-从-v840-版本开始引入) | 新增 | 控制内存驱逐后 Instance Plan Cache 的空闲内存百分比。|
| [`tidb_pre_split_regions`](/system-variables.md#tidb_pre_split_regions-从-v840-版本开始引入) | 新增 | 在 v8.4.0 之前，要设置新建表默认的行分裂分片数，需要在每个 `CREATE TABLE` SQL 语句里声明 `PRE_SPLIT_REGIONS`，一旦需要同样配置的表数量较多，操作复杂。为解决这些问题，引入了该变量。你可以在 `GLOBAL` 或 `SESSION` 级别设置该系统变量，提升易用性。  |
| [`tidb_shard_row_id_bits`](/system-variables.md#tidb_shard_row_id_bits-从-v840-版本开始引入) | 新增 | 在 v8.4.0 之前，要设置新建表默认的行 ID 的分片数，需要在每个 `CREATE TABLE` 或 `ALTER TABLE` 的 SQL 语句里声明 `SHARD_ROW_ID_BITS`，一旦需要同样配置的表数量较多，操作复杂。为解决这些问题，引入了该变量。你可以在 `GLOBAL` 或 `SESSION` 级别设置该系统变量，提升易用性。  |
| [`tidb_tso_client_rpc_mode`](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入) | 新增 | 设置 TiDB 向 PD 发送 TSO RPC 请求时使用的模式。这里的模式将用于控制 TSO RPC 请求是否并行，调节获取 TS 时消耗在请求攒批阶段的时间，从而在某些场景中减少执行查询时等待 TS 阶段的时间。 |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
| TiDB | [`grpc-keepalive-time`](/tidb-configuration-file.md#grpc-keepalive-time) | 修改 | 增加最小值 `1`。|
| TiDB | [`grpc-keepalive-timeout`](/tidb-configuration-file.md#grpc-keepalive-timeout) | 修改 | 在 v8.4.0 之前，该参数为 INT 类型，且最小值仅支持设置为 `1`。从 v8.4.0 开始，数据类型修改为 FLOAT64，且最小值支持设置为 `0.05`。在网络抖动比较频繁的场景中可以适当调小该值，通过减少重试间隔，来减少网络抖动带来的性能影响。|
| TiDB | [`tidb_enable_stats_owner`](/tidb-configuration-file.md#tidb_enable_stats_owner-从-v840-版本开始引入) | 新增 | 表示该 tidb-server 是否可以运行统计信息自动更新任务。|
| TiKV | [`region-split-keys`](/tikv-configuration-file.md#region-split-keys) | 修改 | 默认值从 `"960000"` 修改为 `"2560000"`。|
| TiKV | [`region-split-size`](/tikv-configuration-file.md#region-split-size) | 修改 | 默认值从 `"96MiB"` 修改为 `"256MiB"`。|
| TiKV | [`sst-max-size`](/tikv-configuration-file.md#sst-max-size) | 修改 | 默认值从 `"144MiB"` 修改为 `"384MiB"`。|
| TiKV | [`pessimistic-txn.in-memory-instance-size-limit`](/tikv-configuration-file.md#in-memory-instance-size-limit-从-v840-版本开始引入) | 新增 | 控制单个 TiKV 实例内存悲观锁的内存使用上限。超过此限制时，悲观锁将回退到持久化方式写入磁盘。|
| TiKV | [`pessimistic-txn.in-memory-peer-size-limit`](/tikv-configuration-file.md#in-memory-peer-size-limit-从-v840-版本开始引入) | 新增 | 控制单个 Region 内存悲观锁的内存使用上限。超过此限制时，悲观锁将回退到持久化方式写入磁盘。|
| TiKV | [`raft-engine.spill-dir`](/tikv-configuration-file.md#spill-dir-从-v840-版本开始引入) | 新增 | 指定 TiKV 实例存储 Raft 日志文件的辅助目录，用于支持多盘存储 Raft 日志文件。|
| TiKV | [`resource-control.priority-ctl-strategy`](/tikv-configuration-file.md#priority-ctl-strategy-从-v840-版本开始引入) | 新增 | 配置低优先级任务的管控策略。TiKV 通过对低优先级的任务添加流量控制来确保优先执行更高优先级的任务。|
| PD | [`cert-allowed-cn`](/enable-tls-between-components.md#认证组件调用者身份) | 修改 | 从 v8.4.0 开始，支持设置多个 `Common Name`。在 v8.4.0 之前，只能设置一个 `Common Name`。 |
| PD | [`max-merge-region-keys`](/pd-configuration-file.md#max-merge-region-keys) | 修改 | 默认值从 `200000` 修改为 `540000`。|
| PD | [`max-merge-region-size`](/pd-configuration-file.md#max-merge-region-size) | 修改 | 默认值从 `20` 修改为 `54`。|
| TiFlash | [`storage.format_version`](/tiflash/tiflash-configuration.md) | 修改 | TiFlash 底层存储格式的默认版本从 `5` 修改为 `7`，以支持向量索引的构建与存储。由于该格式修改，升级 TiFlash 到 v8.4.0 或更高版本后，不支持原地降级到之前的版本。|
| TiDB Binlog | `--enable-binlog` | 删除 | 从 v8.4.0 开始，[TiDB Binlog](https://docs.pingcap.com/zh/tidb/v8.3/tidb-binlog-overview) 被移除。该参数用于开启或关闭 TiDB 中 binlog 的生成，从 v8.4.0 开始被删除。|
| TiCDC | [`claim-check-raw-value`](/ticdc/ticdc-sink-to-kafka.md#只发送-value-部分到外部存储) | 新增 | 控制 TiCDC 是否仅将 Kafka 消息的 `value` 部分发送到外部存储，该功能仅适用于非 Open Protocol 协议。|
| TiDB Lightning | [`logical-import-prep-stmt`](/tidb-lightning/tidb-lightning-configuration.md) | 新增 | 在逻辑导入模式下，该参数控制是否使用预处理语句和语句缓存来提高性能。默认值为 `false`。|
| BR | [`--log.crypter.key`](/br/br-pitr-manual.md#加密日志备份数据) | 新增 | 设置日志备份数据的加密密钥，十六进制字符串格式，`aes128-ctr` 对应 128 位（16 字节）密钥长度，`aes192-ctr` 为 24 字节，`aes256-ctr` 为 32 字节。|
| BR | [`--log.crypter.key-file`](/br/br-pitr-manual.md#加密日志备份数据) | 新增 | 设置日志备份数据的密钥文件，可直接将存放密钥的文件路径作为参数传入，此时 `log.crypter.key` 不需要配置。 |
| BR | [`--log.crypter.method`](/br/br-pitr-manual.md#加密日志备份数据) | 新增 | 设置日志备份数据的加密算法，支持 `aes128-ctr`、`aes192-ctr` 和 `aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密。|
| BR | [`--master-key`](/br/br-pitr-manual.md#加密日志备份数据) | 新增 | 设置日志备份数据的主密钥，可以是基于本地磁盘的主密钥或基于云 KMS (Key Management Service) 的主密钥。|
| BR | [`--master-key-crypter-method`](/br/br-pitr-manual.md#加密日志备份数据) | 新增 | 设置日志备份数据基于主密钥的加密算法，支持 `aes128-ctr`、`aes192-ctr` 和 `aes256-ctr` 三种算法，缺省值为 `plaintext`，表示不加密。 |

### 离线包变更

从 v8.4.0 开始，`TiDB-community-toolkit` [二进制软件包](/binary-package.md)中移除了以下内容：

- `pump-{version}-linux-{arch}.tar.gz`
- `drainer-{version}-linux-{arch}.tar.gz`
- `binlogctl`
- `arbiter`

### 操作系统支持变更

升级 TiDB 前，请务必确保你的操作系统版本符合[操作系统及平台要求](/hardware-and-software-requirements.md#操作系统及平台要求)。

- 根据 [CentOS Linux EOL](https://www.centos.org/centos-linux-eol/)，CentOS Linux 7 的上游支持已于 2024 年 6 月 30 日终止。因此，在 v8.4.0 版本中，TiDB 移除了对 CentOS 7 的支持，建议使用 Rocky Linux 9.1 及以上的版本。如果将运行在 CentOS 7 上的 TiDB 集群升级到 v8.4.0 版本，将导致集群不可用。
- 根据 [Red Hat Enterprise Linux Life Cycle](https://access.redhat.com/support/policy/updates/errata/#Life_Cycle_Dates)，Red Hat Enterprise Linux 7 的 Maintenance Support 已于 2024 年 6 月 30 日终止。从 v8.4.0 版本开始，TiDB 已结束对 Red Hat Enterprise Linux 7 的支持，建议使用 Rocky Linux 9.1 及以上的版本。如果将运行在 Red Hat Enterprise Linux 7 上的 TiDB 集群升级到 v8.4.0 或之后版本，将导致集群不可用。

## 移除功能

* 以下为从 v8.4.0 开始已移除的功能：

    * [TiDB Binlog](https://docs.pingcap.com/zh/tidb/v8.3/tidb-binlog-overview) 在 v8.4.0 中被移除。从 v8.3.0 开始，TiDB Binlog 被完全废弃。如需进行增量数据同步，请使用 [TiCDC](/ticdc/ticdc-overview.md)。如需按时间点恢复 (point-in-time recovery, PITR)，请使用 [PITR](/br/br-pitr-guide.md)。在将 TiDB 集群升级到 v8.4.0 或之后版本前，务必先切换至 TiCDC 和 PITR。

* 以下为计划将在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 废弃功能

以下为计划将在未来版本中废弃的功能：

* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
* TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
* TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v6.3.0 开始，分区表默认使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，相比静态裁剪模式，动态裁剪模式支持 IndexJoin、Plan Cache 等特性，性能表现更好。在未来版本中，静态裁剪模式将被废弃。

## 改进提升

+ TiDB

    - 优化扫描大量数据时构造 BatchCop Task 的效率 [#55915](https://github.com/pingcap/tidb/issues/55915) [#55413](https://github.com/pingcap/tidb/issues/55413) @[wshwsh12](https://github.com/wshwsh12)
    - 优化事务的缓存，以降低事务中的写操作延时与 TiDB CPU 使用 [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06)
    - 优化系统变量 `tidb_dml_type` 为 `"bulk"` 时 DML 语句的执行性能 [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium)
    - 支持使用 [Optimizer Fix Control 47400](/optimizer-fix-controls.md#47400-从-v840-版本开始引入) 控制优化器是否将 `estRows` 的最小值限制为 `1`，与 Oracle 和 DB2 等数据库的行为保持一致 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell)
    - 为日志表 [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#runaway-queries-相关系统表) 增加写入控制，降低大量并发写入引发的开销 [#54434](https://github.com/pingcap/tidb/issues/54434) @[HuSharp](https://github.com/HuSharp)
    - 当内表上有 `Selection`、`Projection` 或 `Aggregation` 算子时默认支持 Index Join [#47233](https://github.com/pingcap/tidb/issues/47233) @[winoros](https://github.com/winoros)
    - 在某些场景下减少 `DELETE` 操作从 TiKV 获取的列信息数量，降低 `DELETE` 操作的资源开销 [#38911](https://github.com/pingcap/tidb/issues/38911) @[winoros](https://github.com/winoros)
    - 支持通过系统变量 `tidb_auto_analyze_concurrency` 设置单个自动统计信息收集任务内部的并发度 [#53460](https://github.com/pingcap/tidb/issues/53460) @[hawkingrei](https://github.com/hawkingrei)
    - 优化一个内部函数的处理逻辑，提升查询大量列的表时的性能 [#52112](https://github.com/pingcap/tidb/issues/52112) @[Rustin170506](https://github.com/Rustin170506)
    - 支持将形如 `a = 1 AND (a > 1 OR (a = 1 AND b = 2))` 的过滤条件简化为 `a = 1 AND b = 2` [#56005](https://github.com/pingcap/tidb/issues/56005) @[ghazalfamilyusa](https://github.com/ghazalfamilyusa)
    - 在选中不优执行计划风险较高的场景中，提高代价模型中全表扫描的代价，使得优化器更倾向于使用索引 [#56012](https://github.com/pingcap/tidb/issues/56012) @[terry1purcell](https://github.com/terry1purcell)
    - TiDB 支持 `MID()` 函数的两参数版本，即 `MID(str, pos)` [#52420](https://github.com/pingcap/tidb/issues/52420) @[dveeden](https://github.com/dveeden)
    - 支持对主键为非 binary 类型的表拆分 TTL 任务 [#55660](https://github.com/pingcap/tidb/issues/55660) @[lcwangchao](https://github.com/lcwangchao)
    - 优化系统元数据相关语句性能 [#50305](https://github.com/pingcap/tidb/issues/50305) @[ywqzzy](https://github.com/ywqzzy) @[tangenta](https://github.com/tangenta) @[joechenrh](https://github.com/joechenrh) @[CbcWestwolf](https://github.com/CbcWestwolf)
    - 采用新的优先级队列处理自动收集统计信息操作，以提高收集性能并减少重建队列的开销 [#55906](https://github.com/pingcap/tidb/issues/55906) @[Rustin170506](https://github.com/Rustin170506)
    - 引入 DDL 通知程序，允许统计信息模块订阅 DDL 事件 [#55722](https://github.com/pingcap/tidb/issues/55722) @[fzzf678](https://github.com/fzzf678) @[lance6716](https://github.com/lance6716) @[Rustin170506](https://github.com/Rustin170506)
    - TiDB 升级期间强制新版 TiDB 节点接管 DDL Owner，避免旧版本 TiDB 节点接管引发的兼容性问题 [#51285](https://github.com/pingcap/tidb/pull/51285) @[wjhuang2016](https://github.com/wjhuang2016)
    - 支持集群级别的 Scatter Region 打散 [#8424](https://github.com/tikv/pd/issues/8424) @[River2000i](https://github.com/River2000i)

+ TiKV

    - Region 的默认值由 96 MiB 提升到 256 MiB，避免 Region 数量过多导致额外开销 [#17309](https://github.com/tikv/tikv/issues/17309) @[LykxSassinator](https://github.com/LykxSassinator)
    - 支持指定单个 Region 或 TiKV 实例的内存悲观锁的内存上限，在热点写导致大量悲观锁加锁时，可以通过修改配置提高内存上限，避免悲观锁落盘导致的 CPU/IO 开销 [#17542](https://github.com/tikv/tikv/issues/17542) @[cfzjywxk](https://github.com/cfzjywxk)
    - Raft Engine 新增 `spill-dir` 配置，支持 Raft 日志的多磁盘存储。当主目录 `dir` 所在磁盘的容量不足时，Raft Engine 会自动将新日志写入 `spill-dir`，从而确保系统的持续运行 [#17356](https://github.com/tikv/tikv/issues/17356) @[LykxSassinator](https://github.com/LykxSassinator)
    - 优化存在大量 DELETE 版本时 RocksDB 的 compaction 触发机制，以加快磁盘空间回收 [#17269](https://github.com/tikv/tikv/issues/17269) @[AndreMouche](https://github.com/AndreMouche)
    - 支持在线更改写入流量控制 (flow-control) 的相关配置 [#17395](https://github.com/tikv/tikv/issues/17395) @[glorv](https://github.com/glorv)
    - 优化空表和小 Region 场景下 Region Merge 的速度 [#17376](https://github.com/tikv/tikv/issues/17376) @[LykxSassinator](https://github.com/LykxSassinator)
    - [Pipelined DML](https://github.com/pingcap/tidb/blob/master/docs/design/2024-01-09-pipelined-DML.md) 不会长时间阻塞 resolved-ts [#17459](https://github.com/tikv/tikv/issues/17459) @[ekexium](https://github.com/ekexium)

+ PD

    - 支持 TiKV 节点在 TiDB Lightning 导入数据期间优雅下线 (graceful offline) [#7853](https://github.com/tikv/pd/issues/7853) @[okJiang](https://github.com/okJiang)
    - 在 `pd-ctl` 命令中将 `scatter-range` 重命名为 `scatter-range-scheduler` [#8379](https://github.com/tikv/pd/issues/8379) @[okJiang](https://github.com/okJiang)
    - 为 `grant-hot-leader-scheduler` 添加冲突检测 [#4903](https://github.com/tikv/pd/issues/4903) @[lhy1024](https://github.com/lhy1024)

+ TiFlash

    - 优化 `LENGTH()` 和 `ASCII()` 函数执行效率 [#9344](https://github.com/pingcap/tiflash/issues/9344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 减少处理存算分离请求时创建的线程数，避免 TiFlash 计算节点在处理大量请求时崩溃 [#9334](https://github.com/pingcap/tiflash/issues/9334) @[JinheLin](https://github.com/JinheLin)
    - 改进 Pipeline Model 执行模型下任务的等待机制 [#8869](https://github.com/pingcap/tiflash/issues/8869) @[SeaRise](https://github.com/SeaRise)
    - 改进 JOIN 算子的取消机制，使得 JOIN 算子内部能及时响应取消请求 [#9430](https://github.com/pingcap/tiflash/issues/9430) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 当集群的 `split-table` 和 `split-region-on-table` 配置项为默认值 `false` 时，BR 在恢复数据到该集群的过程中不会按照 table 分裂 Region，以提升恢复速度 [#53532](https://github.com/pingcap/tidb/issues/53532) @[Leavrth](https://github.com/Leavrth)
        - 默认不支持使用 SQL 语句 `RESTORE` 全量恢复数据到非空集群 [#55087](https://github.com/pingcap/tidb/issues/55087) @[BornChanger](https://github.com/BornChanger)

## 错误修复

+ TiDB

    - 修复当 `tidb_restricted_read_only` 变量设置为 `true` 时可能死锁的问题 [#53822](https://github.com/pingcap/tidb/issues/53822) [#55373](https://github.com/pingcap/tidb/issues/55373) @[Defined2014](https://github.com/Defined2014)
    - 修复 TiDB 优雅关闭时不等待 auto commit 事务完成的问题 [#55464](https://github.com/pingcap/tidb/issues/55464) @[YangKeao](https://github.com/YangKeao)
    - 修复在 TTL 任务执行过程中，减小 `tidb_ttl_delete_worker_count` 的值导致任务无法完成的问题 [#55561](https://github.com/pingcap/tidb/issues/55561) @[lcwangchao](https://github.com/lcwangchao)
    - 修复当一张表的索引中包含生成列时，通过 `ANALYZE` 语句收集这张表的统计信息时可能报错 `Unknown column 'column_name' in 'expression'` 的问题 [#55438](https://github.com/pingcap/tidb/issues/55438) @[hawkingrei](https://github.com/hawkingrei)
    - 废弃统计信息相关的无用配置，减少冗余代码 [#55043](https://github.com/pingcap/tidb/issues/55043) @[Rustin170506](https://github.com/Rustin170506)
    - 修复执行一条包含关联子查询和 CTE 的查询时，TiDB 可能卡住或返回错误结果的问题 [#55551](https://github.com/pingcap/tidb/issues/55551) @[guo-shaoge](https://github.com/guo-shaoge)
    - 修复禁用 `lite-init-stats` 可能导致统计信息同步加载失败的问题 [#54532](https://github.com/pingcap/tidb/issues/54532) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当 `UPDATE` 或 `DELETE` 语句包含递归的 CTE 时，语句可能报错或不生效的问题 [#55666](https://github.com/pingcap/tidb/issues/55666) @[time-and-fate](https://github.com/time-and-fate)
    - 修复当一条 SQL 绑定涉及窗口函数时，有一定概率不生效的问题 [#55981](https://github.com/pingcap/tidb/issues/55981) @[winoros](https://github.com/winoros)
    - 修复统计信息初始化时，使用非二进制排序规则的字符串类型列的统计信息可能无法正常加载的问题 [#55684](https://github.com/pingcap/tidb/issues/55684) @[winoros](https://github.com/winoros)
    - 修复当查询条件为 `column IS NULL` 访问唯一索引时，优化器将行数错误地估算为 1 的问题 [#56116](https://github.com/pingcap/tidb/issues/56116) @[hawkingrei](https://github.com/hawkingrei)
    - 修复当查询包含形如 `(... AND ...) OR (... AND ...) ...` 的过滤条件时，优化器没有使用最优的多列统计信息估算行数的问题 [#54323](https://github.com/pingcap/tidb/issues/54323) @[time-and-fate](https://github.com/time-and-fate)
    - 修复当一个查询有索引合并 (Index Merge) 执行计划可用时，`read_from_storage` hint 可能不生效的问题 [#56217](https://github.com/pingcap/tidb/issues/56217) @[AilinKid](https://github.com/AilinKid)
    - 修复 `IndexNestedLoopHashJoin` 中存在数据竞争的问题 [#49692](https://github.com/pingcap/tidb/issues/49692) @[solotzg](https://github.com/solotzg)
    - 修复 `INFORMATION_SCHEMA.STATISTICS` 表中 `SUB_PART` 值为空的问题 [#55812](https://github.com/pingcap/tidb/issues/55812) @[Defined2014](https://github.com/Defined2014)
    - 修复 DML 语句中包含嵌套的生成列时报错的问题 [#53967](https://github.com/pingcap/tidb/issues/53967) @[wjhuang2016](https://github.com/wjhuang2016)
    - 修复带有最小显示宽度的 integer 类型的数据参与除法运算时，可能导致除法结果溢出的问题 [#55837](https://github.com/pingcap/tidb/issues/55837) @[windtalker](https://github.com/windtalker)
    - 修复 TopN 算子之后的算子无法在内存超限时触发回退操作的问题 [#56185](https://github.com/pingcap/tidb/issues/56185) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复 Sort 算子中的 `ORDER BY` 列如果包含常量会卡住的问题 [#55344](https://github.com/pingcap/tidb/issues/55344) @[xzhangxian1008](https://github.com/xzhangxian1008)
    - 修复在添加索引期间，kill PD leader 后出现 `8223 (HY000)` 报错，且表中数据不一致的问题 [#55488](https://github.com/pingcap/tidb/issues/55488) @[tangenta](https://github.com/tangenta)
    - 修复当请求历史 DDL 任务信息时，DDL 历史任务过多导致 OOM 的问题 [#55711](https://github.com/pingcap/tidb/issues/55711) @[joccau](https://github.com/joccau)
    - 修复当 Region 大小超过 96 MiB 时，启动全局排序后执行 `IMPORT INTO` 卡住的问题 [#55374](https://github.com/pingcap/tidb/issues/55374) @[lance6716](https://github.com/lance6716)
    - 修复在临时表上执行 `IMPORT INTO` 会导致 TiDB crash 的问题 [#55970](https://github.com/pingcap/tidb/issues/55970) @[D3Hunter](https://github.com/D3Hunter)
    - 修复添加唯一索引出现 `duplicate entry` 报错的问题 [#56161](https://github.com/pingcap/tidb/issues/56161) @[tangenta](https://github.com/tangenta)
    - 修复当 TiKV 停机超过 810 秒后时，TiDB Lightning 未 ingest 所有 KV 对，导致表中数据不一致的问题 [#55808](https://github.com/pingcap/tidb/issues/55808) @[lance6716](https://github.com/lance6716)
    - 修复无法对缓存表使用 `CREATE TABLE LIKE` 语句的问题 [#56134](https://github.com/pingcap/tidb/issues/56134) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复 CTE 中 `FORMAT()` 表达式的警告信息混乱的问题 [#56198](https://github.com/pingcap/tidb/pull/56198) @[dveeden](https://github.com/dveeden)
    - 修复 `CREATE TABLE` 与 `ALTER TABLE` 建立分区表时对列的类型限制不一致的问题 [#56094](https://github.com/pingcap/tidb/issues/56094) @[mjonss](https://github.com/mjonss)
    - 修复 `INFORMATION_SCHEMA.RUNAWAY_WATCHES` 表中时间类型不正确的问题 [#54770](https://github.com/pingcap/tidb/issues/54770) @[HuSharp](https://github.com/HuSharp)

+ TiKV

    - 修复当主密钥存储于 KMS (Key Management Service) 时无法轮换主密钥的问题 [#17410](https://github.com/tikv/tikv/issues/17410) @[hhwyt](https://github.com/hhwyt)
    - 修复删除大表或分区后可能导致的流量控制问题 [#17304](https://github.com/tikv/tikv/issues/17304) @[Connor1996](https://github.com/Connor1996)
    - 修复过期副本处理 Raft 快照时，由于分裂操作过慢并且随后立即删除新副本，可能导致 TiKV panic 的问题 [#17469](https://github.com/tikv/tikv/issues/17469) @[hbisheng](https://github.com/hbisheng)

+ TiFlash

    - 修复当表里含 Bit 类型列并且带有表示非法字符的默认值时，TiFlash 无法解析表 schema 的问题 [#9461](https://github.com/pingcap/tiflash/issues/9461) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)
    - 修复当多个 Region 并发进行副本同步时，可能错误触发 Region overlap 检查失败而导致 TiFlash panic 的问题 [#9329](https://github.com/pingcap/tiflash/issues/9329) @[CalvinNeo](https://github.com/CalvinNeo)
    - 修复一些 TiFlash 不支持的 JSON 函数被错误地下推到 TiFlash 的问题 [#9444](https://github.com/pingcap/tiflash/issues/9444) @[windtalker](https://github.com/windtalker)

+ Tools

    + Backup & Restore (BR)

        - 修复 TiDB 节点停止时，监控中 PITR checkpoint 间隔显示异常增大，与实际情况不符的问题 [#42419](https://github.com/pingcap/tidb/issues/42419) @[YuJuncen](https://github.com/YuJuncen)
        - 修复备份过程中由于 TiKV 没有响应导致备份任务无法结束的问题 [#53480](https://github.com/pingcap/tidb/issues/53480) @[Leavrth](https://github.com/Leavrth)
        - 修复开启日志备份时，BR 日志可能打印权限凭证敏感信息的问题 [#55273](https://github.com/pingcap/tidb/issues/55273) @[RidRisR](https://github.com/RidRisR)
        - 修复当 PITR 日志备份任务失败时，用户停止了该任务后，PD 中与该任务相关的 safepoint 未被正确清除的问题 [#17316](https://github.com/tikv/tikv/issues/17316) @[Leavrth](https://github.com/Leavrth)

    + TiDB Data Migration (DM)

        - 修复多个 DM-master 节点可能同时成为 Leader 导致数据不一致的问题 [#11602](https://github.com/pingcap/tiflow/issues/11602) @[GMHDBJD](https://github.com/GMHDBJD)
        - 修复 DM 在处理 `ALTER DATABASE` 语句时未设置默认数据库导致同步报错的问题 [#11503](https://github.com/pingcap/tiflow/issues/11503) @[lance6716](https://github.com/lance6716)

    + TiDB Lightning

        - 修复两个实例同时并行开始导入任务时，由于分配到的任务 ID 相同导致 TiDB Lightning 报 `verify allocator base failed` 错误的问题 [#55384](https://github.com/pingcap/tidb/issues/55384) @[ei-sugimoto](https://github.com/ei-sugimoto)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [ei-sugimoto](https://github.com/ei-sugimoto)
- [eltociear](https://github.com/eltociear)
- [guoshouyan](https://github.com/guoshouyan)（首次贡献者）
- [JackL9u](https://github.com/JackL9u)
- [kafka1991](https://github.com/kafka1991)（首次贡献者）
- [qingfeng777](https://github.com/qingfeng777)
- [samba-rgb](https://github.com/samba-rgb)（首次贡献者）
- [SeaRise](https://github.com/SeaRise)
- [tuziemon](https://github.com/tuziemon)（首次贡献者）
- [xyproto](https://github.com/xyproto)（首次贡献者）
