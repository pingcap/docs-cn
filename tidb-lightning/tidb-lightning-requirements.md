---
title: TiDB Lightning 目标数据库要求
summary: 了解 TiDB Lightning 运行时对目标数据库的必需条件。
---

# TiDB Lightning 目标数据库要求

使用 TiDB Lightning 导入数据前，先检查环境是否满足要求，这有助于减少导入过程的错误，避免导入失败的情况。

## 目标数据库权限要求

TiDB Lightning 导入数据时，根据导入方式和启用特性等，需要下游数据库用户具备不同的权限，可参考下表：

<table>
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
      <td>逻辑导入模式</td>
      <td>information_schema.columns</td>
      <td>SELECT</td>
      <td></td>
   </tr>
   <tr>
      <td  rowspan="3">物理导入模式</td>
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
      <td>如不需要，该值必须设为""</td>
   </tr>
   <tr>
      <td>可选</td>
      <td>并行导入</td>
      <td>lightning.meta-schema-name 配置的 schema</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>如不需要，该值必须设为""</td>
   </tr>
   <tr>
      <td>可选</td>
      <td>checkpoint.driver = "mysql"</td>
      <td>checkpoint.schema 设置</td>
      <td>SELECT,INSERT,UPDATE,DELETE,CREATE,DROP</td>
      <td>使用数据库而非文件形式存放 checkpoint 信息时需要</td>
   </tr>
</table>

## 目标数据库所需空间

目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/manage-cluster-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。公式中的 2 倍可能难以理解，其依据是以下因素的估算空间占用：

- 索引会占据额外的空间
- RocksDB 的空间放大效应

目前无法精确计算 Dumpling 从 MySQL 导出的数据大小，但你可以用下面 SQL 语句统计信息表的 `DATA_LENGTH` 字段估算数据量：

统计所有 schema 大小，单位 MiB，注意修改 ${schema_name}

```sql
-- 统计所有 schema 大小
SELECT
  TABLE_SCHEMA,
  FORMAT_BYTES(SUM(DATA_LENGTH)) AS 'Data Size',
  FORMAT_BYTES(SUM(INDEX_LENGTH)) 'Index Size'
FROM
  information_schema.tables
GROUP BY
  TABLE_SCHEMA;

-- 统计最大的 5 个单表
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