---
title: Data App 配置文件
summary: 本文档描述了 TiDB Cloud 中 Data App 的配置文件。
---

# Data App 配置文件

本文档描述了 TiDB Cloud 中 [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) 的配置文件。

如果你已经[将你的 Data App 连接到 GitHub](/tidb-cloud/data-service-manage-github-connection.md)，你可以在 GitHub 上的指定目录中找到你的 Data App 的配置文件，如下所示：

```
├── <你的 Data App 目录>
│   ├── data_sources
│   │   └── cluster.json
│   ├── dataapp_config.json
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-path1>.sql
│   │       ├── <method>-<endpoint-path2>.sql
│   │       └── <method>-<endpoint-path3>.sql
```

## 数据源配置

Data App 的数据源来自其链接的 TiDB 集群。你可以在 `data_sources/cluster.json` 中找到数据源配置。

```
├── <你的 Data App 目录>
│   ├── data_sources
│   │   └── cluster.json
```

对于每个 Data App，你可以链接一个或多个 TiDB 集群。

以下是 `cluster.json` 的示例配置。在此示例中，此 Data App 有两个链接的集群。

```json
[
  {
    "cluster_id": <集群 ID1>
  },
  {
    "cluster_id": <集群 ID2>
  }
]
```

字段说明如下：

| 字段   | 类型    | 说明  |
|---------|---------|--------------|
| `cluster_id` | Integer | 你的 TiDB 集群的 ID。你可以从集群的 URL 获取它。例如，如果你的集群 URL 是 `https://tidbcloud.com/clusters/1234567891234567890/overview`，你的集群 ID 是 `1234567891234567890`。 |

## Data App 配置

Data App 的属性包含 App ID、名称和类型。你可以在 `dataapp_config.json` 文件中找到这些属性。

```
├── <你的 Data App 目录>
│   ├── dataapp_config.json
```

以下是 `dataapp_config.json` 的示例配置。

```json
{
  "app_id": "<Data App ID>",
  "app_name": "<Data App 名称>",
  "app_type": "dataapi",
  "app_version": "<Data App 版本>",
  "description": "<Data App 描述>"
}
```

每个字段的说明如下：

| 字段      | 类型   | 说明        |
|------------|--------|--------------------|
| `app_id`   | String | Data App ID。除非你的 `dataapp_config.json` 文件是从另一个 Data App 复制的，并且你想将其更新为当前 Data App 的 ID，否则不要更改此字段。否则，由此修改触发的部署将失败。 |
| `app_name` | String | Data App 名称。 |
| `app_type` | String | Data App 类型，只能是 `"dataapi"`。 |
| `app_version` | String | Data App 版本，格式为 `"<major>.<minor>.<patch>"`。例如，`"1.0.0"`。 |
| `description` | String | Data App 描述。 |

## HTTP 端点配置

在你的 Data App 目录中，你可以在 `http_endpoints/config.json` 中找到端点配置，在 `http_endpoints/sql/<method>-<endpoint-name>.sql` 中找到 SQL 文件。

```
├── <你的 Data App 目录>
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-path1>.sql
│   │       ├── <method>-<endpoint-path2>.sql
│   │       └── <method>-<endpoint-path3>.sql
```

### 端点配置

对于每个 Data App，可以有一个或多个端点。你可以在 `http_endpoints/config.json` 中找到 Data App 的所有端点的配置。

以下是 `config.json` 的示例配置。在此示例中，此 Data App 有两个端点。

```json
[
  {
    "name": "<端点名称1>",
    "description": "<端点描述1>",
    "method": "<HTTP 方法1>",
    "endpoint": "<端点路径1>",
    "data_source": {
      "cluster_id": <集群 ID1>
    },
    "params": [],
    "settings": {
      "timeout": <端点超时时间>,
      "row_limit": <最大行数>,
      "enable_pagination": <0 | 1>,
      "cache_enabled": <0 | 1>,
      "cache_ttl": <生存时间周期>
    },
    "tag": "Default",
    "batch_operation": <0 | 1>,
    "sql_file": "<SQL 文件目录1>",
    "type": "sql_endpoint",
    "return_type": "json"
  },
  {
    "name": "<端点名称2>",
    "description": "<端点描述2>",
    "method": "<HTTP 方法2>",
    "endpoint": "<端点路径2>",
    "data_source": {
      "cluster_id": <集群 ID2>
    },
    "params": [
      {
        "name": "<参数名称>",
        "type": "<参数类型>",
        "required": <0 | 1>,
        "default": "<参数默认值>",
        "description": "<参数描述>",
        "is_path_parameter": <true | false>
      }
    ],
    "settings": {
      "timeout": <端点超时时间>,
      "row_limit": <最大行数>,
      "enable_pagination": <0 | 1>,
      "cache_enabled": <0 | 1>,
      "cache_ttl": <生存时间周期>
    },
    "tag": "Default",
    "batch_operation": <0 | 1>,
    "sql_file": "<SQL 文件目录2>",
    "type": "sql_endpoint",
    "return_type": "json"
  }
]
```

每个字段的说明如下：

| 字段         | 类型   | 说明 |
|---------------|--------|-------------|
| `name`        | String | 端点名称。            |
| `description` | String | （可选）端点描述。          |
| `method`      | String | 端点的 HTTP 方法。你可以使用 `GET` 检索数据，使用 `POST` 创建或插入数据，使用 `PUT` 更新或修改数据，使用 `DELETE` 删除数据。 |
| `endpoint`    | String | Data App 中端点的唯一路径。路径中只允许使用字母、数字、下划线（`_`）和斜杠（`/`），必须以斜杠（`/`）开头，以字母、数字或下划线（`_`）结尾。例如，`/my_endpoint/get_id`。路径长度必须小于 64 个字符。|
| `cluster_id`  | String | 端点使用的 TiDB 集群的 ID。你可以从 TiDB 集群的 URL 获取它。例如，如果你的集群 URL 是 `https://tidbcloud.com/clusters/1234567891234567890/overview`，集群 ID 是 `1234567891234567890`。 |
| `params` | Array | 端点使用的参数。通过定义参数，你可以通过端点动态替换查询中的参数值。在 `params` 中，你可以定义一个或多个参数。对于每个参数，你需要定义其 `name`、`type`、`required` 和 `default` 字段。如果你的端点不需要任何参数，你可以将 `params` 留空，如 `"params": []`。 |
| `params.name` | String | 参数的名称。名称只能包含字母、数字和下划线（`_`），且必须以字母或下划线（`_`）开头。**不要**使用 `page` 和 `page_size` 作为参数名称，这些是为请求结果分页保留的。 |
| `params.type` | String | 参数的数据类型。支持的值有 `string`、`number`、`integer`、`boolean` 和 `array`。使用 `string` 类型参数时，不需要添加引号（`'` 或 `"`）。例如，`foo` 对于 `string` 类型是有效的，会被处理为 `"foo"`，而 `"foo"` 会被处理为 `"\"foo\""` 。 |
| `params.required` | Integer | 指定请求中是否必须包含该参数。支持的值为 `0`（不必须）和 `1`（必须）。默认值为 `0`。  |
| `params.enum` | String | （可选）指定参数的值选项。此字段仅在 `params.type` 设置为 `string`、`number` 或 `integer` 时有效。要指定多个值，可以用逗号（`,`）分隔。 |
| `params.default` | String | 参数的默认值。确保值与你指定的参数类型匹配。否则，端点将返回错误。`ARRAY` 类型参数的默认值是一个字符串，你可以使用逗号（`,`）分隔多个值。 |
| `params.description` | String | 参数的描述。 |
| `params.is_path_parameter` | Boolean | 指定参数是否为路径参数。如果设置为 `true`，请确保 `endpoint` 字段包含相应的参数占位符；否则，将导致部署失败。相反，如果 `endpoint` 字段包含相应的参数占位符但此字段设置为 `false`，也会导致部署失败。 |
| `settings.timeout`     | Integer | 端点的超时时间（以毫秒为单位），默认为 `30000`。你可以将其设置为 `1` 到 `60000` 之间的整数。  |
| `settings.row_limit`   | Integer  | 端点可以操作或返回的最大行数，默认为 `1000`。当 `batch_operation` 设置为 `0` 时，你可以将其设置为 `1` 到 `2000` 之间的整数。当 `batch_operation` 设置为 `1` 时，你可以将其设置为 `1` 到 `100` 之间的整数。  |
| `settings.enable_pagination`   | Integer  | 控制是否为请求返回的结果启用分页。支持的值为 `0`（禁用）和 `1`（启用）。默认值为 `0`。 |
| `settings.cache_enabled`   | Integer  | 控制是否在指定的生存时间（TTL）期间内缓存你的 `GET` 请求返回的响应。支持的值为 `0`（禁用）和 `1`（启用）。默认值为 `0`。 |
| `settings.cache_ttl`   | Integer  | 当 `settings.cache_enabled` 设置为 `1` 时，缓存响应的生存时间（TTL）期限（以秒为单位）。你可以将其设置为 30 到 600 之间的整数。在 TTL 期间内，如果你再次发出相同的 `GET` 请求，Data Service 将直接返回缓存的响应，而不是再次从目标数据库获取数据，这样可以提高你的查询性能。 |
| `tag`    | String | 端点的标签。默认值为 `"Default"`。 |
| `batch_operation`    | Integer | 控制是否启用端点以批处理模式运行。支持的值为 `0`（禁用）和 `1`（启用）。当设置为 `1` 时，你可以在单个请求中操作多行。要启用此选项，请确保请求方法为 `POST` 或 `PUT`。 |
| `sql_file`    | String | 端点的 SQL 文件目录。例如，`"sql/GET-v1.sql"`。 |
| `type`        | String | 端点的类型。预定义的系统端点值为 `"system-data"`，其他端点值为 `"sql_endpoint"`。 |
| `return_type` | String | 端点的响应格式，只能是 `"json"`。             |

### SQL 文件配置

端点的 SQL 文件指定了通过端点查询数据的 SQL 语句。你可以在 `http_endpoints/sql/` 目录中找到 Data App 的端点 SQL 文件。每个端点都应该有一个对应的 SQL 文件。

SQL 文件的名称格式为 `<method>-<endpoint-path>.sql`，其中 `<method>` 和 `<endpoint-path>` 必须与 [`http_endpoints/config.json`](#端点配置) 中的 `method` 和 `endpoint` 配置匹配。

在 SQL 文件中，你可以编写表连接查询、复杂查询和聚合函数等语句。以下是一个示例 SQL 文件。

```sql
/* 入门：
在输入 SQL 语句之前，输入 "USE {database};"。
输入 "--你的问题" + Enter 可以在 TiDB Cloud 控制台中尝试 AI 生成的 SQL 查询。
声明参数的格式为 "Where id = ${arg}"。
*/
USE sample_data;
SELECT
  rank,
  company_name,
FROM
  global_fortune_500_2018_2022
WHERE
  country = ${country};
```

编写 SQL 文件时，请注意以下事项：

- 在 SQL 文件的开头，你需要在 SQL 语句中指定数据库。例如，`USE database_name;`。

- 要定义端点的参数，你可以将其作为变量占位符（如 `${variable-name}`）插入到 SQL 语句中。

    在上述示例中，`${country}` 用作端点的参数。使用此参数，你可以在端点 curl 命令中指定所需的国家/地区进行查询。

    > **注意：**
    >
    > - 参数名称区分大小写。
    > - 参数不能是表名或列名。
    > - SQL 文件中的参数名称必须与 [`http_endpoints/config.json`](#端点配置) 中配置的参数名称匹配。
