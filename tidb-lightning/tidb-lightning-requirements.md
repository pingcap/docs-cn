---
title: Prerequisites for using TiDB Lightning
summary: Learn prerequisites for running TiDB Lightning.
---

# Prerequisites for using TiDB Lightning

Before using TiDB Lightning, you need to check whether the environment meets the requirements. This helps reduce errors during import and ensures import success.

## Downstream privilege requirements

Based on the import mode and features enabled, downstream database users should be granted with different privileges. The following table provides a reference.

<table border="1">
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
      <td>tidb-backend</td>
      <td>information_schema.columns</td>
      <td>SELECT</td>
      <td></td>
   </tr>
   <tr>
      <td  rowspan="3">local-backend</td>
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
      <td>checkpoint.driver = “mysql”</td>
      <td>checkpoint.schema setting</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>Required when checkpoint information is stored in databases, instead of files</td>
   </tr>
</table>

## Downstream storage space requirements

The target TiKV cluster must have enough disk space to store the imported data. In addition to the [standard hardware requirements](/hardware-and-software-requirements.md), the storage space of the target TiKV cluster must be larger than **the size of the data source x the number of replicas x 2**. For example, if the cluster uses 3 replicas by default, the target TiKV cluster must have a storage space larger than 6 times the size of the data source. The formula has x 2 because:

- Indexes might take extra space.
- RocksDB has a space amplification effect.

It is difficult to calculate the exact data volume exported by Dumpling from MySQL. However, you can estimate the data volume by using the following SQL statement to summarize the data-length field in the information_schema.tables table:

Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name.

```sql
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_schema;
```

Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name.

{{< copyable "sql" >}}

```sql
select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;
```

## Resource requirements

**Operating system**: The example in this document uses fresh CentOS 7 instances. You can deploy a virtual machine either on your local host or in the cloud. Because TiDB Lightning consumes as much CPU resources as needed by default, it is recommended that you deploy it on a dedicated server. If this is not possible, you can deploy it on a single server together with other TiDB components (for example, tikv-server) and then configure `region-concurrency` to limit the CPU usage from TiDB Lightning. Usually, you can configure the size to 75% of the logical CPU.

**Memory and CPU**:

The CPU and memory consumed by TiDB Lightning vary with the backend mode. Run TiDB Lightning in an environment that supports the optimal import performance based on the backend you use.

- Local-backend: TiDB lightning consumes much CPU and memory in this mode. It is recommended that you allocate CPU higher than 32 cores and memory greater than 64 GiB.

> **Note**:
>
> When data to be imported is large, one parallel import may consume about 2 GiB memory. In this case, the total memory usage can be `region-concurrency` x 2 GiB. `region-concurrency` is the same as the number of logical CPUs. If the memory size (GiB) is less than twice of the CPU or OOM occurs during the import, you can decrease `region-concurrency` to address OOM.

- TiDB-backend: In this mode, the performance bottleneck lies in TiDB. It is recommended that you allocate 4-core CPU and 8 GiB memory for TiDB Lightning. If the TiDB cluster does not reach the write threshold in an import, you can increase `region-concurrency`.
- Importer-backend: In this mode, resource consumption is nearly the same as that in Local-backend. Importer-backend is not recommended and you are advised to use Local-backend if you have no particular requirements.

**Storage space**: The `sorted-kv-dir` configuration item specifies the temporary storage directory for the sorted key-value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.
