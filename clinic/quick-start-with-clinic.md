---
title: Quick Start Guide for PingCAP Clinic
summary: Learn how to use PingCAP Clinic to collect, upload, and view cluster diagnosis data quickly.
---

# Quick Start Guide for PingCAP Clinic

This document describes how to use PingCAP Clinic diagnosis service (PingCAP Clinic) to collect, upload, and view cluster diagnosis data quickly.

PingCAP Clinic consists of two components: Diag client (shorten as Diag) and [Clinic Server cloud service](https://clinic.pingcap.com.cn) (shorten as Clinic Server). For details of two components, refer to [PingCAP Clinic Overview](/clinic/clinic-introduction.md).

When your cluster has some problems, if you need to contact PingCAP technical support, you can perform the following operations to facilitate the remote troubleshooting: collect diagnostic data with Diag, upload the collected data to the Clinic Server, and provide the data access link to the technical support staff.

PingCAP Clinic is currently in the Technical Preview stage.

> **Note:**
>
> - The following methods to collect and upload data are only applicable to [clusters deployed with TiUP](/production-deployment-using-tiup.md).
> - The diagnostic data collected by PingCAP Clinic is **only** used for troubleshooting cluster problems.

## Prerequisites

Before using PingCAP Clinic, you need to install Diag and prepare an environment for uploading data.

1. On your control machine with TiUP installed, run the following command to install Diag:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup install diag
    ```

2. Log in to [Clinic Server](https://clinic.pingcap.com.cn) and select **Sign in with AskTUG** to enter the AskTUG community login page. If you do not have an AskTUG account, you can register on the login page.

3. Create an organization on the Clinic Server. Organization is a collection of TiDB clusters. You can upload diagnostic data on the created organization.

4. Get an access token to upload data. When uploading collected data through Diag, you need a token for user authentication to ensure the data is isolated securely. If you already get a token from the Clinic Server, you can reuse the token.

    To get a token, click the icon in the lower-right corner of the Cluster page, and select **Get Access Token For Diag Tool**. Then, click **+** in the pop-up window, and copy and save the displayed token information.

    ![An example of a token](/media/clinic-get-token.png)

    > **Note:**
    >
    > - For data security, TiDB only displays the token information when it is created. If you lost the information, you can delete the old token and create a new one.
    > - A token is only used for uploading data.

5. Set the token in Diag.

    For example:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag config clinic.token ${token-value}
    ```

6. (Optional) Enable log redaction.

    When TiDB provides detailed log information, it might print sensitive information (for example, user data) in the log. If you want to avoid leaking sensitive information in the local log and Clinic Server, you can enable log redaction in the TiDB side. For more information, see [log redaction](/log-redaction.md#log-redaction-in-tidb-side).

## Steps

1. Run Diag to collect diagnostic data.

    For example, to collect the diagnostic data from 4 hours ago to 2 hours ago based on the current time, run the following command:

    {{< copyable "shell-regular" >}}

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    After you run the command, Diag does not start collecting data immediately. Instead, Diag provides the estimated data size and the target data storage path in the output for you to confirm whether to continue. To confirm that you want to start collecting data, enter `Y`.

    After the collection is complete, Diag provides the folder path where the collected data is located.

2. Upload the collected data to Clinic Server.

    > **Note:**
    >
    > The size of data (the folder with collected data) to be uploaded should be **no larger than** 10 GB. Otherwise, the data upload fails.

    - If the network where your cluster is located can access the internet, you can directly upload the folder with collected data using the following command:

        {{< copyable "shell-regular" >}}

        ```bash
        tiup diag upload ${filepath}
        ```

        After the upload is completed, the `Download URL` is displayed in the output.

        > **Note:**
        >
        > When uploading data using this method, you need to use Diag v0.7.0 or a later version. You can get the Diag version when you run it. If the Diag version is earlier than 0.7.0, you can use the `tiup update diag` command to upgrade Diag to the latest version.

    - If the network where your cluster is located cannot access the internet, you need to pack the collected data and upload the package. For details, see [Method 2. Pack and upload data](/clinic/clinic-user-guide-for-tiup.md#method-2-pack-and-upload-data).

3. After the upload is complete, get the data access link from `Download URL` in the command output.

    By default, the diagnostic data includes the cluster name, cluster topology information, log content in the collected diagnostic data, and Grafana Dashboard information reorganized based on the metrics in the collected data.

    You can use the data to troubleshoot cluster problems by yourself, or you can provide the data access link to PingCAP technical support staff to facilitate the remote troubleshooting.

## What's next

- [PingCAP Clinic Overview](/clinic/clinic-introduction.md)
- [Use PingCAP Clinic](/clinic/clinic-user-guide-for-tiup.md)
- [PingCAP Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md)