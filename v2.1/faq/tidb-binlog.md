---
title: TiDB Binlog 常见问题
category: FAQ
---

# TiDB Binlog 常见问题

## 开启 binog 对 TiDB 的性能影响

对于查询无影响。

对于有写入或更新数据的事务有一点性能影响，延迟上在 Prewrite 阶段要并发写一条 p-binlog 成功后才可以提交事务，一般写 binlog 比 KV Prewrite 快所以不会增加延迟，写 binlog 的响应时间可以在 pump 的监控面板看到。

## drainer 同步下游 TiDB/Mysql 的帐号需要有什么权限

drainer 同步帐号需要有如下权限：

* Insert
* Update
* Delete
* Create
* Drop
* Alter
* Execute
* Index
* Select

## pump 磁盘快满了怎么办

确认 gc 正常:

- 确认 pump 监控面板 **gc_tso** 时间是否与配置一致。

如 gc 正常以下调整可以降低单个 pump 需要的空间大小：

- 调整 pump **GC** 参数减少保留数据天数。
- 添加 pump 结点。

## drainer 同步中断怎么办

使用 binlogctl 如下命令查看 pump 状态是否正常,是否全部非 offline 的 pump 都在正常运行。

```
binlogctl -cmd pumps
```

查看 drainer 监控与日志, 是否有对应报错，看具体问题处理。

## drainer 同步下游 TiDB/Mysql 慢怎么办

一些特别需要关注的监控项:

- drainer 监控 **drainer event** 可以看到 drainer 当前每秒同步 Insert/Update/Delete 时间到下游的速度
- drainer 监控 **sql query time** 可以看到 drainer 在下游执行 sql 的响应时间

可能同步慢的原因与调整:

- 同步的数据库包含没有主键或者唯一索引的表, 需要给表加上主键。
- drainer 跟下游之间延迟大, 可以调大 drainer **worker-count** 参数(跨机房同步建议 drainer 部署在下游)。
- 下游负载不高, 可以尝试调大 drainer **worker-count** 参数。

## 假如有一个 pump crash 了会怎样

drainer 会因为获取不到这个 pump 的数据没法同步数据到下游,如果这个 pump 能恢复 drainer 就能恢复同步

如果 pump 没法恢复, 可以如下处理:
    1. 使用 [binlogctl 修改这个 pump 状态成 offline](/v2.1/how-to/maintain/tidb-binlog.md)(丢失这个pump的数据)
    2. drainer 获取到的数据会丢失这个 pump 上的数据，下游跟上游数据会不一致，需要如下重新做全量 + 增量:
        1. 停止当前 drainer
        2. 上游做全量备份
        3. 清理掉下游数据包括 checkpoint 表 `tidb_binlog.checkpoint`
        4. 使用上游的全量备份恢复下游
        5. 部署 drainer, 使用 `initialCommitTs`= {从全量备份获取快照的时间戳}

## 什么是 checkpoint

checkpoint 记录了 drainer 同步到下游的 commit-ts, 重启的时候可以读取 checkpoint 接着从对应 commit-ts 同步数据到下游
drainer 日志 `["write save point"] [ts=411222863322546177]` 表示保存对应时间戳的 checkpoint。

下游类型不同，checkpoint 的保存方式也不同:

- 下游 MySQL/TiDB 保存在 `tidb_binlog.checkpoint` 表
- 下游 kafka/file 保存在对应配置目录里的文件

因为 kafka/file 的数据内容包含了 commit-ts, 所以如果 checkpoint 丢失我们可以消费下游最新的一条数据看写到下游数据的最新 commit-ts。

drainer 启动的时候会去读取 checkpoint, 读取不到的话就会使用配置的 `initial-commit-ts` 做为初次启动开始的同步时间点。

## drainer 机器故障如何在新机器重新部署 drainer (下游数据还在的情况下）

因为下游数据还在我们只要保证能从对应 checkpoint 接着同步就可以了。

假如 checkpoint 还在可以如下处理：

1. 部署新的 drainer 启动即可(参考 `checkpoint 介绍`, drainer 可以读取 checkpoint 接着同步)
2. 使用 [binlogctl 修改老的 drainer 状态成 offline](/v2.1/how-to/maintain/tidb-binlog.md)

假如 checkpoint 不在，可以如下处理：

1. 获取 之前 drainer 的 checkpoint `commit-ts` 做为新部署 drainer 的 `initial-commit-ts` 配置部署新的 drainer
2. 使用 [binlogctl 修改老的 drainer 状态成 offline](/v2.1/how-to/maintain/tidb-binlog.md)

## 如何用全量 + binlog 备份文件来恢复一个集群

1. 清理集群数据并使用全部备份恢复数据
2. 使用 reparo 设置 `start-tso` = {全量备份文件快照时间戳+1}, `end-ts` = 0 (或者指定时间点) 恢复到备份文件最新的数据

## 主从同步开启 `ignore-error` 触发 critical error 后如何重新部署

1. 停止当前 drainer
2. 重启触发 critical error 的 `tidb-server` 实例重新开始写 binlog (触发 critical error 后不会再写 binlog 到 pump)
3. 上游做全量备份
4. 清理掉下游数据包括 checkpoint 表 `tidb_binlog.checkpoint`
5. 使用上游的全量备份恢复下游
6. 部署 drainer, 使用 `initialCommitTs`= {从全量备份获取快照的时间戳}
