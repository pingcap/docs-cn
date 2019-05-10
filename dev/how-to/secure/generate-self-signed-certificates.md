---
title: Generate Self-signed Certificates
summary: Use `cfssl` to generate self-signed certificates.
category: how-to
aliases: ['/docs/op-guide/generate-self-signed-certificates/']
---

# Generate Self-signed Certificates

## Overview

This document describes how to generate self-signed certificates using `cfssl`.

Assume that the topology of the instance cluster is as follows:

| Name  | Host IP     | Services   |
| ----- | ----------- | ---------- |
| node1 | 172.16.10.1 | PD1, TiDB1 |
| node2 | 172.16.10.2 | PD2, TiDB2 |
| node3 | 172.16.10.3 | PD3        |
| node4 | 172.16.10.4 | TiKV1      |
| node5 | 172.16.10.5 | TiKV2      |
| node6 | 172.16.10.6 | TiKV3      |

## Download `cfssl`

Assume that the host is x86_64 Linux:

```bash
mkdir ~/bin
curl -s -L -o ~/bin/cfssl https://pkg.cfssl.org/R1.2/cfssl_linux-amd64
curl -s -L -o ~/bin/cfssljson https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64
chmod +x ~/bin/{cfssl,cfssljson}
export PATH=$PATH:~/bin
```

## Initialize the certificate authority

To make it easy for modification later, generate the default configuration of `cfssl`:

```bash
mkdir ~/cfssl
cd ~/cfssl
cfssl print-defaults config > ca-config.json
cfssl print-defaults csr > ca-csr.json
```

## Generate certificates

### Certificates description

- tidb-server certificate: used by TiDB to authenticate TiDB for other components and clients
- tikv-server certificate: used by TiKV to authenticate TiKV for other components and clients
- pd-server certificate: used by PD to authenticate PD for other components and clients
- client certificate: used to authenticate the clients from PD, TiKV and TiDB, such as `pd-ctl`, `tikv-ctl` and `pd-recover`

### Configure the CA option

Edit `ca-config.json` according to your need:

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

Edit `ca-csr.json` according to your need:

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

### Generate the CA certificate

```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
```

The command above generates the following files:

```bash
ca-key.pem
ca.csr
ca.pem
```

### Generate the server certificate

The IP address of all components and `127.0.0.1` are included in `hostname`.

```bash
echo '{"CN":"tidb-server","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="172.16.10.1,172.16.10.2,127.0.0.1" - | cfssljson -bare tidb-server

echo '{"CN":"tikv-server","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="172.16.10.4,172.16.10.5,172.16.10.6,127.0.0.1" - | cfssljson -bare tikv-server

echo '{"CN":"pd-server","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server -hostname="172.16.10.1,172.16.10.2,172.16.10.3,127.0.0.1" - | cfssljson -bare pd-server
```

The command above generates the following files:

```Bash
tidb-server-key.pem     tikv-server-key.pem      pd-server-key.pem
tidb-server.csr         tikv-server.csr          pd-server.csr
tidb-server.pem         tikv-server.pem          pd-server.pem
```

### Generate the client certificate

```bash
echo '{"CN":"client","hosts":[""],"key":{"algo":"rsa","size":2048}}' | cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client -hostname="" - | cfssljson -bare client
```

The command above generates the following files:

```bash
client-key.pem
client.csr
client.pem
```
