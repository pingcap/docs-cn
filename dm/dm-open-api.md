---
title: 使用 OpenAPI 运维 TiDB Data Migration 集群
summary: 了解如何使用 OpenAPI 接口来管理 DM 集群状态和数据同步。
---

# 使用 OpenAPI 运维 TiDB Data Migration 集群

TiDB Data Migration (DM) 提供 OpenAPI 功能，你可以通过 OpenAPI 方便地对 DM 集群进行查询和运维操作。OpenAPI 的功能范围和 [dmctl 工具](/dm/dmctl-introduction.md)相当。

如需开启 OpenAPI，可通过以下方法：

+ 如果你的 DM 集群是通过二进制直接部署的，则在 DM-master 的配置文件中添加如下配置：

    ```toml
    openapi = true
    ```

+ 如果你的 DM 集群是通过 TiUP 部署的，则在拓扑文件中添加如下配置：

    ```yaml
    server_configs:
      master:
        openapi: true
    ```

> **注意：**
>
> - DM 提供符合 OpenAPI 3.0.0 标准的 [Spec 文档](https://github.com/pingcap/tiflow/blob/master/dm/openapi/spec/dm.yaml)，其中包含了所有 API 的请求参数和返回体，你可自行复制到如 [Swagger Editor](https://editor.swagger.io/) 等工具中在线预览文档。
>
> - 部署 DM-master 后，你可访问 `http://{master-addr}/api/v1/docs` 在线预览文档。
>
> - 配置文件中支持的某些功能在 OpenAPI 中是不支持的，二者的功能没有完全对齐。在生产环境中，建议使用[配置文件](/dm/dm-config-overview.md)。

你可以通过 OpenAPI 完成 DM 集群的如下运维操作：

## 集群相关 API

* [获取 DM-master 节点信息](#获取-dm-master-节点信息)
* [下线 DM-master 节点](#下线-dm-master-节点)
* [获取 DM-worker 节点信息](#获取-dm-worker-节点信息)
* [下线 DM-worker 节点](#下线-dm-worker-节点)

## 数据源相关 API

* [创建数据源](#创建数据源)
* [获取数据源](#获取数据源)
* [删除数据源](#删除数据源)
* [更新数据源](#更新数据源)
* [启用数据源](#启用数据源)
* [停用数据源](#停用数据源)
* [获取数据源状态](#获取数据源状态)
* [获取数据源列表](#获取数据源列表)
* [对数据源开启 relay-log 功能](#对数据源开启-relay-log-功能)
* [对数据源停止 relay-log 功能](#对数据源停止-relay-log-功能)
* [清除数据源不需要的 relay-log 文件](#清除数据源不需要的-relay-log-文件)
* [更改数据源和 DM-worker 的绑定关系](#更改数据源和-dm-worker-的绑定关系)
* [获取数据源的数据库名列表](#获取数据源的数据库名列表)
* [获取数据源的指定数据库的表名列表](#获取数据源的指定数据库的表名列表)

## 同步任务相关 API

* [创建同步任务](#创建同步任务)
* [获取同步任务](#获取同步任务)
* [删除同步任务](#删除同步任务)
* [更新同步任务](#更新同步任务)
* [开始同步任务](#开始同步任务)
* [停止同步任务](#停止同步任务)
* [获取同步任务状态](#获取同步任务状态)
* [获取同步任务列表](#获取同步任务列表)
* [获取同步任务的同步规则列表](#获取同步任务的同步规则列表)
* [获取同步任务关联数据源的数据库名列表](#获取同步任务关联数据源的数据库名列表)
* [获取同步任务关联数据源的数据表名列表](#获取同步任务关联数据源的数据表名列表)
* [获取同步任务关联数据源的数据表的创建语句](#获取同步任务关联数据源的数据表的创建语句)
* [更新同步任务关联数据源的数据表的创建语句](#更新同步任务关联数据源的数据表的创建语句)
* [删除同步任务关联数据源的数据表](#删除同步任务关联数据源的数据表)

本文档以下部分描述当前提供的 API 的具体使用方法。

## API 统一错误格式

对 API 发起的请求后，如发生错误，返回错误信息的格式如下所示：

```json
{
    "error_code": 46018,
    "error_msg": "[code=46018:class=scheduler:scope=internal:level=medium], Message: task with name task-test not exist, Workaround: Please use `query-status` command to see tasks."
}
```

如上所示，`error_msg` 描述错误信息，`error_code` 则是对应的错误码。

## 获取 DM-master 节点信息

该接口是一个同步接口，请求成功会返回对应节点的状态信息。

### 请求 URI

`GET /api/v1/cluster/masters`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/cluster/masters' \
  -H 'accept: application/json'
```

```json
{
    "data": [
        {
            "addr": "http://127.0.0.1:8261",
            "alive": true,
            "leader": false,
            "name": "master1"
        },
        {
            "addr": "http://1.2.3.4:5678",
            "alive": true,
            "leader": false,
            "name": "master2"
        },
        {
            "addr": "http://2.3.4.5:6789",
            "alive": true,
            "leader": true,
            "name": "master3"
        }
    ],
    "total": 3
}
```

## 下线 DM-master 节点

该接口是一个同步接口，请求成功后返回体的 Status Code 是 204。

### 请求 URI

`DELETE /api/v1/cluster/masters/{master-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/masters/master1' \
  -H 'accept: */*'
```

## 获取 DM-worker 节点信息

该接口是一个同步接口，请求成功会返回对应节点的状态信息。

### 请求 URI

`GET /api/v1/cluster/workers`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/cluster/workers' \
  -H 'accept: application/json'
```

```json
{
    "data": [
        {
            "addr": "10.2.8.3:8862",
            "bound_source_name": "mysql-01",
            "bound_stage": "bound",
            "name": "dm-10.2.8.3-8862"
        },
        {
            "addr": "10.2.8.3:8962",
            "bound_source_name": "",
            "bound_stage": "free",
            "name": "dm-10.2.8.3-8962"
        }
    ],
    "total": 2
}
```

## 下线 DM-worker 节点

该接口是一个同步接口，请求成功后返回体的 Status Code 是 204。

### 请求 URI

`DELETE /api/v1/cluster/workers/{worker-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/cluster/workers/worker1' \
  -H 'accept: */*'
```

## 创建数据源

该接口是一个同步接口，请求成功会返回对应数据源信息。

### 请求 URI

`POST /api/v1/sources`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
{
  "source": {
    "source_name": "mysql-01",
    "host": "10.2.8.3",
    "port": 3306,
    "user": "root",
    "password": "password",
    "enable": true,
    "enable_gtid": false
  }
}'
```

```json
{
    "enable": true,
    "enable_gtid": false,
    "host": "10.2.8.3",
    "password": "support123",
    "port": 3306,
    "security": null,
    "source_name": "mysql-01",
    "user": "root"
}
```

## 获取数据源

该接口是一个同步接口，请求成功会返回数据源列表信息。

### 请求 URI

`GET /api/v1/sources/{source-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET'\
  'http://127.0.0.1:8261/api/v1/sources/mysql-01?with_status=true'\
  -H 'accept: application/json'
```

```json
{
    "enable": true,
    "enable_gtid": false,
    "flavor": "mysql",
    "host": "10.2.8.3",
    "password": "******",
    "port": 3306,
    "purge": {
        "expires": 0,
        "interval": 3600,
        "remain_space": 15
    },
    "relay_config": {
        "enable_relay": false,
        "relay_binlog_gtid": "",
        "relay_binlog_name": "",
        "relay_dir": "relay-dir"
    },
    "security": null,
    "source_name": "mysql-01",
    "status_list": [
        {
            "source_name": "mysql-01",
            "worker_name": "dm-10.2.8.3-8962"
        }
    ],
    "task_name_list": [],
    "user": "root"
}
```

## 删除数据源

该接口是一个同步接口，请求成功后返回的 Status Code 是 204。

### 请求 URI

`DELETE /api/v1/sources/{source-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01?force=true' \
  -H 'accept: application/json'
```

## 更新数据源

该接口是一个同步接口，请求成功会返回对应的数据源信息。

> **注意：**
>
> 更新数据源配置时，须确保当前数据源下没有任何正在运行的同步任务。

### 请求 URI

`PUT /api/v1/sources/{source-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
{
  "source": {
    "source_name": "mysql-01",
    "host": "10.2.8.3",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "enable": true,
    "enable_gtid": false,
    "purge": {
      "expires": 0,
      "interval": 3600,
      "remain_space": 15
    }
  }
}'
```

```json
{
    "enable": true,
    "enable_gtid": false,
    "host": "10.2.8.3",
    "password": "123456",
    "port": 3306,
    "purge": {
        "expires": 0,
        "interval": 3600,
        "remain_space": 15
    },
    "security": null,
    "source_name": "mysql-01",
    "user": "root"
}
```

## 启用数据源

这是一个同步接口，请求成功后会启用此数据源，并批量开始数据迁移任务中依赖该数据源的所有子任务。

### 请求 URI

`POST /api/v1/sources/{source-name}/enable`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## 停用数据源

这是一个同步接口，请求成功后会停用此数据源，并批量停止数据迁移任务中依赖该数据源的所有子任务。

### 请求 URI

`POST /api/v1/sources/{source-name}/disable`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json'
```

## 获取数据源列表

该接口是一个同步接口，请求成功会返回数据源列表信息。

### 请求 URI

`GET /api/v1/sources`

### 使用样例

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
            "enable": true,
            "enable_gtid": false,
            "flavor": "mysql",
            "host": "10.2.8.3",
            "password": "******",
            "port": 3306,
            "purge": {
                "expires": 0,
                "interval": 3600,
                "remain_space": 15
            },
            "relay_config": {
                "enable_relay": false,
                "relay_binlog_gtid": "",
                "relay_binlog_name": "",
                "relay_dir": "relay-dir"
            },
            "security": null,
            "source_name": "mysql-01",
            "status_list": [
                {
                    "source_name": "mysql-01",
                    "worker_name": "dm-10.2.8.3-8962"
                }
            ],
            "task_name_list": [],
            "user": "root"
        }
    ],
    "total": 1
}
```

## 获取数据源状态

该接口是一个同步接口，请求成功会返回对应节点的状态信息。

### 请求 URI

`GET /api/v1/sources/{source-name}/status`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-replica-01/status' \
  -H 'accept: application/json'
```

```json
{
    "data": [
        {
            "source_name": "mysql-01",
            "worker_name": "dm-10.2.8.3-8962"
        }
    ],
    "total": 1
}
```

## 对数据源开启 relay-log 功能

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取数据源状态](#获取数据源状态)接口获取最新的状态。

### 请求 URI

`POST /api/v1/sources/{source-name}/relay/enable`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/enable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '
{
  "worker_name_list": [
    "dm-10.2.8.3-8862"
  ]
}'
```

## 对数据源停止 relay-log 功能

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取数据源状态](#获取数据源状态)接口获取最新的状态。

### 请求 URI

`POST /api/v1/sources/{source-name}/relay/disable`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/disable' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '
{
  "worker_name_list": [
    "dm-10.2.8.3-8862"
  ]
}'
```

## 清除数据源不需要的 relay-log 文件

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取数据源状态](#获取数据源状态)接口获取最新的状态。

### 请求 URI

`POST /api/v1/sources/{source-name}/relay/purge`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/relay/purge' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '
{
  "relay_binlog_name": "mysql-bin.000002",
  "relay_dir": "string"
}'
```

## 更改数据源和 DM-worker 的绑定关系

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取 DM-worker 节点信息](#获取-dm-worker-节点信息)接口获取最新的状态。

### 请求 URI

`POST /api/v1/sources/{source-name}/transfer`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/sources/mysql-01/transfer' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '
{
  "worker_name": "dm-10.2.8.3-8862"
}'
```

## 获取数据源的数据库名列表

该接口是一个同步接口，请求成功会返回对应的列表。

### 请求 URI

`GET /api/v1/sources/{source-name}/schemas`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1/schemas' \
  -H 'accept: application/json'
```

```json
[
    "information_schema",
    "mysql",
    "performance_schema",
    "sbtest1",
    "sbtest3",
    "sys",
    "test",
]
```

## 获取数据源的指定数据库的表名列表

该接口是一个同步接口，请求成功会返回对应的列表。

### 请求 URI

`GET /api/v1/sources/{source-name}/schemas/{schema-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/sources/source-1/schemas/db1' \
  -H 'accept: application/json'
```

```json
[
    "sbtest1",
    "sbtest2"
]
```

## 创建同步任务

这是一个同步接口，请求成功的 Status Code 是 200，请求成功会返回对应的同步任务信息。

### 请求 URI

`POST /api/v1/tasks`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
{
  "task": {
    "name": "task-1",
    "task_mode": "all",
    "meta_schema": "dm-meta",
    "enhance_online_schema_change": true,
    "on_duplicate": "error",
    "target_config": {
      "host": "10.2.8.3",
      "port": 4913,
      "user": "root",
      "password": "password"
    },
    "binlog_filter_rule": {
      "rule-1": {
        "ignore_sql": [
          "DROP DATABASE"
        ]
      }
    },
    "table_migrate_rule": [
      {
        "source": {
          "source_name": "mysql-01",
          "schema": "db1",
          "table": "tb1"
        },
        "target": {
          "schema": "db1",
          "table": "tb1"
        },
        "binlog_filter_rule": [
          "rule-1"
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
          "source_name": "mysql-01"
        }
      ]
    }
  }
}'
```

```json
{
    "check_result": "pre-check is passed. ",
    "task": {
        "binlog_filter_rule": {
            "rule-1": {
                "ignore_sql": [
                    "DROP DATABASE"
                ]
            }
        },
        "enhance_online_schema_change": true,
        "meta_schema": "dm-meta",
        "name": "task-1",
        "on_duplicate": "error",
        "source_config": {
            "full_migrate_conf": {
                "consistency": "auto",
                "data_dir": "./exported_data",
                "export_threads": 4,
                "import_threads": 16
            },
            "incr_migrate_conf": {
                "repl_batch": 100,
                "repl_threads": 16
            },
            "source_conf": [
                {
                    "source_name": "mysql-01"
                }
            ]
        },
        "table_migrate_rule": [
            {
                "binlog_filter_rule": [
                    "rule-1"
                ],
                "source": {
                    "schema": "db1",
                    "source_name": "mysql-01",
                    "table": "tb1"
                },
                "target": {
                    "schema": "db1",
                    "table": "tb1"
                }
            }
        ],
        "target_config": {
            "host": "10.2.8.3",
            "password": "password",
            "port": 4913,
            "security": null,
            "user": "root"
        },
        "task_mode": "all"
    }
}
```

## 获取同步任务

这是一个同步接口，请求成功的 Status Code 是 200。

### 请求 URI

`GET /api/v1/tasks/{task-name}?with_status=true`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1?with_status=true' \
  -H 'accept: application/json'
```

```json
{
    "binlog_filter_rule": {
        "mysql-01-filter-rule-0": {
            "ignore_sql": [
                "DROP DATABASE"
            ]
        }
    },
    "enhance_online_schema_change": true,
    "meta_schema": "dm-meta",
    "name": "task-1",
    "on_duplicate": "error",
    "source_config": {
        "full_migrate_conf": {
            "consistency": "auto",
            "data_dir": "./exported_data",
            "export_threads": 4,
            "import_threads": 16
        },
        "incr_migrate_conf": {
            "repl_batch": 100,
            "repl_threads": 16
        },
        "source_conf": [
            {
                "source_name": "mysql-01"
            }
        ]
    },
    "status_list": [
        {
            "name": "task-1",
            "source_name": "mysql-01",
            "stage": "Stopped",
            "sync_status": {
                "binlog_type": "remote",
                "blocking_ddls": null,
                "master_binlog": "(mysql-bin.000005, 15403)",
                "master_binlog_gtid": "",
                "recent_tps": 0,
                "seconds_behind_master": 0,
                "synced": true,
                "syncer_binlog": "(mysql-bin.000005, 15403)",
                "syncer_binlog_gtid": "",
                "total_events": 0,
                "total_tps": 0,
                "unresolved_groups": null
            },
            "unit": "Sync",
            "unresolved_ddl_lock_id": "",
            "worker_name": "dm-10.2.8.3-8862"
        }
    ],
    "strict_optimistic_shard_mode": false,
    "table_migrate_rule": [
        {
            "binlog_filter_rule": [
                "mysql-01-filter-rule-0"
            ],
            "source": {
                "schema": "db1",
                "source_name": "mysql-01",
                "table": "tb1"
            },
            "target": {
                "schema": "db1",
                "table": "tb1"
            }
        }
    ],
    "target_config": {
        "host": "10.2.8.3",
        "password": "password",
        "port": 4913,
        "security": null,
        "user": "root"
    },
    "task_mode": "all"
}
```

## 删除同步任务

该接口是一个同步接口，请求成功后返回的 Status Code 是 204。

### 请求 URI

`DELETE /api/v1/tasks/{task-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json'
```

## 更新同步任务

该接口是一个同步接口，请求成功会返回对应同步任务的信息。

> **注意：**
>
> 更新同步任务配置时，须确保该任务处于暂停状态，并已经运行到增量同步的阶段，且仅有部分字段可以更新。

### 请求 URI

`PUT /api/v1/tasks/{task-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '
{
  "task": {
    "name": "task-1",
    "task_mode": "all",
    "meta_schema": "dm-meta",
    "enhance_online_schema_change": true,
    "on_duplicate": "error",
    "target_config": {
      "host": "10.2.8.3",
      "port": 4913,
      "user": "root",
      "password": ""
    },
    "table_migrate_rule": [
      {
        "source": {
          "source_name": "mysql-01",
          "schema": "db1",
          "table": "tb1"
        },
        "target": {
          "schema": "db1",
          "table": "tb1"
        }
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
          "source_name": "mysql-01"
        }
      ]
    }
  }
}'
```

```json
{
    "check_result": "pre-check is passed. ",
    "task": {
        "enhance_online_schema_change": true,
        "meta_schema": "dm-meta",
        "name": "task-1",
        "on_duplicate": "error",
        "source_config": {
            "full_migrate_conf": {
                "consistency": "auto",
                "data_dir": "./exported_data",
                "export_threads": 4,
                "import_threads": 16
            },
            "incr_migrate_conf": {
                "repl_batch": 100,
                "repl_threads": 16
            },
            "source_conf": [
                {
                    "source_name": "mysql-01"
                }
            ]
        },
        "table_migrate_rule": [
            {
                "source": {
                    "schema": "db1",
                    "source_name": "mysql-01",
                    "table": "tb1"
                },
                "target": {
                    "schema": "db1",
                    "table": "tb1"
                }
            }
        ],
        "target_config": {
            "host": "10.2.8.3",
            "password": "",
            "port": 4913,
            "security": null,
            "user": "root"
        },
        "task_mode": "all"
    }
}
```

## 开始同步任务

这是一个异步接口，请求成功的 Status Code 是 200。可通过[获取同步任务状态](#获取同步任务状态)接口获取最新的任务状态。

### 请求 URI

`POST /api/v1/tasks/{task-name}/start`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/start' \
  -H 'accept: */*'
```

## 停止同步任务

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取同步任务状态](#获取同步任务状态)接口获取最新的任务状态。

### 请求 URI

`POST /api/v1/tasks/{task-name}/stop`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'POST' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/stop' \
  -H 'accept: */*'
```

## 获取同步任务状态

该接口是一个同步接口，请求成功会返回对应节点的状态信息。

### 请求 URI

`GET /api/v1/tasks/task-1/status`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/status' \
  -H 'accept: application/json'
```

```json
{
    "data": [
        {
            "name": "task-1",
            "source_name": "mysql-01",
            "stage": "Stopped",
            "sync_status": {
                "binlog_type": "remote",
                "blocking_ddls": null,
                "master_binlog": "(mysql-bin.000005, 15403)",
                "master_binlog_gtid": "",
                "recent_tps": 0,
                "seconds_behind_master": 0,
                "synced": true,
                "syncer_binlog": "(mysql-bin.000005, 15403)",
                "syncer_binlog_gtid": "",
                "total_events": 0,
                "total_tps": 0,
                "unresolved_groups": null
            },
            "unit": "Sync",
            "unresolved_ddl_lock_id": "",
            "worker_name": "dm-10.2.8.3-8862"
        }
    ],
    "total": 1
}
```

## 获取同步任务列表

该接口是一个同步接口，请求成功会返回对应的同步任务列表。

### 请求 URI

`GET /api/v1/tasks`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'GET' \
  'http://127.0.0.1:8261/api/v1/tasks' \
  -H 'accept: application/json'
```

```json
{
    "data": [
        {
            "enhance_online_schema_change": true,
            "meta_schema": "dm-meta",
            "name": "task-1",
            "on_duplicate": "error",
            "source_config": {
                "full_migrate_conf": {
                    "consistency": "auto",
                    "data_dir": "./exported_data",
                    "export_threads": 4,
                    "import_threads": 16
                },
                "incr_migrate_conf": {
                    "repl_batch": 100,
                    "repl_threads": 16
                },
                "source_conf": [
                    {
                        "source_name": "mysql-01"
                    }
                ]
            },
            "strict_optimistic_shard_mode": false,
            "table_migrate_rule": [
                {
                    "source": {
                        "schema": "db1",
                        "source_name": "mysql-01",
                        "table": "tb1"
                    },
                    "target": {
                        "schema": "db1",
                        "table": "tb1"
                    }
                }
            ],
            "target_config": {
                "host": "10.2.8.3",
                "password": "",
                "port": 4913,
                "security": null,
                "user": "root"
            },
            "task_mode": "all"
        }
    ],
    "total": 1
}
```

## 获取同步任务的同步规则列表

该接口是一个同步接口，请求成功会返回对应同步任务的同步规则列表。

### 请求 URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/migrate_targets`

### 使用样例

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

## 获取同步任务关联数据源的数据库名列表

该接口是一个同步接口，请求成功会返回对应的列表。

### 请求 URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas`

### 使用样例

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

## 获取同步任务关联数据源的数据表名列表

该接口是一个同步接口，请求成功会返回对应的列表。

### 请求 URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}`

### 使用样例

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

## 获取同步任务关联数据源的数据表的创建语句

该接口是一个同步接口，请求成功会返回对应的创建语句。

### 请求 URI

`GET /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 使用样例

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

## 更新同步任务关联数据源的数据表的创建语句

该接口是一个同步接口，返回体的 Status Code 是 200。

### 请求 URI

`POST /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 使用样例

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

## 删除同步任务关联数据源的数据表

该接口是一个同步接口，返回体的 Status Code 是 200。

### 请求 URI

`DELETE /api/v1/tasks/{task-name}/sources/{source-name}/schemas/{schema-name}/{table-name}`

### 使用样例

{{< copyable "shell-regular" >}}

```shell
curl -X 'DELETE' \
  'http://127.0.0.1:8261/api/v1/tasks/task-1/sources/source-1/schemas/db1/table1' \
  -H 'accept: */*'
```
