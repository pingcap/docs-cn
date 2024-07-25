---
title: TiDB 备份与恢复实践示例
summary: 介绍 TiDB 备份与恢复的具体使用示例，包括推荐环境配置、存储配置、备份策略及如何进行备份与恢复。
---

# TiDB 备份与恢复实践示例

[TiDB 快照备份与恢复使用指南](/br/br-snapshot-guide.md)及 [TiDB 日志备份与 PITR 使用指南](/br/br-pitr-guide.md)系统介绍了 TiDB 提供的备份与恢复方案，即快照（全量）备份与恢复、日志备份和恢复到指定时间点 (Point-in-time recovery, PITR)。本文档将基于具体的使用场景，介绍如何快速上手使用 TiDB 的备份与恢复方案。

介绍具体操作前，设想有如下使用场景，你在 AWS 部署了一套 TiDB 生产集群，业务团队提出如下需求：

- 及时备份用户数据变更，在数据库遭遇异常情况时，能够以最小的数据丢失代价（容忍异常前几分钟内的用户数据丢失）快速地恢复业务。
- 每个月不定期进行业务审计。接收到审计请求后，提供一个数据库来查询审计要求的一个月内某个时间点的数据。

通过 TiDB 提供的 PITR 功能，你可以满足业务团队的需求。

## 部署 TiDB 集群和 br 命令行工具

使用 PITR 功能，需要部署 v6.2.0 或以上版本的 TiDB 集群，并且更新 br 命令行工具到与 TiDB 集群相同的版本，本文假设使用的是 v7.5.3 版本。

下表介绍了在 TiDB 集群中使用日志备份功能的推荐配置。

|**组件** | **CPU** | **内存** |**硬盘类型** | **AWS 机型** | **实例数量** |
| --- | --- | --- | --- | --- | --- |
| TiDB | 8 核+ | 16 GB+ | SAS | c5.2xlarge | 2 |
| PD | 8 核+ | 16 GB+ | SSD | c5.2xlarge | 3 |
| TiKV | 8 核+ | 32 GB+ | SSD | m5.2xlarge | 3 |
| br cli | 8 核+ | 16 GB+ | SAS | c5.2xlarge | 1 |
| 监控 | 8 核+ | 16 GB+ | SAS | c5.2xlarge | 1 |

> **注意：**
>
> - br 命令行工具执行备份恢复功能需要访问 PD 和 TiKV，请确保 br 命令行工具与所有 PD 和 TiKV 连接正常。
> - br 命令行工具与 PD 所在服务器时区需要相同。

使用 TiUP 部署或升级 TiDB 集群：

- 如果没有部署 TiDB 集群，请[部署 TiDB 集群](/production-deployment-using-tiup.md)。
- 如果已经部署的 TiDB 集群版本低于 v6.2.0，请[升级 TiDB 集群](/upgrade-tidb-using-tiup.md)。

使用 TiUP 安装或升级 br 命令行工具：

- 安装：

    ```shell
    tiup install br:v7.5.3
    ```

- 升级：

    ```shell
    tiup update br:v7.5.3
    ```

## 配置备份存储 (Amazon S3)

在开始备份任务之前需要准备好备份存储，包括：

1. 准备用于存放备份数据的 S3 bucket 和目录；
2. 配置访问 S3 中备份目录的权限；
3. 规划备份数据保存的目录结构。

配置备份存储的步骤如下：

1. 在 S3 创建用于保存备份数据的目录 `s3://tidb-pitr-bucket/backup-data`。

    1. 创建 bucket。你也可以选择已有的 S3 bucket 来保存备份数据。如果没有可用的 bucket，可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html)创建一个 S3 Bucket。本文使用的 bucket 名为 `tidb-pitr-bucket`。
    2. 创建备份数据总目录。在上一步创建的 bucket（例如 `tidb-pitr-bucket`）下创建目录 `backup-data`，参考 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html)。

2. 配置 br 命令行工具和 TiKV 访问 S3 中的备份目录的权限。本文推荐使用最安全的 IAM 访问方式，配置过程可以参考[控制存储桶访问](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/walkthrough1.html)。权限要求如下：

    - 备份集群的 TiKV 和 br 命令行工具需要的 `s3://tidb-pitr-bucket/backup-data` 权限：`s3:ListBucket`、`s3:GetObject`、`s3:DeleteObject`、`s3:PutObject` 和 `s3:AbortMultipartUpload`。
    - 恢复集群的 TiKV 和 br 命令行工具需要 `s3://tidb-pitr-bucket/backup-data` 的最小权限：`s3:ListBucket`、`s3:GetObject`、`s3:DeleteObject` 和 `s3:PutObject`。

3. 规划备份数据保存的目录结构，以及快照（全量）备份和日志备份的目录。

    - 所有快照备份保存在 `s3://tidb-pitr-bucket/backup-data/snapshot-${date}` 目录下，`${date}` 为快照备份开始的时间点，如在 2022/05/12 00:01:30 开始的快照备份保存为 `s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`。
    - 日志备份保存在 `s3://tidb-pitr-bucket/backup-data/log-backup/` 目录下。

## 确定备份策略

为了满足业务最小数据丢失、快速恢复、一个月内任意时间点审计需求，你可以制定如下备份策略：

- 运行日志备份，持续不断备份数据库数据变更；
- 每隔两天在零点左右进行一次快照备份；
- 保存 30 天内的快照备份和日志备份数据，清理超过 30 天的备份数据。

## 执行日志备份

启动日志备份任务后，日志备份进程会在 TiKV 集群运行，持续不断将数据库变更数据备份到 S3 中。日志备份任务启动命令：

```shell
tiup br log start --task-name=pitr --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

启动日志备份任务后，可以查询日志备份任务状态：

```shell
tiup br log status --task-name=pitr --pd="${PD_IP}:2379"

● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-13 11:09:40.7 +0800
      end: 2035-01-01 00:00:00 +0800
    storage: s3://tidb-pitr-bucket/backup-data/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

## 执行快照备份

通过自动化运维工具（如 crontab）设置定期的快照备份任务，例如：每隔两天在零点左右进行一次快照（全量）备份。下面是两次备份的示例：

- 在 2022/05/14 00:00:00 执行一次快照备份：

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
    --backupts='2022/05/14 00:00:00 +08:00'
    ```

- 在 2022/05/16 00:00:00 执行一次快照备份：

    ```shell
    tiup br backup full --pd="${PD_IP}:2379" \
    --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220516000000' \
    --backupts='2022/05/16 00:00:00 +08:00'
    ```

## 执行 PITR

假设你接到需求，要准备一个集群查询 2022/05/15 18:00:00 时间点的用户数据。此时，你可以制定 PITR 方案，恢复 2022/05/14 的快照备份和该快照到 2022/05/15 18:00:00 之间的日志备份数据，从而收集到目标数据。执行命令如下：

```shell
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://tidb-pitr-bucket/backup-data/log-backup' \
--full-backup-storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000' \
--restored-ts '2022-05-15 18:00:00+0800'

Full Restore <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.132 +08:00] [INFO] [collector.go:69] ["Full Restore success summary"] [total-ranges=12] [ranges-succeed=xxx] [ranges-failed=0] [split-region=xxx.xxxµs] [restore-ranges=xxx] [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
[2022/05/29 18:15:39.325 +08:00] [INFO] [collector.go:69] ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

## 清理过期备份数据

通过自动化运维工具（如 crontab) 每两天定期清理过期备份数据的任务。

下面是执行过期备份数据清理任务：

- 删除早于 2022/05/14 00:00:00 的快照备份

  ```shell
  rm s3://tidb-pitr-bucket/backup-data/snapshot-20220514000000
  ```

- 删除早于 2022/05/14 00:00:00 的日志备份数据

  ```shell
  tiup br log truncate --until='2022-05-14 00:00:00 +0800' --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
  ```

## 探索更多

- [备份存储](/br/backup-and-restore-storages.md)
- [快照备份与恢复命令手册](/br/br-snapshot-manual.md)
- [日志备份与 PITR 命令手册](/br/br-pitr-manual.md)
