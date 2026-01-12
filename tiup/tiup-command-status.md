---
title: tiup status
summary: tiup status 命令用于查看组件的运行信息，包括组件名称、进程 ID、运行状态、启动时间、数据目录、二进制文件路径和启动参数。组件可能处于在线、离线、无法访问、已缩容下线、下线中或未知状态。这些状态来自于 PD 的调度信息。
---

# tiup status

使用命令 `tiup status` 可查看组件的运行信息：通过 `tiup [flags] <component> [args...]` 运行组件之后，可以通过该命令查看组件的运行信息。

> **注意：**
>
> 只能查询到以下两种组件的信息：
>
> + 尚在运行的组件
> + 通过 `tiup -T/--tag` 指定 tag 运行的组件

## 语法

```shell
tiup status [flags]
```

## 选项

无

## 输出

由以下字段构成的表格：

- Name: 通过 `-T/--tag` 指定的 Tag 名字，若未指定，则为随机字符串
- Component: 运行的组件
- PID: 对应的进程 ID
- Status: 组件运行状态
- Created Time: 启动时间
- Directory: 数据目录
- Binary: 二进制文件路径
- Args: 启动参数

### 组件运行状态 (Status)

组件可能处于如下任一运行状态：

- 在线 (Up)：组件正常运行。
- 离线 (Down) 或无法访问 (Unreachable)：组件未启动或对应主机存在网络问题。
- 已缩容下线 (Tombstone)：组件上的数据已被完整迁出并缩容完毕。仅 TiKV 或 TiFlash 组件存在该状态。
- 下线中 (Pending Offline)：组件上的数据正在被迁出并缩容。仅 TiKV 或 TiFlash 组件存在该状态。
- 未知 (Unknown)：未知的组件运行状态。

> **注意：**
>
> TiUP 显示的 `Pending Offline`、PD API 返回的 `Offline` 以及 TiDB Dashboard 显示的 `Leaving` 这三个状态的含义相同。

组件运行状态来自于 PD 的调度信息。更详细的描述请参考 [TiDB 数据库的调度 -- 信息收集](/tidb-scheduling.md#信息收集)。