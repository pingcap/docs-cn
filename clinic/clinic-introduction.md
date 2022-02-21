---
title: Clinic 诊断服务简介
summary: 介绍 Clinic 诊断服务，包括工具组件、使用场景和工作原理。
---

## Clinic 诊断服务简介

Clinic 是 PingCAP 为 TiDB 集群提供的诊断服务，支持对使用 TiUP 或 TiDB Operator 部署的集群进行远程定位集群问题和本地快速检查集群状态，用于从全生命周期确保 TiDB 集群稳定运行、预测并降低问题出现概率、快速定位并修复问题。

> **注意：**
>
> Clinic 诊断服务目前处于 Beta 受邀测试使用阶段，不建议在生产场景中直接使用。

Clinic 服务提供以下两个组件进行集群诊断：

- Diag：部署在集群侧的工具，用于采集集群的诊断数据 (collect）、对集群进行本地快速健康检查 (check)、上传诊断数据。如需了解 Diag 工具采集的详细的数据列表，请参阅 [Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)。

    > **注意：**
    >
    > - Diag 暂时**不支持**对开启了 TLS 加密的集群和使用 TiDB Ansible 部署的集群进行数据采样。
    > - 目前 Clinic 处于 Beta 受邀测试使用阶段，如需使用 Diag 将数据上传到 Clinic Server，请联系与你对接的 PingCAP 技术人员获取试用账号。

- Clinic Server：部署在云端的云服务。Clinic Server 提供 SaaS 模式的诊断服务，可接收上传到该组件的诊断数据，也可提供诊断数据的存储、在线查看、在线诊断以及诊断报告。

    > **注意：**
    >
    > Clinic Beta 版本的 Server 端功能暂未开放给外部用户使用。当你将采集好的数据上传到 Clinic Server 并获取了数据链接后，只有经过授权的 PingCAP 技术支持人员可以访问其链接并查看数据。

## 使用场景

- 远程定位集群问题：

    当集群出现无法快速修复的问题时，可以求助社区论坛或者联系 PingCAP 技术支持。当申请远程协助时，你需要先保存问题现场的各种诊断数据后，将其转发给相关技术人员。此时，你可以使用 Clinic Diag 工具，对诊断数据进行一键采集，快速收集完整的诊断数据，替代复杂的手动数据采集操作。随后，你可以将其诊断数据上传到 Clinic Server，供 PingCAP 技术人员查看。Clinic Server 为诊断数据提供了安全的存储，并支持在线诊断，提升了技术人员进行问题定位的效率。

    目前 Clinic 处于 Beta 受邀测试使用阶段，如需将数据上传到 Clinic Server，请联系与你对接的 PingCAP 技术人员获取试用账号。

- 本地快速检查集群状态：

    即使集群可以正常运行，也需要定期检查集群是否有潜在的稳定性风险。Clinic 提供的本地快速诊断功能，用于检查集群潜在的健康风险。目前 Clinic Beta 版本主要提供对集群配置项的合理性检查，用于发现不合理的配置，并提供修改建议。

## 工作原理

本章节主要介绍 Clinic 的集群侧工具 Diag 采集集群诊断数据的工作原理。

首先，Diag 需要从部署工具 TiUP (tiup-cluster) 或 TiDB Operator (tidb-operator) 获取集群拓扑信息，然后通过不同的数据采集方式来采集不同类型的诊断数据，具体采集方式如下：

- 通过 SCP 方式传输服务器文件

    对于使用 TiUP 部署的集群，Diag 可通过 SCP 方式直接从目标组件的节点采集日志文件和配置文件。

- 通过 SSH 远程执行命令采集数据

    对于 TiUP 部署的集群，Diag 可以通过 SSH (Secure Shell) 连接到目标组件系统，并可执行 Insight 等命令获取系统信息，包括内核日志、内核参数、基础的系统和硬件信息等。

- 通过 HTTP 调用采集数据

    - 通过调用 TiDB 组件的 HTTP 接口，Diag 可获取 TiDB、TiKV、PD 等组件的实时配置采样信息与实时性能采样信息。
    - 通过调用 Prometheus 的 HTTP 接口，Diag 可获取报警信息和 metrics 监控数据。

- 通过 SQL 语句查询数据库参数

    通过 SQL 语句，Diag 可查询 TiDB 数据库的系统参数等信息。对于这种方式，你需要在采集数据时**额外提供**访问 TiDB 数据库的用户名和密码。

## 探索更多

 - [使用 Clinic](/clinic/clinic-data-instruction-for-tiup.md)
 - [Clinic 数据采集说明](/clinic/clinic-data-instruction-for-tiup.md)