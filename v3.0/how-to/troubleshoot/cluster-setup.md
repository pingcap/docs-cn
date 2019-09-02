---
title: TiDB 集群故障诊断
category: how-to
aliases: ['/docs-cn/trouble-shooting/']
---

# TiDB 集群故障诊断

当试用 TiDB 遇到问题时，请先参考本篇文档。如果问题未解决，请按文档要求收集必要的信息通过 Github [提供给 TiDB 开发者](https://github.com/pingcap/tidb/issues/new/choose)。

## 如何给 TiDB 开发者报告错误

当使用 TiDB 遇到问题并且通过后面所列信息无法解决时，请收集以下信息并[创建新 Issue](https://github.com/pingcap/tidb/issues/new/choose):

+ 具体的出错信息以及正在执行的操作
+ 当前所有组件的状态
+ 出问题组件 log 中的 error/fatal/panic 信息
+ 机器配置以及部署拓扑
+ dmesg 中 TiDB 组件相关的问题

## 数据库连接不上

首先请确认集群的各项服务是否已经启动，包括 tidb-server、pd-server、tikv-server。请用 ps 命令查看所有进程是否在。如果某个组件的进程已经不在了，请参考对应的章节排查错误。

如果所有的进程都在，请查看 tidb-server 的日志，看是否有报错？常见的错误包括：

+ InformationSchema is out of date

    无法连接 tikv-server，请检查 pd-server 以及 tikv-server 的状态和日志。

+ panic

    程序有错误，请将具体的 panic log [提供给 TiDB 开发者](https://github.com/pingcap/tidb/issues/new/choose)。

    如果是清空数据并重新部署服务，请确认以下信息：

+ pd-server、tikv-server 数据都已清空

    tikv-server 存储具体的数据，pd-server 存储 tikv-server 中数据的的元信息。如果只清空 pd-server 或只清空 tikv-server 的数据，会导致两边数据不匹配。

+ 清空 pd-server 和 tikv-server 的数据并重启后，也需要重启 tidb-server

    集群 ID 是由 pd-server 在集群初始化时随机分配，所以重新部署集群后，集群 ID 会发生变化。tidb-server 业务需要重启以获取新的集群 ID。

## tidb-server 启动报错

tidb-server 无法启动的常见情况包括：

+ 启动参数错误

    请参考[TiDB 命令行参数](v3.0/reference/configuration/tidb-server/configuration.md)

+ 端口被占用：`lsof -i:port`

    请确保 tidb-server 启动所需要的端口未被占用。

+ 无法连接 pd-server

    首先检查 pd-server 的进程状态和日志，确保 pd-server 成功启动，对应端口已打开：`lsof -i:port`。

    若 pd-server 正常，则需要检查 tidb-server 机器和 pd-server 对应端口之间的连通性，
    确保网段连通且对应服务端口已添加到防火墙白名单中，可通过 nc 或 curl 工具检查。

    例如，假设 tidb 服务位于 `192.168.1.100`，无法连接的 pd 位于 `192.168.1.101`，且 2379 为其 client port，
    则可以在 tidb 机器上执行 `nc -v -z 192.168.1.101 2379`，测试是否可以访问端口。
    或使用 `curl -v 192.168.1.101:2379/pd/api/v1/leader` 直接检查 pd 是否正常服务。

## tikv-server 启动报错

+ 启动参数错误

    请参考[TiKV 启动参数](v3.0/reference/configuration/tikv-server/configuration.md)文档。

+ 端口被占用：`lsof -i:port`

    请确保 tikv-server 启动所需要的端口未被占用： `lsof -i:port`。
+ 无法连接 pd-server

    首先检查 pd-server 的进程状态和日志。确保 pd-server 成功启动，对应端口已打开：`lsof -i:port`。

    若 pd-server 正常，则需要检查 tikv-server 机器和 pd-server 对应端口之间的连通性，
    确保网段连通且对应服务端口已添加到防火墙白名单中，可通过 nc 或 curl 工具检查。具体命令参考上一节。

+ 文件被占用

    不要在一个数据库文件目录上打开两个 tikv。

## pd-server 启动报错

+ 启动参数错误

    请参考[PD 命令行参数](v3.0/reference/configuration/pd-server/configuration.md)文档。
+ 端口被占用：`lsof -i:port`

    请确保 pd-server 启动所需要的端口未被占用： `lsof -i:port`。

## TiDB/TiKV/PD 进程异常退出

+ 进程是否是启动在前台

    当前终端退出给其所有子进程发送 HUP 信号，从而导致进程退出。
+ 是否是在命令行用过 `nohup+&` 方式直接运行

    这样依然可能导致进程因终端连接突然中断，作为终端 SHELL 的子进程被杀掉。
    推荐将启动命令写在脚本中，通过脚本运行（相当于二次 fork 启动）。

## TiKV 进程异常重启

+ 检查 dmesg 或者 syslog 里面是否有 OOM 信息

    如果有 OOM 信息并且杀掉的进程为 TiKV，请减少 TiKV 的 RocksDB 的各个 CF 的 `block-cache-size` 值。

+ 检查 TiKV 日志是否有 panic 的 log

    提交 Issue 并附上 panic 的 log。

## TiDB panic

请提供 panic 的 log

## 连接被拒绝

+ 请确保操作系统的网络参数正确，包括但不限于
    - 连接字符串中的端口和 tidb-server 启动的端口需要一致
    - 请保证防火墙的配置正确

## Too many open files

在启动进程之前，请确保 `ulimit -n` 的结果足够大，推荐设为 unlimited 或者是大于 1000000。

## 数据库访问超时，系统负载高

首先检查 [SLOW-QUERY](v3.0/how-to/maintain/identify-slow-queries.md) 日志，判断是否是因为某条 SQL 语句导致。如果未能解决，请提供如下信息：

+ 部署的拓扑结构
    - tidb-server/pd-server/tikv-server 部署了几个实例
    - 这些实例在机器上是如何分布的
+ 机器的硬件配置
    - CPU 核数
    - 内存大小
    - 硬盘类型（SSD 还是机械硬盘）
    - 是实体机还是虚拟机
+ 机器上除了 TiDB 集群之外是否还有其他服务
+ pd-server 和 tikv-server 是否分开部署
+ 目前正在进行什么操作
+ 用 `top -H` 命令查看当前占用 CPU 的线程名
+ 最近一段时间的网络/IO 监控数据是否有异常
