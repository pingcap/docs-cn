---
title: 为 TiDB 组件间通信开启加密传输
summary: 了解如何为 TiDB 集群内各组件间开启加密传输。
aliases: ['/docs-cn/dev/enable-tls-between-components/','/docs-cn/dev/how-to/secure/enable-tls-between-components/']
---

# 为 TiDB 组件间通信开启加密传输

本部分介绍如何为 TiDB 集群内各组件间开启加密传输。一旦开启，以下组件间均将使用加密传输：

- TiDB、TiKV、PD、TiFlash 之间的通讯
- TiDB Control 与 TiDB，TiKV Control 与 TiKV，PD Control 与 PD
- TiKV、PD、TiDB、TiFlash 各自集群内内部通讯

目前暂不支持只开启其中部分组件的加密传输。

## 配置开启加密传输

1. 准备证书。

    推荐为 TiDB、TiKV、PD 分别准备一个 Server 证书，并保证可以相互验证，而它们的 Control 工具则可选择共用 Client 证书。

    有多种工具可以生成自签名证书，如 `openssl`，`easy-rsa`，`cfssl`。

    这里提供一个使用 `openssl` 生成证书的示例：[生成自签名证书](/generate-self-signed-certificates.md)。

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

    - TiFlash（从 v4.0.5 版本开始引入）

        在 `tiflash.toml` 文件中设置,

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs. if set, following four settings shouldn't be empty
        ca_path = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format.
        cert_path = "/path/to/tiflash-server.pem"
        # Path of file that contains X509 key in PEM format.
        key_path = "/path/to/tiflash-server-key.pem"
        ```

        在 `tiflash-learner.toml` 文件中设置，

        ```toml
        [security]
        # Sets the path for certificates. The empty string means that secure connections are disabled.
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/tiflash-server.pem"
        key-path = "/path/to/tiflash-server-key.pem"
        ```

    - TiCDC

        在 `config` 文件中设置

        ```toml
        [security]
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/cdc-server.pem"
        key-path = "/path/to/cdc-server-key.pem"
        ```

        或者在启动命令行中设置，并设置相应的 URL 为 `https`：

        {{< copyable "shell-regular" >}}

        ```bash
        cdc server --pd=https://127.0.0.1:2379 --log-file=ticdc.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301 --ca=/path/to/ca.pem --cert=/path/to/ticdc-cert.pem --key=/path/to/ticdc-key.pem
        ```

    此时 TiDB 集群各个组件间已开启加密传输。

    > **注意：**
    >
    > 若 TiDB 集群各个组件间开启加密传输后，在使用 tidb-ctl、tikv-ctl 或 pd-ctl 工具连接集群时，需要指定 client 证书，示例：

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-ctl -u https://127.0.0.1:10080 --ca /path/to/ca.pem --ssl-cert /path/to/client.pem --ssl-key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    tiup ctl:v<CLUSTER_VERSION> pd -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

## 认证组件调用者身份

通常被调用者除了校验调用者提供的密钥、证书和 CA 有效性外，还需要通过 `Common Name` 校验调用方身份以防止拥有有效证书的非法访问者进行访问（例如：TiKV 只能被 TiDB 访问，需阻止拥有合法证书但非 TiDB 的其他访问者访问 TiKV）。

如希望对组件调用方进行身份认证，需要在生成证书时通过 `Common Name` 标识证书调用方身份，并在被调用者的配置文件中配置 `cluster-verify-cn` (TiDB 组件）或 `cert-allowed-cn`（其它组件）来检查调用方身份。

> **注意：**
>
> - 从 v8.4.0 起，PD 的 `cert-allowed-cn` 配置项支持设置多个值。你可以根据需要在 TiDB 的 `cluster-verify-cn` 配置项以及其它组件的 `cert-allowed-cn` 配置项中设置多个 `Common Name`。需要额外注意的是，TiUP 在查询组件状态的时候会使用独立的标识，比如集群名是 `test`，它会使用 `test-client` 作为 `Common Name`。
> - 对于 v8.3.0 及之前版本，PD 的 `cert-allowed-cn` 配置项只能设置一个值。因此，所有认证对象的 `Common Name` 必须设置成同一个值。相关配置示例可参见 [v8.3.0 文档](https://docs.pingcap.com/zh/tidb/v8.3/enable-tls-between-components)。

- TiDB

    在 `config` 文件或命令行参数中设置：

    ```toml
    [security]
    cluster-verify-cn = ["tidb", "test-client", "prometheus"]
    ```

- TiKV

    在 `config` 文件或命令行参数中设置：

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "pd", "tikv", "tiflash", "prometheus"]
    ```

- PD

    在 `config` 文件或命令行参数中设置：

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "pd", "tikv", "tiflash", "test-client", "prometheus"]
    ```

- TiFlash（从 v4.0.5 版本开始引入）

    在 `tiflash.toml` 文件中设置：

    ```toml
    [security]
    cert_allowed_cn = ["tidb", "tikv", "prometheus"]
    ```

    在 `tiflash-learner.toml` 文件中设置：

    ```toml
    [security]
    cert-allowed-cn = ["tidb", "tikv", "tiflash", "prometheus"]
    ```

## 证书重新加载

- 如果 TiDB 集群部署在本地的数据中心，TiDB、PD、TiKV、TiFlash、TiCDC 和各种 client 在每次新建相互通讯的连接时都会重新读取当前的证书和密钥文件内容，实现证书和密钥的重新加载，无需重启 TiDB 集群。
- 如果 TiDB 集群部署在自己管理的 Cloud，TLS 证书的签发需要与云服务商的证书管理服务集成，TiDB、PD、TiKV、TiFlash、TiCDC 组件的 TLS 证书支持自动轮换，无需重启 TiDB 集群。

## 证书有效期

你可以自定义 TiDB 集群中各组件 TLS 证书的有效期。例如，使用 OpenSSL 签发生成 TLS 证书时，可以通过 **days** 参数设置有效期，详见[生成自签名证书](/generate-self-signed-certificates.md)。

## 另请参阅

- [为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)
