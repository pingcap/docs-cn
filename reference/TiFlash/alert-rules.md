
# TiFlash 报警规则
## TiFlash_memory_abnormal
监控规则
tiflash_system_asynchronous_metric_jemalloc_allocated > 1.6e+10

含义
  * TiFlash进程占用内存超过16G。

处理方法
  * 怀疑有内存泄漏，联系TiFlash开发人员进行排查。

处理方法
  * 可能是磁盘有问题（损坏，空间占用较满，碎片较多），检查系统环境，联系 TiFlash 开发人员

## TiFlash_schema_error
监控规则
increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0

含义
  * 出现了 schema apply 错误的问题

处理方法
  * 可能是逻辑问题，联系 TiFlash 开发人员
## TiFlash_schema_apply_duration
监控规则
histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20

含义
  * 99% 的概率 apply 时间超过了 20 s

处理方法
  * 可能是 TiFlash TMT 引擎内部问题，联系 TiFlash 开发人员

## TiFlash_raft_read_index_duration
监控规则
histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3

含义
  * 99% 的概率，read index 的时间超过 3s。 注：read index 请求是发送给 TiKV leader 的 kvproto 请求，TiKV region 的重试，或 Store 的繁忙/网络问题都可能导致 read index 请求时间过长。

处理方法
  * 可能 TiKV 集群分裂/迁移频繁，导致频繁重试，可以查看 TiKV 集群状态确认

## TiFlash_raft_wait_index_duration
监控规则
histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2

含义
  * TiFlash 等待 Region Raft Index 的时间 99% 的概率超过 2s

处理方法
  * 可能 TiKV 和 Proxy 的通信出现问题，联系 TiFlash 开发人员确认
