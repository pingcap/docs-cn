---
title: TiDB 证书鉴权使用指南
summary: 了解使用 TiDB 的证书鉴权功能。
aliases: ['/docs-cn/stable/certificate-authentication/','/docs-cn/v4.0/certificate-authentication/','/docs-cn/stable/reference/security/cert-based-authentication/']
---

# TiDB 证书鉴权使用指南

TiDB 支持基于证书鉴权的登录方式。采用这种方式，TiDB 对不同用户签发证书，使用加密连接来传输数据，并在用户登录时验证证书。相比 MySQL 用户常用的用户名密码验证方式，与 MySQL 相兼容的证书鉴权方式更安全，因此越来越多的用户使用证书鉴权来代替用户名密码验证。

在 TiDB 上使用证书鉴权的登录方法，可能需要进行以下操作：

+ 创建安全密钥和证书
+ 配置 TiDB 和客户端使用的证书
+ 配置登录时需要校验的用户证书信息
+ 更新和替换证书

本文介绍了如何进行证书鉴权的上述几个操作。

## 创建安全密钥和证书

目前推荐使用 [OpenSSL](https://www.openssl.org/) 来生成密钥和证书，生成证书的过程和[为 TiDB 客户端服务端间通信开启加密传输](/enable-tls-between-clients-and-servers.md)过程类似，下面更多演示如何在证书中配置更多需校验的属性字段。

### 生成 CA 密钥和证书

1. 执行以下命令生成 CA 密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    命令执行后输出以下结果：

    {{< copyable "shell-regular" >}}

    ```bash
    Generating RSA private key, 2048 bit long modulus (2 primes)
    ....................+++++
    ...............................................+++++
    e is 65537 (0x010001)
    ```

2. 执行以下命令生成该密钥对应的证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3. 输入证书细节信息，示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (eg, city) []:San Francisco
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (eg, section) []:TiDB
    Common Name (e.g. server FQDN or YOUR name) []:TiDB admin
    Email Address []:s@pingcap.com
    ```

    > **注意：**
    >
    > 以上信息中，`:` 后的文字为用户输入的信息。

### 生成服务端密钥和证书

1. 执行以下命令生成服务端的密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2. 输入证书细节信息，示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (eg, city) []:San Francisco
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (eg, section) []:TiKV
    Common Name (e.g. server FQDN or YOUR name) []:TiKV Test Server
    Email Address []:k@pingcap.com

    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:
    An optional company name []:
    ```

3. 执行以下命令生成服务端的 RSA 密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    输出结果如下：

    ```bash
    writing RSA key
    ```

4. 使用 CA 证书签名来生成服务端的证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    输出结果示例如下：

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **注意：**
    >
    > 以上结果中，用户登录时 TiDB 将强制检查 `subject` 部分的信息是否一致。

### 生成客户端密钥和证书

生成服务端密钥和证书后，需要生成客户端使用的密钥和证书。通常需要为不同的用户生成不同的密钥和证书。

1. 执行以下命令生成客户端的密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2. 输入证书细节信息，示例如下：

    {{< copyable "shell-regular" >}}

    ```bash
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Locality Name (eg, city) []:San Francisco
    Organization Name (eg, company) [Internet Widgits Pty Ltd]:PingCAP Inc.
    Organizational Unit Name (eg, section) []:TiDB
    Common Name (e.g. server FQDN or YOUR name) []:tpch-user1
    Email Address []:zz@pingcap.com

    Please enter the following 'extra' attributes
    to be sent with your certificate request
    A challenge password []:
    An optional company name []:
    ```

3. 执行以下命令生成客户端 RSA 证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl rsa -in client-key.pem -out client-key.pem
    ```

    以上命令的输出结果如下：

    ```bash
    writing RSA key
    ```

4. 执行以下命令，使用 CA 证书签名来生成客户端证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    输出结果示例如下：

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **注意：**
    >
    > 以上结果中，`subject` 部分后的信息会被用来在 `require` 中配置和要求验证。

### 验证证书

执行以下命令验证证书：

{{< copyable "shell-regular" >}}

```bash
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
```

如果验证通过，会显示以下信息：

```
server-cert.pem: OK
client-cert.pem: OK
```

## 配置 TiDB 和客户端使用证书

在生成证书后，需要在 TiDB 中配置服务端所使用的证书，同时让客户端程序使用客户端证书。

### 配置 TiDB 服务端

修改 TiDB 配置文件中的 `[security]` 段。这一步指定 CA 证书、服务端密钥和服务端证书存放的路径。可将 `path/to/server-cert.pem`、`path/to/server-key.pem` 和 `path/to/ca-cert.pem` 替换成实际的路径。

{{< copyable "" >}}

```
[security]
ssl-cert ="path/to/server-cert.pem"
ssl-key ="path/to/server-key.pem"
ssl-ca="path/to/ca-cert.pem"
```

启动 TiDB 日志。如果日志中有以下内容，即代表配置生效：

```
[INFO] [server.go:264] ["secure connection is enabled"] ["client verification enabled"=true]
```

### 配置客户端程序

配置客户端程序，让客户端使用客户端密钥和证书来登录 TiDB。

以 MySQL 客户端为例，可以通过指定 `ssl-cert`、`ssl-key`、`ssl-ca` 来使用新的 CA 证书、客户端密钥和证书：

{{< copyable "shell-regular" >}}

```bash
mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

> **注意：**
>
> `/path/to/client-cert.new.pem`、`/path/to/client-key.new.pem` 和 `/path/to/ca-cert.pem` 是 CA 证书、客户端密钥和客户端存放的路径。可将以上命令中的这些部分替换为实际的路径。

## 配置登录时需要校验的用户证书信息

使用客户端连接 TiDB 进行授权配置。先获取需要验证的用户证书信息，再对这些信息进行配置。

### 获取用户证书信息

用户证书信息可由 `require subject`、`require issuer`、`require san` 和 `require cipher` 来指定，用于检查 X.509 certificate attributes。

+ `require subject`：指定用户在连接时需要提供客户端证书的 `subject` 内容。指定该选项后，不需要再配置 `require ssl` 或 x509。配置内容对应[生成客户端密钥和证书](#生成客户端密钥和证书)中的录入信息。

    可以执行以下命令来获取该项的信息：

    {{< copyable "shell-regular" >}}

    ```
    openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

+ `require issuer`：指定签发用户证书的 CA 证书的 `subject` 内容。配置内容对应[生成 CA 密钥和证书](#生成-ca-密钥和证书)中的录入信息。

    可以执行以下命令来获取该项的信息：

    {{< copyable "shell-regular" >}}

    ```
    openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'
    ```

+ `require san`：指定签发用户证书的 CA 证书的 `Subject Alternative Name` 内容。配置内容对应生成客户端证书使用的 [openssl.cnf 配置文件的 `alt_names` 信息](/generate-self-signed-certificates.md)。

    + 可以执行以下命令来获取已生成证书中的 `require san` 项的信息：

        {{< copyable "shell-regular" >}}

        ```shell
        openssl x509 -noout -ext subjectAltName -in client.crt
        ```

    + `require san` 目前支持以下 `Subject Alternative Name` 检查项：

        - URI
        - IP
        - DNS

    + 多个检查项可通过逗号连接后进行配置。例如，对用户 `u1` 进行以下配置：

        {{< copyable "sql" >}}

        ```sql
        create user 'u1'@'%' require san 'DNS:d1,URI:spiffe://example.org/myservice1,URI:spiffe://example.org/myservice2'
        ```

        以上配置只允许用户 `u1` 使用 URI 项为 `spiffe://example.org/myservice1` 或 `spiffe://example.org/myservice2`、DNS 项为 `d1` 的证书登录 TiDB。

+ `require cipher`：配置该项检查客户端支持的 `cipher method`。可以使用以下语句来查看支持的列表：

    {{< copyable "sql" >}}

    ```sql
    SHOW SESSION STATUS LIKE 'Ssl_cipher_list';
    ```

### 配置用户证书信息

获取用户证书信息（`require subject`, `require issuer`、`require san` 和 `require cipher`）后，可在创建用户、赋予权限或更改用户时配置用户证书信息。将以下命令中的 `<replaceable>` 替换为对应的信息。可以选择配置其中一项或多项，使用空格或 `and` 分隔。

+ 可以在创建用户 (`create user`) 时配置登录时需要校验的证书信息：

    {{< copyable "sql" >}}

    ```sql
    create user 'u1'@'%'  require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

+ 可以在赋予权限 (`grant`) 时配置登录时需要校验的证书信息：

    {{< copyable "sql" >}}

    ```sql
    grant all on *.* to 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

+ 还可以在修改已有用户 (alter user) 时配置登录时需要校验的证书信息：

    {{< copyable "sql" >}}

    ```sql
    alter user 'u1'@'%' require issuer '<replaceable>' subject '<replaceable>' san '<replaceable>' cipher '<replaceable>';
    ```

配置完成后，用户在登录时 TiDB 会验证以下内容：

+ 使用 SSL 登录，且证书为服务器配置的 CA 证书所签发
+ 证书的 `Issuer` 信息和权限配置里的信息相匹配
+ 证书的 `Subject` 信息和权限配置里的信息相匹配
+ 证书的 `Subject Alternative Name` 信息和权限配置里的信息相匹配

全部验证通过后用户才能登录，否则会报 `ERROR 1045 (28000): Access denied` 错误。登录后，可以通过以下命令来查看当前链接是否使用证书登录、TLS 版本和 Cipher 算法。

连接 MySQL 客户端并执行：

{{< copyable "sql" >}}

```sql
\s
```

返回结果如下：

```
--------------
mysql  Ver 15.1 Distrib 10.4.10-MariaDB, for Linux (x86_64) using readline 5.1

Connection id:       1
Current database:    test
Current user:        root@127.0.0.1
SSL:                 Cipher in use is TLS_AES_256_GCM_SHA384
```

然后执行：

{{< copyable "sql" >}}

```sql
show variables like '%ssl%';
```

返回结果如下：

```
+---------------+----------------------------------+
| Variable_name | Value                            |
+---------------+----------------------------------+
| ssl_cert      | /path/to/server-cert.pem         |
| ssl_ca        | /path/to/ca-cert.pem             |
| have_ssl      | YES                              |
| have_openssl  | YES                              |
| ssl_key       | /path/to/server-key.pem          |
+---------------+----------------------------------+
6 rows in set (0.067 sec)
```

## 更新和替换证书

证书和密钥通常会周期性更新。下文介绍更新密钥和证书的流程。

CA 证书是客户端和服务端相互校验的依据，所以如果需要替换 CA 证书，则需要生成一个组合证书来在替换期间同时支持客户端和服务器上新旧证书的验证，并优先替换客户端和服务端的 CA 证书，再替换客户端和服务端的密钥和证书。

### 更新 CA 密钥和证书

1. 以替换 CA 密钥为例（假设 `ca-key.pem` 被盗），将旧的 CA 密钥和证书进行备份：

    {{< copyable "shell-regular" >}}

    ```bash
    mv ca-key.pem ca-key.old.pem && \
    mv ca-cert.pem ca-cert.old.pem
    ```

2. 生成新的 CA 密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3. 用新的密钥生成新的 CA 证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **注意：**
    >
    > 生成新的 CA 证书是为了替换密钥和证书，保证在线用户不受影响。所以以上命令中填写的附加信息必须与已配置的 `require issuer` 信息一致。

4. 生成组合 CA 证书：

    {{< copyable "shell-regular" >}}

    ```bash
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

之后使用新生成的组合 CA 证书并重启 TiDB Server，此时服务端可以同时接受和使用新旧 CA 证书。

之后先将所有客户端用的 CA 证书也替换为新生成的组合 CA 证书，使客户端能同时和使用新旧 CA 证书。

### 更新客户端密钥和证书

> **注意：**
>
> 需要将集群中所有服务端和客户端使用的 CA 证书都替换为新生成的组合 CA 证书后才能开始进行以下步骤。

1. 生成新的客户端 RSA 密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem && \
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

    > **注意：**
    >
    > 以上命令是为了替换密钥和证书，保证在线用户不受影响，所以以上命令中填写的附加信息必须与已配置的 `require subject` 信息一致。

2. 使用新的组合 CA 证书和新 CA 密钥生成新客户端证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in client-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.new.pem
    ```

3. 让客户端使用新的客户端密钥和证书来连接 TiDB （以 MySQL 客户端为例）：

    {{< copyable "shell-regular" >}}

    ```bash
    mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
    ```

    > **注意：**
    >
    > `/path/to/client-cert.new.pem`、`/path/to/client-key.new.pem` 和 `/path/to/ca-cert.pem` 是 CA 证书、客户端密钥和客户端存放的路径。可将以上命令中的这些部分替换为实际的路径。

### 更新服务端密钥和证书

1. 生成新的服务端 RSA 密钥：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem && \
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2. 使用新的组合 CA 证书和新 CA 密钥生成新服务端证书：

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3. 配置 TiDB 使用上面新生成的服务端密钥和证书并重启。参见[配置 TiDB 服务端](#配置-tidb-服务端)。
