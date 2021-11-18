---
title: Online Unsafe Recovery 使用文档
summary: 如何使用 Online Unsafe Recovery。
---

# Online Unsafe Recovery 使用文档

> **警告：**
>
> - 此功能为有损恢复，无法保证数据和数据索引完整性。
> - 此功能为实验特性，其接口、策略和内部实现在 GA 前可能会有所变化。虽然已通过部分场景的测试，但尚未经过广泛验证，使用此功能可能导致系统不可用，不建议在生产环境中使用。
> - 建议在 TiDB 团队支持下进行相关操作，操作不当可能导致集群难以恢复。

当多数副本的永久性损坏造成部分数据不可读写时，可以使用 Online Unsafe Recovery 功能进行数据有损恢复。

## 功能说明

在 TiDB 中，根据用户定义的多种副本规则，一份数据可能会同时存储在多个节点中，从而保证在单个或少数节点暂时离线或损坏时，读写数据不受任何影响。但是，当一个 Region 的多数或全部副本在短时间内全部下线时，为了保证数据的完整性，该 Region 会处于暂不可用的状态。

如果一段数据的多数副本发生了永久性损坏（如磁盘损坏）等问题，从而导致节点无法上线时，此段数据会一直保持暂不可用的状态。这时，如果用户希望集群恢复正常使用，在用户能够容忍数据回退或数据丢失的前提下，用户理论上可以通过手动移除不可用副本的方式，使 TiDB 重新形成多数派，进而让上层业务可以写入和读取（可能是 stale 的，或者为空）这一段数据分片。

在这个情况下，当存有可容忍丢失的数据的部分节点受到永久性损坏时，用户可以通过使用 Online Unsafe Recovery，快速简单地进行有损恢复。使用 Online Unsafe Recovery 时，PD 会收集全部节点内的数据分片元信息，用 PD 的全局视角生成一份更实时、更完整的恢复计划后，将其计划下发给各个存活的节点，使各节点执行数据恢复任务。另外，下发恢复计划后，PD 还会定期查看恢复进度，并在需要时，重新向各节点分发恢复计划。

## 适用场景

Online Unsafe Recovery 功能适用于以下场景：

* 部分节点受到永久性损坏，导致节点无法重启，造成业务端的部分数据不可读、不可写。
* 可以容忍数据丢失，希望受影响的数据恢复读写。
* 希望在线一站式恢复数据。

## 使用步骤

### 前提条件

在使用 Online Unsafe Recovery 功能进行数据有损恢复前，请确认以下事项：

* 离线节点导致部分数据确实不可用。
* 离线节点确实无法自动恢复或重启。

### 第 1 步：关闭各类调度

暂时关闭负载均衡等各类内部调度。关闭后，建议等待约 10 分钟，使已经触发的调度能有充分的时间完成调度任务。

> **注意：**
>
> 关闭调度后，系统将无法处理系统数据热点问题，请在恢复后尽快重新开启调度。

1. 使用 PD Control 执行 [`config show`](/pd-control.md#config-show--set-option-value--placement-rules) 命令，获取当前的配置信息。
2. 使用 PD Control 关闭各类调度：

    * [`config set region-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
    * [`config set replica-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)
    * [`config set merge-schedule-limit 0`](/pd-control.md#config-show--set-option-value--placement-rules)

### 第 2 步：移除无法自动恢复的节点

使用 PD Control 执行 [`unsafe remove-failed-stores <store_id>[,<store_id>,...]`](/pd-control.md#unsafe-remove-failed-stores-store-ids--show--history)命令，移除无法自动恢复的节点。

> **注意：**
>
> 此命令成功返回，仅表示请求已被接受，而不代表恢复成功。节点实际会在后台进行恢复。

### 第 3 步：查看进度

节点移除命令运行成功后，使用 PD Control 执行 [`unsafe remove-failed-stores show`](/pd-control.md#config-show--set-option-value--placement-rules)命令，查看移除进度。当命令执行结果显示 "Last recovery has finished" 时，系统恢复完成。

### 第 4 步：测试读写任务

进度命令提示任务已完成后，可以尝试运行一些简单 SQL 查询或写入操作确保数据可以读写。示例如下：

```sql
select count(*) from table_that_suffered_from_group_majority_failure;
```

> **注意：**
>
> 数据可以读写并不代表没有数据丢失。

### 第 5 步：重新开启调度

把在第 1 步中修改的配置 `config set region-schedule-limit 0`，`config set replica-schedule-limit 0`，`config set merge-schedule-limit 0` 调整回初始值，重新开启调度功能。至此，整个流程结束。
