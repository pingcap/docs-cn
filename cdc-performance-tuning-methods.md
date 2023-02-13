---

summary: 本文介绍了 Performance Overview 仪表盘中 CDC 部分，帮助 TiDB 用户了解和监控 CDC MPP 工作负载。
---

# CDC 性能分析和优化方法
本文介绍 CDC 资源使用率和关键的性能指标，用户通过 CDC 仪表盘，可以用来监控和评估 CDC 集群性能。

## CDC 集群资源利用率

通过以下三个数据，可以快速判断 CDC 集群的资源使用率

- CPU usage：TiCDC 节点的 CPU 使用情况
- Memory usage：TiCDC 节点的内存使用情况
- Goroutine count：TiCDC 节点 Goroutine 的个数

## CDC 关键指标

### 延迟指标和 CDC 状态

- Changefeed checkpoint lag：同步任务上下游数据的进度差（以时间单位秒计算）如果 CDC 消费数据的速度和写入下游的速度跟得上上游的数据变更，checkpoint lag 将维持在短时间内，通常是 1 分钟以内；如果 CDC 消费数据的速度和写入下游的速度跟不上上游的数据变更，checkpoint lag 将持续增长。常见 CDC checkpoint lag 过长的原因：
  - 系统资源不足：如果 TiCDC 系统中的 CPU、内存或磁盘空间不足，可能会导致数据处理速度过慢，从而导致 TiCDC Changefeed checkpoint 过长。
  - 网络问题：如果 TiCDC 系统中存在网络中断、延迟或带宽不足的问题，可能会影响数据的传输速度，从而导致 TiCDC Changefeed checkpoint 过长。
  - 数据量过大：如果 TiCDC 系统需要处理的数据量过大，可能会导致数据处理超时，从而导致 TiCDC Changefeed checkpoint 过长。
  - 数据库问题：如果 TiCDC 系统中源数据库存在问题，例如长时间的延迟、数据丢失或不一致，可能会导致 TiCDC Changefeed checkpoint 过长。


- Changefeed resolved ts lag：TiCDC 节点内部同步状态与上游的进度差（以时间单位秒计算）如果 TiCDC Changefeed resolved ts lag 值很高，可能意味着 TiCDC 系统的 Puller 或者 Sorter 模块数据处理能力不足，或者可能存在网络延迟或磁盘读写速度慢的问题。在这种情况下，需要采取适当的行动，例如增加 TiCDC 实例数量或优化网络配置，以确保 TiCDC 系统的高效和稳定运行。
- The status of changefeeds：changefeed 的状态
    - 0：Normal
    - 1：Error
    - 2：Failed
    - 3：Stopped
    - 4：Finished
    - -1：Unknown

### 数据流吞吐指标
- Puller output events/s：TiCDC 节点中 Puller 模块每秒输出到 Sorter 模块的数据变更行数
- Sorter output events/s：TiCDC 节点中 Sorter 模块每秒输出到 Mounter 模块的行数
- Mounter output events/s：TiCDC 节点中 Mounter 模块每秒输出到 Sink 模块的行数
- Table sink output events/s：TiCDC 节点中 Table Sorter 模块每秒输出到 Sink 模块的行数
- SinkV2 - Sink flush rows/s：TiCDC 节点中 Sink 模块每秒输出到下游的行数
- Transaction Sink Full Flush Duration：TiCDC 节点中 MySQL Sink 写下游事务的平均延迟和 p999 延迟
- MQ Worker Send Message Duration Percentile：下游为 Kafka 时 MQ worker 发送消息的延迟
- Kafka Outgoing Bytes：MQ Workload 写下游事务的流量
