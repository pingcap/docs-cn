---
title: BR 快速备份恢复最佳实践
category: how-to
---

# BR 快速备份恢复最佳实践

本文介绍了 PingCAP 新推出的分布式快速备份和恢复工具（下文简称 BR） 的原理和使用场景，并且总结了一些场景下的使用经验。

## 面向对象

本文面向所有 BR 的用户，并且最好对 TiDB 和 TiKV 有一定的了解。在阅读本文前推荐通过 BR 使用手册了解基本的备份恢复原理。

## 使用限制

* BR 只支持 TiDB v3.1 及以上版本。

* 目前不支持分区表的备份恢复。

* 目前只支持在全新的集群上执行恢复操作。

* BR 备份必须串行执行

## 环境准备

Tips：BR 可以直接将命令下发到 TiKV 集群来执行备份和恢复，不需要依赖 tidb-server 组件。

## 部署

* 通过官方推荐的 tidb-ansible 部署 TiDB 集群

* 通过下载 tidb-toolkit 获取 br 应用

## 版本

* TiKV: v3.1.0-beta

* PD: v3.1.0-beta

* br: v3.1.0-beta

## TiKV 集群硬件信息

| 类别   | 名称                                   |
| ---- | :----------------------------------- |
| OS   | CentOS Linux release 7.6.1810 (Core) |
| CPU  | 16 Core Common KVM processor         |
| RAM  | 32GB                                 |
| DISK | 500G SSD * 2                         |
| NIC  | 10000Mb/s                            |

## 配置

* TiKV Configurations: Default

* PD Configurations: Default

## 使用场景

使用场景分为网络盘的备份恢复和本地盘的备份恢复，推荐使用网络盘来进行操作，这样可以省去繁琐的收集备份数据文件的步骤，尤其在 TiKV 集群规模较大的情况下，使用网络盘可以大幅提升操作效率。

### 准备工作

BR backup 命令的详细使用方法请参考[文档](/v3.1/how-to/maintain/backup-and-restore/br.md#BR命令行描述)。

#### 备份准备工作

1. 运行 BR backup 命令前，查询 TiDB 集群的 GC 值并使用 MySQL 客户端将其调整为合适的值，确保备份期间不会发生 GC。

    ```
    SELECT * FROM mysql.tidb WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    UPDATE mysql.tidb SET VARIABLE_VALUE = '720h' WHERE VARIABLE_NAME = 'tikv_gc_life_time';
    ```

2. 在备份完成后，将该参数调回原来的值。

    ```
    update mysql.tidb set VARIABLE_VALUE = '10m' where VARIABLE_NAME = 'tikv_gc_life_time';
    ```

BR restore 命令的详细使用方法请参考[文档](/v3.1/how-to/maintain/backup-and-restore/br.md#BR命令行描述)。

#### 恢复准备工作

1. 运行 BR restore 前检查新集群没有同名 table。
2. （可选， only recommended for ≤3.1.0-beta）运行 BR restore 前关闭 pd leader schedulers 提升恢复性能。

   ```
   ./pd-ctl -u 172.16.5.198:2379 scheduler remove balance-leader-scheduler
   ./pd-ctl -u 172.16.5.198:2379 scheduler remove balance-hot-region-scheduler
   ./pd-ctl -u 172.16.5.198:2379 scheduler remove balance-region-scheduler
   ```

   同时在恢复数据后，要将删除的 scheduler 添加回来

   ```
   ./pd-ctl -u 172.16.5.198:2379 scheduler add balance-leader-scheduler
   ./pd-ctl -u 172.16.5.198:2379 scheduler add balance-hot-region-scheduler
   ./pd-ctl -u 172.16.5.198:2379 scheduler add balance-region-scheduler
   ```

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
bin/br backup table --db batchmark --table order_line -s local:///br_data --pd 172.16.4.217:2379 --log-file backup-nfs.log --concurrency 16
```

#### <span id="backup-status">运行指标</span>

Backup CPU Utilization  - 参与备份的 TiKV 节点（backup-worker）和 br 节点（backup-endpoint）CPU 使用率）

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

备份耗时

```
["Table backup summary: total backup ranges: 4, total success: 4, total failed: 0, total take(s): 529.53, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 667.06"]["backup total regions"=4] ["backup checksum"=48.856817ms]
```

|      | 数据                        |
| ---- | :------------------------ |
| 备份耗时 | total take(s): 529.53     |
| 数据大小 | total size(MB): 353227.18 |
| 备份吞吐 | avg speed(MB/s): 667.06   |

根据上述数据可以得到：

|             | 数据                                |
| ----------- | :-------------------------------- |
| 单 TiKV 实例吞吐 | avg speed(MB/s)/tikv_count：166.77 |

校验耗时

```
["table checksum finished"][table=`batchmark`.`order_line`] [Crc64Xor=10912722838344822475][TotalKvs=5659888624] [TotalBytes=370385538778][take=9m18.482090425s]
```

|      | 数据                   |
| ---- | :------------------- |
| 校验耗时 | take=9m18.482090425s |

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
bin/br restore table --db batchmark --table order_line -s local:///br_data --pd 172.16.5.198:2379 --log-file restore-nfs.log --concurrency 2048
```

#### <span id="restore-status">运行指标</span>

Region 分布，Region 分布越均匀，说明恢复资源利用越充分!

![img](/media/br/restore-region.png)

IO Utilization - 参与恢复的 TiKV 节点的 IO 使用率

![img](/media/br/restore-io.png)

#### 结果解读

恢复耗时

```
["Restore table summary: total restore tables: 1, total success: 1, total failed: 0, total take(s): 1253.17, total kv: 5659888624, total size(MB): 353227.18, avg speed(MB/s): 281.87"]["restore files"=14013] ["restore ranges"=9230]["split region"=5m41.332778455s] ["restore checksum"=11m13.276398441s]
```

|                  | 数据                        |
| ---------------- | :------------------------ |
| 恢复耗时             | total take(s):1253.17     |
| 数据大小             | total size(MB): 353227.18 |
| 恢复吞吐             | avg speed(MB/s):281.87    |
| region spilit 耗时 | take=5m41.332778455s      |

|           | 数据                            |
| --------- | :---------------------------- |
| 单 TiKV 吞吐 | avg speed(MB/s)/tikv_count：70 |

校验耗时

|      | 数据                    |
| ---- | :-------------------- |
| 校验耗时 | take=11m13.276398441s |

### 单表数据备份到本地磁盘

通过 BR backup 命令，将单表数据 --db batchmark --table order_line 备份到指定的本地磁盘路径下 local:///home/tidb/backup_restore_benchmark/backup-2020-01-01/

#### 前置要求

* 各个 TiKV 节点有单独的磁盘用来存放 backupSST 数据

* backup_endpoint 节点有单独的磁盘用来存放备份的 backupmeta 文件

* TiKV 和 backup_endpoint 节点需要有相同的备份目录，例如/home/tidb/backup_restore_benchmark/backup-2020-01-01/

#### 部署拓扑

![img](/media/br/backup-local-deploy.png)

#### 运行备份

备份前在 TiDB 里通过 `admin checksum table order_line` 获得备份的目标表 --db batchmark --table order_line 统计信息如下

![img](/media/br/test-data.png)

备份前，调 GC 可以参考[备份准备工作](#备份准备工作)

运行 BR backup 命令

bin/br backup table --db batchmark --table order_line -s local:///home/tidb/backup_restore_benchmark/backup-2020-01-01/ --pd 172.16.4.217:2379 --log-file backup-2020-01-01.log

#### 运行指标

指标介绍可以参考[运行指标](#backup-status)

#### 结果解读

备份耗时

```
["Table backup summary: total backup ranges: 1, total success: 1, total failed: 0, total take(s): 487.82, total kv: 1414972156, total size(MB): 138668.98, avg speed(MB/s): 284.26"]["backup total regions"=1] ["backup checksum"=25.108352ms]
```

|      | 数据                        |
| ---- | :------------------------ |
| 备份耗时 | total take(s): 487.82     |
| 数据大小 | total size(MB): 138668.98 |
| 备份吞吐 | avg speed(MB/s): 284.26   |

根据上述数据可以得到：

|             | 数据                            |
| ----------- | :---------------------------- |
| 单 TiKV 实例吞吐 | avg speed(MB/s)/tikv_count：71 |

校验耗时

```
["table checksum finished"][table=`batchmark`.`order_line`] [Crc64Xor=16518250710662763892][TotalKvs=1414972156] [TotalBytes=145404965974][take=3m27.782808253s]
```

|      | 数据                   |
| ---- | :------------------- |
| 校验耗时 | take=3m27.782808253s |

#### 性能调优

如果 TiKV 资源使用没有明显的瓶颈，比如上面[指标](#backup-status)中的 Backup CPU Utilization 400% 和 IO Utilization 60%，可以尝试调大 br backup concurrency（对大量的小表 case 无用）， 例如 `bin/br backup table --db batchmark --table order_line -s local:///home/tidb/backup_restore_benchmark/backup-2020-01-01/ --pd 172.16.5.198:2379 --log-file backup-2020-01-01.log --concurrency 16`

![img](/media/br/backup-diff.png)

|             | 数据                                       |
| ----------- | :--------------------------------------- |
| 备份耗时        | total take(s): 487.82 ->  207.73 ↓       |
| 数据大小        | total size(MB): 138668.98                |
| 备份吞吐        | avg speed(MB/s): 284.26 -> 667.55 ↑      |
| 单 TiKV 实例吞吐 | avg speed(MB/s)/tikv_count：71 -> 166.89 ↑ |

### 从本地磁盘进行备份恢复

通过 BR restore 命令，将一份完整的备份数据恢复的一个离线集群（暂不支持恢复到在线集群）。

#### 前置要求

* 确认 restore cluster 中没有与备份数据相同的库表，目前 br 不支持 table route
* restore cluster  的各个 TiKV 节点有单独的磁盘用来存放要恢复的 backupSST 数据
* restore_endpoint 节点有单独的磁盘用来存放要恢复的 backupmeta 数据
* restore cluster  的 TiKV 和 restore_endpoint 节点需要有相同的备份目录，例如 /home/tidb/backup_restore_benchmark/backup-2020-01-01/
* 如果你备份来的数据在本地磁盘，那么需要执行下面的操作
    1. 汇总所有 backupSST 文件到一个统一的目录下 all backupSST
    2. copy 汇总后的 all backupSST 到 restore cluster 的所有 TiKV 节点下
    3. copy backupmeta 到 restore endpoint 下

#### 部署拓扑

![img](/media/br/restore-local-deploy.png)

#### 运行恢复

运行 BR restore 命令

```
bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_restore_benchmark/backup-2020-01-01/ --pd 172.16.5.198:2379 --log-file restore-2020-01-01.log
```

#### 运行指标

指标介绍可以参考[运行指标](#restore-status)

#### 结果解读

恢复耗时

```
["Restore table summary: total restore tables: 1, total success: 1, total failed: 0, total take(s): 598.43, total kv: 1414972156, total size(MB): 138668.98, avg speed(MB/s): 231.72"]["restore files"=4578] ["restore ranges"=2289]["split region"=1m23.848547477s] ["restore checksum"=5m28.487069032s]
```

|                  | 数据                           |
| ---------------- | :--------------------------- |
| 恢复耗时             | total take(s): 598.43        |
| 数据大小             | total size(MB): 138668.98.18 |
| 恢复吞吐             | avg speed(MB/s): 231.72      |
| region spilit 耗时 | take=1m23.848547477s         |

|           | 数据                            |
| --------- | :---------------------------- |
| 单 TiKV 吞吐 | avg speed(MB/s)/tikv_count：58 |

校验耗时

|      | 数据                   |
| ---- | :------------------- |
| 校验耗时 | take=5m28.487069032s |

#### 性能调优

如果 TiKV 资源使用没有明显的瓶颈，可以尝试调大 Restore concurrency 参数(默认 128)， 例如 `bin/br restore table --db batchmark --table order_line -s local:///home/tidb/backup_restore_benchmark/backup-2020-01-01/ --pd 172.16.5.198:2379 --log-file restore-2020-01-01.log --concurrency 1024`

|           | 数据                                    |
| --------- | :------------------------------------ |
| 恢复耗时      | total take(s): 598.43 -> 510.08 ↓     |
| 恢复吞吐      | avg speed(MB/s): 231.72 -> 271.86 ↑   |
| 单 TiKV 吞吐 | avg speed(MB/s)/tikv_count：58 -> 68 ↑ |

### 异常处理

#### Table backup 一直进度 100%

* `v3.1.0 beta 及之前版本的 bug，已经在最新版本中修复`

#### 备份耗时太久

* `log - ["backup occur kv error"][error="{\"KvError\":{\"locked\":`
    * 目前备份必须串行执行，因为 key locked 错误现在 TiKV 处理起来确实很慢，一是没有 batch，二是 lock 有 ttl，只能等待 TiKV 处理完

#### 备份失败重来

* `log - Error: msg:"Io(Custom { kind: AlreadyExists, error: \"[5_5359_42_123_default.sst] is already exists in /dir/backup-2020-01-01/\" })"`
    * 更换备份数据目录，例如 /dir/backup-2020-01-01/ -> /dir/backup-2020-01-01.v1/
    * 删除所有 TiKV 和 br 节点的备份目录 /dir/backup-2020-01-01/
