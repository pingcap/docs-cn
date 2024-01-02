---
title: Data App Configuration Files
summary: This document describes the configuration files of Data App in TiDB Cloud.
---

# Data App Configuration Files

This document describes the configuration files of a [Data App](/tidb-cloud/tidb-cloud-glossary.md#data-app) in TiDB Cloud.

If you have [connected your Data App to GitHub](/tidb-cloud/data-service-manage-github-connection.md), you can find the configuration files of your Data App in your specified directory on GitHub as follows:

```
├── <Your Data App directory>
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

## Data source configuration

The data source of a Data App comes from its linked TiDB clusters. You can find the data source configuration in `data_sources/cluster.json`.

```
├── <Your Data App directory>
│   ├── data_sources
│   │   └── cluster.json
```

For each Data App, you can link to one or multiple TiDB clusters.

The following is an example configuration of `cluster.json`. In this example, there are two linked clusters for this Data App.

```json
[
  {
    "cluster_id": <Cluster ID1>
  },
  {
    "cluster_id": <Cluster ID2>
  }
]
```

The field description is as follows:

| Field   | Type    | Description  |
|---------|---------|--------------|
| `cluster_id` | Integer | The ID of your TiDB cluster. You can get it from the URL of your cluster. For example, if your cluster URL is `https://tidbcloud.com/console/clusters/1234567891234567890/overview`, your cluster ID is `1234567891234567890`. |

## Data App configuration

The properties of a Data App contain the App ID, name, and type. You can find the properties in the `dataapp_config.json` file.

```
├── <Your Data App directory>
│   ├── dataapp_config.json
```

The following is an example configuration of `dataapp_config.json`.

```json
{
  "app_id": "<Data App ID>",
  "app_name": "<Data App name>",
  "app_type": "dataapi",
  "app_version": "<Data App version>",
  "description": "<Data App description>"
}
```

The description of each field is as follows:

| Field      | Type   | Description        |
|------------|--------|--------------------|
| `app_id`   | String | The Data App ID. Do not change this field unless your `dataapp_config.json` file is copied from another Data App and you want to update it to the ID of your current Data App. Otherwise, the deployment triggered by this modification will fail. |
| `app_name` | String | The Data App name. |
| `app_type` | String | The Data App type, which can only be `"dataapi"`. |
| `app_version` | String | The Data App version, which is in the `"<major>.<minor>.<patch>"` format. For example, `"1.0.0"`. |
| `description` | String | The Data App description. |

## HTTP endpoint configuration

In your Data App directory, you can find endpoint configurations in `http_endpoints/config.json` and the SQL files in `http_endpoints/sql/<method>-<endpoint-name>.sql`.

```
├── <Your Data App directory>
│   ├── http_endpoints
│   │   ├── config.json
│   │   └── sql
│   │       ├── <method>-<endpoint-path1>.sql
│   │       ├── <method>-<endpoint-path2>.sql
│   │       └── <method>-<endpoint-path3>.sql
```

### Endpoint configuration

For each Data App, there can be one or multiple endpoints. You can find the configurations of all endpoints for a Data App in `http_endpoints/config.json`.

The following is an example configuration of `config.json`. In this example, there are two endpoints for this Data App.

```json
[
  {
    "name": "<Endpoint name1>",
    "description": "<Endpoint description1>",
    "method": "<HTTP method1>",
    "endpoint": "<Endpoint path1>",
    "data_source": {
      "cluster_id": <Cluster ID1>
    },
    "params": [],
    "settings": {
      "timeout": <Endpoint timeout>,
      "row_limit": <Maximum rows>,
      "enable_pagination": <0 | 1>,
      "cache_enabled": <0 | 1>,
      "cache_ttl": <time-to-live period>
    },
    "tag": "Default",
    "batch_operation": <0 | 1>,
    "sql_file": "<SQL file directory1>",
    "type": "sql_endpoint",
    "return_type": "json"
  },
  {
    "name": "<Endpoint name2>",
    "description": "<Endpoint description2>",
    "method": "<HTTP method2>",
    "endpoint": "<Endpoint path2>",
    "data_source": {
      "cluster_id": <Cluster ID2>
    },
    "params": [
      {
        "name": "<Parameter name>",
        "type": "<Parameter type>",
        "required": <0 | 1>,
        "default": "<Parameter default value>",
        "description": "<Parameter description>"
      }
    ],
    "settings": {
      "timeout": <Endpoint timeout>,
      "row_limit": <Maximum rows>,
      "enable_pagination": <0 | 1>,
      "cache_enabled": <0 | 1>,
      "cache_ttl": <time-to-live period>
    },
    "tag": "Default",
    "batch_operation": <0 | 1>,
    "sql_file": "<SQL file directory2>",
    "type": "sql_endpoint",
    "return_type": "json"
  }
]
```

The description of each field is as follows:

| Field         | Type   | Description |
|---------------|--------|-------------|
| `name`        | String | The endpoint name.            |
| `description` | String | (Optional) The endpoint description.          |
| `method`      | String | The HTTP method of the endpoint. You can use `GET` to retrieve data, use `POST` to create or insert data, use `PUT` to update or modify data, and use `DELETE` to delete data. |
| `endpoint`    | String | The unique path of the endpoint in the Data App. Only letters, numbers, underscores (`_`), and slashes (`/`) are allowed in the path, which must start with a slash (`/`) and end with a letter, number, or underscore (`_`). For example, `/my_endpoint/get_id`. The length of the path must be less than 64 characters.|
| `cluster_id`  | String | The ID of the TiDB cluster for your endpoint. You can get it from the URL of your TiDB cluster. For example, if your cluster URL is `https://tidbcloud.com/console/clusters/1234567891234567890/overview`, the cluster ID is `1234567891234567890`. |
| `params` | Array | The parameters used in the endpoint. By defining parameters, you can dynamically replace the parameter value in your queries through the endpoint. In `params`, you can define one or multiple parameters. For each parameter, you need to define its `name`, `type`, `required`, and `default` fields. If your endpoint does not need any parameters. You can leave `params` empty such as `"params": []`. |
| `params.name` | String | The name of the parameter. The name can only include letters, digits, and underscores (`_`) and must start with a letter or an underscore (`_`). **DO NOT** use `page` and `page_size` as parameter names, which are reserved for pagination of request results. |
| `params.type` | String | The data type of the parameter. Supported values are `string`, `number`, `integer`, `boolean`, and `array`. When using a `string` type parameter, you do not need to add quotation marks (`'` or `"`). For example, `foo` is valid for the `string` type and is processed as `"foo"`, whereas `"foo"` is processed as `"\"foo\""`. |
| `params.required` | Integer | Specifies whether the parameter is required in the request. Supported values are `0` (not required) and `1` (required). The default value is `0`.  |
| `params.enum` | String | (Optional) Specifies the value options of the parameter. This field is only valid when `params.type` is set to `string`, `number`, or `integer`. To specify multiple values, you can separate them with a comma (`,`). |
| `params.default` | String | The default value of the parameter. Make sure that the value matches the type of parameter you specified. Otherwise, the endpoint returns an error. The default value of an `ARRAY` type parameter is a string and you can use a comma (`,`) to separate multiple values. |
| `params.description` | String | The description of the parameter. |
| `settings.timeout`     | Integer | The timeout for the endpoint in milliseconds, which is `30000` by default. You can set it to an integer from `1` to `60000`.  |
| `settings.row_limit`   | Integer  | The maximum number of rows that the endpoint can operate or return, which is `1000` by default. When `batch_operation` is set to `0`, you can set it to an integer from `1` to `2000`. When `batch_operation` is set to `1`, you can set it to an integer from `1` to `100`.  |
| `settings.enable_pagination`   | Integer  | Controls whether to enable the pagination for the results returned by the request. Supported values are `0` (disabled) and `1` (enabled). The default value is `0`. |
| `settings.cache_enabled`   | Integer  | Controls whether to cache the response returned by your `GET` requests within a specified time-to-live (TTL) period. Supported values are `0` (disabled) and `1` (enabled). The default value is `0`. |
| `settings.cache_ttl`   | Integer  | The time-to-live (TTL) period in seconds for cached response when `settings.cache_enabled` is set to `1`. You can set it to an integer from 30 to 600. During the TTL period, if you make the same `GET` requests again, Data Service returns the cached response directly instead of fetching data from the target database again, which improves your query performance. |
| `tag`    | String | The tag for the endpoint. The default value is `"Default"`. |
| `batch_operation`    | Integer | Controls whether to enable the endpoint to operate in batch mode. Supported values are `0` (disabled) and `1` (enabled). When it is set to `1`, you can operate on multiple rows in a single request. To enable this option, make sure that the request method is `POST` or `PUT`. |
| `sql_file`    | String | The SQL file directory for the endpoint. For example, `"sql/GET-v1.sql"`. |
| `type`        | String | The type of the endpoint, which can only be `"sql_endpoint"`.          |
| `return_type` | String | The response format of the endpoint, which can only be `"json"`.             |

### SQL file configuration

The SQL file of an endpoint specifies the SQL statements to query data through the endpoint. You can find the endpoint SQL files of a Data App in the `http_endpoints/sql/` directory. For each endpoint, there should be a corresponding SQL file.

The name of a SQL file is in the `<method>-<endpoint-path>.sql` format, where `<method>` and `<endpoint-path>` must match the `method` and `endpoint` configuration in [`http_endpoints/config.json`](#endpoint-configuration).

In the SQL file, you can write statements such as table join queries, complex queries, and aggregate functions. The following is an example SQL file.

```sql
/* Getting Started:
Enter "USE {database};" before entering your SQL statements.
Type "--your question" + Enter to try out AI-generated SQL queries in the TiDB Cloud console.
Declare a parameter like "Where id = ${arg}".
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

When writing a SQL file, pay attention to the following:

- At the beginning of the SQL file, you need to specify the database in the SQL statements. For example, `USE database_name;`.

- To define a parameter of the endpoint, you can insert it as a variable placeholder like `${variable-name}` to the SQL statement.

    In the preceding example, `${country}` is used as a parameter of the endpoint. With this parameter, you can specify a desired country to query in your endpoint curl command.

    > **Note:**
    >
    > - The parameter name is case-sensitive.
    > - The parameter cannot be a table name or column name.
    > - The parameter name in the SQL file match the parameter name configured in [`http_endpoints/config.json`](#endpoint-configuration).
