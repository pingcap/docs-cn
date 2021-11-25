---
title: Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster
summary: Learn how to use PLAN REPLAYER to save and restore the on-site information of a cluster.
---

# Use PLAN REPLAYER to Save and Restore the On-Site Information of a Cluster

When you locate and troubleshoot the issues of a TiDB cluster, you often need to provide information on the system and the execution plan. To help you get the information and troubleshoot cluster issues in a more convenient and efficient way, the `PLAN REPLAY` command is introduced in TiDB v5.3.0. This command enables you to easily save and restore the on-site information of a cluster, improves the efficiency of troubleshooting, and helps you more easily archive the issue for management.

The features of `PLAN REPLAYER` are as follows:

- Exports the information of a TiDB cluster at an on-site troubleshooting to a ZIP-formatted file for storage.
- Imports into a cluster the ZIP-formatted file exported from another TiDB cluster. This file contains the information of the latter TiDB cluster at an on-site troubleshooting.

## Use `PLAN REPLAER` to export cluster information

You can use `PLAN REPLAYER` to save the on-site information of a TiDB cluster. The export interface is as follows:

{{< copyable "sql" >}}

```sql
PLAN REPLAYER DUMP EXPLAIN [ANALYZE] sql-statement;
```

Based on `sql-statement`, TiDB sorts out and exports the following on-site information:

- TiDB version
- TiDB configuration
- TiDB session variables
- TiDB SQL bindings
- The table schema in `sql-statement`
- The statistics of the table in `sql-statement`
- The result of `EXPLAIN [ANALYZE] sql-statement`

> **Note:**
>
> `PLAN REPLAYER` **DOES NOT** export any table data.

### Examples of exporting cluster information

{{< copyable "sql" >}}

```sql
use test;
create table t(a int, b int);
insert into t valuse(1,1), (2, 2), (3, 3);
analyze table t;

plan replayer dump explain select * from t;
```

`PLAN REPLAYER DUMP` packages the table information above into a `ZIP` file and returns the file identifier as the execution result. This file is a one-time file. After the file is downloaded, TiDB will delete it.

> **Note:**
>
> The `ZIP` file is stored in a TiDB cluster for at most one hour. After one hour, TiDB will delete it.

```sql
MySQL [test]> plan replayer dump explain select * from t;
+------------------------------------------------------------------+
| Dump_link                                                        |
+------------------------------------------------------------------+
| replayer_single_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip |
+------------------------------------------------------------------+
1 row in set (0.015 sec)
```

Because the file cannot be downloaded on MySQL Client, you need to use the TiDB HTTP interface and the file identifier to download the file:

{{< copyable "shell-regular" >}}

```shell
http://${tidb-server-ip}:${tidb-server-status-port}/plan_replayer/dump/${file_token}
```

`${tidb-server-ip}:${tidb-server-status-port}` is the address of any TiDB server in the cluster. For example:

{{< copyable "shell-regular" >}}

```shell
curl http://127.0.0.1:10080/plan_replayer/dump/replayer_single_JOGvpu4t7dssySqJfTtS4A==_1635750890568691080.zip > plan_replayer.zip
```

## Use `PLAN REPLAYER` to import cluster information

> **Warning:**
>
> When you import the on-site information of a TiDB cluster to another cluster, the TiDB session variables, SQL bindings, table schemas and statistics of the latter cluster are modified.

With an existing `ZIP` file exported using `PLAN REPLAYER`, you can use the `PLAN REPLAYER` import interface to restore the on-site information of a cluster to any other TiDB cluster. The syntax is as follows:

{{< copyable "sql" >}}

```sql
PLAN REPLAYER LOAD 'file_name';
```

In the statement above, `file_name` is the name of the `ZIP` file to be exported.

For example:

{{< copyable "sql" >}}

```sql
PLAN REPLAYER LOAD 'plan_replayer.zip';
```
