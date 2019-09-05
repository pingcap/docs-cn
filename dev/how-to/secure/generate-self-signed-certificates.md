---
title: 生成自签名证书
category: how-to
---

# 生成自签名证书

## 概述

本文档提供使用 `cfssl` 生成自签名证书的示例。

假设实例集群拓扑如下：

| Name  | Host IP     | Services   |
| ----- | ----------- | ---------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3        |
| node4 | 172.16.10.4 | TiKV1      |
| node5 | 172.16.10.5 | TiKV2      |
| node6 | 172.16.10.6 | TiKV3      |

## 下载 cfssl

假设使用 x86_64 Linux 主机：

```bash
mkdir ~/bin
curl -s -L -o ~/bin/cfssl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
curl -s -L -o ~/bin/cfssljson https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x ~/bin/{cfssl,cfssljson}
export PATH=$PATH:~/bin
```

## 初始化证书颁发机构

生成 cfssl 的默认配置，以便于之后修改：

```bash
mkdir ~/cfssl
cd ~/cfssl
cfssl print-defaults config > ca-config.json
cfssl print-defaults csr > ca-csr.json
```

## 生成证书

### 证书介绍

- tidb-server certificate 由 TiDB 使用，为其他组件和客户端验证 TiDB 身份。
- tikv-server certificate 由 TiKV 使用，为其他组件和客户端验证 TiKV 身份。
- pd-server certificate 由 PD 使用，为其他组件和客户端验证 PD 身份。
- client certificate 用于通过 PD、TiKV、TiDB 验证客户端。例如 `pd-ctl`，`tikv-ctl`，`pd-recover`。

### 配置 CA 选项

根据实际需求修改 `ca-config.json`：

```json
{
    "signing": {
        "default": {
            "expiry": "43800h"
        },
        "profiles": {
            "server": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth",
                    "client auth"
                ]
            },
            "client": {
                "expiry": "43800h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            }
        }
    }
}
```

根据实际需求修改 `ca-csr.json` ：

```json
{
    "CN": "My own CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "L": "Beijing",
            "O": "PingCAP",
            "ST": "Beijing"
        }
    ]
}
```

### 生成 CA 证书

```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
```

将会生成以下几个文件：

```bash
ca-key.pem
ca.csr
ca.pem
```

### 生成服务器端证书

`hostname` 中为各组件的 IP 地址，以及 `127.0.0.1`

```bash
echo '{"CN":"tidb-server","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="172.16.10.1,172.16.10.2,127.0.0.1" - | cfssljson -bare tidb-server

echo '{"CN":"tikv-server","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="172.16.10.4,172.16.10.5,172.16.10.6,127.0.0.1" - | cfssljson -bare tikv-server

echo '{"CN":"pd-server","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="172.16.10.1,172.16.10.2,172.16.10.3,127.0.0.1" - | cfssljson -bare pd-server
```

将会生成以下几个文件：

```Bash
tidb-server-key.pem     tikv-server-key.pem      pd-server-key.pem
tidb-server.csr         tikv-server.csr          pd-server.csr
tidb-server.pem         tikv-server.pem          pd-server.pem
```

### 生成客户端证书

```bash
echo '{"CN":"client","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client -hostname="" - | cfssljson -bare client
```

将会生成以下几个文件：

```bash
client-key.pem
client.csr
client.pem
```
