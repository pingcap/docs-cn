---
title: 导出和导入集群的数据源和任务配置
summary: 了解 TiDB Data Migration 导出和导入集群的数据源和任务配置。
---

# 导出和导入集群的数据源和任务配置

`config` 命令用于导出和导入集群的数据源和任务配置。

> **注意：**
>
> 对于 v2.0.5 版本之前的集群，可使用 v2.0.5 版本及之后的 dmctl 导出和导入集群的数据源和任务配置文件。

{{< copyable "" >}}

```bash
» help config
Commands to import/export config

Usage:
  dmctl config [command]

Available Commands:
  export      Export the configurations of sources and tasks.
  import      Import the configurations of sources and tasks.

Flags:
  -h, --help   help for config

Global Flags:
  -s, --source strings   MySQL Source ID.

Use "dmctl config [command] --help" for more information about a command.
```

## 导出集群的数据源和任务配置

使用 `export` 子命令导出集群的数据源和任务配置到指定文件夹中。

{{< copyable "" >}}

```bash
config export [--dir directory]
```

### 参数解释

- `dir`：
    - 可选
    - 指定导出文件夹路径
    - 默认值为 `./configs`

### 返回结果示例

{{< copyable "" >}}

```bash
config export -d /tmp/configs
```

```
export configs to directory `/tmp/configs` succeed
```

## 导入集群的数据源和任务配置

使用 `import` 子命令从指定文件夹中导入集群的数据源和任务配置。

{{< copyable "" >}}

```bash
config import [--dir directory]
```

> **注意：**
>
> 对于 v2.0.2 版本之后的集群，暂不支持自动导入 relay worker 的相关配置，可以手动使用 `start-relay` 命令开启 relay log。

### 参数解释

- `dir`：
    - 可选
    - 指定导入文件夹路径
    - 默认值为 `./configs`

### 返回结果示例

{{< copyable "" >}}

```bash
config import -d /tmp/configs
```

```
start creating sources
start creating tasks
import configs from directory `/tmp/configs` succeed
```
