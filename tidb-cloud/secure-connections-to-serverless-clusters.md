---
title: TiDB Cloud Serverless 的 TLS 连接
summary: 介绍 TiDB Cloud Serverless 中的 TLS 连接。
aliases: ['/tidbcloud/secure-connections-to-serverless-tier-clusters']
---

# TiDB Cloud Serverless 的 TLS 连接

在客户端和 TiDB Cloud Serverless 集群之间建立安全的 TLS 连接是连接数据库的基本安全实践之一。TiDB Cloud Serverless 的服务器证书由独立的第三方证书提供商颁发。您可以轻松连接到 TiDB Cloud Serverless 集群，而无需下载服务器端数字证书。

## 前提条件

- 通过[密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)或 [SSO 认证](/tidb-cloud/tidb-cloud-sso-authentication.md)登录 TiDB Cloud。
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/tidb-cloud-quickstart.md)。

## 连接到 TiDB Cloud Serverless 集群的 TLS 连接

在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，您可以获取不同连接方法的示例，并按以下方式连接到 TiDB Cloud Serverless 集群：

1. 导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击集群名称进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个对话框。

3. 在对话框中，保持连接类型的默认设置为 `Public`，然后选择您首选的连接方法和操作系统。

4. 如果您尚未设置密码，请点击**生成密码**为 TiDB Cloud Serverless 集群生成随机密码。该密码将自动嵌入到示例连接字符串中，以便轻松连接到您的集群。

    > **注意：**
    >
    > - 随机密码由 16 个字符组成，包括大小写字母、数字和特殊字符。
    > - 关闭此对话框后，生成的密码将不再显示，因此您需要将密码保存在安全的位置。如果您忘记了密码，可以在此对话框中点击**重置密码**进行重置。
    > - TiDB Cloud Serverless 集群可以通过互联网访问。如果您需要在其他地方使用密码，建议重置密码以确保数据库安全。

5. 使用连接字符串连接到您的集群。

    > **注意：**
    >
    > 连接到 TiDB Cloud Serverless 集群时，您必须在用户名中包含集群的前缀，并用引号将名称括起来。有关更多信息，请参见[用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

## 根证书管理

### 根证书颁发和有效期

TiDB Cloud Serverless 使用 [Let's Encrypt](https://letsencrypt.org/) 的证书作为证书颁发机构（CA），用于客户端和 TiDB Cloud Serverless 集群之间的 TLS 连接。一旦 TiDB Cloud Serverless 证书过期，它将自动轮换，而不会影响集群的正常运行和已建立的 TLS 安全连接。

如果客户端默认使用系统的根 CA 存储，例如 Java 和 Go，您可以轻松安全地连接到 TiDB Cloud Serverless 集群，而无需指定 CA 根证书的路径。但是，某些驱动程序和 ORM 不使用系统根 CA 存储。在这些情况下，您需要将驱动程序或 ORM 的 CA 根路径配置为系统根 CA 存储。例如，当您在 macOS 上使用 [mysqlclient](https://github.com/PyMySQL/mysqlclient) 连接 TiDB Cloud Serverless 集群时，需要在 `ssl` 参数中设置 `ca: /etc/ssl/cert.pem`。

如果您使用的是不接受包含多个证书的证书文件的 GUI 客户端（如 DBeaver），则必须下载 [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem) 证书。

### 根证书默认路径

在不同的操作系统中，根证书的默认存储路径如下：

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

Windows 不提供 CA 根证书的特定路径。相反，它使用[注册表](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores)来存储证书。因此，要在 Windows 上指定 CA 根路径，请执行以下步骤：

1. 下载 [ISRG Root X1 证书](https://letsencrypt.org/certs/isrgrootx1.pem)，然后将其保存在您喜欢的路径中，例如 `<path_to_ca>`。
2. 连接到 TiDB Cloud Serverless 集群时，使用该路径（`<path_to_ca>`）作为您的 CA 根路径。

## 常见问题

### 连接到 TiDB Cloud Serverless 集群支持哪些 TLS 版本？

出于安全考虑，TiDB Cloud Serverless 仅支持 TLS 1.2 和 TLS 1.3，不支持 TLS 1.0 和 TLS 1.1 版本。详情请参见 IETF [弃用 TLS 1.0 和 TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/)。

### 是否支持连接客户端和 TiDB Cloud Serverless 之间的双向 TLS 认证？

不支持。

TiDB Cloud Serverless 仅支持单向 TLS 认证，这意味着您的客户端使用公钥验证 TiDB Cloud 集群证书的私钥签名，而集群不验证客户端。

### TiDB Cloud Serverless 是否必须配置 TLS 才能建立安全连接？

对于标准连接，TiDB Cloud Serverless 仅允许 TLS 连接，禁止非 SSL/TLS 连接。原因是当您通过互联网连接到 TiDB Cloud Serverless 集群时，SSL/TLS 是减少数据暴露在互联网上风险的最基本安全措施之一。

对于私有端点连接，由于它支持对 TiDB Cloud 服务的高度安全和单向访问，且不会将您的数据暴露在公共互联网上，因此配置 TLS 是可选的。
