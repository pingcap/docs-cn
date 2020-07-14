---
title: Generate Self-signed Certificates
summary: Use `openssl` to generate self-signed certificates.
aliases: ['/docs/dev/generate-self-signed-certificates/','/docs/dev/how-to/secure/generate-self-signed-certificates/']
---

# Generate Self-signed Certificates

This document provides an example of using `openssl` to generate a self-signed certificate. You can also generate certificates and keys that meet requirements according to your demands.

Assume that the topology of the instance cluster is as follows:

| Name  | Host IP      | Services   |
| ----- | -----------  | ---------- |
| node1 | 172.16.10.11 | PD1, TiDB1 |
| node2 | 172.16.10.12 | PD2        |
| node3 | 172.16.10.13 | PD3        |
| node4 | 172.16.10.14 | TiKV1      |
| node5 | 172.16.10.15 | TiKV2      |
| node6 | 172.16.10.16 | TiKV3      |

## Install OpenSSL

- For Debian or Ubuntu OS:

    {{< copyable "shell-regular" >}}

    ```bash
    apt install openssl
    ```

- For RedHat or CentOS OS:

    {{< copyable "shell-regular" >}}

    ```bash
    yum install openssl
    ```

You can also refer to OpenSSL's official [download document](https://www.openssl.org/source/) for installation.

## Generate the CA certificate

A certificate authority (CA) is a trusted entity that issues digital certificates. In practice, contact your administrator to issue the certificate or use a trusted CA. CA manages multiple certificate pairs. Here you only need to generate an original pair of certificates as follows.

1. Generate the root key:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl genrsa -out root.key 4096
    ```

2. Generate root certificates:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl req -new -x509 -days 1000 -key root.key -out root.crt
    ```

3. Validate root certificates:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -text -in root.crt -noout
    ```

## Issue certificates for individual components

This section describes how to issue certificates for individual components.

### Certificates that might be used in the cluster

- tidb-server certificate: used by TiDB to authenticate TiDB for other components and clients
- tikv-server certificate: used by TiKV to authenticate TiKV for other components and clients
- pd-server certificate: used by PD to authenticate PD for other components and clients
- client certificate: used to authenticate the clients from PD, TiKV and TiDB, such as `pd-ctl`, `tikv-ctl`

### Issue certificates to TiKV instances

To issue a certificate to a TiKV instance, perform the following steps:

1. Generate the private key corresponding to the certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl genrsa -out tikv.key 2048
    ```

2. Make a copy of the OpenSSL configuration template file (Refer to the actual location of your template file because it might have more than one location):

    {{< copyable "shell-regular" >}}

    ```bash
    cp /usr/lib/ssl/openssl.cnf .
    ```

    If you do not know the actual location, look for it in the root directory:

    ```bash
    find / -name openssl.cnf
    ```

3. Edit `openssl.cnf`, add `req_extensions = v3_req` under the `[ req ]` field, and add `subjectAltName = @alt_names` under the `[ v3_req ]` field. Finally, create a new field and edit the information of SAN.

    ```
    [ alt_names ]
    IP.1 = 127.0.0.1
    IP.2 = 172.16.10.14
    IP.3 = 172.16.10.15
    IP.4 = 172.16.10.16
    ```

4. Save the `openssl.cnf` file, and generate the certificate request file (in this step, you can also assign a Common Name to the certificate, which is used to allow the server to validate the identity of the client. Each component does not enable the validation by default, and you can enable it in the configuration file):

    {{< copyable "shell-regular" >}}

    ```bash
    openssl req -new -key tikv.key -out tikv.csr -config openssl.cnf
    ```

5. Issue and generate the certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in tikv.csr -out tikv.crt -extensions v3_req -extfile openssl.cnf
    ```

6. Verify that the certificate includes the SAN field (optional):

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -text -in tikv.crt -noout
    ```

7. Confirm that the following files exist in your current directory:

    ```
    root.crt
    tikv.crt
    tikv.key
    ```

The process of issuing certificates for other TiDB components is similar and will not be repeated in this document.

### Issue certificates for clients

To issue a certificate to a client, perform the following steps:

1. Generate the private key corresponding to the certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl genrsa -out client.key 2048
    ```

2. Generate the certificate request file (in this step, you can also assign a Common Name to the certificate, which is used to allow the server to validate the identity of the client. Each component does not enable the validation by default, and you can enable it in the configuration file):

    {{< copyable "shell-regular" >}}

    ```bash
    openssl req -new -key client.key -out client.csr
    ```

3. Issue and generate the certificate:

    {{< copyable "shell-regular" >}}

    ```bash
    openssl x509 -req -days 365 -CA root.crt -CAkey root.key -CAcreateserial -in client.csr -out client.crt
    ```
