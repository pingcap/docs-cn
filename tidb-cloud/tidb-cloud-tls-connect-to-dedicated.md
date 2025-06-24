---
title: TiDB Cloud Dedicated 的 TLS 连接
summary: 介绍 TiDB Cloud Dedicated 中的 TLS 连接。
aliases: ['/tidbcloud/tidb-cloud-tls-connect-to-dedicated-tier']
---

# TiDB Cloud Dedicated 的 TLS 连接

在 TiDB Cloud 中，建立 TLS 连接是连接到 TiDB Cloud Dedicated 集群的基本安全实践之一。你可以从客户端、应用程序和开发工具配置多个 TLS 连接到 TiDB Cloud Dedicated 集群，以保护数据传输安全。出于安全考虑，TiDB Cloud Dedicated 仅支持 TLS 1.2 和 TLS 1.3，不支持 TLS 1.0 和 TLS 1.1 版本。

为确保数据安全，你的 TiDB Cloud Dedicated 集群的 TiDB 集群 CA 托管在 [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/) 上，TiDB 集群私钥存储在符合 [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) 安全标准的 AWS 托管硬件安全模块（HSMs）中。

## 前提条件

- 通过[密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)或 [SSO 认证](/tidb-cloud/tidb-cloud-sso-authentication.md)登录 TiDB Cloud，然后[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

- 在安全设置中设置访问集群的密码。

    为此，你可以导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，点击 TiDB Cloud Dedicated 集群所在行的 **...**，然后选择**密码设置**。在密码设置中，你可以点击**自动生成密码**自动生成一个长度为 16 个字符的 root 密码，包括数字、大小写字符和特殊字符。

## 安全连接到 TiDB Cloud Dedicated 集群

在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，你可以获取不同连接方式的示例并按以下步骤连接到 TiDB Cloud Dedicated 集群：

1. 导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面，然后点击 TiDB Cloud Dedicated 集群的名称以进入其概览页面。

2. 点击右上角的**连接**。此时会显示一个对话框。

3. 在连接对话框中，从**连接类型**下拉列表中选择**公共**。

    如果你尚未配置 IP 访问列表，请在首次连接之前点击**配置 IP 访问列表**进行配置。更多信息，请参阅[配置 IP 访问列表](/tidb-cloud/configure-ip-access-list.md)。

4. 点击 **CA 证书**下载用于 TLS 连接到 TiDB 集群的 CA 证书。CA 证书默认支持 TLS 1.2 版本。

    > **注意：**
    >
    > - 你可以将下载的 CA 证书存储在操作系统的默认存储路径中，或指定其他存储路径。在后续步骤中，你需要将代码示例中的 CA 证书路径替换为你自己的 CA 证书路径。
    > - TiDB Cloud Dedicated 不强制客户端使用 TLS 连接，目前不支持在 TiDB Cloud Dedicated 上自定义配置 [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610) 变量。

5. 选择你喜欢的连接方式，然后参考选项卡上的连接字符串和示例代码连接到你的集群。

以下示例展示了 MySQL、MyCLI、JDBC、Python、Go 和 Node.js 中的连接字符串：

<SimpleTab>
<div label="MySQL CLI">

MySQL CLI 客户端默认尝试建立 TLS 连接。连接到 TiDB Cloud Dedicated 集群时，你需要设置 `ssl-mode` 和 `ssl-ca`。

```shell
mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=ca.pem --tls-version="TLSv1.2" -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test -p
```

参数说明：

- 使用 `--ssl-mode=VERIFY_IDENTITY` 强制启用 TLS 并验证 TiDB Cloud Dedicated 集群。
- 使用 `--ssl-ca=<CA_path>` 指定下载的 TiDB 集群 `ca.pem` 的本地路径。
- 使用 `--tls-version=TLSv1.2` 限制 TLS 协议的版本。如果要使用 TLS 1.3，可以将版本设置为 `TLSv1.3`。

</div>

<div label="MyCLI">

[MyCLI](https://www.mycli.net/) 在使用 TLS 相关参数时会自动启用 TLS。连接到 TiDB Cloud Dedicated 集群时，你需要设置 `ssl-ca` 和 `ssl-verify-server-cert`。

```shell
mycli --ssl-ca=ca.pem --ssl-verify-server-cert -u root -h tidb.eqlfbdgthh8.clusters.staging.tidb-cloud.com -P 4000 -D test
```

参数说明：

- 使用 `--ssl-ca=<CA_path>` 指定下载的 TiDB 集群 `ca.pem` 的本地路径。
- 使用 `--ssl-verify-server-cert` 验证 TiDB Cloud Dedicated 集群。

</div>

<div label="JDBC">

这里以 [MySQL Connector/J](https://dev.mysql.com/doc/connector-j/en/) 的 TLS 连接配置为例。

下载 TiDB 集群 CA 后，如果要将其导入到操作系统中，可以使用 `keytool -importcert -alias TiDBCACert -file ca.pem -keystore <your_custom_truststore_path> -storepass <your_truststore_password>` 命令。

```shell
/* 请确保替换以下连接字符串中的参数。 */
/* version >= 8.0.28 */
jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>
```

你可以点击**显示示例用法**查看详细的代码示例。

```
import com.mysql.jdbc.Driver;
import java.sql.*;

class Main {
  public static void main(String args[]) throws SQLException, ClassNotFoundException {
    Class.forName("com.mysql.cj.jdbc.Driver");
    try {
      Connection conn = DriverManager.getConnection("jdbc:mysql://tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000/test?user=root&password=<your_password>&sslMode=VERIFY_IDENTITY&tlsVersions=TLSv1.2&trustCertificateKeyStoreUrl=file:<your_custom_truststore_path>&trustCertificateKeyStorePassword=<your_truststore_password>");
      Statement stmt = conn.createStatement();
      try {
        ResultSet rs = stmt.executeQuery("SELECT DATABASE();");
        if (rs.next()) {
          System.out.println("using db:" + rs.getString(1));
        }
      } catch (Exception e) {
        System.out.println("exec error:" + e);
      }
    } catch (Exception e) {
      System.out.println("connect error:" + e);
    }
  }
}
```

参数说明：

- 设置 `sslMode=VERIFY_IDENTITY` 启用 TLS 并验证 TiDB Cloud Dedicated 集群。
- 设置 `enabledTLSProtocols=TLSv1.2` 限制 TLS 协议的版本。如果要使用 TLS 1.3，可以将版本设置为 `TLSv1.3`。
- 设置 `trustCertificateKeyStoreUrl` 为你的自定义信任库路径。
- 设置 `trustCertificateKeyStorePassword` 为你的信任库密码。

</div>

<div label="Python">

这里以 [mysqlclient](https://pypi.org/project/mysqlclient/) 的 TLS 连接配置为例。

```
host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", user="root", password="<your_password>", port=4000, database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"}
```

你可以点击**显示示例用法**查看详细的代码示例。

```
import MySQLdb

connection = MySQLdb.connect(host="tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com", port=4000, user="root", password="<your_password>", database="test", ssl_mode="VERIFY_IDENTITY", ssl={"ca": "ca.pem"})

with connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT DATABASE();")
        m = cursor.fetchone()
        print(m[0])
```

参数说明：

- 设置 `ssl_mode="VERIFY_IDENTITY"` 启用 TLS 并验证 TiDB Cloud Dedicated 集群。
- 使用 `ssl={"ca": "<CA_path>"}` 指定下载的 TiDB 集群 `ca.pem` 的本地路径。

</div>

<div label="Go">

这里以 [Go-MySQL-Driver](https://github.com/go-sql-driver/mysql) 的 TLS 连接配置为例。

```
rootCertPool := x509.NewCertPool()
pem, err := ioutil.ReadFile("ca.pem")
if err != nil {
    log.Fatal(err)
}
if ok := rootCertPool.AppendCertsFromPEM(pem); !ok {
    log.Fatal("Failed to append PEM.")
}
mysql.RegisterTLSConfig("tidb", &tls.Config{
    RootCAs:    rootCertPool,
    MinVersion: tls.VersionTLS12,
    ServerName: "tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com",
})

db, err := sql.Open("mysql", "root:<your_password>@tcp(tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000)/test?tls=tidb")
```

你可以点击**显示示例用法**查看详细的代码示例。

```
package main
import (
  "crypto/tls"
  "crypto/x509"
  "database/sql"
  "fmt"
  "io/ioutil"
  "log"

  "github.com/go-sql-driver/mysql"
)
func main() {
  rootCertPool := x509.NewCertPool()
  pem, err := ioutil.ReadFile("ca.pem")
  if err != nil {
    log.Fatal(err)
  }
  if ok := rootCertPool.AppendCertsFromPEM(pem); !ok {
    log.Fatal("Failed to append PEM.")
  }
  mysql.RegisterTLSConfig("tidb", &tls.Config{
    RootCAs:    rootCertPool,
    MinVersion: tls.VersionTLS12,
    ServerName: "tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com",
  })
  db, err := sql.Open("mysql", "root:<your_password>@tcp(tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com:4000)/test?tls=tidb")
  if err != nil {
    log.Fatal("failed to connect database", err)
  }
  defer db.Close()

  var dbName string
  err = db.QueryRow("SELECT DATABASE();").Scan(&dbName)
  if err != nil {
    log.Fatal("failed to execute query", err)
  }
  fmt.Println(dbName)
}
```

参数说明：

- 在 TLS 连接配置中注册 `tls.Config` 以启用 TLS 并验证 TiDB Cloud Dedicated 集群。
- 设置 `MinVersion: tls.VersionTLS12` 限制 TLS 协议的版本。
- 设置 `ServerName: "<host>"` 验证 TiDB Cloud Dedicated 的主机名。
- 如果你不想注册新的 TLS 配置，可以在连接字符串中直接设置 `tls=true`。

</div>

<div label="Node.js">

这里以 [Mysql2](https://www.npmjs.com/package/mysql2) 的 TLS 连接配置为例。

```
var connection = mysql.createConnection({
  host: 'tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com',
  port: 4000,
  user: 'root',
  password: '<your_password>',
  database: 'test',
  ssl: {
    ca: fs.readFileSync('ca.pem'),
    minVersion: 'TLSv1.2',
    rejectUnauthorized: true
  }
});
```

你可以点击**显示示例用法**查看详细的代码示例。

```
var mysql = require('mysql2');
var fs = require('fs');
var connection = mysql.createConnection({
  host: 'tidb.srgnqxji5bc.clusters.staging.tidb-cloud.com',
  port: 4000,
  user: 'root',
  password: '<your_password>',
  database: 'test',
  ssl: {
    ca: fs.readFileSync('ca.pem'),
    minVersion: 'TLSv1.2',
    rejectUnauthorized: true
  }
});
connection.connect(function(err) {
  if (err) {
    throw err
  }
  connection.query('SELECT DATABASE();', function(err, rows) {
    if (err) {
      throw err
    }
    console.log(rows[0]['DATABASE()']);
    connection.end()
  });
});
```

参数说明：

- 设置 `ssl: {minVersion: 'TLSv1.2'}` 限制 TLS 协议的版本。如果要使用 TLS 1.3，可以将版本设置为 `TLSv1.3`。
- 设置 `ssl: {ca: fs.readFileSync('<CA_path>')}` 读取下载的 TiDB 集群 `ca.pem` 的本地路径。

</div>
</SimpleTab>

## 管理 TiDB Cloud Dedicated 的根证书

TiDB Cloud Dedicated 使用来自 [AWS Certificate Manager (ACM)](https://aws.amazon.com/certificate-manager/) 的证书作为客户端和 TiDB Cloud Dedicated 集群之间 TLS 连接的证书颁发机构（CA）。通常，ACM 的根证书安全地存储在符合 [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) 安全标准的 AWS 托管硬件安全模块（HSMs）中。

## 常见问题

### 连接到 TiDB Cloud Dedicated 集群支持哪些 TLS 版本？

出于安全考虑，TiDB Cloud Dedicated 仅支持 TLS 1.2 和 TLS 1.3，不支持 TLS 1.0 和 TLS 1.1 版本。详情请参阅 IETF [弃用 TLS 1.0 和 TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/)。

### 是否支持客户端和 TiDB Cloud Dedicated 之间的双向 TLS 认证？

不支持。

TiDB Cloud Dedicated 目前仅支持单向 TLS 认证，不支持双向 TLS 认证。如果你需要双向 TLS 认证，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。
