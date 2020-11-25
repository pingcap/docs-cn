---
title: Backup & Restore 常见问题
summary: BR 相关的常见问题以及解决方法。
aliases: ['/docs-cn/stable/br/backup-and-restore-faq/','/docs-cn/v4.0/br/backup-and-restore-faq/']
---
 
# Backup & Restore 常见问题
 
本文列出了在使用 Backup & Restore (BR) 时，可能会遇到的问题及相应的解决方法。
 
如果遇到未包含在此文档且无法解决的问题，可以在 [AskTUG](http://asktug.com) 社区中提问。

## 恢复的时候，报错 `could not read local://...:download sst failed`，该如何处理？

在恢复的时候，每个节点都必须能够访问到**所有**的备份文件（SST files），默认情况下，假如使用 local storage，备份文件会分散在各个节点中，此时是无法直接恢复的，必须将每个 TiKV 节点的备份文件拷贝到其它所有 TiKV 节点才能恢复。
 
建议在备份的时候挂载一块 NFS 网盘作为备份盘，详见[将单表数据备份到网络盘](/br/backup-and-restore-use-cases.md#将单表数据备份到网络盘推荐)。
 
## BR 备份时，对集群影响多大？
 
使用 `sysbench` 的 `oltp_read_only` 场景全速备份到非服务盘，对集群的影响依照表结构的不同，对集群 QPS 的影响在 15%~25% 之间。
 
如果需要控制备份带来的影响，可以使用 `--ratelimit` 参数限速。
 
## BR 会备份系统表吗？在数据恢复的时候，这些系统表会冲突吗？
 
全量备份的时候会过滤掉系统库（`information_schema`，`performance_schema`，`mysql`）。参考[备份原理](/br/backup-and-restore-tool.md#工作原理)。

因为这些系统库根本不可能存在于备份中，恢复的时候自然不可能发生冲突。
 
## BR 遇到 Permission denied 错误，即使用 root 运行 BR 也无法解决，该如何处理？
 
需要确认 TiKV 是否有访问备份目录的权限。如果是备份，确认是否有写权限；如果是恢复，确认是否有读权限。

在进行备份操作时，如果使用本地磁盘或 NFS 作为存储介质，请确保执行 BR 的用户和启动 TiKV 的用户相同（如果 BR 和 TiKV 位于不同的机器，则需要用户的 UID 相同），否则很备份可能会出现该问题。

使用 root 运行 BR 仍旧有可能会因为磁盘权限而失败，因为备份文件 (SST) 的保存是由 TiKV 执行的。
 
> **注意：**
>
> 在恢复的时候也可能遇到同样的问题。
> 
> 使用 BR 进行数据的恢复时，检验读权限的时机是在第一次读取 SST 文件时，考虑到执行 DDL 的耗时，这个时刻可能会离开始运行 BR 的时间很远。这样可能会出现等了很长时间之后遇到 Permission denied 错误失败的情况。
> 
> 因此，最好在恢复前提前检查权限。
 
## BR 遇到错误信息 `Io(Os...)`，该如何处理？
 
这类问题几乎都是 TiKV 在写盘的时候遇到的系统调用错误。检查备份目录的挂载方式和文件系统，试试看备份到其它文件夹或者其它硬盘。
 
目前已知备份到 samba 搭建的网盘时可能会遇到 `Code: 22(invalid argument)` 错误。
 
## BR 遇到错误信息 `rpc error: code = Unavailable desc =...`，该如何处理？
 
该问题一般是因为使用 BR 恢复数据的时候，恢复集群的性能不足导致的。可以从恢复集群的监控或者 TiKV 日志来辅助确认。

要解决这类问题，可以尝试扩大集群资源，以及调小恢复时的并发度 (concurrency)，打开限速 (ratelimit) 设置。
 
## 使用 local storage 的时候，BR 备份的文件会存在哪里？
 
在使用 local storage 的时候，会在运行 BR 的节点生成 `backupmeta`，在各个 Region 的 Leader 节点生成备份文件。
 
## 备份数据有多大，备份会有副本吗？
 
备份的时候仅仅在每个 Region 的 Leader 处生成该 Region 的备份文件。因此备份的大小等于数据大小，不会有多余的副本数据。所以最终的总大小大约是 TiKV 数据总量除以副本数。
 
但是假如想要从本地恢复数据，因为每个 TiKV 都必须要能访问到所有备份文件，在最终恢复的时候会有等同于恢复时 TiKV 节点数量的副本。

## BR 恢复到 TiCDC / Drainer 的上游集群时，要注意些什么？

+ **BR 恢复的数据无法被同步到下游**，因为 BR 直接导入 SST 文件，而下游集群目前没有办法获得上游的 SST 文件。

+ 在 4.0.3 版本之前，BR 恢复时产生的 DDL jobs 还可能会让 TiCDC / Drainer 执行异常的 DDL。所以，如果一定要在 TiCDC / Drainer 的上游集群执行恢复，请将 BR 恢复的所有表加入 TiCDC / Drainer 的阻止名单。

TiCDC 可以通过配置项中的 [`filter.rules`](https://github.com/pingcap/ticdc/blob/7c3c2336f98153326912f3cf6ea2fbb7bcc4a20c/cmd/changefeed.toml#L16) 项完成，Drainer 则可以通过 [`syncer.ignore-table`](/tidb-binlog/tidb-binlog-configuration-file.md#ignore-table) 完成。
