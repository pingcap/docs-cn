---
title: Back up and Restore Data on Azure Blob Storage Using BR
summary: Learn how to use BR to back up and restore data on Azure Blob Storage.
aliases: ['/tidb/dev/backup-and-restore-azblob/']
---

# Back up and Restore Data on Azure Blob Storage Using BR

The Backup & Restore (BR) tool supports using Azure Blob Storage as the external storage for backing up and restoring data.

## User scenario

Azure virtual machines can quickly store large-scale data on Azure Blob Storage. If you are using Azure virtual machines to deploy your cluster, you can back up your data on Azure Blob Storage.

## Usage

With BR, you can back up and restore data on Azure Blob Storage by the following two methods:

- Back up and restore data using Azure AD (Azure Active Directory)
- Back up and restore data using an access key

In common cases, to avoid exposing the key information (such as `account-key`) in command lines, it is recommended to use Azure AD.

The following is an example of backup and restoration operations on Azure Blob Storage using the preceding two methods. The purpose of the operations are as follows:

- Back up: Back up the `test` database to a space in the `container=test` container with `t1` as the path prefix in Azure Blob Storage.
- Restore: Restore data from a space in the `container=test` container with `t1` as the path prefix in Azure Blob Storage to the `test` database.

> **Note:**
>
> When backing up data to the Azure Blob Storage using Azure AD or an access key, you need to set `send-credentials-to-tikv = true` (which is `true` by default). Otherwise, the backup task will fail.

### Method 1: Back up and restore data using Azure AD (recommended)

This section describes how to back up and restore data using Azure AD. Before performing backup or restoration, you need to configure environment variables.

#### Configure environment variables

In the operating environment of BR and TiKV, configure the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET`.

- When you start a cluster using TiUP, TiKV uses the "systemd" service. The following example introduces how to configure the preceding three environment variables as parameters for TiKV:

    > **Note:**
    >
    > You need to restart TiKV in Step 3. If your TiKV cannot be restarted, use [Method 2](#method-2-back-up-and-restore-using-an-access-key-easy) to back up and restore data.

    1. Suppose that the TiKV port on this node is 24000, that is, the name of the "systemd" service is "tikv-24000":

        ```
        systemctl edit tikv-24000
        ```

    2. Fill in the environment variable information:

        ```
        [Service]
        Environment="AZURE_CLIENT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_TENANT_ID=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
        Environment="AZURE_CLIENT_SECRET=aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        ```

    3. Reload the configuration and restart TiKV:

        ```
        systemctl daemon-reload
        systemctl restart tikv-24000
        ```

- To configure the Azure AD information for TiKV and BR started with command lines, you only need to check whether the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` are configured in the operating environment by running the following commands:

    ```
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

For more information about the environment variables, see [Azblob URL parameters](/br/backup-and-restore-storages.md#azblob-url-parameters).

#### Back up

This section shows backing up data to `cool tier`, that is, the access tier of the uploaded object is `Cool`. You can specify `account-name` and `access-tier` in two ways. The backup operations differ depending on the way you choose:

- Specify `account-name` and `access-tier` as parameters in URL:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

    If `access-tier` is not set (the value is empty), the value is `Hot` by default.

- Specify `account-name` and `access-tier` as command-line parameters:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### Restore

Similar to how `account-name` is specified in [Back up](#back-up), you can restore data either using URLs or command-line parameters:

- Specify `account-name` as a parameter in URL:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

- Specify `account-name` as a command-line parameter:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### Method 2: Back up and restore using an access key (easy)

Compared with backing up and restoring data using Azure AD, backup and restoration using an access key is easier because you do not need to configure environment variables. Other steps are similar to those of using Azure AD.

#### Back up

- Specify `account-name`, `account-key`, and `access-tier` as parameters in URL:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

- Specify `account-name`, `account-key`, and `access-tier` as command-line parameters:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### Restore

- Specify `account-name` and `account-key` as parameters in URL:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

- Specify `account-name` and `account-key` as command-line parameters:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## Compatibility

This feature is **only compatible** with v5.4.0 and later versions.

## See also

- To learn other external storages supported by BR, see [External storages](/br/backup-and-restore-storages.md).
- To learn more about the parameters, see the following documents:

    - [Azblob URL parameters](/br/backup-and-restore-storages.md#azblob-url-parameters)
    - [Azblob command-line parameters](/br/backup-and-restore-storages.md#azblob-command-line-parameters)
