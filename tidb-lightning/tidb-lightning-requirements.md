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

It is difficult to calculate the exact data volume exported by Dumpling from MySQL. However, you can estimate the data volume by using the following SQL statement to summarize the `DATA_LENGTH` field in the information_schema.tables table:

```sql
-- Calculate the size of all schemas
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- Calculate the 5 largest tables
SELECT 
  TABLE_NAME,
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(data_length)) AS 'Data Size',
  FORMAT_BYTES(SUM(index_length)) AS 'Index Size',
  FORMAT_BYTES(SUM(data_length+index_length)) AS 'Total Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_NAME,
  TABLE_SCHEMA
ORDER BY
  SUM(DATA_LENGTH+INDEX_LENGTH) DESC
LIMIT
  5;
```
