---
title: Table Attributes
summary: Learn how to use the table attribute feature of TiDB.
---

# Table Attributes

The Table Attributes feature is introduced in TiDB v5.3.0. Using this feature, you can add specific attributes to a table or partition to perform the operations corresponding to the attributes. For example, you can use table attributes to control the Region merge behavior.

<CustomContent platform="tidb">

Currently, TiDB only supports adding the `merge_option` attribute to a table or partition to control the Region merge behavior. The `merge_option` attribute is only part of how to deal with hotspots. For more information, refer to [Troubleshoot Hotspot Issues](/troubleshoot-hot-spot-issues.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Currently, TiDB only supports adding the `merge_option` attribute to a table or partition to control the Region merge behavior. The `merge_option` attribute is only part of how to deal with hotspots.

</CustomContent>

> **Note:**
>
> - When you use TiDB Binlog or TiCDC to perform replication or use BR to perform incremental backup, the replication or backup operations skip the DDL statement that sets table attributes. To use table attributes in the downstream or in the backup cluster, you need to manually execute the DDL statement in the downstream or in the backup cluster.

## Usage

The table attribute is in the form of `key=value`. Multiple attributes are separated by commas. In the following examples, `t` is the name of the table to be modified, `p` is the name of the partition to be modified. Items in `[]` are optional.

+ Set attributes for a table or partition:

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] 'key=value[, key1=value1...]';
    ```

+ Reset attributes for a table or partition:

    ```sql
    ALTER TABLE t [PARTITION p] ATTRIBUTES [=] DEFAULT;
    ```

+ See the attributes of all tables and partitions:

    ```sql
    SELECT * FROM information_schema.attributes;
    ```

+ See the attribute configured to a table or partition:

    ```sql
    SELECT * FROM information_schema.attributes WHERE id='schema/t[/p]';
    ```

+ See all tables and partitions that have a specific attribute:

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%key%';
    ```

## Attribute override rules

The attribute configured to a table takes effect on all partitions of the table. However, there is one exception: If the table and partition are configured with the same attribute but different attribute values, the partition attribute overrides the table attribute. For example, suppose that the table `t` is configured with the `key=value` attribute, and the partition `p` is configured with `key=value1`.

```sql
ALTER TABLE t ATTRIBUTES[=]'key=value';
ALTER TABLE t PARTITION p ATTRIBUTES[=]'key=value1';
```

In this case, `key=value1` is the attribute that actually takes effect on the `p1` partition.

## Control the Region merge behavior using table attributes

### User scenarios

If there is a write hotspot or read hotspot, you can use table attributes to control the Region merge behavior. You can first add the `merge_option` attribute to a table or partition and then set its value to `deny`. The two scenarios are as follows.

#### Write hotspot on a newly created table or partition

If a hotspot issue occurs when data is written to a newly created table or partition, you usually need to split and scatter Regions. However, if there is a certain time interval between the split/scatter operation and writes, these operations do not truly avoid the write hotspot. This is because the split operation performed when the table or partition is created produces empty Regions, so if the time interval exists, the split Regions might be merged. To handle this case, you can add the `merge_option` attribute to the table or partition and set the attribute value to `deny`.

#### Periodic read hotspot in read-only scenarios

Suppose that in a read-only scenario, you try to reduce the periodic read hotspot that occurs on a table or partition by manually splitting Regions, and you do not want the manually split Regions to be merged after the hotspot issue is resolved. In this case, you can add the `merge_option` attribute to the table or partition and set its value to `deny`.

### Usage

+ Prevent the Regions of a table from merging:

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=deny';
    ```

+ Allow merging Regions belonging to a table:

    ```sql
    ALTER TABLE t ATTRIBUTES 'merge_option=allow';
    ```

+ Reset attributes of a table:

    ```sql
    ALTER TABLE t ATTRIBUTES DEFAULT;
    ```

+ Prevent the Regions of a partition from merging:

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=deny';
    ```

+ Allow merging Regions belonging to a partition:

    ```sql
    ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
    ```

+ See all tables or partitions configured the `merge_option` attribution:

    ```sql
    SELECT * FROM information_schema.attributes WHERE attributes LIKE '%merge_option%';
    ```

### Attribute override rules

```sql
ALTER TABLE t ATTRIBUTES 'merge_option=deny';
ALTER TABLE t PARTITION p ATTRIBUTES 'merge_option=allow';
```

When the above two attributes are configured at the same time, the Regions belonging to the partition `p` can actually be merged. When the attribute of the partition is reset, the partition `p` inherits the attribute from the table `t`, and the Regions cannot be merged.

<CustomContent platform="tidb">

> **Note:**
>
> - For a table with partitions, if the `merge_option` attribute is configured at the table level only, even if `merge_option=allow`, the table is still split into multiple Regions by default according to the actual number of partitions. To merge all Regions, you need to [reset the attribute of the table](#usage).
> - When using the `merge_option` attribute, you need to pay attention to the PD configuration parameter [`split-merge-interval`](/pd-configuration-file.md#split-merge-interval). Suppose that the `merge_option` attribute is not configured. In this case, if Regions meet conditions, Regions can be merged after the interval specified by `split-merge-interval`. If the `merge_option` attribute is configured, PD decides whether to merge Regions after the specified interval according to the `merge_option` configuration.

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - For a table with partitions, if the `merge_option` attribute is configured at the table level only, even if `merge_option=allow`, the table is still split into multiple Regions by default according to the actual number of partitions. To merge all Regions, you need to [reset the attribute of the table](#usage).
> - Suppose that the `merge_option` attribute is not configured. In this case, if Regions meet conditions, Regions can be merged after one hour. If the `merge_option` attribute is configured, PD decides whether to merge Regions after one hour according to the `merge_option` configuration.

</CustomContent>