---
title: 压缩日志备份
summary: 了解如何通过压缩日志备份为 SST 格式来提升按时间点恢复 (Point-in-time recovery, PITR) 的效率。
---

# 压缩日志备份

本文介绍如何通过压缩日志备份 (Compact Log Backup) 为 [SST](/glossary.md#static-sorted-table--sorted-string-table-sst) 格式来提升按时间点恢复 (Point-in-time recovery, [PITR](/glossary.md#point-in-time-recovery-pitr)) 的效率。

## 功能概述

传统日志备份以一种高度非结构化的方式存储写入操作，可能导致以下问题：

- 恢复性能下降：无序数据需通过 Raft 协议逐条写入集群。
- 写放大：所有写入必须从 LSM Tree 的 L0 开始被逐级别 compact 到底层。
- 全量备份依赖：需频繁执行全量备份以控制恢复数据量，对业务有一定影响。

从 v8.5.5 开始，压缩日志备份功能提供了离线压缩能力，可将日志备份的非结构化数据转换为结构化的 SST 文件，从而实现以下改进：

- SST 可以被快速导入集群，从而提升恢复性能。
- 压缩过程中消除重复记录，从而减少空间消耗。
- 在确保 RTO (Recovery Time Objective) 的前提下允许用户设置更长的全量备份间隔，从而降低对业务的影响。

## 使用限制

- 压缩日志备份并不是全量备份的替代方案，需与定期全量备份配合使用。为了保证能进行 PITR，日志备份的压缩过程会保留所有 MVCC 版本，长期不进行全量备份将导致存储膨胀并且可能在未来恢复时遇到问题。
- 目前不支持压缩启用了 Local Encryption 的备份。

## 使用方法

目前仅支持手动压缩日志备份，流程较为复杂。**建议在生产中使用后续发布的 TiDB Operator 方案来压缩日志备份**。

### 手动压缩

本节介绍手动压缩日志备份的操作步骤。

#### 前提条件

手动压缩日志备份需要两个工具：`tikv-ctl` 和 `br`。

#### 第 1 步：将存储编码为 Base64

执行以下编码命令：

```shell
br operator base64ify --storage "s3://your/log/backup/storage/here" --load-creds
```

> **注意：**
>
> - 如果执行以上命令时带了 `--load-cerds` 这个选项，编码出来的 Base64 中会包含从 BR 当前环境中加载的密钥信息，请注意安全保护和权限管控。
> - 此处的 `--storage` 值应该和日志备份任务的 `log status` 命令输出的 storage 相同。

#### 第 2 步：执行日志压缩

有了存储的 Base64 之后，你可以执行以下命令通过 `tikv-ctl` 发起压缩，注意 `tikv-ctl` 默认日志等级为 `warning`，启用 `--log-level info` 来获得更多信息：

```shell
tikv-ctl --log-level info compact-log-backup \
    --from "<start-tso>" --until "<end-tso>" \
    -s 'bAsE64==' -N 8
```

参数解释如下：

- `-s`：已获得的存储的 Base64。
- `-N`：最大并发压缩日志任务的数量。
- `--from`：压缩开始的时间戳。
- `--until`：压缩结束的时间戳。

`--from` 和 `--until` 这对参数指定了压缩操作的时间范围。压缩操作将处理所有包含指定时间范围内任意写入的日志文件，因此最终生成的 SST 文件可能包含该范围外的写入数据。

要获取某个特定时间点的时间戳，请执行以下命令：

```shell
echo $(( $(date --date '2004-05-06 15:02:01Z' +%s%3N) << 18 ))
```

> **注意：**
>
> 如果你是 macOS 用户，需要先使用 Homebrew 安装 `coreutils`，并且使用 `gdate` 而非 `date`。
>
> ```shell
> echo $(( $(gdate --date '2004-05-06 15:02:01Z' +%s%3N) << 18 ))
> ```
