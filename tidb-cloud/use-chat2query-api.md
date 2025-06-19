---
title: Chat2Query API 入门指南
summary: 了解如何使用 TiDB Cloud Chat2Query API，通过提供指令来生成和执行 SQL 语句。
---

# Chat2Query API 入门指南

TiDB Cloud 提供 Chat2Query API，这是一个 RESTful 接口，使您能够通过提供指令来使用 AI 生成和执行 SQL 语句。然后，API 会为您返回查询结果。

Chat2Query API 只能通过 HTTPS 访问，确保所有通过网络传输的数据都使用 TLS 加密。

> **注意：**
>
> Chat2Query API 适用于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。要在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 Chat2Query API，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。

## 开始之前

在调用 Chat2Query 端点之前，您需要创建一个 Chat2Query Data App 并为该 Data App 创建一个 API 密钥。

### 创建 Chat2Query Data App

要为您的项目创建 Data App，请执行以下步骤：

1. 在项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面，点击左侧窗格中的 <MDSvgIcon name="icon-create-data-app" /> **Create DataApp**。此时会显示数据应用创建对话框。

    > **提示：**
    >
    > 如果您在集群的 **SQL Editor** 页面，也可以通过点击右上角的 **...** ，选择 **Access Chat2Query via API**，然后点击 **New Chat2Query Data App** 来打开数据应用创建对话框。

2. 在对话框中，为您的 Data App 定义一个名称，选择所需的集群作为数据源，并选择 **Chat2Query Data App** 作为 **Data App** 类型。您还可以选择为 App 编写描述。

3. 点击 **Create**。

   新创建的 Chat2Query Data App 将显示在左侧窗格中。在此 Data App 下，您可以找到 Chat2Query 端点列表。

### 创建 API 密钥

在调用端点之前，您需要为 Chat2Query Data App 创建一个 API 密钥，该密钥用于端点访问 TiDB Cloud 集群中的数据。

要创建 API 密钥，请执行以下步骤：

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 的左侧窗格中，点击您的 Chat2Query Data App 以在右侧查看其详细信息。
2. 在 **Authentication** 区域，点击 **Create API Key**。
3. 在 **Create API Key** 对话框中，输入描述，然后为您的 API 密钥选择以下角色之一：

   - `Chat2Query Admin`：允许 API 密钥管理数据摘要、根据提供的指令生成 SQL 语句，并执行任何 SQL 语句。
   - `Chat2Query Data Summary Management Role`：仅允许 API 密钥生成和更新数据摘要。

        > **提示：**
        >
        > 对于 Chat2Query API，数据摘要是 AI 对您的数据库的分析结果，包括您的数据库描述、表描述和列描述。通过生成数据库的数据摘要，您可以在通过提供指令生成 SQL 语句时获得更准确的响应。

   - `Chat2Query SQL ReadOnly`：仅允许 API 密钥根据提供的指令生成 SQL 语句并执行 `SELECT` SQL 语句。
   - `Chat2Query SQL ReadWrite`：允许 API 密钥根据提供的指令生成 SQL 语句并执行任何 SQL 语句。

4. 默认情况下，API 密钥永不过期。如果您想为密钥设置过期时间，请点击 **Expires in**，选择时间单位（`Minutes`、`Days` 或 `Months`），然后填写所需的时间单位数值。

5. 点击 **Next**。此时会显示公钥和私钥。

    确保您已将私钥复制并保存在安全的位置。离开此页面后，您将无法再次获取完整的私钥。

6. 点击 **Done**。

## 调用 Chat2Query 端点

> **注意：**
>
> 每个 Chat2Query Data App 每天有 100 个请求的速率限制。如果超过速率限制，API 将返回 `429` 错误。如需更多配额，您可以向我们的支持团队[提交请求](https://tidb.support.pingcap.com/)。

在每个 Chat2Query Data App 中，您可以找到以下端点：

- Chat2Query v3 端点：名称以 `/v3` 开头的端点，如 `/v3/dataSummaries` 和 `/v3/chat2data`（推荐）
- Chat2Query v2 端点：名称以 `/v2` 开头的端点，如 `/v2/dataSummaries` 和 `/v2/chat2data`
- Chat2Query v1 端点：`/v1/chat2data`（已弃用）

> **提示：**
>
> 与 `/v1/chat2data` 相比，`/v3/chat2data` 和 `/v2/chat2data` 需要您先通过调用 `/v3/dataSummaries` 或 `/v2/dataSummaries` 分析您的数据库。因此，`/v3/chat2data` 和 `/v2/chat2data` 返回的结果通常更准确。

### 获取端点的代码示例

TiDB Cloud 提供代码示例来帮助您快速调用 Chat2Query 端点。要获取 Chat2Query 端点的代码示例，请执行以下步骤：

1. 在 [**Data Service**](https://tidbcloud.com/project/data-service) 页面的左侧窗格中，点击 Chat2Query 端点的名称。

    右侧将显示调用此端点的信息，如端点 URL、代码示例和请求方法。

2. 点击 **Show Code Example**。

3. 在显示的对话框中，选择要用于调用端点的集群、数据库和身份验证方法，然后复制代码示例。

    > **注意：**
    >
    > 对于某些端点（如 `/v2/jobs/{job_id}`），您只需要选择身份验证方法。

4. 要调用端点，您可以将示例粘贴到您的应用程序中，用您自己的参数替换示例中的参数（如用您的 API 密钥替换 `${PUBLIC_KEY}` 和 `${PRIVATE_KEY}` 占位符），然后运行它。

### 调用 Chat2Query v3 端点或 v2 端点

TiDB Cloud Data Service 提供以下 Chat2Query v3 端点和 v2 端点：

| 方法 | 端点 | 描述 |
| ------ | -------- | ----------- |
| POST   | `/v3/dataSummaries` | 此端点使用人工智能分析为您的数据库模式、表模式和列模式生成数据摘要。 |
| GET    | `/v3/dataSummaries` | 此端点检索您数据库的所有数据摘要。 |
| GET    | `/v3/dataSummaries/{data_summary_id}` | 此端点检索特定的数据摘要。 |
| PUT    | `/v3/dataSummaries/{data_summary_id}` | 此端点更新特定的数据摘要。 |
| PUT    | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}` | 此端点更新特定数据摘要中特定表的描述。 |
| PUT    | `/v3/dataSummaries/{data_summary_id}/tables/{table_name}/columns` | 此端点更新特定数据摘要中特定表的列描述。 |
| POST   | `/v3/knowledgeBases` | 此端点创建新的知识库。有关知识库相关端点的使用信息，请参见[使用知识库](/tidb-cloud/use-chat2query-knowledge.md)。 |
| GET    | `/v3/knowledgeBases` | 此端点检索所有知识库。 |
| GET    | `/v3/knowledgeBases/{knowledge_base_id}` | 此端点检索特定的知识库。 |
| PUT    | `/v3/knowledgeBases/{knowledge_base_id}` | 此端点更新特定的知识库。 |
| POST   | `/v3/knowledgeBases/{knowledge_base_id}/data` | 此端点向特定知识库添加数据。 |
| GET    | `/v3/knowledgeBases/{knowledge_base_id}/data` | 此端点从特定知识库检索数据。 |
| PUT    | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | 此端点更新知识库中的特定数据。 |
| DEL    | `/v3/knowledgeBases/{knowledge_base_id}/data/{knowledge_data_id}` | 此端点从知识库中删除特定数据。 |
| POST   | `/v3/sessions` | 此端点创建新的会话。有关会话相关端点的使用信息，请参见[开始多轮 Chat2Query](/tidb-cloud/use-chat2query-sessions.md)。 |
| GET    | `/v3/sessions` | 此端点检索所有会话的列表。 |
| GET    | `/v3/sessions/{session_id}` | 此端点检索特定会话的详细信息。 |
| PUT    | `/v3/sessions/{session_id}` | 此端点更新特定会话。 |
| PUT    | `/v3/sessions/{session_id}/reset` | 此端点重置特定会话。 |
| POST   | `/v3/sessions/{session_id}/chat2data` | 此端点在特定会话中使用人工智能生成和执行 SQL 语句。更多信息，请参见[使用会话开始多轮 Chat2Query](/tidb-cloud/use-chat2query-sessions.md)。 |
| POST   | `/v3/chat2data` | 此端点使您能够通过提供数据摘要 ID 和指令使用人工智能生成和执行 SQL 语句。 |
| POST   | `/v3/refineSql` | 此端点使用人工智能优化现有的 SQL 查询。 |
| POST   | `/v3/suggestQuestions` | 此端点根据提供的数据摘要建议问题。 |
| POST   | `/v2/dataSummaries` | 此端点使用人工智能为您的数据库模式、表模式和列模式生成数据摘要。 |
| GET    | `/v2/dataSummaries` | 此端点检索所有数据摘要。 |
| POST   | `/v2/chat2data` | 此端点使您能够通过提供数据摘要 ID 和指令使用人工智能生成和执行 SQL 语句。 |
| GET    | `/v2/jobs/{job_id}` | 此端点使您能够查询特定数据摘要生成作业的状态。 |

调用 `/v3/chat2data` 和 `/v2/chat2data` 的步骤相同。以下部分以 `/v3/chat2data` 为例说明如何调用它。

#### 1. 通过调用 `/v3/dataSummaries` 生成数据摘要

在调用 `/v3/chat2data` 之前，先让 AI 分析数据库并通过调用 `/v3/dataSummaries` 生成数据摘要，这样 `/v3/chat2data` 在后续的 SQL 生成中可以获得更好的性能。

以下是调用 `/v3/dataSummaries` 分析 `sp500insight` 数据库并为该数据库生成数据摘要的代码示例：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/dataSummaries'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "description": "Data summary for SP500 Insight",
    "reuse": false
}'
```

在上述示例中，请求体是一个具有以下属性的 JSON 对象：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库的名称。
- `description`：_string_。数据摘要的描述。
- `reuse`：_boolean_。指定是否重用现有的数据摘要。如果设置为 `true`，API 将重用现有的数据摘要。如果设置为 `false`，API 将生成新的数据摘要。

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "data_summary_id": 304823,
    "job_id": "fb99ef785da640ab87bf69afed60903d"
  }
}
```

#### 2. 通过调用 `/v2/jobs/{job_id}` 检查分析状态

`/v3/dataSummaries` API 是异步的。对于具有大型数据集的数据库，可能需要几分钟才能完成数据库分析并返回完整的数据摘要。

要检查数据库的分析状态，您可以调用 `/v2/jobs/{job_id}` 端点，如下所示：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>`/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1699518950, // 作业完成时的 UNIX 时间戳
    "job_id": "fb99ef785da640ab87bf69afed60903d", // 当前作业的 ID
    "result": DataSummaryObject, // 给定数据库的 AI 探索信息
    "status": "done" // 当前作业的状态
  }
}
```

如果 `"status"` 为 `"done"`，则完整的数据摘要已准备就绪，您现在可以通过调用 `/v3/chat2data` 为此数据库生成和执行 SQL 语句。否则，您需要等待并稍后再次检查分析状态，直到完成。

在响应中，`DataSummaryObject` 表示给定数据库的 AI 探索信息。`DataSummaryObject` 的结构如下：

```js
{
    "cluster_id": "10140100115280519574", // 集群 ID
    "data_summary_id": 304823, // 数据摘要 ID
    "database": "sp500insight", // 数据库名称
    "default": false, // 此数据摘要是否为默认摘要
    "status": "done", // 数据摘要的状态
    "description": {
        "system": "Data source for financial analysis and decision-making in stock market", // AI 生成的数据摘要描述
        "user": "Data summary for SP500 Insight" // 用户提供的数据摘要描述
    },
    "keywords": ["User_Stock_Selection", "Index_Composition"], // 数据摘要的关键词
    "relationships": {
        "companies": {
            "referencing_table": "...", // 引用 `companies` 表的表
            "referencing_table_column": "..." // 引用 `companies` 表的列
            "referenced_table": "...", // `companies` 表引用的表
            "referenced_table_column": "..." // `companies` 表引用的列
        }
    }, // 表之间的关系
    "summary": "Financial data source for stock market analysis", // 数据摘要的概要
    "tables": { // 数据库中的表
      "companies": {
        "name": "companies" // 表名
        "description": "This table provides comprehensive...", // 表的描述
        "columns": {
          "city": { // 表中的列
            "name": "city" // 列名
            "description": "The city where the company is headquartered.", // 列的描述
          }
        },
      },
    }
}
```

#### 3. 通过调用 `/v3/chat2data` 生成和执行 SQL 语句

当数据库的数据摘要准备就绪时，您可以通过提供集群 ID、数据库名称和您的问题来调用 `/v3/chat2data` 生成和执行 SQL 语句。

例如：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "question": "<Your question to generate data>",
    "sql_generate_mode": "direct"
}'
```

请求体是一个具有以下属性的 JSON 对象：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库的名称。
- `data_summary_id`：_integer_。用于生成 SQL 的数据摘要的 ID。此属性仅在未提供 `cluster_id` 和 `database` 时生效。如果同时指定了 `cluster_id` 和 `database`，API 将使用数据库的默认数据摘要。
- `question`：_string_。用自然语言描述您想要的查询的问题。
- `sql_generate_mode`：_string_。生成 SQL 语句的模式。值可以是 `direct` 或 `auto_breakdown`。如果设置为 `direct`，API 将直接根据您提供的 `question` 生成 SQL 语句。如果设置为 `auto_breakdown`，API 将把 `question` 分解为多个任务，并为每个任务生成 SQL 语句。

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "job_id": "20f7577088154d7889964f1a5b12cb26",
    "session_id": 304832
  }
}
```

如果您收到状态码为 `400` 的响应，如下所示，这意味着您需要等待一段时间，让数据摘要准备就绪。

```js
{
    "code": 400,
    "msg": "Data summary is not ready, please wait for a while and retry",
    "result": {}
}
```

`/v3/chat2data` API 是异步的。您可以通过调用 `/v2/jobs/{job_id}` 端点来检查作业状态：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request GET 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v2/jobs/{job_id}'\
 --header 'content-type: application/json'
```

示例响应如下：

```js
{
  "code": 200,
  "msg": "",
  "result": {
    "ended_at": 1718785006, // 作业完成时的 UNIX 时间戳
    "job_id": "20f7577088154d7889964f1a5b12cb26",
    "reason": "", // 如果作业失败，则为失败原因
    "result": {
      "assumptions": [],
      "chart_options": { // 为结果生成的图表选项
        "chart_name": "Table",
        "option": {
          "columns": [
            "total_users"
          ]
        },
        "title": "Total Number of Users in the Database"
      },
      "clarified_task": "Count the total number of users in the database.", // 任务的明确描述
      "data": { // SQL 语句返回的数据
        "columns": [
          {
            "col": "total_users"
          }
        ],
        "rows": [
          [
            "1"
          ]
        ]
      },
      "description": "",
      "sql": "SELECT COUNT(`user_id`) AS total_users FROM `users`;", // 生成的 SQL 语句
      "sql_error": null, // SQL 语句的错误消息
      "status": "done", // 作业的状态
      "task_id": "0",
      "type": "data_retrieval" // 作业的类型
    },
    "status": "done"
  }
}
```

### 调用 Chat2Data v1 端点（已弃用）

> **注意：**
>
> Chat2Data v1 端点已弃用。建议您改用 Chat2Data v3 端点。

TiDB Cloud Data Service 提供以下 Chat2Query v1 端点：

|  方法 | 端点| 描述 |
|  ----  | ----  |----  |
|  POST | `/v1/chat2data`  | 此端点允许您通过提供目标数据库名称和指令使用人工智能生成和执行 SQL 语句。  |

您可以直接调用 `/v1/chat2data` 端点来生成和执行 SQL 语句。与 `/v2/chat2data` 相比，`/v1/chat2data` 提供更快的响应但性能较低。

TiDB Cloud 生成代码示例来帮助您调用端点。要获取示例并运行代码，请参见[获取端点的代码示例](#获取端点的代码示例)。

调用 `/v1/chat2data` 时，您需要替换以下参数：

- 用您的 API 密钥替换 `${PUBLIC_KEY}` 和 `${PRIVATE_KEY}` 占位符。
- 用您要查询的表名替换 `<your table name, optional>` 占位符。如果不指定表名，AI 将查询数据库中的所有表。
- 用您希望 AI 生成和执行 SQL 语句的指令替换 `<your instruction>` 占位符。

> **注意：**
>
> - 每个 Chat2Query Data App 每天有 100 个请求的速率限制。如果超过速率限制，API 将返回 `429` 错误。如需更多配额，您可以向我们的支持团队[提交请求](https://tidb.support.pingcap.com/)。
> - 具有 `Chat2Query Data Summary Management Role` 角色的 API 密钥不能调用 Chat2Data v1 端点。

以下代码示例用于计算 `sp500insight.users` 表中有多少用户：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.dev.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "10939961583884005252",
    "database": "sp500insight",
    "tables": ["users"],
    "instruction": "count the users"
}'
```

在上述示例中，请求体是一个具有以下属性的 JSON 对象：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库的名称。
- `tables`：_array_。（可选）要查询的表名列表。
- `instruction`：_string_。用自然语言描述您想要的查询的指令。

响应如下：

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [
      {
        "col": "COUNT(`user_id`)",
        "data_type": "BIGINT",
        "nullable": false
      }
    ],
    "rows": [
      {
        "COUNT(`user_id`)": "1"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1699529488292,
      "end_ms": 1699529491901,
      "latency": "3.609656403s",
      "row_count": 1,
      "row_affect": 0,
      "limit": 1000,
      "sql": "SELECT COUNT(`user_id`) FROM `users`;",
      "ai_latency": "3.054822491s"
    }
  }
}
```

如果您的 API 调用不成功，您将收到状态码不是 `200` 的响应。以下是状态码 `500` 的示例：

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 500,
      "message": "internal error! defaultPermissionHelper: rpc error: code = DeadlineExceeded desc = context deadline exceeded",
      "start_ms": "",
      "end_ms": "",
      "latency": "",
      "row_count": 0,
      "row_affect": 0,
      "limit": 0
    }
  }
}
```

## 了解更多

- [管理 API 密钥](/tidb-cloud/data-service-api-key.md)
- [开始多轮 Chat2Query](/tidb-cloud/use-chat2query-sessions.md)
- [使用知识库](/tidb-cloud/use-chat2query-knowledge.md)
- [Data Service 的响应和状态码](/tidb-cloud/data-service-response-and-status-code.md)
