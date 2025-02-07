---
title: tiup telemetry
summary: TiUP 遥测功能在 v1.11.3 及以上版本默认关闭，以下版本默认开启。开启后会分享使用情况信息给 PingCAP，包括遥测标示符、命令执行情况、部署情况等。不会分享集群准确名字、拓扑结构、配置文件。使用命令 `tiup telemetry` 控制遥测，支持 status、reset、enable、disable 命令。
---

# tiup telemetry

在 v1.11.3 及以上的 TiUP 版本中，遥测功能默认关闭，即默认不收集使用情况信息分享给 PingCAP。在 v1.11.3 以下的 TiUP 版本中，遥测功能默认开启，即默认收集使用情况信息分享给 PingCAP 用于改善产品。

当 TiUP 遥测功能开启时，执行 TiUP 命令时会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiUP 命令的执行情况，如命令执行是否成功、命令执行耗时等
- 使用 TiUP 进行部署的情况，如部署的目标机器硬件信息、组件版本号、修改过的部署配置名称等

以下信息不会被分享：

- 集群的准确名字
- 集群的拓扑结构
- 集群的配置文件

TiUP 使用命令 `tiup telemetry` 来控制遥测。

## 语法

```shell
tiup telemetry <command>
```

`<command>` 代表子命令，支持的子命令列表请参考下方命令一节。

## 命令

### status

命令 `tiup telemetry status` 查看当前的遥测设置，输出以下信息：

- `status`: 当前是否开启遥测 `(enable|disable)`
- `uuid`: 随机生成的遥测标示符

### reset

命令 `tiup telemetry reset` 重置当前的遥测标示符，以一个新的随机标识符代替之。

### enable

命令 `tiup telemetry enable` 启用遥测。

### disable

命令 `tiup telemetry disable` 停用遥测。
