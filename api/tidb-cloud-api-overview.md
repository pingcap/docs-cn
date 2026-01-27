---
title: TiDB Cloud API 概览
summary: 了解 TiDB Cloud API 的定义、特性，以及如何使用该 API 管理 TiDB Cloud 集群。
---

# TiDB Cloud API 概览

> **注意：**
>
> TiDB Cloud API 目前处于 beta 阶段。

TiDB Cloud API 是一个 [REST 接口](https://zh.wikipedia.org/wiki/表现层状态转换)，提供了以编程方式访问和操作 TiDB Cloud 中的各类管理资源的能力。通过该 API，你可以自动且高效地管理项目、集群、备份、恢复、导入、账单，以及 [Data Service](https://docs.pingcap.com/tidbcloud/data-service-overview) 中的相关资源。

该 API 具有以下特性：

- **JSON 实体 (JSON entities)**：API 中的所有资源和数据均使用 JSON 格式。
- **仅支持 HTTPS**：仅支持通过 HTTPS 访问该 API，从而确保所有通过网络传输的数据均经过 TLS 加密。
- **基于密钥的访问与摘要认证**：在访问 TiDB Cloud API 之前，你需要先生成一个 API key。具体步骤请参阅 [API Key Management](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)。所有请求都会通过 [HTTP 摘要认证](https://zh.wikipedia.org/wiki/HTTPP摘要认证)进行身份验证，从而确保 API key 不会以明文形式在网络中传输。

TiDB Cloud API 提供以下两个版本：

- [v1beta1](/api/tidb-cloud-api-v1beta1.md)：管理 TiDB Cloud Starter、Essential 与 Dedicated 集群，以及账单、Data Service 与 IAM 资源。
- [v1beta](/api/tidb-cloud-api-v1beta.md)：管理 TiDB Cloud 的项目、集群、备份、导入与恢复。
