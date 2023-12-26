---
title: TiProxy 配置文件
summary: 了解与 TiProxy 部署和使用相关的配置参数。
---

# TiProxy 配置文件

本文档介绍了与 TiProxy 部署和使用相关的配置参数。以下是一个配置示例：

```toml
[proxy]
addr = "0.0.0.0:6000"
max-connections = 100

[api]
addr = "0.0.0.0:3080"

[log]
level = "info"

[security]
[security.cluster-tls]
skip-ca = true

[security.sql-tls]
skip-ca = true
```

## 配置 `tiproxy.toml` 文件

本小节介绍了 TiProxy 的配置参数。

> **建议：**
>
> 如需调整配置项的值，参见[修改配置参数](/maintain-tidb-using-tiup.md#修改配置参数)。通常情况下，修改配置项会导致重启，但是 TiProxy 支持热加载，你可以通过 `tiup cluster reload --skip-restart` 跳过重启。

### proxy

SQL 端口的配置。

#### `addr`

+ 默认值：`0.0.0.0:6000`
+ SQL 网关地址。格式为 `<ip>:<port>`。

#### `graceful-wait-before-shutdown`

+ 默认值：`0`
+ 支持热加载：是
+ 单位：秒
+ 当 HTTP 状态不健康时，SQL 端口在 `graceful-wait-before-shutdown` 秒内接受新连接。之后 SQL 端口将拒绝新连接并关闭现有连接。如果客户端和 TiProxy 之间没有其他代理（例如 NLB），建议将这个配置的值设置为 `0`。

#### `graceful-close-conn-timeout`

+ 默认值：`15`
+ 支持热加载：是
+ 单位：秒
+ 在当前事务完成后，在 `graceful-close-conn-timeout` 秒内关闭连接，也叫“排空客户端”。建议将此超时时间设置为长于事务的生命周期。

#### `max-connections`

+ 默认值：`0`
+ 支持热加载：是
+ 每个 TiProxy 实例最多可以接受 `max-connections` 个连接。`0` 表示没有限制。

#### `conn-buffer-size`

+ 默认值：`0`
+ 支持热加载：是，但只对新连接有效
+ 取值范围：`[1024, 16777216]`
+ 此配置项用于设置连接缓冲区大小，单位为字节。例如，`1024` 表示 1K 缓冲区。最小值为 `1K`，最大值为 `16M`。这是内存空间和性能之间的平衡。默认情况下，当值为 `0` 时，TiProxy 会使用默认大小的缓冲区，较大的缓冲区可能会有更高的性能。

#### `pd-addrs`

+ 默认值：`127.0.0.1:2379`
+ TiProxy 连接的 PD 地址。TiProxy 通过从 PD 获取 TiDB 列表来发现 TiDB 实例。如果使用 TiUP 或 TiDB Operator 部署 TiProxy，则会自动设置此项。

#### `proxy-protocol`

+ 默认值：`""`
+ 支持热加载：是
+ 可选值：`v2`
+ 在端口启用代理协议处理。可以指定 `v2` 来处理代理协议版本 2。不支持 `v1`。

#### `require-backend-tls`

+ 默认值：`true`
+ 支持热加载：是
+ 要求 TiProxy 和 TiDB 服务器之间使用 TLS 连接。如果 TiDB 服务器不支持 TLS，则客户端在连接到 TiProxy 时会报错。

### api

HTTP 网关的配置。

#### `addr`

+ 默认值：`0.0.0.0:3090`
+ API 网关地址。格式为 `<ip>:<port>`。

#### `proxy-protocol`

+ 默认值：``
+ 在端口启用代理协议处理

### log

#### `level`

+ 默认值：`info`
+ 支持热加载：是
+ 可选值：

    + `tidb`：TiDB 使用的格式。有关详细信息，请参见 [统一日志格式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)。
    + `json`：结构化 JSON 格式。
    + `console`：易读的日志格式。

### log.log-file

#### `filename`

+ 默认值：``
+ 支持热加载：是
+ 日志文件路径。非空值将启用日志记录到文件。

#### `max-size`

+ 默认值：`300`
+ 支持热加载：是
+ 日志文件的最大大小（以 MB 为单位）。日志将被轮转。

#### `max-days`

+ 默认值：`3`
+ 支持热加载：是
+ 指定保留旧日志文件的最大天数。超过此期限后，将删除过时的日志文件。

#### `max-backups`

+ 默认值：`3`
+ 支持热加载：是
+ 指定要保留的日志文件的最大数量。当超过此数量时，将自动删除多余的日志文件。

### security

在 `[security]` 部分有四个名称不同的 TLS 对象，它们共享相同的配置格式和字段，但是不同名称对象的字段解释可能不同。

```toml
[security]
    [sql-tls]
    skip-ca = true
    [server-tls]
    auto-certs = true
```

所有 TLS 选项都支持热加载。

TLS 对象字段：

+ `ca`：指定 CA
+ `cert`：指定证书
+ `key`：指定私钥
+ `auto-certs`：主要用于测试。如果没有指定证书/密钥，则会生成证书。
+ `skip-ca`：在客户端对象上跳过使用 CA 验证证书，或在服务器对象上跳过服务器端验证。
+ `min-tls-version`：设置最低 TLS 版本。
+ `rsa-key-size`：启用 `auto-certs` 时设置 RSA 密钥大小。
+ `autocert-expire-duration`：设置自动生成证书的默认到期时间。

对象根据名称被分类为客户端或服务器对象。

对客户端 TLS 对象：

- 必须设置 `ca` 或 `skip-ca` 来跳过验证服务器证书。
- 可选：可以设置 `cert`/`key` 来通过服务器端客户端验证。
- 无用字段：auto-certs。

对服务器 TLS 对象：

- 必须设置 `cert`/`key` 或 `auto-certs` 来生成临时证书，主要用于测试。
- 可选：如果 `ca` 不为空，则启用服务器端的客户端验证。客户端必须提供证书。如果 `skip-ca` 为 `true` 且 `ca` 不为空，则服务器仅在客户端提供证书时才验证客户端证书。

#### `cluster-tls`

客户端 TLS 对象。用于访问 TiDB 或 PD。

#### `sql-tls`

客户端 TLS 对象。用于访问 TiDB SQL 端口（4000）。

#### `server-tls`

服务器 TLS 对象。用于在 SQL 端口（6000）上提供 TLS。

#### `server-http-tls`

服务器 TLS 对象。用于在 HTTP 状态端口（3080）上提供 TLS。
