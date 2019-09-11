---
title: TiDB Binlog 常见问题
category: FAQ
---

# TiDB Binlog 常见问题

## 开启 binog 对 TiDB 的性能影响

- 对于查询无影响

- 对于有写入或更新数据的事务有一点性能影响，延迟上在 Prewrite 阶段要写一条 p-binlog 成功后才可以提交事务，一般写 binlog 比 KV Prewrite 快所以不会增加延迟，写 binlog 的响应时间可以在 pump 的监控面板看到。

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
    - 是否全部非下线 pump 都在正常运行
- 查看 drainer 监控与日志
    - 是否有对应报错，看具体问题处理

## drainer 同步下游 TiDB/Mysql 慢怎么办

- drainer 监控 **drainer event** 可以看到 drainer 当前每秒同步 Insert/Update/Delete 时间到下游的速度
- drainer 监控 **sql query time** 可以看到 drainer 在下游执行 sql 的响应时间
- 下游负载不高的情况下可以尝试调大 drainer **worker-count** 参数
    - 会加大并发写下游
    - drainer 跟下游之间延迟大的情况下需要调大并发数(跨机房同步建议 drainer 部署在下游)

## 假如有一个 pump crash 了会怎样

- drainer 会因为获取不到这个 pump 的数据没法同步数据到下游
- 如果这个 pump 能恢复 drainer 就能恢复同步
- 如果 pump 没法恢复需要考虑强制用 binlogctl 修改这个 pump 状态成 offline(丢失这个pump的数据), 或者重新部署
