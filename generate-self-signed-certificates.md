---
title: 生成自签名证书
---

# 生成自签名证书

本文档提供使用 `openssl` 生成自签名证书的一个示例，用户也可以根据自己的需求生成符合要求的证书和密钥。

假设实例集群拓扑如下：

| Name  | Host IP      | Services   |
| ----- | -----------  | ---------- |
| node1 | 172.16.10.11 | PD1, TiDB1 |
| node2 | 172.16.10.12 | PD2        |
| node3 | 172.16.10.13 | PD3        |
| node4 | 172.16.10.14 | TiKV1      |
| node5 | 172.16.10.15 | TiKV2      |
| node6 | 172.16.10.16 | TiKV3      |

## 安装 OpenSSL

对于 Debian 或 Ubuntu 操作系统：

{{< copyable "shell-regular" >}}

```bash
apt install openssl
```

对于 RedHat 或 CentOS 操作系统：

{{< copyable "shell-regular" >}}

```bash
yum install openssl
```

也可以参考 OpenSSL 官方的[下载文档](https://www.openssl.org/source/)进行安装。

## 生成 CA 证书

CA 的作用是签发证书。实际情况中，请联系你的管理员签发证书或者使用信任的 CA 机构。CA 会管理多个证书对，这里只需生成原始的一对证书，步骤如下：

1. 生成 root 密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl genrsa -out root.key 4096
    ```

2. 生成 root 证书：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl req -new -x509 -days 1000 -key root.key -out root.crt
    ```

3. 验证 root 证书：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -text -in root.crt -noout
    ```

## 签发各个组件的证书

### 集群中可能使用到的证书

- tidb certificate 由 TiDB 使用，为其他组件和客户端验证 TiDB 身份。
- tikv certificate 由 TiKV 使用，为其他组件和客户端验证 TiKV 身份。
- pd certificate 由 PD 使用，为其他组件和客户端验证 PD 身份。
- client certificate 用于 PD、TiKV、TiDB 验证客户端。例如 `pd-ctl`，`tikv-ctl` 等。

### 给 TiKV 实例签发证书

给 TiKV 实例签发证书的步骤如下：

1. 生成该证书对应的私钥：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl genrsa -out tikv.key 2048
    ```

2. 拷贝一份 OpenSSL 的配置模板文件。

    模板文件可能存在多个位置，请以实际位置为准：

    {{< copyable "shell-regular" >}}

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    如果不知道实际位置，请在根目录下查找：

    ```bash
    find / -name openssl.cnf
    ```

3. 编辑 `openssl.cnf`，在 `[ req ]` 字段下加入 `req_extensions = v3_req`，然后在 `[ v3_req ]` 字段下加入 `subjectAltName = @alt_names`。最后新建一个字段，并编辑 SAN 的信息：

    ```
    [ alt_names ]
    IP.1 = 127.0.0.1
    IP.2 = 172.16.10.14
    IP.3 = 172.16.10.15
    IP.4 = 172.16.10.16
    ```

4. 保存 `openssl.cnf` 文件后，生成证书请求文件（在这一步也可以为该证书指定 Common Name，其作用是让服务端验证接入的客户端的身份，各个组件默认不会开启验证，需要在配置文件中启用该功能才生效）：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl req -new -key tikv.key -out tikv.csr -config openssl.cnf
    ```

5. 签发生成证书：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in tikv.csr -out tikv.crt -extensions v3_req -extfile openssl.cnf
    ```

6. 验证证书携带 SAN 字段信息（可选）：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -text -in tikv.crt -noout
    ```

7. 确认在当前目录下得到如下文件：

    ```
    root.crt
    tikv.crt
    tikv.key
    ```

为其它 TiDB 组件签发证书的过程类似，此文档不再赘述。

### 为客户端签发证书

为客户端签发证书的步骤如下。

1. 生成该证书对应的私钥：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl genrsa -out client.key 2048
    ```

2. 生成证书请求文件（在这一步也可以为该证书指定 Common Name，其作用是让服务端验证接入的客户端的身份，默认不会开启对各个组件的验证，需要在配置文件中启用该功能才生效）

    {{< copyable "shell-regular" >}}

    ```bash
    openssl req -new -key client.key -out client.csr
    ```

3. 签发生成证书：

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in client.csr -out client.crt
    ```
