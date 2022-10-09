---
title: 使用 PingCAP Clinic 生成诊断报告
summary: 介绍 PingCAP Clinic 诊断报告的使用场景、方法以及如何解读报告。
---

# 使用 PingCAP Clinic 生成诊断报告

PingCAP Clinic Server 云诊断平台（以下简称为 Clinic Server）可以基于上传的诊断数据生成诊断报告，包括 Benchmark Report 和 Comparison Report，用于在特定场景下检查集群健康风险，并协助定位集群问题。本文介绍 [Benchmark Report](#benchmark-report) 和 [Comparison Report](#comparison-report) 报告的使用场景和使用方法。

> **注意：**
>
> 使用 PingCAP Clinic 生成的报告是基于诊断数据中的 Metrics 数据和日志数据。要获取完整的诊断建议，你需要**完整收集**集群诊断数据。

## 使用场景

- 压力测试场景

    在性能测试或新业务压力接入测试阶段，需要对系统性能进行评估，并通过调整上层业务请求和下层数据库配制参数来提升整体性能。通过 [Benchmark Report](#benchmark-report)，可以检查当前系统性能状态，发现风险问题，提出业务层和集群配置的优化建议。

- 性能对比检查场景

    很多场景需要对比集群各种关键指标，通过 [Comparison Report](#comparison-report)，可以快速了解机器不同时间段运行状态的差异。相对于手动对比，Comparison Report 能够提升效率和准确性。对比的内容包括：QPS 差异、延迟差异、性能指标差异、系统资源使用差异和关键日志差异等。需要使用 Comparison Report 对比性能的场景有：

    - 集群健康巡检时，对比本次性能与上次巡检的差异
    - 集群修改了关键参数或配置后，对比修改前后的差异
    - 集群升级后，对比升级前后的差异
    - 集群接入新业务后，对比接入新业务前后的差异

## 前提条件

要生成 PingCAP Clinic 报告，需要使用 Diag 诊断客户端采集集群诊断数据，并上传到 Clinic Server。具体使用 Diag 采集诊断数据的方法，在 TiUP 部署环境参见[使用 PingCAP Clinic 诊断集群](/clinic/clinic-user-guide-for-tiup.md)，TiDB Operator 部署环境参见[使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)。

## 使用方法

### Benchmark Report

#### 生成报告

- 生成默认报告

    Benchmark Report 会在数据包上传到 Clinic Server 后自动生成。由于生成报告需要先将相关诊断数据从数据包中解压提取，所以生成报告时间会在 5 分钟以上（数据包越大，所需时间越长）。

- 生成自定义报告

    默认生成的报告是基于数据包的起止时间，如果需要自定义生成报告的时间，可以按如下步骤进行自定义：

    1. 登录 Clinic Server（[中国区](https://clinic.pingcap.com.cn)、[美国区](https://clinic.pingcap.com)）
    2. 打开需要生成诊断报告的集群页面
    3. 点击集群页面上的 **Benchmark Report**
    4. 在 **Time Range** 部分选择报告的开始 (Start date) 和结束时间 (End date)
    5. 点击 **Create Report** 生成自定义报告

#### 解读报告

打开 Clinic Server 集群页，点击页面上的 **Benchmark Report**，在 **All Reports** 列表中点击 **View** 可以查看相应的报告，报告内容示例如下：

![benchmark-report](/media/clinic-benchmark-report.png)

> **注意：**
>
> 报告功能会持续优化，实际生成的内容可能比下面的说明更丰富。

报告分为以下几个部分：

- Workload situation：业务侧性能指标结果和建议。该部分的建议主要是针对业务请求的调整。
- Performance：数据库主要性能指标分析和建议。该部分分析节点是否均衡、数据库时间 (DB Time) 中主要阶段的时延是否在合理区间，并基于业务压力和时延数据提供配置优化的建议。
- Connection：连接数据分析和建议。该部分分析各节点连接是否均衡、空闲连接是否异常。
- Server：各节点资源使用情况分析。该部分分析各节点资源使用的现状和趋势。对于资源使用不均衡，或在短时间内资源使用可能会超过阈值的情况显示 Warning。

### Comparison Report

#### 生成报告

生成 Comparison Report 的步骤如下：

1. 登录 Clinic Server（[中国区](https://clinic.pingcap.com.cn)、[美国区](https://clinic.pingcap.com)）
2. 打开需要生成诊断报告的集群页面
3. 点击集群页面上的 **Comparison Report**
4. 选择两个对比时间段 **T1 Range** 和 **T2 Range**
5. 点击 **Create Report** 生成自定义报告

生成 Comparison Report 大约需要 5～30 分钟。因为报告需要处理日志数据，所以报告生成时间与对比时间段中日志数据量相关。

#### 解读报告

Comparison Report 会基于所选的两个时间段的 Metrics 和日志进行对比分析。报告中 Metrics 的计算方法是对两个时间段相应的指标时间序列数据取均值，然后将均值进行对比。

打开 Clinic Server 集群页，点击页面上的 **Comparison Report**，在 **All Reports** 列表中点击 **View** 可以查看相应的报告，报告内容示例如下：

![comparison-report](/media/clinic-comparison-report.png)

> **注意：**
>
> 报告功能会持续优化，实际生成的内容可能比下面的说明更丰富。

报告分为以下几个部分：

- 基本信息：列出 Comparison Report 对比的两个时间段信息。
- 主要指标对比：列出最关键的 12 个指标在前后两个时间段的对比。
- 业务指标对比：列出以下 5 个关键业务指标的对比：

    - QPS：每秒钟的请求次数。可以点击 **More** 对比不同请求类型的 QPS
    - Connection_count：连接数量。可以点击 **More** 对比不同 TiDB 节点的连接数量
    - Active_connection_count：活跃连接数量
    - CPS：每秒处理的命令数。可以点击 **More** 对比不同命令类型的 CPS
    - Plan_cache_OPS：所有 TiDB 实例每秒使用 Plan Cache 的查询数量

- 性能指标对比：列出系统中最重要的二十多个性能指标的对比，包括以下几个部分：

    - 基础指标：数据库时间和延迟等最基础的性能指标对比
    - 基于 SQL Phase 拆分的数据库时间对比
    - 数据库时间中耗时最长的 SQL 类型对比
    - SQL_execute_time 指标中耗时最长的请求类型对比
    - Duration 指标中耗时最长的 SQL 类型对比
    - KV request 细节数据对比
    - 其他性能指标对比

- 资源指标对比：列出 TiDB、TiKV、TiFlash 和 PD 节点的资源指标对比。不仅包括节点本身的对比，还会计算同类型节点资源使用的最大差值 delta，基于 delta 进行对比，展示节点不均衡状态的变化。

- 日志聚类对比：列出不同类型日志在前后两个时间段的数量，可以通过日志数量的变化了解系统内部任务运行情况的变化。

## 探索更多

- 在 TiUP 部署环境使用 PingCAP Clinic

    - [快速上手 PingCAP Clinic](/clinic/quick-start-with-clinic.md)
    - [PingCAP Clinic 诊断服务简介](/clinic/clinic-introduction.md)
    - [使用 PingCAP Clinic 诊断集群](/clinic/clinic-user-guide-for-tiup.md)
    - [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)

- 在 TiDB Operator 部署环境使用 PingCAP Clinic

    - [使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)
    - [PingCAP Clinic 数据采集说明](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-data-instruction)