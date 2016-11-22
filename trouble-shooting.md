# TiDB 集群故障诊断

当试用 TiDB 遇到问题时，请先参考本篇文档。如果问题未解决，请按文档要求收集必要的信息通过票[提供给 TiDB 开发者](https://github.com/pingcap/tidb/issues/new)。

## 如何给 TiDB 开发者报告错误
当使用 TiDB 遇到问题并且通过后面所列信息无法解决时，请收集以下信息并[创建新 Issue](https://github.com/pingcap/tidb/issues/new):
+ 具体的出错信息以及正在执行的操作
+ 当前所有组件的状态
+ 出问题组件 log 中的 error/fatal/panic 信息
+ 机器配置以及部署拓扑
+ dmesg 中 TiDB 组件相关的问题


## 数据库连接不上
首先请确认集群的各项服务是否已经启动，包括 tidb-server、pd-server、tikv-server。请用 ps 命令查看所有进程是否在。如果某个组件的进程已经不在了，请参考对应的章节排查错误。

如果所有的进程都在，请查看 tidb-server 的日志，看是否有报错？常见的错误包括：
+ InfomationSchema is out of date.

  无法连接 tikv-server，请检查 pd-server 以及 tikv-server 的状态和日志
+ panic

  程序有错误，请将具体的 panic log [提供给 TiDB 开发者](https://github.com/pingcap/tidb/issues/new)

如果是清空数据并重新部署服务，请确认以下信息：
+ pd-server、tikv-server 数据都已清空

  tikv-server 存储具体的数据，pd-server 存储 tikv-server 中数据的的元信息。如果只清空 pd-server 或只清空 tikv-server 的数据，会导致两边数据不匹配。
+ 清空 pd-server 和 tikv-server 的数据并重启后，也需要重启 tidb-server

  集群 ID 是由 pd-server 在集群初始化时随机分配，所以重新部署集群后，集群 ID 会发生变化。tidb-server 业务需要重启以获取新的集群 ID。

## tidb-server 启动报错
tidb-server 无法启动的常见情况包括：
+ 启动参数错误

  请参考[TiDB 命令行参数](https://github.com/pingcap/docs-cn/blob/master/op-guide/configuration.md#tidb)文档
+ 端口被占用：`lsof -i:port`

  请确保 tidb-server 启动所需要的端口未被占用
+ 无法连接 pd-server

  请确保 tidb 和 pd 之间的网络畅通，包括是否能 ping 通，防火墙配置是否有问题。

  如果网络没问题检查 pd-server 的进程状态和日志。

## tikv-server 启动报错
+ 启动参数错误
  请参考[TiKV 启动参数](https://github.com/pingcap/docs-cn/blob/master/op-guide/configuration.md#tikv)文档

+ 端口被占用：`lsof -i:port`

  请确保 tikv-server 启动所需要的端口未被占用： `lsof -i:port`
+ 无法连接 pd-server

  请确保 tikv 和 pd 之间的网络畅通，包括是否能 ping 通，防火墙配置是否有问题。
  如果网络没问题检查 pd-server 的进程状态和日志。

+ 文件被占用
  不要在一个数据库文件目录上打开两个 tikv

## pd-server 启动报错
+ 启动参数错误

  请参考[PD 命令行参数](https://github.com/pingcap/docs-cn/blob/master/op-guide/configuration.md#placement-driver-pd)文档
+ 端口被占用：`lsof -i:port`

  请确保 pd-server 启动所需要的端口未被占用： `lsof -i:port`

## TiDB/TiKV/PD 进程异常退出
+ 进程是否是启动在前台

  终端退出导致进程退出。
+ 是否是在命令行用过 `nohup+&` 方式运行

  这样依然可能导致进程收到 hup 信号并退出，推荐将启动命令写在脚本中，通过脚本运行。


## TiDB panic
请提供 panic 的 log

## 连接被拒绝
+ 请确保操作系统的网络参数正确，包括但不限于
+ 连接字符串中的端口和 tidb-server 启动的端口是否一致
+ 请保证防火墙的配置正确

## Open too many files
在启动进程之前，请确保 ulimit -n 的结果足够大，推荐设为 unlimited 或者是大于 1000000

## 数据库访问超时，系统负载高
首先请提供如下信息
+ 部署的拓扑结构
  - tidb-server/pd-server/tikv-server 部署了几个实例
  - 这些实例在机器上是如何分布的
+ 机器的硬件配置
  - CPU 核数
  - 内存大小
  - 硬盘类型（SSD还是机械硬盘）
  - 是实体机还是虚拟机
+ 机器上除了 TiDB 集群之外是否还有其他服务
+ pd-server 和 tikv-server 是否分开部署
+ 目前正在进行什么操作
+ 用 `top -H` 命令查看当前占用 CPU 的线程名
+ 最近一段时间的网络/IO 监控数据是否有异常
