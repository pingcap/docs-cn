---
title: Back up and Restore Data on Azure Blob Storage
summary: Learn how to use BR to back up and restore data on Azure Blob Storage.
---

# Back up and Restore Data on Azure Blob Storage

The Backup & Restore (BR) tool supports using Azure Blob Storage as the external storage for backing up and restoring data.

For detailed information on other external storages supported by BR, refer to [External Storages](/br/backup-and-restore-storages.md).

## User scenario

Azure virtual machines can quickly store large-scale data on Azure Blob Storage. If you are using Azure virtual machines to deploy your cluster, you can back up your data on Azure Blob Storage.

## Usage

With BR, you can back up and restore data on Azure Blob Storage by the following two methods:

- Back up and restore data using Azure AD (Azure Active Directory)
- Back up and restore data using an access key

In common cases, to avoid exposing the key information (such as `account-key`) in command lines, it is recommended to use Azure AD.

The following is an example of backup and restore operations on Azure Blob Storage using the above two methods. The purpose of the operations are as follows:

- Back up: Back up the `test` database to a space in the `container=test` container with `t1` as the path prefix in Azure Blob Storage.
- Restore: Restore data from a space in the `container=test` container with `t1` as the path prefix in Azure Blob Storage to the `test` database.

### Method 1: Back up and restore using Azure AD (recommended)

In the operating environment of BR and TiKV, the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` must be configured. When these variables are configured, BR can use Azure AD to access Azure Blob Storage without configuring `account-key`. This method is safer and therefore recommended. `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` refer to the application ID `client_id`, the tenant ID `tenant_id`, and the client password `client_secret` of Azure application.

To learn how to check `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` are in your operating environment, or if you want to configure these environment variables as parameters, refer to [Configure environment variables as parameters](#configure-environment-variables-as-parameters).

#### Back up

When backing up data using Azure AD, you need to specify `account-name` and `access-tier`. If `access-tier` is not set (the value is empty), the value is `Hot` by default.

> **Note:**
>
> When using Azure Blob Storage as the external storage, you must set `send-credentials-to-tikv = true` (which is set by default). Otherwise, the backup task will fail.

This section shows backing up data to `cool tier`, that is, the access tier of the uploaded object is `Cool`. You can specify `account-name` and `access-tier` in two ways:

- Write the parameters information in URL parameters:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&access-tier=Cool'
    ```

- Write the parameters information in command-line parameters:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.access-tier=Cool
    ```

#### Restore

When restoring data using Azure AD, you need to specify `account-name`. You can specify it in two ways:

- Write the parameter information in URL parameters:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1'
    ```

- Write the parameter information in command-line parameters:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1
    ```

### Method 2: Back up and restore using an access key (easy)

#### Back up

When backing up data using an access key, you need to specify `account-name`, `account-key`, and `access-tier`. If `access-tier` is not set (the value is empty), the value is `Hot` by default.

> **Note:**
>
> When using Azure Blob Storage as the external storage, you must set `send-credentials-to-tikv = true` (which is set by default). Otherwise, the backup task will fail.

This section shows backing up data to `cool tier`, that is, the access tier of the uploaded object is `Cool`. You can specify `account-name`, `account-key`, and `access-tier` in two ways:

- Write the parameter information in URL parameters:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==&access-tier=Cool'
    ```

- Write the parameter information in command-line parameters:

    ```
    tiup br backup db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw== --azblob.access-tier=Cool
    ```

#### Restore

When restoring data using an access key, you need to specify `account-name` and `account-key`. You can specify the parameters in two ways:

- Write the parameters information in URL parameters:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?account-name=devstoreaccount1&account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=='
    ```

- Write the parameters information in command-line parameters:

    ```
    tiup br restore db --db test -u 127.0.0.1:2379 -s 'azure://test/t1?' --azblob.account-name=devstoreaccount1 --azblob.account-key=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==
    ```

## Parameter description

During the backup and restore process, you need to use `account-name`, `account-key`, and `access-tier`. The following is the detailed description of the parameters:

- [URL parameters](/br/backup-and-restore-storages.md#azblob-url-parameters)
- [Command-line parameters](/br/backup-and-restore-storages.md#azblob-command-line-parameters)

### Configure environment variables as parameters

When backing up and restoring data using Azure AD, the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` must be configured in the operating environment of BR and TiKV.

- When you start a cluster using TiUP, TiKV uses the "systemd" service. The following example provides how to configure the above three environment variables as parameters for TiKV:

    > **Note:**
    >
    > You need to restart TiKV in Step 3. If your TiKV cannot be restarted, you can back up and restore data using the [Method 2](#method-2-back-up-and-restore-using-an-access-key-easy).

    1. Suppose that the TiKV port on this node is `24000`, that is, the name of the "systemd" service is "tikv-24000":

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

- For TiKV and BR started with command lines, to configure the Azure AD information for them, you only need to check whether the environment variables `$AZURE_CLIENT_ID`, `$AZURE_TENANT_ID`, and `$AZURE_CLIENT_SECRET` are configured in the operating environment. You can check whether the variables are in the operating environment of BR and TiKV by running the following commands:

    ```shell
    echo $AZURE_CLIENT_ID
    echo $AZURE_TENANT_ID
    echo $AZURE_CLIENT_SECRET
    ```

## Compatibility

This feature is **only compatible** with v5.4.0 and later versions.