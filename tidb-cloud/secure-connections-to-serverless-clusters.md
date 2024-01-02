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

4. If you have not set a password yet, click **Generate Password** to generate a random password for your TiDB Serverless cluster. The password will be automatically embedded in the sample connection string for connecting to your cluster easily.

    > **Note:**
    >
    > - The random password consists of 16 characters, including uppercase and lowercase letters, numbers, and special characters.
    > - After you close this dialog, the generated password will not show again, so you need to save the password in a secure location. If you forget it, you can click **Reset Password** in this dialog to reset it.
    > - The TiDB Serverless cluster can be accessed through the internet. If you need to use the password elsewhere, it is recommended that you reset it to ensure database security.

5. Connect to your cluster with the connection string.

    > **Note:**
    >
    > When you connect to a TiDB Serverless cluster, you must include the prefix for your cluster in the user name and wrap the name with quotation marks. For more information, see [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix).

## Root certificate management

### Root certificate issuance and validity

TiDB Serverless uses certificates from [Let's Encrypt](https://letsencrypt.org/) as a Certificate Authority (CA) for TLS connection between clients and TiDB Serverless clusters. Once the TiDB Serverless certificate expires, it will be automatically rotated without affecting the normal operations of your cluster and the established TLS secure connection.

If the client uses the system's root CA stores by default, such as Java and Go, you can easily connect securely to TiDB Serverless clusters without specifying the path of CA roots. However, some drivers and ORMs do not use the system root CA stores. In those cases, you need to configure the CA root path of the drivers or ORMs to your system root CA stores. For example, when you use [mysqlclient](https://github.com/PyMySQL/mysqlclient) to connect a TiDB Serverless cluster in Python on macOS, you need to set `ca: /etc/ssl/cert.pem` in the `ssl` argument.

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

1. Download the [ISRG Root X1 certificate](https://letsencrypt.org/certs/isrgrootx1.pem.txt) and then save it in a path you prefer, such as `<path_to_ca>`.
2. Use the path (`<path_to_ca>`) as your CA root path when you connect to a TiDB Serverless cluster.

## FAQs

### Which TLS versions are supported to connect to my TiDB Serverless cluster?

For security reasons, TiDB Serverless only supports TLS 1.2 and TLS 1.3, and does not support TLS 1.0 and TLS 1.1 versions. See IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/) for details.

### Is two-way TLS authentication between my connection client and TiDB Serverless supported?

No.

TiDB Serverless only supports one-way TLS authentication, which means your client uses the public key to verify the signature of your TiDB Cloud cluster certificate's private key while the cluster does not validate the client.

### Does TiDB Serverless have to configure TLS to establish a secure connection?

For standard connection, TiDB Serverless only allows TLS connections and prohibits non-SSL/TLS connections. The reason is that SSL/TLS is one of the most basic security measures for you to reduce the risk of data exposure to the internet when you connect to the TiDB Serverless cluster through the internet.

For private endpoint connection, because it supports highly secure and one-way access to the TiDB Cloud service and does not expose your data to the public internet, configuring TLS is optional.
