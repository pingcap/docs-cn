---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# Placement Rules in SQL

Placement Rules in SQL is a feature that enables you to specify where data is stored in a TiKV cluster using SQL statements. With this feature, you can schedule data of clusters, databases, tables, or partitions to specific regions, data centers, racks, or hosts.

This feature can fulfill the following use cases:

- Deploy data across multiple data centers and configure rules to optimize high availability strategies.
- Merge multiple databases from different applications and isolate data of different users physically, which meets the isolation requirements of different users within an instance.
- Increase the number of replicas for important data to improve application availability and data reliability.

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

## Overview

With the Placement Rules in SQL feature, you can [create placement policies](#create-and-attach-placement-policies) and configure desired placement policies for data at different levels, with granularity from coarse to fine as follows:

| Level            | Description                                                                          |
|------------------|--------------------------------------------------------------------------------------|
| Cluster          | By default, TiDB configures a policy of 3 replicas for a cluster. You can configure a global placement policy for your cluster. For more information, see [Specify the number of replicas globally for a cluster](#specify-the-number-of-replicas-globally-for-a-cluster). |
| Database         | You can configure a placement policy for a specific database. For more information, see [Specify a default placement policy for a database](#specify-a-default-placement-policy-for-a-database). |
| Table            | You can configure a placement policy for a specific table. For more information, see [Specify a placement policy for a table](#specify-a-placement-policy-for-a-table). |
| Partition        | You can create partitions for different rows in a table and configure placement policies for partitions separately. For more information, see [Specify a placement policy for a partitioned table](#specify-a-placement-policy-for-a-partitioned-table). |

> **Tip:**
>
> The implementation of *Placement Rules in SQL* relies on the *placement rules feature* of PD. For details, refer to [Configure Placement Rules](https://docs.pingcap.com/zh/tidb/stable/configure-placement-rules). In the context of Placement Rules in SQL, *placement rules* might refer to *placement policies* attached to other objects, or to rules that are sent from TiDB to PD.

## Limitations

- To simplify maintenance, it is recommended to limit the number of placement policies within a cluster to 10 or fewer.
- It is recommended to limit the total number of tables and partitions attached with placement policies to 10,000 or fewer. Attaching policies to too many tables and partitions can increase computation workloads on PD, thereby affecting service performance.
- It is recommended to use the Placement Rules in SQL feature according to examples provided in this document rather than using other complex placement policies.

## Prerequisites

Placement policies rely on the configuration of labels on TiKV nodes. For example, the `PRIMARY_REGION` placement option relies on the `region` label in TiKV.

<CustomContent platform="tidb">

When you create a placement policy, TiDB does not check whether the labels specified in the policy exist. Instead, TiDB performs the check when you attach the policy. Therefore, before attaching a placement policy, make sure that each TiKV node is configured with correct labels. The configuration method for a TiDB Self-Hosted cluster is as follows:

```
tikv-server --labels region=<region>,zone=<zone>,host=<host>
```

For detailed configuration methods, see the following examples:

| Deployment method | Example |
| --- | --- |
| Manual deployment | [Schedule replicas by topology labels](/schedule-replicas-by-topology-labels.md) |
| Deployment with TiUP | [Geo-distributed deployment topology](/geo-distributed-deployment-topology.md) |
| Deployment with TiDB Operator | [Configure a TiDB cluster in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster#high-data-high-availability) |

> **Note:**
>
> For TiDB Dedicated clusters, you can skip these label configuration steps because the labels on TiKV nodes in TiDB Dedicated clusters are configured automatically.

</CustomContent>

<CustomContent platform="tidb-cloud">

For TiDB Dedicated clusters, labels on TiKV nodes are configured automatically.

</CustomContent>

To view all available labels in the current TiKV cluster, you can use the [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) statement:

```sql
SHOW PLACEMENT LABELS;
+--------+----------------+
| Key    | Values         |
+--------+----------------+
| disk   | ["ssd"]        |
| region | ["us-east-1"]  |
| zone   | ["us-east-1a"] |
+--------+----------------+
3 rows in set (0.00 sec)
```

## Usage

This section describes how to create, attach, view, modify, and delete placement policies using SQL statements.

### Create and attach placement policies

1. To create a placement policy, use the [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) statement:

    ```sql
    CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
    ```

    In this statement:

    - The `PRIMARY_REGION="us-east-1"` option means placing Raft Leaders on nodes with the `region` label as `us-east-1`.
    - The `REGIONS="us-east-1,us-west-1"` option means placing Raft Followers on nodes with the `region` label as `us-east-1` and nodes with the `region` label as `us-west-1`.

    For more configurable placement options and their meanings, see the [Placement options](#placement-option-reference).

2. To attach a placement policy to a table or a partitioned table, use the `CREATE TABLE` or `ALTER TABLE` statement to specify the placement policy for that table or partitioned table:

    ```sql
    CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
    CREATE TABLE t2 (a INT);
    ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
    ```

   `PLACEMENT POLICY` is not associated with any database schema and can be attached in a global scope. Therefore, specifying a placement policy using `CREATE TABLE` does not require any additional privileges.

### View placement policies

- To view an existing placement policy, you can use the [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) statement:

    ```sql
    SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
    *************************** 1. row ***************************
           Policy: myplacementpolicy
    Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
    1 row in set (0.00 sec)
    ```

- To view the placement policy attached to a specific table, you can use the [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) statement:

    ```sql
    SHOW CREATE TABLE t1\G
    *************************** 1. row ***************************
           Table: t1
    Create Table: CREATE TABLE `t1` (
      `a` int(11) DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
    1 row in set (0.00 sec)
    ```

- To view the definitions of placement policies in a cluster, you can query the [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) system table:

    ```sql
    SELECT * FROM information_schema.placement_policies\G
    ***************************[ 1. row ]***************************
    POLICY_ID            | 1
    CATALOG_NAME         | def
    POLICY_NAME          | p1
    PRIMARY_REGION       | us-east-1
    REGIONS              | us-east-1,us-west-1
    CONSTRAINTS          |
    LEADER_CONSTRAINTS   |
    FOLLOWER_CONSTRAINTS |
    LEARNER_CONSTRAINTS  |
    SCHEDULE             |
    FOLLOWERS            | 4
    LEARNERS             | 0
    1 row in set
    ```

- To view all tables that are attached with placement policies in a cluster, you can query the `tidb_placement_policy_name` column of the `information_schema.tables` system table:

    ```sql
    SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- To view all partitions that are attached with placement policies in a cluster, you can query the `tidb_placement_policy_name` column of the `information_schema.partitions` system table:

    ```sql
    SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
    ```

- Placement policies attached to all objects are applied *asynchronously*. To check the scheduling progress of placement policies, you can use the [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) statement:

    ```sql
    SHOW PLACEMENT;
    ```

### Modify placement policies

To modify a placement policy, you can use the  [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) statement. The modification will apply to all objects that are attached with the corresponding policy.

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=4;
```

In this statement, the `FOLLOWERS=4` option means configuring 5 replicas for the data, including 4 Followers and 1 Leader. For more configurable placement options and their meanings, see [Placement option reference](#placement-option-reference).

### Drop placement policies

To drop a policy that is not attached to any table or partition, you can use the [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) statement:

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## Placement option reference

When creating or modifying placement policies, you can configure placement options as needed.

> **Note:**
>
> The `PRIMARY_REGION`, `REGIONS`, and `SCHEDULE` options cannot be specified together with the `CONSTRAINTS` option, or an error will occur.

### Regular placement options

Regular placement options can meet the basic requirements of data placement.

| Option name                | Description                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | Specifies that placing Raft Leaders on nodes with a `region` label that matches the value of this option.     |
| `REGIONS`                  | Specifies that placing Raft Followers on nodes with a `region` label that matches the value of this option. |
| `SCHEDULE`                 | Specifies the strategy for scheduling the placement of Followers. The value options are `EVEN` (default) or `MAJORITY_IN_PRIMARY`. |
| `FOLLOWERS`                | Specifies the number of Followers. For example, `FOLLOWERS=2` means there will be 3 replicas of the data (2 Followers and 1 Leader). |

### Advanced placement options

Advanced configuration options provide more flexibility for data placement to meet the requirements of complex scenarios. However, configuring advanced options is more complex than regular options and requires you to have a deep understanding of the cluster topology and the TiDB data sharding.

| Option name                | Description                                                                                    |
| --------------| ------------ |
| `CONSTRAINTS`              | A list of constraints that apply to all roles. For example, `CONSTRAINTS="[+disk=ssd]"`. |
| `LEADER_CONSTRAINTS`       | A list of constraints that only apply to Leader.                                      |
| `FOLLOWER_CONSTRAINTS`     | A list of constraints that only apply to Followers.                                   |
| `LEARNER_CONSTRAINTS`      | A list of constraints that only apply to learners.                                     |
| `LEARNERS`                 | The number of learners. |
| `SURVIVAL_PREFERENCE`      | The replica placement priority according to the disaster tolerance level of the labels. For example, `SURVIVAL_PREFERENCE="[region, zone, host]"`. |

### CONSTRAINTS formats

You can configure `CONSTRAINTS`, `FOLLOWER_CONSTRAINTS`, and `LEARNER_CONSTRAINTS` placement options using either of the following formats:

| CONSTRAINTS format | Description |
|----------------------------|-----------------------------------------------------------------------------------------------------------|
| List format  | If a constraint to be specified applies to all replicas, you can use a key-value list format. Each key starts with `+` or `-`. For example: <br/><ul><li>`[+region=us-east-1]` means placing data on nodes  that have a `region` label as `us-east-1`.</li><li>`[+region=us-east-1,-type=fault]` means placing data on nodes that have a `region` label as `us-east-1` but do not have a `type` label as `fault`.</li></ul><br/>  |
| Dictionary format | If you need to specify different numbers of replicas for different constraints, you can use the dictionary format. For example: <br/><ul><li>`FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` means placing one Follower in `us-east-1`, one Follower in `us-east-2`, and one Follower in `us-west-1`.</li><li>`FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+type=scale-node": 1,"+region=us-west-1": 1}';` means placing one Follower on a node that is located in the `us-east-1` region and has the `type` label as `scale-node`, and one Follower in `us-west-1`.</li></ul>The dictionary format supports each key starting with `+` or `-` and allows you to configure the special `#reject-leader` attribute. For example, `FOLLOWER_CONSTRAINTS='{"+region=us-east-1":1, "+region=us-east-2": 2, "+region=us-west-1,#reject-leader": 1}'` means that the Leaders elected in `us-west-1` will be evicted as much as possible during disaster recovery.|

> **Note:**
>
> - The `LEADER_CONSTRAINTS` placement option only supports the list format.
> - Both list and dictionary formats are based on the YAML parser, but YAML syntax might be incorrectly parsed in some cases. For example, `"{+region=east:1,+region=west:2}"` (no space after `:`) can be incorrectly parsed as `'{"+region=east:1": null, "+region=west:2": null}'`, which is unexpected. However, `"{+region=east: 1,+region=west: 2}"` (space after `:`) can be correctly parsed as `'{"+region=east": 1, "+region=west": 2}'`. Therefore, it is recommended to add a space after `:`.

## Basic examples

### Specify the number of replicas globally for a cluster

After a cluster is initialized, the default number of replicas is `3`. If a cluster needs more replicas, you can increase this number by configuring a placement policy, and then apply the policy at the cluster level using [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md). For example:

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;
ALTER RANGE global PLACEMENT POLICY five_replicas;
```

Note that because TiDB defaults the number of Leaders to `1`, `five replicas` means `4` Followers and `1` Leader.

### Specify a default placement policy for a database

You can specify a default placement policy for a database. This works similarly to setting a default character set or collation for a database. If no other placement policy is specified for a table or partition in the database, the placement policy for the database will apply to the table and partition. For example:

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Creates a placement policy

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- Creates a table t1 without specifying any placement policy.

ALTER DATABASE test PLACEMENT POLICY=p2;  -- Changes the default placement policy of the database to p2, which does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2. The default placement policy p2 applies to t2.

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- Creates a table t3. Because this statement has specified another placement rule, the default placement policy p2 does not apply to table t3.

ALTER DATABASE test PLACEMENT POLICY=p3;  -- Changes the default policy of the database again, which does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4. The default placement policy p3 applies to t4.

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- `FOLLOWERS=3` applies to the table attached with policy p3 (that is, table t4).
```

Note that the policy inheritance from a table to its partitions differs from the policy inheritance in the preceding example. When you change the default policy of a table, the new policy also applies to partitions in that table. However, a table inherits the policy from the database only if it is created without any policy specified. Once a table inherits the policy from the database, modifying the default policy of the database does not apply to that table.

### Specify a placement policy for a table

You can specify a default placement policy for a table. For example:

```sql
CREATE PLACEMENT POLICY five_replicas FOLLOWERS=4;

CREATE TABLE t (a INT) PLACEMENT POLICY=five_replicas;  -- Creates a table t and attaches the 'five_replicas' placement policy to it.

ALTER TABLE t PLACEMENT POLICY=default; -- Removes the placement policy 'five_replicas' from the table t and resets the placement policy to the default one.
```

### Specify a placement policy for a partitioned table

You can also specify a placement policy for a partitioned table or a partition. For example:

```sql
CREATE PLACEMENT POLICY storageforhisotrydata CONSTRAINTS="[+node=history]";
CREATE PLACEMENT POLICY storagefornewdata CONSTRAINTS="[+node=new]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageforhisotrydata,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storagefornewdata
);
```

If no placement policy is specified for a partition in a table, the partition attempts to inherit the policy (if any) from the table. In the preceding example:

- The `p0` partition will apply the `storageforhisotrydata` policy.
- The `p4` partition will apply the `storagefornewdata` policy.
- The `p1`, `p2`, and `p3` partitions will apply the `companystandardpolicy` placement policy inherited from the table `t1`.
- If no placement policy is specified for the table `t1`, the `p1`, `p2`, and `p3` partitions will inherit the database default policy or the global default policy.

After placement policies are attached to these partitions, you can change the placement policy for a specific partition as in the following example:

```sql
ALTER TABLE t1 PARTITION p1 PLACEMENT POLICY=storageforhisotrydata;
```

## High availability examples

Assume that there is a cluster with the following topology, where TiKV nodes are distributed across 3 regions, with each region containing 3 available zones:

```sql
SELECT store_id,address,label from INFORMATION_SCHEMA.TIKV_STORE_STATUS;
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
| store_id | address         | label                                                                                                                    |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+
|        1 | 127.0.0.1:20163 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1a"}, {"key": "host", "value": "host1"}]     |
|        2 | 127.0.0.1:20162 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1b"}, {"key": "host", "value": "host2"}]     |
|        3 | 127.0.0.1:20164 | [{"key": "region", "value": "us-east-1"}, {"key": "zone", "value": "us-east-1c"}, {"key": "host", "value": "host3"}]     |
|        4 | 127.0.0.1:20160 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2a"}, {"key": "host", "value": "host4"}]     |
|        5 | 127.0.0.1:20161 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2b"}, {"key": "host", "value": "host5"}]     |
|        6 | 127.0.0.1:20165 | [{"key": "region", "value": "us-east-2"}, {"key": "zone", "value": "us-east-2c"}, {"key": "host", "value": "host6"}]     |
|        7 | 127.0.0.1:20166 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1a"}, {"key": "host", "value": "host7"}]     |
|        8 | 127.0.0.1:20167 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1b"}, {"key": "host", "value": "host8"}]     |
|        9 | 127.0.0.1:20168 | [{"key": "region", "value": "us-west-1"}, {"key": "zone", "value": "us-west-1c"}, {"key": "host", "value": "host9"}]     |
+----------+-----------------+--------------------------------------------------------------------------------------------------------------------------+

```

### Specify survival preferences

If you are not particularly concerned about the exact data distribution but prioritize fulfilling disaster recovery requirements, you can use the `SURVIVAL_PREFERENCES` option to specify data survival preferences.

As in the preceding example, the TiDB cluster is distributed across 3 regions, with each region containing 3 zones. When creating placement policies for this cluster, assume that you configure the `SURVIVAL_PREFERENCES` as follows:

``` sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[region, zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+region=us-east-1]" SURVIVAL_PREFERENCES="[zone]";
```

After creating the placement policies, you can attach them to the corresponding tables as needed:

- For tables attached with the `multiaz` placement policy, data will be placed in 3 replicas in different regions, prioritizing to meet the cross-region survival goal of data isolation, followed by the cross-zone survival goal, and finally the cross-host survival goal.
- For tables attached with the `singleaz` placement policy, data will be placed in 3 replicas in the `us-east-1` region first, and then meet the cross-zone survival goal of data isolation.

<CustomContent platform="tidb">

> **Note:**
>
> `SURVIVAL_PREFERENCES` is equivalent to `location-labels` in PD. For more information, see [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> `SURVIVAL_PREFERENCES` is equivalent to `location-labels` in PD. For more information, see [Schedule Replicas by Topology Labels](https://docs.pingcap.com/tidb/stable/schedule-replicas-by-topology-labels).

</CustomContent>

### Specify a cluster with 5 replicas distributed 2:2:1 across multiple data centers

If you need a specific data distribution, such as a 5-replica distribution in the proportion of 2:2:1, you can specify different numbers of replicas for different constraints by configuring these `CONSTRAINTS` in the [dictionary formats](#constraints-formats):

```sql
CREATE PLACEMENT POLICY `deploy221` CONSTRAINTS='{"+region=us-east-1":2, "+region=us-east-2": 2, "+region=us-west-1": 1}';

ALTER RANGE global PLACEMENT POLICY = "deploy221";

SHOW PLACEMENT;
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| Target            | Placement                                                                                   | Scheduling_State |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
| POLICY deploy221  | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | NULL             |
| RANGE TiDB_GLOBAL | CONSTRAINTS="{\"+region=us-east-1\":2, \"+region=us-east-2\": 2, \"+region=us-west-1\": 1}" | SCHEDULED        |
+-------------------+---------------------------------------------------------------------------------------------+------------------+
```

After the global  `deploy221` placement policy is set for the cluster, TiDB distributes data according to this policy: placing two replicas in the `us-east-1` region, two replicas in the `us-east-2` region, and one replica in the `us-west-1` region.

### Specify the distribution of Leaders and Followers

You can specify a specific distribution of Leaders and Followers using constraints or `PRIMARY_REGION`.

#### Use constraints

If you have specific requirements for the distribution of Raft Leaders among nodes, you can specify the placement policy using the following statement:

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1: 1}';
```

After this placement policy is created and attached to the desired data, the Raft Leader replicas of the data will be placed in the `us-east-1` region specified by the `LEADER_CONSTRAINTS` option, while other replicas of the data will be placed in regions specified by the `FOLLOWER_CONSTRAINTS` option. Note that if the cluster fails, such as a node outage in the `us-east-1` region, a new Leader will still be elected from other regions, even if these regions are specified in `FOLLOWER_CONSTRAINTS`. In other words, ensuring service availability takes the highest priority.

In the event of a failure in the `us-east-1` region, if you do not want to place new Leaders in `us-west-1`, you can configure a special `reject-leader` attribute to evict the newly elected Leaders in that region:

```sql
CREATE PLACEMENT POLICY deploy221_primary_east1 LEADER_CONSTRAINTS="[+region=us-east-1]" FOLLOWER_CONSTRAINTS='{"+region=us-east-1": 1, "+region=us-east-2": 2, "+region=us-west-1,#reject-leader": 1}';
```

#### Use `PRIMARY_REGION`

If the `region` label is configured in your cluster topology, you can also use the `PRIMARY_REGION` and `REGIONS` options to specify a placement policy for Followers:

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

- `PRIMARY_REGION` specifies the distribution region of the Leaders. You can only specify one region in this option.
- The `SCHEDULE` option specifies how TiDB balances the distribution of Followers.
    - The default `EVEN` scheduling rule ensures a balanced distribution of Followers across all regions.
    - If you want to ensure a sufficient number of Follower replicas are placed in the `PRIMARY_REGION` (that is, `us-east-1`), you can use the `MAJORITY_IN_PRIMARY` scheduling rule. This scheduling rule provides lower latency transactions at the expense of some availability. If the primary region fails, `MAJORITY_IN_PRIMARY` does not provide automatic failover.

## Data isolation examples

As in the following example, when creating placement policies, you can configure a constraint for each policy, which requires data to be placed on TiKV nodes with the specified `app` label.

```sql
CREATE PLACEMENT POLICY app_order CONSTRAINTS="[+app=order]";
CREATE PLACEMENT POLICY app_list CONSTRAINTS="[+app=list_collection]";
CREATE TABLE order (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_order
CREATE TABLE list (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=app_list
```

In this example, the constraints are specified using the list format, such as `[+app=order]`. You can also specify them using the dictionary format, such as `{+app=order: 3}`.

After executing the statements in the example, TiDB will place the `app_order` data on TiKV nodes with the `app` label as `order`, and place the `app_list` data on TiKV nodes with the `app` label as `list_collection`, thus achieving physical data isolation in storage.

## Compatibility

## Compatibility with other features

- Temporary tables do not support placement policies.
- Placement policies only ensure that data at rest resides on the correct TiKV nodes but do not guarantee that data in transit (via either user queries or internal operations) only occurs in a specific region.
- To configure TiFlash replicas for your data, you need to [create TiFlash replicas](/tiflash/create-tiflash-replicas.md) rather than using placement policies.
- Syntactic sugar rules are permitted for setting `PRIMARY_REGION` and `REGIONS`. In the future, we plan to add varieties for `PRIMARY_RACK`, `PRIMARY_ZONE`, and `PRIMARY_HOST`. See [issue #18030](https://github.com/pingcap/tidb/issues/18030).

## Compatibility with tools

<CustomContent platform="tidb">

| Tool Name | Minimum supported version | Description |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | Before v6.0, BR does not support backing up and restoring placement policies. For more information, see [Why does an error occur when I restore placement rules to a cluster](/faq/backup-and-restore-faq.md#why-does-an-error-occur-when-i-restore-placement-rules-to-a-cluster). |
| TiDB Lightning | Not compatible yet | An error is reported when TiDB Lightning imports backup data that contains placement policies  |
| TiCDC | 6.0 | Ignores placement policies, and does not replicate the policies to the downstream |
| TiDB Binlog | 6.0 | Ignores placement policies, and does not replicate the policies to the downstream |

</CustomContent>

<CustomContent platform="tidb-cloud">

| Tool Name | Minimum supported version | Description |
| --- | --- | --- |
| TiDB Lightning | Not compatible yet | An error is reported when TiDB Lightning imports backup data that contains placement policies  |
| TiCDC | 6.0 | Ignores placement policies, and does not replicate the policies to the downstream |

</CustomContent>