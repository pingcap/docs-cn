---
title: 为 TiDB 组件间开启 TLS 和数据加密存储
category: how-to
---

# 为 TiDB 组件间开启 TLS 和数据加密存储

本文档介绍 TiDB 集群如何开启 TLS 验证和数据加密存储。

## 开启 TLS 验证

本部分介绍 TiDB 集群如何开启 TLS 验证，TLS 验证支持：

- TiDB 组件之间的双向验证，包括 TiDB、TiKV、PD 相互之间，TiKV Control 与 TiKV、PD Control 与 PD 的双向认证，以及 TiKV peer 之间、PD peer 之间。一旦开启，所有组件之间均使用验证，不支持只开启某一部分的验证。
- MySQL Client 与 TiDB 之间的客户端对服务器身份的单向验证以及双向验证。

MySQL Client 与 TiDB 之间使用一套证书，TiDB 集群组件之间使用另外一套证书。

### TiDB 集群组件间开启 TLS（双向认证）

1. 准备证书。

    推荐为 TiDB、TiKV、PD 分别准备一个 server 证书，并保证可以相互验证，而它们的各种客户端共用 client 证书。

    有多种工具可以生成自签名证书，如 `openssl`，`easy-rsa`，`cfssl`。

    这里提供一个使用 `cfssl` 生成证书的示例：[生成自签名证书](/how-to/secure/generate-self-signed-certificates.md)。

2. 配置证书。

    - TiDB

        在 `config` 文件或命令行参数中设置：

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs for connection with cluster components.
        cluster-ssl-ca = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format for connection with cluster components.
        cluster-ssl-cert = "/path/to/tidb-server.pem"
        # Path of file that contains X509 key in PEM format for connection with cluster components.
        cluster-ssl-key = "/path/to/tidb-server-key.pem"
        ```

    - TiKV

        在 `config` 文件或命令行参数中设置，并设置相应的 URL 为 https：

        ```toml
        [security]
        # set the path for certificates. Empty string means disabling secure connectoins.
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/tikv-server.pem"
        key-path = "/path/to/tikv-server-key.pem"
        ```

    - PD

        在 `config` 文件或命令行参数中设置，并设置相应的 URL 为 https：

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs. if set, following four settings shouldn't be empty
        cacert-path = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format.
        cert-path = "/path/to/pd-server.pem"
        # Path of file that contains X509 key in PEM format.
        key-path = "/path/to/pd-server-key.pem"
        ```

    此时 TiDB 集群各个组件间已开启双向验证。

    > **注意：**
    >
    > 若 TiDB 集群各个组件间已开启 TLS，在使用 tikv-ctl 或 pd-ctl 工具连接集群时，需要指定 client 证书，示例：

    ```bash
    ./pd-ctl -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem

    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

### MySQL 与 TiDB 间开启 TLS

请参考 [使用加密连接](/how-to/secure/enable-tls-clients.md)。

## 开启数据加密存储

在 TiDB 集群中，用户的数据都存储在 TiKV 中，配置了 TiKV 数据加密存储功能，就代表 TiDB 集群已经加密存储了用户的数据。本部分主要介绍如何配置 TiKV 的加密存储功能。

### 操作流程

1. 生成 token 文件。

    token 文件存储的是密钥，用于对用户数据进行加密，以及对已加密的数据进行解密。

    ```bash
    ./tikv-ctl random-hex --len 256 > cipher-file-256
    ```

    > **注意：**
    >
    > TiKV 只接受 hex 格式的 token 文件，文件的长度必须是 2^n，并且小于等于 1024。

2. 配置 TiKV。

    ```toml
    [security]
    # Cipher file 的存储路径
    cipher-file = "/path/to/cipher-file-256"
    ```

> **注意：**
>
> 若使用 [Lightning](/reference/tools/tidb-lightning/overview.md) 向集群导入数据，如果目标集群开启了加密功能，Lightning 生成的 sst 文件也必须是加密的格式。

### 使用限制

目前 TiKV 数据加密存储存在以下限制：

- 对之前没有开启加密存储的集群，不支持开启该功能。
- 已经开启加密功能的集群，不允许关闭加密存储功能。
- 同一集群内部，不允许部分 TiKV 实例开启该功能，部分 TiKV 实例不开启该功能。对于加密存储功能，所有 TiKV 实例要么都开启该功能，要么都不开启该功能。这是由于 TiKV 实例之间会有数据迁移，如果开启了加密存储功能，迁移过程中数据也是加密的。
