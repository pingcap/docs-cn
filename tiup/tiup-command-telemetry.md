---
title: tiup telemetry
aliases: ['/docs-cn/dev/tiup/tiup-command-telemetry/']
---

# tiup telemetry

## 介绍

TiDB、TiUP 及 TiDB Dashboard 默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品，例如，通过这些使用情况信息，PingCAP 可以了解常见的 TiDB 集群操作，从而确定新功能优先级。

当 TiUP 遥测功能开启时，执行 TiUP 命令时将会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiUP 命令的执行情况，如命令执行是否成功、命令执行耗时等
- 使用 TiUP 进行部署的情况，如部署的目标机器硬件信息、组件版本号、修改过的部署配置名称等

TiUP 使用命令 `tiup telemetry` 来控制遥测。

## 语法

```sh
tiup telemetry <command>
```

`<command>` 代表子命令，支持的子命令列表请参考下方命令一节。

## 命令

### status

命令 `tiup telemetry status` 查看当前的遥测设置，输出以下信息：

- status: 当前是否开启遥测（enable|disable）
- uuid: 随机生成的遥测标示符

### reset

命令 `tiup telemetry reset` 重置当前的遥测标示符，以一个新的随机标识符代替之。

### enable

命令 `tiup telemetry enable` 启用遥测。

### disable

命令 `tiup telemetry disable` 停用遥测。