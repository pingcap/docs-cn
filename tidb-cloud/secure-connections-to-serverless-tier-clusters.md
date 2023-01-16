---
title: Secure Connections to Serverless Tier Clusters
summary: Introduce TLS connection in TiDB Serverless Tier clusters.
---

# Secure Connections to Serverless Tier Clusters

This document introduces the core information about TLS in TiDB Serverless Tier.

## Can I disable TLS in TiDB Serverless Tier?

No.

TiDB Serverless Tier allows only TLS connections and rejects non-TLS connections. The reason is that users connect to TiDB Serverless Tier clusters through a public network, so it is really important to use TLS to ensure communication security.

## What TLS versions can I use?

TiDB Serverless Tier supports TLS 1.2 and TLS 1.3. 

TLS 1.0 and TLS 1.1 are not supported due to security reasons. For background information, refer to IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/).

## What certificates do I need？

TiDB Serverless Tier uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless Tier clusters. Usually, the root certificate ([ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt)) of Let's Encrypt is present in your system's root CA stores. If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless Tier clusters without specifying the path of CA roots.

However, some drivers and ORMs do not use the system root CA stores. In those cases, you need to configure the CA root path of the drivers or ORMs to your system root CA stores. For example, when you use [mysqlclient](https://github.com/PyMySQL/mysqlclient) to connect a TiDB Serverless Tier cluster in Python on macOS, you need to set `ca: /etc/ssl/cert.pem` in the `ssl` argument.

> **Note:**
>
> TiDB Serverless Tier does not provide a CA root certificate download, because we don't guarantee that the same CA will be used to issue a certificate in the future, which will cause the CA root certificate to change.
>
> However, TiDB Serverless Tier ensures always using a CA root certificate that is commonly available, which is provided in all common systems.
>
> If you really need the CA certificate of a TiDB Serverless Tier cluster, it is recommended that you download the [Mozilla CA Certificate bundle](https://curl.se/docs/caextract.html) instead of the single CA certificate in case we change the CA in the future.
>
> If you are using a GUI client, such as DBeaver, which does not accept a certificate file with multiple certificates inside, you must download the [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) certificate.

## How do I connect to a TiDB Serverless Tier cluster in TLS connection?

TiDB Cloud provides some connection examples in the **Connect** dialog. You can follow the instructions in [Connect via standard connection](/tidb-cloud/connect-via-standard-connection.md) to connect to a TiDB Serverless Tier cluster.

Generally, enabling TLS and offering a CA root path to authenticate the server is a good practice to prevent a man-in-the-middle attack. Different clients have different operations in the TLS connection. Enable TLS and verify the server according to your actual use of the client.

The following examples show the connection string in MySQL CLI client, MyCLI client, Java, Python, Go, and Node.js:

<SimpleTab>
<div label="MySQL CLI client">

MySQL CLI client attempts to establish TLS connection by default. When you connect to TiDB Serverless Tier clusters, you should set `ssl-mode` and `ssl-ca`.

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL CLI client forces to enable TLS and validate TiDB Serverless Tier clusters.
- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.

</div>

<div label="MyCLI client">

[MyCLI](https://www.mycli.net/) automatically enables TLS when using TLS related parameters. When you connect to TiDB Serverless Tier clusters, you need to set `ssl-ca` and `ssl-verify-server-cert`.

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.
- With `--ssl-verify-server-cert` to validate TiDB Serverless Tier clusters.

</div>

<div label="Java">

[MySQL Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/)'s TLS connection configurations are used here as an example.

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
```

- Set `sslMode=VERIFY_IDENTITY` to enable TLS and validate TiDB Serverless Tier clusters. JDBC trusts system CA root certificates by default, so you do not need to configure certificates.
- Set `enabledTLSProtocols=TLSv1.2,TLSv1.3` to restrict the versions of TLS protocol.

</div>

<div label="Python">

[mysqlclient](https://pypi.org/project/mysqlclient/)'s TLS connection configurations are used here as an example.

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}
```

- Set `ssl_mode="VERIFY_IDENTITY"` to enable TLS and validate TiDB Serverless Tier clusters.
- Set `ssl={"ca": "<CA_root_path>"}` to set the CA root path on your system.

</div>

<div label="Go">

[Go-MySQL-Driver](https://github.com/go-sql-driver/mysql)'s TLS connection configurations are used here as an example.

```
mysql.RegisterTLSConfig("tidb", &tls.Config{
  MinVersion: tls.VersionTLS12,
  ServerName: "<host>",
})

db, err := sql.Open("mysql", "<usename>:<your_password>@tcp(<host>:4000)/test?tls=tidb")
```

- Register `tls.Config` in connection to enable TLS and validate TiDB Serverless Tier clusters. Go-MySQL-Driver uses system CA root certificates by default, so you do not need to configure certificates.
- Set `MinVersion: tls.VersionTLS12` to restrict the versions of TLS protocol.
- Set `ServerName: "<host>"` to verify TiDB Serverless Tier's hostname.
- If you do not want to register a new TLS configuration, you can just set `tls=true` in the connection string.

</div>

<div label="Node.js">

[Mysql2](https://www.npmjs.com/package/mysql2)'s TLS connection configurations are used here as an example.

```
host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {minVersion: 'TLSv1.2', rejectUnauthorized: true}
```

- Set `ssl: {minVersion: 'TLSv1.2'}` to restrict the versions of TLS protocol.
- Set `ssl: {rejectUnauthorized: true}` to validate TiDB Serverless Tier clusters. Mysql2 uses system CA root certificates by default, so you do not need to configure certificates.

</div>
</SimpleTab>

## Where is the CA root path on my system?

The following lists the CA root paths on common platforms.

**MacOS**

```
/etc/ssl/cert.pem
```

**Debian / Ubuntu / Arch**

```
/etc/ssl/certs/ca-certificates.crt
```

**RedHat / Fedora / CentOS / Mageia**

```
/etc/pki/tls/certs/ca-bundle.crt
```

**Alpine**

```
/etc/ssl/cert.pem
```

**OpenSUSE**

```
/etc/ssl/ca-bundle.pem
```

**Windows**

Windows does not offer a specific path to the CA root. Instead, it uses the [registry](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores) to store certificates. For this reason, to specify the CA root path on Windows, take the following steps:

1. Download the [Mozilla CA Certificate bundle](https://curl.se/docs/caextract.html) and save it in a path you prefer, such as `<path_to_mozilla_ca_cert_bundle>`.
2. Use the path (`<path_to_mozilla_ca_cert_bundle>`) as your CA root path when you connect to a Serverless Tier cluster.

## Can TiDB Serverless Tier verify the client's identity?

No.

Currently, TiDB Serverless Tier uses one-way TLS authentication, which means only the client uses the public certificate pair to validate the server while the server does not validate the client. For example, when you use MySQL CLI client, you cannot configure `--ssl-cert` or `--ssl-key` in connection strings.
