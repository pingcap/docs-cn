---
title: PiTR 功能介绍 
summary: 了解 PiTR 使用。
---

> **警告：**
>
> 当前该功能为实验特性，不建议在生产环境中使用。打开该功能需要配置参数 tikv:  log-backup.enable: true 开启该功能。

# 使用 PiTR 

本教程介绍如何部署和使用 PiTR，帮助不熟悉 PiTR 的用户顺利上手该功能。在介绍具体操作前，我们设想一个用户场景，来加深对以下的操作的理解：用户 A 在 AWS 部署一套 TiDB 的生产集群供业务使用，业务团队提出了两个需求

1. 用户数据变更需要及时地备份下来，在数据库遭遇异常情况的时候能够以最小的用户数据丢失代价（容忍异常前几分钟内的用户数据丢失）快速地恢复业务；
2. 每个月不定期进行业务审计。要求 A  接收到审计请求后，提供一个数据库来查询审计要求的一个月内某个时间点的数据 

用户 A 通过 TiDB 提供的 PiTR 功能，满足了业务团队的需求。

## 部署 TiDB 集群和 BR

使用 PiTR 功能，需要部署 v6.2.0 及以上版本的 TiDB 集群，并且更新 BR 到与部署 TiDB 集群相同的版本， 该教程假设使用 v6.2.0 版本。

TiDB 集群拓扑和配置：

|**组件** | **CPU** | **内存** |**硬盘类型** | **AWS 机型** | **实例数量** | **实例数量** |
| --- | --- | --- | --- | --- | --- | --- |
| TiDB | 16 核+ | 32 GB+ | SAS | c5.2xlarge | 2 | 172.16.102.94:4000 |
| PD | 4核+ | 8 GB+ | SSD | c5.2xlarge | 3 | 172.16.102.95:2379 |
| TiKV | 16 核+ | 32 GB+ | SSD | m5.2xlarge | 3 | - |
| BR | 8 核+ | 16 GB+ | SAS | c5.2xlarge |  2 | 172.16.102.93:3000 |
| 监控 | 8 核+ | 16 GB+ | SAS | c5.2xlarge | 1 | - |

注意：

- BR 执行备份恢复功能需要访问 PD/TiKV，请确保 BR 与所有 PD/TiKV 的联通性；
- BR 与 PD 所在服务器时区需要相同。

使用 TiUP 部署或升级 TiDB 集群

- 没有部署 TiDB 集群，请参考 [部署 TiDB 集群](/production-deployment-using-tiup.md)
- 已经部署老版本 TiDB 集群，请先升级 TiDB 集群 [升级 TiDB 集群](/upgrade-tidb-using-tiup.md)
- 在 v6.1.0 版本 TiDB 集群开启 PiTR 实验特性，请在 TiUP 集群拓扑文件中配置

  ```shell
  server_configs:
  tikv:
    log-backup.enable: true
  ```

使用 TiUP 安装或升级 BR  

- 没有安装 BR， 使用命令 `tiup install br:v6.1.0` 
- 升级 BR，使用命令 `tiup update br:v6.1.0` 

## 配置备份存储（S3）

在开始备份任务之前需要准备好备份存储，在该场景中包含 

1. 准备用于存放备份数据的 s3 bucket 和目录；
2. 配置访问 s3 中备份目录的权限；
3. 规划备份数据保存的目录结构。

首先在 S3 创建用于保存备份数据的目录 `s3://tidb-pitr-bucket/backup-data`

1. 创建 bucket。你也可以选择已有的 S3 bucket 来保存备份数据。如果没有可用的 bucket，可以参照 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-bucket.html) 创建一个 S3  Bucket。本教程使用的 bucket 名为 `tidb-pitr-bucket`。 
2. 创建备份数据总目录，在 bucket `tidb-pitr-bucket` 下创建目录 `backup-data`, 参考 [AWS 官方文档](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/user-guide/create-folder.html)

配置 BR  和 TiKV  访问 S3 中的备份目录的权限。本教程推荐使用最安全的 IAM 访问方式，配置过程可以参考[控制存储桶访问](https://docs.aws.amazon.com/zh_cn/AmazonS3/latest/userguide/walkthrough1.html)。权限要求如下：

- 备份集群的  TiKV 和 BR 需要  `s3://tidb-pitr-bucket/backup-data` 的： `s3:ListBucket`、`s3:PutObject` 和 `s3:AbortMultipartUpload`
- 恢复集群的  TiKV 和 BR 需要  `s3://tidb-pitr-bucket/backup-data` 的最小权限： `s3:ListBucket` 和 `s3:GetObject`

规划备份数据保存的目录结构，安排快照（全量）备份和日志备份的目录

- 每个快照备份保存在 `s3://tidb-pitr-bucket/backup-data/snapshot-${date}` 目录下，date 为快照备份开始的时间点，如在 2022/05/12 00:01:30 开始的快照备份  `s3://tidb-pitr-bucket/backup-data/snapshot-20220512000130`
- 日志备份保存在 `s3://tidb-pitr-bucket/backup-data/log-backup/` 目录下

## 确定备份策略

为了满足业务最小数据丢失、快速恢复、一个月内任意时间点审计需求，用户 A 制定了如下的备份策略

- 运行日志备份，持续不断备份数据库数据变更；
- 每隔两天在零点左右进行一次快照备份；
- 保存 30 天内的快照备份和日志备份数据，清理超过 30 天的备份数据；

## 启动日志备份

首先启动日志备份任务，日志备份进程会在 TiKV 集群运行，持续不断将数据库变更数据备份到 S3 中。 日志备份任务启动命令：

```shell
tiup br log start --task-name=pitr --pd=172.16.102.95:2379 --storage='s3://tidb-pitr-bucket/backup-data/log-backup'
```

启动日志备份任务后查询日志备份任务状态

```shell
tiup br log status --task-name=pitr --pd=172.16.102.95:2379 

● Total 1 Tasks.
> #1 <
    name: pitr
    status: ● NORMAL
    start: 2022-05-14 11:09:40.7 +0800 CST
    end: 2035-01-01 00:00:00 +0800 CST
    storage: s3://tidb-pitr-bucket/backup-data/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-04-24 11:31:47.2 +0800 CST; gap=4m53s
checkpoint[store=1]: 2022-04-24 11:31:47.2 +0800 CST; gap=4m53s
error[store=1]: KV:logbackup:NoSuchTask
checkpoint[store=4]: 2022-04-24 11:31:47.25 +0800 CST; gap=4m53s
checkpoint[store=5]: 2022-04-24 11:31:47.351 +0800 CST; gap=4m53s
```

## 执行快照备份

通过自动化运维工具（如 crontab）设置定期的快照备份任务，例如：每隔两天在零点左右行一次快照（全量）备份。 下面是两次备份的示例

在 2022/05/12 00:00:00 执行一次快照备份

```shell
tiup br backup full --pd=172.16.102.95:2379 --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220512000000' --backupts='2022/05/12 00:00:00'
```

在 2022/05/14 00:00:00 执行一次快照备份

```shell
tiup br backup full --pd=172.16.102.95:2379 --storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220512000000'
--backupts='2022/05/14 00:00:00'
```

## 清理过期备份数据

通过自动化运维工具（如 crontab)  每两天定期清理过期备份数据的任务。

下面是在 2022/05/14 执行的过期备份数据清理任务：

- 删除早于 2022/04/14 00:00:00 的快照备份  

  ```shell
  rm s3://tidb-pitr-bucket/backup-data/snapshot-20220414000000
  ```

- 删除早于 2022/04/14 00:00:00  的日志备份数据

  ```shell
  tiup br log truncate --until='2022/04/14 06:00:00'
  ```

## 执行 PiTR

用户 A 接到需求，准备一个集群查询 2022/04/13 18:00:00 时间点的用户数据。用户 A 通过查看备份存储中的备份数据后，制定了 PiTR 方案。通过恢复 2022/04/12 的快照备份和该快照到 2022/04/13 18:00:00 之间的日志备份数据就可以实现需要，用户 A 执行命令如下：

```shell
tiup br restore point -pd=172.16.102.95:2379
--storage='s3://tidb-pitr-bucket/backup-data/log-backup'
--full-backup-storage='s3://tidb-pitr-bucket/backup-data/snapshot-20220512000000' 

Full Restore <---------------------------------------------------------------------> 100.00%
Restore DDL files <----------------------------------------------------------------> 100.00%
Restore DML Files <----------------------------------------------------------------> 100.00%
Restore DDL files <----------------------------------------------------------------> 100.00%
```

## 备份任务失败

### 任务失败
在创建日志备份任务后，日志备份任务在遇到一些故障场景下（如将备份日志下刷到外部存储失败等）会做重试操作，当重试超过一定次数就会将备份任务的状态从 `NORMAL` 置为 `ERROR` 状态，通过命令 `br log status --PD {IP}:{PORT}` 可以查询到任务状态和任务失败的原因。

### 恢复任务
当任务状态变为 `ERROR` 后，用户需要根据提示确认故障原因并主动恢复故障环境。之后通过 `br log resume --task-name {TASK-NAME} --PD {IP}:{PORT}` 来恢复任务，备份任务将续接上一次的备份时间点继续备份数据。

> **注意：**
>
> 由于此功能会备份集群的多版本数据，当任务发生错误且状态变更为 `ERROR` 后，同时会将当前任务的备份进度点的数据设为一个 `safe point`，`safe point` 的数据将保证 24 小时不被 GC 
> 掉。所以，当任务恢复之后，会持续从上一个备份点继续备份日志。如果任务失败时间超过 24 小时，前一次备份进度点的数据已经被 GC，此时恢复任务操作会提示失败。这种场景下只能 stop 掉本次
> 的任务，并重新开启新的备份任务。


