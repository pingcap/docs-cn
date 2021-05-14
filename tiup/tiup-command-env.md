---
title: tiup env
---

# tiup env

TiUP 为用户提供了灵活的定制化接口，其中一部分是使用环境变量来实现的，命令 `tiup env` 用于查询 TiUP 支持用户自定义的环境变量以及它们此时的值。

## 语法

```shell
tiup env [name1...N]
```

`[name1...N]` 用于查看指定的环境变量，若不指定，则默认查看所有支持的环境变量。

## 选项

无

## 输出

- 若未指定 `[name1...N]`，则输出 "{key}"="{value}" 列表
- 若指定了 `[name1...N]`，则按顺序输出 "{value}" 列表

以上输出中若 `value` 为空则代表未设置环境变量的值，此时 TiUP 会使用默认值。

[<< 返回上一页 - TiUP 命令清单](/tiup/tiup-reference.md#命令清单)