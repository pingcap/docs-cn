---
title: Enable TLS Authentication
summary: Learn how to enable TLS authentication in a TiDB cluster.
category: how-to
aliases: ['/docs/op-guide/security/']
---

# Enable TLS Authentication

## Overview

This document describes how to enable TLS authentication in the TiDB cluster. The TLS authentication includes the following two conditions:

- The mutual authentication between TiDB components, including the authentication among TiDB, TiKV and PD, between TiKV Control and TiKV, between PD Control and PD, between TiKV peers, and between PD peers. Once enabled, the mutual authentication applies to all components, and it does not support applying to only part of the components.
- The one-way and mutual authentication between the TiDB server and the MySQL Client.

> **Note:**
>
> The authentication between the MySQL Client and the TiDB server uses one set of certificates, while the authentication among TiDB components uses another set of certificates.

## Enable mutual TLS authentication among TiDB components

### Prepare certificates

It is recommended to prepare a separate server certificate for TiDB, TiKV and PD, and make sure that they can authenticate each other. The clients of TiDB, TiKV and PD share one client certificate.

You can use multiple tools to generate self-signed certificates, such as `openssl`, `easy-rsa` and `cfssl`.

See an example of [generating self-signed certificates](/v3.0/how-to/secure/generate-self-signed-certificates.md) using `cfssl`.

### Configure certificates

To enable mutual authentication among TiDB components, configure the certificates of TiDB, TiKV and PD as follows.

#### TiDB

Configure in the configuration file or command line arguments:

```toml
[security]
# Path of file that contains list of trusted SSL CAs for connection with cluster components.
cluster-ssl-ca = "/path/to/ca.pem"
# Path of file that contains X509 certificate in PEM format for connection with cluster components.
cluster-ssl-cert = "/path/to/tidb-server.pem"
# Path of file that contains X509 key in PEM format for connection with cluster components.
cluster-ssl-key = "/path/to/tidb-server-key.pem"
```

#### TiKV

Configure in the configuration file or command line arguments, and set the corresponding URL to https:

```toml
[security]
# set the path for certificates. Empty string means disabling secure connections.
ca-path = "/path/to/ca.pem"
cert-path = "/path/to/tikv-server.pem"
key-path = "/path/to/tikv-server-key.pem"
```

#### PD

Configure in the configuration file or command line arguments, and set the corresponding URL to https:

```toml
[security]
# Path of file that contains list of trusted SSL CAs. If set, following four settings shouldn't be empty
cacert-path = "/path/to/ca.pem"
# Path of file that contains X509 certificate in PEM format.
cert-path = "/path/to/pd-server.pem"
# Path of file that contains X509 key in PEM format.
key-path = "/path/to/pd-server-key.pem"
```

Now mutual authentication among TiDB components is enabled.

When you connect the server using the client, it is required to specify the client certificate. For example:

```bash
./pd-ctl -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem

./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
```

## Enable TLS authentication between the MySQL client and TiDB server

See [Use Encrypted Connections](/v3.0/how-to/secure/enable-tls-clients.md).
