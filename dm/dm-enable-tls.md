---
title: Enable TLS for DM Connections
summary: Learn how to enable TLS for DM connections.
---

# Enable TLS for DM Connections

This document describes how to enable encrypted data transmission for DM connections, including connections between the DM-master, DM-worker, and dmctl components, and connections between DM and the upstream or downstream database.

## Enable encrypted data transmission between DM-master, DM-worker, and dmctl

This section introduces how to enable encrypted data transmission between DM-master, DM-worker, and dmctl.

### Configure and enable encrypted data transmission

1. Prepare certificates.

    It is recommended to prepare a server certificate for DM-master and DM-worker separately. Make sure that the two components can authenticate each other. You can choose to share one client certificate for dmctl.

    To generate self-signed certificates, you can use `openssl`, `cfssl` and other tools based on `openssl`, such as `easy-rsa`.

    If you choose `openssl`, you can refer to [generating self-signed certificates](/dm/dm-generate-self-signed-certificates.md).

2. Configure certificates.

    > **Note:**
    >
    > You can configure DM-master, DM-worker, and dmctl to use the same set of certificates.

    - DM-master

        Configure in the configuration file or command-line arguments:

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/master-cert.pem"
        ssl-key = "/path/to/master-key.pem"
        ```

    - DM-worker

        Configure in the configuration file or command-line arguments:

        ```toml
        ssl-ca = "/path/to/ca.pem"
        ssl-cert = "/path/to/worker-cert.pem"
        ssl-key = "/path/to/worker-key.pem"
        ```

    - dmctl

        After enabling encrypted transmission in a DM cluster, if you need to connect to the cluster using dmctl, specify the client certificate. For example:

        {{< copyable "shell-regular" >}}

        ```bash
        ./dmctl --master-addr=127.0.0.1:8261 --ssl-ca /path/to/ca.pem --ssl-cert /path/to/client-cert.pem --ssl-key /path/to/client-key.pem
        ```

### Verify component caller's identity

The Common Name is used for caller verification. In general, the callee needs to verify the caller's identity, in addition to verifying the key, the certificates, and the CA provided by the caller. For example, DM-worker can only be accessed by DM-master, and other visitors are blocked even though they have legitimate certificates.

To verify component caller's identity, you need to mark the certificate user identity using `Common Name` (CN) when generating the certificate, and to check the caller's identity by configuring the `Common Name` list for the callee.

- DM-master

    Configure in the configuration file or command-line arguments:

    ```toml
    cert-allowed-cn = ["dm"]
    ```

- DM-worker

    Configure in the configuration file or command-line arguments:

    ```toml
    cert-allowed-cn = ["dm"]
    ```

### Reload certificates

To reload the certificates and the keys, DM-master, DM-worker, and dmctl reread the current certificates and the key files each time a new connection is created.

When the files specified by `ssl-ca`, `ssl-cert` or `ssl-key` are updated, restart DM components to reload the certificates and the key files and reconnect with each other.

## Enable encrypted data transmission between DM components and the upstream or downstream database

This section introduces how to enable encrypted data transmission between DM components and the upstream or downstream database.

### Enable encrypted data transmission for upstream database

1. Configure the upstream database, enable the encryption support, and set the server certificate. For detailed operations, see [Using encrypted connections](https://dev.mysql.com/doc/refman/8.0/en/using-encrypted-connections.html).

2. Set the MySQL client certificate in the source configuration file:

    > **Note:**
    >
    > Make sure that all DM-master and DM-worker components can read the certificates and the key files via specified paths.

    ```yaml
    from:
        security:
            ssl-ca: "/path/to/mysql-ca.pem"
            ssl-cert: "/path/to/mysql-cert.pem"
            ssl-key: "/path/to/mysql-key.pem"
    ```

### Enable encrypted data transmission for downstream TiDB

1. Configure the downstream TiDB to use encrypted connections. For detailed operatons, refer to [Configure TiDB server to use secure connections](/enable-tls-between-clients-and-servers.md#configure-tidb-server-to-use-secure-connections).

2. Set the TiDB client certificate in the task configuration file:

    > **Note:**
    >
    > Make sure that all DM-master and DM-worker components can read the certificates and the key files via specified paths.

    ```yaml
    target-database:
        security:
            ssl-ca: "/path/to/tidb-ca.pem"
            ssl-cert: "/path/to/tidb-client-cert.pem"
            ssl-key: "/path/to/tidb-client-key.pem"
    ```
