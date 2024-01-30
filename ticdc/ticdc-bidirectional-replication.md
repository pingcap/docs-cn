---
title: TiCDC 双向复制
summary: 了解 TiCDC 双向复制的使用方法。
---

# TiCDC 双向复制

TiCDC 支持在两个 TiDB 集群之间进行双向复制 (Bidirectional replication, BDR)。基于该功能，你可以使用 TiCDC 来构建 TiDB 集群的多写多活解决方案。

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

从 v7.6.0 开始，为了在双向复制中尽可能地支持 DDL 同步，根据 DDL 对业务的影响，TiDB 将 [TiCDC 原本支持同步的 DDL](/ticdc/ticdc-ddl.md) 划分为两种 DDL：可复制的 DDL 和不可复制的 DDL。

### 可复制的 DDL

可复制的 DDL 是指在双向复制中，可以直接执行并同步到其他 TiDB 集群的 DDL。

可复制的 DDL 包括：

- `CREATE DATABASE`
- `CREATE TABLE`
- `ADD COLUMN`：添加的列必须可以为 `null`，或者是同时带有 `not null` 和 `default value`
- `ADD NON-UNIQUE INDEX`
- `DROP INDEX`
- `MODIFY COLUMN`：仅能修改列的 `default value` 和 `comment`
- `ALTER COLUMN DEFAULT VALUE`
- `MODIFY TABLE COMMENT`
- `RENAME INDEX`
- `ADD TABLE PARTITION`
- `DROP PRIMARY KEY`
- `ALTER TABLE INDEX VISIBILITY`
- `ALTER TABLE TTL`
- `ALTER TABLE REMOVE TTL`
- `CREATE VIEW`
- `DROP VIEW`

### 不可复制的 DDL

不可复制的 DDL 是指对业务影响较大、可能会造成集群间数据不一致性的 DDL，这类 DDL 不能在双向复制中直接通过 TiCDC 同步到其他 TiDB 集群的 DDL。不可复制的 DDL 必须通过特定的操作来执行。

不可复制的 DDL 包括：

- `DROP DATABASE`
- `DROP TABLE`
- `ADD COLUMN`：添加的列为 `not null` 且不带有 `default value`
- `DROP COLUMN`
- `ADD UNIQUE INDEX`
- `TRUNCATE TABLE`
- `MODIFY COLUMN`：修改列除 `default value` 和 `comment` 以外的属性
- `RENAME TABLE`
- `DROP PARTITION`
- `TRUNCATE PARTITION`
- `ALTER TABLE CHARACTER SET`
- `ALTER DATABASE CHARACTER SET`
- `RECOVER TABLE`
- `ADD PRIMARY KEY`
- `REBASE AUTO ID`
- `EXCHANGE PARTITION`
- `REORGANIZE PARTITION`

## DDL 同步

为了能够解决上述可复制的 DDL 和不可复制的 DDL 两类 DDL 的同步问题，TiDB 引入了两种 BDR role：

- `PRIMARY`：你可以执行可复制的 DDL，但不能执行不可复制的 DDL，可复制的 DDL 会被 TiCDC 同步到下游。
- `SECONDARY`：你不能执行可复制的 DDL，也不能执行不可复制的 DDL，但是可以执行从 TiCDC 同步过来的 DDL。

在不设置 BDR role 时，你可以执行任意 DDL。但是在 TiCDC 开启 `bdr_mode=true` 之后，执行的 DDL 不会被 TiCDC 同步。

> **警告：**
>
> 双向复制的 DDL 同步目前为实验特性，不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tidb/issues) 反馈。

### 可复制的 DDL 的同步场景

1. 选择一个 TiDB 集群，执行 `ADMIN SET BDR ROLE PRIMARY` 将其设置为主集群。如下所示：

    ```sql
    ADMIN SET BDR ROLE PRIMARY;
    Query OK, 0 rows affected
    Time: 0.003s

    ADMIN SHOW BDR ROLE;
    +----------+
    | BDR_ROLE |
    +----------+
    | primary  |
    +----------+
    ```

2. 在其他 TiDB 集群上，执行 `ADMIN SET BDR ROLE SECONDARY` 将其设置为从集群。
3. 在主集群上执行**可复制的 DDL**，执行成功的 DDL 会被 TiCDC 同步到从集群中。

> **注意：**
>
> 为了防止误操作：
>
> - 如果在主集群中尝试执行**不可复制的 DDL**，会[报错 8263](/error-codes.md)。
> - 无论在从集群中尝试执行**可复制的 DDL** 还是**不可复制的 DDL**，都会[报错 8263](/error-codes.md)。

### 不可复制的 DDL 的同步场景

1. 对所有 TiDB 集群执行 `ADMIN UNSET BDR ROLE`，撤销集群的 BDR role。
2. 暂停所有集群中需要执行 DDL 的对应的表的写入操作。
3. 等待所有集群中对应表的所有写入已经同步到其他集群后，手动在每一个 TiDB 集群上单独执行所有的 DDL。
4. 等待 DDL 完成之后，重新恢复写入。
5. 按照[可复制的 DDL 的同步场景](#可复制的-ddl-的同步场景)的操作步骤，切换回可复制的 DDL 的同步场景。

> **注意：**
>
> 对所有 TiDB 集群执行 `ADMIN UNSET BDR ROLE` 之后，所有 DDL 都不会被 TiCDC 同步，需要手动在各个集群上分别执行 DDL。

## 停止双向复制

在业务数据停止写入之后，你可以在两个集群中都插入一行特殊的值，通过检查这两行特殊的值来确保数据达到了一致的状态。

检查完毕之后，停止同步任务，并对所有集群执行 `ADMIN UNSET BDR ROLE`。

## 使用限制

- BDR role 只能在以下两种场景中正常使用：

    - 1 个 `PRIMARY` 集群和 n 个 `SECONDARY` 集群（可复制的 DDL 的同步场景）
    - n 个不设置 BDR role 的集群（用于在每个集群手动执行不可复制的 DDL 的同步场景）

    > **注意：**
    >
    > 请勿将 BDR role 设置为其他情况，例如，既存在设置了 `PRIMARY`、`SECONDARY` 的集群，又存在没有设置 BDR role 的集群。如果错误地设置了 BDR role，TiCDC 同步数据期间无法保证数据正确性和一致性。

- 一般情况下，禁止在同步的表中使用 `AUTO_INCREMENT` 或 `AUTO_RANDOM` 键，以免产生数据冲突的问题。如果需要使用 `AUTO_INCREMENT` 或 `AUTO_RANDOM` 键，可以通过在不同的集群设置 `auto_increment_increment` 和 `auto_increment_offset` 来使得不同的集群都能够分配到不同的主键。假设有三个 TiDB 集群（A、B、C）处于双向同步中，那么你可以采取如下设置：

    - 在 A 中设置 `auto_increment_increment=3`，`auto_increment_offset=2000`
    - 在 B 中设置 `auto_increment_increment=3`，`auto_increment_offset=2001`
    - 在 C 中设置 `auto_increment_increment=3`，`auto_increment_offset=2002`

  这样 A、B、C 隐式分配到的 `AUTO_INCREMENT` ID 和 `AUTO_RANDOM` ID 就不会互相冲突。如果需要增加 BDR 模式的集群，需要临时暂停相关业务的写入，重新在所有集群上设置合适的 `auto_increment_increment` 和 `auto_increment_offset`，然后再开启相关业务。

- 双向复制的集群不具备检测写冲突的功能，写冲突将会导致未定义问题。你需要在业务层面保证不出现写冲突。

- TiCDC 双向复制功能支持超过 2 个集群的双向同步，但是不支持多个集群级联模式的同步，即 TiDB A -> TiDB B ->  TiDB C -> TiDB A 的环形复制方式。在这种部署方式下，如果其中一个链路出现问题则会影响整个数据同步链路。因此，如果需要部署多个集群之间的双向复制，每个集群都需要与其他集群两两相连，即 `TiDB A <-> TiDB B`，`TiDB B <-> TiDB C`，`TiDB C <-> TiDB A`。
