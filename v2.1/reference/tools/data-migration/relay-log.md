---
title: DM Relay Log
summary: 了解目录结构、初始同步规则和 DM relay log 的数据清理。
category: reference
---

# DM Relay Log

DM (Data Migration) 工具的 relay log 由一组有编号的文件和一个索引文件组成。这些有编号的文件包含了描述数据库更改的事件。索引文件包含所有使用过的 relay log 的文件名。

DM-worker 在启动后，会自动将上游 binlog 同步到本地配置目录（若使用 DM-Ansible 部署 DM，则同步目录默认为 `<deploy_dir> / relay_log` ）。DM-worker 在运行过程中，会将上游 binlog 实时同步到本地文件。DM-worker 的处理单元 Syncer 会实时读取本地 relay log 的 binlog 事件，将这些事件转换为 SQL 语句，再将 SQL 语句同步到下游数据库。

本文档介绍 DM relay log 的目录结构、初始同步规则和数据清理方法。

## 目录结构

Relay-log 本地存储的目录结构示例如下：

```
<deploy_dir>/relay_log/
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

    - DM-worker 把从上游数据库同步到的 binlog 存储在同一目录下，每个目录都为一个 `subdir`。
    - `subdir` 的命名格式为 `<上游数据库 UUID>.<本地 subdir 序列号>`。
    - 在上游进行 master 和 slave 实例切换后，DM-worker 会生成一个序号递增的新 `subdir` 目录。

        - 在以上示例中，对于 `7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001` 这一目录，`7e427cc0-091c-11e9-9e45-72b7c59d52d7` 是上游数据库的 UUID，`000001` 是本地 `subdir` 的序列号。

- `server-uuid.index`：记录当前可用的 `subdir` 目录。

- `relay.meta`：存储每个 `subdir` 中已同步的 binlog 信息。例如，

    ```
    $ cat c0149e17-dff1-11e8-b6a8-0242ac110004.000001/relay.meta
    binlog-name = "mysql-bin.000010"    # 当前同步的 binlog 名
    binlog-pos = 63083620               # 当前同步的 binlog 位置
    binlog-gtid = "c0149e17-dff1-11e8-b6a8-0242ac110004:1-3328" # 当前同步的 binlog GTID

    # 可能包含多个 GTID
    $ cat 92acbd8a-c844-11e7-94a1-1866daf8accc.000001/relay.meta
    binlog-name = "mysql-bin.018393"
    binlog-pos = 277987307
    binlog-gtid = "3ccc475b-2343-11e7-be21-6c0b84d59f30:1-14,406a3f61-690d-11e7-87c5-6c92bf46f384:1-94321383,53bfca22-690d-11e7-8a62-18ded7a37b78:1-495,686e1ab6-c47e-11e7-a42c-6c92bf46f384:1-34981190,03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170,10b039fc-c843-11e7-8f6a-1866daf8d810:1-308290454"
    ```

## 初始同步规则

DM-worker 每次启动时（或在 DM-worker 暂停后 relay log 恢复同步），同步的起始位置会出现以下几种情况：

- 若是有效的本地 relay log（有效是指 relay log 具有有效的 `server-uuid.index`，`subdir` 和 `relay.meta` 文件），DM-worker 从 `relay.meta` 记录的位置恢复同步。

- 若不存在有效的本地 relay log，而且 DM 配置文件中未指定 `relay-binlog-name` 或 `relay-binlog-gtid`：

    - 在非 GTID 模式下，DM-worker 从初始的上游 binlog 开始同步，并将所有上游 binlog 文件连续同步至最新。

    - 在 GTID 模式下，DM-worker 从初始上游 GTID 开始同步。

        > **注意：**
        >
        > 若上游的 relay log 被清理掉，则会发生错误。在这种情况下，需设置 `relay-binlog-gtid` 来指定同步的起始位置。

- 若不存在有效的本地 relay log：

    - 在非 GTID 模式下，若指定了 `relay-binlog-name`，则 DM-worker 从指定的 binlog 文件开始同步。
    - 在 GTID 模式下，若指定了 `relay-binlog-gtid`，则 DM-worker 从指定的 GTID 开始同步。

## 数据清理

因为存在文件读写的检测机制，所以 DM-worker 不会清理正在使用的 relay log，也不会清理当前任务稍后会使用到的 relay log。

Relay log 的数据清理包括自动清理和手动清理这两种方法。

### 自动数据清理

自动数据清理需对 DM-worker 配置文件中的以下三项进行配置：

- `purge-interval`
    - 后台自动清理的时间间隔，以秒为单位。
    - 默认为 "3600"，表示每 3600 秒执行一次后台清理任务。

- `purge-expires`
    - 未更新的 relay log 在被后台清理前可保留的小时数。
    - 默认为 "0"，表示不按 relay log 的更新时间执行数据清理。

- `purge-remain-space`
    - 剩余磁盘空间，单位为 GB。若剩余磁盘空间小于该配置，则指定的 DM-worker 机器会在后台尝试自动清理可被安全清理的 relay-log。若这一数字被设为 "0"，则表示不按剩余磁盘空间来清理数据。
    - 默认为 "15"，表示可用磁盘空间小于 15GB 时，DM-master 会尝试安全地清理 relay log。

### 手动数据清理

手动数据清理是指使用 dmctl 提供的 `purge-relay` 命令，通过指定 `subdir` 和 binlog 文件名，来清理掉指定 binlog 之前的所有 relay log。

假设当前 relay log 的目录结构如下：

```
$ tree .
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

$ cat server-uuid.index
deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
```

若使用 dmctl 来执行以下命令，可得到如下相应的结果：

```
# 执行该命令会清空 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001` 目录
# `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002` 和 `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` 目录保留

» purge-relay -w 10.128.16.223:10081 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002

# 执行该命令会清空 `deb76a2b-09cc-11es9-9129-5242cf3bb246.000001、e4e0e8ab-09cc-11e9-9220-82cc35207219.000002` 目录
# `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` 目录保留

» purge-relay -w 10.128.16.223:10081 --filename mysql-bin.000001
```
