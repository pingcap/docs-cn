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
+ 支持热加载：否
+ SQL 网关地址。格式为 `<ip>:<port>`。

#### `graceful-wait-before-shutdown`

+ 默认值：`0`
+ 支持热加载：是
+ 单位：秒
+ 在 TiProxy 关闭时，在 `graceful-wait-before-shutdown` 秒内，HTTP 状态返回不健康，但 SQL 端口仍接受新连接。`graceful-wait-before-shutdown` 秒之后 SQL 端口将拒绝新连接并关闭现有连接。如果客户端和 TiProxy 之间没有其他代理（例如 NLB），建议将这个配置的值设置为 `0`。

#### `graceful-close-conn-timeout`

+ 默认值：`15`
+ 支持热加载：是
+ 单位：秒
+ 在 TiProxy 关闭前，最多等待 `graceful-close-conn-timeout` 秒，连接的当前事务完成后将关闭连接。超时之后 TiProxy 将强制关闭所有连接。`graceful-close-conn-timeout` 发生在 `graceful-wait-before-shutdown` 之后。建议将此超时时间设置为长于事务的生命周期。

#### `max-connections`

+ 默认值：`0`
+ 支持热加载：是
+ 每个 TiProxy 实例最多可以接受 `max-connections` 个连接。`0` 表示没有限制。

#### `conn-buffer-size`

+ 默认值：`32768`
+ 支持热加载：是，但只对新连接有效
+ 单位：字节
+ 取值范围：`[1024, 16777216]`
+ 每个连接的缓冲区大小，读和写分别使用一个缓冲区。它是内存空间和性能之间的平衡，较大的缓冲区可能会有更高的性能，但占用更多内存。当值为 `0` 时，TiProxy 会使用默认大小的缓冲区。

#### `pd-addrs`

+ 默认值：`127.0.0.1:2379`
+ 支持热加载：否
+ TiProxy 连接的 PD 地址。TiProxy 通过从 PD 获取 TiDB 列表来发现 TiDB 实例。如果使用 TiUP 或 TiDB Operator 部署 TiProxy，则会自动设置此项。

#### `proxy-protocol`

+ 默认值：`""`
+ 支持热加载：是，但只对新连接有效
+ 可选值：`""`, `"v2"`
+ 在 SQL 端口启用 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)。开启 PROXY 协议后能让 TiProxy 透传客户端真实的 IP 地址给 TiDB。`"v2"` 代表使用 PROXY 协议 v2 版本，`""` 代表不使用 PROXY 协议。在 TiProxy 启用 PROXY 协议后，需要同时在 TiDB 服务器上启用 [PROXY 协议](/tidb-configuration-file.md#proxy-protocol)。

### api

HTTP 网关的配置。

#### `addr`

+ 默认值：`0.0.0.0:3080`
+ 支持热加载：否
+ API 网关地址。格式为 `<ip>:<port>`。

#### `proxy-protocol`

+ 默认值：`""`
+ 支持热加载：否
+ 可选值：`""`, `"v2"`
+ 在端口启用 [PROXY 协议](https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt)。`"v2"` 代表使用 PROXY 协议 v2 版本，`""` 代表不使用 PROXY 协议。

### log

#### `level`

+ 默认值：`info`
+ 支持热加载：是
+ 可选值：`debug`, `info`, `warn`, `error`, `panic`
+ 指定日志的级别。当指定 `panic` 级别时，TiProxy 遇到错误时会 panic。

#### `encoder`

+ 默认值：`tidb`
+ 可选值：

    + `tidb`：TiDB 使用的格式。有关详细信息，请参见 [统一日志格式](https://github.com/tikv/rfcs/blob/master/text/0018-unified-log-format.md)。
    + `json`：结构化 JSON 格式。
    + `console`：易读的日志格式。

### log.log-file

#### `filename`

+ 默认值：`""`
+ 支持热加载：是
+ 日志文件路径。非空值将启用日志记录到文件。使用 TiUP 部署时会自动设置文件路径。

#### `max-size`

+ 默认值：`300`
+ 支持热加载：是
+ 单位：MB
+ 日志文件的最大大小。超过该大小后，日志将被轮转。

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
+ `auto-certs`：主要用于测试。如果没有指定证书或密钥，则会生成证书。
+ `skip-ca`：在客户端对象上跳过使用 CA 验证证书，或在服务器对象上跳过服务器端验证。
+ `min-tls-version`：设置最低 TLS 版本。可选值：`1.0`、`1.1`、`1.2` 和 `1.3`。默认为 `1.2`，代表支持 TLSv1.2 及以上版本。
+ `rsa-key-size`：启用 `auto-certs` 时设置 RSA 密钥大小。
+ `autocert-expire-duration`：设置自动生成证书的默认到期时间。

对象根据名称被分类为客户端或服务器对象。

对客户端 TLS 对象：

- 必须设置 `ca` 或 `skip-ca` 来跳过验证服务器证书。
- 可选：可以设置 `cert` 或 `key` 来通过服务器端客户端验证。
- 无用字段：`auto-certs`。

对服务器 TLS 对象：

- 设置 `cert`、`key` 或 `auto-certs` 后支持 TLS 连接，否则不支持 TLS 连接。
- 可选：如果 `ca` 不为空，则启用服务器端的客户端验证。客户端必须提供证书。如果 `skip-ca` 为 `true` 且 `ca` 不为空，则服务器仅在客户端提供证书时才验证客户端证书。

#### `cluster-tls`

客户端 TLS 对象。用于访问 TiDB 或 PD。

#### `require-backend-tls`

+ 默认值：`false`
+ 支持热加载：是，但只对新连接有效
+ 要求 TiProxy 和 TiDB 服务器之间使用 TLS 连接。如果 TiDB 服务器不支持 TLS，则客户端在连接到 TiProxy 时会报错。

#### `sql-tls`

客户端 TLS 对象。用于访问 TiDB SQL 端口（4000）。

#### `server-tls`

服务器 TLS 对象。用于在 SQL 端口（6000）上提供 TLS。

#### `server-http-tls`

服务器 TLS 对象。用于在 HTTP 状态端口（3080）上提供 TLS。
