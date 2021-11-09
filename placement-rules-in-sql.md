---
title: Placement Rules in SQL
summary: Learn how to schedule placement of tables and partitions.
---

# Placement Rules in SQL

> **Warning:**
>
> Placement Rules in SQL is an experimental feature. The syntax might change before its GA, and there might also be bugs.
>
> If you understand the risks, you can enable this experiment feature by executing `SET GLOBAL tidb_enable_alter_placement = 1;`.

Placement Rules allow you to configure where data will be stored in a TiKV cluster. This is useful for scenarios including optimizing a high availability strategy, ensuring that local copies of data will be available for local stale reads, and adhering to compliance requirements.

## Specify placement options

To use Placement Rules in SQL, you need to specify one or more placement options in a SQL statement. To specify the Placement options, you can either use _direct placement_ or use a _placement policy_.

In the following example, both tables `t1` and `t2` have the same rules. `t1` is specified rules using a direct placement while `t2` is specified rules using a placement policy.

```sql
CREATE TABLE t1 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE PLACEMENT POLICY eastandwest PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-west-1";
CREATE TABLE t2 (a INT) PLACEMENT POLICY=eastandwest;
```

It is recommended to use placement policies for simpler rule management. When you change a placement policy (via [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md)), the change automatically propagates to all database objects.

If you use direct placement options, you have to alter rules for each object (for example, tables and partitions).

`PLACEMENT POLICY` is not associated with any database schema and has the global scope. Therefore, assigning a placement policy does not require any additional privileges over the `CREATE TABLE` privilege.

## Option reference

> **Note:**
>
> Placement options depend on labels correctly specified in the configuration of each TiKV node. For example, the `PRIMARY_REGION` option depends on the `region` label in TiKV. To see a summary of all labels available in your TiKV cluster, use the statement [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md):
>
> ```sql
> mysql> show placement labels;
> +--------+----------------+
> | Key    | Values         |
> +--------+----------------+
> | disk   | ["ssd"]        |
> | region | ["us-east-1"]  |
> | zone   | ["us-east-1a"] |
> +--------+----------------+
> 3 rows in set (0.00 sec)
> ```

| Option Name                | Description                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|
| `PRIMARY_REGION`           | Raft leaders are placed in stores that have the `region` label that matches the value of this option.     |
| `REGIONS`                  | Raft followers are placed in stores that have the `region` label that matches the value of this option. |
| `SCHEDULE`                 | The strategy used to schedule the placement of followers. The value options are `EVEN` (default) or `MAJORITY_IN_PRIMARY`. |
| `FOLLOWERS`                | The number of followers. For example, `FOLLOWERS=2` means that there will be 3 replicas of the data (2 followers and 1 leader). |

In addition to the placement options above, you can also use the advance configurations. For details, see [Advance placement](#advanced-placement).

| Option Name                | Description                                                                                    |
|----------------------------|------------------------------------------------------------------------------------------------|                                                                                       
| `CONSTRAINTS`              | A list of constraints that apply to all roles. For example, `CONSTRAINTS="[+disk=ssd]`.        |
| `FOLLOWER_CONSTRAINTS`     | A list of constraints that only apply to followers.                                            |

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

The `SCHEDULE` option instructs TiDB on how to balance the followers.

The default schedule of `EVEN` ensures a balance of followers in all regions. You can use the `MAJORITY_IN_PRIMARY` schedule to ensure that enough followers are placed in the primary region (`us-east-1`) so that quorum can be achieved. If the primary region completely fails, you can the `MAJORITY_IN_PRIMARY` schedule for lower latency transactions at the expense of availability.

### Assign placement to a partitioned table

> **Note:**
>
> The following example uses list partitioning, which is currently an experimental feature of TiDB. Partitioned tables also require the `PRIMARY KEY` to be included in all columns in the table's partitioning function.

In addition to assigning placement options to tables, you can also assign the options to table partitions. For example:

```sql
CREATE PLACEMENT POLICY europe PRIMARY_REGION="eu-central-1" REGIONS="eu-central-1,eu-west-1";
CREATE PLACEMENT POLICY northamerica PRIMARY_REGION="us-east-1" REGIONS="us-east-1";

SET tidb_enable_list_partition = 1;
CREATE TABLE t1 (
  country VARCHAR(10) NOT NULL,
  userdata VARCHAR(100) NOT NULL
) PARTITION BY LIST COLUMNS (country) (
  PARTITION pEurope VALUES IN ('DE', 'FR', 'GB') PLACEMENT POLICY=europe,
  PARTITION pNorthAmerica VALUES IN ('US', 'CA', 'MX') PLACEMENT POLICY=northamerica
);
```

### Set the default placement for a schema

You can directly attach the default placement options to a database schema. This works similar to setting the default character set or collation for a schema. Your specified placement options apply when no other options are specified. For example:

```sql
CREATE TABLE t1 (a INT);  -- Creates a table t1 with no placement options.

ALTER DATABASE test FOLLOWERS=4;  -- Changes the default placement option, and does not apply to the existing table t1.

CREATE TABLE t2 (a INT);  -- Creates a table t2 with the default placement of FOLLOWERS=4.

CREATE TABLE t3 (a INT) PRIMARY_REGION="us-east-1" REGIONS="us-east-1,us-east-2";  -- Creates a table t3 without the default FOLLOWERS=4 placement, because this statement has specified another placement.

ALTER DATABASE test FOLLOWERS=2;  -- Changes the default placement, and does not apply to existing tables.

CREATE TABLE t4 (a INT);  -- Creates a table t4 with the default FOLLOWERS=2 option.
```

Because placement options are only inherited from the database schema when a table is created, it is recommended to set the default placement option using a `PLACEMENT POLICY`. This ensures that future changes to the policy propagate to existing tables.

### Advanced placement

The placement options `PRIMARY_REGION`, `REGIONS`, and `SCHEDULE` meet the basic needs of data placement at the loss of some flexibility. For more complex scenarios with the need for higher flexibility, you can also use the advanced placement options of `CONSTRAINTS` and `FOLLOWER_CONSTRAINTS`. These two options are mutually exclusive. If you specify both at the same time, an error will be returned.

For example, to set constraints that data must reside on a TiKV store where the label `disk` must match a value:

```sql
CREATE PLACEMENT POLICY storeonfastssd CONSTRAINTS="[+disk=ssd]";
CREATE PLACEMENT POLICY storeonhdd CONSTRAINTS="[+disk=hdd]";
CREATE PLACEMENT POLICY companystandardpolicy CONSTRAINTS="";

CREATE TABLE t1 (id INT, name VARCHAR(50), purchased DATE)
PLACEMENT POLICY=companystandardpolicy
PARTITION BY RANGE( YEAR(purchased) ) (
  PARTITION p0 VALUES LESS THAN (2000) PLACEMENT POLICY=storeonhdd,
  PARTITION p1 VALUES LESS THAN (2005),
  PARTITION p2 VALUES LESS THAN (2010),
  PARTITION p3 VALUES LESS THAN (2015),
  PARTITION p4 VALUES LESS THAN MAXVALUE PLACEMENT POLICY=storeonfastssd
);
```

You can either specify constraints in list format (`[+disk=ssd]`) or in dictionary format (`{+disk=ssd:1,+disk=hdd:2}`).

In list format, constraints are specified as a list of key-value pairs. The key starts with either a `+` or a `-` with `+disk=ssd` indicating that the label `disk` must be set to `ssd`, and `-disk=hdd`, indicating that the label `disk` must not be `hdd`.

In dictionary format, constraints also indicate a number of instances that apply to that rule. For example `FOLLOWER_CONSTRAINTS="{+region=us-east-1:1,+region=us-east-2:1,+region=us-west-1:1,+any:1}";` indicates that 1 follower is in us-east-1, 1 follower is in us-east-2, 1 follower is in us-west-1, and 1 follower can be in any region.

## Known limitations

The following known limitations exist in the experimental release of Placement Rules in SQL:

* Dumpling does not support dumping placement policies. See [issue #29371](https://github.com/pingcap/tidb/issues/29371).
* TiDB tools, including Backup & Restore (BR), TiCDC, TiDB Lightning, and TiDB Data Migration (DM), do not yet support placement rules.
* Temporary tables do not support placement options (either via direct placement or placement policies).
* Syntactic sugar rules exist for setting `PRIMARY_REGION` and `REGIONS`, but in future we plan to add varieties for `PRIMARY_RACK`, `PRIMARY_ZONE` and `PRIMARY_HOST`. See [issue #18030](https://github.com/pingcap/tidb/issues/18030)
* TiFlash learners are not configurable through Placement Rules syntax.
* Placement rules only ensure that data at rest resides on the correct TiKV store. The rules do not guarantee that data in transit (via either user-queries or internal operations) only occurs in a specific region.
