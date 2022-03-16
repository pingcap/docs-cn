---
title: BR 批量建表
summary: 了解如何使用 BR 工具的批量建表功能。在恢复备份数据时，BR 可以通过批量建表功能加快数据的恢复速度。
---

# BR 批量建表

使用 BR 工具（以下简称为 BR）执行数据恢复任务时，BR 会先在下游 TiDB 创建库和表后，再进行数据恢复。在 TiDB v6.0 之前，在数据恢复阶段创建表时，BR 采用了[串行执行](#实现原理)的方案。然而，当需要恢复的数据中带有大量的表（【约 XXX 张】）时，该方案会在创建表时消耗较多时间。

为了加快 BR 在执行数据恢复任务时创建表的速度，从而减少数据恢复时间，从 TiDB v6.0 起，BR 引入了批量建表功能，此功能会默认开启。

> **注意：**
>
> 为使用 BR 建表功能，TiDB 和 BR 都必须为 v6.0 或以上版本。如果 TiDB 或 BR 的任意一方的版本低于 v6.0，BR 会采用原来的串行建表方案。

## 使用场景

当需要恢复的数据中带有大量的表（【约 XXX 张】）时，使用 BR 批量建表功能可以明显地提升数据恢复速度。具体提升效果，请见[测试结果](#实现原理)。

## 使用方法

BR 默认开启了批量建表功能，在 v6.0 或以上版本中默认设置了 `--ddl-batch-size=128`。因此，你不需要额外配置该参数。

- 如果需要关闭此功能，你可以通过以下命令将 `--ddl-batch-size` 的值设置为 `0`：

    {{< copyable "shell-regular" >}}
    【XXX】

    关闭批量建表功能后，BR 会采用原来的[串行建表方案](#实现原理)。

- 如果你需要恢复的数据中有过多的表（约大于 5 万张），推荐在 BR 中同时配置 `--concurrency=1024` 和 `--ddl-batch-size=256`：

    {{< copyable "shell-regular" >}}

    ```shell
    bin/br restore full -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024 --ddl-batch-size=256
    ```

    其中，`--concurrency` 参数用于进行性能调优，默认值为 【`128`（待确认）】。

    内部测试显示，在恢复数据时同时配置上述的两个参数后，创建 6 万张表仅需 5 分钟。

## 实现原理

在 v6.0 之前的版本，BR 采用了串行建表方案。在使用 BR 执行数据恢复任务时，BR 会先在下游 TiDB 创建库和表后，再开始进行数据恢复。在建表的过程中，BR 调用 TiDB 接口，使用 SQL `Create Table` 创建表，并由 TiDB DDL owner 依次串行执行建表任务。然而，每张表被创建时会引起一次 schema 版本的变更，每次的 schema 变更需要同步到【其他 BR 和其他 TiDB（其他能否用其他更仔细的描述代替呢？）】。该方案会导致在需要创建的表比较多的场景下，建表时间过长。

批量建表功能采用并发批量建表方案。在默认情况下，BR 以 128 张表为一批，并发创建多批表。采用该方案后，BR 每次建一批表时，TiDB schema 版本仅会变更一次。此方法极大地提高了建表速度。

以下为在 TiDB v6.0 集群中测试批量建表功能的测试内容。具体的测试条件如下：

【这里可以补充在同等条件下，“未开启功能”时的数据吗？这样用户可以看出功能开启前后的明显的对比】

- 集群配置：
    - 15 个 TiKV
        - 配备 16 个 CPU 80 G 内存
        - [import.num-threads](/tikv-configuration-file.md#num-threads) 设置为 `16`
    - 3 个 TiDB
    - 3 个 PD
- 待恢复数据的规模：16.16 TB

具体测试结果如下：

```
‘[2022/03/12 22:37:49.060 +08:00] [INFO] [collector.go:67] ["Full restore success summary"] [total-ranges=751760] [ranges-succeed=751760] [ranges-failed=0] [split-region=1h33m18.078448449s] [restore-ranges=542693] [total-take=1h41m35.471476438s] [restore-data-size(after-compressed)=8.337TB] [Size=8336694965072] [BackupTS=431773933856882690] [total-kv=148015861383] [total-kv-size=16.16TB] [average-speed=2.661GB/s]’
```

- 恢复吞吐：`average-speed=2.661GB/s`
- 单个 TiKV 实例的平均恢复速度：`average-speed(GB/s)`/`tikv_count` = `181.65(MB/s)`