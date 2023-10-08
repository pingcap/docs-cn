---
title: TIDB_HOT_REGIONS_HISTORY
summary: Learn the `TIDB_HOT_REGIONS_HISTORY` information_schema table.
---

# TIDB_HOT_REGIONS_HISTORY

The `TIDB_HOT_REGIONS_HISTORY` table provides information about history hot Regions that are periodically recorded locally by PD.

> **Note:**
>
> This table is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

<CustomContent platform="tidb">

You can specify the record interval by configuring [`hot-regions-write-interval`](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540). The default value is 10 minutes. You can specify the period for reserving history information about hot Regions by configuring [`hot-regions-reserved-days`](/pd-configuration-file.md#hot-regions-reserved-days-new-in-v540). The default value is 7 days. See [PD configuration file description](/pd-configuration-file.md#hot-regions-write-interval-new-in-v540) for details.

</CustomContent>

<CustomContent platform="tidb-cloud">

By default, the record interval is 10 minutes, and the period for reserving history information about hot Regions is 7 days.

</CustomContent>

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC tidb_hot_regions_history;
```

```sql
+-------------+--------------+------+------+---------+-------+
| Field       | Type         | Null | Key  | Default | Extra |
+-------------+--------------+------+------+---------+-------+
| UPDATE_TIME | timestamp(6) | YES  |      | NULL    |       |
| DB_NAME     | varchar(64)  | YES  |      | NULL    |       |
| TABLE_NAME  | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID    | bigint(21)   | YES  |      | NULL    |       |
| INDEX_NAME  | varchar(64)  | YES  |      | NULL    |       |
| INDEX_ID    | bigint(21)   | YES  |      | NULL    |       |
| REGION_ID   | bigint(21)   | YES  |      | NULL    |       |
| STORE_ID    | bigint(21)   | YES  |      | NULL    |       |
| PEER_ID     | bigint(21)   | YES  |      | NULL    |       |
| IS_LEARNER  | tinyint(1)   | NO   |      | 0       |       |
| IS_LEADER   | tinyint(1)   | NO   |      | 0       |       |
| TYPE        | varchar(64)  | YES  |      | NULL    |       |
| HOT_DEGREE  | bigint(21)   | YES  |      | NULL    |       |
| FLOW_BYTES  | double       | YES  |      | NULL    |       |
| KEY_RATE    | double       | YES  |      | NULL    |       |
| QUERY_RATE  | double       | YES  |      | NULL    |       |
+-------------+--------------+------+------+---------+-------+
16 rows in set (0.00 sec)
```

The fields in the `TIDB_HOT_REGIONS_HISTORY` table are described as follows:

* UPDATE_TIME: The update time of the hot Region.
* DB_NAME: The database name of the object in which the hot Region is located.
* TABLE_ID: The ID of the table in which the hot Region is located.
* TABLE_NAME: The name of the table in which the hot Region is located.
* INDEX_NAME: The name of the index in which the hot Region is located.
* INDEX_ID: The ID of the index in which the hot Region is located.
* REGION_ID: The ID of the hot Region.
* STORE_ID: The ID of the store in which the hot Region is located.
* PEER_ID: The ID of the Peer corresponding to the hot Region.
* IS_LEARNER: Whether the PEER is the LEARNER.
* IS_LEADER: Whether the PEER is the LEADER.
* TYPE: The type of the hot Region.
* HOT_DEGREE: The hot degree of the hot Region.
* FLOW_BYTES: The number of bytes written and read in the Region.
* KEY_RATE: The number of keys written and read in the Region.
* QUERY_RATE: The number of queries written and read in the Region.

> **Note:**
>
> `UPDATE_TIME`, `REGION_ID`, `STORE_ID`, `PEER_ID`, `IS_LEARNER`, `IS_LEADER` and `TYPE` fields are pushed down to the PD servers for execution. To reduce the overhead of using the table, you must specify the time range for the search, and specify as many conditions as possible. For example, `select * from tidb_hot_regions_history where store_id = 11 and update_time > '2020-05-18 20:40:00' and update_time < '2020-05-18 21:40:00' and type='write'`.

## Common user scenarios

* Query hot Regions within a specific period of time. Replace `update_time` with your actual time.

    {{< copyable "sql" >}}

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00';
    ```

    > **Note:**
    >
    > `UPDATE_TIME` also supports Unix timestamps. For example, `update_time >TIMESTAMP('2021-08-18 21:40:00')` or `update_time > FROM_UNIXTIME(1629294000.000)`.

* Query hot Regions in a table within a specific period of time. Replace `update_time` and `table_name` with your actual values.

    {{< copyable "sql" >}}

    ```SQL
    SELECT * FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and TABLE_NAME = 'table_name';
    ```

* Query the distribution of hot Regions within a specific period of time. Replace `update_time` and `table_name` with your actual values.

    {{< copyable "sql" >}}

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

* Query the distribution of hot Leader Regions within a specific period of time. Replace `update_time` and `table_name` with your actual values.

    {{< copyable "sql" >}}

    ```sql
    SELECT count(region_id) cnt, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 GROUP BY STORE_ID ORDER BY cnt DESC;
    ```

* Query the distribution of hot Index Regions within a specific period of time. Replace `update_time` and `table_name` with your actual values.

    {{< copyable "sql" >}}

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2021-09-19 00:00:00' and table_name = 'table_name' group by index_name, store_id order by index_name,cnt desc;
    ```

* Query the distribution of hot Index Leader Regions within a specific period of time. Replace `update_time` and `table_name` with your actual values.

    {{< copyable "sql" >}}

    ```sql
    SELECT count(region_id) cnt, index_name, store_id FROM INFORMATION_SCHEMA.TIDB_HOT_REGIONS_HISTORY WHERE update_time >'2021-08-18 21:40:00' and update_time <'2022-09-19 00:00:00' and table_name = 'table_name' and is_leader=1 group by index_name, store_id order by index_name,cnt desc;
    ```
