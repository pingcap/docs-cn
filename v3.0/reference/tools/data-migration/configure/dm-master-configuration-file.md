---
title: DM-master Configuration File
summary: Learn the configuration file of DM-master.
category: reference
---

# DM-master Configuration File

This document introduces the configuration of DM-master, including the configuration file template and configurable items.

## Configuration file template

The following is a configuration file template of DM-master.

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

## Configurable items

### Global configuration

| Name        | Description                                    |
| :------------ | :--------------------------------------- |
| `log-file` | The log file. If not specified, the log is printed to the standard output. |
| `master-addr` | The address of DM-master which provides services. You can omit the IP address and specify the port number only, such as ":8261". |

### DM-worker configuration

Each DM-worker must be configured in separate `[deploy]` sections.

| Name        | Description                                    |
| :------------ | :--------------------------------------- |
| `source-id` | Uniquely identifies a MySQL or MariaDB instance, or a replication group with the master-slave structure, which needs to be consistent with the `source-id` of DM-worker. |
| `dm-worker` | The service address of DM-worker. |
