---
title: TiProxy 命令行参数
summary: 了解 TiProxy 的命令行参数。
---

# TiProxy 命令行参数

本文介绍了在启动 TiProxy 时可用的命令行参数，以及 `tiproxyctl` 的参数。

## TiProxy server

本节介绍 TiProxy 服务器程序 `tiproxy` 的参数。

### `--config`

+ 指定 TiProxy 配置文件的路径。
+ 类型：`string`
+ 默认值：`""`
+ 必须指定配置文件。有关详细配置项，请参见[配置 TiProxy](/tiproxy/tiproxy-configuration.md)。注意，修改配置文件时 TiProxy 会自动重新加载配置，因此不要直接修改配置文件，建议通过 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 或 [`kubectl edit tc`](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/modify-tidb-configuration) 修改配置。

## TiProxy control

本节介绍 TiProxy 客户端程序 `tiproxyctl` 的参数。

### `--log_encoder`

+ 指定 `tiproxyctl` 的日志格式。
+ 类型：`string`
+ 默认值：`"tidb"`
+ 如果为空，则使用 TiDB 的日志格式。此外，还可以指定以下格式之一：

    - `console`：更易读的格式
    - `json`：结构化日志格式

### `--log_level`

+ 指定 `tiproxyctl` 的日志级别。
+ 类型：`string`
+ 默认值：`"warn"`
+ 可以指定以下日志级别之一：`debug`、`info`、`warn`、`error`、`panic`。

### `--curls`

+ 指定服务器地址。可以添加多个监听地址。
+ 类型：逗号分隔的 ip:port 列表
+ 默认值：`localhost:3080`
+ 服务器 API 网关地址。

### `-k, --insecure`

+ 指定是否在与服务器建立连接时跳过 TLS CA 验证。
+ 类型：`boolean`
+ 默认值：`false`
+ 用于测试。

### `--ca`

+ 指定在与服务器建立连接时使用的 CA。
+ 类型：`string`
+ 默认值：`""`

### `--cert`

+ 指定在与服务器建立连接时使用的证书。
+ 类型：`string`
+ 默认值：`""`
