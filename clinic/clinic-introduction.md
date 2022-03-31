---
title: PingCAP Clinic 诊断服务简介
summary: 介绍 PingCAP Clinic 诊断服务，包括工具组件、使用场景和工作原理。
---

# PingCAP Clinic 诊断服务简介

PingCAP Clinic 诊断服务（以下简称为 PingCAP Clinic）是 PingCAP 为 TiDB 集群提供的诊断服务，支持对使用 TiUP 或 TiDB Operator 部署的集群进行远程定位集群问题和本地快速检查集群状态，用于从全生命周期确保 TiDB 集群稳定运行、预测可出现的集群问题、降低问题出现概率、快速定位并修复问题。

[PingCAP Clinic 诊断服务](https://clinic.pingcap.com.cn)目前处于 Technical Preview 阶段。该服务提供以下两个组件进行集群诊断：

- Diag 诊断客户端：部署在集群侧的工具，用于采集集群的诊断数据 (collect)、上传诊断数据到 Clinic Server、对集群进行本地快速健康检查 (check)。如需了解 Diag 工具可采集的详细的数据列表，请参阅 [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)。

    > **注意：**
    >
    > Diag 诊断客户端暂时**不支持**对使用 TiDB Ansible 部署的集群进行数据采样。

- Clinic Server：部署在云端的云服务。Clinic Server 提供 SaaS 模式的诊断服务，不仅能接收上传到该组件的诊断数据，也可以提供在线诊断环境，用于存储、查看和诊断已上传的诊断数据，并提供集群诊断报告。

## 使用场景

- 远程定位集群问题

    当集群出现无法快速修复的问题时，可以求助社区论坛或者联系 PingCAP 技术支持。当申请远程协助时，你需要先保存问题现场的各种诊断数据，然后将其转发给相关技术人员。此时，你可以使用 Diag 诊断客户端，对诊断数据进行一键采集，快速收集完整的诊断数据，替代复杂的手动数据采集操作。随后，你可以将其诊断数据上传到 Clinic Server，供 PingCAP 技术人员查看。Clinic Server 为诊断数据提供了安全的存储，并支持在线诊断，提升了技术人员进行问题定位的效率。

- 本地快速检查集群状态

    即使集群可以正常运行，也需要定期检查集群是否有潜在的稳定性风险。PingCAP Clinic 提供的本地快速诊断功能，用于检查集群潜在的健康风险。目前 PingCAP Clinic Technical Preview 版本主要提供对集群配置项的合理性检查，用于发现不合理的配置，并提供修改建议。

## 工作原理

本章节主要介绍 Diag 诊断客户端（以下简称为 Diag）采集集群诊断数据的工作原理。

首先，Diag 需要从部署工具 TiUP (tiup-cluster) 或 TiDB Operator (tidb-operator) 获取集群拓扑信息，然后通过不同的数据采集方式来采集不同类型的诊断数据，具体采集方式如下：

- 通过 SCP 传输服务器文件

    对于使用 TiUP 部署的集群，Diag 可通过 SCP (Secure copy protocol) 直接从目标组件的节点采集日志文件和配置文件。

- 通过 SSH 远程执行命令采集数据

    对于 TiUP 部署的集群，Diag 可以通过 SSH (Secure Shell) 连接到目标组件系统，并可执行 Insight 等命令获取系统信息，包括内核日志、内核参数、系统和硬件的基础信息等。

- 通过 HTTP 调用采集数据

    - 通过调用 TiDB 组件的 HTTP 接口，Diag 可获取 TiDB、TiKV、PD 等组件的实时配置采样信息与实时性能采样信息。
    - 通过调用 Prometheus 的 HTTP 接口，Diag 可获取报警信息和 metrics 监控数据。

- 通过 SQL 语句查询数据库参数

    通过 SQL 语句，Diag 可以查询 TiDB 数据库的系统参数等信息。对于这种方式，你需要在采集数据时**额外提供**访问 TiDB 数据库的用户名和密码。

## 探索更多

- [快速上手 PingCAP Clinic](/clinic/quick-start-with-clinic)
- [使用 PingCAP Clinic](/clinic/clinic-user-guide-for-tiup.md)
- [PingCAP Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)