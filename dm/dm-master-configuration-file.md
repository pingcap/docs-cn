---
title: DM-master 配置文件介绍
aliases: ['/docs-cn/tidb-data-migration/dev/dm-master-configuration-file/']
---

# DM-master 配置文件介绍

本文介绍 DM-master 的配置文件，包括配置文件示例与配置项说明。

## 配置文件示例

DM-master 的示例配置文件如下所示：

```toml
name = "dm-master"

# log configuration
log-level = "info"
log-file = "dm-master.log"

# DM-master listening address
master-addr = ":8261"
advertise-addr = "127.0.0.1:8261"

# URLs for peer traffic
peer-urls = "http://127.0.0.1:8291"
advertise-peer-urls = "http://127.0.0.1:8291"

# cluster configuration
initial-cluster = "master1=http://127.0.0.1:8291,master2=http://127.0.0.1:8292,master3=http://127.0.0.1:8293"
join = ""

ssl-ca = "/path/to/ca.pem"
ssl-cert = "/path/to/cert.pem"
ssl-key = "/path/to/key.pem"
cert-allowed-cn = ["dm"]

secret-key-path = "/path/to/secret/key"
```

## 配置项说明

### Global 配置

| 配置项        | 说明                                    |
| :------------ | :--------------------------------------- |
| `name` | 标识一个 DM-master。|
| `log-level` | 日志级别：debug、info、warn、error、fatal。默认为 info。|
| `log-file` | 日志文件，如果不配置，日志会输出到标准输出中。|
| `master-addr` | DM-master 服务的地址，可以省略 IP 信息，例如：":8261"。|
| `advertise-addr` | DM-master 向外界宣告的地址。|
| `peer-urls` | DM-master 节点的对等 URL。|
| `advertise-peer-urls` | DM-master 向外界宣告的对等 URL。默认为 `peer-urls` 的值。|
| `initial-cluster` | 初始集群中所有 DM-master 的 `advertise-peer-urls` 的值。|
| `join` | 集群里已有的 DM-master 的 `advertise-peer-urls` 的值。如果是新加入的 DM-master 节点，使用 `join` 替代 `initial-cluster`。|
| `ssl-ca` | DM-master 组件用于与其它组件连接的 SSL CA 证书所在的路径  |
| `ssl-cert` | DM-master 组件用于与其它组件连接的 PEM 格式的 X509 证书所在的路径 |
| `ssl-key` | DM-master 组件用于与其它组件连接的 PEM 格式的 X509 密钥所在的路径  |
| `cert-allowed-cn` | 证书检查 Common Name 列表 |
| `secret-key-path` | 用来加解密上下游密码的密钥所在的路径，该文件内容必须是长度为 64 个字符的十六进制的 AES-256 密钥 |
