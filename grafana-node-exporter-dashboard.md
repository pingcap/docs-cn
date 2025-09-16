---
title: Node Exporter 面板重要监控指标详解
aliases: ['/docs-cn/dev/grafana-node-exporter-dashboard/','/docs-cn/dev/reference/key-monitoring-metrics/node-exporter-dashboard/']
---

# Node Exporter 面板重要监控指标详解

使用 TiUP 部署 TiDB 集群时，一键部署监控系统 (Prometheus & Grafana)，监控架构参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node_exporter、Overview 等。

以下为 Node Exporter Dashboard 监控说明：

## Overview

- Virtual CPUs: CPU 核心数量。
- Total RAM: 内存总大小。
- Total Swap: 可使用的交换内存大小。
- System Uptime: 系统启动时长。
- Node_exporter version: Node Exporter 使用版本。
- CPU Used: CPU 的使用率。
- Memory Used: 内存的使用率。
- Swap Used: 交换内存的使用率。
- Load1: 1 分钟的负载情况。
- Load5: 5 分钟的负载情况。
- Load15: 15 分钟的负载情况。

## Kernel

- OS: 操作系统类型
- Machine: 机器平台
- Kernel version: 内核版本
- Interrupts: 内核中断情况
- Forks: Linux 下创建进程的系统调用情况
- Context Switches: CPU（中央处理单元）从一个进程或线程切换到另一个进程或线程的过程。

## CPU

- CPU Usage: CPU 的使用率

## Memory

- Memory: 内存的使用情况
- Distribution: 内存分布情况
- Available Buddy Pages - Zone Normal: linuxbuddy 系统管理物理内存的 debug 信息，低值表示内存碎片严重
- Active/Inactive: 活跃或非活跃内存情况，非活跃的内存将会优先回收，活跃的内存，除非绝对必要否则不会回收
- Writeback and Dirty: 回写和脏页。回写：准备主动回写硬盘的缓存页；临时回写：用于临时写回缓冲区的内存；脏页：等待写回磁盘的内存。
- Shared and Mapped: 共享内存和被映射占用的内存情况
- Mlocked/Slab: 内存的 Mlock 和 Slab 情况
- KernelStack: 内存堆栈大小（常驻内存，不可回收）
- Anonymous: 匿名内存页面的情况
- HugePages Size: 内存大页大小
- HugePages Counter: 内存大页数量
- Commit: 系统分配内存情况
- Swap: 系统的交换内存情况
- Swap Activity: 交换内存使用情况
- Page/Swap in/out: 分页和交换内存的写入/写出情况
- Mem Fault: 内存缺页异常情况

## Vmstat - Page

- Pages In/Out: 分页的写入/写出情况
- Pages Swap In/Out: 分页交换的写入/写出情况
- Page Operations: 分页的操作情况
- Allocstall: 请求直接回收的平均分页数
- Page Drop: 分页释放数量情况
- Page Allocation: 分页分配情况

## Vmstat - Numa

- Numa Allocations: Numa 的分配情况。Numa(Non-Uniform Memory Access) 指非一致内存访问
- Numa Page Migrations: Numa 分页的迁移情况
- Numa Hints: Numa 提示故障的情况
- Numa Table Updates: Numa 表更新情况
- Numa Mem Usage: Numa 内存使用率
- Numa Mem Free: Numa 内存空闲情况

## Vmstat - THP

- THP Splits: 大页分裂情况
- THP Allocations: 大页分配情况

## Vmstat - Compact

- Compact Status: 内存压缩状态
- Compact Stall: 开始执行内存碎片失败的页面数
- Compact Isolated: 用于内存压缩隔离的页面情况
- Compact Free Scanned: 扫描由压缩守护程序释放的页面情况
- Compact Migrate Scanned: 通过内存压缩守护程序扫描以进行迁移的页面情况

## Load

- Load: 1m: 1 分钟的负载情况
- Load: 5m: 5 分钟的负载情况
- Load: 15m: 15 分钟的负载情况

# Disk

- total Disk Size: 硬盘大小总和
- Disk State: 硬盘状态情况
- Disk Space Utilzation: 硬盘空间利用率
- I/O Util: 硬盘写入/读出利用率
- IOPs: 硬盘每秒的读写次数
- Disk Write Latency（ms）: 硬盘写延迟（毫秒）
- Disk Read Latency（ms）: 硬盘读延迟（毫秒）
- Disk Throughput: 硬盘吞吐量

## Filesystem

- Filesystem Device Error: 文件系统错误情况
- Filesystem Space Used: 文件系统已用空间
- Filesystem Inodes Used: 文件系统使用文件节点情况

# Descriptors

- Allocated File Descriptor: 分配的文件描述符
- Maximum File Descriptor: 最大的文件描述符
- File Descriptors Used: 已经使用的文件描述符
- Process Open Files Used: 已经处理的打开文件描述符

## Network

- Network Interface State: 网络接口状态情况
- Network IN/OUT Drops: 网络 IN/OUT 掉线情况
- Network IN/OUT Errors: 网络 IN/OUT 错误情况
- Network IN/OUT Traffic: 网络 IN/OUT 流量情况
- Network IN/OUT Packets: 网络 IN/OUT 数据包情况
- Network Interface Speed: 网络接口速度情况
- Network Utilization Hourly: 每小时网络利用率

## TCP

- TCP In Use: 处于使用状态的 TCP socket
- Segments retransmitted: 重传报文数量
- TCP Connections: TCP 连接数量

## Processes:

- Processes: 进程情况
