---
title: DM Cluster Performance Test
summary: Learn how to test the performance of DM clusters.
---

# DM Cluster Performance Test

This document describes how to build a test scenario to do a performance test on the DM cluster, including the speed test and latency test regarding data migration.

## Migration data flow

You can use a simple migration data flow, that is, MySQL -> DM -> TiDB, to test the data migration performance of the DM cluster.

## Deploy test environment

- Deploy the TiDB test cluster using TiUP, with all default configurations.
- Deploy the MySQL service. Enable the `ROW` mode for binlog, and use default configurations for other configuration items.
- Deploy a DM cluster, with a DM-worker and a DM-master.

## Performance test

### Table schema

Use tables with the following schema for the performance test:

{{< copyable "sql" >}}

```sql
CREATE TABLE `sbtest` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `k` int(11) NOT NULL DEFAULT '0',
  `c` char(120) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `pad` char(60) CHARSET utf8mb4 COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `k_1` (`k`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
```

### Full import benchmark case

#### Generate test data

Use `sysbench` to create test tables upstream and generate test data for full import. Execute the following `sysbench` command to generate test data:

{{< copyable "shell-regular" >}}

```bash
sysbench --test=oltp_insert --tables=4 --mysql-host=172.16.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --table-size=50000000 prepare
```

#### Create a data migration task

1. Create an upstream MySQL source and set `source-id` to `source-1`. For details, see [Load the Data Source Configurations](/dm/dm-manage-source.md#operate-data-source).

2. Create a migration task (in `full` mode). The following is a task configuration template:

  ```yaml
  ---
  name: test-full
  task-mode: full

  # Configure the migration task using the TiDB information of your actual test environment.
  target-database:
    host: "192.168.0.1"
    port: 4000
    user: "root"
    password: ""

  mysql-instances:
    -
      source-id: "source-1"
      block-allow-list:  "instance"
      mydumper-config-name: "global"
      loader-thread: 16

  # Configure the name of the database where sysbench generates data.
  block-allow-list:
    instance:
      do-dbs: ["dm_benchmark"]

  mydumpers:
    global:
      rows: 32000
      threads: 32
  ```

For details about how to create a migration task, see [Create a Data Migration Task](/dm/dm-create-task.md).

> **Note:**
>
> - To enable concurrently exporting data from a single table using multi-thread, you can use the `rows` option in the `mydumpers` configuration item. This speeds up data export.
> - To test the performance under different configurations, you can tune `loader-thread` in the `mysql-instances` configuration, as well as `rows` and `threads` in the `mydumpers` configuration item.

#### Get test results

Observe the DM-worker log. When you see `all data files have been finished`, it means that full data has been imported. In this case, you can see the time consumed to import data. The sample log is as follows:

```
 [INFO] [loader.go:604] ["all data files have been finished"] [task=test] [unit=load] ["cost time"=52.439796ms]
```

According to the size of the test data and the time consumed to import data, you can calculate the migration speed of the full data.

### Incremental replication benchmark case

#### Initialize tables

Use `sysbench` to create test tables in the upstream.

#### Create a data migration task

1. Create the source of the upstream MySQL. Set `source-id` to `source-1` (if the source has been created in the [full import benchmark case](#full-import-benchmark-case), you do not need to create it again). For details, see [Load the Data Source Configurations](/dm/dm-manage-source.md#operate-data-source).

2. Create a DM migration task (in `all` mode). The following is an example of the task configuration file:

  ```yaml
  ---
  name: test-all
  task-mode: all

  # Configure the migration task using the TiDB information of your actual test environment.
  target-database:
    host: "192.168.0.1"
    port: 4000
    user: "root"
    password: ""

  mysql-instances:
    -
      source-id: "source-1"
      block-allow-list:  "instance"
      syncer-config-name: "global"

  # Configure the name of the database where sysbench generates data.
  block-allow-list:
    instance:
      do-dbs: ["dm_benchmark"]

  syncers:
    global:
      worker-count: 16
      batch: 100
  ```

For details about how to create a data migration task, see [Create a Data Migration Task](/dm/dm-create-task.md).

> **Note:**
>
> To test the performance under different configurations, you can tune `worker-count` and `batch` in the `syncers` configuration item.

#### Generate incremental data

To continuously generate incremental data in the upstream, run the `sysbench` command:

{{< copyable "shell-regular" >}}

```bash
sysbench --test=oltp_insert --tables=4 --num-threads=32 --mysql-host=172.17.4.40 --mysql-port=3306 --mysql-user=root --mysql-db=dm_benchmark --db-driver=mysql --report-interval=10 --time=1800 run
```

> **Note:**
>
> You can test the data migration performance under different scenarios by using different `sysbench` statements.

#### Get test results

To observe the migration status of DM, you can run the `query-status` command. To observe the monitoring metrics of DM, you can use Grafana. Here the monitoring metrics refer to `finished sqls jobs` (the number of jobs finished per unit time), and other related metrics. For more information, see [Binlog Migration Monitoring Metrics](/dm/monitor-a-dm-cluster.md#binlog-replication).
