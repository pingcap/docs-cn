---
title: TiDB-Binlog 集群运维
category: tools
---

# TiDB-Binlog 集群运维

## Pump/Drainer 状态

Pump/Drainer 中状态的定义：

* online：正常运行中。
* pausing：暂停中，当使用 kill 或者 Ctrl+C 退出进程时，都将处于该状态。当 Pump/Drainer 安全退出了所有的内部线程后，将自己的状态切换为 paused。
* paused：已暂停，处于该状态时 Pump 不接受写 binlog 的请求，也不继续为 Drainer 提供 binlog，Drainer 不再往下游同步数据。
* closing：下线中，使用 binlogctl 控制 Pump/Drainer 下线，在进程退出前都处于该状态。下线时 Pump 不再接受写 binlog 的请求，等待所有的 binlog 数据被 Drainer 消费完。
* offline：已下线，当 Pump 已经将已保存的所有 binlog 数据全部发送给 Drainer 后，该 Pump 将状态切换为 offline。

> **注意：**
>
> * 当暂停 Pump/Drainer 时，数据同步会中断。
> * Pump/Drainer 的状态需要区分已暂停（paused）和下线（offline），Ctrl + C 或者 kill 进程，Pump 和 Drainer 的状态会变为 pausing，最终变为 paused。进入 paused 状态前 Pump 不需要将已保存的 Binlog 数据全部发送到 Drainer，进入 offline 状态前 pump 需要将已保存的 Binlog 数据全部发送到 Drainer。如果需要较长时间退出 Pump（或不再使用该 Pump），需要使用 binlogctl 工具来下线 Pump。Drainer 同理。
> * Pump 在下线时需要确认自己的数据被所有的非 offline 状态的 Drainer 消费了，所以在下线 Pump 时需要确保所有的 Drainer 都是处于 online 状态，否则 Pump 无法正常下线。
> * Pump 保存的 binlog 数据只有在被所有非 offline 状态的 Drainer 消费的情况下才会被 GC 处理。
> * 不要轻易下线 Drainer，只有在永久不需要使用该 Drainer 的情况下才需要下线 Drainer。

关于 Pump/Drainer 暂停、下线、状态查询、状态修改等具体的操作方法，参考如下 binlogctl 工具的使用方法介绍。

## binlogctl 工具

* 获取 TiDB 集群当前的 TSO
* 查看 Pump/Drainer 状态
* 修改 Pump/Drainer 状态
* 暂停/下线 Pump/Drainer

使用 binlogctl 的场景：

* 第一次运行 Drainer，需要获取 TiDB 集群当前的 TSO
* Pump/Drainer 异常退出，状态没有更新，对业务造成影响，可以直接使用该工具修改状态
* 同步出现故障/检查运行情况，需要查看 Pump/Drainer 的状态
* 维护集群，需要暂停/下线 Pump/Drainer

binlogctl 下载链接：

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-{version}-linux-amd64.sha256
```

对于 v2.1.0 GA 及以上版本，binlogctl 已经包含在 TiDB 的下载包中，其他版本需要单独下载 binlogctl:

```bash
wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.tar.gz
wget https://download.pingcap.org/tidb-enterprise-tools-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-enterprise-tools-latest-linux-amd64.sha256
```

binlogctl 使用说明：

命令行参数：

```bash
Usage of binlogctl:
-V
输出 binlogctl 的版本信息
-cmd string
    命令模式，包括 "generate_meta", "pumps", "drainers", "update-pump" ,"update-drainer", "pause-pump", "pause-drainer", "offline-pump", "offline-drainer"
-data-dir string
    保存 Drainer 的 checkpoint 的文件的路径 (默认 "binlog_position")
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
```

命令示例：

- 查询所有的 Pump/Drainer 的状态：

    设置 `cmd` 为 `pumps` 或者 `drainers` 来查看所有 Pump 或者 Drainer 的状态。例如：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps

    [2019/04/28 09:29:59.016 +00:00] [INFO] [nodes.go:48] ["query node"] [type=pump] [node="{NodeID: 1.1.1.1:8250, Addr: pump:8250, State: online, MaxCommitTS: 408012403141509121, UpdateTime: 2019-04-28 09:29:57 +0000 UTC}"]
    ```

- 修改 Pump/Drainer 的状态
  
    设置 `cmd` 为 `update-pump` 或者 `update-drainer` 来更新 Pump 或者 Drainer 的状态。Pump 和 Drainer 的状态可以为：online，pausing，paused，closing 以及 offline。例如：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    这条命令会修改 Pump/Drainer 保存在 PD 中的状态。

- 暂停/下线 Pump/Drainer

    分别设置 `cmd` 为 `pause-pump`、`pause-drainer`、`offline-pump`、`offline-drainer` 来暂停 Pump、暂停 Drainer、下线 Pump、下线 Drainer。例如：

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250
    ```

    binlogctl 会发送 HTTP 请求给 Pump/Drainer，Pump/Drainer 收到命令后会退出进程，并且将自己的状态设置为 paused/offline。

- 生成 Drainer 启动需要的 meta 文件

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd generate_meta

    INFO[0000] [pd] create pd client with endpoints [http://192.168.199.118:32379]
    INFO[0000] [pd] leader switches to: http://192.168.199.118:32379, previous:
    INFO[0000] [pd] init cluster id 6569368151110378289
    [2019/04/28 09:33:15.950 +00:00] [INFO] [meta.go:114] ["save meta"] [meta="commitTS: 408012454863044609"]
    ```

    该命令会生成一个文件 `{data-dir}/savepoint`，该文件中保存了 Drainer 初次启动需要的 tso 信息。
    
## 使用 TiDB SQL 管理 Pump/Drainer

目前支持通过在 TiDB 中执行 SQL 来查看/管理 binlog 相关的状态。

- 查看 TiDB 是否开启 binlog

```bash
mysql> show variables like "log_bin";
+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       |  ON   |
+---------------+-------+

```

值为 `ON` 时表示 TiDB 开启了 binlog。

- 查看 Pump/Drainer 状态

```bash
mysql> show pump status;
+--------|----------------|--------|--------------------|---------------------|
| NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+--------|----------------|--------|--------------------|---------------------|
| pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
+--------|----------------|--------|--------------------|---------------------|
| pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
+--------|----------------|--------|--------------------|---------------------|

```

```bash
mysql> show drainer status;
+----------|----------------|--------|--------------------|---------------------|
|  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
+----------|----------------|--------|--------------------|---------------------|
| drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
+----------|----------------|--------|--------------------|---------------------|
| drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
+----------|----------------|--------|--------------------|---------------------|

```

- 修改 Pump/Drainer 状态

```bach
mysql> change pump to node_state ='paused' for node_id 'pump1'";
Query OK, 0 rows affected (0.01 sec)
```

```bach
mysql> change drainer to node_state ='paused' for node_id 'drainer1'";
Query OK, 0 rows affected (0.01 sec)
```

- 注意

1. 查看 binlog 开启状态以及Pump/Drainer 状态的功能在 TiDB v2.1.7 及以上版本支持。
2. 修改 Pump/Drainer 状态的功能在 TiDB v3.0.0-rc.1 及以上版本支持。该功能只修改 PD 中存储的 Pump/Drainer 状态，如果需要暂停/下线节点，仍然需要使用 `binlogctl`。
