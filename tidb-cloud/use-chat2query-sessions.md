---
title: 开始多轮 Chat2Query 对话
summary: 了解如何使用 Chat2Query 会话相关的 API 开始多轮对话。
---

# 开始多轮 Chat2Query 对话

从 v3 版本开始，Chat2Query API 支持通过调用会话相关的端点来进行多轮对话。您可以使用 `/v3/chat2data` 端点返回的 `session_id` 在下一轮对话中继续会话。

## 开始之前

在开始多轮 Chat2Query 对话之前，请确保您已经具备以下条件：

- 一个 [Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app)。
- 一个 [Chat2Query Data App 的 API 密钥](/tidb-cloud/use-chat2query-api.md#create-an-api-key)。
- 一个[目标数据库的数据摘要](/tidb-cloud/use-chat2query-api.md#1-generate-a-data-summary-by-calling-v3datasummaries)。

## 步骤 1. 开始会话

要开始会话，您可以调用 Chat2Query Data App 的 `/v3/sessions` 端点。

以下是调用此端点的通用代码示例。

> **提示：**
>
> 要获取特定端点的代码示例，请在 Data App 左侧窗格中点击端点名称，然后点击 **Show Code Example**。更多信息，请参见[获取端点的示例代码](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/sessions'\
    --header 'content-type: application/json'\
    --data-raw '{
    "cluster_id": "10140100115280519574",
    "database": "sp500insight",
    "name": "<Your session name>"
}'
```

在上述代码中，请求体是一个具有以下属性的 JSON 对象：

- `cluster_id`：_string_。TiDB 集群的唯一标识符。
- `database`：_string_。数据库名称。
- `name`：_string_。会话名称。

以下是一个响应示例：

```json
{
    "code": 200,
    "msg": "",
    "result": {
    "messages": [],
    "meta": {
        "created_at": 1718948875, // 表示会话创建时间的 UNIX 时间戳
        "creator": "<Your email>", // 会话创建者
        "name": "<Your session name>", // 会话名称
        "org_id": "1", // 组织 ID
        "updated_at": 1718948875 // 表示会话更新时间的 UNIX 时间戳
    },
    "session_id": 305685 // 会话 ID
    }
}
```

## 步骤 2. 使用会话调用 Chat2Data 端点

开始会话后，您可以调用 `/v3/sessions/{session_id}/chat2data` 在下一轮对话中继续会话。

以下是通用代码示例：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://eu-central-1.data.tidbcloud.com/api/v1beta/app/chat2query-YqAvnlRj/endpoint/v3/sessions/{session_id}/chat2data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "question": "<Your question to generate data>",
    "feedback_answer_id": "",
    "feedback_task_id": "",
    "sql_generate_mode": "direct"
}'
```

在上述代码中，请求体是一个具有以下属性的 JSON 对象：

- `question`：_string_。用自然语言描述您想要的查询的问题。
- `feedback_answer_id`：_string_。反馈答案 ID。此字段是可选的，仅用于反馈。
- `feedback_task_id`：_string_。反馈任务 ID。此字段是可选的，仅用于反馈。
- `sql_generate_mode`：_string_。生成 SQL 语句的模式。值可以是 `direct` 或 `auto_breakdown`。如果设置为 `direct`，API 将直接根据您提供的 `question` 生成 SQL 语句。如果设置为 `auto_breakdown`，API 将把 `question` 分解为多个任务，并为每个任务生成 SQL 语句。

以下是一个响应示例：

```json
{
  "code": 200,
  "msg": "",
  "result": {
    "job_id": "d96b6fd23c5f445787eb5fd067c14c0b",
    "session_id": 305685
  }
}
```

此响应与 `/v3/chat2data` 端点的响应类似。您可以通过调用 `/v2/jobs/{job_id}` 端点来检查作业状态。更多信息，请参见[通过调用 `/v2/jobs/{job_id}` 检查分析状态](/tidb-cloud/use-chat2query-api.md#2-check-the-analysis-status-by-calling-v2jobsjob_id)。
