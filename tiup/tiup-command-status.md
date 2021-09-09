---
title: tiup status
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

[<< 返回上一页 - TiUP 命令清单](/tiup/tiup-reference.md#命令清单)