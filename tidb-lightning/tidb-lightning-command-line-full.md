---
title: TiDB Lightning 命令行参数
summary: 使用命令行配置 TiDB Lightning。
---

# TiDB Lightning 命令行参数

你可以使用配置文件或命令行配置 TiDB Lightning。本文主要介绍 TiDB Lightning 的命令行参数。

## 命令行参数

### `tidb-lightning`

使用 `tidb-lightning` 可以对下列参数进行配置：

| 参数 | 描述 | 对应配置项 |
|:----|:----|:----|
| --config *file* | 从 *file* 读取全局设置。如果没有指定则使用默认设置。 | |
| -V | 输出程序的版本 | |
| -d *directory* | 读取数据的本地目录或[外部存储服务的 URI 格式](/external-storage-uri.md) | `mydumper.data-source-dir` |
| -L *level* | 日志的等级： debug、info、warn、error 或 fatal (默认为 info) | `lightning.log-level` |
| -f *rule* | [表库过滤的规则](/table-filter.md) (可多次指定) | `mydumper.filter` |
| --backend [*backend*](/tidb-lightning/tidb-lightning-overview.md) | 选择导入的模式：`local` 为[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)，`tidb` 为[逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md) | `tikv-importer.backend` |
| --log-file *file* | 日志文件路径（默认值为 `/tmp/lightning.log.{timestamp}`，设置为 '-' 表示日志输出到终端） | `lightning.log-file` |
| --status-addr *ip:port* | TiDB Lightning 服务器的监听地址 | `lightning.status-port` |
| --pd-urls *host1:port1,host2:port2,...,hostn:portn* | PD endpoint 的地址。从 v7.6.0 开始支持设置多个地址。 | `tidb.pd-addr` |
| --tidb-host *host* | TiDB Server 的 host | `tidb.host` |
| --tidb-port *port* | TiDB Server 的端口（默认为 4000） | `tidb.port` |
| --tidb-status *port* | TiDB Server 的状态端口的（默认为 10080） | `tidb.status-port` |
| --tidb-user *user* | 连接到 TiDB 的用户名 | `tidb.user` |
| --tidb-password *password* | 连接到 TiDB 的密码，可为明文或 Base64 编码 | `tidb.password` |
| --enable-checkpoint *bool* | 是否启用断点 (默认值为 true) | `checkpoint.enable` |
| --analyze *level* | 导入后分析表信息，可选值为 required、optional（默认值）、off | `post-restore.analyze` |
| --checksum *level* | 导入后比较校验和，可选值为 required（默认值）、optional、off | `post-restore.checksum` |
| --check-requirements *bool* | 任务开始之前检查集群版本兼容性，以及运行过程中检查 TiKV 的可用存储空间是否大于 10%（默认值为 true）| `lightning.check-requirements` |
| --ca *file* | TLS 连接的 CA 证书路径 | `security.ca-path` |
| --cert *file* | TLS 连接的证书路径 | `security.cert-path` |
| --key *file* | TLS 连接的私钥路径 | `security.key-path` |
| --server-mode | 在服务器模式下启动 TiDB Lightning | `lightning.server-mode` |

如果同时对命令行参数和配置文件中的对应参数进行更改，命令行参数将优先生效。例如，在 `cfg.toml` 文件中，不管对日志等级做出什么修改，运行 `tiup tidb-lightning -L debug --config cfg.toml` 命令总是将日志级别设置为 “debug”。

### `tidb-lightning-ctl`

所有 `tidb-lightning` 的参数也适用于 `tidb-lightning-ctl`。此外，使用 `tidb-lightning-ctl` 还可以对下列参数进行配置：

| 参数 | 描述 |
|:----|:----------|
| --compact | 执行 full compact |
| --switch-mode *mode* | 将每个 TiKV Store 切换到指定模式（normal 或 import） |
| --fetch-mode | 打印每个 TiKV Store 的当前模式 |
| --import-engine *uuid* | 将 TiKV Importer 上关闭的引擎文件导入到 TiKV 集群 |
| --cleanup-engine *uuid* | 删除 TiKV Importer 上的引擎文件 |
| --checkpoint-dump *folder* | 将当前的断点以 CSV 格式存储到文件夹中 |
| --checkpoint-error-destroy *tablename* | 删除断点，如果报错则删除该表 |
| --checkpoint-error-ignore *tablename* | 忽略指定表中断点的报错 |
| --checkpoint-remove *tablename* | 无条件删除表的断点 |

*tablename* 必须是`` `db`.`tbl` `` 中的限定表名（包括反引号），或关键词 `all`。
