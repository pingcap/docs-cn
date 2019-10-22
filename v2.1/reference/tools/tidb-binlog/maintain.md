---
title: TiDB Binlog 集群运维
category: reference
aliases: ['/docs-cn/v2.1/how-to/maintain/tidb-binlog/']
---

# TiDB Binlog 集群运维

本文首先介绍 Pump 和 Drainer 的状态及启动、退出的内部处理流程，然后说明如何通过 binlogctl 工具或者直接在 TiDB 执行 SQL 操作来管理 binlog 集群，最后的 FAQ 部分会介绍一些常见问题以及处理方法。

## Pump/Drainer 的状态

Pump/Drainer 中状态的定义：

* online：正常运行中
* pausing：暂停中
* paused：已暂停
* closing：下线中
* offline：已下线

这些状态由 Pump/Drainer 服务自身进行维护，并定时将状态信息更新到 PD 中。

## Pump/Drainer 的启动、退出流程

### Pump

* 启动：Pump 启动时会通知所有 online 状态的 Drainer，如果通知成功，则 Pump 将状态设置为 online，否则 Pump 将报错，然后将状态设置为 paused 并退出进程。
* 退出：Pump 进程正常退出前要选择进入暂停或者下线状态；非正常退出（kill -9、进程 panic、宕机）都依然保持 online 状态。

    * 暂停：使用 kill（非 kill -9）、Ctrl+C 或者使用 binlogctl 的 pause-pump 命令都可以暂停 Pump。接收到暂停指令后，Pump 会变更状态为 pausing，并停止接受 binlog 的写请求，也停止向 Drainer 提供 binlog 数据。安全退出所有线程后，更新状态为 paused 然后退出进程。
    * 下线：仅在使用 binlogctl 的 offline-pump 命令的情况下才会下线 Pump。接收到下线指令后，Pump 会变更状态为 closing，并停止接受 binlog 的写请求。Pump 继续向 Drainer 提供 binlog，等待所有 binlog 数据都被 Drainer 消费后再将状态设置为 offline 并退出进程。

### Drainer

* 启动：Drainer 启动时将状态设置为 online，并尝试从所有非 offline 状态的 Pump 获取 binlog，如果获取 binlog 失败，会不断尝试重新获取。
* 退出：Drainer 进程正常退出前要选择进入暂停或者下线状态；非正常退出（kill -9 、进程 panic、宕机）都依然保持 online 状态。

    * 暂停：使用 kill（非 kill -9）、Ctrl+C 或者使用 binlogctl 的 pause-drainer 命令都可以暂停 Drainer。接收到指令后，Drainer 会变更状态为 pausing，并停止从 Pump 获取 binlog。安全退出所有线程后，更新状态为 paused 然后退出进程。
    * 下线：仅在使用 binlogctl 的 offline-drainer 命令的情况下才会下线 Drainer。接收到下线指令后，Drainer 变更状态为 closing，并停止从 Pump 获取 binlog。安全退出所有线程后，更新状态为 offline 然后退出进程。

关于 Pump/Drainer 暂停、下线、状态查询、状态修改等具体的操作方法，参考如下 binlogctl 工具的使用方法介绍。

## binlogctl 工具

支持如下这些功能：

* 查看 Pump/Drainer 状态
* 暂停/下线 Pump/Drainer
* Pump/Drainer 异常状态处理

使用 binlogctl 的场景：

* 同步出现故障/检查运行情况，需要查看 Pump/Drainer 的状态
* 维护集群，需要暂停/下线 Pump/Drainer
* Pump/Drainer 异常退出，状态没有更新，或者状态不符合预期，对业务造成影响

binlogctl 下载链接：

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz && \
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256
```

检查文件完整性，返回 ok 则正确：

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-{version}-linux-amd64.sha256
```

对于 v2.1.0 GA 及以上版本，binlogctl 已经包含在 TiDB 的下载包中，其他版本需要单独下载 binlogctl:

{{< copyable "shell-regular" >}}

```bash
wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz && \
wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256
```

检查文件完整性，返回 ok 则正确：

{{< copyable "shell-regular" >}}

```bash
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
```

binlogctl 使用说明：

命令行参数：

```bash
Usage of binlogctl:
-V
输出 binlogctl 的版本信息
-cmd string
    命令模式，包括 "generate_meta"（已废弃）, "pumps", "drainers", "update-pump" ,"update-drainer", "pause-pump", "pause-drainer", "offline-pump", "offline-drainer"
-data-dir string
    保存 Drainer 的 checkpoint 的文件的路径 (默认 "binlog_position")（已废弃）
-node-id string
    Pump/Drainer 的 ID
-pd-urls string
    PD 的地址，如果有多个，则用"," 连接 (默认 "http://127.0.0.1:2379")
-ssl-ca string
    SSL CAs 文件的路径
-ssl-cert string
        PEM 格式的 X509 认证文件的路径
-ssl-key string
        PEM 格式的 X509 key 文件的路径
-time-zone string
    如果设置时区，在 "generate_meta" 模式下会打印出获取到的 tso 对应的时间。例如"Asia/Shanghai" 为 CST 时区，"Local" 为本地时区
-show-offline-nodes
    在用 -cmd pumps 或 -cmd drainers 时使用，这两个命令默认不显示 offline 的节点，仅当明确指定 -show-offline-nodes 时会显示 
```

命令示例：

- 查询所有的 Pump/Drainer 的状态：

    设置 `cmd` 为 `pumps` 或者 `drainers` 来查看所有 Pump 或者 Drainer 的状态。例如：

    {{< copyable "shell-regular" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps
    ```

    ```
    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=pump] [node="{NodeID: 1.1.1.1:8250, Addr: pump:8250, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

    {{< copyable "shell-regular" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd drainers
    ```

    ```
    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=drainer] [node="{NodeID: 1.1.1.1:8249, Addr: 1.1.1.1:8249, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

- 暂停/下线 Pump/Drainer

    binlogctl 提供以下命令暂停/下线服务：

    | cmd             | 说明           | 示例                                                                                             |
    | --------------- | ------------- | ------------------------------------------------------------------------------------------------|
    | pause-pump      | 暂停 Pump      | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250`       |
    | pause-drainer   | 暂停 Drainer   | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-drainer -node-id ip-127-0-0-1:8249`    |
    | offline-pump    | 下线 Pump      | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-pump -node-id ip-127-0-0-1:8250`     |
    | offline-drainer | 下线 Drainer   | `bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd offline-drainer -node-id ip-127-0-0-1:8249`  |

    binlogctl 会发送 HTTP 请求给 Pump/Drainer，Pump/Drainer 收到命令后会主动执行对应的退出流程。

- 异常情况下修改 Pump/Drainer 的状态

    在服务正常运行以及符合流程的暂停、下线过程中，Pump/Drainer 的状态都是可以正确的。但是在一些异常情况下 Pump/Drainer 无法正确维护自己的状态，可能会影响数据同步任务，在这种情况下需要使用 binlogctl 修复状态信息。

    设置 `cmd` 为 `update-pump` 或者 `update-drainer` 来更新 Pump 或者 Drainer 的状态。Pump 和 Drainer 的状态可以为 paused 或者 offline。例如：

    {{< copyable "shell-regular" >}}

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    > **注意：**
    >
    > Pump/Drainer 在正常运行过程中会定期在 PD 中更新自己的状态，而这条命令是直接去修改 Pump/Drainer 保存在 PD 中的状态，所以在 Pump/Drainer 服务正常的情况下使用这些命令是没有意义的。仅在 Pump/Drainer 服务异常的情况下使用，具体哪些场景下使用这条命令可以参考 FAQ。

## 使用 TiDB SQL 管理 Pump/Drainer

要查看和管理 binlog 相关的状态，可在 TiDB 中执行相应的 SQL 语句。

- 查看 TiDB 是否开启 binlog

    {{< copyable "sql" >}}

    ```sql
    show variables like "log_bin";
    ```

    ```
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | log_bin       |  ON   |
    +---------------+-------+
    ```

    值为 `ON` 时表示 TiDB 开启了 binlog。

- 查看 Pump/Drainer 状态

    {{< copyable "sql" >}}

    ```sql
    show pump status;
    ```

    ```
    +--------|----------------|--------|--------------------|---------------------|
    | NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +--------|----------------|--------|--------------------|---------------------|
    | pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
    +--------|----------------|--------|--------------------|---------------------|
    | pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
    +--------|----------------|--------|--------------------|---------------------|
    ```

    {{< copyable "sql" >}}

    ```sql
    show drainer status;
    ```

    ```
    +----------|----------------|--------|--------------------|---------------------|
    |  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
    +----------|----------------|--------|--------------------|---------------------|
    ```

- 异常情况下修改 Pump/Drainer 状态

    {{< copyable "sql" >}}

    ```sql
    change pump to node_state ='paused' for node_id 'pump1';
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    change drainer to node_state ='paused' for node_id 'drainer1';
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    该 SQL 的功能和 binlogctl 中的 update-pump 和 update-drainer 命令的功能一样，因此也只有在 Pump/Drainer 异常的情况下使用。

> **注意：**
>
> 1. 查看 binlog 开启状态以及 Pump/Drainer 状态的功能在 TiDB v2.1.7 及以上版本中支持。
> 2. 修改 Pump/Drainer 状态的功能在 TiDB v3.0.0-rc.1 及以上版本中支持。该功能只修改 PD 中存储的 Pump/Drainer 状态，如果需要暂停/下线节点，仍然需要使用 `binlogctl`。

## FAQ

### 在什么情况下暂停和下线 Pump/Drainer？

首先需要通过以上的内容来了解 Pump/Drainer 的状态定义和启动、退出的流程。

暂停主要针对临时需要停止服务的场景，例如：

- 版本升级：停止进程后使用新的 binary 启动服务
- 服务器维护：需要对服务器进行停机维护，退出进程，等维护完成后重启服务

下线主要针对永久（或长时间）不再使用该服务的场景，例如：

- Pump 缩容：不再需要那么多服务了，下线部分服务
- 同步任务取消：不再需要同步到某个下游，下线对应的 Drainer
- 服务器迁移：服务需要迁移到其他服务器，下线服务，在新的服务器上重新部署

### 可以通过哪些方式暂停 Pump/Drainer？

- 直接 kill 进程。注意：不能使用 kill -9，这种情况 Pump/Drainer 无法对信号进行处理
- Pump/Drainer 运行在前台，则可以通过 Ctrl+C 暂停
- 使用 binlogctl 的 pause-pump/pause-drainer

### 可以使用 binlogctl 的 update-pump/update-drainer 命令来暂停 Pump/Drainer 服务吗？

不可以，update-pump/update-drainer 命令直接修改 PD 中保存的状态信息，使用这个命令并不会通知 Pump/Drainer 做相应的操作，**而且使用不当会使数据同步中断，甚至造成数据丢失。**

### 什么情况下使用 binlogctl 的 update-pump 命令设置 Pump 状态为 paused？

在某些异常情况下，Pump 没有正确维护自己的状态，实际上状态应该为 paused，可以使用 update-pump 对状态进行修正，例如：

- Pump 异常退出（出现 panic 直接退出进程，或者误操作执行 kill -9 直接 kill 掉进程），Pump 保存在 PD 中的状态仍然为 online。如果暂时不需要重启 Pump 恢复服务，可以使用 update-pump 把该 Pump 状态设置为 paused，避免对 TiDB 写 binlog 和 Drainer 获取 binlog 造成干扰。

### 什么情况下使用 binlogctl 的 update-drainer 命令设置 Drainer 状态为 paused？

在某些异常情况下，Drainer 没有正确维护自己的状态，实际上状态应该为 paused，对数据同步造成了影响，可以使用 update-drainer 对状态进行修正，例如：

- Drainer 异常退出（出现 panic 直接退出进程，或者误操作执行 kill -9 直接 kill 掉进程），Drainer 保存在 PD 中的状态仍然为 online。当 Pump 启动时无法正常通知该 Drainer（报错 `notify drainer ...`），导致 Pump 无法正常运行。这个时候可以使用 update-drainer 将 Drainer 状态更新为 paused，再启动 Pump。

### 可以通过哪些方式下线 Pump/Drainer？

目前只可以使用 binlogctl 的 offline-pump 和 offline-drainer 来下线 Pump 和 Drainer。

### 可以使用 binlogctl 的 update-pump/update-drainer 命令来下线 Pump/Drainer 服务吗？

不可以，使用 update-pump/update-drainer 命令会直接修改 PD 中保存的状态信息，并且不会通知 Pump/Drainer 做相应的操作。使用不当时，可能会干扰数据同步，某些情况下还可能会造成*数据不一致*的严重后果。例如：

- 当 Pump 正常运行或者处于暂停状态时，使用 update-pump 将该 Pump 设置为 offline，Drainer 会放弃获取处于 offline 状态的 Pump 的 binlog 数据，导致该 Pump 最新的 binlog 数据没有同步到 Drainer，造成上下游数据不一致。
- 当 Drainer 正常运行时，使用 update-drainer 将该 Drainer 设置为 offline。这个时候启动一个 Pump，Pump 只会通知 online 状态的 Drainer，导致该 Drainer 没有及时获取到该 Pump 的 binlog 数据，造成上下游数据不一致。

### 什么情况下使用 binlogctl 的 update-pump 命令设置 Pump 状态为 offline?

> **警告：**
>
> 仅在可以容忍 binlog **数据丢失、上下游数据不一致**或者确认不再需要使用该 Pump 存储的 binlog 数据的情况下，才能使用 update-pump 修改 Pump 状态为 offline。

可以使用 update-pump 修改 Pump 状态为 offline 的情况有：

- 在某些情况下，Pump 异常退出进程，且无法恢复服务，同步就会中断。如果希望恢复同步且可以容忍部分 binlog 数据丢失，可以使用 update-pump 命令将该 Pump 状态设置为 offline，则 Drainer 会放弃拉取该 Pump 的 binlog 然后继续同步数据。
- 有从历史任务遗留下来且不再使用的 Pump 且进程已经退出（例如测试使用的服务），之后不再需要使用该服务，使用 update-pump 将该 Pump 设置为 offline。

在其他情况下一定要使用 offline-pump 命令让 Pump 走正常的下线处理流程。

### Pump 进程已经退出，且状态为 paused，现在不想使用这个 Pump 了，能否用 update-pump 命令设置状态为 offline？

Pump 以 paused 状态退出进程时，不保证所有 binlog 数据被下游 Drainer 消费。所以这样做会有上下游数据不一致的风险。正确的做法是重新启动 Pump，然后使用 offline-pump 下线该 Pump。

### 什么情况下使用 binlogctl 的 update-drainer 命令设置 Drainer 状态为 offline？

- 有从历史任务遗留下来且不再使用的 Drainer 且进程已经退出（例如测试使用的服务），之后不再需要使用该服务，使用 update-drainer 将该 Drainer 设置为 offline。

### 可以使用 `change pump`、`change drainer` 等 SQL 操作来暂停或者下线 Pump/Drainer 服务吗？

目前还不支持，这种 SQL 操作会直接修改 PD 中保存的状态，在功能上等同与 binlogctl 的 update-pump、update-drainer 命令。如果需要暂停或者下线，仍然要使用 binlogctl。

### 同步时出现上游数据库支持但是下游数据库执行会出错的 DDL，应该怎么办？

1. 查看 drainer.log 日志，查找 `exec failed` 找到 Drainer 退出前最后一条执行失败的 DDL。
2. 将 DDL 改为下游兼容支持的版本，在下游数据库中手动执行。
3. 查看 drainer.log 日志，查找执行失败的 DDL 语句，可以查询到该 DDL 的 commit-ts。
4. 编辑 drainer.toml 配置文件，在 ignore-txn-commit-ts 项中添加该 commit-ts，重启 Drainer。

在绝大部分情况下，TiDB 和 MySQL 的语句都是兼容的。用户需要注意的是上下游的 sql_mode 应当保持一致。
