---
title: 集群实时增量同步
---

# 集群实时增量同步

本文档介绍如何为一个 TiDB 集群开启一个 TiDB/MySQL 的从集群，并且将增量数据实时同步到从集群。

## 使用场景

当需要为一个运行中的 TiDB 集群设置从集群，并行进行数据同步的时候，可使用 BR/Dumpling/TiDB Binlog 进行操作。例如要将集群 A 的数据同步到新集群 B。

## 实现原理

任何写入 TiDB 的事务均指定了唯一的 commit TS，可以通过该 TS 获取一个 TiDB 集群全局一致的状态。

通过 BR 或者 Dumpling 将集群的数据从一个全局一致的时间点导出，然后再用 TiDB Binlog 衔接这个全局一致的时间点开启增量同步。

总结来说，同步过程分为全量同步和增量同步

1. 执行全量备份恢复，并且获取到备份数据的 commit TS。
2. 执行增量同步，确保增量同步的起始点是备份数据的 commit TS。

> **注意：**
>
> * 备份导出时候的 commit ts 是闭区间，TiDB Binlog 开启同步的 initial-commit-ts 是开区间。

## 步骤

假设现有 A 集群正常运行，要新建一个 B 集群进行同步。可以通过以下步骤来实现

### 开启 TiDB Binlog

确保 A 集群已经部署并且开启了 TiDB-Binlog(/tidb-binlog/deploy-tidb-binlog.md)。

### 全量导出

1. 全局一致的数据导出：将集群 A 的数据导出到指定路径下，以下工具二选一即可。

    - 使用 [BR 全量备份](/br/use-br-command-line-tool.md#备份全部集群数据)。

    - 使用 [Dumpling 全量导出](/dumpling-overview.md)，

2. 获取全局一致的时间点 COMMIT_TS：

    - 使用 br `validate` 指令获取备份的时间戳，示例如下：

        {{< copyable "shell-regular" >}}

        ```shell
        COMMIT_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
        ```

    - 查阅 Dumpling metadata 获取 Pos(COMMIT_TS)。

        {{< copyable "shell-regular" >}}

        ```shell
        cat metadata
        ```

        ```shell
        Started dump at: 2020-11-10 10:40:19
        SHOW MASTER STATUS:
                Log: tidb-binlog
                Pos: 420747102018863124

        Finished dump at: 2020-11-10 10:40:20
        ```

3. 将集群 A 的数据导入 B 集群。

## 增量同步

1. 修改 TiDB Binlog 的 drainer toml 配置文件，增加如下配置，从指定位置开始同步至 B 集群。

{{< copyable "" >}}

```toml
initial-commit-ts = COMMIT_TS
[syncer.to]
host = {B 集群}
port = 3306
```
