---
title: DM-master 配置文件介绍
category: reference
---

# DM-master 配置文件介绍

## 示例配置文件

DM-master 的示例配置文件如下所示：

```toml
#log configuration
log-level = "info"
log-file = "dm-master.log"

#dm-master listen address
master-addr = ":8261"

# replication group <-> dm-Worker deployment, we'll refine it when new deployment function is available
[[deploy]]
source-id = "mysql-replica-01"
dm-worker = "172.16.10.72:8262"

[[deploy]]
source-id = "mysql-replica-02"
dm-worker = "172.16.10.73:8262"
```

## 配置项说明

### 日志相关配置

`log-level`：日志等级，值可以为 "debug", "info", "warn", "error", "fatal"，默认值为 "info"。

`log-file`：日志文件。