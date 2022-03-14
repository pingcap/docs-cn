---
title: 使用 OpenAPI 运维集群
summary: 了解如何使用 OpenAPI 接口来管理集群状态和数据同步。
---

# 使用 OpenAPI 运维集群

DM 提供 OpenAPI 功能，您可以通过 OpenAPI 方便地对 DM 集群进行查询和运维操作。OpenAPI 的功能范围和 [dmctl 工具](/dm/dmctl-introduction.md)相当。如需开启 OpenAPI，请在 DM-master 的配置文件中增加如下配置项：

```toml
openapi = true
```

> **注意：**
>
> - DM 提供符合 OpenAPI 3.0.0 标准的 [Spec 文档](https://github.com/pingcap/tiflow/blob/master/dm/openapi/spec/dm.yaml)，其中包含了所有 API 的请求参数和返回体，你可自行复制到如 [Swagger Editor](https://editor.swagger.io/) 等工具中在线预览文档。
>
> - 部署 DM-master 后，你可访问 `http://{master-addr}/api/v1/docs` 在线预览文档。
>
> - OpenAPI v6.0.0 版本中有较大改动。

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
* [清除对数据源上已经不需要的 relay-log 文件](#清除对数据源上已经不需要的-relay-log-文件)
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
* [获取同步任务同步规则列表](#获取同步任务同步规则列表)
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
    "error_msg": "",
    "error_code": ""
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

## 获取数据源

该接口是一个同步接口，请求成功会返回数据源列表信息。

### 请求 URI

 `GET /api/v1/sources/{source-name}`

### 使用样例

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

## 删除数据源

该接口是一个同步接口，请求成功后返回体的 Status Code 是 204。

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

该接口是一个同步接口，请求成功会返回对应数据源信息。
> **注意：**
>
> 更新数据源配置时需要当前数据源下没有任何正在运行的同步任务

### 请求 URI

 `PUT /api/v1/sources/{source-name}`

### 使用样例

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

## 启用数据源

这是一个同步接口，请求成功的时会启用此数据源，并批量开始数据迁移任务中依赖该数据源的所有子任务。

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

这是一个同步接口，请求成功的时会停用此数据源，并批量停止数据迁移任务中依赖该数据源的所有子任务。

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
  -d '{
  "worker_name_list": [
    "worker-1"
  ],
  "relay_binlog_name": "mysql-bin.000002",
  "relay_binlog_gtid": "e9a1fc22-ec08-11e9-b2ac-0242ac110003:1-7849",
  "relay_dir": "./relay_log"
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
  -d '{
  "worker_name_list": [
    "worker-1"
  ]
}'
```

## 清除对数据源上已经不需要的 relay-log 文件

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
  -d '{
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
  -d '{
  "worker_name": "worker-1"
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
  "db1"
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
  "table1"
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

## 获取同步任务

这是一个同接口，请求成功的 Status Code 是 200

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

## 删除同步任务

该接口是一个同步接口，请求成功后返回体的 Status Code 是 204。

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

该接口是一个同步接口，请求成功会返回对应数据源信息。

> **注意：**
>
> 更新同步任务配置时需要该任务处于暂停状态并已经运行到增量同步的阶段，且仅有部分字段可以更新。

### 请求 URI

 `PUT /api/v1/tasks/{task-name}`

### 使用样例

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

## 开始同步任务

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取同步任务状态](#获取同步任务状态)接口获取最新的状态。

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

这是一个异步接口，请求成功的 Status Code 是 200，可通过[获取同步任务状态](#获取同步任务状态)接口获取最新的状态。

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

## 获取同步任务列表

该接口是一个同步接口，请求成功会返回对应的同步任务信息。

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

## 获取同步任务同步规则列表

该接口是一个同步接口，请求成功会返回对应的列表。

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
