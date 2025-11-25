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
+ 必须指定配置文件。有关详细配置项，请参见[配置 TiProxy](/tiproxy/tiproxy-configuration.md)。注意，修改配置文件时 TiProxy 会自动重新加载配置，因此不要直接修改配置文件，建议通过 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 或 [`kubectl edit tc`](https://docs.pingcap.com/zh/tidb-in-kubernetes/v1.6/modify-tidb-configuration) 修改配置。

## TiProxy Control

本节介绍 TiProxy 客户端程序 `tiproxyctl` 的语法、选项和命令。

> **注意：**
>
> TiProxy Control 主要用于诊断调试，不保证和 TiProxy 未来引入的新特性完全兼容。因此不推荐在应用程序开发或工具开发中利用 TiProxy Control 获取结果。

### 语法

```
tiproxyctl [flags] [command]
```

示例：

```
tiproxyctl --curls 127.0.0.1:3080 config get
```

### 选项

#### `--log_encoder`

+ 指定 `tiproxyctl` 的日志格式。
+ 类型：`string`
+ 默认值：`"tidb"`
+ 如果为空，则使用 TiDB 的日志格式。此外，还可以指定以下格式之一：

    - `console`：更易读的格式
    - `json`：结构化日志格式

#### `--log_level`

+ 指定 `tiproxyctl` 的日志级别。
+ 类型：`string`
+ 默认值：`"warn"`
+ 可以指定以下日志级别之一：`debug`、`info`、`warn`、`error`、`panic`。

#### `--curls`

+ 指定服务器地址。可以添加多个监听地址。
+ 类型：逗号分隔的 ip:port 列表
+ 默认值：`localhost:3080`
+ 服务器 API 网关地址。

#### `-k, --insecure`

+ 指定是否在与服务器建立连接时跳过 TLS CA 验证。
+ 类型：`boolean`
+ 默认值：`false`
+ 用于测试。

#### `--ca`

+ 指定在与服务器建立连接时使用的 CA。
+ 类型：`string`
+ 默认值：`""`

#### `--cert`

+ 指定在与服务器建立连接时使用的证书。
+ 类型：`string`
+ 默认值：`""`

### 命令

#### `config set`

`tiproxyctl config set` 从标准输入读取 TOML 格式的配置文件，并将这些配置项设置到 TiProxy。其他未指定的配置项将保持不变，因此只需指定需要更改的配置项。

以下命令将 `log.level` 设置为 `'warning'`，其他配置项的值保持不变：

```bash
$ cat test.toml
[log]
level='warning'
$ cat test.toml | tiproxyctl config set
""
$ tiproxyctl config get | grep level
level = 'warning'
```

#### `config get`

`tiproxyctl config get` 用于获取当前 TiProxy 的配置，输出格式为 TOML。

#### `health`

`tiproxyctl health` 用于获取 TiProxy 的健康状况以及配置的校验和 (checksum)。当 TiProxy 正常运行时，返回配置的 checksum。当 TiProxy 处于关闭状态或者正在关闭时，返回错误。

输出示例：

```json
{"config_checksum":3006078629}
```