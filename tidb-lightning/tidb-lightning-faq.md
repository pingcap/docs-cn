---
title: TiDB Lightning 常见问题
aliases: ['/docs-cn/dev/tidb-lightning/tidb-lightning-faq/','/docs-cn/dev/faq/tidb-lightning/','/docs-cn/dev/troubleshoot-tidb-lightning/','/docs-cn/dev/how-to/troubleshoot/tidb-lightning/','/docs-cn/dev/reference/tools/error-case-handling/lightning-misuse-handling/','/docs-cn/dev/tidb-lightning/tidb-lightning-misuse-handling/','/zh/tidb/dev/troubleshoot-tidb-lightning/']
---

# TiDB Lightning 常见问题

本文列出了一些使用 TiDB Lightning 时可能会遇到的问题与解决办法。

## TiDB Lightning 对 TiDB/TiKV/PD 的最低版本要求是多少？

TiDB Lightning 的版本应与集群相同。如果使用 Local-backend 模式，最低版本要求为 4.0.0。如果使用 Importer-backend 或 TiDB-backend 模式 最低版本要求是 2.0.9，但建议使用最新的稳定版本 3.0。

## TiDB Lightning 支持导入多个库吗？

支持。

## TiDB Lightning 对下游数据库的账号权限要求是怎样的？

TiDB Lightning 需要以下权限：

* SELECT
* UPDATE
* ALTER
* CREATE
* DROP

如果选择 [TiDB-backend](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-tidb-backend) 模式，或目标数据库用于存储断点，则 TiDB Lightning 额外需要以下权限：

* INSERT
* DELETE

Local-backend 和 Importer-backend 无需以上两个权限，因为数据直接被 Ingest 到 TiKV 中，所以绕过了 TiDB 的权限系统。只要 TiKV、TiKV Importer 和 TiDB Lightning 的端口在集群之外不可访问，就可以保证安全。

如果 TiDB Lightning 配置项 `checksum = true`，则 TiDB Lightning 需要有下游 TiDB admin 用户权限。

## TiDB Lightning 在导数据过程中某个表报错了，会影响其他表吗？进程会马上退出吗？

如果只是个别表报错，不会影响整体。报错的那个表会停止处理，继续处理其他的表。

## 如何正确重启 TiDB Lightning？

如果使用 Importer-backend，根据 `tikv-importer` 的状态，重启 TiDB Lightning 的基本顺序如下：

如果 `tikv-importer` 仍在运行：

1. [结束 `tidb-lightning` 进程](#如何正确结束-tidb-lightning-进程)。
2. 执行修改操作（如修复数据源、更改设置、更换硬件等）。
3. 如果上面的修改操作更改了任何表，你还需要[清除对应的断点](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-remove)。
4. 重启 `tidb-lightning`。

如果 `tikv-importer` 需要重启：

1. [结束 `tidb-lightning` 进程](#如何正确结束-tidb-lightning-进程)。
2. [结束 `tikv-importer` 进程](#如何正确结束-tikv-importer-进程)。
3. 执行修改操作（如修复数据源、更改设置、更换硬件等）。
4. 重启 `tikv-importer`。
5. 重启 `tidb-lightning` 并等待，**直到程序因校验和错误（如果有的话）而失败**。
    * 重启 `tikv-importer` 将清除所有仍在写入的引擎文件，但是 `tidb-lightning` 并不会感知到该操作。从 v3.0 开始，最简单的方法是让 `tidb-lightning` 继续，然后再重试。
6. [清除失败的表及断点](#checkpoint-for--has-invalid-status错误码)。
7. 再次重启 `tidb-lightning`。

如果使用 Local-backend 和 TiDB-backend，操作和 Importer-backend 的 `tikv-importer` 仍在运行时相同。

## 如何校验导入的数据的正确性？

TiDB Lightning 默认会对导入数据计算校验和 (checksum)，如果校验和不一致就会停止导入该表。可以在日志看到相关的信息。

TiDB 也支持从 MySQL 命令行运行 `ADMIN CHECKSUM TABLE` 指令来计算校验和。

{{< copyable "sql" >}}

```sql
ADMIN CHECKSUM TABLE `schema`.`table`;
```

```
+---------+------------+---------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor  | Total_kvs | Total_bytes |
+---------+------------+---------------------+-----------+-------------+
| schema  | table      | 5505282386844578743 |         3 |          96 |
+---------+------------+---------------------+-----------+-------------+
1 row in set (0.01 sec)
```

## TiDB Lightning 支持哪些格式的数据源？

TiDB Lightning 只支持两种格式的数据源：

1. [Dumpling](/dumpling-overview.md) 生成的 SQL dump
2. 储存在本地文件系统的 [CSV](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md) 文件

## 我已经在下游创建好库和表了，TiDB Lightning 可以忽略建库建表操作吗？

可以。在配置文档中的 `[mydumper]` 部分将 `no-schema` 设置为 `true` 即可。`no-schema=true` 会默认下游已经创建好所需的数据库和表，如果没有创建，会报错。

## 有些不合法的数据，能否通过关掉严格 SQL 模式 (Strict SQL Mode) 来导入？

可以。TiDB Lightning 默认的 [`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html) 为 `"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`。

这个设置不允许一些非法的数值，例如 `1970-00-00` 这样的日期。可以修改配置文件 `[tidb]` 下的 `sql-mode` 值。

```toml
...
[tidb]
sql-mode = ""
...
```

## 可以启用一个 `tikv-importer`，同时有多个 `tidb-lightning` 进程导入数据吗？

只要每个 TiDB Lightning 操作的表互不相同就可以。

## 如何正确结束 `tikv-importer` 进程？

手动部署：如果 `tikv-importer` 正在前台运行，可直接按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 退出。否则，可通过 `ps aux | grep tikv-importer` 获取进程 ID，然后通过 `kill «pid»` 结束进程。

## 如何正确结束 `tidb-lightning` 进程？

根据部署方式，选择相应操作结束进程

手动部署：如果 `tidb-lightning` 正在前台运行，可直接按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 退出。否则，可通过 `ps aux | grep tidb-lightning` 获取进程 ID，然后通过 `kill -2 «pid»` 结束进程。

## `tidb-lightning` 在服务器上运行，进程莫名其妙地退出了，是怎么回事呢？

这种情况可能是启动方式不正确，导致收到 SIGHUP 信号而退出。此时 `tidb-lightning.log` 通常有如下日志：

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

不推荐在命令行中直接使用 `nohup` 启动进程，推荐[使用脚本启动 `tidb-lightning`](/tidb-lightning/deploy-tidb-lightning.md)。

另外，如果从 TiDB Lightning 的 log 的最后一条日志显示遇到的错误是 "Context canceled"，需要在日志中搜索第一条 "ERROR" 级别的日志。在这条日志之前，通常也会紧跟有一条 "got signal to exit"，表示 Lighting 是收到中断信号然后退出的。

## 为什么用过 TiDB Lightning 之后，TiDB 集群变得又慢又耗 CPU？

如果 `tidb-lightning` 异常退出，集群可能仍处于“导入模式” (import mode)，该模式不适用于生产环境。此时可执行以下命令查看当前使用的模式：

{{< copyable "shell-regular" >}}

```sh
tidb-lightning-ctl --fetch-mode
```

可执行以下命令强制切换回“普通模式” (normal mode)：

{{< copyable "shell-regular" >}}

```sh
tidb-lightning-ctl --switch-mode=normal
```

## TiDB Lightning 可以使用千兆网卡吗？

使用 TiDB Lightning 建议配置万兆网卡。**不推荐**使用千兆网卡，尤其是在部署 `tikv-importer` 的机器上。

千兆网卡的总带宽只有 120 MB/s，而且需要与整个 TiKV 集群共享。在使用 TiDB Lightning 导入时，极易用尽所有带宽，继而因 PD 无法联络集群使集群断连。为了避免这种情况，你可以在 [`tikv-importer` 的配置文件](/tidb-lightning/tidb-lightning-configuration.md#tikv-importer-配置参数)中**限制上传速度**。

```toml
[import]
# Importer 上传至 TiKV 的最大速度（字节/秒）。
# 建议将该速度设为 100 MB/s 或更小。
upload-speed-limit = "100MB"
```

## 为什么 TiDB Lightning 需要在 TiKV 集群预留这么多空间？

当使用默认的 3 副本设置时，TiDB Lightning 需要 TiKV 集群预留数据源大小 6 倍的空间。多出来的 2 倍是算上下列没储存在数据源的因素的保守估计：

- 索引会占据额外的空间
- RocksDB 的空间放大效应

## TiDB Lightning 使用过程中是否可以重启 TiKV Importer？

不能，TiKV Importer 会在内存中存储一些引擎文件，重启后，`tidb-lightning` 会因连接失败而停止。此时，你需要[清除失败的断点](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)，因为这些 TiKV Importer 特有的信息丢失了。你可以在之后[重启 TiDB Lightning](#如何正确重启-tidb-lightning)。

## 如何清除所有与 TiDB Lightning 相关的中间数据？

1. 删除断点文件。

    {{< copyable "shell-regular" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    如果出于某些原因而无法运行该命令，你可以尝试手动删除 `/tmp/tidb_lightning_checkpoint.pb` 文件。

2. 如果使用 Local-backend，删除配置中 `sorted-kv-dir` 对应的目录；如果使用 Importer-backend，删除 `tikv-importer` 所在机器上的整个 `import` 文件目录。

3. 如果需要的话，删除 TiDB 集群上创建的所有表和库。

## TiDB Lightning 报错 `could not find first pair, this shouldn't happen`

报错原因是遍历本地排序的文件时出现异常，可能在 TiDB Lightning 打开的文件数量超过系统的上限时发生报错。在 Linux 系统中，可以使用 `ulimit -n` 命令确认此值是否过小。建议在导入期间将此设置调整为 `1000000`（即 `ulimit -n 1000000`）。

## TiDB Lightning 导入速度太慢

TiDB Lightning 的正常速度为每条线程每 2 分钟导入一个 256 MB 的数据文件，如果速度远慢于这个数值就是有问题。导入的速度可以检查日志提及 `restore chunk … takes` 的记录，或者观察 Grafana 的监控信息。

导入速度太慢一般有几个原因：

**原因 1**：`region-concurrency` 设定太高，线程间争用资源反而减低了效率。

1. 从日志的开头搜寻 `region-concurrency` 能知道 TiDB Lightning 读到的参数是多少。
2. 如果 TiDB Lightning 与其他服务（如 TiKV Importer）共用一台服务器，必需**手动**将 `region-concurrency` 设为该服务器 CPU 数量的 75%。
3. 如果 CPU 设有限额（例如从 Kubernetes 指定的上限），TiDB Lightning 可能无法自动判断出来，此时亦需要**手动**调整 `region-concurrency`。

**原因 2**：表结构太复杂。

每条索引都会额外增加键值对。如果有 N 条索引，实际导入的大小就差不多是 Dumpling 文件的 N+1 倍。如果索引不太重要，可以考虑先从 schema 去掉，待导入完成后再使用 `CREATE INDEX` 加回去。

**原因 3**: 单个文件过大。

把源数据分割为单个大小约为 256 MB 的多个文件时，TiDB Lightning 会并行处理数据，达到最佳效果。如果导入的单个文件过大，TiDB Lightning 可能无响应。

如果源数据是 CSV 格式文件，并且所有的 CSV 文件内都不存在包含字符换行符的字段 (U+000A 及 U+000D)，则可以启用 `strict-format`，TiDB Lightning 会自动分割大文件。

```toml
[mydumper]
strict-format = true
```

**原因 4**：TiDB Lightning 版本太旧。

试试最新的版本吧！可能会有改善。

## `checksum failed: checksum mismatched remote vs local`

**原因**：本地数据源跟目标数据库某个表的校验和不一致。这通常有更深层的原因：

1. 这张表可能本身已有数据，影响最终结果。
2. 如果目标数据库的校验和全是 0，表示没有发生任何导入，有可能是集群太忙无法接收任何数据。
3. 如果数据源是由机器生成而不是从 Dumpling 备份的，需确保数据符合表的限制，例如：

    * 自增 (AUTO_INCREMENT) 的列需要为正数，不能为 0。
    * 唯一键和主键 (UNIQUE and PRIMARY KEYs) 不能有重复的值。
4. 如果 TiDB Lightning 之前失败停机过，但没有正确重启，可能会因为数据不同步而出现校验和不一致。

**解决办法**：

1. 使用 `tidb-lightning-ctl` 把出错的表删除，然后重启 TiDB Lightning 重新导入那些表。

    {{< copyable "shell-regular" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

2. 把断点存放在外部数据库（修改 `[checkpoint] dsn`），减轻目标集群压力。

3. 参考[如何正确重启 TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#如何正确重启-tidb-lightning)中的解决办法。

## `Checkpoint for … has invalid status:`（错误码）

**原因**：[断点续传](/tidb-lightning/tidb-lightning-checkpoints.md)已启用。TiDB Lightning 或 TiKV Importer 之前发生了异常退出。为了防止数据意外损坏，TiDB Lightning 在错误解决以前不会启动。

错误码是小于 25 的整数，可能的取值是 0、3、6、9、12、14、15、17、18、20、21。整数越大，表示异常退出所发生的步骤在导入流程中越晚。

**解决办法**：

如果错误原因是非法数据源，使用 `tidb-lightning-ctl` 删除已导入数据，并重启 TiDB Lightning。

{{< copyable "shell-regular" >}}

```sh
tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
```

其他解决方法请参考[断点续传的控制](/tidb-lightning/tidb-lightning-checkpoints.md#断点续传的控制)。

## `ResourceTemporarilyUnavailable("Too many open engines …: …")`

**原因**：并行打开的引擎文件 (engine files) 超出 `tikv-importer` 里的限制。这可能由配置错误引起。即使配置没问题，如果 `tidb-lightning` 曾经异常退出，也有可能令引擎文件残留在打开的状态，占据可用的数量。

**解决办法**：

1. 提高 `tikv-importer.toml` 内 `max-open-engines` 的值。这个设置主要由内存决定，计算公式为：

    最大内存使用量 ≈ `max-open-engines` × `write-buffer-size` × `max-write-buffer-number`

2. 降低 `table-concurrency` + `index-concurrency`，使之低于 `max-open-engines`。

3. 重启 `tikv-importer` 来强制移除所有引擎文件 (默认值为 `./data.import/`)。这样也会丢弃导入了一半的表，所以启动 TiDB Lightning 前必须清除过期的断点记录：

    {{< copyable "shell-regular" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

## `cannot guess encoding for input file, please convert to UTF-8 manually`

**原因**：TiDB Lightning 只支持 UTF-8 和 GB-18030 编码的表架构。此错误代表数据源不是这里任一个编码。也有可能是文件中混合了不同的编码，例如，因为在不同的环境运行过 `ALTER TABLE`，使表架构同时出现 UTF-8 和 GB-18030 的字符。

**解决办法**：

1. 编辑数据源，保存为纯 UTF-8 或 GB-18030 的文件。
2. 手动在目标数量库创建所有的表，然后设置 `[mydumper] no-schema = true` 跳过创建表的步骤。
3. 设置 `[mydumper] character-set = "binary"` 跳过这个检查。但是这样可能使数据库出现乱码。

## [sql2kv] sql encode error = [types:1292]invalid time format: '{1970 1 1 …}'

**原因**: 一个 `timestamp` 类型的时间戳记录了不存在的时间值。时间值不存在是由于夏时制切换或超出支持的范围（1970 年 1 月 1 日至 2038 年 1 月 19 日）。

**解决办法**:

1. 确保 TiDB Lightning 与数据源时区一致。

    * 手动部署的话，通过设定 `$TZ` 环境变量强制时区设定。

        强制使用 Asia/Shanghai 时区：

        {{< copyable "shell-regular" >}}

        ```sh
        TZ='Asia/Shanghai' bin/tidb-lightning -config tidb-lightning.toml
        ```

2. 导出数据时，必须加上 `--skip-tz-utc` 选项。

3. 确保整个集群使用的是同一最新版本的 `tzdata` (2018i 或更高版本)。

    如果你使用的是 CentOS 机器，你可以运行 `yum info tzdata` 命令查看 `tzdata` 的版本及是否有更新。然后运行 `yum upgrade tzdata` 命令升级 `tzdata`。

## `[Error 8025: entry too large, the max entry size is 6291456]`

**原因**：TiDB Lightning 生成的单行 KV 超过了 TiDB 的限制。

**解决办法**:

目前无法绕过 TiDB 的限制，只能忽略这张表，确保其它表顺利导入。

## switch-mode 时遇到 `rpc error: code = Unimplemented ...`

**原因**：集群中有不支持 switch-mode 的节点。目前已知的组件中，4.0.0-rc.2 之前的 TiFlash [不支持 switch-mode 操作](https://github.com/pingcap/tidb-lightning/issues/273)。

**解决办法**：

- 如果集群中有 TiFlash 节点，可以将集群更新到 4.0.0-rc.2 或更新版本。
- 如果不方便升级，可以临时禁用 TiFlash。

## `tidb lightning encountered error: TiDB version too old, expected '>=4.0.0', found '3.0.18'`

TiDB Lightning Local-backend 只支持导入到 v4.0.0 及以上版本的 TiDB 集群。如果尝试使用 Local-backend 导入到 v2.x 或 v3.x 的集群，就会报以上错误。此时可以修改配置使用 Importer-backend 或 TiDB-backend 进行导入。

部分 `nightly` 版本的 TiDB 集群的版本可能类似 4.0.0-beta.2。这种版本的 TiDB Lightning 实际支持 Local-backend，如果使用 `nightly` 版本遇到该报错，可以通过设置配置  `check-requirements = false` 跳过版本检查。在设置此参数之前，请确保 TiDB Lightning 的配置支持对应的版本，否则无法保证导入成功。

## `restore table test.district failed: unknown columns in header [...]`

出现该错误通常是因为 CSV 格式的数据文件不包含 header（第一行也是数据），因此需要在 TiDB Lightning 的配置文件中增加如下配置项：

```
[mydumper.csv]
header = false
```

## 如何获取 TiDB Lightning 运行时的 goroutine 信息

1. 如果配置文件中已经指定了 [status-port](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-全局配置)，可以跳过此步骤。否则，需要向 TiDB Lightning 发送 USR1 信号开启 status-port。

   首先通过 `ps` 等命令获取 TiDB Lightning 的进程 ID（PID），然后运行如下命令

   {{< copyable "shell-regular" >}}

   ```sh
   kill -USR1 <lightning-pid>
   ```
   
   查看 TiDB Lightning 的日志，其中有“starting HTTP server / start HTTP server / started HTTP server”的日志显示了新开启的 status-port。

2. 访问 `http://<lightning-ip>:<status-port>/debug/pprof/goroutine?debug=2` 返回 goroutine 信息。
