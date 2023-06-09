---
title: TiFlash pipeline model 执行模型
summary: 介绍 TiFlash 新的执行模型 pipeline model。
---

# TiFlash pipeline model

> **注意：**
>
> - TiFlash Pipeline Model 目前为实验特性，不建议在生产环境中使用。
> - TiFlash Pipeline Model 目前不支持 [join 算子落盘](/tiflash/tiflash-spill-disk.md)，在开启 join 算子落盘且 `tidb_enable_tiflash_pipeline_model` 设置为 `ON` 时，下推到 tiflash 的查询仍会使用原有的执行模型 Stream Model 来执行。
> - TiFlash Pipeline Model 目前不支持 [TiFlash 存算分离架构与 S3](/tiflash/tiflash-disaggregated-and-s3.md)，在开启 TiFlash 存算分离架构与 S3 且 `tidb_enable_tiflash_pipeline_model` 设置为 `ON` 时，下推到 tiflash 的查询仍会使用原有的执行模型 Stream Model 来执行。

## 启用和禁用 TiFlash pipeline model

默认情况下，session 和 global 级别的变量 `tidb_enable_tiflash_pipeline_model=OFF`，即关闭 TiFlash Pipeline Model。你可以通过以下语句来查看对应的变量信息。

```sql
SHOW VARIABLES LIKE 'tidb_enable_tiflash_pipeline_model';
```

```
+------------------------------------+-------+
| Variable_name                      | Value |
+------------------------------------+-------+
| tidb_enable_tiflash_pipeline_model | OFF   |
+------------------------------------+-------+
```

```sql
SHOW GLOBAL VARIABLES LIKE 'tidb_enable_tiflash_pipeline_model';
```

```
+------------------------------------+-------+
| Variable_name                      | Value |
+------------------------------------+-------+
| tidb_enable_tiflash_pipeline_model | OFF   |
+------------------------------------+-------+
```

变量 `tidb_enable_tiflash_pipeline_model` 支持 session 级别和 global 级别的修改。

- 如果需要在当前 session 中开启 TiFlash Pipeline Model，可以通过以下语句设置:

    ```sql
    SET SESSION tidb_enable_tiflash_pipeline_model=ON;
    ```

- 如果需要在 global 级别开启 TiFlash Pipeline Model，可以通过以下语句设置：

    ```sql
    SET GLOBAL tidb_enable_tiflash_pipeline_model=OFF;
    ```

    设置后，新建的会话中 session 和 global 级别 `tidb_enable_tiflash_pipeline_model` 都将默认启用新值。

如需关闭 TiFlash Pipeline Model，可以通过以下语句设置：

```sql
SET SESSION tidb_enable_tiflash_pipeline_model=OFF;
```

```sql
SET GLOBAL tidb_enable_tiflash_pipeline_model=OFF;
```

## 架构介绍

