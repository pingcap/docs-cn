---
title: 为 TiDB 客户端服务端间通信开启加密传输
---

# 为 TiDB 客户端服务端间通信开启加密传输

TiDB 服务端与客户端之间默认采用非加密连接，因而具备监视信道流量能力的第三方可以知悉 TiDB 服务端与客户端之间发送和接受的数据，包括但不限于查询语句内容、查询结果等。若信道是不可信的，例如客户端是通过公网连接到 TiDB 服务端的，则非加密连接容易造成信息泄露，建议使用加密连接确保安全性。

TiDB 服务端支持启用基于 TLS（传输层安全）协议的加密连接，协议与 MySQL 加密连接一致，现有 MySQL Client 如 MySQL Shell 和 MySQL 驱动等能直接支持。TLS 的前身是 SSL，因而 TLS 有时也被称为 SSL，但由于 SSL 协议有已知安全漏洞，TiDB 实际上并未支持。TiDB 支持的 TLS/SSL 协议版本为 TLSv1.0、TLSv1.1、TLSv1.2 和 TLSv1.3。

使用加密连接后，连接将具有以下安全性质：

- 保密性：流量明文被加密，无法被窃听；
- 完整性：流量明文无法被篡改；
- 身份验证（可选）：客户端和服务端能验证双方身份，避免中间人攻击。

要为 TiDB 客户端与服务端间的通信开启 TLS 加密传输，首先需要在 TiDB 服务端通过配置开启 TLS 加密连接的支持，然后通过配置客户端应用程序使用 TLS 加密连接。一般情况下，如果服务端正确配置了 TLS加密连接支持，客户端库都会自动启用 TLS 加密传输。

另外，与 MySQL 相同，TiDB 也支持在同一 TCP 端口上开启 TLS 连接或非 TLS 连接。对于开启了 TLS 连接支持的 TiDB 服务端，客户端既可以选择通过加密连接安全地连接到该 TiDB 服务端，也可以选择使用普通的非加密连接。如需使用加密连接，你可以通过以下方式进行配置：

+ 通过在启动参数中配置 `--require-secure-transport` 要求所有用户必须使用加密连接来连接到 TiDB。
+ 通过在创建用户 (`create user`)，或修改已有用户 (`alter user`) 时指定 `REQUIRE SSL` 要求指定用户必须使用加密连接来连接 TiDB。以创建用户为例：

    ```sql
    CREATE USER 'u1'@'%' IDENTIFIED BY 'my_random_password' REQUIRE SSL;
    ```

> **注意：**
>
> 如果登录用户已配置使用 [TiDB 证书鉴权功能](/certificate-authentication.md#配置登录时需要校验的用户证书信息)校验用户证书，也会隐式要求对应用户必须使用加密连接连接 TiDB。

## 配置 TiDB 服务端启用安全连接

要启用安全连接，请参考以下相关参数说明：

- [`auto-tls`](/tidb-configuration-file.md#auto-tls): 启用证书自动生成功能（从 v5.2.0 开始）
- [`ssl-cert`](/tidb-configuration-file.md#ssl-cert)：指定 SSL 证书文件路径
- [`ssl-key`](/tidb-configuration-file.md#ssl-key)：指定证书文件对应的私钥
- [`ssl-ca`](/tidb-configuration-file.md#ssl-ca)：可选，指定受信任的 CA 证书文件路径
- [`tls-version`](/tidb-configuration-file.md#tls-version)：可选，指定最低 TLS 版本，例如 `TLSv1.2`

`auto tls` 支持安全连接，但不提供客户端证书验证。有关证书验证和控制证书生成方式的说明，请参考下面配置 `ssl-cert`，`ssl-key` 和 `ssl-ca` 变量的建议：

- 在启动 TiDB 时，至少需要在配置文件中同时指定 `ssl-cert` 和 `ssl-key` 参数，才能在 TiDB 服务端开启安全连接。还可以指定 `ssl-ca` 参数进行客户端身份验证（请参见[配置启用身份验证](#配置启用身份验证)章节）。
- 参数指定的文件都为 PEM 格式。另外目前 TiDB 尚不支持加载有密码保护的私钥，因此必须提供一个没有密码的私钥文件。若提供的证书或私钥无效，则 TiDB 服务端将照常启动，但并不支持客户端加密连接到 TiDB 服务端。
- 若证书参数无误，则 TiDB 在启动时将会输出 `secure connection is enabled`，否则 TiDB 会输出 `secure connection is NOT ENABLED`。

> **注意：**
>
> v5.2.0 版本之前，你可以使用 `mysql_ssl_rsa_setup --datadir=./certs` 生成证书。`mysql_ssl_rsa_setup` 工具是 MySQL Server 的一部分。

## 配置 MySQL Client 使用安全连接

MySQL 5.7 及以上版本自带的客户端默认尝试使用安全连接，若服务端不支持安全连接则自动退回到使用非安全连接；MySQL 5.7 以下版本自带的客户端默认采用非安全连接。

可以通过命令行参数修改客户端的连接行为，包括：

- 强制使用安全连接，若服务端不支持安全连接则连接失败 (`--ssl-mode=REQUIRED`)
- 尝试使用安全连接，若服务端不支持安全连接则退回使用不安全连接
- 使用不安全连接 (`--ssl-mode=DISABLED`)

除此参数外，MySQL 8.0 客户端有两种 SSL 模式：

- `--ssl-mode=VERIFY_CA`: 根据 `--ssl-ca` 签发的 CA 验证来自服务器的证书。
- `--ssl-mode=VERIFY_IDENTITY`: 与 `VERIFY_CA` 相同，但也验证所连接的主机名是否与证书匹配。

详细信息请参阅 MySQL 文档中关于[客户端配置安全连接](https://dev.mysql.com/doc/refman/5.7/en/using-encrypted-connections.html#using-encrypted-connections-client-side-configuration)的部分。

## 配置启用身份验证

若在 TiDB 服务端或 MySQL Client 中未指定 `ssl-ca` 参数，则默认不会进行客户端或服务端身份验证，无法抵御中间人攻击，例如客户端可能会“安全地”连接到了一个伪装的服务端。可以在服务端和客户端中配置 `ssl-ca` 参数进行身份验证。一般情况下只需验证服务端身份，但也可以验证客户端身份进一步增强安全性。

- 若要使 MySQL Client 验证 TiDB 服务端身份，TiDB 服务端需至少配置 `ssl-cert` 和 `ssl-key` 参数，客户端需至少指定 `--ssl-ca` 参数，且 `--ssl-mode` 至少为 `VERIFY_CA`。必须确保 TiDB 服务端配置的证书 (`ssl-cert`) 是由客户端 `--ssl-ca` 参数所指定的 CA 所签发的，否则身份验证失败。
- 若要使 TiDB 服务端验证 MySQL Client 身份，TiDB 服务端需配置 `ssl-cert`、`ssl-key`、`ssl-ca` 参数，客户端需至少指定 `--ssl-cert`、`--ssl-key` 参数。必须确保服务端配置的证书和客户端配置的证书都是由服务端配置指定的 `ssl-ca` 签发的。
- 若要进行双向身份验证，请同时满足上述要求。

默认情况，服务端对客户端的身份验证是可选的。若客户端在 TLS 握手时未出示自己的身份证书，也能正常建立 TLS 连接。但也可以通过在创建用户 (`create user`)，赋予权限 (`grant`) 或修改已有用户 (`alter user`) 时指定 `require x509` 要求客户端需进行身份验证，以创建用户为例：

```sql
create user 'u1'@'%'  require x509;
```

> **注意：**
>
> 如果登录用户已配置使用 [TiDB 证书鉴权功能](/certificate-authentication.md#配置登录时需要校验的用户证书信息)校验用户证书，也会隐式要求对应用户需进行身份验证。

## 检查当前连接是否是加密连接

可以通过 `SHOW STATUS LIKE "%Ssl%";` 了解当前连接的详细情况，包括是否使用了安全连接、安全连接采用的加密协议、TLS 版本号等。

以下是一个安全连接中执行该语句的结果。由于客户端支持的 TLS 版本号和加密协议会有所不同，执行结果相应地也会有所变化。

{{< copyable "sql" >}}

```sql
SHOW STATUS LIKE "%Ssl%";
```

```
......
| Ssl_verify_mode | 5                            |
| Ssl_version     | TLSv1.2                      |
| Ssl_cipher      | ECDHE-RSA-AES128-GCM-SHA256  |
......
```

除此以外，对于 MySQL 自带客户端，还可以使用 `STATUS` 或 `\s` 语句查看连接情况：

{{< copyable "sql" >}}

```sql
\s
```

```
...
SSL: Cipher in use is ECDHE-RSA-AES128-GCM-SHA256
...
```

## 支持的 TLS 版本及密钥交换协议和加密算法

TiDB 支持的 TLS 版本及密钥交换协议和加密算法由 Golang 官方库决定。

你使用的客户端库和操作系统加密策略也可能会影响到支持的协议版本和密码套件。

### 支持的 TLS 版本

- TLSv1.0 （默认禁用）
- TLSv1.1
- TLSv1.2
- TLSv1.3

可以使用配置项 `tls-version` 来限制 TLS 版本。

实际可用的 TLS 版本取决于操作系统的加密策略、MySQL 客户端版本和客户端的 SSL/TLS 库。

### 支持的密钥交换协议及加密算法

- TLS\_RSA\_WITH\_AES\_128\_CBC\_SHA
- TLS\_RSA\_WITH\_AES\_256\_CBC\_SHA
- TLS\_RSA\_WITH\_AES\_128\_CBC\_SHA256
- TLS\_RSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_RSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_CBC\_SHA
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_256\_CBC\_SHA
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_CBC\_SHA
- TLS\_ECDHE\_RSA\_WITH\_AES\_256\_CBC\_SHA
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_CBC\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_CBC\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_128\_GCM\_SHA256
- TLS\_ECDHE\_RSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_ECDSA\_WITH\_AES\_256\_GCM\_SHA384
- TLS\_ECDHE\_RSA\_WITH\_CHACHA20\_POLY1305\_SHA256
- TLS\_ECDHE\_ECDSA\_WITH\_CHACHA20\_POLY1305\_SHA256
- TLS\_AES\_128\_GCM\_SHA256
- TLS\_AES\_256\_GCM\_SHA384
- TLS\_CHACHA20\_POLY1305\_SHA256

## 重加载证书、密钥和 CA

在需要替换证书、密钥或 CA 时，可以在完成对应文件替换后，对运行中的 TiDB 实例执行 [`ALTER INSTANCE RELOAD TLS`](/sql-statements/sql-statement-alter-instance.md) 语句从原配置的证书 ([`ssl-cert`](/tidb-configuration-file.md#ssl-cert))、密钥 ([`ssl-key`](/tidb-configuration-file.md#ssl-key)) 和 CA ([`ssl-ca`](/tidb-configuration-file.md#ssl-ca)) 的路径重新加证书、密钥和 CA，而无需重启 TiDB 实例。

新加载的证书密钥和 CA 将在语句执行成功后对新建立的连接生效，不会影响语句执行前已建立的连接。

## 监控

自 TiDB v5.2.0 版本起，你可以使用 `Ssl_server_not_after` 和 `Ssl_server_not_before` 状态变量监控证书有效期的起止时间。

```sql
SHOW GLOBAL STATUS LIKE 'Ssl\_server\_not\_%';
```

```
+-----------------------+--------------------------+
| Variable_name         | Value                    |
+-----------------------+--------------------------+
| Ssl_server_not_after  | Nov 28 06:42:32 2021 UTC |
| Ssl_server_not_before | Aug 30 06:42:32 2021 UTC |
+-----------------------+--------------------------+
2 rows in set (0.0076 sec)
```

## 另请参阅

- [为 TiDB 组件间通信开启加密传输](/enable-tls-between-components.md)
