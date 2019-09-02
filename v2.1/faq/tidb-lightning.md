---
title: TiDB Lightning 常见问题
category: FAQ
---

# TiDB Lightning 常见问题

## TiDB Lightning 对 TiDB/TiKV/PD 的最低版本要求是多少？

最低版本要求是 2.0.9。

## TiDB Lightning 支持导入多个库吗？

支持。

## TiDB Lightning 对下游数据库的账号权限要求是怎样的？

TiDB Lightning 需要以下权限：

* SELECT
* UPDATE
* ALTER
* CREATE
* DROP

存储断点的数据库额外需要以下权限：

* INSERT
* DELETE

如果 TiDB Lightning 配置项 `checksum = true`，则 TiDB Lightning 需要有下游 TiDB admin 用户权限。

## TiDB Lightning 在导数据过程中某个表报错了，会影响其他表吗？进程会马上退出吗？

如果只是个别表报错，不会影响整体。报错的那个表会停止处理，继续处理其他的表。

## 如何校验导入的数据的正确性？

TiDB Lightning 默认会对导入数据计算校验和 (checksum)，如果校验和不一致就会停止导入该表。可以在日志看到相关的信息。

TiDB 也支持从 MySQL 命令行运行 `ADMIN CHECKSUM TABLE` 指令来计算校验和。

```text
mysql> ADMIN CHECKSUM TABLE `schema`.`table`;
+---------+------------+---------------------+-----------+-------------+
| Db_name | Table_name | Checksum_crc64_xor  | Total_kvs | Total_bytes |
+---------+------------+---------------------+-----------+-------------+
| schema  | table      | 5505282386844578743 |         3 |          96 |
+---------+------------+---------------------+-----------+-------------+
1 row in set (0.01 sec)
```

## TiDB Lightning 支持哪些格式的数据源？

到 v2.1.6 版本为止，只支持本地文档形式的数据源，支持 [Mydumper](v2.1/reference/tools/mydumper.md) 或 [CSV](v2.1/reference/tools/tidb-lightning/csv.md) 格式。

## 我已经在下游创建好库和表了，Lightning 可以忽略建库建表操作吗？

可以。在配置文档中的 `[mydumper]` 将 `no-schema` 设置为 `true` 即可。`no-schema=true` 会默认下游已经创建好所需的数据库和表，如果没有创建，会报错。

## 有些不合法的数据，能否通过关掉严格 SQL 模式 (Strict SQL MOde) 来导入？

可以。Lightning 默认的 [`sql_mode`](https://dev.mysql.com/doc/refman/5.7/en/sql-mode.html) 为 `"STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION"`。

这个设置不允许一些非法的数值，例如 `1970-00-00` 这样的日期。可以修改配置文件 `[tidb]` 下的 `sql-mode` 值。

```toml
...
[tidb]
sql-mode = ""
...
```

## 可以起一个 `tikv-importer`，同时有多个 `tidb-lightning` 进程导入数据吗？

只要每个 Lightning 操作的表互不相同就可以。

## 如何正确关闭 `tikv-importer` 进程？

如使用 TiDB Ansible 部署，在 Importer 的服务器上运行 `scripts/stop_importer.sh` 即可。否则，可通过 `ps aux | grep tikv-importer` 获取进程ID，然后 `kill «pid»`。

## 如何正确关闭 `tidb-lightning` 进程？

如使用 TiDB Ansible 部署，在 Lightning 的服务器上运行 `scripts/stop_lightning.sh` 即可。

如果 `tidb-lightning` 正在前台运行，可直接按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 退出。

否则，可通过 `ps aux | grep tidb-lightning` 获取进程 ID，然后 `kill -2 «pid»`。

## 进程在服务器上运行，进程莫名其妙地就退出了，是怎么回事呢？

这种情况可能是启动方式不正确，导致因为收到 SIGHUP 信号而退出，此时 `tidb-lightning.log` 通常有这幺一行日志：

```
2018/08/10 07:29:08.310 main.go:47: [info] Got signal hangup to exit.
```

不推荐直接在命令行中使用 `nohup` 启动进程，而应该把 `nohup` 这行命令放到一个脚本中运行。

## 为什么用过 TiDB Lightning 之后，TiDB 集群变得又慢又耗 CPU？

如果 `tidb-lightning` 曾经异常退出，集群可能仍留在“导入模式” (import mode)，不适合在生产环境工作。此时需要强制切换回“普通模式” (normal mode)：

```sh
tidb-lightning-ctl --switch-mode=normal
```

## TiDB Lightning 可以使用千兆网卡吗？

使用 TiDB Lightning 必须配置万兆网卡。**不能使用**千兆网卡，尤其是在部署 `tikv-importer` 的机器上。千兆网卡的总带宽只有 120 MB/s，而且需要与整个 TiKV 集群共享。在使用 TiDB Lightning 导入时，极易用尽所有带宽，继而因 PD 无法联络集群使集群断连。

## 为什么 TiDB Lightning 需要在 TiKV 集群预留这么多空间？

当使用默认的 3 副本设置时，TiDB Lightning 需要 TiKV 集群预留数据源大小 6 倍的空间。多出来的 2 倍是算上下列没储存在数据源的因素的保守估计：

- 索引会占据额外的空间
- RocksDB 的空间放大效应

## TiDB Lightning 使用过程中是否可以重启 TiKV Importer？

不能，Importer 会保存一些 Engine 的信息在内存中，Importer 重启后，Lightning 必须重启。
