---
title: TiDB 8.4.0 Release Notes
summary: 了解 TiDB 8.4.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.4.0 Release Notes

发版日期：2024 年 xx 月 xx 日

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
    <td rowspan="5">可扩展性和性能</td>
    <td> 执行计划缓存在实例内共享（实验特性）<!-- tw@Oreoxmt 1569 --></td>
    <td> 实例级执行计划缓存支持在内存中缓存更多的执行计划，消除 SQL 编译时所消耗的时间，从而减少 SQL 的运行时间，提升 OLTP 系统的性能和吞吐。同时，也能更好的控制内存占用，提升数据库稳定性。</td>
  </tr>
  <tr>
    <td>分区表全局索引成为正式功能<!-- tw@hfxsd 1961 --></td>
    <td>全局索引可以有效提高检索非分区列的效率，并且消除了唯一键必须包含分区键的限制。该功能扩展了 TiDB 分区表的使用场景，避免了数据迁移过程中的一些应用修改工作。</td>
  </tr>
  <tr>
    <td> TiDB 并行获取 TSO<!-- tw@qiancai 1893 --></td>
    <td>在高并发场景下，并行获取 TSO 能够有效降低等待获取 TSO 的时间，提升集群的吞吐。</td>
  </tr>
  <tr>
    <td> 提升管理类 SQL 的执行效率<!-- tw@hfxsd 1941 --></td>
    <td>在一部分 SaaS 系统中，存在批量创建大量用户，以及定期轮换所有用户密码的需求。TiDB 提升了创建和修改数据库用户的性能，保证操作能在期望的时间窗口。</td>
  </tr>
  <tr>
    <td> 缓存表的查询性能提升<!-- tw@hfxsd 1965 --></td>
    <td>优化了缓存表的查询性能，提升幅度最高可达5.4倍。在需要对小表进行高速查询的场景下，整体性能得到提升。</td>
  </tr>
  <tr>
    <td rowspan="4">稳定性与高可用</td>
    <td> Runaway Queries 支持更多触发条件，并能够切换资源组<!-- tw@hfxsd 1832 --></td>
    <td>Runaway Queries 为用户提供了有效的手段，降低突发的 SQL 性能问题对系统产生的影响。新版本中新增<CODE>处理行数</CODE>和 <CODE>Request Unit</CODE> 作为识别条件，并可以将识别到的查询置入指定资源组，对 Runaway Queries 做更精确的识别与控制。</td>
  </tr>
  <tr>
    <td> 支持为后台任务设置资源使用上限<!-- tw@hfxsd 1909 --></td>
    <td>为后台任务设置百分比上线，针对不同业务系统的需求控制后台任务的消耗，可以按需将后台任务的消耗限制在一个很低的水平，保证在线业务的服务质量。</td>
  </tr>
  <tr>
    <td> TiProxy 流量捕捉和回放<!-- tw@Oreoxmt 1942 --></td>
    <td>在做集群升级、迁移、部署变化等重要变更之前，通过捕捉真实负载来验证目标集群的性能，确保变更的成功。</td>
  </tr>
  <tr>
    <td> 统计信息收集自适应并发度<!-- tw@Oreoxmt 1739 --></td>
    <td>自动统计信息收集会根据节点规模和硬件规格自动决定采集并发度，提升统计信息收集效率，减少手工调优，保证集群性能稳定。</td>
  </tr>
  <tr>
    <td rowspan="2">SQL</td>
    <td> 外键成为正式功能<!-- tw@lilin90 1894 --></td>
    <td>支持 MySQL 兼容的外键约束，维护数据一致性，进一步提升了 TiDB 对 MySQL 的兼容能力。</td>
  </tr>
  <tr>
    <td> 向量搜索功能（实验特性）<!-- tw@qiancai 1898 --></td>
    <td>加速向量搜索的性能，适用于检索增强生成（RAG）、语义搜索、推荐系统等应用类型。把 TiDB 应用场景扩展到 AI 和 大语言模型（LLM）领域。</td>
  </tr>
  <tr>
    <td rowspan="3">数据库管理和可观测性</td>
    <td> 持久化内存表到 Workload Repository（实验特性）<!-- tw@lilin90 1823 --></td>
    <td> 持久化内存表中的运行指标和状态信息，是观测性的重要增强，能极大提升过往问题诊断和追溯的效率，并为未来的自动化运维，提供了数据集支持。 围绕 Workload Repository 构建报告、诊断、推荐一体化的能力，会成为未来提升 TiDB 易用性的重要组成。</td>
  </tr>
  <tr>
    <td> 在内存表中显示 TiKV 和 TiDB 的 CPU 时间<!-- tw@hfxsd 1877 --></td>
    <td>将 CPU 时间合入系统表中展示，与会话或 SQL 的其他指标并列，方便用户从多角度对高 CPU 消耗的操作进行观测，提升诊断效率。尤其适用于诊断实例 CPU 飙升或集群读写热点等场景。</td>
  </tr>
  <tr>
    <td> 支持对开启了 IMDSv2 服务的 TiKV 实例做备份<!-- tw@hfxsd 1945 --></td>
    <td><a href="https://aws.amazon.com/cn/blogs/security/get-the-full-benefits-of-imdsv2-and-disable-imdsv1-across-your-aws-infrastructure/">IMDSv2 目前是 AWS EC2 的默认元数据服务</a>。TiDB 支持从开启了 IMDSv2 的 TiKV 实例中备份数据，协助客户更好地在公有云服务中运行 TiDB 集群。</td>
  </tr>
  <tr>
    <td rowspan="1">安全</td>
    <td> 备份数据加密成为正式功能<!-- tw@qiancai 1920 --></td>
    <td> 加密数据库备份是一种增强数据安全性的重要措施，既可以保护数据备份中敏感信息，又有助于合规，确保数据在存储和传输中的安全。</td>
  </tr>
</tbody>
</table>

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 增加获取 TSO 的 RPC 模式，降低获取 TSO 的延迟 [#54960](https://github.com/pingcap/tidb/issues/54960) @[MyonKeminta](https://github.com/MyonKeminta) **tw@qiancai** <!--1893-->

    TiDB 在向 PD 请求 TSO 时，会将一段时间内的请求汇总起来并以同步的方式进行批处理，以减少 RPC (Remote Procedure Call) 请求数量从而降低 PD 负载。对于延迟敏感的场景，这种模式的性能并不理想。在 v8.4.0 中，TiDB 新增 TSO 请求的异步批处理模式，并提供不同的并发能力。异步模式可以降低获取 TSO 的延迟，但可能会增加 PD 的负载。你可以通过 [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入) 变量设定获取 TSO 的 RPC 模式。

    更多信息，请参考[用户文档](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入)。

* 优化 TiDB 的 Hash Join 算子实现效率（实验特性） [#55153](https://github.com/pingcap/tidb/issues/55153) [#53127](https://github.com/pingcap/tidb/issues/53127) @[windtalker](https://github.com/windtalker) @[xzhangxian1008](https://github.com/xzhangxian1008) @[XuHuaiyu](https://github.com/XuHuaiyu) @[wshwsh12](https://github.com/wshwsh12) **tw@qiancai** <!--1633-->

    在 v8.4.0 版本之前，TiDB 的 Hash Join 算子实现效率不高。从 v8.4.0 开始，TiDB 将对 Hash Join 算子进行重构优化，提升执行效率。在 v8.4.0 版本，该功能为实验特性，只有 INNER JOIN 和 OUTER JOIN 可以使用重构后的高性能 Hash Join 算子。当该功能启用时，执行器会根据高性能 Hash Join 算子对关联操作的支持情况，自动选择是否使用高性能 Hash Join 算子。你可以通过 [tidb_hash_join_version](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入) 变量控制是否启用高性能 Hash Join 算子。

    更多信息，请参考[用户文档](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入)。

* 支持下推以下字符串函数到 TiKV [#17529](https://github.com/tikv/tikv/issues/17529) @[gengliqi](https://github.com/gengliqi) **tw@qiancai** <!--1716-->

    * `DATE_ADD()`
    * `DATE_SUB()`

  更多信息，请参考[用户文档](/functions-and-operators/expressions-pushed-down.md)。

* 提升批量创建用户和修改用户密码操作的性能，提升达数百倍 [#55604](https://github.com/pingcap/tidb/pull/55604) @[wjhuang2016](https://github.com/wjhuang2016) **tw@hfxsd** <!--1941-->

    在 SaaS 场景下，存在批量创建大量用户，以及定期轮换所有用户密码的需求，且需要在指定时间窗口内完成，从 V8.3.0 开始，对批量创建用户，批量修改用户密码的性能做了提升，且用户可以通过增加 session 连接数来提升并发，提升性能，大大缩短了该场景下的执行时间。

    更多信息，请参考[用户文档](链接)。

* 实例中的会话共享执行计划缓存 (实验特性) [#issue号](链接) @[qw4990](https://github.com/qw4990) **tw@Oreoxmt** <!--1569-->

    相比会话级执行计划缓存，执行计划缓存在会话间共享有明显的优势：

    - 消除冗余，相同的内存消耗下能缓存更多的执行计划。
    - 在实例上开辟固定大小的内存区域，能更有效的对内存进行限制。

    在 v8.4.0 中，实例级执行计划缓存作为实验特性，只支持对查询的执行计划进行缓存，默认关闭，通过设置系统变量 [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入) 开启，缓存最大值通过变量 [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-从-v840-版本开始引入) 设置。同时，会话执行计划缓存需要保持关闭状态，具体参见 [Prepare 语句执行计划缓存](/sql-prepared-plan-cache.md) 和 [非 Prepare 语句执行计划缓存](/sql-non-prepared-plan-cache.md)。

    实例级执行计划缓存能够大幅降低 TiDB 的时延，提升集群吞吐，并能够减少执行计划突变的机会，保持集群性能的稳定，是 TiDB 改善性能和稳定性的重要改进。

* `Lightning` 的逻辑导入支持 prepare 接口 [#54850](https://github.com/pingcap/tidb/issues/54850) @[dbsid](https://github.com/dbsid) @[qw4990](https://github.com/qw4990) **tw@lilin90** <!--1922-->

    通过开启配置 [`logical-import-prep-stmt`]()，`Lightning` 逻辑导入产生的 SQL 语句将会通过 prepare 接口执行，提升 SQL 执行效率，并有更大机会命中执行计划缓存，提升逻辑导入的速度。

    更多信息，请参考[用户文档]()

### 稳定性

* 超出预期的查询 (Runaway Queries) 新增 "处理行数" 和 RU 作为阈值 [#issue号](链接) @[HuSharp](https://github.com/HuSharp) **tw@lilin90** <!--1800-->

    TiDB 在 v8.4.0 可以依据 "处理行数 (`PROCESSED_KEYS`)" 和 "Request Unit (`RU`)" 定义超出预期的查询。和"执行时间(`EXEC_ELAPSED`)"相比，新增阈值能够更准确的定义查询的资源消耗，避免整体性能下降时发生识别偏差。
    
    支持同时设置多个条件，满足任意条件即识别为 `Runaway Queries`。

    用户可以观测 [`Statement Summary Tables`](/statement-summary-tables.md) 中的几个对应字段 (`RESOURCE_GROUP`、`MAX_REQUEST_UNIT_WRITE`、`MAX_REQUEST_UNIT_READ`、`MAX_PROCESSED_KEYS`)，根据历史执行情况决定条件值的大小。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* 超出预期的查询 (Runaway Queries) 支持切换资源组 [#issue号](链接) @[JmPotato](https://github.com/JmPotato) **tw@hfxsd** <!--1832-->

    v8.4.0 新增支持将 `Runaway Queries` 切换到指定资源组。在降低优先级 (COOLDOWN) 仍旧无法有效降低资源消耗的情况下，用户可以创建一个资源组 [`RESOURCE GROUP`](/tidb-resource-control.md#管理资源组)，并指定将识别到的查询切换到该资源组中，会话的后续查询仍旧会遵循原资源组。切换资源组的行为能够更精确地限制资源使用，对 `Runaway Queries` 的资源消耗做更加严格的控制。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

* ‘tidb_scatter_region’ 支持设置集群级别的 region 打算策略 [#issue号](链接) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1927-->

     ‘tidb_scatter_region’  在之前的版本仅支持设置为开启或者关闭，开启后，建表时会使用表级别打算策略。在批量快速建表，且表的数量达到几十万张后，该策略会导致 Region 集中分布在其中几个 TiKV 节点，导致这些 TiKV 节点 OOM。因此，从 V8.3.0 版本开始，将该系统变量改为字符串类型，且新增支持集群级别的打散策略，避免上述场景下导致 TiKV OOM 的问题。

    更多信息，请参考[用户文档](链接)。

* 资源管控为后台任务设置资源上限 [#issue号](链接) @[glorv](https://github.com/glorv) **tw@hfxsd** <!--1909-->

    TiDB 资源管控能够识别并降低后台任务的运行优先级。在部分场景下，即使有空闲资源，客户希望后台任务消耗能够控制在很低的水平。在新版本中，资源管控可以通过 `UTILIZATION_LIMIT` 指令为后台任务设置资源百分比，每个节点把所有后台任务的使用量控制在这个百分比以下。精细控制后台任务的资源占用，进一步提升集群稳定性。

    更多信息，请参考[用户文档](/tidb-resource-control.md#管理后台任务)。

* 优化资源组资源分配策略 [#issue号](链接) @[nolouch](https://github.com/nolouch) **tw@hfxsd** <!--1833--> <!--1940-->

    TiDB 在 v8.4.0 部分调整了资源分配策略，更好的满足客户对资源管控的预期。

    - 拥有 `BURSTABLE` 属性的资源组，超出 `RU_PER_SEC` 的资源请求会被控制在一定范围内，降低对其他资源组产生的影响。
    - 控制大查询在运行时的资源分配，避免超出资源组限额。配合 Runaway Queries 的 `COOLDOWN` 动作，识别并降低大查询并发度，降低瞬时资源消耗。
    - 调整默认的优先级调度策略。当不同优先级的任务同时运行时，高优先级的任务获得更多资源。

### 高可用

* TiProxy 支持流量回放功能（实验特性） [#642](https://github.com/pingcap/tiproxy/issues/642) @[djshow832](https://github.com/djshow832) **tw@Oreoxmt** <!--1942-->

    从 TiProxy v1.3.0 版本开始，TiProxy 将支持流量捕获回放功能。该功能可以从 TiDB 生产集群中捕获所有的访问流量，并在测试集群中按照指定的速率进行回放，验证所有 SQL 的执行结果和性能表现。

    该功能适用于以下场景：
    - TiDB 版本升级前验证
    - 执行变更前影响评估
    - TiDB 扩缩容前性能验证
    - 测试集群性能上限

    你可以通过 `tiproxyctrl` 命令连接 TiProxy 实例，进行流量捕获、回放。

    更多信息，请参考[用户文档](/tiproxy/tiproxy-traffic-replay.md)。

### SQL 功能

* 支持向量搜索功能（实验特性） [#54245](https://github.com/pingcap/tidb/issues/54245) [#9032](https://github.com/pingcap/tiflash/issues/9032) @[breezewish](https://github.com/breezewish) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger) @[EricZequan](https://github.com/EricZequan) @[zimulala](https://github.com/zimulala) @[JaySon-Huang](https://github.com/JaySon-Huang) **tw@qiancai** <!--1898-->

    向量搜索是一种基于数据语义的搜索方法，旨在提供更相关的搜索结果，是 AI 和大语言模型（LLM）的关键功能之一。通过使用向量索引，数据库能够加速向量搜索的性能，快速基于不同的距离函数查询相似向量，从而支持检索增强生成（Retrieval-Augmented Generation, RAG）、语义搜索、推荐系统等多种应用场景。
    
    从 v8.4 版本开始，TiDB 支持向量数据类型和向量索引，具备强大的向量搜索能力。TiDB 的向量数据类型最多可支持 16383 维度，并提供多种距离函数支持，包括 L2 距离（欧式距离）、余弦距离、负内积和 L1 距离（曼哈顿距离）。
    
    在使用时，用户只需创建包含向量类型的表并插入数据，即可执行向量搜索查询，也可进行向量数据与传统关系数据的混合查询。
    值得注意的是，TiDB 的向量索引依赖于 TiFlash，因此，在使用向量索引之前，需要确保 TiDB 集群中已添加 TiFlash 节点。

    更多信息，请参考[用户文档](/vector-search-overview.md)。

* TiDB 外键约束检查功能成为正式功能（GA） [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@lilin90** <!--1894-->

    TiDB 从 v6.6.0 版本开始，可通过变量 foreign_key_checks 做外键约束检查，但是其一直为实验特性。v8.3.0 对外键特性在更多场景做了覆盖测试，稳定性和性能方面也有一些提升，因此从 v8.3.0 开始外键功能成为正式功能（GA）

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 持久化部分内存表的快照 (实验特性) [#issue号](链接) @[xhebox](https://github.com/xhebox)  **tw@lilin90** <!--1823-->

    TiDB 的内存表中会保存很多运行时状态信息，比如会话状态、锁状态、SQL 运行状态等，用户可以据此了解数据库运行情况，这些信息被大量用在故障诊断和性能调优的场景。实际使用中会遇到几个问题：

    - 内存表中的信息会随 TiDB 实例的关闭而消失
    - 用户无法追溯过去某个时间的状态信息

    为了解决上述问题，受流行商业数据库的启发，TiDB 新增对内存表持久化的能力，为 TiDB 构建 `Workload Repository`。通过设置变量 [`tidb_workload_repository_dest`]() 为 `SCHEMA`, TiDB 将内存表中的信息阶段性写入特定数据库 (`WORKLOAD_SCHEMA`)，持久化到 TiKV 中。持久化的数据大体有两类用途：

    - **故障定位**：获取过去某一段时间的数据库运行情况，分析故障可能的原因。
    - **自动运维**：对数据库的历史负载进行分析，发现潜在的优化点，并得出优化建议。比如索引推荐，SQL 调优推荐等。
    
    被持久化的内存表大体分为两类：

    一类是保存累计运行指标的内存表，通常体积较大，快照一次有明显开销。这类内存表默认每 60 分钟记录一次快照，通过系统变量 [`tidb_workload_repository_snapshot_interval`]() 修改快照间隔。包括：

    - SQL 语句运行指标
    - 索引运行指标

    另一类内存表显示实时状态信息，会被快速刷新。这类内存记录默认每秒采样一次，通过系统变量 [`tidb_workload_repository_active_sampling_interval`]() 修改采样间隔。这类表包括：

    - 活动会话的状态
    - 锁状态
    - 活动事务状态

    TiDB `Workload Repository` 的引入，极大地提升了数据库的可观测性，并为未来的自动化运维工作提供了数据基础。在接下来的版本，TiDB 会加入更多的内存观测指标，并持久化到 `Workload Repository`，通过提供丰富的工具、报告、建议，协助用户的管理工作，提升运维 TiDB 集群的效率。

    更多信息，请参考[用户文档](链接)。

* 在系统表中显示 TiDB 和 TiKV 的 CPU 时间 [#55542](https://github.com/pingcap/tidb/issues/55542) @[yibin87](https://github.com/yibin87) **tw@hfxsd** <!--1877-->

    [TiDB Dashboard](/dashboard/dashboard-intro.md) 的 [TOP SQL 页面](/dashboard/top-sql.md)能够展示 CPU 消耗高的 SQL 语句。v8.4.0 开始，TiDB 将 CPU 时间消耗信息加入系统表展示，与会话或 SQL 的其他指标并列，方便客户从多角度对高 CPU 消耗的操作进行观测。在实例 CPU 飙升 或集群读写热点的场景下，这些信息能够协助客户快速发现问题的原因。

    - [`STATEMENTS_SUMMARY`](/statement-summary-tables.md) 增加 `AVG_TIDB_CPU_TIME` 和 `AVG_TIKV_CPU_TIME`，显示单个 SQL 语句在历史上消耗的平均 CPU 时间。
    - [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md) 增加 `TIDB_CPU` 和 `TIKV_CPU`，显示会话当前正在执行 SQL 的累计 CPU 消耗。
    - [慢日志](/analyze-slow-queries.md)中增加字段 `Tidb_cpu_time` 和 `Tikv_cpu_time`，显示被捕捉到的 SQL 语句的 CPU 时间。

    其中，TiKV 的 CPU 时间默认显示；采集 TiDB 的 CPU 时间会引入额外开销（大概在8%），因此仅在开启 [Top SQL 特性](/dashboard/top-sql.md)时，TiDB 的 CPU 时间才会显示为实际值，否则始终显示为 `0`。

* TOP SQL 可按 `Schema` 或 `Table` 维度聚合 [#issue号](链接) @[nolouch](https://github.com/nolouch) **tw@lilin90** <!--1878-->

    当前的 [TOP SQL](/dashboard/top-sql.md) 以 SQL 为单位来聚合 CPU 时间。如果 CPU 时间不是由少数几个 SQL 贡献，按 SQL 聚合并不能有效发现问题。从 v8.4.0 开始，用户可以选择按照 `Schema` 或 `Table` 聚合 CPU 时间。在多系统融合的场景下，新的聚合方式能够更有效地识别来自某个特定系统的负载变化，提升问题诊断的效率。

    更多信息，请参考[用户文档](/dashboard/top-sql.md)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.3.0 升级至当前版本 (v8.4.0) 所需兼容性变更信息。如果从 v8.2.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
| [`tidb_enable_inl_join_inner_multi_pattern`](/system-variables.md#tidb_enable_inl_join_inner_multi_pattern-从-v700-版本开始引入) |   修改  |   默认值改为 `ON`。当内表上有 `Selection` 或 `Projection` 算子时默认支持 Index Join  |
| [`tidb_enable_instance_plan_cache`](/system-variables.md#tidb_enable_instance_plan_cache-从-v840-版本开始引入)| 新增 | 这个变量控制是否开启 Instance Plan Cache 功能。 |
| [`tidb_instance_plan_cache_max_size`](/system-variables.md#tidb_instance_plan_cache_max_size-从-v840-版本开始引入) | 新增 | 这个变量控制 Instance Plan Cache 的目标内存大小，超过这个大小则触发清理。|
| tidb_scatter_region       |          修改                    | 原先为布尔型，仅支持开启或关闭，且开启后新建的表的 region 只支持表级别打散，v8.3.0 开始改成字符串型，并新增支持集群级别的打算策略，避免快速批量建表时由于 region 分布不均匀导致 TiKV OOM 的问题     |
| tidb_shard_row_id_bits       |         新增                     |   原先 ‘shard_row_id_bits’ 需要在每个 Create Table 或 Alter Table 的 SQL 语句里声明，一旦需要同样配置的表数量较多，操作复杂，因此引入该变量，可在 Global 或 Session 级别设置该系统变量，提升易用性  |
| tidb_pre_split_regions       |         新增                     |   原先 ‘pre_split_regions’ 需要在每个 Create Table SQL 语句里声明，一旦需要同样配置的表数量较多，操作复杂，因此引入该变量，可在 Global 或 Session 级别设置该系统变量，提升易用性  |
|  [tidb_tso_client_rpc_mode](/system-variables.md#tidb_tso_client_rpc_mode-从-v840-版本开始引入)      |         新增                     |   原有的 TSO 请求为同步模式。现在引入 TSO 请求的异步批处理模式，并提供不同的并发能力。异步模式可以降低获取 TSO 的延迟，但可能会增加 PD 的负载。  |
|  [tidb_hash_join_version](/system-variables.md#tidb_hash_join_version-从-v840-版本开始引入)     |         新增                     |   原有的 TiDB Hash Join 算法效率不佳，引入新的 HashJoin 版本，实现更加高效的计算  |


### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|  TiKV        |   grpc-keepalive-timeout       |    修改      |  该配置文件参数原先为 int 类型，且最小值仅支持设置为 1，从 v8.3.0 开始，数据类型修改为 float64 ，且最小值支持设置为 0.05，可以在网络抖动比较频繁的场景，适当调小该值，通过减少重试间隔，来减少网络抖动带来的性能影响。       |
|  TiKV        |   in_memory_peer_size_limit       |    新增      |    该配置文件参数用于指定单 region 的 内存上限      |
|  TiKV        |   in_memory_global_size_limit      |   新增       |   该配置文件参数用于指定 TiKV 实例的 内存上限       |
|          |          |          |          |

### 系统表

## 离线包变更

## 废弃功能

* 以下为从 v8.4.0 开始已废弃的功能：

    * 废弃功能 1

* 以下为计划将在未来版本中废弃的功能：

    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
    * TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
    * 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
    * TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
    * TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。

* 以下为计划将在未来版本中移除的功能：

    * 从 v8.0.0 开始，TiDB Lightning 废弃了物理导入模式下的[旧版冲突检测](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#旧版冲突检测从-v800-开始已被废弃)策略，支持通过 [`conflict.strategy`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 参数统一控制逻辑导入和物理导入模式的冲突检测策略。旧版冲突检测的参数 [`duplicate-resolution`](/tidb-lightning/tidb-lightning-configuration.md) 将在未来版本中被移除。

## 改进提升

+ TiDB
  - 优化扫描大量数据时构造 BatchCop Task 的效率 [#55915](https://github.com/pingcap/tidb/issues/55915) [#55413](https://github.com/pingcap/tidb/issues/55413) @[wshwsh12](https://github.com/wshwsh12) **tw@caiqian** <!--1902-->
  - 优化 MEMDB 实现，降低事务中的写操作延时与 TiDB CPU 使用 [#55287](https://github.com/pingcap/tidb/issues/55287) @[you06](https://github.com/you06) **tw@hfxsd** <!--1892-->
  - 优化 BULK 模式 DML 的执行性能 [#50215](https://github.com/pingcap/tidb/issues/50215) @[ekexium](https://github.com/ekexium) **tw@qiancai** <!--1860-->
  - 优化器估行的最小值为`1`，与其他数据库行为一致 [#47400](https://github.com/pingcap/tidb/issues/47400) @[terry1purcell](https://github.com/terry1purcell) **tw@Oreoxmt** <!--1929-->
  - 为日志表 [`mysql.tidb_runaway_queries`](/mysql-schema/mysql-schema.md#runaway-queries-相关系统表) 增加写入控制，降低并发大量写入引发的开销 [#issue号](链接) @[HuSharp](https://github.com/HuSharp) <!--1908--> **tw@lilin90** 
  - 当内表上有 `Selection` 或 `Projection` 算子时默认支持 Index Join [#issue号](链接) @[winoros](https://github.com/winoros) **tw@qiancai** <!--1709-->
  - 减少部分场景的 DELETE 操作从 TiKV 获取的列信息数量，降低 DELETE 操作的资源开销。[#issue号](链接) [winoros](https://github.com/winoros) **tw@Oreoxmt** <!--1798-->
  - 优化 Priority Queue 基于 Meta Cache V2 的运行效率 [#49972](https://github.com/pingcap/tidb/issues/49972) [Rustin170506](https://github.com/Rustin170506) **tw@Oreoxmt** <!--1935-->
  - 自动统计信息收集根据部署规模和硬件规格决定执行和扫描的并发度 [#issue号](链接) @[hawkingrei](https://github.com/hawkingrei) **tw@Oreoxmt** <!--1739-->
  - ‘tidb_enable_fast_create_table’ 开启后，支持了批量快速创建外键表的场景。 [#issue号](链接) @[D3Hunter](https://github.com/D3Hunter) **tw@hfxsd** <!--1896-->
+ TiKV

  - 默认 Region 大小由 96 MB 提升到 256 MB，避免 Region 数量过多带来的额外开销 [#17309](https://github.com/tikv/tikv/issues/17309) [LykxSassinator](https://github.com/LykxSassinator) **tw@hfxsd** <!--1925-->

  - 增加配置项指定单 region 和实例的内存用量，在热点写时通过增加内存避免落盘带来的额外 CPU/IO 消耗 [#17542](https://github.com/tikv/tikv/issues/17542) @[cfzjywxk](https://github.com/cfzjywxk) **tw@qiancai** <!--1967-->


+ PD

  - `Lightning` 导入过程中，允许 PD 做 `evict-leader` 调度来避免阻断 TiKV 的 offline 进程 [#issue号](链接) @[okJiang](https://github.com/okJiang) **tw@qiancai**  <!--1852-->  

+ TiFlash

+ Tools

    + Backup & Restore (BR)

      - 集群恢复时同时设置 `split-table=false` 和 `split-region-on-table=false`，优化 region 的分配策略 [#53532](https://github.com/pingcap/tidb/issues/53532) @[Leavrth](https://github.com/Leavrth) 
      **tw@qiancai** <!--1914-->
      - 默认不允许使用 SQL 全量恢复数据到非空集群 [#55087](https://github.com/pingcap/tidb/issues/55087) @[BornChanger](https://github.com/BornChanger) **tw@Oreoxmt** <!--1711-->
      - 快照恢复和日志恢复产生的断点数据将存储在恢复集群的临时库表中，日志恢复产生的上下游 ID 映射存储到系统表 `mysql.tidb_pitr_id_map` 中 [#55870](https://github.com/pingcap/tidb/issues/55870) @[Leavrth](https://github.com/Leavrth) **tw@Oreoxmt** <!--1943-->

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## 错误修复

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

    + Backup & Restore (BR)

    + TiCDC

    + TiDB Data Migration (DM)

    + TiDB Lightning

    + Dumpling

    + TiUP

    + TiDB Binlog

## 贡献者

感谢来自 TiDB 社区的贡献者们：
