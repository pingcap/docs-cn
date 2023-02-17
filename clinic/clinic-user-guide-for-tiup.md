---
title: Troubleshoot Clusters Using PingCAP Clinic
summary: Learn how to use the PingCAP Clinic Diagnostic Service to troubleshoot cluster problems remotely and perform a quick check of the cluster status on a TiDB cluster or DM cluster deployed using TiUP.
---

# Troubleshoot Clusters Using PingCAP Clinic

For TiDB clusters and DM clusters deployed using TiUP, you can use PingCAP Clinic Diagnostic Service (PingCAP Clinic) to troubleshoot cluster problems remotely and perform a quick check on cluster status locally using [Diag client (Diag)](https://github.com/pingcap/diag) and Clinic Server.

> **Note:**
>
> - This document **only** applies to clusters deployed using TiUP in an on-premises environment. For clusters deployed using TiDB Operator on Kubernetes, see [PingCAP Clinic for TiDB Operator environments](https://docs.pingcap.com/tidb-in-kubernetes/stable/clinic-user-guide).
>
> - PingCAP Clinic **does not support** collecting data from clusters deployed using TiDB Ansible.

## User scenarios

- [Troubleshoot cluster problems remotely](#troubleshoot-cluster-problems-remotely)

    - When your cluster has some problems, if you need to [get support](/support.md) from PingCAP, you can perform the following operations to facilitate the remote troubleshooting: collect diagnostic data with Diag, upload the collected data to the Clinic Server, and provide the data access link to the technical support staff.
    - When your cluster has some problems, if you cannot analyze the problems immediately, you can use Diag to collect and save the data for later analysis.

- [Perform a quick check on the cluster status locally](#perform-a-quick-check-on-the-cluster-status-locally)

    Even if your cluster is running stably for now, it is necessary to periodically check the cluster to detect potential stability risks. You can identify potential health risks of a cluster using the local quick check feature provided by PingCAP Clinic. The local check only checks configuration. To check more items, such as metrics and logs, it is recommended to upload the diagnostic data to the Clinic Server and use the Health Report feature.

## Prerequisites

Before using PingCAP Clinic, you need to install Diag (a component to collect data provided by PingCAP Clinic) and prepare the environment to upload data.

1. Install Diag.

   - If you have installed TiUP on your control machine, run the following command to install Diag:

        ```bash
        tiup install diag
        ```

    - If you have installed Diag, you can use the following command to upgrade Diag to the latest version:

        ```bash
        tiup update diag
        ```

    > **Note:**
    >
    > - For clusters without an internet connection, you need to deploy Diag offline. For details, refer to [Deploy TiUP offline: Method 2](/production-deployment-using-tiup.md#deploy-tiup-offline).
    > - Diag is **only** provided in the TiDB Server offline mirror package of v5.4.0 or later.

2. Get and set an access token (token) to upload data.

    When uploading collected data through Diag, you need a token for user authentication. If you already set a token Diag, you can reuse the token and skip this step.

    To get a token, perform the following steps:

    - Log in to the Clinic Server.

        <SimpleTab groupId="clinicServer">
        <div label="Clinic Server for international users" value="clinic-us">

        [Clinic Server for international users](https://clinic.pingcap.com): Data is stored in AWS in US.

        </div>
        <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

        [Clinic Server for users in the Chinese mainland](https://clinic.pingcap.com.cn): Data is stored in AWS in China (Beijing) regions.

        </div>

        </SimpleTab>

    - Click the icon in the lower-right corner of the Cluster page, select **Get Access Token For Diag Tool**, and click **+** in the pop-up window. Make sure that you have copied and saved the token that is displayed.

        ![Get the Token](/media/clinic-get-token.png)

    > **Note:**
    >
    > - When accessing Clinic Server for the first time, before getting a token, you need to prepare the environment by referring to [Quick Start with PingCAP Clinic](/clinic/quick-start-with-clinic.md#prerequisites).
    > - For data security, TiDB only displays the token upon the token creation. If you have lost the token, delete the old token and create a new one.
    > - A token is only used for uploading data.

    - Then, set the token in Diag. For example:

        ```bash
        tiup diag config clinic.token ${token-value}
        ```

3. Set the `region` in Diag.

    `region` determines the encryption certificate used for packing data and the target service when uploading the data. For example:

    > **Note:**
    >
    > - Diag v0.9.0 and later versions support setting `region`.
    > - For versions earlier than Diag v0.9.0, data is uploaded to Clinic Server in the Chinese region by default. To set `region` in these versions, run the `tiup update diag` command to upgrade Diag to the latest version and then set `region` in Diag.

    <SimpleTab groupId="clinicServer">
    <div label="Clinic Server for international users" value="clinic-us">

    When using Clinic Server for international users, set `region` to `US` using the following command:

    ```bash
    tiup diag config clinic.region US
    ```

    </div>
    <div label="Clinic Server for users in the Chinese mainland" value="clinic-cn">

    When using Clinic Server for users in the Chinese mainland, set `region` to `CN` using the following command:

    ```bash
    tiup diag config clinic.region CN
    ```

    </div>

    </SimpleTab>

4. (Optional) Enable log redaction.

    When TiDB provides detailed log information, it might print sensitive information (for example, user data) in the log. If you want to avoid leaking sensitive information in the local log and Clinic Server, you can enable log redaction in the TiDB side. For more information, see [log redaction](/log-redaction.md#log-redaction-in-tidb-side).

## Troubleshoot cluster problems remotely

You can use Diag to quickly collect diagnostic data from TiDB clusters and DM clusters, including monitoring data and configuration information.

### Step 1. Check the data to be collected

For a full list of data that can be collected by Diag, see [PingCAP Clinic Diagnostic Data](/clinic/clinic-data-instruction-for-tiup.md).

To improve the efficiency of the later diagnosis, you are recommended to collect full diagnostic data including monitoring data and configuration information. For details, see [Collect data from clusters](#step-2-collect-data).

### Step 2. Collect data

With Diag, you can collect data from the TiDB clusters and the DM clusters deployed using TiUP.

1. Run the data collection command of Diag.

    For example, to collect the diagnostic data from 4 hours ago to 2 hours ago based on the current time, run the following command:

    <SimpleTab>
    <div label="TiDB Cluster">

    ```bash
    tiup diag collect ${cluster-name} -f="-4h" -t="-2h"
    ```

    </div>
    <div label="DM Cluster">

    ```bash
    tiup diag collectdm ${dm-cluster-name} -f="-4h" -t="-2h"
    ```

    </div>
    </SimpleTab>

    Descriptions of the parameters for data collection:

    - `-f/--from`: specifies the start time of the data collection. If you do not specify this parameter, the default start time is 2 hours before the current time. To modify the time zone, use the `-f="12:30 +0800"` syntax. If you do not specify the time zone information in this parameter, such as `+0800`, the time zone is UTC by default.
    - `-t/--to`: specifies the end time of the data collection. If you do not specify this parameter, the default end time is the current moment. To modify the time zone, use the `-f="12:30 +0800"` syntax. If you do not specify the time zone information in this parameter, such as `+0800`, the time zone is UTC by default.

    Parameter usage tips:

    In addition to specifying the data collection time, you can use Diag to specify more parameters. To get all parameters, run the `tiup diag collect -h` or `tiup diag collectdm -h` command.

    > **Note:**
    >
    > - Diag does not collect system variables data (db_vars) by default. To collect this data, you need to additionally provide a username and password that can access the database. Note that the reading access to system variables should be enabled in this database.
    > - Diag does not collect performance data (`perf`) and debug data (`debug`) by default.
    > - To collect full diagnostic data including system variables, use the command `tiup diag collect <cluster-name> --include="system,monitor,log,config,db_vars,perf,debug"`.

    - `-l`: the bandwidth limit for transferring files, the unit is Kbit/s, and the default value is `100000` (the `-l` parameter of scp).
    - `-N/--node`: only collects data from a specified node. The format is `ip:port`.
    - `--include`: only collects specific types of data. The optional values are `system`, `monitor`, `log`, `config`, and `db_vars`. To include two or more types, you can use `,` as a separator between the types.
    - `--exclude`: does not collect specific types of data. The optional values are `system`, `monitor`, `log`, `config`, and `db_vars`. To exclude two or more types, you can use `,` as a separator between the types.

    After you run the command, Diag does not start collecting data immediately. Instead, Diag provides the estimated data size and the target data storage path in the output for you to confirm whether to continue. For example:

    ```bash
    Estimated size of data to collect:
    Host               Size       Target
    ----               ----       ------
    172.16.7.129:9090  43.57 MB   1775 metrics, compressed
    172.16.7.87        0 B        /tidb-deploy/tidb-4000/log/tidb_stderr.log
    ... ...
    172.16.7.179       325 B      /tidb-deploy/tikv-20160/conf/tikv.toml
    Total              2.01 GB    (inaccurate)
    These data will be stored in /home/user/diag-fNTnz5MGhr6
    Do you want to continue? [y/N]: (default=N)
    ```

2. Enter `Y` to confirm that you want to start collecting data.

    Collecting data takes a certain amount of time. The time varies according to the volume of data to be collected. For example, in a test environment, collecting 1 GB of data takes about 10 minutes.

    After the collection is complete, Diag provides the folder path where the collected data is located. For example:

    ```bash
    Collected data are stored in /home/user/diag-fNTnz5MGhr6
    ```

### Step 3. View data locally (optional)

The collected data is stored in separate subdirectories based on its data source. These subdirectories are named after machine names and port numbers. The storage locations of the configuration, logs, and other files of each node are the same as their relative storage paths in the real server of your TiDB cluster:

- Basic information of the system and hardware: in `insight.json`
- Contents in the system `/etc/security/limits.conf`: in `limits.conf`
- List of kernel parameters: in `sysctl.conf`
- Kernel logs: in `dmesg.log`
- Network connection during data collection: in `ss.txt`
- Configuration data: in the `config.json` directory of each node
- Meta-information for the cluster itself: in `meta.yaml` (this file is located at the top level of the directory that stores collected data)
- Monitoring data: in the `/monitor` file directory. The monitoring data is compressed by default and cannot be viewed directly. To directly view the JSON files with monitoring data, disable compression with the `--compress-metrics=false` parameter when collecting data.

### Step 4. Upload data

To provide cluster diagnostic data to PingCAP technical support staff, you need to upload the data to the Clinic Server first, and then send the obtained data access link to the staff. The Clinic Server is a cloud service that stores and shares diagnostic data securely.

Depending on the network connection of the cluster, you can choose one of the following methods to upload data:

- Methods 1: if the network where the cluster is located can access the internet, you can [directly upload data using the upload command](#method-1-upload-directly).
- Methods 2: if the network where the cluster is located cannot access the internet, you need to [pack the data and then upload it](#method-2-pack-and-upload-data).

> **Note:**
>
> If you did not set a token or `region` in Diag before uploading data, Diag reports the upload failure and reminds you to set a token or `region`. To set a token, see [the second step in Prerequisites](#prerequisites).

#### Method 1. Upload directly

If the network where the cluster is located can access the internet, you can directly upload the folder with collected data obtained in [Step 2: Collect data](#step-2-collect-data) using the following command:

{{< copyable "shell-regular" >}}

```bash
tiup diag upload
```

After the upload is completed, the `Download URL` is displayed in the output. You can open the link of `Download URL` to see the uploaded data or send the link to the PingCAP technical support staff you contacted before.

#### Method 2. Pack and upload data

If the network where your cluster is located cannot access the internet, you need to pack the data on your intranet and upload the data package to the Clinic Server using a device with internet access. The detailed operations are as follows:

1. Pack the collected data obtained in [Step 2. Collect data](#step-2-collect-data) by running the following command:

    ```bash
    tiup diag package ${filepath}
    ```

    During packaging, Diag encrypts and compresses the data at the same time. In the test environment, 800 MB of data was compressed to 57 MB. The following is an example output:

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag package diag-fNTnz5MGhr6
    packaged data set saved to /home/user/diag-fNTnz5MGhr6.diag
    ```

    After the packaging is complete, the data is packaged to the `.diag` format. The `.diag` file can only be decrypted and viewed after being uploaded to the Clinic Server. If you want to directly forward the collected data instead of uploading it to the Clinic Server, you can compress the data by your own method and forward it.

2. From a machine with internet access, upload the compressed data package:

    ```bash
    tiup diag upload ${filepath}
    ```

    The following is an example output:

    ```bash
    [root@Copy-of-VM-EE-CentOS76-v1 user]# tiup diag upload /home/user/diag-fNTnz5MGhr6
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag upload /home/user/diag-fNTnz5MGhr6
    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>><>>>>>>>>>
    Completed!
    Download URL: "https://clinic.pingcap.com.cn/portal/#/orgs/4/clusters/XXXX"
    ```

3. After the upload is complete, you can open the link of `Download URL` to see the uploaded data or send the link to the PingCAP technical support staff you contacted before.

## Perform a quick check on the cluster status locally

You can have a quick check on the cluster status locally using Diag. Even if your cluster is running stably for now, it is necessary to periodically check the cluster to detect potential stability risks. You can identify potential health risks of a cluster using the local quick check feature provided by PingCAP Clinic. The local check only checks configuration. To check more items, such as metrics and logs, it is recommended to upload the diagnostic data to the Clinic Server and use the Health Report feature.

1. Collect configuration data:

    ```bash
    tiup diag collect ${cluster-name} --include="config"
    ```

    The data of configuration files are relatively small. After the collection, the collected data is stored in the current path by default. In the test environment, for a cluster with 18 nodes, the data size of configuration files is less than 10 KB.

2. Diagnose configuration data:

    ```bash
    tiup diag check ${subdir-in-output-data}
    ```

    `${subdir-in-output-data}` in the above command is the path that stores the collected data, and this path has the `meta.yaml` file.

3. View the diagnostic result:

    The diagnostic result is returned on the command line. For example:

    ```bash
    Starting component `diag`: /root/.tiup/components/diag/v0.7.0/diag check diag-fNTnz5MGhr6

    # Diagnostic result
    lili 2022-01-24T09:33:57+08:00

    ## 1. Cluster basic information
    - Cluster ID: 7047403704292855808
    - Cluster Name: lili
    - Cluster Version: v5.3.0

    ## 2. Sampling information
    - Sample ID: fNTnz5MGhr6
    - Sampling Date: 2022-01-24T09:33:57+08:00
    - Sample Content:: [system monitor log config]

    ## 3. Diagnostic result, including potential configuration problems
    In this inspection, 22 rules were executed.

    The results of **1** rules were abnormal and needed to be further discussed with support team.

    The following is the details of the abnormalities.

    ### Diagnostic result summary
    The configuration rules are all derived from PingCAP’s OnCall Service.

    If the results of the configuration rules are found to be abnormal, they may cause the cluster to fail.

    There were **1** abnormal results.

    #### Path to save the diagnostic result file

    Rule Name: tidb-max-days
    - RuleID: 100
    - Variation: TidbConfig.log.file.max-days
    - For more information, please visit: https://s.tidb.io/msmo6awg
    - Check Result:
      TidbConfig_172.16.7.87:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.86:4000   TidbConfig.log.file.max-days:0   warning
      TidbConfig_172.16.7.179:4000   TidbConfig.log.file.max-days:0   warning

    Result report and record are saved at diag-fNTnz5MGhr6/report-220125153215
    ```

    In the last section of the diagnostic result (under `#### Path to save the diagnostic result file` in the above example output), for each configuration potential risk found, Diag provides a corresponding knowledge base link with detailed configuration suggestions. In the example above, the relevant link is `https://s.tidb.io/msmo6awg`.

## FAQ

1. If the data upload fails, can I re-upload it?

    Yes. Data upload supports breakpoint upload. If the upload fails, you can upload it again directly.

2. After uploading data, I cannot open the returned data access link. What should I do?

    Log in to Clinic Server first. If you still cannot open the link after login success, check whether you have access to data. If not, contact the data owner for permission. After getting the permission, log in to Clinic Server and open the link again.

3. How long will the uploaded data be kept on the Clinic Server?

    The longest time is 180 days. You can delete the data you uploaded on the Clinic Server page at any time.