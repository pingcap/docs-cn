---
title: CLI and Configuration Parameters of TiCDC Changefeeds
summary: Learn the definitions of CLI and configuration parameters of TiCDC changefeeds.
---

# CLI and Configuration Parameters of TiCDC Changefeeds

## Changefeed CLI parameters

This section introduces the command-line parameters of TiCDC changefeeds by illustrating how to create a replication (changefeed) task:

```shell
cdc cli changefeed create --server=http://10.0.10.25:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"upstream_id":7178706266519722477,"namespace":"default","id":"simple-replication-task","sink_uri":"mysql://root:xxxxx@127.0.0.1:4000/?time-zone=","create_time":"2022-12-19T15:05:46.679218+08:00","start_ts":438156275634929669,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":true,"bdr_mode":false,"sync_point_interval":30000000000,"sync_point_retention":3600000000000,"filter":{"rules":["test.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0"}
```

- `--changefeed-id`: The ID of the replication task. The format must match the `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$` regular expression. If this ID is not specified, TiCDC automatically generates a UUID (the version 4 format) as the ID.
- `--sink-uri`: The downstream address of the replication task. Configure `--sink-uri` according to the following format. Currently, the scheme supports `mysql`, `tidb`, and `kafka`.

    ```
    [scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
    ```

    When the sink URI contains special characters such as `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`, you need to escape the special characters, for example, in [URI Encoder](https://meyerweb.com/eric/tools/dencoder/).

- `--start-ts`: Specifies the starting TSO of the changefeed. From this TSO, the TiCDC cluster starts pulling data. The default value is the current time.
- `--target-ts`: Specifies the ending TSO of the changefeed. To this TSO, the TiCDC cluster stops pulling data. The default value is empty, which means that TiCDC does not automatically stop pulling data.
- `--config`: Specifies the configuration file of the changefeed.

## Changefeed configuration parameters

This section introduces the configuration of a replication task.

```toml
# Specifies whether the database names and tables in the configuration file are case-sensitive.
# The default value is true.
# This configuration item affects configurations related to filter and sink.
case-sensitive = true

# Specifies whether to output the old value. New in v4.0.5. Since v5.0, the default value is `true`.
enable-old-value = true

# Specifies whether to enable the Syncpoint feature, which is supported since v6.3.0 and is disabled by default.
# Since v6.4.0, only the changefeed with the SYSTEM_VARIABLES_ADMIN or SUPER privilege can use the TiCDC Syncpoint feature.
# enable-sync-point = false

# Specifies the interval at which Syncpoint aligns the upstream and downstream snapshots.
# The format is in h m s. For example, "1h30m30s".
# The default value is "10m" and the minimum value is "30s".
# sync-point-interval = "5m"

# Specifies how long the data is retained by Syncpoint in the downstream table. When this duration is exceeded, the data is cleaned up.
# The format is in h m s. For example, "24h30m30s".
# The default value is "24h".
# sync-point-retention = "1h"

[mounter]
# The number of threads with which the mounter decodes KV data. The default value is 16.
# worker-num = 16

[filter]
# Ignores the transaction of specified start_ts.
# ignore-txn-start-ts = [1, 2]

# Filter rules.
# Filter syntax: <https://docs.pingcap.com/tidb/stable/table-filter#syntax>.
rules = ['*.*', '!test.*']

# Event filter rules.
# The detailed syntax is described in the event filter rules section.
# The first event filter rule.
[[filter.event-filters]]
matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
ignore-event = ["insert"] # Ignore insert events.
ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
ignore-update-old-value-expr = "age < 18" # Ignore update DMLs whose old value contains "age < 18".
ignore-update-new-value-expr = "gender = 'male'" # Ignore update DMLs whose new value contains "gender = 'male'".

# The second event filter rule.
matcher = ["test.fruit"] # matcher is an allow list, which means this rule only applies to the fruit table in the test database.
ignore-event = ["drop table"] # Ignore drop table events.
ignore-sql = ["delete"] # Ignore delete DMLs.
ignore-insert-value-expr = "price > 1000 and origin = 'no where'" # Ignore insert DMLs that contain the conditions "price > 1000" and "origin = 'no where'".

[scheduler]
# Splits a table into multiple replication ranges based on the number of Regions, and these ranges can be replicated by multiple TiCDC nodes.
# Note:
# 1. This parameter only takes effect on Kafka changefeeds and is not supported on MySQL changefeeds.
# 2. TiCDC does not split tables with fewer Regions than this parameter value into multiple replication ranges.
# region-per-span = 50000

[sink]
# For the sink of MQ type, you can use dispatchers to configure the event dispatcher.
# Since v6.1.0, TiDB supports two types of event dispatchers: partition and topic. For more information, see <partition and topic link>.
# The matching syntax of matcher is the same as the filter rule syntax. For details about the matcher rules, see <>.
dispatchers = [
    {matcher = ['test1.*', 'test2.*'], topic = "Topic expression 1", partition = "ts" },
    {matcher = ['test3.*', 'test4.*'], topic = "Topic expression 2", partition = "index-value" },
    {matcher = ['test1.*', 'test5.*'], topic = "Topic expression 3", partition = "table"},
    {matcher = ['test6.*'], partition = "ts"}
]

# The protocol configuration item specifies the protocol format of the messages sent to the downstream.
# When the downstream is Kafka, the protocol can only be canal-json or avro.
# When the downstream is a storage service, the protocol can only be canal-json or csv.
protocol = "canal-json"

# The following three configuration items are only used when you replicate data to storage sinks and can be ignored when replicating data to MQ or MySQL sinks.
# Row terminator, used for separating two data change events. The default value is an empty string, which means "\r\n" is used.
terminator = ''
# Date separator type used in the file directory. Value options are `none`, `year`, `month`, and `day`. `none` is the default value and means that the date is not separated. For more information, see <https://docs.pingcap.com/tidb/dev/ticdc-sink-to-cloud-storage#data-change-records>.
date-separator = 'none'
# Whether to use partitions as the separation string. The default value is false, which means that partitions in a table are not stored in separate directories. For more information, see <https://docs.pingcap.com/tidb/dev/ticdc-sink-to-cloud-storage#data-change-records)>.
enable-partition-separator = false

# Since v6.5.0, TiCDC supports saving data changes to storage services in CSV format. Ignore the following configurations if you replicate data to MQ or MySQL sinks.
[sink.csv]
# The character used to separate fields in the CSV file. The value must be an ASCII character and defaults to `,`.
delimiter = ','
# The quotation character used to surround fields in the CSV file. The default value is `"`. If the value is empty, no quotation is used.
quote = '"'
# The character displayed when a CSV column is null. The default value is `\N`.
null = '\N'
# Whether to include commit-ts in CSV rows. The default value is false.
include-commit-ts = false
```
