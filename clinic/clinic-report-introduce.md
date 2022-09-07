---
title: 使用 PingCAP Clinic Reports
summary: 介绍 PingCAP Clinic Report 相关功能。
---

# 使用 PingCAP Clinic Reports

Clinic 服务端对用户上传的诊断数据提供报告，可以在特定场景下检查集群健康风险并协助定位集群问题。本文将介绍报告的使用场景和使用方法。

> **注意：**
>
> 报告基于诊断数据中的 Metrics 数据和日志数据，为了获取完整的诊断建议，用户需要完整收集集群诊断数据。


## 使用场景

- 压力测试场景

    在性能测试或者新业务压力接入测试的阶段，需要对系统性能进行评估，并通过对上层业务请求和下层数据库配制参数的调整，提升整体性能。通过 Benchmark Report 可以检查当前系统性能状态，发现风险问题，提出对业务层和集群配置的优化建议。

- 性能对比检查场景

    在很多场景中，需要对集群各种关键指标进行对比，可以通过 Comparison Report 快速了解不同时间段的运行状态差异，比手动对比提升效率和准确性，对比的内容包括：QPS 差异，延迟差异，性能指标差异，系统资源使用差异，关键日志差异等。需要进行对比的场景有：
    - 集群健康巡检时，对比本次性能与上次巡检的差异
    - 集群修改了关键参数或配置后，对比修改前后的差异
    - 集群升级后，对比升级前后的差异
    - 集群接入新业务后，对比接入前后的差异

## 使用方法

### Benchmark Report

#### 前提条件

Clinic 报告基于集群诊断数据生成，需要使用 Diag 采集数据并上传到 Clinic server 后，报告才能生成。具体的采集方法，TiUP 部署环境参见[使用 PingCAP Clinic 诊断 TiDB 集群](/clinic/clinic-user-guide-for-tiup.md) ， Operator 部署环境参见[使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)。

#### 生成报告
- 生成默认报告

    Benchmark Report 会在数据包上传到 Clinic Server 后自动生成，由于生产报告需要先将相关诊断数据从数据包中解压提取，所以报告运行时间会在 5 分钟以上（数据包越大，所需时间越长）。

- 生成自定义报告

    默认生成的报告是基于数据包的起止时间，如果需要自定义报告时间，可以打开 Clinic 的集群详情页，点击页面上的“ Benchmark Report”, 选择报告的开始和结束时间，点击“create” 生成新的报告。

#### 解读报告

打开 Clinic 集群页面，点击页面上的“ Benchmark Report”,  点击“View” 可以查看报告。
[benchmark-report](/media/clinic-benchmark-report.png)

报告分为以下几个部分：

-  Workload situation ：业务侧性能指标结果和建议，该部分的建议主要是针对业务请求的调整。
- Performance ：数据库主要性能指标分析和建议，该部分分析节点是否均衡，数据库时间（DB time） 中主要阶段的时延是否在合理区间，并基于用户业务压力和时延数据提供配置优化的建议。
- Connection ：连接数据分析和建议，该部分分析各节点连接是否均衡， Idle connection 是否有异常。
- Server ：各节点资源使用情况分析，该部分分析各节点资源使用的现状和趋势，对于资源使用不均衡，或者在短时间内资源使用会超过阈值的情况显示 warning。

### Comparison Report

#### 前提条件

Clinic 报告基于集群诊断数据生成，需要使用 Diag 采集数据并上传到 Clinic server 后，报告才能生成。具体的采集方法，TiUP 部署环境参见[使用 PingCAP Clinic 诊断 TiDB 集群](/clinic/clinic-user-guide-for-tiup.md) ， Operator 部署环境参见[使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)。

#### 运行报告

打开 Clinic 集群页面，点击页面上的“ Comparison Report”，选择两个时间段，点击 “Create Report” 创建报告。对比报告生成大约需要 5 ～ 30分钟，因为对比分析需要处理日志数据，运行时间与该时间段中日志数据量相关。

#### 解读报告

对比报告会基于所选的两个时间段的 metrics 和日志进行对比分析。打开 Clinic 集群页面，点击页面上的“ Comparison Report”，在 Report 列表中点击“View” 可以查看。
[comparison-report](/media/clinic-comparison-report.png)

报告中的 Metrics 计算方法是对两个时间段相应的指标时间序列数据取均值，然后将均值进行对比。

报告分为以下几个部分：
- 主要指标对比 ：列出最关键的12个指标在前后两个时间段的对比。
- 业务指标对比 ：列出以下五个关键业务指标的对比：
  - QPS：每秒钟的请求次数 ，支持展开不同请求类型的 QPS 对比。
  - Connnection_count ：连接数量，支持展开不同 TiDB 节点的连接数量对比。
  - Active_connection_count ：活跃连接数量
  - CPS ：每秒处理的命令数，支持展开不同命令类型的对比。
- 性能指标对比 ：列出系统中最重要的20+性能指标的对比，包括以下几个部分：
  - 基础指标: 数据库时间（DB Time）和延迟等最基础的性能指标对比。
  - 基于 SQL Phase 拆分的 Database time 对比
  - DB 时间中耗时最长的 SQL 类型比对
  - SQL_execute_time 指标中耗时最长的请求类型对比
  - Duration 指标中耗时最长的 SQL 类型对比
  - KV request 细节数据对比
  - 其他性能指标对比
- 资源指标对比 ：列出系统 PD、TiDB、TiKV、TiFlash 节点的资源指标对比，不但包括节点本身的对比，还会计算同类型节点资源使用的最大差值 delta，基于 delta 进行对比，展示节点不均衡状态的变化。
- 日志聚类对比 ：列出不同类型日志在前后两个时间段的数量，可以通过日志数量的变化了解系统内部任务运行情况的变化。

> **说明：**
>
> 报告功能会持续优化，您看到的内容可能比本文说明中更丰富。

## 探索更多

- 在 TiUP 部署环境使用 PingCAP Clinic

    - [快速上手 PingCAP Clinic](/clinic/quick-start-with-clinic.md)
    - [使用 PingCAP Clinic 诊断 TiDB 集群](/clinic/clinic-user-guide-for-tiup.md)
    - [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)

- 在 TiDB Operator 部署环境使用 PingCAP Clinic

    - [使用 PingCAP Clinic](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-user-guide)
    - [PingCAP Clinic 数据采集说明](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/clinic-data-instruction)