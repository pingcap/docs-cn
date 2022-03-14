---
title: 为 DM 的连接开启加密传输
summary: 了解如何为 DM 的连接开启加密传输。
---

# 为 DM 的连接开启加密传输

本文介绍如何为 DM 的连接开启加密传输，包括 DM-master，DM-worker，dmctl 组件之间的连接以及 DM 组件与上下游数据库之间的连接。

## 为 DM-master，DM-worker，dmctl 组件之间的连接开启加密传输

本节介绍如何为 DM-master，DM-worker，dmctl 组件之间的连接开启加密传输。

### 配置开启加密传输

1. 准备证书。

    推荐为 DM-master、DM-worker 分别准备一个 Server 证书，并保证可以相互验证，而 dmctl 工具则可选择共用 Client 证书。

    有多种工具可以生成自签名证书，如 `openssl`，`cfssl` 及 `easy-rsa` 等基于 `openssl` 的工具。

    这里提供一个使用 `openssl` 生成证书的示例：[生成自签名证书](/dm/dm-generate-self-signed-certificates.md)。

2. 配置证书。

    > **注意：**
    >
    > DM-master、DM-worker 与 dmctl 三个组件可使用同一套证书。

    - DM-master

        在 DM-master 配置文件或命令行参数中设置：

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/master-cert.pem"
        ssl-key = "/path/to/master-key.pem"
        ```

    - DM-worker

        在 DM-worker 配置文件或命令行参数中设置：

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/worker-cert.pem"
        ssl-key = "/path/to/worker-key.pem"
        ```

    - dmctl
    
        若 DM 集群各个组件间开启加密传输后，在使用 dmctl 工具连接集群时，需要指定 Client 证书，示例如下：

        {{< copyable "shell-regular" >}}

        ```bash
        ./dmctl --master-addr=127.0.0.1:8261 --ssl-ca /path/to/ca.pem --ssl-cert /path/to/client-cert.pem --ssl-key /path/to/client-key.pem
        ```

### 认证组件调用者身份

通常被调用者除了校验调用者提供的密钥、证书和 CA 有效性外，还需要校验调用者身份以防止拥有有效证书的非法访问者进行访问（例如：DM-worker 只能被 DM-master 访问，需阻止拥有合法证书但非 DM-master 的其他访问者访问 DM-worker）。

如希望进行组件调用者身份认证，需要在生成证书时通过 `Common Name` (CN) 标识证书使用者身份，并在被调用者配置检查证书 `Common Name` 列表时检查调用者身份。

- DM-master

    在 `config` 文件或命令行参数中设置：

    ```toml
    cert-allowed-cn = ["dm"] 
    ```

- DM-worker

    在 `config` 文件或命令行参数中设置：

    ```toml
    cert-allowed-cn = ["dm"] 
    ```

### 证书重加载

DM-master、DM-worker 和 dmctl 都会在每次新建相互通讯的连接时重新读取当前的证书和密钥文件内容，实现证书和密钥的重加载。

当 `ssl-ca`、`ssl-cert` 或 `ssl-key` 的文件内容更新后，可通过重启 DM 组件使其重新加载证书与密钥内容并重新建立连接。

## DM 组件与上下游数据库之间的连接开启加密传输

本节介绍如何为 DM 组件与上下游数据库之间的连接开启加密传输。

### 为上游数据库连接开启加密传输

1. 配置上游数据库，启用加密连接支持并设置 Server 证书，具体可参考 [Using encrypted connections](https://dev.mysql.com/doc/refman/5.7/en/using-encrypted-connections.html)

2. 在 source 配置文件中设置 MySQL Client 证书：

    > **注意：**
    >
    > 请确保所有 DM-master 与 DM-worker 组件能通过指定路径读取到证书与密钥文件的内容。

    ```yaml
    from:
        security:
            ssl-ca: "/path/to/mysql-ca.pem"
            ssl-cert: "/path/to/mysql-client-cert.pem"
            ssl-key: "/path/to/mysql-client-key.pem"
    ```

### 为下游 TiDB 连接开启加密传输

1. 配置下游 TiDB 启用加密连接支持，具体可参考 [配置 TiDB 启用加密连接支持](/enable-tls-between-clients-and-servers.md#配置-tidb-服务端启用安全连接)

2. 在 task 配置文件中设置 TiDB Client 证书：

    > **注意：**
    >
    > 请确保所有 DM-master 与 DM-worker 组件能通过指定路径读取到证书与密钥文件的内容。

    ```yaml
    target-database:
        security:
            ssl-ca: "/path/to/tidb-ca.pem"
            ssl-cert: "/path/to/tidb-client-cert.pem"
            ssl-key: "/path/to/tidb-client-key.pem"
    ```
