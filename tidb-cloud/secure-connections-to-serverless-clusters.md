---
title: TLS Connections to TiDB Serverless
summary: Introduce TLS connections in TiDB Serverless.
aliases: ['/tidbcloud/secure-connections-to-serverless-tier-clusters']
---

# TLS Connections to TiDB Serverless

Establishing a secure TLS connection between your client and your TiDB Serverless cluster is one of the basic security practices for connecting to your databases. The server certificate for TiDB Serverless is issued by an independent third-party certificate provider. You can easily connect to your TiDB Serverless cluster without downloading a server-side digital certificate.

## Prerequisites

- Log in to TiDB Cloud via [Password Authentication](/tidb-cloud/tidb-cloud-password-authentication.md) or [SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md).
- [Create a TiDB Serverless cluster](/tidb-cloud/tidb-cloud-quickstart.md).

## TLS connection to a TiDB Serverless cluster

In the [TiDB Cloud console](https://tidbcloud.com/), you can get examples of different connection methods and connect to your TiDB Serverless cluster as follows:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project, and then click the name of your cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A dialog is displayed.

3. In the dialog, keep the default setting of the endpoint type as `Public`, and select your preferred connection method and operating system.

    - Supported connection methods: MySQL CLI, MyCLI, JDBC, Python, Go, and Node.js.
    - Supported operating systems: MacOS, Debian, CentOS/RedHat/Fedora, Alpine, OpenSUSE, and Windows.

4. If you have not set a password yet, click **Create password** to generate a random password for your TiDB Serverless cluster. The password will be automatically embedded in the sample connection string for connecting to your cluster easily.

    > **Note:**
    >
    > - The random password consists of 16 characters, including uppercase and lowercase letters, numbers, and special characters.
    > - After you close this dialog, the generated password will not show again, so you need to save the password in a secure location. If you forget it, you can click **Reset password** in this dialog to reset it.
    > - The TiDB Serverless cluster can be accessed through the internet. If you need to use the password elsewhere, it is recommended that you reset it to ensure database security.

5. Connect to your cluster with the connection string.

    > **Note:**
    >
    > When you connect to a TiDB Serverless cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

The following examples show the connection strings in MySQL CLI, MyCLI, JDBC, Python, Go, and Node.js. To learn how to get the `<CA_root_path>` of your operating system, see [Root certificate management](#root-certificate-management).

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI client attempts to establish a TLS connection by default. When you connect to TiDB Serverless clusters, you should set `ssl-mode` and `ssl-ca`.

```shell
mysql --connect-timeout 15 -u <username> -h <host> -P 4000 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_root_path> -D test -p
```

- With `--ssl-mode=VERIFY_IDENTITY`, MySQL CLI client forces to enable TLS and validate TiDB Serverless clusters.
- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) automatically enables TLS when using TLS related parameters. When you connect to TiDB Serverless clusters, you need to set `ssl-ca` and `ssl-verify-server-cert`.

```shell
mycli -u <username> -h <host> -P 4000 -D test --ssl-ca=<CA_root_path> --ssl-verify-server-cert
```

- Use `--ssl-ca=<CA_root_path>` to set the CA root path on your system.
- With `--ssl-verify-server-cert` to validate TiDB Serverless clusters.

</div>

<div label="JDBC">

[MySQL Connector/J](https://dev.mysql.com/doc/connector-j/8.0/en/)'s TLS connection configurations are used here as an example.

```
jdbc:mysql://<host>:4000/test?user=<username>&password=<your_password>&sslMode=VERIFY_IDENTITY&enabledTLSProtocols=TLSv1.2,TLSv1.3
```

- Set `sslMode=VERIFY_IDENTITY` to enable TLS and validate TiDB Serverless clusters. JDBC trusts system CA root certificates by default, so you do not need to configure certificates.
- Set `enabledTLSProtocols=TLSv1.2,TLSv1.3` to restrict the versions of TLS protocol.

</div>

<div label="Python">

[mysqlclient](https://pypi.org/project/mysqlclient/)'s TLS connection configurations are used here as an example.

```
host="<host>", user="<username>", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<CA_root_path>"}
```

- Set `ssl_mode="VERIFY_IDENTITY"` to enable TLS and validate TiDB Serverless clusters.
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

- Register `tls.Config` in connection to enable TLS and validate TiDB Serverless clusters. Go-MySQL-Driver uses system CA root certificates by default, so you do not need to configure certificates.
- Set `MinVersion: tls.VersionTLS12` to restrict the versions of TLS protocol.
- Set `ServerName: "<host>"` to verify TiDB Serverless's hostname.
- If you do not want to register a new TLS configuration, you can just set `tls=true` in the connection string.

</div>

<div label="Node.js">

[Mysql2](https://www.npmjs.com/package/mysql2)'s TLS connection configurations are used here as an example.

```
host: '<host>', port: 4000,user: '<username>', password: '<your_password>', database: 'test', ssl: {minVersion: 'TLSv1.2', rejectUnauthorized: true}
```

- Set `ssl: {minVersion: 'TLSv1.2'}` to restrict the versions of TLS protocol.
- Set `ssl: {rejectUnauthorized: true}` to validate TiDB Serverless clusters. Mysql2 uses system CA root certificates by default, so you do not need to configure certificates.

</div>
</SimpleTab>

## Root certificate management

### Root certificate issuance and validity

TiDB Serverless uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless clusters. Once the TiDB Serverless certificate expires, it will be automatically rotated without affecting the normal operations of your cluster and the established TLS secure connection.

> **Note:**
>
> TiDB Serverless does not provide a CA root certificate download, because we don't guarantee that the same CA will be used to issue a certificate in the future, which will cause the CA root certificate to change.

If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless clusters without specifying the path of CA roots. If you still want to get a CA certificate for a TiDB Serverless cluster, you can download and use the [Mozilla CA Certificate bundle](https://curl.se/docs/caextract.html) instead of a single CA certificate.

However, some drivers and ORMs do not use the system root CA stores. In those cases, you need to configure the CA root path of the drivers or ORMs to your system root CA stores. For example, when you use [mysqlclient](https://github.com/PyMySQL/mysqlclient) to connect a TiDB Serverless cluster in Python on macOS, you need to set `ca: /etc/ssl/cert.pem` in the `ssl` argument.

If you are using a GUI client, such as DBeaver, which does not accept a certificate file with multiple certificates inside, you must download the [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem.txt) certificate.

### Root certificate default path

In different operating systems, the default storage paths of the root certificate are as follows：

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
2. Use the path (`<path_to_mozilla_ca_cert_bundle>`) as your CA root path when you connect to a TiDB Serverless cluster.

## FAQs

### Which TLS versions are supported to connect to my TiDB Serverless cluster?

For security reasons, TiDB Serverless only supports TLS 1.2 and TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions. See IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/) for details.

### Is two-way TLS authentication between my connection client and TiDB Serverless supported?

No.

TiDB Serverless only supports one-way TLS authentication, which means your client uses the public key to verify the signature of your TiDB Cloud cluster certificate's private key while the cluster does not validate the client.

### Does TiDB Serverless have to configure TLS to establish a secure connection?

For standard connection, TiDB Serverless only allows TLS connections and prohibits non-SSL/TLS connections. The reason is that SSL/TLS is one of the most basic security measures for you to reduce the risk of data exposure to the internet when you connect to the TiDB Serverless cluster through the internet.

For private endpoint connection, because it supports highly secure and one-way access to the TiDB Cloud service and does not expose your data to the public internet, configuring TLS is optional.
