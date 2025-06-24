---
title: Data Service 中的 API 密钥
summary: 了解如何为 Data App 创建、编辑和删除 API 密钥。
---

# Data Service 中的 API 密钥

TiDB Cloud Data API 支持[基本认证](https://en.wikipedia.org/wiki/Basic_access_authentication)和[摘要认证](https://en.wikipedia.org/wiki/Digest_access_authentication)。

- [基本认证](https://en.wikipedia.org/wiki/Basic_access_authentication)使用非加密的 base64 编码来传输你的公钥和私钥。HTTPS 确保传输安全。更多信息，请参见 [RFC 7617 - The 'Basic' HTTP Authentication Scheme](https://datatracker.ietf.org/doc/html/rfc7617)。
- [摘要认证](https://en.wikipedia.org/wiki/Digest_access_authentication)通过在网络传输前对你的公钥、私钥、服务器提供的 nonce 值、HTTP 方法和请求的 URI 进行哈希处理，提供了额外的安全层。这样可以加密私钥，防止其以明文形式传输。更多信息，请参见 [RFC 7616 - HTTP Digest Access Authentication](https://datatracker.ietf.org/doc/html/rfc7616)。

> **注意：**
>
> Data Service 中的 Data API 密钥与 [TiDB Cloud API](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication) 中使用的密钥不同。Data API 密钥用于访问 TiDB Cloud 集群中的数据，而 TiDB Cloud API 密钥用于管理项目、集群、备份、恢复和导入等资源。

## API 密钥概述

- API 密钥包含一个公钥和一个私钥，它们作为认证所需的用户名和密码。私钥仅在密钥创建时显示。
- 每个 API 密钥仅属于一个 Data App，用于访问 TiDB Cloud 集群中的数据。
- 你必须在每个请求中提供正确的 API 密钥。否则，TiDB Cloud 将返回 `401` 错误。

## 速率限制

请求配额受以下速率限制：

- TiDB Cloud Data Service 默认允许每个 API 密钥每分钟最多 100 个请求（rpm）。

    你可以在[创建](#创建-api-密钥)或[编辑](#编辑-api-密钥) API 密钥时编辑其速率限制。支持的值范围是从 `1` 到 `1000`。如果你每分钟的请求超过速率限制，API 将返回 `429` 错误。要获得每个 API 密钥每分钟超过 1000 个请求的配额，你可以向我们的支持团队[提交请求](https://tidb.support.pingcap.com/)。

    每个 API 请求都会返回以下有关限制的标头。

    - `X-Ratelimit-Limit-Minute`：每分钟允许的请求数。
    - `X-Ratelimit-Remaining-Minute`：当前分钟内剩余的请求数。当它达到 `0` 时，API 将返回 `429` 错误并指示你超过了速率限制。
    - `X-Ratelimit-Reset`：当前速率限制重置的时间（以秒为单位）。

  如果你超过速率限制，将返回如下错误响应：

    ```bash
    HTTP/2 429
    date: Mon, 05 Sep 2023 02:50:52 GMT
    content-type: application/json
    content-length: 420
    x-debug-trace-id: 202309040250529dcdf2055e7b2ae5e9
    x-ratelimit-reset: 8
    x-ratelimit-remaining-minute: 0
    x-ratelimit-limit-minute: 10
    x-kong-response-latency: 1
    server: kong/2.8.1

    {"type":"","data":{"columns":[],"rows":[],"result":{"latency":"","row_affect":0,"code":49900007,"row_count":0,"end_ms":0,"limit":0,"message":"API key rate limit exceeded. The limit can be increased up to 1000 requests per minute per API key in TiDB Cloud console. For an increase in quota beyond 1000 rpm, please contact us: https://tidb.support.pingcap.com/","start_ms":0}}}
    ```

- TiDB Cloud Data Service 允许每个 Chat2Query Data App 每天最多 100 个请求。

## API 密钥过期

默认情况下，API 密钥永不过期。但是，出于安全考虑，你可以在[创建](#创建-api-密钥)或[编辑](#编辑-api-密钥) API 密钥时为其指定过期时间。

- API 密钥仅在其过期时间之前有效。一旦过期，使用该密钥的所有请求都将失败并返回 `401` 错误，响应类似如下：

    ```bash
    HTTP/2 401
    date: Mon, 05 Sep 2023 02:50:52 GMT
    content-type: application/json
    content-length: 420
    x-debug-trace-id: 202309040250529dcdf2055e7b2ae5e9
    x-kong-response-latency: 1
    server: kong/2.8.1

    {"data":{"result":{"start_ms":0,"end_ms":0,"latency":"","row_affect":0,"limit":0,"code":49900002,"message":"API Key is no longer valid","row_count":0},"columns":[],"rows":[]},"type":""}
    ```

- 你也可以手动使 API 密钥过期。详细步骤，请参见[使单个 API 密钥过期](#使单个-api-密钥过期)和[使所有 API 密钥过期](#使所有-api-密钥过期)。一旦你手动使 API 密钥过期，过期将立即生效。

- 你可以在目标 Data App 的**认证**区域查看 API 密钥的状态和过期时间。

- 一旦过期，API 密钥就无法再次激活或编辑。

## 管理 API 密钥

以下部分描述如何为 Data App 创建、编辑、删除和使 API 密钥过期。

### 创建 API 密钥

要为 Data App 创建 API 密钥，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**认证**区域，点击**创建 API 密钥**。
4. 在**创建 API 密钥**对话框中，执行以下操作：

    1. （可选）为你的 API 密钥输入描述。
    2. 为你的 API 密钥选择角色。

        角色用于控制 API 密钥是否可以读取或写入链接到 Data App 的集群数据。你可以选择 `ReadOnly` 或 `ReadAndWrite` 角色：

        - `ReadOnly`：仅允许 API 密钥读取数据，如 `SELECT`、`SHOW`、`USE`、`DESC` 和 `EXPLAIN` 语句。
        - `ReadAndWrite`：允许 API 密钥读取和写入数据。你可以使用此 API 密钥执行所有 SQL 语句，如 DML 和 DDL 语句。

    3. （可选）为你的 API 密钥设置所需的速率限制。

       如果你每分钟的请求超过速率限制，API 将返回 `429` 错误。要获得每个 API 密钥每分钟超过 1000 个请求（rpm）的配额，你可以向我们的支持团队[提交请求](https://tidb.support.pingcap.com/)。

    4. （可选）为你的 API 密钥设置所需的过期时间。

        默认情况下，API 密钥永不过期。如果你想为 API 密钥指定过期时间，点击**在此时间后过期**，选择一个时间单位（`分钟`、`天`或`月`），然后填写该时间单位的所需数字。

5. 点击**下一步**。将显示公钥和私钥。

    确保你已将私钥复制并保存在安全的位置。离开此页面后，你将无法再次获取完整的私钥。

6. 点击**完成**。

### 编辑 API 密钥

> **注意**：
>
> 你无法编辑已过期的密钥。

要编辑 API 密钥的描述或速率限制，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**认证**区域，找到**操作**列，然后在要更改的 API 密钥行中点击 **...** > **编辑**。
4. 更新 API 密钥的描述、角色、速率限制或过期时间。
5. 点击**更新**。

### 删除 API 密钥

> **注意：**
>
> 在删除 API 密钥之前，请确保该 API 密钥未被任何 Data App 使用。

要删除 Data App 的 API 密钥，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在 **API 密钥**区域，找到**操作**列，然后在要删除的 API 密钥行中点击 **...** > **删除**。
4. 在显示的对话框中，确认删除。

### 使单个 API 密钥过期

> **注意**：
>
> 你无法使已过期的密钥过期。

要使 Data App 的 API 密钥过期，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**认证**区域，找到**操作**列，然后在要使其过期的 API 密钥行中点击 **...** > **立即过期**。
4. 在显示的对话框中，确认过期。

### 使所有 API 密钥过期

要使 Data App 的所有 API 密钥过期，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，点击目标 Data App 的名称以查看其详细信息。
3. 在**认证**区域，点击**全部过期**。
4. 在显示的对话框中，确认过期。
