---
title: 开启TLS验证
category: deployment
---

# 开启TLS验证

## 概述

本文档介绍 TIDB 集群如何开启 TLS 验证，其支持

- TIDB组件之间的双向验证，包括 TiDB、TiKV、PD 相互之间， TiKV Control 与 TiKV、PD Control 与 PD 的双向认证，以及 TiKV peer 之间、 PD peer 之间。一旦开启，所有组件之间均使用验证，不支持只开启某一部分的验证。
- MySQL Client 与 TiDB 之间的客户端对服务器身份的单向验证以及双向验证。

MySQL Client 与 TiDB 之间使用一套证书，TiDB 集群组件之间使用另外一套证书。



## TiDB 集群组件间开启 TLS（双向认证）

###准备证书

在这里，使用 cfssl 来自建 CA 签发证书。

####下载 cfssl

这里假设使用的是 x86_64 Linux 主机

```bash
mkdir ~/bin
curl -s -L -o ~/bin/cfssl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
curl -s -L -o ~/bin/cfssljson https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x ~/bin/{cfssl,cfssljson}
export PATH=$PATH:~/bin
```

####初始化证书颁发机构

生成默认的 cfssl 配置，方便之后的修改

```bash
mkdir ~/cfssl
cd ~/cfssl
cfssl print-defaults config > ca-config.json
cfssl print-defaults csr > ca-csr.json
```

####生成证书

##### 证书介绍

- tidb-client certificate 用于通过 TiDB 验证客户端。例如`benchdb`，`benchkv`，`benchraw`
- tidb-server certificate 由 TiDB 使用，为其他组件和客户端验证 TiDB 身份。
- tikv-client certificate 用于通过 TiKV 验证客户端。例如`tikv-ctl`
- tikv-server certificate 由 TiKV 使用，为其他组件和客户端验证 TiKV 身份。
- pd-client certificate 用于通过 PD 验证客户端。例如`pd-ctl`，`pd-recover`，`pd-tso-bench`
- pd-server certificate 由 PD 使用，为其他组件和客户端验证 PD 身份。

##### 配置 CA 选项

修改`ca-config.json`：

```
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
                    "server auth"
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

修改`ca-csr.json`

```
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

生成CA证书

```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
```

将会生成以下几个文件：

```Bash
ca-key.pem
ca.csr
ca.pem
```

##### 生成服务器端证书

```bash
echo '{"CN":"tidb-server","hosts":["127.0.0.1"],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="127.0.0.1" - | cfssljson -bare tidb-server

echo '{"CN":"tikv-server","hosts":["127.0.0.1"],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="127.0.0.1" - | cfssljson -bare tikv-server

echo '{"CN":"pd-server","hosts":["127.0.0.1"],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="127.0.0.1" - | cfssljson -bare pd-server
```

将会生成以下几个文件：

```
tidb-server-key.pem     tikv-server-key.pem      pd-server-key.pem
tidb-server.csr         tikv-server.csr          pd-server.csr
tidb-server.pem         tikv-server.pem          pd-server.pem
```

##### 生成客户端证书

```bash
echo '{"CN":"tidb-client","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client -hostname="" - | cfssljson -bare tidb-client

echo '{"CN":"tikv-client","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client -hostname="" - | cfssljson -bare tikv-client

echo '{"CN":"pd-client","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client -hostname="" - | cfssljson -bare pd-client
```

将会生成以下几个文件：

```bash
tidb-client-key.pem     tikv-client-key.pem      pd-client-key.pem
tidb-client.csr         tikv-client.csr          pd-client.csr
tidb-client.pem         tikv-client.pem          pd-client.pem
```

### 配置证书

##### TiDB

在 config 文件或命令行参数中设置

```toml
[security]
# Path of file that contains list of trusted SSL CAs for connection with cluster components.
cluster-ssl-ca = "/path/to/ca.pem"
# Path of file that contains X509 certificate in PEM format for connection with cluster components.
cluster-ssl-cert = "/path/to/tidb-server.pem"
# Path of file that contains X509 key in PEM format for connection with cluster components.
cluster-ssl-key = "/path/to/tidb-server-key.pem"
```

##### TiKV

在 config 文件或命令行参数中设置，并设置相应 url 为 https

```toml
[security]
# set the path for certificates. Empty string means disabling secure connectoins.
ca-path = "/path/to/ca.pem"
cert-path = "/path/to/tikv-client.pem"
key-path = "/path/to/tikv-client-key.pem"
```

##### PD

在 config 文件或命令行参数中设置，并设置相应 url 为 https

```toml
[security]
# Path of file that contains list of trusted SSL CAs. if set, following four settings shouldn't be empty
cacert-path = "/path/to/ca.pem"
# Path of file that contains X509 certificate in PEM format.
cert-path = "/path/to/server.pem"
# Path of file that contains X509 key in PEM format.
key-path = "/path/to/server-key.pem"
```

此时 TiDB 集群各个组件间便开启了双向验证

在使用客户端连接时，需要指定 client 证书， 示例：

```bash
./pd-ctl -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/pd-client.pem --key /path/to/pd-client-key.pem

./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/tikv-client.pem" --key-path="/path/to/tikv-clinet-key.pem"
```



## MySQL 与 TiDB 间开启 TLS

###准备证书

```bash
mysql_ssl_rsa_setup --datadir=certs
```

### 配置单向认证

在 TiDB 的 config 文件或命令行参数中设置

```toml
[security]
# Path of file that contains list of trusted SSL CAs.
ssl-ca = ""
# Path of file that contains X509 certificate in PEM format.
ssl-cert = "/path/to/certs/server.pem"
# Path of file that contains X509 key in PEM format.
ssl-key = "/path/to/certs/server-key.pem"
```

客户端

```bash
mysql -u root --host 127.0.0.1 --port 4000 --ssl-mode=REQUIRED
```



### 配置双向认证

在 TiDB 的 config 文件或命令行参数中设置

```toml
[security]
# Path of file that contains list of trusted SSL CAs for connection with mysql client.
ssl-ca = "/path/to/certs/ca.pem"
# Path of file that contains X509 certificate in PEM format for connection with mysql client.
ssl-cert = "/path/to/certs/server.pem"
# Path of file that contains X509 key in PEM format for connection with mysql client.
ssl-key = "/path/to/certs/server-key.pem"
```

客户端

```bash
mysql -u root --host 127.0.0.1 --port 4000 --ssl-cert=/path/to/certs/client-cert.pem --ssl-key=/path/to/certs/client-key.pem --ssl-ca=/path/to/certs/ca.pem --ssl-mode=VERIFY_IDENTITY
```



