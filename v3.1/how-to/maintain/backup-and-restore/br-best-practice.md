---
title: BR 快速备份恢复最佳实践
category: how-to
---

# BR 快速备份恢复最佳实践

[Backup & Restore](/v3.1/how-to/maintain/backup-and-restore/br.md)（下文简称 BR）是 PingCAP 新推出的分布式快速备份和恢复工具。本文描述了 BR 在备份和恢复场景下的操作过程，以及操作过程中的注意事项供用户参考，以达到 BR 的最佳实践。

## 目标读者

本文为 BR 用户提供操作参考，因此读者需要对 TiDB 和 TiKV 有一定的了解。在阅读本文前，推荐先阅读 [使用 BR 进行备份与恢复](/v3.1/how-to/maintain/backup-and-restore/br.md)。

## 目标

* 使用网络盘或本地盘进行备份/恢复

* 通过备份/恢复相关指标了解备份/恢复状态

* 了解进行备份/恢复时如何调优性能

* 处理备份时可能发生的异常

## 使用限制

* BR 只支持 TiDB v3.1 及以上版本

* 目前只支持在全新的集群上执行恢复操作

* BR 备份必须串行执行

## 环境准备

Tips：BR 可以直接将命令下发到 TiKV 集群来执行备份和恢复，不需要依赖 tidb-server 组件。

### 部署

* 通过官方推荐的 [tidb-ansible](/v3.1/how-to/deploy/orchestrated/ansible.md) 部署 TiDB 集群

* 通过下载 [tidb-toolkit](/v3.1/reference/tools/download.md#快速备份和恢复br) 获取 br 应用

### 版本

* TiKV: v3.1.0-beta.1

* PD: v3.1.0-beta.1

* br: v3.1.0-beta.1

### TiKV 集群硬件信息

| 类别   | 名称                                   |
| ---- | :----------------------------------- |
| OS   | CentOS Linux release 7.6.1810 (Core) |
| CPU  | 16 Core Common KVM processor         |
| RAM  | 32GB                                 |
| DISK | 500G SSD * 2                         |
| NIC  | 10000Mb/s                            |

### 配置

* TiKV Configurations: Default

* PD Configurations: Default

## 准备工作

### 备份准备工作

BR backup 命令的详细使用方法请参考[文档](/v3.1/how-to/maintain/backup-and-restore/br.md#br-命令行描述)。

1. 运行 BR backup 命令前，查询 TiDB 集群的 GC 值并使用 MySQL 客户端将其调整为合适的值，确保备份期间不会发生 GC。

    ```
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. 在备份完成后，将该参数调回原来的值。

    ```
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

### 恢复准备工作

BR restore 命令的详细使用方法请参考[文档](/v3.1/how-to/maintain/backup-and-restore/br.md#br-命令行描述)。

1. 运行 BR restore 前检查新集群没有同名 table。

## 使用场景

使用场景分为网络盘的备份恢复和本地盘的备份恢复，推荐使用网络盘来进行操作，这样可以省去繁琐的收集备份数据文件的步骤，尤其在 TiKV 集群规模较大的情况下，使用网络盘可以大幅提升操作效率。

### 单表数据备份到网络盘（推荐）

通过 BR backup 命令，将单表数据 --db batchmark --table order_line 备份到指定的网络盘路径下 local:///br_data

#### 前置要求

* 配置一台高性能 SSD 硬盘主机作为 nfs server 存储数据，其他所有 BR 节点和 TiKV 节点作为 nfs client 挂载相同路径(如 /br_data)到 nfs server 上。

* nfs server 和 nfs client 的传输速率至少要达到备份集群的 TiKV 实例数 * 150MB/s。否则网络 IO 有可能成为性能瓶颈。

#### 部署拓扑

![img](/media/br/backup-nfs-deploy.png)

#### 运行备份

备份前在 TiDB 里通过 `admin checksum table order_line` 获得备份的目标表 --db batchmark --table order_line 统计信息如下

![img](/media/br/total-data.png)

备份前，调 GC 可以参考[备份准备工作](#备份准备工作)

运行 BR backup 命令

```
bin/br backup table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file backup-nfs.log
```

#### <span id="backup-status">运行指标</span>

Backup CPU Utilization  - 参与备份的 TiKV 节点（backup-worker）和（backup-endpoint）CPU 使用率

![img](/media/br/backup-cpu.png)

IO Utilization - 参与备份的 TiKV 节点的 IO 使用率

![img](/media/br/backup-io.png)

BackupSST Generation Throughput - 参与备份的 TiKV 节点生成 backupSST 文件的吞吐（正常时单台 TiKV 吞吐在 150MB/s 左右）

![img](/media/br/backup-throughput.png)

One Backup Range Duration - 备份一个 range 操作耗时，分为 scan 耗时（scan KV）和 save 耗时（保存成 backupSST）

 ![img](/media/br/backup-range-duration.png)

One Backup Subtask Duration - 一次备份会拆分成多个子任务运行，监控显示了子任务的耗时，虽然是备份单表，但因为表中有3个索引，所以正常会划分成4个子任务，图中有13个点，说明有9次（13-4）重试，备份过程可能产生 region 调度行为，少量重试是正常的。

![img](/media/br/backup-subtask-duration.png)

Backup Errors - 备份过程中的错误（正常时无错误，如果出现少量错误也不要担心，Backup 有重试机制，可能会导致备份时间增加，但不会影响正确性）

![img](/media/br/backup-errors.png)

Checksum Request duration - 对备份集群执行 admin checksum 的耗时统计

![img](/media/br/checksum-duration.png)

#### 结果解读

从日志中可以获取此次备份的相关统计信息，在日志中搜关键字 "summary"，可以看到下述信息：

```
["Table backup summary: total backup ranges: 4, total success: 4, total failed: 0, total take(s): 986.43, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 358.09"] ["backup total regions"=7196] ["backup checksum"=6m28.291772955s] ["backup fast checksum"=24.950298ms]
```

|      | 数据                        |
| ---- | :------------------------ |
| 备份耗时 | total take(s): 986.43     |
| 数据大小 | total size(MB): 353227.18 |
| 备份吞吐 | avg speed(MB/s): 358.09   |
| 校验耗时 | take=6m28.29s   |

根据上述数据可以得到：

|             | 数据                                |
| ----------- | :-------------------------------- |
| 单 TiKV 实例吞吐 | avg speed(MB/s)/tikv_count：89 |

#### 性能调优

如果 TiKV 资源使用没有明显的瓶颈，比如上面[指标](#backup-status)中的 Backup CPU Utilization 1500% 和 IO Utilization 30%，可以尝试调大 br backup concurrency（对大量的小表 case 无用）, 例如 bin/br backup table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file backup-nfs.log --concurrency 16

![img](/media/br/backup-diff.png)

![img](/media/br/backup-diff2.png)

|             | 数据                                      |
| ----------- | :--------------------------------------- |
| 备份耗时        | total take(s): 986.43 -> 535.53 ↓     |
| 数据大小        | total size(MB): 353227.18             |
| 备份吞吐        | avg speed(MB/s): 358.09 -> 659.59 ↑    |
| 单 TiKV 实例吞吐 | avg speed(MB/s)/tikv_count：89 -> 164.89 ↑ |

### 从网络盘进行备份恢复

通过 BR restore 命令，将一份完整的备份数据恢复的一个离线集群（暂不支持恢复到在线集群）。

#### 前置要求

* 无

#### 部署拓扑

![img](/media/br/restore-nfs-deploy.png)

#### 运行恢复

恢复前，可以参考[恢复准备工作](#恢复准备工作)

运行 BR restore 命令

```
bin/br restore table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file restore-nfs.log
```

#### <span id="restore-status">运行指标</span>

CPU - 参与恢复的 TiKV 节点 CPU 使用率

![img](/media/br/restore-cpu.png)

IO Utilization - 参与恢复的 TiKV 节点的 IO 使用率

![img](/media/br/restore-io.png)

Region 分布 - Region 分布越均匀，说明恢复资源利用越充分!

![img](/media/br/restore-region.png)

Process SST Duration - 处理 SST 文件的延迟，对于一张表来说，在恢复时，tableID 如果发生了变化，需要进行 rewrite，否则会进行 rename, 通常 rewrite 延迟要高于 rename

![img](/media/br/restore-process-sst.png)

DownLoad SST Throughput - 从 External Storage 下载 SST 文件的吞吐

![img](/media/br/restore-download-sst.png)

Restore Errors - 恢复过程中的错误

![img](/media/br/restore-errors.png)

Checksum Request duration - 对备份集群执行 admin checksum 的耗时统计（此时 checksum 会进行 undo rewrite，会比备份时 checksum  延迟高)

![img](/media/br/restore-checksum.png)

#### 结果解读

从日志中可以获取此次恢复的相关统计信息，在日志中搜关键字 "summary"，可以看到下述信息：

```
["Table Restore summary: total restore tables: 1, total success: 1, total failed: 0, total take(s): 961.37, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 367.42"] ["restore files"=9263] ["restore ranges"=6888] ["split region"=49.049182743s] ["restore checksum"=6m34.879439498s]
```

|                  | 数据                        |
| ---------------- | :------------------------ |
| 恢复耗时             | total take(s):961.37 |
| 数据大小             | total size(MB): 353227.18 |
| 恢复吞吐             | avg speed(MB/s): 367.42 |
| region spilit 耗时 | take=49.049182743s |
| 校验耗时 | take=6m34.879439498s |

根据上述数据可以得到：

|           | 数据                            |
| --------- | :---------------------------- |
| 单 TiKV 吞吐 | avg speed(MB/s)/tikv_count：91.8 |
| 单 TiKV 平均恢复速度 | total size(MB)/(split time + restore time)/tikv_count：87.4 |

#### 性能调优

如果 TiKV 资源使用没有明显的瓶颈，可以尝试调大 Restore concurrency 参数(默认 128)， 例如 `bin/br restore table --db batchmark --table order_line -s local:///br_data/ --pd 172.16.5.198:2379 --log-file restore-concurrency.log --concurrency 1024`

|           | 数据                                    |
| --------- | :------------------------------------ |
| 恢复耗时      | total take(s): 961.37 -> 443.49 ↓     |
| 恢复吞吐      | avg speed(MB/s): 367.42 -> 796.47 ↑   |
| 单 TiKV 吞吐 | avg speed(MB/s)/tikv_count：91.8 -> 199.1 ↑ |
| 单 TiKV 平均恢复速度 | total size(MB)/(split time + restore time)/tikv_count：87.4 -> 162.3 ↑ |

### 单表数据备份到本地磁盘

通过 BR backup 命令，将单表数据 --db batchmark --table order_line 备份到指定的本地磁盘路径下 `local:///home/tidb/backup_local`

#### 前置要求

* 各个 TiKV 节点有单独的磁盘用来存放 backupSST 数据

* backup_endpoint 节点有单独的磁盘用来存放备份的 backupmeta 文件

* TiKV 和 backup_endpoint 节点需要有相同的备份目录，例如/home/tidb/backup_local

#### 部署拓扑

![img](/media/br/backup-local-deploy.png)

#### 运行备份

备份前在 TiDB 里通过 `admin checksum table order_line` 获得备份的目标表 --db batchmark --table order_line 统计信息如下

![img](/media/br/total-data.png)

备份前，调 GC 可以参考[备份准备工作](#备份准备工作)

运行 BR backup 命令

```
bin/br backup table --db batchmark --table order_line -s local:///home/tidb/backup_local/ --pd 172.16.5.198:2379 --log-file backup_local.log
```

#### 运行指标

指标介绍可以参考[运行指标](#backup-status)

#### 结果解读

备份耗时

```
["Table backup summary: total backup ranges: 4, total success: 4, total failed: 0, total take(s): 551.31, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 640.71"] ["backup total regions"=6795] ["backup checksum"=6m33.962719217s] ["backup fast checksum"=22.995552ms]
```

|      | 数据                        |
| ---- | :------------------------ |
| 备份耗时 | total take(s): 551.31     |
| 数据大小 | total size(MB): 353227.18 |
| 备份吞吐 | avg speed(MB/s): 640.71   |
| 校验耗时 | take=6m33.962719217s |

根据上述数据可以得到：

|             | 数据                            |
| ----------- | :---------------------------- |
| 单 TiKV 实例吞吐 | avg speed(MB/s)/tikv_count：160 |

### 从本地磁盘进行备份恢复

通过 BR restore 命令，将一份完整的备份数据恢复的一个离线集群（暂不支持恢复到在线集群）。

#### 前置要求

* 确认 restore cluster 中没有与备份数据相同的库表，目前 br 不支持 table route
* restore cluster  的各个 TiKV 节点有单独的磁盘用来存放要恢复的 backupSST 数据
* restore_endpoint 节点有单独的磁盘用来存放要恢复的 backupmeta 数据
* restore cluster  的 TiKV 和 restore_endpoint 节点需要有相同的备份目录，例如 /home/tidb/backup_local/
* 如果你备份来的数据在本地磁盘，那么需要执行下面的操作
    1. 汇总所有 backupSST 文件到一个统一的目录下 all backupSST
    2. copy 汇总后的 all backupSST 到 restore cluster 的所有 TiKV 节点下
    3. copy backupmeta 到 restore endpoint 下

#### 部署拓扑

![img](/media/br/restore-local-deploy.png)

#### 运行恢复

运行 BR restore 命令

```
bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_local/ --pd 172.16.5.198:2379 --log-file restore_local.log
```

#### 运行指标

指标介绍可以参考[运行指标](#restore-status)

#### 结果解读

恢复耗时

```
["Table Restore summary: total restore tables: 1, total success: 1, total failed: 0, total take(s): 908.42, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 388.84"] ["restore files"=9263] ["restore ranges"=6888] ["split region"=58.7885518s] ["restore checksum"=6m19.349067937s]
```

|                  | 数据                           |
| ---------------- | :--------------------------- |
| 恢复耗时             | total take(s): 908.42 |
| 数据大小             | total size(MB): 353227.18 |
| 恢复吞吐             | avg speed(MB/s):  388.84     |
| region spilit 耗时 | take=58.7885518s         |
| 校验耗时 | take=6m19.349067937s |

|           | 数据                            |
| --------- | :---------------------------- |
| 单 TiKV 吞吐 | avg speed(MB/s)/tikv_count：97.2 |
| 单 TiKV 平均恢复速度 | total size(MB)/(split time + restore time)/tikv_count：92.4 |

### 异常处理

#### 备份日志中出现 key locked Error

* `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`
    * 目前备份中遇到 lock 会重试尝试清锁，少量报错不会影响正确性

#### 备份失败重来

* `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup_local/\" })"`
    * 更换备份数据目录, 例如 /dir/backup-2020-01-01/ -> /dir/backup_local.v1/
    * 删除所有 TiKV 和 br 节点的备份目录 /dir/backup_local/
