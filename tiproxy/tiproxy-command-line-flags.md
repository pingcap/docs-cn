---
title: TiProxy Command-Line Flags
summary: Learn the command-line startup flags of TiProxy.
---

# TiProxy Command-Line Flags

This document introduces the command-line flags that you can use when you launch TiProxy. It also introduces flags of `tiproxyctl`.

## TiProxy Server

This section lists the flags of the server program `tiproxy`.

### `--config`

+ Specifies the path of the TiProxy configuration file.
+ Type: `string`
+ Default: `""`
+ You must specify the configuration file. For detailed configuration items, refer to [Configure TiProxy](/tiproxy/tiproxy-configuration.md). Note that TiProxy automatically reloads the configuration when the configuration file is modified. Therefore, do not directly modify the configuration file. It is recommended to modify the configuration by executing [`tiup cluster edit-config`](/tiup/tiup-component-cluster-edit-config.md) or [`kubectl edit tc`](https://docs.pingcap.com/tidb-in-kubernetes/stable/modify-tidb-configuration).

## TiProxy control

This section lists the flags of the client program `tiproxyctl`.

### `--log_encoder`

+ Specifies the log format of `tiproxyctl`.
+ Type: `string`
+ Default: `"tidb"`
+ It defaults to the same log format of TiDB. However, you can also specify it as one of the following:

    - `console`: a more human-readable format
    - `json`: a structured log format

### `--log_level`

+ Specifies the log level of tiproxyctl.
+ Type: `string`
+ Default: `"warn"`
+ You can specify `debug`, `info`, `warn`, `error`, `panic`.

### `--curls`

+ Specifies the server addresses. You can add multiple listening addresses.
+ Type: `comma seperated lists of ip:port`
+ Default: `localhost:3080`
+ Server API gateway addresses.

### `-k`, `--insecure`

+ Specifies whether to skip TLS CA verification when dialing to the server.
+ Type: `boolean`
+ Default: `false`
+ Used for testing.

### `--ca`

+ Specifies the CA when dialing to the server.
+ Type: `string`
+ Default: `""`

### `--cert`

+ Specifies the certificate when dialing to the server.
+ Type: `string`
+ Default: `""`
