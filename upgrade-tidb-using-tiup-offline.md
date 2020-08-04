---
title: 使用 TiUP 离线镜像升级 TiDB
aliases: ['/docs-cn/dev/upgrade-tidb-using-tiup-offline/']
---

# 使用 TiUP 离线镜像升级 TiDB

本文档适用于通过升级 TiUP 离线镜像升级 TiDB 集群，升级步骤如下。

## 1. 更新 TiUP 离线镜像

如果用户希望升级更新本地的 TiUP 离线镜像，可以参考[使用 TiUP 离线部署 TiDB 集群](/production-offline-deployment-using-tiup.md)的步骤 1 与步骤 2 下载部署新版本的 TiUP 离线镜像。在执行 `local_install.sh` 后，TiUP 会完成覆盖升级。

随后，需要按照 `local_install.sh` 执行的结果，重新声明全局环境变量，并将 TIUP_MIRRORS 指向执行 `local_install.sh` 命令时输出的离线镜像包的位置 `/path/to/mirror`。

{{< copyable "shell-regular" >}}

```bash
source .bash_profile
export TIUP_MIRRORS=/path/to/mirror
```

此时离线镜像已经更新成功。如果覆盖后发现 TiUP 运行报错，可能是 manifest 未更新导致，可尝试 `rm -rf ~/.tiup/manifests` 后再使用 TiUP。

## 2. 升级 TiDB 集群

在更新本地镜像后，可参考[使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md#使用-tiup-升级-tidb)升级 TiDB 集群。

> **注意：**
>
> TiUP 及 TiDB（v4.0.2 起）默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。
