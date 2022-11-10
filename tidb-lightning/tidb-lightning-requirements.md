---
title: TiDB Lightning Requirements for the Target Database
summary: Learn prerequisites for running TiDB Lightning.
---

# TiDB Lightning Requirements for the Target Database

Before using TiDB Lightning, you need to check whether the environment meets the requirements. This helps reduce errors during import and ensures import success.

## Privileges of the target database

Based on the import mode and features enabled, the target database users should be granted with different privileges. The following table provides a reference.

<table>
   <tr>
      <td></td>
      <td>Feature</td>
      <td>Scope</td>
      <td>Required privilege</td>
      <td>Remarks</td>
   </tr>
   <tr>
      <td rowspan="2">Mandatory</td>
      <td rowspan="2">Basic functions</td>
      <td>Target table</td>
      <td>CREATE, SELECT, INSERT, UPDATE, DELETE, DROP, ALTER</td>
      <td>DROP is required only when tidb-lightning-ctl runs the checkpoint-destroy-all command</td>
   </tr>
   <tr>
      <td>Target database</td>
      <td>CREATE</td>
      <td></td>
   </tr>
   <tr>
      <td rowspan="4">Mandatory</td>
      <td>Logical Import Mode</td>
      <td>information_schema.columns</td>
      <td>SELECT</td>
      <td></td>
   </tr>
   <tr>
      <td rowspan="3">Physical Import Mode</td>
      <td>mysql.tidb</td>
      <td>SELECT</td>
      <td></td>
   </tr>
   <tr>
      <td>-</td>
      <td>SUPER</td>
      <td></td>
   </tr>
   <tr>
      <td>-</td>
      <td>RESTRICTED_VARIABLES_ADMIN,RESTRICTED_TABLES_ADMIN</td>
      <td>Required when the target TiDB enables SEM</td>
   </tr>
   <tr>
      <td>Recommended</td>
      <td>Conflict detection, max-error</td>
      <td>Schema configured for lightning.task-info-schema-name</td>
      <td>SELECT, INSERT, UPDATE, DELETE, CREATE, DROP</td>
      <td>If not required, the value must be set to ""</td>
   </tr>
   <tr>
      <td>Optional</td>
      <td>Parallel import</td>
      <td>Schema configured for lightning.meta-schema-name</td>
      <td>SELECT, INSERT, UPDATE, DELETE, CREATE, DROP</td>
      <td>If not required, the value must be set to ""</td>
   </tr>
   <tr>
      <td>Optional</td>
      <td>checkpoint.driver = "mysql"</td>
      <td>checkpoint.schema setting</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>Required when checkpoint information is stored in databases, instead of files</td>
   </tr>
</table>

## Storage space of the target database

The target TiKV cluster must have enough disk space to store the imported data. In addition to the [standard hardware requirements](/hardware-and-software-requirements.md), the storage space of the target TiKV cluster must be larger than **the size of the data source x the number of replicas x 2**. For example, if the cluster uses 3 replicas by default, the target TiKV cluster must have a storage space larger than 6 times the size of the data source. The formula has x 2 because:

- Indexes might take extra space.
- RocksDB has a space amplification effect.

It is difficult to calculate the exact data volume exported by Dumpling from MySQL. However, you can estimate the data volume by using the following SQL statement to summarize the data-length field in the information_schema.tables table:

Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name.

```sql
SELECT table_schema, SUM(data_length)/1024/1024 AS data_length, SUM(index_length)/1024/1024 AS index_length, SUM(data_length+index_length)/1024/1024 AS sum FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;
```

Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name.

{{< copyable "sql" >}}

```sql
SELECT table_name, table_schema, SUM(data_length)/1024/1024 AS data_length, SUM(index_length)/1024/1024 AS index_length,sum(data_length+index_length)/1024/1024 AS sum FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY sum DESC LIMIT 5;
```
