---
title: 生成自签名证书
category: how-to
aliases: ['/docs-cn/dev/how-to/secure/generate-self-signed-certificates/']
---

# 生成自签名证书

## 概述

本文档仅提供使用 `openssl` 生成自签名证书的一个示例，用户也可以根据自己的需求生成符合自己需求的证书和密钥。

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

```bash
apt install openssl
```

对于 RedHat 或 CentOS 操作系统：

```bash
yum install openssl
```

也可以参考 OpenSSL 官方的 [下载文档](https://www.openssl.org/source/) 安装

## 生成 CA 证书

CA 的作用是签发证书，在实际情况里，请联系你的管理员签发证书或者使用信任的 CA 机构。CA 会管理多个证书对，这里只需生成原始的一对证书：

```bash
// 生成 root 密钥
openssl genrsa -out root.key 4096
// 生成 root 证书
openssl req -new -x509 -days 1000 -key root.key -out root.crt
// 验证 root 证书
openssl x509 -text -in root.crt -noout
```

## 签发各个组件的证书

### 集群中可能使用到的证书

- tidb certificate 由 TiDB 使用，为其他组件和客户端验证 TiDB 身份。
- tikv certificate 由 TiKV 使用，为其他组件和客户端验证 TiKV 身份。
- pd certificate 由 PD 使用，为其他组件和客户端验证 PD 身份。
- client certificate 用于 PD、TiKV、TiDB 验证客户端。例如 `pd-ctl`，`tikv-ctl` 等。

### 给 TiKV 实例签发证书

生成该证书对应的私钥：

```bash
openssl genrsa -out tikv.key 2048
```

拷贝一份 OpenSSL 的配置模板文件：

```bash
// 模板文件可能存在多个位置，请以实际位置为准
cp /usr/lib/ssl/openssl.cnf .
// 如果不知道实际位置，请在根目录下查找
find / -name openssl.cnf
```

编辑 `openssl.cnf`，在 `[ req ]` 字段下加入 `req_extensions = v3_req`，然后在 `[ v3_req ]` 字段下加入 `subjectAltName = @alt_names`。最后新建一个字段，并编辑 SAN 的信息：

```
[ alt_names ]
IP.1 = 127.0.0.1
IP.2 = 172.16.10.14
IP.3 = 172.16.10.15
IP.4 = 172.16.10.16
```

保存 `openssl.cnf` 文件后，生成证书请求文件（在这一步也可以为该证书指定 Common Name，其作用是让服务端验证接入的客户端的身份，各个组件默认不会开启验证，需要在配置文件中启用该功能才生效）：

```bash
openssl req -new -key tikv.key -out tikv.csr -config openssl.cnf
```

签发生成证书：

```bash
openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in tikv.csr -out tikv.crt -extensions v3_req -extfile openssl.cnf
```

验证证书携带 SAN 字段信息：

```bash
openssl x509 -text -in tikv.crt -noout
```

如果操作成功，会在当前目录下得到如下文件：

```
root.crt
tikv.crt
tikv.key
```

为其它组件签发证书的过程类似，此文档不再赘述。
