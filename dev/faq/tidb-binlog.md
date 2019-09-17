---
title: TiDB Binlog 常见问题
category: FAQ
---

# TiDB Binlog 常见问题

## 开启 binog 对 TiDB 的性能影响

- 对于查询无影响

- 对于有写入或更新数据的事务有一点性能影响，延迟上在 Prewrite 阶段要并发写一条 p-binlog 成功后才可以提交事务，一般写 binlog 比 KV Prewrite 快所以不会增加延迟，写 binlog 的响应时间可以在 pump 的监控面板看到。

## Drainer 同步下游 TiDB/Mysql 的帐号需要有什么权限

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

- 确认 gc 正常
    - 确认 pump 监控面板 **gc_tso** 时间是否与配置一致
- 调整 pump **GC** 参数减少保留数据天数
- 添加 Pump 结点

## drainer 同步中断怎么办

- 查看 pump 状态是否正常
    - binlogctl -cmd pumps
    - 是否全部非 offline 的 pump 都在正常运行
- 查看 drainer 监控与日志
    - 是否有对应报错，看具体问题处理

## drainer 同步下游 TiDB/Mysql 慢怎么办

- drainer 监控 **drainer event** 可以看到 drainer 当前每秒同步 Insert/Update/Delete 时间到下游的速度
- drainer 监控 **sql query time** 可以看到 drainer 在下游执行 sql 的响应时间
- 同步的数据库是否有包含没有主键或者唯一索引的表
- 下游负载不高的情况下可以尝试调大 drainer **worker-count** 参数
    - 会加大并发写下游
    - drainer 跟下游之间延迟大的情况下需要调大并发数(跨机房同步建议 drainer 部署在下游)

## 假如有一个 pump crash 了会怎样

- drainer 会因为获取不到这个 pump 的数据没法同步数据到下游
- 如果这个 pump 能恢复 drainer 就能恢复同步
- 如果 pump 没法恢复
    - 使用 [binlogctl 修改这个 pump 状态成 offline](/dev/how-to/maintain/tidb-binlog.md)(丢失这个pump的数据)
    - drainer 获取到的数据会丢失这个 pump 上的数据，下游跟上游数据会不一致，需要重新全量 + 增量
        1. 停止当前 drainer
        2. 上游做全量备份
        3. 清理掉下游数据包括 checkpoint 表 `tidb_binlog.checkpoint`
        4. 使用上游的全量备份恢复下游
        5. 部署 drainer, 使用 `initialCommitTs`= {从全量备份获取快照的时间戳}

## drainer 故障如何重建 drainer (下游数据还在的情况下）

- checkpoint 还在
    - 部署新的 drainer 启动即可，使用相同 node-id 或者把老的 drainer 直接修改状态成 offline
- checkpoint 丢失
    - 获取写到下游的最新的 commit-ts 做为 initial-commit-ts 部署新的 drainer 启动即可，使用相同 node-id 或者把老的 drainer 直接修改状态成 offline
    - checkpoint 保存与获取
        - 下游 MySQL/TiDB 保存在 `tidb_binlog.checkpoint` 表, 表丢失无法获取下到下游的最新 commit-ts
        - 下游 kafka/file 保存在对应配置目录里的文件, 文件丢失可以消费下游最新的一条数据看写到下游数据的最新 commit-ts
        - 原始 drainer 日志存在可以查看最新保存 checkpoint 的 ts: `["write save point"] [ts=411222863322546177]`

## 如何用全量 + binlog 备份文件来恢复一个集群

1. 清理集群数据并使用全部备份恢复数据
2. 使用 reparo 设置 `start-tso` = {全量备份文件快照时间戳+1}, `end-ts` = 0 (或者指定时间点) 恢复到备份文件最新的数据

## 主从同步开启 `ignore-error` 触发 critical error 后如何重新部署

1. 停止当前 drainer
2. 重启全部 `tidb-server` 实例重新开始写 binlog (触发 critical error 后不会再写 binlog 到 pump)
3. 上游做全量备份
4. 清理掉下游数据包括 checkpoint 表 `tidb_binlog.checkpoint`
5. 使用上游的全量备份恢复下游
6. 部署 drainer, 使用 `initialCommitTs`= {从全量备份获取快照的时间戳}
