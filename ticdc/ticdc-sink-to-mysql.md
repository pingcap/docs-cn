---
title: 同步数据到 MySQL 兼容数据库
summary: 了解如何使用 TiCDC 将数据同步到 TiDB 或 MySQL
---

# 同步数据到 MySQL 兼容数据库

本文介绍如何使用 TiCDC 创建一个将增量数据复制到下游 TiDB 数据库，或其他兼容 MySQL 协议数据库的 Changefeed。同时介绍了如何使用 TiCDC 灾难场景的最终一致性复制功能。

## 创建同步任务，复制增量数据到 MySQL 兼容数据库

使用以下命令来创建同步任务：

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="mysql://root:123456@127.0.0.1:3306/" \
    --changefeed-id="simple-replication-task"
```

```shell
Create changefeed successfully!
ID: simple-replication-task
Info: {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2023-12-07T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"sort-engine":"unified","sort-dir":".","config":{"case-sensitive":false,"filter":{"rules":["*.*"],"ignore-txn-start-ts":null,"ddl-allow-list":null},"mounter":{"worker-num":16},"sink":{"dispatchers":null},"scheduler":{"type":"table-number","polling-time":-1}},"state":"normal","history":null,"error":null}
```

- `--server`：TiCDC 集群中任意一个 TiCDC 服务器的地址。
- `--changefeed-id`：同步任务的 ID，格式需要符合正则表达式 `^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`。如果不指定该 ID，TiCDC 会自动生成一个 UUID（version 4 格式）作为 ID。
- `--sink-uri`：同步任务下游的地址，详见 [Sink URI 配置 `mysql`/`tidb`](#sink-uri-配置-mysqltidb)。
- `--start-ts`：指定 changefeed 的开始 TSO。TiCDC 集群将从这个 TSO 开始拉取数据。默认为当前时间。
- `--target-ts`：指定 changefeed 的目标 TSO。TiCDC 集群拉取数据直到这个 TSO 停止。默认为空，即 TiCDC 不会自动停止。
- `--config`：指定 changefeed 配置文件，详见：[TiCDC Changefeed 配置参数](/ticdc/ticdc-changefeed-config.md)。

> **注意：**
>
> TiCDC 工具只负责复制增量数据，需要使用 Dumpling/TiDB Lightning 工具或者 BR 工具进行全量数据的初始化。
> 经过全量数据的初始化后，需要将 `start-ts` 指定为上游备份时的 TSO。例如：Dumpling 目录下 metadata 文件中的 pos 值，或者 BR 备份完成后输出日志中的 `backupTS`。

## Sink URI 配置 `mysql`/`tidb`

Sink URI 用于指定 TiCDC 目标系统的连接信息，遵循以下格式：

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

> **注意：**
>
> `/path` 不适用于 MySQL sink。

一个通用的配置样例如下所示：

```shell
--sink-uri="mysql://root:123456@127.0.0.1:3306"
```

URI 中可配置的参数如下：

| 参数         | 描述                                             |
| :------------ | :------------------------------------------------ |
| `root`        | 下游数据库的用户名。                             |
| `123456`       | 下游数据库密码。（可采用 Base64 进行编码）                                     |
| `127.0.0.1`    | 下游数据库的 IP。                                |
| `3306`         | 下游数据的连接端口。                                 |
| `worker-count` | 向下游执行 SQL 的并发度（可选，默认值为 `16`）。       |
| `max-txn-row`  | 向下游执行 SQL 的 batch 大小（可选，默认值为 `256`）。 |
| `ssl-ca`       | 连接下游 MySQL 实例所需的 CA 证书文件路径（可选）。 |
| `ssl-cert`     | 连接下游 MySQL 实例所需的证书文件路径（可选）。 |
| `ssl-key`      | 连接下游 MySQL 实例所需的证书密钥文件路径（可选）。 |
| `time-zone`    | 连接下游 MySQL 实例时使用的时区名称，从 v4.0.8 开始生效。（可选。如果不指定该参数，使用 TiCDC 服务进程的时区；如果指定该参数但使用空值，例如：`time-zone=""`，则表示连接 MySQL 时不指定时区，使用下游默认时区）。 |
| `transaction-atomicity`      | 指定事务的原子性级别（可选，默认值为 `none`）。当该值为 `table` 时 TiCDC 保证单表事务的原子性，当该值为 `none` 时 TiCDC 会拆分单表事务。 |
| `safe-mode` | 指定向下游同步数据时 `INSERT` 和 `UPDATE` 语句的处理方式。当设置为 `true` 时，TiCDC 会将上游所有的 `INSERT` 语句转换为 `REPLACE INTO` 语句，所有的 `UPDATE` 语句转换为 `DELETE` + `REPLACE INTO` 语句。在 v6.1.3 版本之前，该参数的默认值为 `true`。从 v6.1.3 版本开始，该参数的默认值调整为 `false`，TiCDC 在启动时会获取一个当前时间戳 `ThresholdTs`，对于 `CommitTs` 小于 `ThresholdTs` 的 `INSERT` 语句和 `UPDATE` 语句，TiCDC 会分别将其转换为 `REPLACE INTO` 语句和 `DELETE` + `REPLACE INTO` 语句。对于 `CommitTs` 大于等于 `ThresholdTs` 的 `INSERT` 语句和 `UPDATE` 语句，`INSERT` 语句将直接同步到下游，`UPDATE` 语句的具体行为则参考 [TiCDC 拆分 UPDATE 事件行为说明](/ticdc/ticdc-split-update-behavior.md)。 |

若需要对 Sink URI 中的数据库密码使用 Base64 进行编码，可以参考如下命令：

```shell
echo -n '123456' | base64   # 假设待编码的密码为 123456
```

编码后的密码如下：

```shell
MTIzNDU2
```

> **注意：**
>
> 当 Sink URI 中包含特殊字符时，如 `! * ' ( ) ; : @ & = + $ , / ? % # [ ]`，需要对 URI 特殊字符进行转义处理。你可以使用 [URI Encoder](https://meyerweb.com/eric/tools/dencoder/) 工具对 URI 进行转义。

## 灾难场景的最终一致性复制

从 v6.1.1 版本开始容灾场景下的最终一致性复制功能 GA。TiCDC 支持将上游 TiDB 的增量数据备份到下游集群的 S3 存储或 NFS 文件系统。当上游集群出现了灾难，完全无法使用时，TiCDC 可以将下游集群恢复到最近的一致状态，即提供灾备场景的最终一致性复制能力，确保应用可以快速切换到下游集群，避免数据库长时间不可用，提高业务连续性。

目前，TiCDC 支持将 TiDB 集群的增量数据复制到 TiDB 或兼容 MySQL 的数据库系统（包括 Aurora、MySQL 和 MariaDB）。当上游发生灾难时，如果 TiCDC 正常运行且上游 TiDB 集群没有出现数据复制延迟大幅度增加的情况，下游集群可以在 5 分钟之内恢复集群，并且最多丢失出现问题前 10 秒钟的数据，即 RTO <= 5 mins, P95 RPO <= 10s。

当上游 TiDB 集群出现以下情况时，会导致 TiCDC 延迟上升，进而影响 RPO：

- TPS 短时间内大幅度上升
- 上游出现大事务或者长事务
- Reload 或 Upgrade 上游 TiKV 集群或 TiCDC 集群
- 执行耗时很长的 DDL 语句，例如：add index
- 使用过于激进的 PD 调度策略，导致频繁 region leader 迁移或 region merge/split

### 使用前提

- 准备好具有高可用的 S3 存储或 NFS 系统，用于存储 TiCDC 的实时增量数据备份文件，在上游发生灾难情况下该文件存储可以访问。
- TiCDC 对需要具备灾难场景最终一致性的 changefeed 开启该功能，开启方式是在 changefeed 配置文件中增加以下配置：

```toml
[consistent]
# 一致性级别，选项有：
# - none： 默认值，非灾难场景，只有在任务指定 finished-ts 情况下保证最终一致性。
# - eventual： 使用 redo log，提供上游灾难情况下的最终一致性。
level = "eventual"

# 单个 redo log 文件大小，单位 MiB，默认值 64，建议该值不超过 128。
max-log-size = 64

# 刷新或上传 redo log 至 S3 的间隔，单位毫秒，建议该参数 >= 2000。
flush-interval = 2000

# 存储 redo log 的形式，包括 nfs（NFS 目录），S3（上传至S3）
storage = "s3://logbucket/test-changefeed?endpoint=http://$S3_ENDPOINT/"
```

### 灾难恢复

当上游发生灾难后，需要通过 `cdc redo` 命令在下游手动恢复。恢复流程如下：

1. 确保 TiCDC 进程已经退出，防止在数据恢复过程中上游恢复服务，TiCDC 重新开始同步数据。
2. 使用 cdc binary 进行数据恢复，具体命令如下：

```shell
cdc redo apply --tmp-dir="/tmp/cdc/redo/apply" \
    --storage="s3://logbucket/test-changefeed?endpoint=http://10.0.10.25:24927/" \
    --sink-uri="mysql://normal:123456@10.0.10.55:3306/"
```

以上命令中：

- `tmp-dir`：指定用于下载 TiCDC 增量数据备份文件的临时目录。
- `storage`：指定存储 TiCDC 增量数据备份文件的地址，为 S3 或者 NFS 目录。
- `sink-uri`：数据恢复的目标地址。scheme 仅支持 `mysql`。
