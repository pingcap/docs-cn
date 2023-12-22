---
title: TiProxy 命令行参数
summary: 了解 TiProxy 的命令行参数。
---

# TiProxy 命令行参数

本文介绍了在启动 TiProxy 时可用的命令行参数，以及 `tiproxyctl` 的参数。

## TiProxy server

本节介绍 TiProxy 服务器程序 `tiproxy` 的参数。

### `--config string`

+ 指定 TiProxy 配置文件的路径。
+ 默认值：`""`
+ 必须指定配置文件。有关详细配置项，请参见 [配置 TiProxy](/tiproxy/tiproxy-configuration.md)。

### `--log_encoder string`

+ 指定 TiProxy 的日志格式。
+ 默认值：`""`
+ 如果为空，则使用 TiDB 的日志格式。

### `--log_level string`

+ 指定 TiProxy 的日志级别。
+ 默认值：`""`
+ 如果为空，则使用 `"info"`。

## TiProxy control

本节介绍 TiProxy 客户端程序 `tiproxyctl` 的参数。

### `--log_encoder string`

+ 指定 tiproxyctl 的日志格式。
+ 默认值：`"tidb"`
+ 如果为空，则使用 TiDB 的日志格式。此外，还可以指定以下格式之一：

    - `console`：更易读的格式
    - `json`：结构化日志格式

### `--log_level string`

+ 指定 tiproxyctl 的日志级别。
+ 默认值：`"warn"`
+ 可以指定以下日志级别之一：`debug`、`info`、`warn`、`error`、`panic`。

### `--curls urls`

+ 指定服务器地址。可以添加多个监听地址。
+ 默认值：`"[localhost:3080]"`
+ 服务器 API 网关地址。

### `-k, --insecure`

+ 指定是否在与服务器建立连接时跳过 TLS CA 验证。
+ 默认值：`false`
+ 用于测试。

### `--ca string`

+ 指定在与服务器建立连接时使用的 CA。
+ 默认值：`""`

### `--cert string`

+ 指定在与服务器建立连接时使用的证书。
+ 默认值：`""`
