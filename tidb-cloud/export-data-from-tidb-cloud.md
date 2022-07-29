---
title: Export Data from TiDB
summary: This page has instructions for exporting data from your TiDB cluster in TiDB Cloud.
---

# Export Data from TiDB

This page describes how to export data from your cluster in TiDB Cloud.

TiDB does not lock in your data. Sometimes you still want to be able to migrate data from TiDB to other data platforms. Because TiDB is highly compatible with MySQL, any export tool suitable for MySQL can also be used for TiDB.

You can use the tool [Dumpling](https://github.com/pingcap/dumpling) for data export.

1. Download and install TiUP:

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. Declare the global environment variable:

    > **Note:**
    >
    > After the installation, TiUP displays the absolute path of the corresponding `profile` file. You need to modify `.bash_profile` in following command to the path of your `profile` file.

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. Install Dumpling.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install dumpling
    ```

4. Export your data using Dumpling from TiDB.

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dumpling -h ${tidb-endpoint} -P 3306 -u ${user} -F 67108864 -t 4 -o /path/to/export/dir
    ```

    If you want to export only the specified databases, use `-B` to specify a comma separated list of database names.

    The minimum permissions required are as follows:

    - `SELECT`
    - `RELOAD`
    - `LOCK TABLES`
    - `REPLICATION CLIENT`

    Currently, Dumpling only supports the Mydumper format output, which can be easily restored into MySQL compatible databases by using [TiDB Lightning](https://github.com/pingcap/tidb-lightning).
