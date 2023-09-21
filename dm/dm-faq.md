---
title: TiDB Data Migration FAQs
summary: Learn about frequently asked questions (FAQs) about TiDB Data Migration (DM).
aliases: ['/docs/tidb-data-migration/dev/faq/']
---

# TiDB Data Migration FAQs

This document collects the frequently asked questions (FAQs) about TiDB Data Migration (DM).

## Does DM support migrating data from Alibaba RDS or other cloud databases?

Currently, DM only supports decoding the standard version of MySQL or MariaDB binlog. It has not been tested for Alibaba Cloud RDS or other cloud databases. If you are confirmed that its binlog is in standard format, then it is supported.

It is a known issue that for an upstream table with no primary key in Alibaba Cloud RDS, its binlog still contains a hidden primary key column, which is inconsistent with the original table structure.

Here are some known incompatible issues:

- In **Alibaba Cloud RDS**, for an upstream table with no primary key, its binlog still contains a hidden primary key column, which is inconsistent with the original table structure.
- In **HUAWEI Cloud RDS**, directly reading binlog files is not supported. For more details, see [Can HUAWEI Cloud RDS Directly Read Binlog Backup Files?](https://support.huaweicloud.com/en-us/rds_faq/rds_faq_0210.html)

## Does the regular expression of the block and allow list in the task configuration support `non-capturing (?!)`?

Currently, DM does not support it and only supports the regular expressions of the Golang standard library. See regular expressions supported by Golang via [re2-syntax](https://github.com/google/re2/wiki/Syntax).

## If a statement executed upstream contains multiple DDL operations, does DM support such migration?

DM will attempt to split a single statement containing multiple DDL change operations into multiple statements containing only one DDL operation, but might not cover all cases. It is recommended to include only one DDL operation in a statement executed upstream, or verify it in the test environment. If it is not supported, you can file an [issue](https://github.com/pingcap/dm/issues) to the DM repository.

## How to handle incompatible DDL statements?

When you encounter a DDL statement unsupported by TiDB, you need to manually handle it using dmctl (skipping the DDL statement or replacing the DDL statement with a specified DDL statement). For details, see [Handle failed DDL statements](/dm/handle-failed-ddl-statements.md).

> **Note:**
>
> Currently, TiDB is not compatible with all the DDL statements that MySQL supports. See [MySQL Compatibility](/mysql-compatibility.md#ddl-operations).

## Does DM replicate view-related DDL statements and DML statements to TiDB?

Currently, DM does not replicate view-related DDL statements to the downstream TiDB cluster, nor does it replicate view-related DML statements to the downstream TiDB cluster.

## How to reset the data migration task?

When an exception occurs during data migration and the data migration task cannot be resumed, you need to reset the task and re-migrate the data:

1. Execute the `stop-task` command to stop the abnormal data migration task.

2. Purge the data migrated to the downstream.

3. Use one of the following ways to restart the data migration task.

   - Specify a new task name in the task configuration file. Then execute `start-task {task-config-file}`.
   - Execute `start-task --remove-meta {task-config-file}`.

## How to handle the error returned by the DDL operation related to the gh-ost table, after `online-ddl: true` is set?

```
[unit=Sync] ["error information"="{\"msg\":\"[code=36046:class=sync-unit:scope=internal:level=high] online ddls on ghost table `xxx`.`_xxxx_gho`\\ngithub.com/pingcap/dm/pkg/terror.(*Error).Generate ......
```

The above error can be caused by the following reason:

In the last `rename ghost_table to origin table` step, DM reads the DDL information in memory, and restores it to the DDL of the origin table.

However, the DDL information in memory is obtained in either of the two ways:

- DM [processes the gh-ost table during the `alter ghost_table` operation](/dm/feature-online-ddl.md#online-schema-change-gh-ost) and records the DDL information of `ghost_table`;
- When DM-worker is restarted to start the task, DM reads the DDL from `dm_meta.{task_name}_onlineddl`.

Therefore, in the process of incremental replication, if the specified Pos has skipped the `alter ghost_table` DDL but the Pos is still in the online-ddl process of gh-ost, the ghost_table is not written into memory or `dm_meta.{task_name}_onlineddl` correctly. In such cases, the above error is returned.

You can avoid this error by the following steps:

1. Remove the `online-ddl-scheme` or `online-ddl` configuration of the task.

2. Configure `_{table_name}_gho`, `_{table_name}_ghc`, and `_{table_name}_del` in `block-allow-list.ignore-tables`.

3. Execute the upstream DDL in the downstream TiDB manually.

4. After the Pos is replicated to the position after the gh-ost process, re-enable the `online-ddl-scheme` or `online-ddl` configuration and comment out `block-allow-list.ignore-tables`.

## How to add tables to the existing data migration tasks?

If you need to add tables to a data migration task that is running, you can address it in the following ways according to the stage of the task.

> **Note:**
>
> Because adding tables to an existing data migration task is complex, it is recommended that you perform this operation only when necessary.

### In the `Dump` stage

Since MySQL cannot specify a snapshot for export, it does not support updating data migration tasks during the export and then restarting to resume the export through the checkpoint. Therefore, you cannot dynamically add tables that need to be migrated at the `Dump` stage.

If you really need to add tables for migration, it is recommended to restart the task directly using the new configuration file.

### In the `Load` stage

During the export, multiple data migration tasks usually have different binlog positions. If you merge the tasks in the `Load` stage, they might not be able to reach consensus on binlog positions. Therefore, it is not recommended to add tables to a data migration task in the `Load` stage.

### In the `Sync` stage

When the data migration task is in the `Sync` stage, if you add additional tables to the configuration file and restart the task, DM does not re-execute full export and import for the newly added tables. Instead, DM continues incremental replication from the previous checkpoint.

Therefore, if the full data of the newly added table has not been imported to the downstream, you need to use a separate data migration task to export and import the full data to the downstream.

Record the position information in the global checkpoint (`is_global=1`) corresponding to the existing migration task as `checkpoint-T`, such as `(mysql-bin.000100, 1234)`. Record the position information of the full export `metedata` (or the checkpoint of another data migration task in the `Sync` stage) of the table to be added to the migration task as `checkpoint-S`, such as `(mysql-bin.000099, 5678)`. You can add the table to the migration task by the following steps:

1. Use `stop-task` to stop an existing migration task. If the table to be added belongs to another running migration task, stop that task as well.

2. Use a MySQL client to connect the downstream TiDB database and manually update the information in the checkpoint table corresponding to the existing migration task to the smaller value between `checkpoint-T` and `checkpoint-S`. In this example, it is `(mysql- bin.000099, 5678)`.

    - The checkpoint table to be updated is `{task-name}_syncer_checkpoint` in the `{dm_meta}` schema.

    - The checkpoint rows to be updated match `id=(source-id)` and `is_global=1`.

    - The checkpoint columns to be updated are `binlog_name` and `binlog_pos`.

3. Set `safe-mode: true` for the `syncers` in the task to ensure reentrant execution.

4. Start the task using `start-task`.

5. Observe the task status through `query-status`. When `syncerBinlog` exceeds the larger value of `checkpoint-T` and `checkpoint-S`, restore `safe-mode` to the original value and restart the task. In this example, it is `(mysql-bin.000100, 1234)`.

## How to handle the error `packet for query is too large. Try adjusting the 'max_allowed_packet' variable` that occurs during the full import?

Set the parameters below to a value larger than the default 67108864 (64M).

- The global variable of the TiDB server: `max_allowed_packet`.
- The configuration item in the task configuration file: `target-database.max-allowed-packet`. For details, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

## How to handle the error `Error 1054: Unknown column 'binlog_gtid' in 'field list'` that occurs when existing DM migration tasks of an DM 1.0 cluster are running on a DM 2.0 or newer cluster?

Since DM v2.0, if you directly run the `start-task` command with the task configuration file of the DM 1.0 cluster to continue the incremental data replication, the error `Error 1054: Unknown column 'binlog_gtid' in 'field list'` occurs.

This error can be handled by [manually importing DM migration tasks of a DM 1.0 cluster to a DM 2.0 cluster](/dm/manually-upgrade-dm-1.0-to-2.0.md).

## Why does TiUP fail to deploy some versions of DM (for example, v2.0.0-hotfix)?

You can use the `tiup list dm-master` command to view the DM versions that TiUP supports to deploy. TiUP does not manage DM versions which are not shown by this command.

## How to handle the error `parse mydumper metadata error: EOF` that occurs when DM is replicating data?

You need to check the error message and log files to further analyze this error. The cause might be that the dump unit does not produce the correct metadata file due to a lack of permissions.

## Why does DM report no fatal error when replicating sharded schemas and tables, but downstream data is lost?

Check the configuration items `block-allow-list` and `table-route`:

- You need to configure the names of upstream databases and tables under `block-allow-list`. You can add "~" before `do-tables` to use regular expressions to match names.
- `table-route` uses wildcard characters instead of regular expressions to match table names. For example, `table_parttern_[0-63]` only matches 7 tables, from `table_parttern_0` to `table_pattern_6`.

## Why does the `replicate lag` monitor metric show no data when DM is not replicating from upstream?

In DM 1.0, you need to enable `enable-heartbeat` to generate the monitor data. In DM 2.0 and later versions, it is expected to have no data in the monitor metric `replicate lag` because this feature is not supported.

## How to handle the error `fail to initial unit Sync of subtask` when DM is starting a task, with the `RawCause` in the error message showing `context deadline exceeded`?

This is a known issue in DM 2.0.0 version and will be fixed in DM 2.0.1 version. It is likely to be triggered when a replication task has a lot of tables to process. If you use TiUP to deploy DM, you can upgrade DM to the nightly version to fix this issue. Or you can download the 2.0.0-hotfix version from [the release page of DM](https://github.com/pingcap/tiflow/releases) on GitHub and manually replace the executable files.

## How to handle the error `duplicate entry` when DM is replicating data?

You need to first check and confirm the following things:

- `disable-detect` is not configured in the replication task ( in v2.0.7 and earlier versions).
- The data is not inserted manually or by other replication programs.
- No DML filter associated with this table is configured.

To facilitate troubleshooting, you can first collect general log files of the downstream TiDB instance and then ask for technical support at [TiDB Community slack channel](https://tidbcommunity.slack.com/archives/CH7TTLL7P). The following example shows how to collect general log files:

```bash
# Enable general log collection
curl -X POST -d "tidb_general_log=1" http://{TiDBIP}:10080/settings
# Disable general log collection
curl -X POST -d "tidb_general_log=0" http://{TiDBIP}:10080/settings
```

When the `duplicate entry` error occurs, you need to check the log files for the records that contain conflict data.

## Why do some monitoring panels show `No data point`?

It is normal for some panels to have no data. For example, when there is no error reported, no DDL lock, or the relay log feature is not enabled, the corresponding panels show `No data point`. For detailed description of each panel, see [DM Monitoring Metrics](/dm/monitor-a-dm-cluster.md).

## In DM v1.0, why does the command `sql-skip` fail to skip some statements when the task is in error?

You need to first check whether the binlog position is still advancing after you execute `sql-skip`. If so, it means that `sql-skip` has taken effect. The reason why this error keeps occurring is that the upstream sends multiple unsupported DDL statements. You can use `sql-skip -s <sql-pattern>` to set a pattern to match these statements.

Sometimes, the error message contains the `parse statement` information, for example:

```
if the DDL is not needed, you can use a filter rule with \"*\" schema-pattern to ignore it.\n\t : parse statement: line 1 column 11 near \"EVENT `event_del_big_table` \r\nDISABLE\" %!!(MISSING)(EXTRA string=ALTER EVENT `event_del_big_table` \r\nDISABLE
```

The reason for this type of error is that the TiDB parser cannot parse DDL statements sent by the upstream, such as `ALTER EVENT`, so `sql-skip` does not take effect as expected. You can add [binlog event filters](/dm/dm-binlog-event-filter.md) in the configuration file to filter those statements and set `schema-pattern: "*"`. Starting from DM v2.0.1, DM pre-filters statements related to `EVENT`.

Since DM v6.0, `binlog` replaces `sql-skip` and `handle-error`. You can use the `binlog` command instead to avoid this issue.

## Why do `REPLACE` statements keep appearing in the downstream when DM is replicating?

You need to check whether the [safe mode](/dm/dm-glossary.md#safe-mode) is automatically enabled for the task. If the task is automatically resumed after an error, or if there is high availability scheduling, then the safe mode is enabled because it is within 1 minutes after the task is started or resumed.

You can check the DM-worker log file and search for a line containing `change count`. If the `new count` in the line is not zero, the safe mode is enabled. To find out why it is enabled, check when it happens and if any errors are reported before.

## In DM v2.0, why does the full import task fail if DM restarts during the task?

In DM v2.0.1 and earlier versions, if DM restarts before the full import completes, the bindings between upstream data sources and DM-worker nodes might change. For example, it is possible that the intermediate data of the dump unit is on DM-worker node A but the load unit is run by DM-worker node B, thus causing the operation to fail.

The following are two solutions to this issue:

- If the data volume is small (less than 1 TB) or the task merges sharded tables, take these steps:

    1. Clean up the imported data in the downstream database.
    2. Remove all files in the directory of exported data.
    3. Delete the task using dmctl and run the command `start-task --remove-meta` to create a new task.

    After the new task starts, it is recommended to ensure that there is no redundant DM worker node and avoid restarting or upgrading the DM cluster during the full import.

- If the data volume is large (more than 1 TB), take these steps:

    1. Clean up the imported data in the downstream database.
    2. Deploy TiDB-Lightning to the DM worker nodes that process the data.
    3. Use the Local-backend mode of TiDB-Lightning to import data that DM dump units export.
    4. After the full import completes, edit the task configuration file in the following ways and restart the task:
        - Change `task-mode` to `incremental`.
        - Set the value of `mysql-instance.meta.pos` to the position recorded in the metadata file that the dump unit outputs.

## Why does DM report the error `ERROR 1236 (HY000): The slave is connecting using CHANGE MASTER TO MASTER_AUTO_POSITION = 1, but the master has purged binary logs containing GTIDs that the slave requires.` if it restarts during an incremental task?

This error indicates that the upstream binlog position recorded in the metadata file output by the dump unit has been purged during the full migration.

If this issue occurs, you need to pause the task, delete all migrated data in the downstream database, and start a new task with the `--remove-meta` option.

You can avoid this issue in advance by configuring in the following ways:

1. Increase the value of `expire_logs_days` in the upstream MySQL database to avoid wrongly purging needed binlog files before the full migration task completes. If the data volume is large, it is recommended to use dumpling and TiDB-Lightning at the same time to speed up the task.
2. Enable the relay log feature for this task so that DM can read data from relay logs even though the binlog position is purged.

## Why does the Grafana dashboard of a DM cluster display `failed to fetch dashboard` if the cluster is deployed using TiUP v1.3.0 or v1.3.1?

This is a known bug of TiUP, which is fixed in TiUP v1.3.2. The following are two solutions to this issue:

- Solution one:
    1. Upgrade TiUP to a later version using the command `tiup update --self && tiup update dm`.
    2. Scale in and then scale out Grafana nodes in the cluster to restart the Grafana service.
- Solution two:
    1. Back up the `deploy/grafana-$port/bin/public` folder.
    2. Download the [TiUP DM offline package](https://download.pingcap.org/tidb-dm-v2.0.1-linux-amd64.tar.gz) and unpack it.
    3. Unpack the `grafana-v4.0.3-**.tar.gz` in the offline package.
    4. Replace the folder `deploy/grafana-$port/bin/public` with the `public` folder in `grafana-v4.0.3-**.tar.gz`.
    5. Execute `tiup dm restart $cluster_name -R grafana` to restart the Grafana service.

## In DM v2.0, why does the query result of the command `query-status` show that the Syncer checkpoint GTIDs are inconsecutive if the task has `enable-relay` and `enable-gtid` enabled at the same time?

This is a known bug in DM, which is fixed in DM v2.0.2. The bug is triggered when the following two conditions are fully met at the same time:

1. Parameters `enable-relay` and `enable-gtid` are set to `true` in the source configuration file.
2. The upstream database is a **MySQL secondary database**. If you execute the command `show binlog events in '<newest-binlog>' limit 2` to query the `previous_gtids` of the database, the result is inconsecutive, such as the following example:

```
mysql> show binlog events in 'mysql-bin.000005' limit 2;
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                               |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
| mysql-bin.000005 |    4 | Format_desc    |    123452 |         123 | Server ver: 5.7.32-35-log, Binlog ver: 4                           |
| mysql-bin.000005 |  123 | Previous_gtids |    123452 |         194 | d3618e68-6052-11eb-a68b-0242ac110002:6-7                           |
+------------------+------+----------------+-----------+-------------+--------------------------------------------------------------------+
```

The bug occurs if you run `query-status <task>` in dmctl to query task information and find that `subTaskStatus.sync.syncerBinlogGtid` is inconsecutive but `subTaskStatus.sync.masterBinlogGtid` is consecutive. See the following example:

```
query-status test
{
    ...
    "sources": [
        {
            ...
            "sourceStatus": {
                "source": "mysql1",
                ...
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000006, 744)",
                    "masterBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-50",
                    ...
                }
            },
            "subTaskStatus": [
                {
                    ...
                    "sync": {
                        ...
                        "masterBinlog": "(mysql-bin.000006, 744)",
                        "masterBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-50",
                        "syncerBinlog": "(mysql-bin|000001.000006, 738)",
                        "syncerBinlogGtid": "f8004e25-6067-11eb-9fa3-0242ac110003:1-20:40-49",
                        ...
                        "synced": false,
                        "binlogType": "local"
                    }
                }
            ]
        },
        {
            ...
            "sourceStatus": {
                "source": "mysql2",
                ...
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000007, 1979)",
                    "masterBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                    ...
                }
            },
            "subTaskStatus": [
                {
                    ...
                    "sync": {
                        "masterBinlog": "(mysql-bin.000007, 1979)",
                        "masterBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                        "syncerBinlog": "(mysql-bin|000001.000008, 1979)",
                        "syncerBinlogGtid": "ddb8974e-6064-11eb-8357-0242ac110002:1-25",
                        ...
                        "synced": true,
                        "binlogType": "local"
                    }
                }
            ]
        }
    ]
}
```

In the example, the `syncerBinlogGtid` of the data source `mysql1` is inconsecutive. In this case, you can do one of the following to handle the data loss:

- If upstream binlogs from the current time to the position recorded in the metadata of the full export task have not been purged, you can take these steps:
    1. Stop the current task and delete all data sources with inconsecutive GTIDs.
    2. Set `enable-relay` to `false` in all source configuration files.
    3. For data sources with inconsecutive GTIDs (such as `mysql1` in the above example), change the task to an incremental task and configure related `mysql-instances.meta` with metadata information of each full export task, including the `binlog-name`, `binlog-pos`, and `binlog-gtid` information.
    4. Set `syncers.safe-mode` to `true` in `task.yaml` of the incremental task and restart the task.
    5. After the incremental task replicates all missing data to the downstream, stop the task and change `safe-mode` to `false` in the `task.yaml`.
    6. Restart the task again.
- If upstream binlogs have been purged but local relay logs remain, you can take these steps:
    1. Stop the current task.
    2. For data sources with inconsecutive GTIDs (such as `mysql1` in the above example), change the task to an incremental task and configure related `mysql-instances.meta` with metadata information of each full export task, including the `binlog-name`, `binlog-pos`, and `binlog-gtid` information.
    3. In the `task.yaml` of the incremental task, change the previous value of `binlog-gtid` to the previous value of `previous_gtids`. For the above example, change `1-y` to `6-y`.
    4. Set `syncers.safe-mode` to `true` in the `task.yaml` and restart the task.
    5. After the incremental task replicates all missing data to the downstream, stop the task and change `safe-mode` to `false` in the `task.yaml`.
    6. Restart the task again.
    7. Restart the data source and set either `enable-relay` or `enable-gtid` to `false` in the source configuration file.
- If none of the above conditions is met or if the data volume of the task is small, you can take these steps:
    1. Clean up imported data in the downstream database.
    2. Restart the data source and set either `enable-relay` or `enable-gtid` to `false` in the source configuration file.
    3. Create a new task and run the command `start-task task.yaml --remove-meta` to migrate data from the beginning again.

For data sources that can be replicated normally (such as `mysql2` in the above example) in the first and second solutions above, configure related `mysql-instances.meta` with `syncerBinlog` and `syncerBinlogGtid` information from `subTaskStatus.sync` when setting the incremental task.

## In DM v2.0, how do I handle the error "heartbeat config is different from previous used: serverID not equal" when switching the connection between DM-workers and MySQL instances in a virtual IP environment with the `heartbeat` feature enabled?

The `heartbeat` feature is disabled by default in DM v2.0 and later versions. If you enable the feature in the task configuration file, it interferes with the high availability feature. To solve this issue, you can disable the `heartbeat` feature by setting `enable-heartbeat` to `false` in the task configuration file, and then reload the task configuration file. DM will forcibly disable the `heartbeat` feature in subsequent releases.

## Why does a DM-master fail to join the cluster after it restarts and DM reports the error "fail to start embed etcd, RawCause: member xxx has already been bootstrapped"?

When a DM-master starts, DM records the etcd information in the current directory. If the directory changes after the DM-master restarts, DM cannot get access to the etcd information, and thus the restart fails.

To solve this issue, you are recommended to maintain DM clusters using TiUP. In the case that you need to deploy using binary files, you need to configure `data-dir` with absolute paths in the configuration file of the DM-master, or pay attention to the current directory where you run the command.

## Why DM-master cannot be connected when I use dmctl to execute commands?

When using dmctl execute commands, you might find the connection to DM master fails (even if you have specified the parameter value of `--master-addr` in the command), and the error message is like `RawCause: context deadline exceeded, Workaround: please check your network connection.`. But afer checking the network connection using commands like `telnet <master-addr>`, no exception is found.

In this case, you can check the environment variable `https_proxy` (note that it is **https**). If this variable is configured, dmctl automatically connects the host and port specified by `https_proxy`. If the host does not have a corresponding `proxy` forwarding service, the connection fails.

To solve this issue, check whether `https_proxy` is mandatory. If not, cancel the setting. Otherwise, add the environment variable setting `https_proxy="" ./dmctl --master-addr "x.x.x.x:8261"` before the oringial dmctl commands.

> **Note:**
>
> The environment variables related to `proxy` include `http_proxy`, `https_proxy`, and `no_proxy`. If the connection error persists after you perform the above steps, check whether the configuration parameters of `http_proxy` and `no_proxy` are correct.

## How to handle the returned error when executing start-relay command for DM versions from 2.0.2 to 2.0.6?

```
flush local meta, Rawcause: open relay-dir/xxx.000001/relay.metayyyy: no such file or directory
```

The above error might be made in the following cases:

- DM has been upgraded from v2.0.1 and earlier to v2.0.2 - v2.0.6, and relay log is started before the upgrade and restarted after the upgrade.
- Execute the stop-relay command to pause the relay log and then restart it.

You can avoid this error by the following options:

- Restart relay log:

    ```
    » stop-relay -s sourceID workerName
    » start-relay -s sourceID workerName
    ```

- Upgrade DM to v2.0.7 or later versions.

## Why does the load unit report the `Unknown character set` error?

TiDB does not support all MySQL character sets. Therefore, DM reports this error if an unsupported character set is used when creating the table schema during a full import. To bypass this error, you can create the table schema in the downstream in advance using the [character sets supported by TiDB](/character-set-and-collation.md) according to the specific data.
