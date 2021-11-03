---
title: Online Unsafe Recover 使用文档
summary: 如何使用 Online Unsafe Recover
---

# Online Unsafe Recover 使用文档

> **警告：**
>
> - 此功能为有损恢复，无法保证数据完整性。
> - 建议在 TiDB 团队支持下进行相关操作，操作不当可能导致集群难以恢复。
> - 此功能仍处于测试阶段，其接口、策略和内部实现在最终发布时可能会有所变化。此功能已通过一部分普通常见场景的测试，但还未经过广泛验证，使用此功能可能导致系统不可用。

本文介绍 Online Unsafe Recover 的使用场景，使用方法和注意事项等。

## 功能背景概述

TiDB 是一个具备高可用性的数据库，根据用户定义的副本规则不同，一份数据在 TiDB 中可能同时存储于多个结点，以保证在单个或少数结点暂时离线或者损坏时，数据的读写不受任何影响。但是，为了保证数据的完整性，如果短时间内多数或全部副本下线，此段数据会变得暂时不可用。

如果一段数据的多数副本发生了永久性损坏（如磁盘损坏）或其他原因导致无法上线时，此段数据则会一直保持其不可用状态。如果用户想让集群可以恢复正常使用，并且可以容忍数据回退或者丢失，理论上可以通过手动覆写数据分片元信息的方式来使其重新可以形成多数派，进而让上层业务可以继续写入，或者读取（可能是 stale 的，或者为空）这一段的数据分片。

但是逐个修改受影响数据分片，不仅枯燥，而且并可靠，当无法恢复的结点数量较多，进而导致受影响的数据分片过多时，更无法 scale 。在此情况下，用户可使用 Onlne Unsafe Recover，对于可容忍数据丢失的数据库在部分结点永久性损坏时，尽量快速简单地进行有损恢复。相较于逐个修改分片元信息， Online Unsafe Recover 会由PD收集全部结点内的数据分片元信息，并借由此全局视角来生成一份更实时，完整的恢复计划下发给各存活结点执行。而且，在恢复计划下发后，PD还会定期查看恢复进度，确保集群状态和所期待的状态相匹配。

## 使用场景

Online Unsafe Recover 的一般使用场景为:

* 有部分结点永久损坏，无法重启，并造成了业务端部分数据不可读，不可写。
* 数据丢失可以容忍，而希望受影响的数据行可以恢复读写。
* 希望在线一站式恢复数据。

## 前提条件

在使用 Online Unsafe Recover 功能前，请确认以下事项：

* 确认部分数据确实不可用。
* 确认离线节点确实无法自动恢复或重启。

## 第 1 步：关闭各类调度

暂时关闭负载均衡等各类内部调度。关闭后，建议等待约 XX 小时，使已经触发的调度能有充分的时间完成调度任务。

1. 使用 pd-ctl 执行 [`config show`](/pd-control.md#config-show--set-option-value--placement-rules) 命令，获取当前的配置信息。
2. 使用 pd-ctl 关闭各类调度：
  * [`config set region-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
  * [`config set replica-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
  * [`config set merge-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)

## 第 2 步：移除无法自动恢复的节点

使用 pd-ctl 执行 [`unsafe remove-failed-stores <store_id>[,<store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show--history)命令，移除无法自动恢复的节点。


> **注意：**
>
> 此命令成功返回代表请求已被接受，节点实际会在后台进行恢复。

## 第 3 步：查看进度

节点移除命令运行成功后，使用 pd-ctl 执行 [`unsafe remove-failed-stores show (or history)`](/pd-control.md#config-show--set-option-value--placement-rules)命令，查看移除进度。

## 第 4 步：测试读写任务

进度命令提示任务已完成后，可以尝试运行一些简单 SQL 查询或写入操作确保数据可以读写。示例如下：

XXX

> **注意：**
>
> 数据可以读写并不代表没有数据丢失。

## 第 5 步：重新开启调度

把在第 1 步中修改的配置 `config set region-schedule-limit 0`，`config set replica-schedule-limit 0`，`config set merge-schedule-limit 0` 调整回初始值，重新开启调度功能。