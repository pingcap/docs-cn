---
title: BR 常见问题解答
summary: BR FAQ & troubleshooting
category: FAQ
---
 
# BR 常见问题解答
 
本文是 BR 的 FAQ，记录了一些在 BR 中的常见问题和解答。
 
我们无法穷尽所有问题，如果遇到未在其中且无法解决的问题，[AskTUG](http://asktug.com) 社区中的友善成员很乐意解答您的问题。

## 恢复的时候，报错 “could not read local://...:download sst failed”，怎么办？

在恢复的时候，每个节点都必须能够访问到**所有**的备份文件（SST files）。
默认情况下，假如使用 `local` storage，备份文件会分散在各个节点中。
此时是无法直接恢复的，必须将每个 TiKV 节点的备份文件拷贝到其它所有 TiKV 节点才能恢复。
 
事实上，建议在备份的时候挂载一块 NFS 网盘作为备份盘，[参考用例](/br/backup-and-restore-use-cases.md#将单表数据备份到网络盘推荐)。
 
## BR 备份时，对集群影响多大？
 
使用 sysbench 的 oltp_read_only 场景全速备份到非服务盘，对集群的影响依照表结构的不同，对集群 QPS 的影响在 15%~25% 之间。
 
如果需要控制备份带来的影响，可以使用 `--ratelimit` 选项限速。
 
## BR 会备份系统表吗？ 等恢复的时候，这些系统表会冲突吗？
 
全量备份的时候会过滤掉系统库（`information_schema`，`performance_schema`，`mysql`）。参考[备份原理](/br/backup-and-restore-tool.md#备份原理)。
 
## BR 遇到 Permission denied 错误，即便用 root 运行 BR 也没用，怎么办？
 
确认 TiKV 是否有访问备份目录的权限。如果是备份，请确认是否有写权限；如果是恢复，请确认是否有读权限。
 
使用 root 运行 BR 仍旧有可能会因为磁盘权限而失败，因为备份文件 (SST) 的保存是由 TiKV 执行的。
 
> **提示：**
>
> 在恢复的时候也可能遇到同样的问题。在现版本 BR 的恢复中，在创建完毕所有表之前我们不会检验读权限。
> 假如备份表的数量特别多，可能会因此遇到等了很长时间之后失败的尴尬状况。
> 因此，最好在恢复前提前检查权限。
 
## BR 遇到 Error: msg:“Io(Os { ... })” 错误，怎么办？
 
这类问题几乎都是 TiKV 在写盘的时候遇到的系统调用错误。检查备份目录的挂载方式和文件系统，试试看备份到其它文件夹或者其它硬盘。
 
目前已知备份到 samba 搭建的网盘时可能会遇到 `Code: 22(invalid argument)` 错误。
 
## 使用 local storage 的时候，BR 备份的文件会存在哪里？
 
在使用 local storage 的时候，会在运行 BR 的节点生成 backupmeta，在各个 Region 的 Leader 节点生成备份文件。
 
## 备份数据会有多大，备份会有副本 (replica) 吗？
 
备份的时候仅仅在每个 region 的 Leader 处生成该 region 的备份文件。因此备份的大小等于数据大小，不会有多余的副本数据。所以最终的总大小大约是 TiKV 数据总量 ／副本数。
 
但是假如想要从本地恢复数据，因为每个 TiKV 都必须要能访问到所有备份文件，在最终恢复的时候会有等同于恢复时 TiKV 节点数量的副本。
