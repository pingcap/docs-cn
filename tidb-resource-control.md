---
title: Use Resource Control to Achieve Resource Isolation
summary: Learn how to use the resource control feature to control and schedule application resources.
---

# Use Resource Control to Achieve Resource Isolation

> **Warning:**
>
> This feature is experimental and its form and usage might change in subsequent versions.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is not available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

As a cluster administrator, you can use the resource control feature to create resource groups, set read and write quotas for resource groups, and bind users to those groups.

The TiDB resource control feature provides two layers of resource management capabilities: the flow control capability at the TiDB layer and the priority scheduling capability at the TiKV layer. The two capabilities can be enabled separately or simultaneously. See the [Parameters for resource control](#parameters-for-resource-control) for details. This allows the TiDB layer to control the flow of user read and write requests based on the quotas set for the resource groups, and allows the TiKV layer to schedule the requests based on the priority mapped to the read and write quota. By doing this, you can ensure resource isolation for your applications and meet quality of service (QoS) requirements.

- TiDB flow control: TiDB flow control uses the [token bucket algorithm](https://en.wikipedia.org/wiki/Token_bucket). If there are not enough tokens in a bucket, and the resource group does not specify the `BURSTABLE` option, the requests to the resource group will wait for the token bucket to backfill the tokens and retry. The retry might fail due to timeout.

- TiKV scheduling: You can set the absolute priority [(`PRIORITY`)](/information-schema/information-schema-resource-groups.md#examples) as needed. Different resources are scheduled according to the `PRIORITY` setting. Tasks with high `PRIORITY` are scheduled first. If you do not set the absolute priority, TiKV uses the value of `RU_PER_SEC` of each resource group to determine the priority of the read and write requests for each resource group. Based on the priorities, the storage layer uses the priority queue to schedule and process requests.

## Scenarios for resource control

The introduction of the resource control feature is a milestone for TiDB. It can divide a distributed database cluster into multiple logical units. Even if an individual unit overuses resources, it does not crowd out the resources needed by other units.

With this feature, you can:

- Combine multiple small and medium-sized applications from different systems into a single TiDB cluster. When the workload of an application grows larger, it does not affect the normal operation of other applications. When the system workload is low, busy applications can still be allocated the required system resources even if they exceed the set read and write quotas, so as to achieve the maximum utilization of resources.
- Choose to combine all test environments into a single TiDB cluster, or group the batch tasks that consume more resources into a single resource group. It can improve hardware utilization and reduce operating costs while ensuring that critical applications can always get the necessary resources.

In addition, the rational use of the resource control feature can reduce the number of clusters, ease the difficulty of operation and maintenance, and save management costs.

## Limitations

Currently, the resource control feature has the following limitations:

* This feature only supports flow control and scheduling of read and write requests initiated by foreground clients. It does not support flow control and scheduling of background tasks such as DDL operations and auto analyze.
* Resource control incurs additional scheduling overhead. Therefore, there might be a slight performance degradation when this feature is enabled.

## What is Request Unit (RU)

Request Unit (RU) is a unified abstraction unit in TiDB for system resources, which currently includes CPU, IOPS, and IO bandwidth metrics. The consumption of these three metrics is represented by RU according to a certain ratio.

The following table shows the consumption of TiKV storage layer CPU and IO resources by user requests and the corresponding RU weights.

| Resource        | RU Weight        |
|:----------------|:-----------------|
| CPU             | 1/3 RU per millisecond |
| Read IO         | 1/64 RU per KB       |
| Write IO        | 1 RU/KB          |
| Basic overhead of a read request   | 0.25 RU  |
| Basic overhead of a write request  | 1.5 RU   |

Based on the above table, assuming that the TiKV time consumed by a resource group is `c` milliseconds, `r1` times of requests read `r2` KB data, `w1` times of write requests write `w2` KB data, and the number of non-witness TiKV nodes in the cluster is `n`. Then, the formula for the total RUs consumed by the resource group is as follows:

`c`\* 1/3 + (`r1` \* 0.25 + `r2` \* 1/64) + (1.5 \* `w1` + `w2` \* 1 \* `n`)

## Parameters for resource control

The resource control feature introduces two new global variables.

* TiDB: you can use the [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) system variable to control whether to enable flow control for resource groups.

<CustomContent platform="tidb">

* TiKV: you can use the [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) parameter to control whether to use request scheduling based on resource groups.

</CustomContent>

<CustomContent platform="tidb-cloud">

* TiKV: For on-premises TiDB, you can use the `resource-control.enabled` parameter to control whether to use request scheduling based on resource group quotas. For TiDB Cloud, the value of the `resource-control.enabled` parameter is `true` by default and does not support dynamic modification.

</CustomContent>

The results of the combinations of these two parameters are shown in the following table.

| `resource-control.enabled`  | `tidb_enable_resource_control`= ON   | `tidb_enable_resource_control`= OFF  |
|:----------------------------|:-------------------------------------|:-------------------------------------|
| `resource-control.enabled`= true  |  Flow control and scheduling (recommended) | Invalid combination      |  
| `resource-control.enabled`= false |  Only flow control (not recommended)                 | The feature is disabled. |

For more information about the resource control mechanism and parameters, see [RFC: Global Resource Control in TiDB](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md).

## How to use resource control

### Manage resource groups

To create, modify, or delete a resource group, you need to have the `SUPER` or `RESOURCE_GROUP_ADMIN` privilege.

You can create a resource group for a cluster by using [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md).

For an existing resource group, you can modify the `RU_PER_SEC` option (the rate of RU backfilling per second) of the resource group by using [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md). The changes to the resource group take effect immediately.

You can delete a resource group by using [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md).

### Create a resource group

The following is an example of how to create a resource group.

1. Create a resource group `rg1`. The RU backfill rate is 500 RUs per second and allows applications in this resource group to overrun resources.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg1 RU_PER_SEC = 500 BURSTABLE;
    ```

2. Create a resource group `rg2`. The RU backfill rate is 600 RUs per second and does not allow applications in this resource group to overrun resources.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg2 RU_PER_SEC = 600;
    ```

3. Create a resource group `rg3` with the absolute priority set to `HIGH`. The absolute priority currently supports `LOW|MEDIUM|HIGH`. The default value is `MEDIUM`.

    ```sql
    CREATE RESOURCE GROUP IF NOT EXISTS rg3 RU_PER_SEC = 100 PRIORITY = HIGH;
    ```

### Bind resource groups

TiDB supports three levels of resource group settings as follows.

- User level. Bind a user to a specific resource group via the [`CREATE USER`](/sql-statements/sql-statement-create-user.md) or [`ALTER USER`](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user) statement. After a user is bound to a resource group, sessions created by the user are automatically bound to the corresponding resource group.
- Session level. Set the resource group for the current session via [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md).
- Statement level. Set the resource group for the current statement via [`RESOURCE_GROUP()`](/optimizer-hints.md#resource_groupresource_group_name) Optimizer Hint.

#### Bind users to a resource group

The following example creates a user `usr1` and binds the user to the resource group `rg1`. `rg1` is the resource group created in the example in [Create Resource Group](#create-a-resource-group).

```sql
CREATE USER 'usr1'@'%' IDENTIFIED BY '123' RESOURCE GROUP rg1;
```

The following example uses `ALTER USER` to bind the user `usr2` to the resource group `rg2`. `rg2` is the resource group created in the example in [Create Resource Group](#create-a-resource-group).

```sql
ALTER USER usr2 RESOURCE GROUP rg2;
```

After you bind users, the resource consumption of newly created sessions will be controlled by the specified quota (Request Unit, RU). If the system workload is relatively high and there is no spare capacity, the resource consumption rate of `usr2` will be strictly controlled not to exceed the quota. Because `usr1` is bound by `rg1` with `BURSTABLE` configured, the consumption rate of `usr1` is allowed to exceed the quota.

If there are too many requests that result in insufficient resources for the resource group, the client's requests will wait. If the wait time is too long, the requests will report an error.

> **Note:**
>
> - When you bind a user to a resource group by using `CREATE USER` or `ALTER USER`, it will not take effect for the user's existing sessions, but only for the user's new sessions.
> - TiDB automatically creates a `default` resource group during cluster initialization. For this resource group, the default value of `RU_PER_SEC` is `UNLIMITED` (equivalent to the maximum value of the `INT` type, that is, `2147483647`) and it is in `BURSTABLE` mode. Statements that are not bound to a resource group are automatically bound to this resource group. This resource group does not support deletion, but you can modify the configuration of its RU.

#### Bind the current session to a resource group

By binding a session to a resource group, the resource usage of the corresponding session is limited by the specified usage (RU).

The following example binds the current session to the resource group `rg1`.

```sql
SET RESOURCE GROUP rg1;
```

#### Bind the current statement to a resource group

By adding the [`RESOURCE_GROUP(resource_group_name)`](/optimizer-hints.md#resource_groupresource_group_name) hint to a SQL statement, you can specify the resource group to which the statement is bound. This hint supports `SELECT`, `INSERT`, `UPDATE`, and `DELETE` statements.

The following example binds the current statement to the resource group `rg1`.

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```

## Disable resource control

<CustomContent platform="tidb">

1. Execute the following statement to disable the resource control feature.

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. Set the TiKV parameter [`resource-control.enabled`](/tikv-configuration-file.md#resource-control) to `false` to disable scheduling based on the RU of the resource group.

</CustomContent>

<CustomContent platform="tidb-cloud">

1. Execute the following statement to disable the resource control feature.

    ```sql
    SET GLOBAL tidb_enable_resource_control = 'OFF';
    ```

2. For on-premises TiDB, you can use the `resource-control.enabled` parameter to control whether to use request scheduling based on resource group quotas. For TiDB Cloud, the value of the `resource-control.enabled` parameter is `true` by default and does not support dynamic modification. If you need to disable it for TiDB Cloud Dedicated Tier clusters, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

## Monitoring metrics and charts

<CustomContent platform="tidb">

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** dashboard. The metrics are detailed in the **Resource Control** section of [TiDB Important Monitoring Metrics](/grafana-tidb-dashboard.md).

TiKV also records the request QPS from different resource groups. For more details, see [TiKV Monitoring Metrics Detail](/grafana-tikv-dashboard.md#grpc).

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is only applicable to on-premises TiDB. Currently, TiDB Cloud does not provide resource control metrics.

TiDB regularly collects runtime information about resource control and provides visual charts of the metrics in Grafana's **TiDB** > **Resource Control** dashboard.

TiKV also records the request QPS from different resource groups in Grafana's **TiKV** dashboard.

</CustomContent>

## Tool compatibility

The resource control feature is still in its experimental stage. It does not impact the regular usage of data import, export, and other replication tools. BR, TiDB Lightning, and TiCDC do not currently support processing DDL operations related to resource control, and their resource consumption is not limited by resource control.

## See also

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [RESOURCE GROUP RFC](https://github.com/pingcap/tidb/blob/master/docs/design/2022-11-25-global-resource-control.md)
