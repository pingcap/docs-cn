---
title: DM-worker 配置文件介绍
---

# DM-worker 配置文件介绍

本文介绍 DM-worker 的配置文件，包括配置文件示例与配置项说明。

## 配置文件示例

```toml
# Worker Configuration.

name = "worker1"

# Log configuration.
log-level = "info"
log-file = "dm-worker.log"

# DM-worker listen address.
worker-addr = ":8262"
advertise-addr = "127.0.0.1:8262"
join = "http://127.0.0.1:8261,http://127.0.0.1:8361,http://127.0.0.1:8461"

keepalive-ttl = 60
relay-keepalive-ttl = 1800 # 版本 2.0.2 新增
# relay-dir = "relay_log" # 版本 5.4.0 新增。使用相对路径时注意结合部署、启动方式确认路径位置。

ssl-ca = "/path/to/ca.pem"
ssl-cert = "/path/to/cert.pem"
ssl-key = "/path/to/key.pem"
cert-allowed-cn = ["dm"] 
```

## 配置项说明

### Global 配置

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `name`   | 标识一个 DM-worker。   |
| `log-level` | 日志级别：debug、info、warn、error、fatal。默认为 info。   |
| `log-file`   | 日志文件，如果不配置日志会输出到标准输出中。   |
| `worker-addr` | DM-worker 服务的地址，可以省略 IP 信息，例如：":8262"。|
| `advertise-addr` | DM-worker 向外界宣告的地址。 |
| `join` | 对应一个或多个 DM-master 配置中的 [`master-addr`](/dm/dm-master-configuration-file.md#global-配置)。 |
| `keepalive-ttl` | 当绑定的上游数据源没有启用 relay log 时，DM-worker 向 DM-master 保持存活的周期，单位为秒。默认是 60 秒。 |
| `relay-keepalive-ttl` | 当绑定的上游数据源启用 relay log 时，DM-worker 向 DM-master 保持存活的周期，单位为秒。默认是 1800 秒。在版本 2.0.2 新增。 |
| `relay-dir` | 当绑定的上游数据源启用 relay log 时，DM-worker 将 relay log 保存在该路径下。该配置优先级比上游数据源配置更高。在版本 5.4.0 新增。 |
| `ssl-ca` | DM-worker 组件用于与其它组件连接的 SSL CA 证书所在的路径  |
| `ssl-cert` | DM-worker 组件用于与其它组件连接的 PEM 格式的 X509 证书所在的路径 |
| `ssl-key` | DM-worker 组件用于与其它组件连接的 PEM 格式的 X509 密钥所在的路径  |
| `cert-allowed-cn` | 证书检查 Common Name 列表 |
