---
title: 使用 TiDB Lightning 所需要的前提条件
summary: 了解 TiDB Lightning 运行时所需要的各种要求。
---

# 使用 Lightning 时所需要的前提条件

使用 Lightning 导入数据之前，预先检查环境确认是否满足要求，有助于减少导入过程的错误，避免导入失败的情况。

## 下游数据库权限要求

Lightning 导入数据时，根据所使用的导入方式，启用的特性等，需要下游数据库用户具备不同的权限，可参考下表：

<table border=1>
   <tr>
      <td></td>
      <td>特性</td>
      <td>作用域</td>
      <td>所需权限</td>
      <td>备注</td>
   </tr>
   <tr>
      <td rowspan="2">必需</td>
      <td rowspan="2">基本功能</td>
      <td>目标 table</td>
      <td>CREATE,SELECT,INSERT,UPDATE,DELETE,DROP,ALTER</td>
      <td>DROP 仅 tidb-lightning-ctl 在执行 checkpoint-destroy-all 时需要</td>
   </tr>
   <tr>
      <td>目标 database</td>
      <td>CREATE</td>
      <td></td>
   </tr>
   <tr>
      <td rowspan="4">必需</td>
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
      <td>当目标 TiDB 开启 SEM</td>
   </tr>
   <tr>
      <td>推荐</td>
      <td>冲突检测，max-error</td>
      <td>lightning.task-info-schema-name 配置的 schema</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>如不需要，该值必需设为""</td>
   </tr>
   <tr>
      <td>可选</td>
      <td>并行导入</td>
      <td>lightning.meta-schema-name 配置的 schema</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>如不需要，该值必需设为""</td>
   </tr>
   <tr>
      <td>可选</td>
      <td>checkpoint.driver = “mysql”</td>
      <td>checkpoint.schema 设置</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>使用数据库而非文件形式存放 checkpoint 信息时</td>
   </tr>
</table>

## 下游数据库所需空间

目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/deploy-and-maintain-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。公式中的 2 倍可能难以理解，其依据是以下因素的估算空间占用：

- 索引会占据额外的空间
- RocksDB 的空间放大效应

目前无法精确计算 Dumpling 从 MySQL 导出的数据大小，但你可以用下面 SQL 语句统计信息表的 data_length 字段估算数据量：

统计所有 schema 大小，单位 MiB，注意修改 ${schema_name}

{{< copyable "sql" >}}

```sql
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_schema;
```

统计最大单表，单位 MiB，注意修改 ${schema_name}

{{< copyable "sql" >}}

```sql
select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;
```

## Lightning 运行时资源要求

**操作系统**：一般建议使用新的、纯净版 CentOS 7 实例，您可以在本地虚拟化或在供应商提供的平台上部署一台小型的云虚拟主机。TiDB Lightning 运行过程默认会占满 CPU，建议单独部署。如果条件不允许，可以和其他组件（比如 `tikv-server`）部署在同一台机器上，然后通过配置 `region-concurrency` 限制 TiDB Lightning 使用 CPU 资源。混合部署的情况下可以将其大小配置为逻辑 CPU 数的 75%，以限制 CPU 的使用。

**内存和 CPU**：因为 TiDB Lightning 对计算机资源消耗较高，建议分配 64 GB 以上的内存以及 32 核以上的 CPU，而且确保 CPU 核数和内存（GB）比为 1:2 以上，以获取最佳性能。

**存储空间**：配置项 `sorted-kv-dir` 设置排序的键值对的临时存放地址，目标路径需要是一个空目录，至少需要数据源最大单表的空间。建议与 `data-source-dir` 使用不同的存储设备，独占 IO 会获得更好的导入性能，且建议优先考虑配置闪存等高性能存储介质。

**网络**： 建议使用带宽 >=10Gbps 的网卡。