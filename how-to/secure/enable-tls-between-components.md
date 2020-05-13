---
title: Enable TLS Authentication and Encrypt the Stored Data
summary: Learn how to enable TLS authentication and encrypt the stored data in a TiDB cluster.
category: how-to
---

# Enable TLS Authentication and Encrypt the Stored Data

This document introduces how to enable TLS authentication and encrypt the stored data in a TiDB cluster.

## Enable TLS Authentication

This section describes how to enable TLS authentication in a TiDB cluster. TLS authentication can be applied to the following scenarios:

- The **mutual authentication** between TiDB components, including the authentication among TiDB, TiKV, and PD; the authentication between TiDB Control and TiDB, between TiKV Control and TiKV, between PD Control and PD; the authentication between TiKV peers, and between PD peers. Once enabled, the mutual authentication applies to all components, rather than to part of the components.
- The **one-way** and **mutual authentication** between the TiDB server and the MySQL Client.

> **Note:**
>
> The authentication between the MySQL Client and the TiDB server uses one set of certificates, while the authentication among TiDB components uses another set of certificates.

## Enable mutual TLS authentication among TiDB components

1. Prepare certificates.

    It is recommended to prepare a server certificate for TiDB, TiKV, and PD separately. Make sure that these components can authenticate each other. The clients of TiDB, TiKV, and PD share one client certificate.

    You can use tools like `openssl`, `easy-rsa` and `cfssl` to generate self-signed certificates.

    If you choose `cfssl`, you can refer to [generating self-signed certificates](/how-to/secure/generate-self-signed-certificates.md).

2. Configure certificates.

   To enable mutual authentication among TiDB components, configure the certificates of TiDB, TiKV, and PD as follows.

   - TiDB

        Configure in the configuration file or command line arguments:

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs for connection with cluster components.
        cluster-ssl-ca = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format for connection with cluster components.
        cluster-ssl-cert = "/path/to/tidb-server.pem"
        # Path of file that contains X509 key in PEM format for connection with cluster components.
        cluster-ssl-key = "/path/to/tidb-server-key.pem"
        ```

   - TiKV

        Configure in the configuration file or command line arguments, and set the corresponding URL to https:

        ```toml
        [security]
        # set the path for certificates. Empty string means disabling secure connections.
        ca-path = "/path/to/ca.pem"
        cert-path = "/path/to/tikv-server.pem"
        key-path = "/path/to/tikv-server-key.pem"
        ```

   - PD

        Configure in the configuration file or command line arguments, and set the corresponding URL to https:

        ```toml
        [security]
        # Path of file that contains list of trusted SSL CAs. If set, following four settings shouldn't be empty
        cacert-path = "/path/to/ca.pem"
        # Path of file that contains X509 certificate in PEM format.
        cert-path = "/path/to/pd-server.pem"
        # Path of file that contains X509 key in PEM format.
        key-path = "/path/to/pd-server-key.pem"
        ```

    After certificates are configured as above, mutual authentication among TiDB components is enabled.

    > **Note:**
    >
    > If you have enabled TLS in a TiDB cluster when you connect to the cluster using tidb-ctl, tikv-ctl, or pd-ctl, you need to specify the client certificate. For example:

    {{< copyable "shell-regular" >}}

    ```bash
    ./tidb-ctl -u https://127.0.0.1:10080 --ca /path/to/ca.pem --ssl-cert /path/to/client.pem --ssl-key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./pd-ctl -u https://127.0.0.1:2379 --cacert /path/to/ca.pem --cert /path/to/client.pem --key /path/to/client-key.pem
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl --host="127.0.0.1:20160" --ca-path="/path/to/ca.pem" --cert-path="/path/to/client.pem" --key-path="/path/to/clinet-key.pem"
    ```

3. Configure Common Name.

    The Common Name is used for caller verification. In general, the callee needs to verify the caller's identity, in addition to verifying the key, the certificates, and the CA provided by the caller. For example, TiKV can only be accessed by TiDB, and other visitors are blocked even though they have legitimate certificates. It is recommended to mark the certificate user identity using `Common Name` when generating the certificate, and to check the caller's identity by configuring the `Common Name` list for the callee.

    - TiDB

        Configure in the configuration file or command line arguments:

        ```toml
        [security]
        cluster-verify-cn = [
            "TiDB-Server",
            "TiKV-Control",
        ]
        ```

    - TiKV

        Configure in the configuration file or command line arguments:

        ```toml
        [security]
        cert-allowed-cn = [
            "TiDB-Server", "PD-Server", "TiKV-Control", "RawKvClient1",
        ]
        ```

    - PD

        Configure in the configuration file or command line arguments:

        ```toml
        [security]
        cert-allowed-cn = ["TiKV-Server", "TiDB-Server", "PD-Control"]
        ```

4. Reload certificates.

    To reload the certificates and the keys, TiDB, PD, and TiKV reread the current certificates and the key files each time a new connection is created. Currently, you cannot reload the CA certificate. 

## Enable TLS authentication between the MySQL client and TiDB server

Refer to [Use Encrypted Connections](/how-to/secure/enable-tls-clients.md).

## Encrypt stored data

In a TiDB cluster, user data is stored in TiKV. Once you configure the encrypted storage feature in TiKV, the TiDB cluster encrypts this data. This section introduces how to configure the data encryption feature in TiKV.

1. Generate the token file.

    The token file stores the keys used to encrypt the user data and to decrypt the encrypted data.

    {{< copyable "shell-regular" >}}

    ```bash
    ./tikv-ctl random-hex --len 256 > cipher-file-256
    ```

    > **Note:**
    >
    > You can only use the hex-formatted token file. The file length must be 2 to the power of N, and is less than or equal to 1024.

2. Configure TiKV as follows.

    ```toml
    [security]
    # Storage path of the Cipher file.
    cipher-file = "/path/to/cipher-file-256"
    ```

> **Note:**
>
> When you import data into a cluster using [TiDB Lightning](/reference/tools/tidb-lightning/overview.md), if the storage encryption feature is enabled in the target cluster, the SST files generated by TiDB Lightning must be encrypted.

### Limitations

The limitations of the storage encryption feature are as follows:

- If the feature has not been enabled in the cluster before, you cannot enable this feature.
- If the feature is enabled in the cluster, you cannot disable this feature.
- You cannot enable the feature for some TiKV instances while disabling it for other instances in one cluster. You can only enable or disable this feature for all TiKV instances. This is because if you enable the encrypted storage feature, data are encrypted during data migration.
