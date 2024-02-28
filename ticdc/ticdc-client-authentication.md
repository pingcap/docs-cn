---
title: TiCDC 客户端鉴权
summary: 了解 TiCDC cli 和 api 的鉴权方式。
---

# TiCDC 客户端鉴权

> **注意：**
>
> TiCDC 只支持在开启 tls 加密时进行客户端鉴权。

## 通过 mtls 进行客户端鉴权

1. 使用 cli 时，cdc 按照以下顺序读取客户端证书：
- 通过命令行参数 `--cert` 和 `--key` 指定用于鉴权的证书和私钥。如果服务端使用了自签名证书，还需要通过 `--ca` 指定受信任的 CA 证书。
- 通过环境变量 `TICDC_CA_PATH`、`TICDC_CERT_PATH`、`TICDC_KEY_PATH` 配置客户端证书。
- 通过共享凭证文件 `~/.ticdc/credentials` 获取客户端证书。你可以通过命令 `cdc cli configure-credentials` 更改这个文件的配置。

2. 使用 curl 命令访问 api 时：通过 `--cert` 和 `--key` 指定客户端证书。如果服务端使用了自签名证书，还需要通过 `--cacert` 指定受信任的 CA 证书。


## 通过 TiDB 用户进行客户端鉴权

1. 使用 cli 时，cdc 按照以下顺序读取客户端鉴权配置：
- 通过命令行参数 `--user` 和 `--password` 指定用于鉴权的用户名和密码。
- 通过命令行参数 `--user` 指定用于鉴权的用户名，之后可以通过终端输入密码。
- 通过环境变量 `TICDC_USER` 和`TICDC_PASSWORD` 配置用于鉴权的用户名和密码。
- 通过共享凭证文件 `~/.ticdc/credentials` 获取用于鉴权的用户名和密码。你可以通过命令 `cdc cli configure-credentials` 更改这个文件的配置。

2. 使用 curl 命令访问 api 时：通过 `--user <user>:<password>` 指定用于鉴权的用户名和密码。
