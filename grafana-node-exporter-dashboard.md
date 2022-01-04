---
title: Node Exporter 面板重要监控指标详解
aliases: ['/docs-cn/dev/grafana-overview-dashboard/','/docs-cn/dev/reference/key-monitoring-metrics/overview-dashboard/']
---

# Node Exporter 面板重要监控指标详解

使用 TiUP 部署 TiDB 集群时，一键部署监控系统 (Prometheus & Grafana)，监控架构参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview 等。

以下为 Node Exporter Dashboard 监控说明：

## Overview

- Virtual CPUs:
- Total RAM:
- Total Swap:
- System Uptime:
- Node_exporter version:
- CPU Used:
- Memory Used:
- Swap Used:
- Load1:
- Load5:
- Load15:

## Kernel

- OS:
- Machine:
- Kernel version:
- Interrupts:
- Forks:
- Context Switches:

## CPU

- CPU Usage:

## Memory

- Memory:
- Distribution:
- Available Buddy Pages - Zone Normal:
- Active/Inactive:
- Writeback and Dirty:
- Shared and Mapped:
- Mlocked/Slab:
- KernelStack:
- Anonymous:
- HugePages Size:
- HugePages Counter:
- Commit:
- Swap:
- Swap Activity:
- Page/Swap in/out
- Mem Fault:

## Vmstat - Page

- Pages In/Out:
- Pages Swap In/Out:
- Page Operations:
- Allocstall:
- Page Drop:
- Page Allocation:

## Vmstat - Numa

- Numa Allocations:
- Numa Page Migrations:
- Numa Hints:
- Numa Table Updates:
- Numa Mem Usage:
- Numa Mem Free:

## Vmstat - THP

- THP Splits:
- THP Allocations:

## Vmstat - Compact

- Compact Status:
- Compact Stall:
- Compact Isolated:
- Compact Free Scanned:
- Compact Migrate Scanned:

## Load

- Load: 1m:
- Load: 5m:
- Load: 15m:

# Disk

- total Disk Size：
- Disk State：
- Disk Space Utilzation：
- I/O Util：
- IOPs：
- Disk Write Latency（ms）：
- Disk Read Latency（ms）：
- Disk Throughput

## Filesystem

- Filesystem Device Error:
- Filesystem Space Used:
- Filesystem Inodes Used:

# Descriptors

- Allocated File Descriptor:
- Maximum File Descriptor:
- File Descriptors Used:
- Process Open Files Used:

## Network

- Network Interface State:
- Network IN/OUT Drops:
- Network IN/OUT Errors:
- Network IN/OUT Traffic:
- Network IN/OUT Packets:
- Network Interface Speed:
- Network Utilization Hourly:

## TCP

- TCP In Use:
- Segments retransmitted:
- TCP Connections:

## Processes:

- Processes:
