---
title: Maintain DM Clusters Using OpenAPI
summary: Learn about how to use OpenAPI interface to manage the cluster status and data replication.
---

# Maintain DM Clusters Using OpenAPI

DM provides the OpenAPI feature for easily querying and operating the DM cluster, which is similar to the feature of [dmctl tools](/dm/dmctl-introduction.md).

To enable OpenAPI, perform one of the following operations:

+ If your DM cluster has been deployed directly using binary, add the following configuration to the DM-master configuration file.

    ```toml
    openapi = true
    ```

+ If your DM cluster has been deployed using TiUP, add the following configuration to the topology file:

    ```yaml
    server_configs:
      master:
        openapi: true
    ```

> **Note:**
>
> - DM provides the [specification document](https://github.com/pingcap/tiflow/blob/master/dm/openapi/spec/dm.yaml) that meets the OpenAPI 3.0.0 standard. This document contains all the request parameters and returned values. You can copy the document yaml and preview it in [Swagger Editor](https://editor.swagger.io/).
>
> - After you deploy the DM-master nodes, you can access `http://{master-addr}/api/v1/docs` to preview the documentation online.
>
> - Some features supported in the configuration file are not supported in OpenAPI. Their capabilities are not fully aligned. In a production environment, it is recommended to use the [configuration file](/dm/dm-config-overview.md).

You can use the APIs to perform the following maintenance operations on the DM cluster:

## APIs for managing clusters

* [Get the information of a DM-master node](#get-the-information-of-a-dm-master-node)
* [Stop a DM-master node](#stop-a-dm-master-node)
* [Get the information of a DM-worker node](#get-the-information-of-a-dm-worker-node)
* [Stop a DM-worker node](#stop-a-dm-worker-node)

## APIs for managing data sources

* [Create a data source](#create-a-data-source)
* [Get a data source](#get-a-data-source)
* [Delete the data source](#delete-the-data-source)
* [Update a data source](#update-a-data-source)
* [Enable a data source](#enable-a-data-source)
* [Disable a data source](#disable-a-data-source)
* [Get the information of a data source](#get-the-information-of-a-data-source)
* [Get the data source list](#get-the-data-source-list)
* [Start the relay-log feature for data sources](#start-the-relay-log-feature-for-data-sources)
* [Stop the relay-log feature for data sources](#stop-the-relay-log-feature-for-data-sources)
* [Purge relay-log files that are no longer required](#purge-relay-log-files-that-are-no-longer-required)
* [Change the bindings between the data source and DM-workers](#change-the-bindings-between-the-data-source-and-dm-workers)
* [Get the list of schema names of a data source](#get-the-list-of-schema-names-of-a-data-source)
* [Get the list of table names of a specified schema in a data source](#get-the-list-of-table-names-of-a-specified-schema-in-a-data-source)

## APIs for managing replication tasks

* [Create a replication task](#create-a-replication-task)
* [Get a replication task](#get-a-replication-task)
* [Delete a replication task](#delete-a-replication-task)
* [Update a replication task](#update-a-replication-task)
* [Start a replication task](#start-a-replication-task)
* [Stop a replication task](#stop-a-replication-task)
* [Get the information of a replication task](#get-the-information-of-a-replication-task)
* [Get the replication task list](#get-the-replication-task-list)
* [Get the migration rules of a replication task](#get-the-migration-rules-of-a-replication-task)
* [Get the list of schema names of the data source that is associated with a replication task](#get-the-list-of-schema-names-of-the-data-source-that-is-associated-with-a-replication-task)
* [Get the list of table names of a specified schema in the data source that is associated with a replication task](#get-the-list-of-table-names-of-a-specified-schema-in-the-data-source-that-is-associated-with-a-replication-task)
* [Get the CREATE statement for schemas of the data source that is associated with a replication task](#get-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
* [Update the CREATE statement for schemas of the data source that is associated with a replication task](#update-the-create-statement-for-schemas-of-the-data-source-that-is-associated-with-a-replication-task)
* [Delete a schema of the data source that is associated with a replication task](#delete-a-schema-of-the-data-source-that-is-associated-with-a-replication-task)

The following sections describe the specific usage of the APIs.

## API error message template

After sending an API request, if an error occurs, the returned error message is in the following format:

```json
{
    "error_msg": "",
    "error_code": ""
}
```

From the above JSON output, `error_msg` describes the error message and `error_code` is the corresponding error code.

## Get the information of a DM-master node

This API is a synchronous interface. If the request is successful, the information of the corresponding node is returned.

### Request URI

`GET /api/v1/cluster/masters`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/cluster/masters' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "name": "master1",
      "alive": true,
      "leader": true,
      "addr": "127.0.0.1:8261"
    }
  ]
}
```

## Stop a DM-master node

This API is a synchronous interface. If the request is successful, the status code of the returned body is 204.

### Request URI

`DELETE /api/v1/cluster/masters/{master-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/masters/master1' \
  -H 'accept: */*'
```

## Get the information of a DM-worker node

This API is a synchronous interface. If the request is successful, the information of the corresponding node is returned.

### Request URI

`GET /api/v1/cluster/workers`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/cluster/workers' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "name": "worker1",
      "addr": "127.0.0.1:8261",
      "bound_stage": "bound",
      "bound_source_name": "mysql-01"
    }
  ]
}
```

## Stop a DM-worker node

This API is a synchronous interface. If the request is successful, the status code of the returned body is 204.

### Request URI

 `DELETE /api/v1/cluster/workers/{worker-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/workers/worker1' \
  -H 'accept: */*'
```

## Create a data source

This API is a synchronous interface. If the request is successful, the information of the corresponding data source is returned.

### Request URI

`POST /api/v1/sources`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable": true,
  "enable_gtid": false,
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  }
}'
```

```json
{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable": true,
  "enable_gtid": false,
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  },
  "status_list": [
    {
      "source_name": "mysql-replica-01",
      "worker_name": "worker-1",
      "relay_status": {
        "master_binlog": "(mysql-bin.000001, 1979)",
        "master_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_dir": "./sub_dir",
        "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_catch_up_master": true,
        "stage": "Running"
      },
      "error_msg": "string"
    }
  ]
}
```

## Get a data source

This API is a synchronous interface. If the request is successful, the information of the corresponding data source is returned.

### Request URI

`GET /api/v1/sources/{source-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1?with_status=true' \
  -H 'accept: application/json'
```

```json
{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable_gtid": false,
  "enable": false,
  "flavor": "mysql",
  "task_name_list": [
    "task1"
  ],
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  },
  "status_list": [
    {
      "source_name": "mysql-replica-01",
      "worker_name": "worker-1",
      "relay_status": {
        "master_binlog": "(mysql-bin.000001, 1979)",
        "master_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_dir": "./sub_dir",
        "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_catch_up_master": true,
        "stage": "Running"
      },
      "error_msg": "string"
    }
  ],
  "relay_config": {
    "enable_relay": true,
    "relay_binlog_name": "mysql-bin.000002",
    "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
    "relay_dir": "./relay_log"
  }
}
```

## Delete the data source

This API is a synchronous interface. If the request is successful, the status code of the returned body is 204.

### Request URI

`DELETE /api/v1/sources/{source-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01?force=true' \
  -H 'accept: application/json'
```

## Update a data source

This API is a synchronous interface. If the request is successful, the information of the corresponding data source is returned.

> **Note:**
>
> When you use this API to update the data source configuration, make sure that there are no running tasks under the current data source.

### Request URI

`PUT /api/v1/sources/{source-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "source": {
    "source_name": "mysql-01",
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "enable_gtid": false,
    "enable": false,
    "flavor": "mysql",
    "task_name_list": [
      "task1"
    ],
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    },
    "purge": {
      "interval": 3600,
      "expires": 0,
      "remain_space": 15
    },
    "relay_config": {
      "enable_relay": true,
      "relay_binlog_name": "mysql-bin.000002",
      "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
      "relay_dir": "./relay_log"
    }
  }
}'
```

```json
{
  "source_name": "mysql-01",
  "host": "127.0.0.1",
  "port": 3306,
  "user": "root",
  "password": "123456",
  "enable": true,
  "enable_gtid": false,
  "security": {
    "ssl_ca_content": "",
    "ssl_cert_content": "",
    "ssl_key_content": "",
    "cert_allowed_cn": [
      "string"
    ]
  },
  "purge": {
    "interval": 3600,
    "expires": 0,
    "remain_space": 15
  }
}
```

## Enable a data source

This is a synchronous interface that enables a data source on a successful request and starts all subtasks of the task that rely on this data source in batch.

### Request URI

`POST /api/v1/sources/{source-name}/enable`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## Disable a data source

This is a synchronous interface that deactivates this data source on a successful request and stops all subtasks of the task that rely on it in batch.

### Request URI

`POST /api/v1/sources/{source-name}/disable`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## Get the data source list

This API is a synchronous interface. If the request is successful, the data source list is returned.

### Request URI

`GET /api/v1/sources`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources?with_status=true' \
  -H 'accept: application/json'
```

```json
{
  "data": [
    {
      "enable_gtid": false,
      "host": "127.0.0.1",
      "password": "******",
      "port": 3306,
      "purge": {
        "expires": 0,
        "interval": 3600,
        "remain_space": 15
      },
      "security": null,
      "source_name": "mysql-01",
      "user": "root"
    },
    {
      "enable_gtid": false,
      "host": "127.0.0.1",
      "password": "******",
      "port": 3307,
      "purge": {
        "expires": 0,
        "interval": 3600,
        "remain_space": 15
      },
      "security": null,
      "source_name": "mysql-02",
      "user": "root"
    }
  ],
  "total": 2
}
```

## Get the information of a data source

This API is a synchronous interface. If the request is successful, the information of the corresponding node is returned.

### Request URI

`GET /api/v1/sources/{source-name}/status`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-replica-01/status' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "source_name": "mysql-replica-01",
      "worker_name": "worker-1",
      "relay_status": {
        "master_binlog": "(mysql-bin.000001, 1979)",
        "master_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_dir": "./sub_dir",
        "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
        "relay_catch_up_master": true,
        "stage": "Running"
      },
      "error_msg": "string"
    }
  ]
}
```

## Start the relay-log feature for data sources

This API is an asynchronous interface. If the request is successful, the status code of the returned body is 200. To learn about its latest status, You can [get the information of a data source](#get-the-information-of-a-data-source).

### Request URI

`POST /api/v1/sources/{source-name}/relay/enable`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name_list": [
    "worker-1"
  ],
  "relay_binlog_name": "mysql-bin.000002",
  "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
  "relay_dir": "./relay_log"
}'
```

## Stop the relay-log feature for data sources

This API is an asynchronous interface. If the request is successful, the status code of the returned body is 200. To learn about its latest status, You can [get the information of a data source](#get-the-information-of-a-data-source).

### Request URI

`POST /api/v1/sources/{source-name}/relay/disable`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name_list": [
    "worker-1"
  ]
}'
```

## Purge relay log files that are no longer required

This API is an asynchronous interface. If the request is successful, the status code of the returned body is 200. To learn about its latest status, You can [get the information of a data source](#get-the-information-of-a-data-source).

### Request URI

`POST /api/v1/sources/{source-name}/relay/purge`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/purge' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "relay_binlog_name": "mysql-bin.000002",
  "relay_dir": "string"
}'
```

## Change the bindings between the data source and DM-workers

This API is an asynchronous interface. If the request is successful, the status code of the returned body is 200. To learn about its latest status, You can [get the information of a DM-worker node](#get-the-information-of-a-dm-worker-node).

### Request URI

`POST /api/v1/sources/{source-name}/transfer`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/transfer' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "worker_name": "worker-1"
}'
```

## Get the list of schema names of a data source

This API is a synchronous interface. If the request is successful, the corresponding list is returned.

### Request URI

`GET /api/v1/sources/{source-name}/schemas`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1/schemas' \
  -H 'accept: application/json'
```

```json
[
  "db1"
]
```

## Get the list of table names of a specified schema in a data source

This API is a synchronous interface. If the request is successful, the corresponding list is returned.

### Request URI

`GET /api/v1/sources/{source-name}/schemas/{schema-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1/schemas/db1' \
  -H 'accept: application/json'
```

```json
[
  "table1"
]
```

## Create a replication task

This API is a synchronous interface. If the request is successful, the status code of the returned body is 200. A successful request will return the information of the corresponding replication task.

### Request URI

`POST /api/v1/tasks`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "task": {
    "name": "task-1",
    "task_mode": "all",
    "shard_mode": "pessimistic",
    "meta_schema": "dm-meta",
    "enhance_online_schema_change": true,
    "on_duplicate": "overwrite",
    "target_config": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "password": "123456",
      "security": {
        "ssl_ca_content": "",
        "ssl_cert_content": "",
        "ssl_key_content": "",
        "cert_allowed_cn": [
          "string"
        ]
      }
    },
    "binlog_filter_rule": {
      "rule-1": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-2": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-3": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      }
    },
    "table_migrate_rule": [
      {
        "source": {
          "source_name": "source-name",
          "schema": "db-*",
          "table": "tb-*"
        },
        "target": {
          "schema": "db1",
          "table": "tb1"
        },
        "binlog_filter_rule": [
          "rule-1",
          "rule-2",
          "rule-3",
        ]
      }
    ],
    "source_config": {
      "full_migrate_conf": {
        "export_threads": 4,
        "import_threads": 16,
        "data_dir": "./exported_data",
        "consistency": "auto"
      },
      "incr_migrate_conf": {
        "repl_threads": 16,
        "repl_batch": 100
      },
      "source_conf": [
        {
          "source_name": "mysql-replica-01",
          "binlog_name": "binlog.000001",
          "binlog_pos": 4,
          "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
        }
      ]
    }
  }
}'
```

```json
{
  "name": "task-1",
  "task_mode": "all",
  "shard_mode": "pessimistic",
  "meta_schema": "dm-meta",
  "enhance_online_schema_change": true,
  "on_duplicate": "overwrite",
  "target_config": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    }
  },
  "binlog_filter_rule": {
    "rule-1": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-2": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-3": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    }
  },
  "table_migrate_rule": [
    {
      "source": {
        "source_name": "source-name",
        "schema": "db-*",
        "table": "tb-*"
      },
      "target": {
        "schema": "db1",
        "table": "tb1"
      },
      "binlog_filter_rule": [
        "rule-1",
        "rule-2",
        "rule-3",
      ]
    }
  ],
  "source_config": {
    "full_migrate_conf": {
      "export_threads": 4,
      "import_threads": 16,
      "data_dir": "./exported_data",
      "consistency": "auto"
    },
    "incr_migrate_conf": {
      "repl_threads": 16,
      "repl_batch": 100
    },
    "source_conf": [
      {
        "source_name": "mysql-replica-01",
        "binlog_name": "binlog.000001",
        "binlog_pos": 4,
        "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
      }
    ]
  }
}
```

## Get a replication task

This API is a synchronous interface. If the request is successful, the information of the corresponding replication task is returned.

### Request URI

`GET /api/v1/tasks/{task-name}?with_status=true`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1?with_status=true' \
  -H 'accept: application/json'
```

```json
{
  "name": "task-1",
  "task_mode": "all",
  "shard_mode": "pessimistic",
  "meta_schema": "dm-meta",
  "enhance_online_schema_change": true,
  "on_duplicate": "overwrite",
  "target_config": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    }
  },
  "binlog_filter_rule": {
    "rule-1": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-2": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-3": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    }
  },
  "table_migrate_rule": [
    {
      "source": {
        "source_name": "source-name",
        "schema": "db-*",
        "table": "tb-*"
      },
      "target": {
        "schema": "db1",
        "table": "tb1"
      },
      "binlog_filter_rule": [
        "rule-1",
        "rule-2",
        "rule-3",
      ]
    }
  ],
  "source_config": {
    "full_migrate_conf": {
      "export_threads": 4,
      "import_threads": 16,
      "data_dir": "./exported_data",
      "consistency": "auto"
    },
    "incr_migrate_conf": {
      "repl_threads": 16,
      "repl_batch": 100
    },
    "source_conf": [
      {
        "source_name": "mysql-replica-01",
        "binlog_name": "binlog.000001",
        "binlog_pos": 4,
        "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
      }
    ]
  }
}
```

## Delete a replication task

This interface is a synchronous interface and the Status Code of the returned body is 204 upon successful request.

### Request URI

`DELETE /api/v1/tasks/{task-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json'
```

## Update a replication task

This interface is a synchronous interface and a successful request returns the information of the task.

> **Note:**
>
> When you use this API to update the task configuration, make sure that the task is stopped and has run into incremental sync and that only some of the fields can be updated.

### Request URI

`PUT /api/v1/tasks/{task-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "task": {
    "name": "task-1",
    "task_mode": "all",
    "shard_mode": "pessimistic",
    "meta_schema": "dm-meta",
    "enhance_online_schema_change": true,
    "on_duplicate": "overwrite",
    "target_config": {
      "host": "127.0.0.1",
      "port": 3306,
      "user": "root",
      "password": "123456",
      "security": {
        "ssl_ca_content": "",
        "ssl_cert_content": "",
        "ssl_key_content": "",
        "cert_allowed_cn": [
          "string"
        ]
      }
    },
    "binlog_filter_rule": {
      "rule-1": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-2": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      },
      "rule-3": {
        "ignore_event": [
          "all dml"
        ],
        "ignore_sql": [
          "^Drop"
        ]
      }
    },
    "table_migrate_rule": [
      {
        "source": {
          "source_name": "source-name",
          "schema": "db-*",
          "table": "tb-*"
        },
        "target": {
          "schema": "db1",
          "table": "tb1"
        },
        "binlog_filter_rule": [
          "rule-1",
          "rule-2",
          "rule-3",
        ]
      }
    ],
    "source_config": {
      "full_migrate_conf": {
        "export_threads": 4,
        "import_threads": 16,
        "data_dir": "./exported_data",
        "consistency": "auto"
      },
      "incr_migrate_conf": {
        "repl_threads": 16,
        "repl_batch": 100
      },
      "source_conf": [
        {
          "source_name": "mysql-replica-01",
          "binlog_name": "binlog.000001",
          "binlog_pos": 4,
          "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
        }
      ]
    }
  }
}'
```

```json
{
  "name": "task-1",
  "task_mode": "all",
  "shard_mode": "pessimistic",
  "meta_schema": "dm-meta",
  "enhance_online_schema_change": true,
  "on_duplicate": "overwrite",
  "target_config": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "security": {
      "ssl_ca_content": "",
      "ssl_cert_content": "",
      "ssl_key_content": "",
      "cert_allowed_cn": [
        "string"
      ]
    }
  },
  "binlog_filter_rule": {
    "rule-1": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-2": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    },
    "rule-3": {
      "ignore_event": [
        "all dml"
      ],
      "ignore_sql": [
        "^Drop"
      ]
    }
  },
  "table_migrate_rule": [
    {
      "source": {
        "source_name": "source-name",
        "schema": "db-*",
        "table": "tb-*"
      },
      "target": {
        "schema": "db1",
        "table": "tb1"
      },
      "binlog_filter_rule": [
        "rule-1",
        "rule-2",
        "rule-3",
      ]
    }
  ],
  "source_config": {
    "full_migrate_conf": {
      "export_threads": 4,
      "import_threads": 16,
      "data_dir": "./exported_data",
      "consistency": "auto"
    },
    "incr_migrate_conf": {
      "repl_threads": 16,
      "repl_batch": 100
    },
    "source_conf": [
      {
        "source_name": "mysql-replica-01",
        "binlog_name": "binlog.000001",
        "binlog_pos": 4,
        "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
      }
    ]
  }
}
```

## Start a replication task

This API is an asynchronous interface. If the request is successful, the status code of the returned body is 204. To learn the latest status of a task, You can [get the information of a replication task](#get-the-information-of-a-replication-task).

### Request URI

`POST /api/v1/tasks/{task-name}/start`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/start' \
  -H 'accept: */*'
```

## Stop a replication task

This API is an asynchronous interface. If the request is successful, the status code of the returned body is 200. To learn the latest status of a task, You can [get the information of a replication task](#get-the-information-of-a-replication-task).

### Request URI

`POST /api/v1/tasks/{task-name}/stop`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/stop' \
  -H 'accept: */*'
```

## Get the information of a replication task

This API is a synchronous interface. If the request is successful, the information of the corresponding node is returned.

### Request URI

`GET /api/v1/tasks/task-1/status`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/status?stage=running' \
  -H 'accept: application/json'
```

```json
{
  "total": 1,
  "data": [
    {
      "name": "string",
      "source_name": "string",
      "worker_name": "string",
      "stage": "runing",
      "unit": "sync",
      "unresolved_ddl_lock_id": "string",
      "load_status": {
        "finished_bytes": 0,
        "total_bytes": 0,
        "progress": "string",
        "meta_binlog": "string",
        "meta_binlog_gtid": "string"
      },
      "sync_status": {
        "total_events": 0,
        "total_tps": 0,
        "recent_tps": 0,
        "master_binlog": "string",
        "master_binlog_gtid": "string",
        "syncer_binlog": "string",
        "syncer_binlog_gtid": "string",
        "blocking_ddls": [
          "string"
        ],
        "unresolved_groups": [
          {
            "target": "string",
            "ddl_list": [
              "string"
            ],
            "first_location": "string",
            "synced": [
              "string"
            ],
            "unsynced": [
              "string"
            ]
          }
        ],
        "synced": true,
        "binlog_type": "string",
        "seconds_behind_master": 0
      }
    }
  ]
}
```

## Get the replication task list

This API is a synchronous interface and a successful request returns a list of the corresponding tasks.

### Request URI

`GET /api/v1/tasks`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json'
```

```json
{
  "total": 2,
  "data": [
    {
      "name": "task-1",
      "task_mode": "all",
      "shard_mode": "pessimistic",
      "meta_schema": "dm-meta",
      "enhance_online_schema_change": true,
      "on_duplicate": "overwrite",
      "target_config": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123456",
        "security": {
          "ssl_ca_content": "",
          "ssl_cert_content": "",
          "ssl_key_content": "",
          "cert_allowed_cn": [
            "string"
          ]
        }
      },
      "binlog_filter_rule": {
        "rule-1": {
          "ignore_event": [
            "all dml"
          ],
          "ignore_sql": [
            "^Drop"
          ]
        },
        "rule-2": {
          "ignore_event": [
            "all dml"
          ],
          "ignore_sql": [
            "^Drop"
          ]
        },
        "rule-3": {
          "ignore_event": [
            "all dml"
          ],
          "ignore_sql": [
            "^Drop"
          ]
        }
      },
      "table_migrate_rule": [
        {
          "source": {
            "source_name": "source-name",
            "schema": "db-*",
            "table": "tb-*"
          },
          "target": {
            "schema": "db1",
            "table": "tb1"
          },
          "binlog_filter_rule": [
            "rule-1",
            "rule-2",
            "rule-3",
          ]
        }
      ],
      "source_config": {
        "full_migrate_conf": {
          "export_threads": 4,
          "import_threads": 16,
          "data_dir": "./exported_data",
          "consistency": "auto"
        },
        "incr_migrate_conf": {
          "repl_threads": 16,
          "repl_batch": 100
        },
        "source_conf": [
          {
            "source_name": "mysql-replica-01",
            "binlog_name": "binlog.000001",
            "binlog_pos": 4,
            "binlog_gtid": "03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170"
          }
        ]
      }
    }
  ]
}
```

## Get the migration rules of a replication task

This API is a synchronous interface and a successful request returns a list of the migration rules of this task.

### Request URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/migrate_targets`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/migrate_targets' \
  -H 'accept: application/json'
```

```json
{
  "total": 0,
  "data": [
    {
      "source_schema": "db1",
      "source_table": "tb1",
      "target_schema": "db1",
      "target_table": "tb1"
    }
  ]
}
```

## Get the list of schema names of the data source that is associated with a replication task

This API is a synchronous interface. If the request is successful, the corresponding list is returned.

### Request URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas' \
  -H 'accept: application/json'
```

```json
[
  "db1"
]
```

## Get the list of table names of a specified schema in the data source that is associated with a replication task

This API is a synchronous interface. If the request is successful, the corresponding list is returned.

### Request URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1' \
  -H 'accept: application/json'
```

```json
[
  "table1"
]
```

## Get the CREATE statement for schemas of the data source that is associated with a replication task

This API is a synchronous interface. If the request is successful, the corresponding CREATE statement is returned.

### Request URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: application/json'
```

```json
{
  "schema_name": "db1",
  "table_name": "table1",
  "schema_create_sql": "CREATE TABLE `t1` (`id` int(11) NOT NULL AUTO_INCREMENT,PRIMARY KEY (`id`) /*T![clustered_index] CLUSTERED */) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin"
}
```

## Update the CREATE statement for schemas of the data source that is associated with a replication task

This API is a synchronous interface. If the request is successful, the status code of the returned body is 200.

### Request URI

`POST /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/task-1/schemas/db1/table1' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "sql_content": "CREATE TABLE `t1` ( `c1` int(11) DEFAULT NULL, `c2` int(11) DEFAULT NULL, `c3` int(11) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;",
  "flush": true,
  "sync": true
}'
```

## Delete a schema of the data source that is associated with a replication task

This API is a synchronous interface. If the request is successful, the status code of the returned body is 200.

### Request URI

`DELETE /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### Example

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: */*'
```
