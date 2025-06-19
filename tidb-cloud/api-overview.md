---
title: TiDB Cloud API 概述
summary: 了解什么是 TiDB Cloud API，其特性以及如何使用 API 管理你的 TiDB Cloud 集群。
---

# TiDB Cloud API 概述（Beta）

> **注意：**
>
> TiDB Cloud API 目前处于 beta 阶段。

TiDB Cloud API 是一个 [REST 接口](https://en.wikipedia.org/wiki/Representational_state_transfer)，为你提供了以编程方式访问和管理 TiDB Cloud 中管理对象的能力。通过这个 API，你可以自动且高效地管理项目、集群、备份、恢复、导入、计费以及 [Data Service](/tidb-cloud/data-service-overview.md) 中的资源。

该 API 具有以下特性：

- **JSON 实体。** 所有实体都以 JSON 格式表示。
- **仅支持 HTTPS。** 你只能通过 HTTPS 访问 API，确保所有通过网络发送的数据都使用 TLS 加密。
- **基于密钥的访问和摘要认证。** 在访问 TiDB Cloud API 之前，你必须生成一个 API 密钥，参考 [API 密钥管理](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-key-management)。所有请求都通过 [HTTP 摘要认证](https://en.wikipedia.org/wiki/Digest_access_authentication) 进行认证，确保 API 密钥永远不会在网络上传输。

要开始使用 TiDB Cloud API，请参考 TiDB Cloud API 文档中的以下资源：

- [入门指南](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Get-Started)
- [认证](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication)
- [速率限制](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Rate-Limiting)
- API 完整参考
    - v1beta1
        - [计费](https://docs.pingcap.com/tidbcloud/api/v1beta1/billing)
        - [Data Service](https://docs.pingcap.com/tidbcloud/api/v1beta1/dataservice)
        - [IAM](https://docs.pingcap.com/tidbcloud/api/v1beta1/iam)
        - [MSP（已弃用）](https://docs.pingcap.com/tidbcloud/api/v1beta1/msp)
    - [v1beta](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project)
- [更新日志](https://docs.pingcap.com/tidbcloud/api/v1beta#section/API-Changelog)
