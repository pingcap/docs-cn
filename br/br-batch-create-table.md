---
title: 批量建表
summary: 了解如何使用批量建表功能。在恢复备份数据时，可以通过批量建表功能加快数据的恢复速度。
---

# 批量建表

使用 Backup & Restore (BR) 执行数据恢复任务时，BR 会先在目标 TiDB 集群上创建库和表，然后再把已备份的数据恢复到表中。TiDB v6.0.0 之前，在数据恢复阶段创建表时，BR 采用了[串行执行](#实现原理)的方案。然而，当需要恢复的数据中带有大量的表（约 50000 张）时，该方案会在创建表上消耗较多时间。

为了加快创建表的速度，以减少数据恢复的时间，TiDB 在 v6.0.0 中引入了批量建表功能，此功能默认开启。

> **注意：**
>
> - 为使用批量建表功能，TiDB 和 br 命令行工具都必须为 v6.0.0 或以上版本。如果 TiDB 或 br 命令行工具的任意一方的版本低于 v6.0.0，br 命令行工具会采用原来的串行建表方案。
> - 如果你在使用 TiUP 等集群管理工具，而且你使用的 TiDB 和 br 命令行工具是 v6.0.0 或以上版本，或是从 v6.0.0 以下版本升级至该版本，此时，br 工具会默认开启批量建表功能，你不需要额外进行相关配置。

## 使用场景

当需要恢复的数据中带有大量的表（约 50000 张）时，你可以使用批量建表功能显著提升数据恢复的速度。

具体提速效果可参考[测试结果](#功能测试)。

## 使用方法

Backup & Restore (BR) 默认开启批量建表功能，在 v6.0.0 或以上版本中默认设置了 `--ddl-batch-size=128`（以 128 张表为一批，并发创建多批表），以加快恢复时的建表速度。因此，你不需要额外配置该参数。

如果需要关闭此功能，你可以参考以下命令将 `--ddl-batch-size` 的值设置为 `1`：

```shell
br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ddl-batch-size=1
```

关闭批量建表功能后，BR 会采用原来的[串行建表方案](#实现原理)。

## 实现原理

- v6.0.0 前的串行建表方案：

    执行数据恢复任务时，BR 会先在目标 TiDB 集群上创建库和表，然后再把已备份的数据恢复到表中。建表时，BR 会调用 TiDB 内部 API 后开始创建表，其运作方式类似 BR 执行 SQL `Create Table` 语句。建表任务由 TiDB DDL owner 依次串行执行。DDL owner 每创建一张表会引起一次 DDL schema 版本的变更，而每次的 schema 版本的变更都需要同步到其他 TiDB DDL worker（含 BR）。因此，当需要创建的表的数量比较多时，串行建表方案会导致建表时间过长。

- v6.0.0 起的批量建表方案：

    在默认情况下，BR 会以 128 张表为一批，并发创建多批表。采用该方案后，BR 每建一批表时，TiDB schema 版本只会变更一次。此方法极大地提高了建表速度。

## 功能测试

以下是在 TiDB v6.0.0 集群中测试批量建表功能的内容。具体的测试环境如下：

- 集群配置：
    - 15 个 TiKV 实例，每个 TiKV 实例共有 16 个 CPU 核心、80 GB 内存、16 个处理 RPC 请求的线程（即 [`import.num-threads`](/tikv-configuration-file.md#num-threads) = 16）
    - 3 个 TiDB 实例，每个 TiDB 实例共有 16 个 CPU 核心、32 GB 内存。
    - 3 个 PD 实例，每个 PD 实例共有 16 个 CPU 核心、32 GB 内存。
- 待恢复数据的规模：16.16 TB

测试结果如下：

```
‘[2022/03/12 22:37:49.060 +08:00] [INFO] [collector.go:67] ["Full restore success summary"] [total-ranges=751760] [ranges-succeed=751760] [ranges-failed=0] [split-region=1h33m18.078448449s] [restore-ranges=542693] [total-take=1h41m35.471476438s] [restore-data-size(after-compressed)=8.337TB] [Size=8336694965072] [BackupTS=431773933856882690] [total-kv=148015861383] [total-kv-size=16.16TB] [average-speed=2.661GB/s]’
```

从结果可见，单个 TiKV 实例的平均恢复速度高达 181.65 MB/s（即 `average-speed`/`tikv_count`）。
