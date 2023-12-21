---
title: TiCDC 双向复制
summary: 了解 TiCDC 双向复制的使用方法。
---

# TiCDC 双向复制

从 v6.5.0 版本开始，TiCDC 支持在两个 TiDB 集群之间进行双向复制。基于该功能，你可以使用 TiCDC 来构建 TiDB 集群的多写多活解决方案。

本文档以在两个 TiDB 集群之间进行双向复制为例，介绍双向复制的使用方法。

## 部署双向复制

TiCDC 复制功能只会将指定时间点之后的增量变更复制到下游集群。开始双向复制之前，需要采取以下步骤：

1. （可选）根据实际需要，使用数据导出工具 [Dumpling](/dumpling-overview.md) 和导入工具 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 将两个集群的数据导入到对方集群。

2. 在这两个 TiDB 集群之间部署两套 TiCDC 集群，集群的拓扑如下图所示，图中箭头所指的方向即为该 TiCDC 集群同步数据的流向。

    ![TiCDC bidirectional replication](/media/ticdc/ticdc-bidirectional-replication.png)

3. 指定上下游集群的数据同步的开始时间点。

    1. 确认上下游集群的时间点。如果进行双集群容灾，那么建议确保两个集群在某个对应的时刻的数据是一致的，例如 TiDB A 在 `ts=1` 时刻与 TiDB B 在 `ts=2` 的时刻数据是一致的。

    2. 在创建同步任务时，分别把对应集群的同步任务的 `--start-ts` 参数指定为对应的 `tso`，即上游为 TiDB A 的同步任务需设置参数 `--start-ts=1`，上游为 TiDB B 的同步任务需设置参数 `--start-ts=2`。

4. 在创建同步任务的 `--config` 参数所指定的配置文件中，添加如下配置:

    ```toml
    # 是否启用 bdr 模式
    bdr-mode = true
    ```

这样，以上搭建好的集群即可对数据进行双向复制。

## DDL 同步

从 v7.6.0 版本之后，TiDB 为了支持双向同步 DDL，引入了四种 BDR role（None、Primary、Secondary 和 Local_only）和两种 BDR 模式。

### BDR 严格模式

把一个 TiDB 集群设置为 Primary，其他 TiDB 集群设置为 Secondary 就可以进入 BDR 严格模式。在这种模式下
1. 用户可以在 primary TiDB 下执行无损 DDL，并通过 TiCDC 同步到 Secondary 集群。无损 DDL 如下：
- create database
- create table
- add column(not null or default value)
- add non-unique index
- drop index
- modify column(can modify default value and comment)
- alter column default value
- modify table comment
- rename index
- add table partition
- drop primary key
- alter table index visibility
- alter table ttl
- alter table remove ttl
2. 其他有损 DDL 在 primary TiDB 上执行会被拦截。有损 DDL 如下：
- drop database
- drop table
- add column 非（not null or default value）
- drop column
- add unique index
- truncate table
- modify column 非（can modify default value and comment）
- rename table
- drop partition
- truncate partition
- alter table character set
- alter database character set
- recover table
- add primary key
- rebase auto id
- exchange partition
- reorganize partition
3. 无论是有损 DDL 还是无损 DDL 都无法在 Secondary TiDB 中执行。在 TiCDC zhi

都可以执行的 DDL
create view
drop view

### BDR 非严格模式

如果需要执行有损 DDL，则需要把所有 TiDB 集群的 BDR role 设置为 local_only，进入 BDR 非严格模式，并且遵循以下步骤：

1. 暂停所有集群中需要执行 DDL 的对应的表的写入操作。
2. 等待所有集群中对应表的所有写入已经同步到其他集群后，手动在每一个 TiDB 集群上单独执行所有的 DDL。
3. 等待 DDL 完成之后，重新恢复写入。
4. 把所有集群切换成 BDR 严格模式。

## 停止双向复制

在业务数据停止写入之后，你可以在两个集群中都插入一行特殊的值，通过检查这两行特殊的值来确保数据达到了一致的状态。

检查完毕之后，停止同步任务即可停止双向复制。

## 使用限制

- DDL 的限制见[DDL 同步 小节](#ddl-同步)。

- 禁止在同步的表中使用 Auto increment/Auto random 键。

- 双向复制的集群不具备检测写冲突的功能，写冲突将会导致未定义问题。你需要在业务层面保证不出现写冲突。

- TiCDC 双向复制功能支持超过 2 个集群的双向同步，但是不支持多个集群级联模式的同步，即 TiDB A -> TiDB B ->  TiDB C -> TiDB A 的环形复制方式。在这种部署方式下，如果其中一个链路出现问题则会影响整个数据同步链路。因此，如果需要部署多个集群之间的双向复制，每个集群都需要与其他集群两两相连，即 `TiDB A <-> TiDB B`，`TiDB B <-> TiDB C`，`TiDB C <-> TiDB A`。
