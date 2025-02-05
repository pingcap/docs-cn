---
title: TiProxy 命令行参数
summary: 了解 TiProxy 的命令行参数。
---

# TiProxy 命令行参数

本文介绍了在启动 TiProxy 时可用的命令行参数，以及 `tiproxyctl` 的参数。

## TiProxy server

本节介绍 TiProxy 服务器程序 `tiproxy` 的参数。

### `--advertise-addr`

+ 指定客户端连接 TiProxy 时使用的地址。
+ 类型：`string`
+ 默认值：`""`
+ 使用 TiUP 或 TiDB Operator 部署 TiProxy 时，此命令行参数会自动设置。如果未设置该参数，将使用该 TiProxy 实例的外部 IP 地址。

### `--config`

+ 指定 TiProxy 配置文件的路径。
+ 类型：`string`
+ 默认值：`""`
+ 必须指定配置文件。有关详细配置项，请参见[配置 TiProxy](/tiproxy/tiproxy-configuration.md)。注意，修改配置文件时 TiProxy 会自动重新加载配置，因此不要直接修改配置文件，建议通过 [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) 或 [`kubectl edit tc`](https://docs.pingcap.com/zh/tidb-in-kubernetes/dev/modify-tidb-configuration) 修改配置。

## TiProxy Control

本节介绍 TiProxy 客户端程序 `tiproxyctl` 的安装方式、语法、选项和命令。

### 安装 TiProxy Control

本节提供两种方式安装 TiProxy Control。

> **注意：**
>
> TiProxy Control 主要用于诊断调试，不保证和 TiProxy 未来引入的新特性完全兼容。因此不推荐在应用程序开发或工具开发中利用 TiProxy Control 获取结果。

#### 使用 TiUP 安装

在安装 [TiUP](/tiup/tiup-overview.md) 之后，可以使用 `tiup install tiproxy` 命令下载并安装 TiProxy 和 TiProxy Control 的二进制程序。安装后，你可以通过 `tiup --binary tiproxy` 查看 TiProxy 的安装路径，TiProxy Control 与 TiProxy 位于同一目录。

例如：

```shell
tiup install tiproxy
# download https://tiup-mirrors.pingcap.com/tiproxy-v1.3.0-linux-amd64.tar.gz 22.51 MiB / 22.51 MiB 100.00% 13.99 MiB/s
ls `tiup --binary tiproxy`ctl
# /root/.tiup/components/tiproxy/v1.3.0/tiproxyctl
```

#### 从源代码编译安装

编译环境要求：[Go](https://golang.org/) 1.21 或以上版本。

编译步骤：在 [TiProxy 项目](https://github.com/pingcap/tiproxy)根目录，使用 `make` 命令进行编译，生成 `tiproxyctl`。

```shell
git clone https://github.com/pingcap/tiproxy.git
cd tiproxy
make
ls bin/tiproxyctl
```

### 语法

```
tiproxyctl [flags] [command]
```

示例：

```
tiproxyctl --host 127.0.0.1 --port 3080 config get
```

### 选项

#### `--host`

+ 指定 TiProxy 服务器地址。
+ 类型：`string`
+ 默认值：`localhost`

#### `--port`

+ 指定 TiProxy API 网关地址的端口号。
+ 类型：`int`
+ 默认值：`3080`

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

#### `traffic capture`

`tiproxyctl traffic capture` 用于捕获流量。

选项：

- `--output`：（必填）指定流量文件存放的目录。
- `--duration`：（必填）指定捕获的时长。可选单位为 `m`（分钟）、`h`（小时）或 `d`（天）。例如 `--duration=1h` 指定捕获一小时的流量。

示例：

以下命令连接到 TiProxy 实例 `10.0.1.10:3080`，捕获一小时的流量，并保存到 TiProxy 实例的 `/tmp/traffic` 目录下：
    
```shell
tiproxyctl traffic capture --host 10.0.1.10 --port 3080 --output="/tmp/traffic" --duration=1h
```

#### `traffic replay`

`tiproxyctl traffic replay` 用于回放流量。

选项：

- `--username`：（必填）指定回放时使用的数据库用户名。
- `--password`：（可选）指定以上用户名的密码，默认为空字符串 `""`。
- `--input`：（必填）指定流量文件存放的目录。
- `--speed`：（可选）指定回放速率的倍数，范围为 `[0.1, 10]`，默认为 1，表示原速回放。

示例：

以下命令通过用户名 `u1` 和密码 `123456` 连接到 TiProxy 实例 `10.0.1.10:3080`，并从 TiProxy 实例的 `/tmp/traffic` 目录下读取流量文件，以 2 倍速率回放流量：

```shell
tiproxyctl traffic replay --host 10.0.1.10 --port 3080 --username="u1" --password="123456" --input="/tmp/traffic" --speed=2
```

#### `traffic cancel`

`tiproxyctl traffic cancel` 用于取消当前的捕获任务或回放任务。

#### `traffic show`

`tiproxyctl traffic show` 用于显示历史的捕获和回放任务。

输出中的 `status` 字段表示任务的状态，其可能的值包括：

- `done`：任务正常完成。
- `canceled`：任务被取消，查看 `error` 字段了解原因。
- `running`：任务正在运行，查看 `progress` 字段了解进度。

输出示例：

```json
[
  {
    "type": "capture",
    "start_time": "2024-09-01T14:30:40.99096+08:00",
    "end_time": "2024-09-01T16:30:40.99096+08:00",
    "duration": "2h",
    "output": "/tmp/traffic",
    "progress": "100%",
    "status": "done"
  },
  {
    "type": "capture",
    "start_time": "2024-09-02T18:30:40.99096+08:00",
    "end_time": "2024-09-02T19:00:40.99096+08:00",
    "duration": "2h",
    "output": "/tmp/traffic",
    "progress": "25%",
    "status": "canceled",
    "error": "canceled manually"
  },
  {
    "type": "capture",
    "start_time": "2024-09-03T13:31:40.99096+08:00",
    "duration": "2h",
    "output": "/tmp/traffic",
    "progress": "45%",
    "status": "running"
  }
]
```
