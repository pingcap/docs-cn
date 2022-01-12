---
title: TiDB Data Migration 日常巡检
summary: 了解 DM 工具的日常巡检。
aliases: ['/docs-cn/tidb-data-migration/dev/daily-check/']
---

# TiDB Data Migration 日常巡检

本文总结了 TiDB Data Migration (DM) 工具日常巡检的方法：

+ 方法一：执行 `query-status` 命令查看任务运行状态以及相关错误输出。详见[查询状态](/dm/dm-query-status.md)。

+ 方法二：如果使用 TiUP 部署 DM 集群时正确部署了 Prometheus 与 Grafana，如 Grafana 的地址为 `172.16.10.71`，可在浏览器中打开 <http://172.16.10.71:3000> 进入 Grafana，选择 DM 的 Dashboard 即可查看 DM 相关监控项。具体监控指标参照[监控与告警设置](/dm/monitor-a-dm-cluster.md)。

+ 方法三：通过日志文件查看 DM 运行状态和相关错误。

    - DM-master 日志目录：通过 DM-master 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录位于 `{log_dir}`。
    - DM-worker 日志目录：通过 DM-worker 进程参数 `--log-file` 设置。如果使用 TiUP 部署 DM，则日志目录位于 `{log_dir}`。
