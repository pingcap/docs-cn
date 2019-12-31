---
title: Certificate-Based Authentication for Login
summary: Learn the certificate-based authentication used for login.
category: reference
---

# Certificate-Based Authentication for Login <span class="version-mark">New in v3.0.8</span>

Starting from v3.0.8, TiDB supports a certificate-based authentication method for users to log into TiDB. With this method, TiDB issues certificates to different users, uses encrypted connections to transfer data, and verifies certificates when users log in. Compared with the user name and password authentication method commonly used by MySQL users, the MySQL compatible certificate-based authentication method is securer, and is thus adopted by an increasing number of users.

To use certificate-based authentication, you might need to perform the following operations:

+ Create security keys and certificates
+ Configure certificates for TiDB and the client
+ Configure the user certificate information to be verified when the user logs in
+ Update and replace certificates

The rest of the document introduces in detail how to perform these operations.

## Create security keys and certificates

### Install OpenSSL

It is recommended that you use [OpenSSL](https://www.openssl.org/) to create keys and certificates. Taking the Debian operating system as an example, execute the following command to install OpenSSL:

{{< copyable "shell-regular" >}}

```bash
sudo apt-get install openssl
```

### Generate CA key and certificate

1. Execute the following command to generate the CA key:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

    The output of the above command:

    {{< copyable "shell-regular" >}}

    ```bash
    Generating RSA private key, 2048 bit long modulus (2 primes)
    ....................+++++
    ...............................................+++++
    e is 65537 (0x010001)
    ```

2. Execute the following command to generate the certificate corresponding to the CA key:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.pem
    ```

3. Enter detailed certificate information. For example:

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

    > **Note:**
    >
    > In the above certificate details, texts after `:` are the entered information.

### Generate server key and certificate

1. Execute the following command to generate the server key:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.pem -out server-req.pem
    ```

2. Enter detailed certificate information. For example:

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

3. Execute the following command to generate the RSA key of the server:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl rsa -in server-key.pem -out server-key.pem
    ```

    The output of the above command:

    {{< copyable "shell-regular" >}}

    ```bash
    writing RSA key
    ```

4. Use the CA certificate signature to generate the server certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in server-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.pem
    ```

    The output of the above command (for example):

    {{< copyable "shell-regular" >}}

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiKV, CN = TiKV Test Server, emailAddress = k@pingcap.com
    Getting CA Private Key
    ```

    > **Note:**
    >
    > When you log in, TiDB checks whether the information in the `subject` section of the above output is consistent or not.

### Generate client key and certificate

After generating the server key and certificate, you need to generate the key and certificate for the client. It is often necessary to generate different keys and certificates for different users.

1. Execute the following command to generate the client key:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.pem -out client-req.pem
    ```

2. Enter detailed certificate information. For example:

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

3. Execute the following command to generate the RSA key of the client:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl rsa -in client-key.pem -out client-key.pem
    ```

    The output of the above command:

    {{< copyable "shell-regular" >}}

    ```bash
    writing RSA key
    ```

4. Use the CA certificate signature to generate the client certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in client-req.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.pem
    ```

    The output of the above command (for example):

    {{< copyable "shell-regular" >}}

    ```bash
    Signature ok
    subject=C = US, ST = California, L = San Francisco, O = PingCAP Inc., OU = TiDB, CN = tpch-user1, emailAddress = zz@pingcap.com
    Getting CA Private Key
    ```

    > **Note:**
    >
    > The information of the `subject` section in the above output is used for [certificate configuration for login verification](#configure-the-user-certificate-information-for-login-verification) in the `require` section.

### Verify certificate

Execute the following command to verify certificate:

{{< copyable "shell-regular" >}}

```bash
openssl verify -CAfile ca-cert.pem server-cert.pem client-cert.pem
```

If the certificate is verified, you will see the following result:

```
server-cert.pem: OK
client-cert.pem: OK
```

## Configure TiDB and the client to use certificates

After generating the certificates, you need to configure the TiDB server and the client to use the corresponding server certificate or client certificate.

### Configure TiDB to use server certificate

Modify the `security` section in the TiDB configuration file:

{{< copyable "" >}}

```
[security]
ssl-cert ="path/to/server-cert.pem"
ssl-key ="path/to/server-key.pem"
ssl-ca="path/to/ca-cert.pem"
```

Start TiDB and check logs. If the following information is displayed in the log, the configuration is successful:

```
[INFO] [server.go:264] ["secure connection is enabled"] ["client verification enabled"=true]
```

### Configure the client to use client certificate

Configure the client so that the client uses the client key and certificate for login.

Taking the MySQL client as an example, you can use the newly created client certificate, client key and CA by specifying `ssl-cert`, `ssl-key`, and `ssl-ca`:

{{< copyable "shell-regular" >}}

```bash
mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
```

## Configure the user certificate information for login verification

First, connect TiDB using the client to configure the login verification. Then, configure the user certificate information to be verified with the following methods:

+ Configure the certificate information to be verified when creating a user (`create user`):

    {{< copyable "sql" >}}

    ```sql
    create user 'u1'@'%'  require issuer '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=TiDB admin/emailAddress=s@pingcap.com' subject '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=tpch-user1/emailAddress=zz@pingcap.com' cipher 'TLS_AES_256_GCM_SHA384';
    grant all on *.* to 'u1'@'%';
    ```

+ Configure the certificate information to be verified when granting privileges:

    {{< copyable "sql" >}}

    ```sql
    create user 'u1'@'%';
    grant all on *.* to 'u1'@'%' require issuer '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=TiDB admin/emailAddress=s@pingcap.com' subject '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=tpch-user1/emailAddress=zz@pingcap.com' cipher 'TLS_AES_256_GCM_SHA384';
    ```

+ Configure the certificate information to be verified when altering a user:

    {{< copyable "sql" >}}

    ```sql
    alter user 'u1'@'%' require issuer '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=TiDB admin/emailAddress=s@pingcap.com' subject '/C=US/ST=California/L=San Francisco/O=PingCAP Inc./OU=TiDB/CN=tpch-user1/emailAddress=zz@pingcap.com' cipher 'TLS_AES_256_GCM_SHA384';
    ```

In the above three methods, `require subject`, `require issuer`, and `require cipher` are used to check the X509 certificate attributes. You can configure one item or multiple items using the space or `and` as the separator.

+ `require subject`: Specifies the `subject` information of the client certificate when you log in. With this option specified, you do not need to configure `require ssl` or x509. The information to be specified is consistent with the entered `subject` information in [Generate client keys and certificates](#generate-client-keys-and-certificates). You can execute `openssl x509 -noout -subject -in client-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'` to configure this item.

+ `require issuer`: Specifies the `subject` information of the CA certificate that issues the user certificate. The information to be specified is consistent with the entered `subject` information in [Generate CA key and certificate](#generate-ca-key-and-certificate). You can execute `openssl x509 -noout -subject -in ca-cert.pem | sed 's/.\{8\}//'  | sed 's/, /\//g' | sed 's/ = /=/g' | sed 's/^/\//'` to configure this item.

+ `require cipher`: Checks the cipher method supported by the client. Use the `SHOW SESSION STATUS LIKE 'Ssl_cipher_list'` statement to check the list of supported cipher methods.

After the above configuration, the following items will be verified when you log in:

+ SSL is used; the CA that issues the client certificate is consistent with the CA configured in the server.
+ The `issuer` information of the client certificate matches the information specified in `require issuer`.
+ The `subject` information of the client certificate matches the information specified in `require cipher`.

You can log into TiDB only after all the above items are verified. Otherwise, the `ERROR 1045 (28000): Access denied` error is returned. You can use the following command to check the TLS version, the cipher algorithm and whether the current connection uses the certificate for the login.

{{< copyable "shell-regular" >}}

```bash
MySQL [test]> \s
--------------
mysql  Ver 15.1 Distrib 10.4.10-MariaDB, for Linux (x86_64) using readline 5.1

Connection id:       1
Current database:    test
Current user:        root@127.0.0.1
SSL:                 Cipher in use is TLS_AES_256_GCM_SHA384
```

Connect the MySQL client and execute the following statement:

{{< copyable "sql" >}}

```sql
show variables like '%ssl%';
```

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

## Update and replace certificate

The key and certificate are updated regularly. The following sections introduce how to update the key and certificate.

The CA certificate is the basis for mutual verification between the client and server. To replace the CA certificate, generate a combined certificate that supports the authentication for both old and new certificates. On the client and server, first replace the CA certificate, then replace the client/server key and certificate.

### Update CA key and certificate

1. Back up the old CA key and certificate (suppose that `ca-key.pem` is stolen):

    {{< copyable "shell-regular" >}}

    ```bash
    mv ca-key.pem ca-key.old.pem
    mv ca-cert.pem ca-cert.old.pem
    ```

2. Generate the new CA key:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl genrsa 2048 > ca-key.pem
    ```

3. Generate the new CA certificate using the newly generated CA key:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -new -x509 -nodes -days 365000 -key ca-key.pem -out ca-cert.new.pem
    ```

    > **Note:**
    >
    > Generating the new CA certificate is to replace the keys and certificates on the client and server, and to ensure that online users are not affected. Therefore, the appended information in the above command must be consistent with the `require issuer` information.

4. Generate the combined CA certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    cat ca-cert.new.pem ca-cert.old.pem > ca-cert.pem
    ```

After the above operations, restart the TiDB server with the newly created combined CA certificate. Then the server accepts both the new and old CA certificates.

Also replace the old CA certificate with the combined certificate so that the client accepts both the old and new CA certificates.

### Update client key and certificate

> **Note:**
>
> Perform the following steps **only after** you have replaced the old CA certificate on the client and server with the combined CA certificate.

1. Generate the new RSA key of the client:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout client-key.new.pem -out client-req.new.pem
    sudo openssl rsa -in client-key.new.pem -out client-key.new.pem
    ```

    > **Note:**
    >
    > The above command is to replace the client key and certificate, and to ensure that the online users are not affected. Therefore, the appended information in the above command must be consistent with the `require subject` information.

2. Use the combined certificate and the new CA key to generate the new client certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in client-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out client-cert.new.pem
    ```

3. Make the client (for example, MySQL) connect TiDB with the new client key and certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    mysql -utest -h0.0.0.0 -P4000 --ssl-cert /path/to/client-cert.new.pem --ssl-key /path/to/client-key.new.pem --ssl-ca /path/to/ca-cert.pem
    ```

### Update the server key and certificate

1. Generate the new RSA key of the server:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl req -newkey rsa:2048 -days 365000 -nodes -keyout server-key.new.pem -out server-req.new.pem
    sudo openssl rsa -in server-key.new.pem -out server-key.new.pem
    ```

2. Use the combined CA certificate and the new CA key to generate the new server certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    sudo openssl x509 -req -in server-req.new.pem -days 365000 -CA ca-cert.pem -CAkey ca-key.pem -set_serial 01 -out server-cert.new.pem
    ```

3. Configure the TiDB server to use the new server key and certificate. See [Configure TiDB server](#configure-tidb-server) for details.
