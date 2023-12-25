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

## DDL 类别

从 v7.6.0 版本之后，为了在双向同步中尽可能地支持 DDL 同步，根据 DDL 对业务的影响，TiDB 把 [TiCDC 原本支持同步的 DDL](ticdc-ddl.md) 划分为了两种 DDL：可执行 DDL 和不可执行 DDL。

### 可执行 DDL

可执行 DDL 是在双向同步中，可以直接执行并同步到其他 TiDB 集群的 DDL。有以下 DDL：
- create database
- create table
- add column：添加的列必须是 `not null` 或者带有 `default value` 的列
- add non-unique index
- drop index
- modify column：仅能修改列的 `default value` 和 `comment`
- alter column default value
- modify table comment
- rename index
- add table partition
- drop primary key
- alter table index visibility
- alter table ttl
- alter table remove ttl
- create view
- drop view

### 不可执行 DDL

另外有些 DDL 对业务的影响较大，这类不可执行 DDL 不能在双向同步中直接通过 TiCDC 同步到其他 TiDB 集群，必须得通过特定的操作来执行。有以下 DDL：
- drop database
- drop table
- add column：添加的列为 `null` 且不带有 `default value` 的列
- drop column
- add unique index
- truncate table
- modify column：修改列除 `default value` 和 `comment` 以外的属性
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

## DDL 同步

为了能够解决上述两类 DDL 的同步问题，TiDB 引入了三种 BDR role：
- `local_only`（默认）：用户能执行任意 DDL，但是在 TiCDC 开启 `bdr_mode=true` 之后，执行的 DDL 不会被 TiCDC 同步。
- `primary`：用户能执行可执行 DDL，但不能执行不可执行 DDL，可执行 DDL 会被 TiCDC 同步到下游。
- `secondary`：用户不能执行这两种 DDL，但是会执行从 TiCDC 同步过来的 DDL。

### 可执行 DDL 的同步场景

1. 选择一个 TiDB 集群为主集群，执行 `admin set bdr role priamry`。
2. 把其他 TiDB 集群设置为从集群，执行 `admin set bdr role secondary`。
3. 在主集群上执行**可执行 DDL**，执行成功的 DDL 会被 TiCDC 同步到从集群中。

> **注意：**
>
> 为了防止用户误操作：
> - 如果有**不可执行 DDL** 在主集群中尝试执行，会报错。
> - 无论是**可执行 DDL** 还是**不可执行 DDL** 在从集群中尝试执行，都会报错。

### 不可执行 DDL 的同步场景

1. 把所有 TiDB 集群的 BDR role 设置为 `local_only`（默认 role）。执行 `admin set bdr role local_only`。
2. 暂停所有集群中需要执行 DDL 的对应的表的写入操作。
3. 等待所有集群中对应表的所有写入已经同步到其他集群后，手动在每一个 TiDB 集群上单独执行所有的 DDL。
4. 等待 DDL 完成之后，重新恢复写入。
5. 按照[可执行 DDL 的同步场景](###可执行-DDL-的同步场景)的步骤切换回可执行 DDL 的同步场景。

## 停止双向复制

在业务数据停止写入之后，你可以在两个集群中都插入一行特殊的值，通过检查这两行特殊的值来确保数据达到了一致的状态。

检查完毕之后，停止同步任务，并把 BDR role 切换回 `local_only` （默认）即可停止双向复制。

## 使用限制

- BDR role 只能在两种场景中正常使用——1 个 `primary` 集群 + n 个 `secondary` 集群（可执行 DDL 的同步场景）和 n 个 `local_only` 集群（不可执行 DDL 的同步场景）。**请勿将 BDR role 设置为其他情况，例如，`primary+secondary+local_only`，TiDB 无法在错误设置 BDR role 的情况下保证正确性。**

- 禁止在同步的表中使用 `Auto increment`/`Auto random` 键。

- 双向复制的集群不具备检测写冲突的功能，写冲突将会导致未定义问题。你需要在业务层面保证不出现写冲突。

- TiCDC 双向复制功能支持超过 2 个集群的双向同步，但是不支持多个集群级联模式的同步，即 TiDB A -> TiDB B ->  TiDB C -> TiDB A 的环形复制方式。在这种部署方式下，如果其中一个链路出现问题则会影响整个数据同步链路。因此，如果需要部署多个集群之间的双向复制，每个集群都需要与其他集群两两相连，即 `TiDB A <-> TiDB B`，`TiDB B <-> TiDB C`，`TiDB C <-> TiDB A`。
