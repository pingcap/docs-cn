---
title: TiCDC 客户端鉴权
summary: 介绍使用 TiCDC 命令行工具或通过 OpenAPI 访问 TiCDC 时，如何进行客户端鉴权。
---

# TiCDC 客户端鉴权

从 v8.1.0 起，TiCDC 支持使用 mTLS（双向传输层安全性协议）或 TiDB 用户名密码进行客户端鉴权。

- mTLS 鉴权：在传输层进行安全控制，使 TiCDC 可以验证客户端身份。
- TiDB 用户名密码鉴权：在应用层进行安全控制，确保只有授权用户才能通过 TiCDC 节点登录。

这两种鉴权方式既可以单独使用，也可以结合使用，以满足不同的场景和安全需求。

> **注意：**
>
> 为了保证网络访问的安全性，强烈建议仅在[开启 TLS 加密传输](/enable-tls-between-clients-and-servers.md)的情况下，使用 TiCDC 客户端鉴权功能。如果不开启 TLS 加密传输，用户名和密码将会以明文的方式通过网络传输，这会带来严重的泄露风险。

## 使用 mTLS 进行客户端鉴权

1. 在 TiCDC Server 中，将 `security.mtls` 配置为 `true` 以开启 mTLS 鉴权：

    ```toml
    [security]
    # 控制是否开启 TLS 客户端鉴权，默认值为 false。
    mtls = true
    ```

2. 配置客户端证书。

    <SimpleTab groupId="cdc">
    <div label="TiCDC 命令行工具" value="cdc-cli">

    使用 [TiCDC 命令行工具](/ticdc/ticdc-manage-changefeed.md)时，你可以通过以下方式之一指定客户端证书。TiCDC 将按照以下顺序依次尝试读取客户端证书：

    1. 通过命令行参数 `--cert` 和 `--key` 指定证书和私钥。如果服务端使用了自签名证书，还需要通过 `--ca` 参数指定受信任的 CA 证书：

        ```bash
        cdc cli changefeed list --cert client.crt --key client.key --ca ca.crt
        ```

    2. 通过环境变量 `TICDC_CERT_PATH`、`TICDC_KEY_PATH` 和 `TICDC_CA_PATH` 指定证书、私钥和 CA 证书的路径：

        ```bash
        export TICDC_CERT_PATH=client.crt
        export TICDC_KEY_PATH=client.key
        export TICDC_CA_PATH=ca.crt
        ```

    3. 通过共享凭证文件 `~/.ticdc/credentials` 指定客户端证书。你可以使用 `cdc cli configure-credentials` 命令修改此文件的配置。

    </div>

    <div label="TiCDC OpenAPI" value="cdc-api">

    使用 [TiCDC OpenAPI](/ticdc/ticdc-open-api-v2.md) 时，通过 `--cert` 和 `--key` 指定客户端证书和私钥。如果服务端使用了自签名证书，还需要通过 `--cacert` 指定受信任的 CA 证书。示例：

    ```bash
    curl -X GET http://127.0.0.1:8300/api/v2/status --cert client.crt --key client.key --cacert ca.crt
    ```

    </div>
    </SimpleTab>

## 使用 TiDB 用户名密码进行客户端鉴权

1. 在 TiDB 中[创建用户](/sql-statements/sql-statement-create-user.md)，并授权该用户从 TiCDC 所在节点登录的权限：

    ```sql
    CREATE USER 'test'@'ticdc_ip_address' IDENTIFIED BY 'password';
    ```

2. 在 TiCDC Server 中，配置 `security.client-user-required` 和 `security.client-allowed-user` 以开启用户名和密码鉴权：

    ```toml
    [security]
    # 控制是否使用用户名和密码进行客户端鉴权，默认值为 false。
    client-user-required = true
    # 指定可用于客户端鉴权的用户名，列表中不存在的用户的鉴权请求将被直接拒绝。默认值为 null。
    client-allowed-user = ["test"]
    ```

3. 指定步骤 1 创建的授权用户的用户名和密码。

    <SimpleTab groupId="cdc">
    <div label="TiCDC 命令行工具" value="cdc-cli">

    使用 [TiCDC 命令行工具](/ticdc/ticdc-manage-changefeed.md)时，你可以通过以下方式之一指定用户名和密码。TiCDC 将按照以下顺序依次尝试读取用户名和密码：

    1. 通过命令行参数 `--user` 和 `--password` 指定用于鉴权的用户名和密码：

        ```bash
        cdc cli changefeed list --user test --password password
        ```

    2. 通过命令行参数 `--user` 指定用于鉴权的用户名，然后通过终端输入密码：

        ```bash
        cdc cli changefeed list --user test
        ```

    3. 通过环境变量 `TICDC_USER` 和 `TICDC_PASSWORD` 指定用于鉴权的用户名和密码：

        ```bash
        export TICDC_USER=test
        export TICDC_PASSWORD=password
        ```

    4. 通过共享凭证文件 `~/.ticdc/credentials` 指定用于鉴权的用户名和密码。你可以使用 `cdc cli configure-credentials` 命令修改此文件的配置。

    </div>

    <div label="TiCDC OpenAPI" value="cdc-api">

    使用 [TiCDC OpenAPI](/ticdc/ticdc-open-api-v2.md) 时，通过 `--user <user>:<password>` 指定用于鉴权的用户名和密码。示例：

    ```bash
    curl -X GET http://127.0.0.1:8300/api/v2/status --user test:password
    ```

    </div>
    </SimpleTab>
