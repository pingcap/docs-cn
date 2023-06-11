---
title: TiFlash Pipeline Model 执行模型
summary: 介绍 TiFlash 新的执行模型 Pipeline Model。
---

# TiFlash Pipeline Model

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

- 如果需要在当前 session 中开启 TiFlash Pipeline Model，可以通过以下语句设置：

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

## 设计实现

TiFlash 原有执行模型 Stream Model 是线程调度执行模型，每一个查询会独立申请若干条线程协同执行。

线程调度模型存在两个缺陷

- 在高并发场景下，过多的线程会引起较多上下文切换，导致较高的线程调度代价。甚至在线程数达到一定数量时，申请线程会报错 `thread constructor failed: Resource temporarily unavailable`。

- 线程调度模型无法精准计量查询的资源使用量以及做细粒度的资源管控。

在新的执行模型 Pipeline Model 中

- Query 被划分为若干 pipeline 执行。在 pipeline 中数据块会尽可能被保留在 cache 中，有很好的时间局部性。

- 将 pipeline 实例化成若干个 task，摆脱 OS 原生的线程调度模型，使用更加精细的 task 调度模型，同时使用固定线程池，减少了 OS 申请和调度线程的开销。

![TiFlash Pipeline Model Design](/media/tiflash/tiflash-pipeline-model.png)
