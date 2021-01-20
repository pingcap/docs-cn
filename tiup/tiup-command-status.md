---
title: tiup status
---

# tiup status

## 介绍

命令 `tiup status` 查看组件运行信息：通过 `tiup [flags] <component> [args...]` 运行组件之后，可以通过该命令查看组件的运行信息。

> **使用限制：**
>
> 只能查询到以下两种组件的信息：
>
> 1. 尚在运行的组件
> 2. 通过 `tiup -T/--tag` 指定 tag 运行的组件

## 语法

```sh
tiup status [flags]
```

## 选项

无

## 输出

由 `Tag 名字`，`组件名`，`进程 PID`，`运行状态`, `启动时间`，`启动参数`，`数据目录`，`二进制文件路径` 构成的表格，若启动时未指定 Tag 名字，则 Tag 名字段为随机字符串。