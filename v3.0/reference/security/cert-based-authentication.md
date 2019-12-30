---
title: TiDB 证书鉴权使用指南
summary: 了解使用 TiDB 的证书鉴权功能。
category: reference
---

# TiDB 证书鉴权使用指南 <span class="version-mark">从v3.0.8 版本开始引入</span>

在 v3.0.8 中，TiDB 支持基于证书鉴权的登录方式。采用这种方式，TiDB 对不同用户签发证书，使用加密链接来传输数据，并在用户登录时验证证书。相比 MySQL 用户常用的用户名密码验证方式，证书鉴权方式更安全，因此越来越多的用户使用证书鉴权来代替用户名密码验证。

TiDB 的证书鉴权方式和 [MySQL](https://dev.mysql.com/doc/refman/8.0/en/create-user.html#create-user-tls) 高度兼容。在 TiDB 上使用证书鉴权，需要进行以下操作：

+ 创建安全密钥和证书
+ 配置 TiDB 和客户端使用的证书
+ 配置登陆时需要校验的用户证书信息
+ 更新和替换证书

本文档描述了使用证书鉴权的以上各个操作。

## 创建安全密钥和证书

### 安装 OpenSS

目前推荐使用 [OpenSSL](https://www.openssl.org/) 来生成密钥和证书。以 Debain 操作系统为例，先执行以下命令来安装 OpenSSL：

```
sudo apt-get install openssl
```

### 生成 CA 密钥和证书

1. 执行以下命令生成 CA 密钥：

    ```
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    命令执行后输出以下结果：

    ```
    Generating RSA private key, 2048 bit long modulus (2 primes)
    ....................+++++
    ...............................................+++++
    e is 65537 (0x010001)
    ```

2. 执行以下命令生成该密钥对应的证书：

    ```
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3. 输入用户信息，示例如下：

    ```
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
    > 以上用户信息中，`:` 后的文字为用户输入的信息。

### 生成服务端密钥和证书

1. 执行以下命令生成服务端的密钥和证书：

    ```
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2. 输入用户信息，示例如下：

    ```
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

    ```
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    输出结果如下：

    ```
    writing RSA key
    ```

4. 使用 CA 证书签名来生成服务端的证书：

    ```
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    输出结果示例如下：

    ```
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **注意：**
    >
    > 以上结果中，用户登陆时 TiDB 将强制检查 `subject` 部分的信息是否一致。

### 生成客户端密钥和证书

生成服务端密钥和证书后，需要生成客户端使用的密钥和证书。通常需要为不同的用户生成不同的密钥和证书。

1. 执行以下命令生成客户端的密钥和证书：

    ```
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2. 输入用户信息，示例如下：

    ```
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

    ```
    sudo openssl rsa -in client-key.pem -out client-key.pem
    ```

    以上命令的输出结果如下：

    ```
    writing RSA key
    ```

4. 执行以下命令，使用 CA 证书签名来生成客户端证书：

    ```
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    输出结果示例如下：

    ```
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **注意：**
    >
    > 以上结果中，`subject` 部分后的信息会被用来在 `require` 中配置和要求验证。

### 验证证书

执行以下命令验证证书：

```
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
server-cert.pem: OK
client-cert.pem: OK
```

## 配置 TiDB 和客户端使用证书

在生成证书后，需要在 TiDB 中配置服务端所使用的证书，同时让客户端程序使用客户端证书。

### 配置 TiDB 服务端

修改 TiDB 配置文件中的 `security` 段：

```
[security]
ssl-cert = "ssl/server-cert.pem"
ssl-key = "ssl/server-key.pem"
ssl-ca="ssl/ca-cert.pem"
```

启动 TiDB 日志。如果日志中有以下内容，即代表配置生效：

```
[INFO] [server.go:264] ["secure connection is enabled"] ["client verification enabled"=true]
```

### 配置客户端程序

配置客户端程序，让客户端使用客户端密钥和证书来登录 TiDB。

以 MySQL 客户端为例，可以通过指定 `ssl-cert`、`ssl-key`、`ssl-ca` 来使用新的 CA 证书、客户端密钥和证书：

```
> mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

## 配置登陆时需要校验的用户证书信息

在 TiDB 中使用 `root` 登录新建的用户并进行配置。

+ 可以在创建用户 (`create user`) 时配置登陆需要校验的证书信息：

    ```
    create user 'u1'@'%'  require issuer '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=TiDB admin/emailAddress=s@pingcap.com' subject '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=tpch-user1/emailAddress=zz@pingcap.com' cipher 'TLS_AES_256_GCM_SHA384';
    grant all on *.* to 'u1'@'%';
    ```

+ 可以在赋予权限 (`grant`) 时配置登陆时需要校验的证书信息：

    ```
    create user 'u1'@'%';
    grant all on *.* to 'u1'@'%' require issuer '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=TiDB admin/emailAddress=s@pingcap.com' subject '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=tpch-user1/emailAddress=zz@pingcap.com' cipher 'TLS_AES_256_GCM_SHA384';
    ```

+ 还可以在修改已有用户 (alter user) 时配置登陆时需要校验的证书信息：

    ```
    alter user 'u1'@'%' require issuer '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=TiDB admin/emailAddress=s@pingcap.com' subject '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=tpch-user1/emailAddress=zz@pingcap.com' cipher 'TLS_AES_256_GCM_SHA384';
    ```

以上 3 个语句中分别通过指定 `require subject`、`require issuer` 和 `require cipher` 来指定检查 X.509 certificate attributes。用户可以选择配置其中一项或多项，使用空格或 `and` 分隔。

+ `require subject`：指定用户在连接时需要提供客户端证书的 `subject` 内容。指定该选项后，不需要再配置 `require ssl` 或 x509。配置内容对应[生成客户端密钥和证书](#生成客户端密钥和证书) 中输出的 `subject` 的内容。将 `subject` 输出内容中的 `,` 替换为 `/` 并去掉空格。可以使用命令 `openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'` 来获取对应 `client-cert` 的 `subject`。
+ `require issuer`：指定签发用户证书的 CA 证书的 `subject` 内容。配置内容对应[生成 CA 密钥和证书](#生成-ca-密钥和证书) 中输入的内容。可以使用命令 `openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'` 来获取对应 `client-cert` 的 `subject`。
+ `require cipher`：配置该项检查客户端支持的 cipher method。可以使用 `SHOW SESSION STATUS LIKE 'Ssl_cipher_list'` 语句查看支持的列表。

配置完成后，用户在登录时 TiDB 会验证以下内容：

+ 使用 SSL 登录，且证书为服务器配置的 CA 证书所签发
+ 证书的 `Issuer` 信息和权限配置里的信息相匹配
+ 证书的 `Subject` 信息和权限配置里的信息相匹配

全部验证通过后用户才能登录，否则会报 `ERROR 1045 (28000): Access denied` 错误。登录后，可以通过以下命令来查看当前链接是否使用证书登录、TLS 版本 和 Cipher 算法。

```
MySQL [test]> \s
--------------
mysql  Ver 15.1 Distrib 10.4.10-MariaDB, for Linux (x86_64) using readline 5.1

Connection id:       1
Current database:    test
Current user:        root@127.0.0.1
SSL:                 Cipher in use is TLS_AES_256_GCM_SHA384
```

```
MySQL [test]> show variables like '%ssl%';
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

CA 证书是客户端和服务端相互校验的依据，所以如果需要替换 CA 证书，则需要生成一个组合证书来在滚动期间同时支持新旧客户端和服务器的验证，并优先替换客户端和服务端的 CA 证书，再替换其他客户端和服务端的密钥和证书。

### 更新 CA 密钥和证书

1. 以替换 CA 密钥为例（假设 `ca-key.pem` 被盗），将旧的 CA 密钥和证书进行备份：

    ```
    mv ca-key.pem ca-key.old.pem
    mv ca-cert.pem ca-cert.old.pem
    ```

2. 生成新的 CA 密钥：

    ```
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3. 用新的密钥生成新的 CA 证书：

    ```
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **注意：**
    >
    > 生成新的 CA 证书是为了替换密钥和证书，保证在线用户不受影响。所以以上命令中填写的附加信息必须与已配置的 `require issuer` 信息一致。

4. 生成组合 CA 证书：

    ```
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

之后使用新生成的组合 CA 证书并重启 TiDB Server，此时服务端可以同时接受和使用新旧 CA 证书。

之后先将所有客户端用的 CA 证书也替换为新生成的组合 CA 证书，使客户端能同时和使用新旧 CA 证书。

### 更新客户端密钥和证书

> **注意：**
>
> 需要将集群中所有服务端和客户端使用的 CA 证书都替换为新生成的组合 CA 证书后才能开始进行以下步骤。

1. 生成新的客户端密钥和证书：

    ```
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem
    ```

    > **注意：**
    >
    > 以上命令是为了替换密钥和证书，保证在线用户不受影响，所以以上命令中填写的附加信息必须与已配置的 `require subject` 信息一致。

    ```
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

2. 使用新的组合 CA 证书和新 CA 密钥生成新客户端证书：

    ```
    sudo openssl x509 -req -in client-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.new.pem
    ```

3. 让客户端使用新的客户端密钥和证书来连接 TiDB （以 MySQL 客户端为例）：

    ```
    mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
    ```

### 更新服务端密钥和证书

1. 生成新的服务端密钥和证书：

    ```
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2. 使用新的组合 CA 证书和新 CA 密钥生成新服务端证书：

    ```
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3. 让配置 TiDB 使用上面新生成的服务端密钥和证书并重启。

通过更新服务端密钥和证书，可以为整个 TiDB 集群和用户更换为新的 CA 证书、新的客户端密钥和证书、新的服务端密钥和证书。
