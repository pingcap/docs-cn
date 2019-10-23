---
title: DM-master 配置文件介绍
category: reference
---

# DM-master 配置文件介绍

本文介绍 DM-master 的配置文件，包括配置文件示例与配置项说明。

## 配置文件示例

DM-master 的示例配置文件如下所示：

```toml
# log configuration
log-file = "dm-master.log"

# DM-master listening address
master-addr = ":8261"

# DM-worker deployment. It will be refined when the new deployment function is available.
[[deploy]]
source-id = "mysql-replica-01"
dm-worker = "172.16.10.72:8262"

[[deploy]]
source-id = "mysql-replica-02"
dm-worker = "172.16.10.73:8262"
```

## 配置项说明

### Global 配置

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `log-file` | 日志文件，如果不配置，日志会输出到标准输出中。 |
| `master-addr` | DM-master 服务的地址，可以省略 IP 信息，例如：":8261"。 |

### DM-Worker 的配置

配置在 `deploy` 中，每一个 DM-worker 都需要设置一个 `deploy`。

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `source-id` | 一个 replication group 或者 MySQL/MariaDB 实例的标识，需要和 DM-worker 中的 `source-id` 一致。 |
| `dm-worker` | DM-worker 的服务地址。 |
