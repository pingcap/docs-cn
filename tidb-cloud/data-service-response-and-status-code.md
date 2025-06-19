---
title: Data Service 的响应和 HTTP 状态码
summary: 本文档描述了 TiDB Cloud 中 Data Service 的响应和 HTTP 状态码。
---

# Data Service 的响应和 HTTP 状态码

当你调用 [Data Service](/tidb-cloud/data-service-overview.md) 中定义的 API 端点时，Data Service 会返回一个 HTTP 响应。理解这个响应的结构和状态码的含义对于解释 Data Service 端点返回的数据至关重要。

本文档描述了 TiDB Cloud 中 Data Service 的响应和状态码。

## 响应

Data Service 返回带有 JSON 主体的 HTTP 响应。

> **注意：**
>
> 当你调用包含多个 SQL 语句的端点时，Data Service 会逐个执行这些语句，但在 HTTP 响应中只返回最后一个语句的执行结果。

响应主体包含以下字段：

- `type`：_string_。此端点的类型。值可能是 `"sql_endpoint"` 或 `"chat2data_endpoint"`。不同的端点返回不同类型的响应。
- `data`：_object_。执行结果，包括三个部分：

    - `columns`：_array_。返回字段的架构信息。
    - `rows`：_array_。以 `key:value` 格式返回的结果。

        当为端点启用**批处理操作**且端点的最后一个 SQL 语句是 `INSERT` 或 `UPDATE` 操作时，请注意以下事项：

        - 端点的返回结果还将包括每行的 `"message"` 和 `"success"` 字段，以指示其响应和状态。
        - 如果目标表的主键列配置为 `auto_increment`，端点的返回结果还将包括每行的 `"auto_increment_id"` 字段。对于 `INSERT` 操作，此字段的值是自增 ID，对于其他操作（如 `UPDATE`），此字段的值是 `null`。

    - `result`：_object_。SQL 语句的执行相关信息，包括成功/失败状态、执行时间、返回的行数和用户配置。

以下是一个示例响应：

<SimpleTab>
<div label="SQL 端点">

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [
            {
                "auto_increment_id": "270001",
                "index": "0",
                "message": "Row insert successfully",
                "success": "true"
            },
            {
                "auto_increment_id": "270002",
                "index": "1",
                "message": "Row insert successfully",
                "success": "true"
            }
        ],
        "result": {
            "code": 200,
            "message": "Query OK, 2 rows affected (8.359 sec)",
            "start_ms": 1689593360560,
            "end_ms": 1689593368919,
            "latency": "8.359s",
            "row_count": 2,
            "row_affect": 2,
            "limit": 500
        }
    }
}
```

</div>

<div label="Chat2Data 端点">

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [
      {
        "col": "id",
        "data_type": "BIGINT",
        "nullable": false
      },
      {
        "col": "type",
        "data_type": "VARCHAR",
        "nullable": false
      }
    ],
    "rows": [
      {
        "id": "20008295419",
        "type": "CreateEvent"
      }
    ],
    "result": {
      "code": 200,
      "message": "Query OK!",
      "start_ms": 1678965476709,
      "end_ms": 1678965476839,
      "latency": "130ms",
      "row_count": 1,
      "row_affect": 0,
      "limit": 50
      "sql": "select id,type from sample_data.github_events limit 1;",
      "ai_latency": "30ms"
    }
  }
}
```

</div>
</SimpleTab>

## 状态码

### 200

如果 HTTP 状态码为 `200` 且 `data.result.code` 字段也显示 `200`，这表示 SQL 语句执行成功。否则，TiDB Cloud 无法执行你的端点中定义的 SQL 语句。你可以查看 `code` 和 `message` 字段以获取详细信息。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 1146,
            "message": "table not found",
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

### 400

此状态码表示参数检查失败。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 400,
            "message": "param check failed! {detailed error}",
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

### 401

此状态码表示由于缺少权限导致认证失败。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 401,
            "message": "auth failed",
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

### 404

此状态码表示由于无法找到指定的端点导致认证失败。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 404,
            "message": "endpoint not found",
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

### 405

此状态码表示请求使用了不允许的方法。请注意，Data Service 仅支持 `GET` 和 `POST`。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 405,
            "message": "method not allowed",
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

### 408

此状态码表示请求超过了端点的超时时间。要修改端点的超时时间，请参见[配置属性](/tidb-cloud/data-service-manage-endpoint.md#配置属性)。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 408,
            "message": "request timeout.",
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

### 429

此状态码表示请求超过了 API 密钥的速率限制。要获取更多配额，你可以向我们的支持团队[提交请求](https://tidb.support.pingcap.com/)。

以下是一个示例响应：

<SimpleTab>
<div label="SQL 端点">

```json
{
  "type": "",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 49900007,
      "message": "The request exceeded the limit of 100 times per apikey per minute. For more quota, please contact us: https://tidb.support.pingcap.com/",
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

</div>

<div label="Chat2Data 端点">

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 429,
      "message": "The AI request exceeded the limit of 100 times per day. For more quota, please contact us: https://tidb.support.pingcap.com/",
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

</div>
</SimpleTab>

### 500

此状态码表示请求遇到了内部错误。这个错误可能有多种原因。

一个可能的原因是由于无法连接到认证服务器导致认证失败。

以下是一个示例响应：

```json
{
    "type": "sql_endpoint",
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

这也可能与无法连接 TiDB Cloud 集群有关。你需要参考 `message` 进行故障排除。

```json
{
    "type": "sql_endpoint",
    "data": {
        "columns": [],
        "rows": [],
        "result": {
            "code": 500,
            "message": "internal error! {detailed error}",
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
