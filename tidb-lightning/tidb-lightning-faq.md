---
title: TiDB Lightning 常见问题
aliases: ['/docs-cn/stable/tidb-lightning/tidb-lightning-faq/','/docs-cn/v4.0/tidb-lightning/tidb-lightning-faq/','/docs-cn/stable/faq/tidb-lightning/']
---

# TiDB Lightning 常见问题

本文列出了一些使用 TiDB Lightning 时可能会遇到的问题与解决办法。

>**注意：**
>
> 使用 TiDB Lightning 的过程中如遇错误，参考 [TiDB Lightning 故障诊断](/troubleshoot-tidb-lightning.md)进行排查。

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

根据 `tikv-importer` 的状态，重启 TiDB Lightning 的基本顺序如下：

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
6. [清除失败的表及断点](/troubleshoot-tidb-lightning.md#checkpoint-for--has-invalid-status错误码)。
7. 再次重启 `tidb-lightning`。

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

可以。Lightning 默认的 [`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html) 为 `"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`。

这个设置不允许一些非法的数值，例如 `1970-00-00` 这样的日期。可以修改配置文件 `[tidb]` 下的 `sql-mode` 值。

```toml
...
[tidb]
sql-mode = ""
...
```

## 可以启用一个 `tikv-importer`，同时有多个 `tidb-lightning` 进程导入数据吗？

只要每个 Lightning 操作的表互不相同就可以。

## 如何正确结束 `tikv-importer` 进程？

根据部署方式，选择相应操作结束进程

- 使用 TiDB Ansible 部署：在 Importer 的服务器上运行 `scripts/stop_importer.sh`。

- 手动部署：如果 `tikv-importer` 正在前台运行，可直接按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 退出。否则，可通过 `ps aux | grep tikv-importer` 获取进程 ID，然后通过 `kill «pid»` 结束进程。

## 如何正确结束 `tidb-lightning` 进程？

根据部署方式，选择相应操作结束进程

- 使用 TiDB Ansible 部署：在 Lightning 的服务器上运行 `scripts/stop_lightning.sh`。

- 手动部署：如果 `tidb-lightning` 正在前台运行，可直接按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 退出。否则，可通过 `ps aux | grep tidb-lightning` 获取进程 ID，然后通过 `kill -2 «pid»` 结束进程。

## `tidb-lightning` 在服务器上运行，进程莫名其妙地退出了，是怎么回事呢？

这种情况可能是启动方式不正确，导致收到 SIGHUP 信号而退出。此时 `tidb-lightning.log` 通常有如下日志：

```
[2018/08/10 07:29:08.310 +08:00] [INFO] [main.go:41] ["got signal to exit"] [signal=hangup]
```

不推荐在命令行中直接使用 `nohup` 启动进程，推荐[使用脚本启动 `tidb-lightning`](/tidb-lightning/deploy-tidb-lightning.md)。

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

不能，Importer 会在内存中存储一些引擎文件，Importer 重启后，`tidb-lightning` 会因连接失败而停止。此时，你需要[清除失败的断点](/tidb-lightning/tidb-lightning-checkpoints.md#--checkpoint-error-destroy)，因为这些 Importer 特有的信息丢失了。你可以在之后[重启 Lightning](#如何正确重启-tidb-lightning)。

## 如何清除所有与 TiDB Lightning 相关的中间数据？

1. 删除断点文件。

    {{< copyable "shell-regular" >}}

    ```sh
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-remove=all
    ```

    如果出于某些原因而无法运行该命令，你可以尝试手动删除 `/tmp/tidb_lightning_checkpoint.pb` 文件。

2. 删除 `tikv-importer` 所在机器上的整个 “import” 文件目录。

3. 如果需要的话，删除 TiDB 集群上创建的所有表和库。
