---
title: TiCDC 客户端鉴权
summary: 了解 TiCDC cli 和 api 的鉴权方式。
---

# TiCDC 客户端鉴权

从 v8.1.0 起，TiCDC 支持通过 mtls 或 TiDB 用户名密码进行客户端鉴权。
  1. mtls（双向传输层安全协议）鉴权：提供了在传输层进行安全控制的方法，使 TiCDC 可以验证客户端身份。
  2. 通过 TiDB 用户名密码鉴权：提供了在应用层进行安全控制的方法，合法用户需要有通过 TiCDC 节点进行登录的权限。

这些鉴权方式可以单独使用，也可以结合起来使用，以满足不同的场景和安全需求。

> **注意：**
>
> TiCDC 只支持在开启 tls 加密时进行客户端鉴权。

## 通过 mtls 进行客户端鉴权

- cdc server 中开启 mtls 鉴权
  ```toml
  [security]
  # 控制是否开启 TLS 客户端鉴权，默认值为 false。
  mtls = true
  ```

- 使用 cli 时，cdc 按照以下顺序读取客户端证书：
  1. 通过命令行参数 `--cert` 和 `--key` 指定用于鉴权的证书和私钥。如果服务端使用了自签名证书，还需要通过 `--ca` 指定受信任的 CA 证书。
  2. 通过环境变量 `TICDC_CA_PATH`、`TICDC_CERT_PATH`、`TICDC_KEY_PATH` 配置客户端证书。
  3. 通过共享凭证文件 `~/.ticdc/credentials` 获取客户端证书。你可以通过命令 `cdc cli configure-credentials` 更改这个文件的配置。

- 使用 curl 命令访问 api 时：
  - 通过 `--cert` 和 `--key` 指定客户端证书。如果服务端使用了自签名证书，还需要通过 `--cacert` 指定受信任的 CA 证书。


## 通过 TiDB 用户进行客户端鉴权

- 在 tidb 中创建用户，并允许从 TiCDC 所在节点登陆
```sql
CREATE USER 'test'@'ticdc_ip_address' IDENTIFIED BY 'password';
```

- cdc server 中开启用户名和密码鉴权
  ```toml
  [security]
  # 控制是否使用用户名和密码进行客户端鉴权，默认值为 false。
  client-user-required = true
  # 指定可用于客户端鉴权的用户名，列表中不存在的鉴权请求将被直接拒绝。默认值为 null。
  client-allowed-user = ["test"]
  ```

- 使用 cli 时，cdc 按照以下顺序读取客户端鉴权配置：
  1. 通过命令行参数 `--user` 和 `--password` 指定用于鉴权的用户名和密码。
  2. 通过命令行参数 `--user` 指定用于鉴权的用户名，之后可以通过终端输入密码。
  3. 通过环境变量 `TICDC_USER` 和`TICDC_PASSWORD` 配置用于鉴权的用户名和密码。
  4. 通过共享凭证文件 `~/.ticdc/credentials` 获取用于鉴权的用户名和密码。你可以通过命令 `cdc cli configure-credentials` 更改这个文件的配置。

- 使用 curl 命令访问 api 时：
  - 通过 `--user <user>:<password>` 指定用于鉴权的用户名和密码。
