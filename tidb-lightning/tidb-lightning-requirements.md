---
title: TiDB Lightning 目标数据库要求
summary: 了解 TiDB Lightning 运行时对目标数据库的必需条件。
---

# TiDB Lightning 目标数据库要求

使用 TiDB Lightning 导入数据前，先检查环境是否满足要求，这有助于减少导入过程的错误，避免导入失败的情况。

## 目标数据库权限要求

TiDB Lightning 导入数据时，根据导入方式和启用特性等，需要下游数据库用户具备不同的权限，可参考下表：

+------+---------------+-------------------+-------------------------+-----------------------+
|      | 特性           | 作用域             | 所需权限                 | 备注                   |
+======+===============+===================+=========================+=======================+
| 必需  | 基本功能       | 目标 table        | CREATE,SELECT,INSERT,UPDATE,DELETE,DROP,ALTER | DROP 仅 tidb-lightning-ctl 在执行 checkpoint-destroy-all 时需要 |
|      |               +-------------------+-------------------------+-----------------------+
|      |               | 目标 database      | CREATE                  |                       |
+------+---------------+-------------------+-------------------------+-----------------------+
| 必需  | Logical Import Mode | information_schema.columns | SELECT   |                       |
|      +---------------+-------------------+-------------------------+-----------------------+
|      | Physical Import Mode | mysql.tidb        | SELECT           |                       |
|      |                      +-------------------+------------------+-----------------------+
|      |                      | -                 | SUPER            |                       |
|      |                      +-------------------+------------------+-----------------------+
|      |                      | -                 | RESTRICTED_VARIABLES_ADMIN,RESTRICTED_TABLES_ADMIN | 当目标 TiDB 开启 SEM |
+------+---------------+-------------------+-------------------------+-----------------------+
| 推荐  | 冲突检测，max-error | lightning.task-info-schema-name 配置的 schema | SELECT,INSERT,UPDATE,DELETE,CREATE,DROP | 如不需要，该值必须设为 "" |
+------+---------------+-------------------+-------------------------+-----------------------+
| 可选  | 并行导入       | lightning.meta-schema-name 配置的 schema | SELECT,INSERT,UPDATE,DELETE,CREATE,DROP | 如不需要，该值必须设为 "" |
+------+---------------+-------------------+-------------------------+-----------------------+
| 可选  | checkpoint.driver = "mysql" | checkpoint.schema 设置 | SELECT,INSERT,UPDATE,DELETE,CREATE,DROP | 使用数据库而非文件形式存放 checkpoint 信息时需要 |
+------+---------------+-------------------+-------------------------+-----------------------+

## 目标数据库所需空间

目标 TiKV 集群必须有足够空间接收新导入的数据。除了[标准硬件配置](/hardware-and-software-requirements.md)以外，目标 TiKV 集群的总存储空间必须大于 **数据源大小 × [副本数量](/faq/manage-cluster-faq.md#每个-region-的-replica-数量可配置吗调整的方法是) × 2**。例如集群默认使用 3 副本，那么总存储空间需为数据源大小的 6 倍以上。公式中的 2 倍可能难以理解，其依据是以下因素的估算空间占用：

- 索引会占据额外的空间
- RocksDB 的空间放大效应

目前无法精确计算 Dumpling 从 MySQL 导出的数据大小，但你可以用下面 SQL 语句统计信息表的 data_length 字段估算数据量：

统计所有 schema 大小，单位 MiB，注意修改 ${schema_name}

{{< copyable "sql" >}}

```sql
SELECT table_schema, SUM(data_length)/1024/1024 AS data_length, SUM(index_length)/1024/1024 AS index_length, SUM(data_length+index_length)/1024/1024 AS sum FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;
```

统计最大单表，单位 MiB，注意修改 ${schema_name}

{{< copyable "sql" >}}

```sql
SELECT table_name, table_schema, SUM(data_length)/1024/1024 AS data_length, SUM(index_length)/1024/1024 AS index_length, SUM(data_length+index_length)/1024/1024 AS sum FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY sum  DESC LIMIT 5;
```