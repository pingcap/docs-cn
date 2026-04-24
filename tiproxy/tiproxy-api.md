---
title: TiProxy API
summary: 了解如何使用 TiProxy API 获取 TiProxy 的配置、健康状况和监控数据等信息。
---

# TiProxy API

[TiProxy](/tiproxy/tiproxy-overview.md) 提供 API 接口，用于获取其配置、健康状况以及监控数据等信息。

> **注意：**
>
> TiProxy API 主要用于诊断调试，不保证与 TiProxy 未来引入的新特性完全兼容。因此不推荐在应用程序开发或工具开发中利用 TiProxy API 获取结果。

TiProxy API 的地址为 `http://${host}:${port}${path}`，其中 `${host}:${port}` 为 TiProxy 配置项 [`api.addr`](/tiproxy/tiproxy-configuration.md#addr-1) 的值，`${path}` 为你要访问的具体 API 的路径。例如：

```bash
curl http://127.0.0.1:3080/api/admin/config/
```

## 获取 TiProxy 的配置

### 请求 URI

`GET /api/admin/config/`

### 参数说明

查询参数：

- `format`：（可选）指定返回配置的格式，可选值为 `json` 和 `toml`，默认值为 `toml`。

### 使用样例

以下示例获取 JSON 格式的 TiProxy 配置：

```bash
curl "http://127.0.0.1:3080/api/admin/config/?format=json"
```

## 设置 TiProxy 的配置

目前，仅支持使用 TOML 格式修改 TiProxy 的配置。未指定的配置项将保持不变，因此只需指定需要更改的配置项。

### 请求 URI

`PUT /api/admin/config/`

### 请求体

TOML 格式的 TiProxy 的配置，例如：

```toml
[log]
level='warning'
```

### 使用样例

以下示例将 `log.level` 设置为 `'warning'`，其他配置项的值保持不变。

1. 查看当前 TiProxy 的配置：

    ```bash
    curl http://127.0.0.1:3080/api/admin/config/
    ```

    输出结果如下：

    ```toml
    [log]
    encoder = 'tidb'
    level = 'info'
    ```

2. 在 `test.toml` 文件中指定 `log.level` 的值，并发送 `PUT /api/admin/config/` 请求更新 `log.level` 的值：

    ```shell
    $ cat test.toml
    [log]
    level='warning'
    $ curl -X PUT --data-binary @test.toml http://127.0.0.1:3080/api/admin/config/
    ```

3. 查看修改后的 TiProxy 配置：

    ```bash
    curl http://127.0.0.1:3080/api/admin/config/
    ```

    输出结果如下：

    ```toml
    [log]
    encoder = 'tidb'
    level = 'warning'
    ```

## 获取 TiProxy 的健康状况

用于获取 TiProxy 的健康状况以及配置的校验和 (checksum)。当 TiProxy 正常运行时，返回配置的 checksum。当 TiProxy 处于关闭状态或者正在关闭时，返回错误。

### 请求 URI

`GET /api/debug/health`

### 使用样例

```bash
curl http://127.0.0.1:3080/api/debug/health
```

输出结果示例：

```bash
{"config_checksum":3006078629}
```

## 获取 TiProxy 的监控数据

### 请求 URI

`GET /metrics/`

### 使用样例

```bash
curl http://127.0.0.1:3080/metrics/
```

## 访问控制

你可以通过启用 [`server-http-tls`](/tiproxy/tiproxy-configuration.md#server-http-tls)，并在 [security](/tiproxy/tiproxy-configuration.md#security) 部分的 `server-http-tls` 子配置中设置 `cert-allowed-cn` 选项，来限制对 TiProxy API 的访问。TiProxy 会使用客户端证书中的通用名 (Common Name, CN) 来[认证组件调用者身份](/enable-tls-between-components.md#认证组件调用者身份)。

如果未启用 TLS，你可以通过防火墙规则来控制访问。
