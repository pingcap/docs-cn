---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions using SQL statements.
---

# Placement Rules in SQL

Placement Rules in SQL is a feature that enables you to specify where data is stored in a TiKV cluster using SQL interfaces. Using this feature, tables and partitions are scheduled to specific regions, data centers, racks, or hosts. This is useful for scenarios including optimizing a high availability strategy with lower cost, ensuring that local replicas of data are available for local stale reads, and adhering to data locality requirements.

> **Note:**
>
> The implementation of *Placement Rules in SQL* relies on the *placement rules feature* of PD. For details, refer to [Configure Placement Rules](/configure-placement-rules.md). In the context of Placement Rules in SQL, *placement rules* might refer to *placement policies* attached to other objects, or to rules that are sent from TiDB to PD.

The detailed user scenarios are as follows:

- Merge multiple databases of different applications to reduce the cost on database maintenance
- Increase replica count for important data to improve the application availability and data reliability
- Store new data into NVMe storage and store old data into SSDs to lower the cost on data archiving and storage
- Schedule the leaders of hotspot data to high-performance TiKV instances
- Separate cold data to lower-cost storage mediums to improve cost efficiency
- Support the physical isolation of computing resources between different users, which meets the isolation requirements of different users in a cluster, and the isolation requirements of CPU, I/O, memory, and other resources with different mixed loads

## Specify placement rules

To specify placement rules, first create a placement policy using [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md):

```sql
CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
```

Then attach the policy to a table or partition using either `CREATE TABLE` or `ALTER TABLE`. Then, the placement rules are specified on the table or the partition:

```sql
CREATE TABLE t1 (a INT) PLACEMENT POLICY=myplacementpolicy;
CREATE TABLE t2 (a INT);
ALTER TABLE t2 PLACEMENT POLICY=myplacementpolicy;
```

A placement policy is not associated with any database schema and has the global scope. Therefore, assigning a placement policy does not require any additional privileges over the `CREATE TABLE` privilege.

To modify a placement policy, you can use [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md), and the changes will propagate to all objects assigned with the corresponding policy.

```sql
ALTER PLACEMENT POLICY myplacementpolicy FOLLOWERS=5;
```

To drop policies that are not attached to any table or partition, you can use [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md):

```sql
DROP PLACEMENT POLICY myplacementpolicy;
```

## View current placement rules

If a table has placement rules attached, you can view the placement rules in the output of [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md). To view the definition of the policy available, execute [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md):

```sql
tidb> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T![placement] PLACEMENT POLICY=`myplacementpolicy` */
1 row in set (0.00 sec)

tidb> SHOW CREATE PLACEMENT POLICY myplacementpolicy\G
*************************** 1. row ***************************
       Policy: myplacementpolicy
Create Policy: CREATE PLACEMENT POLICY myplacementpolicy PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1"
1 row in set (0.00 sec)
```

You can also view definitions of placement policies using the [`INFORMATION_SCHEMA.PLACEMENT_POLICIES`](/information-schema/information-schema-placement-policies.md) table.

```sql
tidb> select * from information_schema.placement_policies\G
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

The `information_schema.tables` and `information_schema.partitions` tables also include a column for `tidb_placement_policy_name`, which shows all objects with placement rules attached:

```sql
SELECT * FROM information_schema.tables WHERE tidb_placement_policy_name IS NOT NULL;
SELECT * FROM information_schema.partitions WHERE tidb_placement_policy_name IS NOT NULL;
```

Rules that are attached to objects are applied *asynchronously*. To view the current scheduling progress of placement, use [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md).

## Option reference

> **Note:**
>
> - Placement options depend on labels correctly specified in the configuration of each TiKV node. For example, the `PRIMARY_REGION` option depends on the `region` label in TiKV. To see a summary of all labels available in your TiKV cluster, use the statement [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md):
>
>    ```sql
>    mysql> show placement labels;
>    +--------+----------------+
>    | Key    | Values         |
>    +--------+----------------+
>    | disk   | ["ssd"]        |
>    | region | ["us-east-1"]  |
>    | zone   | ["us-east-1a"] |
>    +--------+----------------+
>    3 rows in set (0.00 sec)
>    ```
>
> - When you use `CREATE PLACEMENT POLICY` to create a placement policy, TiDB does not check whether the labels exist. Instead, TiDB performs the check when you attach the policy to a table.

| Option Name                | Description                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | Raft leaders are placed in stores that have the `region` label that matches the value of this option.     |
| `REGIONS`                  | Raft followers are placed in stores that have the `region` label that matches the value of this option. |
| `SCHEDULE`                 | The strategy used to schedule the placement of followers. The value options are `EVEN` (default) or `MAJORITY_IN_PRIMARY`. |
| `FOLLOWERS`                | The number of followers. For example, `FOLLOWERS=2` means that there will be 3 replicas of the data (2 followers and 1 leader). |

In addition to the placement options above, you can also use the advance configurations. For details, see [Advance placement options](#advanced-placement-options).

| Option Name                | Description                                                                                    |
| --------------| ------------ |
| `CONSTRAINTS`              | A list of constraints that apply to all roles. For example, `CONSTRAINTS="[+disk=ssd]"`.       |
| `LEADER_CONSTRAINTS`       | A list of constraints that only apply to leader.                                      |
| `FOLLOWER_CONSTRAINTS`     | A list of constraints that only apply to followers.                                   |
| `LEARNER_CONSTRAINTS`      | A list of constraints that only apply to learners.                                     |
| `LEARNERS`                 | The number of learners. |
| `SURVIVAL_PREFERENCE`      | The replica placement priority according to the disaster tolerance level of the labels. For example, `SURVIVAL_PREFERENCE="[region, zone, host]"`. |

## Examples

### Increase the number of replicas

The default configuration of [`max-replicas`](/pd-configuration-file.md#max-replicas) is `3`. To increase this for a specific set of tables, you can use a placement policy as follows:

```sql
CREATE PLACEMENT POLICY fivereplicas FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=fivereplicas;
```

Note that the PD configuration includes the leader and follower count, thus 4 followers + 1 leader equals 5 replicas in total.

To expand on this example, you can also use `PRIMARY_REGION` and `REGIONS` placement options to describe the placement for the followers:

```sql
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2,us-west-1" SCHEDULE="MAJORITY_IN_PRIMARY" FOLLOWERS=4;
CREATE TABLE t1 (a INT) PLACEMENT POLICY=eastandwest;
```

The `SCHEDULE` option instructs TiDB on how to balance the followers. The default schedule of `EVEN` ensures a balance of followers in all regions.

To ensure that enough followers are placed in the primary region (`us-east-1`) so that quorum can be achieved, you can use the `MAJORITY_IN_PRIMARY` schedule. This schedule helps provide lower latency transactions at the expense of some availability. If the primary region fails, `MAJORITY_IN_PRIMARY` cannot provide automatic failover.

### Assign placement to a partitioned table

In addition to assigning placement options to tables, you can also assign the options to table partitions. For example:

```sql
CREATE PLACEMENT POLICY p1 FOLLOWERS=5;
CREATE PLACEMENT POLICY europe PRIMARY_REGION="eu-central-1" REGIONS="eu-central-1,eu-west-1";
CREATE PLACEMENT POLICY northamerica PRIMARY_REGION="us-east-1" REGIONS="us-east-1";

SET tidb_enable_list_partition = 1;
CREATE TABLE t1 (
  country VARCHAR(10) NOT NULL,
  userdata VARCHAR(100) NOT NULL
) PLACEMENT POLICY=p1 PARTITION BY LIST COLUMNS (country) (
  PARTITION pEurope VALUES IN ('DE', 'FR', 'GB') PLACEMENT POLICY=europe,
  PARTITION pNorthAmerica VALUES IN ('US', 'CA', 'MX') PLACEMENT POLICY=northamerica,
  PARTITION pAsia VALUES IN ('CN', 'KR', 'JP')
);
```

If a partition has no attached policies, it tries to apply possibly existing policies on the table. For example, the `pEurope` partition will apply the `europe` policy, but the `pAsia` partition will apply the `p1` policy from table `t1`. If `t1` has no assigned policies, `pAsia` will not apply any policy, too.

You can also alter the placement policies assigned to a specific partition. For example:

```sql
ALTER TABLE t1 PARTITION pEurope PLACEMENT POLICY=p1;
```

### Set the default placement for a schema

You can directly attach the default placement rules to a database schema. This works similar to setting the default character set or collation for a schema. Your specified placement options apply when no other options are specified. For example:

```sql
CREATE PLACEMENT POLICY p1 PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Create placement policies

CREATE PLACEMENT POLICY p2 FOLLOWERS=4;

CREATE PLACEMENT POLICY p3 FOLLOWERS=2;

CREATE TABLE t1 (a INT);  -- Creates a table t1 with no placement options.

ALTER DATABASE test PLACEMENT POLICY=p2;  -- Changes the default placement option, and does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2 with the default placement policy p2.

CREATE TABLE t3 (a INT) PLACEMENT POLICY=p1;  -- Creates a table t3 without the default policy p2, because this statement has specified another placement rule.

ALTER DATABASE test PLACEMENT POLICY=p3;  -- Changes the default policy, and does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4 with the default policy p3.

ALTER PLACEMENT POLICY p3 FOLLOWERS=3; -- The table with policy p3 (t4) will have FOLLOWERS=3.
```

Note that this is different from the inheritance between partitions and tables, where changing the policy of tables will affect their partitions. Tables inherit the policy of schema only when they are created without policies attached, and modifying the policies of schemas does not affect created tables.

### Advanced placement options

The placement options `PRIMARY_REGION`, `REGIONS`, and `SCHEDULE` meet the basic needs of data placement at the loss of some flexibility. For more complex scenarios with the need for higher flexibility, you can also use the advanced placement options of `CONSTRAINTS` and `FOLLOWER_CONSTRAINTS`. You cannot specify the `PRIMARY_REGION`, `REGIONS`, or `SCHEDULE` option with the `CONSTRAINTS` option at the same time. If you specify both at the same time, an error will be returned.

For example, to set constraints that data must reside on a TiKV store where the label `disk` must match a value:

```sql
CREATE PLACEMENT POLICY storageonnvme CONSTRAINTS="[+disk=nvme]";
CREATE PLACEMENT POLICY storageonssd CONSTRAINTS="[+disk=ssd]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storageonssd,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storageonnvme
);
```

You can either specify constraints in list format (`[+disk=ssd]`) or in dictionary format (`{+disk=ssd: 1,+disk=nvme: 2}`).

In list format, constraints are specified as a list of key-value pairs. The key starts with either a `+` or a `-`. `+disk=ssd` indicates that the label `disk` must be set to `ssd`, and `-disk=nvme` indicates that the label `disk` must not be `nvme`.

In dictionary format, constraints also indicate a number of instances that apply to that rule. For example, `FOLLOWER_CONSTRAINTS="{+region=us-east-1: 1,+region=us-east-2: 1,+region=us-west-1: 1}";` indicates that 1 follower is in us-east-1, 1 follower is in us-east-2 and 1 follower is in us-west-1. For another example, `FOLLOWER_CONSTRAINTS='{"+region=us-east-1,+disk=nvme":1,"+region=us-west-1":1}';` indicates that 1 follower is in us-east-1 with an nvme disk, and 1 follower is in us-west-1.

> **Note:**
>
> Dictionary and list formats are based on the YAML parser, but the YAML syntax might be incorrectly parsed. For example, `"{+disk=ssd:1,+disk=nvme:2}"` is incorrectly parsed as `'{"+disk=ssd:1": null, "+disk=nvme:1": null}'`. But `"{+disk=ssd: 1,+disk=nvme: 1}"` is correctly parsed as `'{"+disk=ssd": 1, "+disk=nvme": 1}'`.

### Survival preferences

When you create or modify a placement policy, you can use the `SURVIVAL_PREFERENCES` option to set the preferred survivability for your data.

For example, assuming that you have a TiDB cluster across 3 availability zones, with multiple TiKV instances deployed on each host in each zone. And when creating placement policies for this cluster, you have set the `SURVIVAL_PREFERENCES` as follows:

``` sql
CREATE PLACEMENT POLICY multiaz SURVIVAL_PREFERENCES="[zone, host]";
CREATE PLACEMENT POLICY singleaz CONSTRAINTS="[+zone=zone1]" SURVIVAL_PREFERENCES="[host]";
```

After creating the placement policies, you can attach them to the corresponding tables as needed:

- For tables attached with the `multiaz` placement policy, data will be placed in 3 replicas in different availability zones, prioritizing survival goals of data isolation cross zones, followed by survival goals of data isolation cross hosts.
- For tables attached with the `singleaz` placement policy, data will be placed in 3 replicas in the `zone1` availability zone first, and then meet survival goals of data isolation cross hosts.

> **Note:**
>
> `SURVIVAL_PREFERENCES` is equivalent to `location-labels` in PD. For more information, see [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md).

## Compatibility with tools

| Tool Name | Minimum supported version | Description |
| --- | --- | --- |
| Backup & Restore (BR) | 6.0 | Supports importing and exporting placement rules. Refer to [BR Compatibility](/br/backup-and-restore-overview.md#compatibility) for details. |
| TiDB Lightning | Not compatible yet | An error is reported when TiDB Lightning imports backup data that contains placement policies  |
| TiCDC | 6.0 | Ignores placement rules, and does not replicate the rules to the downstream |
| TiDB Binlog | 6.0 | Ignores placement rules, and does not replicate the rules to the downstream |

## Known limitations

The following known limitations are as follows:

* Temporary tables do not support placement options.
* Syntactic sugar rules are permitted for setting `PRIMARY_REGION` and `REGIONS`. In the future, we plan to add varieties for `PRIMARY_RACK`, `PRIMARY_ZONE`, and `PRIMARY_HOST`. See [issue #18030](https://github.com/pingcap/tidb/issues/18030).
* Placement rules only ensure that data at rest resides on the correct TiKV store. The rules do not guarantee that data in transit (via either user queries or internal operations) only occurs in a specific region.
