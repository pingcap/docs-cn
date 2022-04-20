---
title: DM Relay Log
summary: 了解目录结构、初始迁移规则和 DM relay log 的数据清理。
aliases: ['/docs-cn/tidb-data-migration/dev/relay-log/']
---

# DM Relay Log

DM (Data Migration) 工具的 relay log 由若干组有编号的文件和一个索引文件组成。这些有编号的文件包含了描述数据库更改的事件。索引文件包含所有使用过的 relay log 的文件名。

在启用 relay log 功能后，DM-worker 会自动将上游 binlog 迁移到本地配置目录（若使用 TiUP 部署 DM，则迁移目录默认为 `<deploy_dir> / <relay_log>`）。本地配置目录 `<relay_log>` 的默认值是 `relay-dir`，可在[上游数据库配置文件](/dm/dm-source-configuration-file.md)中进行修改。自 v5.4.0 版本起，你可以在 [DM-worker 配置文件](/dm/dm-worker-configuration-file.md)中通过 `relay-dir` 配置本地配置目录，其优先级高于上游数据库的配置文件。

![reley](/media/dm/dm-relay-log.png)

Relay log 的使用场景:

- Mysql 的存储空间是有限制的，一般都会设置 binlog 的最长保存时间，当上游把 binlog 清除掉之后，如果 DM 还需要对应位置的 binlog 就会拉取失败，导致同步任务出错；
- 若未开启 relay log ，DM 每增加一个同步任务都会在上游建立一条链接用于拉取 binlog，这样会对上游造成比较大的负载，开启 relay log 后同一个上游的多个同步任务可以复用已经拉倒本地的 relay log，这样就减少了对上游的压力；
- all 类型的迁移任务中，DM 需要先进行全量数据迁移，再根据 binlog 增量同步。若全量阶段持续时间较长，上游 binlog 可能会被清除，导致增量同步无法进行。若先开启了 relay log，则 DM 会自动在本地保留足够的日志，保证增量任务正常进行。

一般情况下建议开启 relay log ，但仍需知晓其可能导致的负面作用：

- 由于写 relay log 有一个落盘的过程，这里产生了外部 IO 和一些 CPU 消耗，可能导致整个同步链路变长从而增加数据同步的时延，如果是对时延要求十分敏感的同步任务暂时还不推荐使用 relay log。注意：在最新版本的 DM（>v2.0.7） 中，对这里进行了优化，增加的时延和 CPU 消耗已经相对较小了。

## 开启/关闭 relay log

<SimpleTab>

<div label="v5.4.0 及之后的版本">

在 v5.4.0 及之后的版本中，你可以通过将 `enable-relay` 设为 `true` 开启 relay log。自 v5.4.0 起，DM-worker 在绑定上游数据源时，会检查上游数据源配置中的 `enable-relay` 项。如果 `enable-relay` 为 `true`，则为该数据源启用 relay log 功能。

具体配置方式参见[上游数据源配置文件介绍](/dm/dm-source-configuration-file.md)
    
除此以外，你也可以通过 `start-relay` 或 `stop-relay` 命令动态调整数据源的 `enable-relay` 并即时开启或关闭 relay log。
    
{{< copyable "shell-regular" >}}

```bash
» start-relay -s mysql-replica-01
```

```
{
    "result": true,
    "msg": ""
}
```

</div> 
    
<div label="v2.0.2（包含）到 v5.3.0（包含）">

> **注意：**
> 
> 在 v2.0.2 及之后的 v2.0 版本，以及在 v5.3.0 版本中，上游数据源配置中的 `enable-relay` 项失效，你只能通过`start-relay` 和 `stop-relay`命令开启和关闭 relay log。[加载数据源配置](/dm/dm-manage-source.md#数据源操作)时，如果 DM 发现配置中的 `enable-relay` 项为 `true`，会给出如下信息提示：
> 
> ```
> Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.
> ```

`start-relay` 命令可以配置一个或多个 DM-worker 为指定数据源迁移 relay log，但只能指定空闲或者已绑定了该上游数据源的 DM-worker。使用示例如下：

{{< copyable "" >}}

```bash
» start-relay -s mysql-replica-01 worker1 worker2
```

```
{
    "result": true,
    "msg": ""
}
```

{{< copyable "" >}}

```bash
» stop-relay -s mysql-replica-01 worker1 worker2
```

```
{
    "result": true,
    "msg": ""
}
```

</div>

<div label="v2.0.2 之前的版本">

在 v2.0.2 之前的版本（不含 v2.0.2），DM-worker 在绑定上游数据源时，会检查上游数据源配置中的 `enable-relay` 项。如果 `enable-relay` 为 `true`，则为该数据源启用 relay log 功能。

具体配置方式参见[上游数据源配置文件介绍](/dm/dm-source-configuration-file.md)

</div>
</SimpleTab>

## 查询 relay log

`query-status -s` 命令可以查询 relay log 的状态。

{{< copyable "" >}}

```bash
» query-status -s mysql-replica-01
```

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "no sub task started",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker2",
                "result": null,
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000005, 916)",
                    "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relaySubDir": "09bec856-ba95-11ea-850a-58f2b4af5188.000001",
                    "relayBinlog": "(mysql-bin.000005, 4)",
                    "relayBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relayCatchUpMaster": false,
                    "stage": "Running",
                    "result": null
                }
            },
            "subTaskStatus": [
            ]
        },
        {
            "result": true,
            "msg": "no sub task started",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000005, 916)",
                    "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relaySubDir": "09bec856-ba95-11ea-850a-58f2b4af5188.000001",
                    "relayBinlog": "(mysql-bin.000005, 916)",
                    "relayBinlogGtid": "",
                    "relayCatchUpMaster": true,
                    "stage": "Running",
                    "result": null
                }
            },
            "subTaskStatus": [
            ]
        }
    ]
}
```

## 暂停、恢复 relay log

`pause-relay` 与 `resume-relay` 命令可以分别暂停及恢复 relay log 的拉取。这两个命令执行时都需要指定上游数据源的 `source-id`，例如：

{{< copyable "" >}}

```bash
» pause-relay -s mysql-replica-01 -s mysql-replica-02
```

```
{
    "op": "PauseRelay",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        },
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-02",
            "worker": "worker2"
        }
    ]
}
```
    
{{< copyable "" >}}

```bash
» resume-relay -s mysql-replica-01
```    

```
{
    "op": "ResumeRelay",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```

## 清理 relay log

relay log  的清理 DM 提供了两种方式，手动清理和自动清理，需要注意的是这两种清理方法都不会清理活跃的 relay log 。

> **注意：**
> 
> 活跃的 relay log  定义：该 relay log  正在被同步任务使用。
> 
> 过期的 relay log  定义：该 relay log  文件最后被改动的时间与当前时间差值大于配置文件中的 `expires` 字段。
> 
> 活跃的 relay log 当前只在 Syncer Unit 被更新和写入，假设一个为 All 模式的同步任务在全量导出/导入阶段花费了超过数据源 purge 里配置的过期时间，该 relay log  依旧会被清除。

### 自动数据清理

启用自动数据清理需在 source 配置文件中进行以下配置：

```yaml
# relay log purge strategy
purge:
    interval: 3600
    expires: 24
    remain-space: 15
```

- `purge.interval`
    - 后台自动清理的时间间隔，以秒为单位。
    - 默认为 "3600"，表示每 3600 秒执行一次后台清理任务。

- `purge.expires`
    - 当前 relay 处理单元没有写入、或已有数据迁移任务当前或未来不需要读取的 relay log 在被后台清理前可保留的小时数。
    - 默认为 "0"，表示不按 relay log 的更新时间执行数据清理。

- `purge.remain-space`
    - 剩余磁盘空间，单位为 GB。若剩余磁盘空间小于该配置，则指定的 DM-worker 机器会在后台尝试自动清理可被安全清理的 relay-log。若这一数字被设为 "0"，则表示不按剩余磁盘空间来清理数据。
    - 默认为 "15"，表示可用磁盘空间小于 15GB 时，DM-master 会尝试安全地清理 relay log。

### 手动数据清理

手动数据清理是指使用 dmctl 提供的 `purge-relay` 命令，通过指定 `subdir` 和 binlog 文件名，来清理掉**指定 binlog 之前**的所有 relay log。若在命令中不填 `-subdir` 选项，则默认清理**最新 relay log 子目录之前**的所有 relay log。

假设当前 relay log 的目录结构如下：

{{< copyable "shell-regular" >}}

```bash
tree .
```

```
.
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   `-- relay.meta
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
|   |-- mysql-bin.000001
|   `-- relay.meta
|-- e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index
```

{{< copyable "shell-regular" >}}

```bash
cat server-uuid.index
```

```
deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
```

在 dmctl 中使用 `purge-relay` 命令的示例如下：

+ 以下命令指定的 relay log 子目录为 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`，该子目录之前的 relay log 子目录为 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`。所以该命令实际清空了 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001` 子目录，保留 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002` 和 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` 子目录。

    {{< copyable "" >}}

    ```bash
    » purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

+ 以下命令默认 `--sub-dir` 为最新的 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` 子目录。该目录之前的 relay log 子目录为 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001` 和 `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`，所以该命令实际清空了这两个子目录，保留了 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`。

    {{< copyable "" >}}

    ```bash
    » purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```

## 目录结构

Relay log 本地存储的目录结构示例如下：

```
<deploy_dir>/<relay_log>/
|-- 7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   |-- mysql-bin.000004
|   `-- relay.meta
|-- 842965eb-091c-11e9-9e45-9a3bff03fa39.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index
```

- `subdir`：

    - DM-worker 把从上游数据库迁移到的 binlog 存储在同一目录下，每个目录都为一个 `subdir`。
    - `subdir` 的命名格式为 `<上游数据库 UUID>.<本地 subdir 序列号>`。
    - 在上游进行 master 和 slave 实例切换后，DM-worker 会生成一个序号递增的新 `subdir` 目录。

        - 在以上示例中，对于 `7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001` 这一目录，`7e427cc0-091c-11e9-9e45-72b7c59d52d7` 是上游数据库的 UUID，`000001` 是本地 `subdir` 的序列号。

- `server-uuid.index`：记录当前可用的 `subdir` 目录。

- `relay.meta`：存储每个 `subdir` 中已迁移的 binlog 信息。例如，

    ```bash
    cat c0149e17-dff1-11e8-b6a8-0242ac110004.000001/relay.meta
    ```

    ```
    binlog-name = "mysql-bin.000010"    # 当前迁移的 binlog 名
    binlog-pos = 63083620               # 当前迁移的 binlog 位置
    binlog-gtid = "c0149e17-dff1-11e8-b6a8-0242ac110004:1-3328" # 当前迁移的 binlog GTID
    ```

    也可能包含多个 GTID：

    ```bash
    cat 92acbd8a-c844-11e7-94a1-1866daf8accc.000001/relay.meta
    ```

    ```
    binlog-name = "mysql-bin.018393"
    binlog-pos = 277987307
    binlog-gtid = "3ccc475b-2343-11e7-be21-6c0b84d59f30:1-14,406a3f61-690d-11e7-87c5-6c92bf46f384:1-94321383,53bfca22-690d-11e7-8a62-18ded7a37b78:1-495,686e1ab6-c47e-11e7-a42c-6c92bf46f384:1-34981190,03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170,10b039fc-c843-11e7-8f6a-1866daf8d810:1-308290454"
    ```

## DM 从什么位置开始接收 binlog

- 从保存的 checkpoint 中（默认位于下游 dm_meta 库），获取各同步任务需要该数据源的最早位置。如果该位置晚于下述任何一个位置，则从此位置开始迁移。

- 若本地 relay log 有效（有效是指 relay log 具有有效的 `server-uuid.index`，`subdir` 和 `relay.meta` 文件），DM-worker 从 `relay.meta` 记录的位置恢复迁移。

- 若不存在有效的本地 relay log，但上游数据源配置文件中指定了 `relay-binlog-name` 或 `relay-binlog-gtid`：

    - 在非 GTID 模式下，若指定了 `relay-binlog-name`，则 DM-worker 从指定的 binlog 文件开始迁移。

    - 在 GTID 模式下，若指定了 `relay-binlog-gtid`，则 DM-worker 从指定的 GTID 开始迁移。

- 若不存在有效的本地 relay log，而且 DM 配置文件中未指定 `relay-binlog-name` 或 `relay-binlog-gtid`：

    - 在非 GTID 模式下，DM-worker 从初始的上游 binlog 开始迁移，并将所有上游 binlog 文件连续迁移至最新。

    - 在 GTID 模式下，DM-worker 从初始上游 GTID 开始迁移。

        > **注意：**
        >
        > 若上游的 relay log 被清理掉，则会发生错误。在这种情况下，需设置 `relay-binlog-gtid` 来指定迁移的起始位置。

## 更多

- [DM 源码阅读系列文章（六）relay log 的实现丨TiDB 工具](https://pingcap.com/zh/blog/dm-source-code-reading-6)