---
title: TiProxy API
summary: 了解 TiProxy 的 API。
---

# TiProxy API

本文介绍了 TiProxy 的 API。

> **注意：**
>
> TiProxy API 主要用于诊断调试，不保证和 TiProxy 未来引入的新特性完全兼容。因此不推荐客户在应用程序开发或工具开发中利用 TiProxy API 获取结果。

## 使用方法

TiProxy API 地址：`http://${host}:${port}`

其中 `host` 和 `port` 由 TiProxy 配置中的 [api.addr](/tiproxy/tiproxy-configuration.md#addr-1) 指定。

例如：

```bash
curl http://127.0.0.1:3080/api/admin/config/
```

## API

### 配置

`/api/admin/config/` 用于设置或获取 TiProxy 配置。

当使用 `GET` 方式访问 `/api/admin/config/` 时，API 返回当前配置。可通过 `format` 指定格式，支持 `json` 和 `toml` 格式，默认为 `toml` 格式。

例如获取 `json` 格式的配置：

```bash
curl "http://127.0.0.1:3080/api/admin/config/?format=json"
```

当使用 `PUT` 方式访问 `/api/admin/config/` 时，给 TiProxy 设置 `toml` 格式的配置。其他未指定的配置项将不会改变，因此你只需指定需要更改的配置项。

例如，以下命令将 `log.level` 设置为 `warning`，其他配置项的值不会改变：

```bash
$ cat test.toml
[log]
level='warning'
$ curl -X PUT --data-binary @test.toml http://127.0.0.1:3080/api/admin/config/
```

### 健康

`/api/debug/health` 用于获取 TiProxy 的健康状况以及配置的 checksum。当 TiProxy 正常运行时，返回配置的 checksum；当 TiProxy 正在关闭时，返回错误。

例如：

```bash
$ curl http://127.0.0.1:3080/api/debug/health
{"config_checksum":3006078629}
```

### 监控

`/metrics` 用于获取 TiProxy 的监控数据。