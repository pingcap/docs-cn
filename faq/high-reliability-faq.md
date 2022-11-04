---
title: High Reliability FAQs
summary: Learn about the FAQs related to high reliability of TiDB.
---

# High Reliability FAQs

This document summarizes the FAQs related to high reliability of TiDB.

## Does TiDB support data encryption?

Yes. To encrypt data in the network traffic, you can [enable TLS between TiDB clients and servers](/enable-tls-between-clients-and-servers.md). To encrypt data in the storage engine, you can enable [transparent data encryption (TDE)](/encryption-at-rest.md).

## Does TiDB support modifying the MySQL version string of the server to a specific one that is required by the security vulnerability scanning tool?

- Since v3.0.8, TiDB supports modifying the version string of the server by modifying [`server-version`](/tidb-configuration-file.md#server-version) in the configuration file.

- Since v4.0, if you deploy TiDB using TiUP, you can also specify the proper version string by executing `tiup cluster edit-config <cluster-name>` to edit the following section:

    ```
    server_configs:
      tidb:
        server-version: 'YOUR_VERSION_STRING'
    ```

    Then, use the `tiup cluster reload <cluster-name> -R tidb` command to make the preceding modification effective to avoid the failure of security vulnerability scan.

## What authentication protocols does TiDB support? What's the process?

Like MySQL, TiDB supports the SASL protocol for user login authentication and password processing.

When the client connects to TiDB, the challenge-response authentication mode starts. The process is as follows:

1. The client connects to the server.
2. The server sends a random string challenge to the client.
3. The client sends the username and response to the server.
4. The server verifies the response.

## How to modify the user password and privilege?

To modify the user password in TiDB, it is recommended to use `ALTER USER` (for example, `ALTER USER 'test'@'localhost' IDENTIFIED BY 'mypass';`), not `UPDATE mysql.user` which might lead to the condition that the password in other nodes is not refreshed timely.

It is recommended to use the official standard statements when modifying the user password and privilege. For details, see [TiDB user account management](/user-account-management.md).
