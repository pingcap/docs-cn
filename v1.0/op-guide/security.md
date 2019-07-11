---
title: 开启 TLS 验证
category: deployment
---

# 开启 TLS 验证

## 概述

本文档介绍 TiDB 集群如何开启 TLS 验证，其支持：

- TiDB 组件之间的双向验证，包括 TiDB、TiKV、PD 相互之间，TiKV Control 与 TiKV、PD Control 与 PD 的双向认证，以及 TiKV peer 之间、PD peer 之间。一旦开启，所有组件之间均使用验证，不支持只开启某一部分的验证。
- MySQL Client 与 TiDB 之间的客户端对服务器身份的单向验证以及双向验证。

MySQL Client 与 TiDB 之间使用一套证书，TiDB 集群组件之间使用另外一套证书。

## TiDB 集群组件间开启 TLS（双向认证）

### 准备证书

推荐为 TiDB、TiKV、PD 分别准备一个 server 证书，并保证可以相互验证，而它们的各种客户端共用 client 证书。

有多种工具可以生成自签名证书，如 `openssl`，`easy-rsa`，`cfssl`。

这里提供一个使用 `cfssl` 生成证书的示例：[生成自签名证书](generate-self-signed-certificates.md)。

### 配置证书

#### TiDB

在 config 文件或命令行参数中设置：

```toml
[security]
# Path of file that contains list of trusted SSL CAs for connection with cluster components.
cluster-ssl-ca = "/path/to/ca.pem"
# Path of file that contains X509 certificate in PEM format for connection with cluster components.
cluster-ssl-cert = "/path/to/tidb-server.pem"
# Path of file that contains X509 key in PEM format for connection with cluster components.
cluster-ssl-key = "/path/to/tidb-server-key.pem"
```

#### TiKV

在 config 文件或命令行参数中设置，并设置相应 url 为 https：

```toml
[security]
# set the path for certificates. Empty string means disabling secure connectoins.
ca-path = "/path/to/ca.pem"
cert-path = "/path/to/client.pem"
key-path = "/path/to/client-key.pem"
```

#### PD

在 config 文件或命令行参数中设置，并设置相应 url 为 https：

```toml
[security]
# Path of file that contains list of trusted SSL CAs. if set, following four settings shouldn't be empty
cacert-path = "/path/to/ca.pem"
# Path of file that contains X509 certificate in PEM format.
cert-path = "/path/to/server.pem"
# Path of file that contains X509 key in PEM format.
key-path = "/path/to/server-key.pem"
```

此时 TiDB 集群各个组件间便开启了双向验证。

在使用客户端连接时，需要指定 client 证书，示例：

```bash
./pd-ctl -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/pd-client.pem --key /path/to/pd-client-key.pem

./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
```

## MySQL 与 TiDB 间开启 TLS

### 准备证书

```bash
mysql_ssl_rsa_setup --datadir=certs
```

### 配置单向认证

在 TiDB 的 config 文件或命令行参数中设置：

```toml
[security]
# Path of file that contains list of trusted SSL CAs.
ssl-ca = ""
# Path of file that contains X509 certificate in PEM format.
ssl-cert = "/path/to/certs/server.pem"
# Path of file that contains X509 key in PEM format.
ssl-key = "/path/to/certs/server-key.pem"
```

客户端

```bash
mysql -u root --host 127.0.0.1 --port 4000 --ssl-mode=REQUIRED
```

### 配置双向认证

在 TiDB 的 config 文件或命令行参数中设置：

```toml
[security]
# Path of file that contains list of trusted SSL CAs for connection with mysql client.
ssl-ca = "/path/to/certs/ca.pem"
# Path of file that contains X509 certificate in PEM format for connection with mysql client.
ssl-cert = "/path/to/certs/server.pem"
# Path of file that contains X509 key in PEM format for connection with mysql client.
ssl-key = "/path/to/certs/server-key.pem"
```

客户端需要指定 client 证书

```bash
mysql -u root --host 127.0.0.1 --port 4000 --ssl-cert=/path/to/certs/client-cert.pem --ssl-key=/path/to/certs/client-key.pem --ssl-ca=/path/to/certs/ca.pem --ssl-mode=VERIFY_IDENTITY
```
