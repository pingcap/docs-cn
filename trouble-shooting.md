# TiDB 集群故障诊断

当试用 TiDB 遇到问题时，请先参考本篇文档。如果问题未解决，请按文档要求提供对应的信息给 TiDB 开发者。

### 数据库连接不上
首先请确认集群的各项服务是否已经启动，包括 tidb-server、pd-server、tikv-server。请用 ps 命令查看所有进程是否在。如果某个组件的进程已经不在了，请参考对应的章节排查错误。

如果所有的进程都在，请查看 tidb-server 的日志，看是否有报错？常见的错误包括：
+ InforSchema out of date

无法连接 tikv-server，请检查 tikv-server 的状态和日志
+ panic

程序有错误，请将具体的报错信息发给我们

### tidb-server 启动报错
tidb-server 无法启动的常见情况包括：
+ 端口被占用

请确保 tidb-server 启动所需要的端口未被占用
+ 无法连接 pd-server

请确保 tidb 和 pd 之间的网络畅通，包括是否能 ping 通，防火墙配置是否有问题。

如果网络没问题检查 pd-server 的进程状态和日志。

### tikv-server 启动报错
+ 端口被占用

请确保 tikv-server 启动所需要的端口未被占用
+ 无法连接 pd-server

请确保 tikv 和 pd 之间的网络畅通，包括是否能 ping 通，防火墙配置是否有问题。
如果网络没问题检查 pd-server 的进程状态和日志。

+ 文件被占用
不要在一个数据库文件目录上打开两个 tikv

### pd-server 启动报错

### TiDB/TiKV/PD 进程异常退出
+ 进程是否是启动在前台
终端退出导致进程退出。
+ 是否是在命令行用过 nohup+& 方式运行
这样依然可能导致进程收到 hup 信号并退出，推荐将启动命令写在脚本中，通过脚本运行


### TiDB panic
请提供 panic 的 log

### 连接被拒绝
+ 请确保操作系统的网络参数正确，包括但不限于
+ 连接字符串中的端口和 tidb-server 启动的端口是否一致
+ 请保证防火墙的配置正确

### Open too many files
在启动进程之前，请确保 ulimit -n 的结果足够大，推荐设为 unlimited 或者是大于 10240

### 数据库访问超时，系统负载高
首先请提供如下信息
+ 部署的拓扑结构
  - tidb-server/pd-server/tikv-server 部署了几个实例
  - 这些实例机器上
+ 机器的硬件配置
  - CPU 核数
  - 内存大小
  - 硬盘类型（SSD还是机械硬盘）
  - 是实体机还是虚拟机
+ 机器上除了 TiDB 集群之外是否还有其他服务
+ pd-server 和 tikv-server 是否分开部署
+ 目前正在进行什么操作
+ 用 top -H 命令查看当前占用 CPU 的线程名
+ 最近一段时间的网络/IO 监控数据是否有异常
