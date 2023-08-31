---
title: Response and HTTP Status Codes of Data Service
summary: This document describes the response and HTTP status codes of Data Service in TiDB Cloud.
---

# Response and HTTP Status Codes of Data Service

When you call an API endpoint defined in [Data Service](/tidb-cloud/data-service-overview.md), Data Service returns an HTTP response. Understanding the structure of this response and the meaning of status codes is essential for interpreting data returned by a Data Service endpoint.

This document describes the response and status codes of Data Service in TiDB Cloud.

## Response

Data Service returns an HTTP response with a JSON body.

> **Note:**
>
> When you call an endpoint with multiple SQL statements, Data Service executes the statements one by one, but it only returns the execution result of the last statement in the HTTP response.

The response body contains the following fields:

- `type`: _string_. The type of this endpoint. The value might be `"sql_endpoint"` or `"chat2data_endpoint"`. Different endpoints return different types of responses.
- `data`: _object_. The execution results, which include three parts:

    - `columns`: _array_. Schema information for the returned fields.
    - `rows`: _array_. The returned results in `key:value` format.

        When **Batch Operation** is enabled for an endpoint and the last SQL statement of the endpoint is an `INSERT`, `UPDATE`, or `DELETE` operation, note the following:

        - The returned results of the endpoint will also include the `"message"` and `"success"` fields for each row to indicate their response and status.
        - If the primary key column of the target table is configured as `auto_increment`, the returned results of the endpoint will also include the `"auto_increment_id"` field for each row. The value of this field is the auto increment ID for an `INSERT` operation and is `null` for other operations such as `UPDATE` and `DELETE`.

    - `result`: _object_. The execution-related information of the SQL statement, including success/failure status, execution time, number of rows returned, and user configuration.

An example response is as follows:

<SimpleTab>
<div label="SQL Endpoint">

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

<div label="Chat2Data Endpoint">

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

## Status code

### 200

If the HTTP status code is `200` and the `data.result.code` field also shows `200`, this indicated that the SQL statement is executed successfully. Otherwise, TiDB Cloud fails to execute the SQL statement defined in your endpoint. You can check the `code` and `message` fields for detailed information.

An example response is as follows:

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

This status code indicates that the parameter check failed.

An example response is as follows:

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

This status code indicates that the authentication failed due to lack of permission.

An example response is as follows:

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

This status code indicates that the authentication failed due to the inability to find the specified endpoint.

An example response is as follows:

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

This status code indicates that the request used a method that is not allowed. Note that Data Service only supports `GET` and `POST`.

An example response is as follows:

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

This status code indicates that the request exceeds the timeout duration of the endpoint. To modify the timeout of an endpoint, refer to [Configure properties](/tidb-cloud/data-service-manage-endpoint.md#configure-properties).

An example response is as follows:

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

This status code indicates that the request exceeds the rate limit of the API key. For more quota, you can [submit a request](https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519) to our support team.

An example response is as follows:

<SimpleTab>
<div label="SQL Endpoint">

```json
{
  "type": "",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 49900007,
      "message": "The request exceeded the limit of 100 times per apikey per minute. For more quota, please contact us: https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519",
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

<div label="Chat2Data Endpoint">

```json
{
  "type": "chat2data_endpoint",
  "data": {
    "columns": [],
    "rows": [],
    "result": {
      "code": 429,
      "message": "The AI request exceeded the limit of 100 times per day. For more quota, please contact us: https://support.pingcap.com/hc/en-us/requests/new?ticket_form_id=7800003722519",
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

This status code indicates that the request met an internal error. There might be various causes for this error.

One possible cause is that the authentication failed due to the inability to connect to the authentication server.

An example response is as follows:

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

This might also be related to the inability to connect the TiDB Cloud cluster. You need to refer to the `message` for troubleshooting.

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
