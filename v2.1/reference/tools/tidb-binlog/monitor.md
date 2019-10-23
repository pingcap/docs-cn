---
title: TiDB Binlog 集群监控
category: reference
aliases: ['/docs-cn/v2.1/how-to/monitor/tidb-binlog/']
---

# TiDB Binlog 集群监控

使用 Ansible 成功部署 TiDB Binlog 集群后，可以进入 Grafana Web 界面（默认地址: <http://grafana_ip:3000>，默认账号：admin，密码：admin）查看 Pump 和 Drainer 的运行状态。

## 监控指标

### Pump

| metric 名称 | 说明 |
|:----|:------------|
| Storage Size | 记录磁盘的总空间大小 (capacity)，以及可用磁盘空间大小 (available) |
| Metadata | 记录每个 Pump 的可删除 binlog 的最大 tso (gc_tso)，以及保存的 binlog 的最大的 commit tso (max_commit_tso)。 |
| Write Binlog QPS by Instance | 每个 Pump 接收到的写 binlog 请求的 QPS |
| Write Binlog Latency | 记录每个 Pump 写 binlog 的延迟时间 |
| Storage Write Binlog Size | Pump 写 binlog 数据的大小 |
| Storage Write Binlog Latency | Pump 中的 storage 模块写 binlog 数据的延迟 |
| Pump Storage Error By Type | Pump 遇到的 error 数量，按照 error 的类型进行统计 |
| Query TiKV | Pump 通过 TiKV 查询事务状态的次数 |

### Drainer

| metric 名称 | 说明 |
|:----|:------------|
| Checkpoint TSO | Drainer 已经同步到下游的 binlog 的最大 TSO 对应的时间。可以通过该指标估算同步延迟时间 |
| Pump Handle TSO | 记录 Drainer 从各个 Pump 获取到的 binlog 的最大 TSO 对应的时间 | | Pull Binlog QPS by Pump NodeID | Drainer 从每个 Pump 获取 binlog 的 QPS |
| 95% Binlog Reach Duration By Pump | 记录 binlog 从写入 Pump 到被 Drainer 获取到这个过程的延迟时间 |
| Error By Type | Drainer 遇到的 error 数量，按照 error 的类型进行统计 |
| SQL Query Time| Drainer 在下游执行 SQL 的耗时 |
| Drainer Event | 各种类型 event 的数量，event 包括 ddl、insert、delete、update、flush、savepoint |
| Execute Time | 写入 binlog 到同步下游模块所消耗的时间 |
| 95% Binlog Size | Drainer 从各个 Pump 获取到 binlog 数据的大小 |
| DL Job Count | Drainer 处理的 DDL 的数量|
| Queue Size | Drainer 内部工作队列大小 |

## 监控报警规则

本节介绍了 TiDB Binlog 组件的报警项及相应的报警规则。根据严重级别，报警项可分为三类，按照严重程度由高到低依次为：紧急级别 (Emergency)、重要级别 (Critical)、警告级别 (Warning)。

### 紧急级别报警项

紧急级别的报警通常由于服务停止或节点故障导致，此时需要马上进行人工干预操作。

#### `binlog_pump_storage_error_count`

* 报警规则：

    `changes(binlog_pump_storage_error_count[1m]) > 0`

* 规则描述：

    Pump 写 binlog 到本地存储时失败。

* 处理方法：

    确认 `pump_storage_error` 监控是否存在错误，查看 Pump 日志确认原因。

### 重要级别报警项

对于重要级别的报警，需要密切关注异常指标。

#### `binlog_drainer_checkpoint_high_delay`

* 报警规则：

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

* 规则描述：

    Drainer 同步落后延迟超过 1 个小时。

* 处理方法：

    * 判断从 Pump 获取数据是否太慢：

        监控 Pump handle tso 可以看每个 Pump 最近一条消息的时间，是不是有延迟特别大的 Pump，确认对应 Pump 正常运行。

    * 根据 Drainer event 和 Drainer execute latency 来判断是否下游同步太慢：

        * 如果 Drainer execute time 过大，则检查到目标库网络带宽和延迟，以及目标库状态。
        * 如果 Drainer execute time 不大，Drainer event 过小，则增加 work count 和 batch 进行重试。

    * 如果上面都不满足或者操作后没有改观，则报备开发人员 [support@pingcap.com](mailto:support@pingcap.com) 进行处理。

### 警告级别报警项

警告级别的报警是对某一问题或错误的提醒。

#### `binlog_pump_write_binlog_rpc_duration_seconds_bucket`

* 报警规则：

    `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m])) > 1`

* 规则描述：

    Pump 处理 TiDB 写 Binlog 请求耗时过大。

* 处理方法：

    * 确认磁盘性能压力，通过 `node exported` 查看 disk performance 监控。
    * 如果 `disk latency` 和 `util` 都很低，那么报备开发人员 [support@pingcap.com](mailto:support@pingcap.com) 进行处理。

#### `binlog_pump_storage_write_binlog_duration_time_bucket`

* 报警规则：

    `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m])) > 1`

* 规则描述：

    Pump 写本地 binlog 到本地盘的耗时。

* 处理方法：

    确认 Pump 本地盘情况，进行修复。

#### `binlog_pump_storage_available_size_less_than_20G`

* 报警规则：

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

* 规则描述：

    Pump 剩余可用磁盘空间不足 20 G。

* 处理方法：

    监控确认 Pump 的 `gc_tso` 是否正常。如果不正常，调整 Pump 的 GC 时间配置或者下线对应 Pump。

#### `binlog_drainer_checkpoint_tso_no_change_for_1m`

* 报警规则：

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

* 规则描述：

    Drainer 的 `checkpoint` 在 1 分钟内没有更新。

* 处理方法：

    确认所有非下线的 Pump 是否正常运行。

#### `binlog_drainer_execute_duration_time_more_than_10s`

* 报警规则：

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

* 规则描述：

    Drainer 同步到 TiDB 的事务耗时。如果这个值过大，会影响 Drainer 同步。

* 处理方法：

    * 查看 TiDB 集群的状态。
    * 查看 Drainer 日志或监控，如果是 DDL 操作导致了该问题，则忽略。
