---
title: TiFlash 数据校验
summary: 了解 TiFlash 的数据校验机制以及相关的工具。
---

# TiFlash 数据校验

本文档介绍 TiFlash 的数据校验机制以及相关的工具。

## 使用场景

数据损坏通常意味着严重的硬件故障。在这种情形下，即使尝试自主修复，也会使得数据的可靠性下降。TiFlash 默认对数据文件进行基础的校验，使用固定的 City128 算法。一旦发现数据校验不符的情况，TiFlash 将立刻报错退出，避免因错误数据造成次生灾害。此时，您需要手动检查干预并重新同步数据，才可以恢复节点的使用。

自 v5.4.0 起，TiFlash 完善了数据校验功能，默认使用 XXH3 算法，并允许用户调整校验帧大小和校验算法。

## 校验机制简介

DTFile（即 DeltaTree File）是 TiFlash 落盘数据的存储文件。TiFlash 的数据校验机制基于 DTFile，目前该校验机制共有三个版本：

| 数据校验机制版本 | 状态 | 校验机制 | 备注 |
| :-- | :-- | :-- |:-- |
| V1 | 已废弃 | 在数据文件中内嵌哈希值 | |
| V2 | v6.0.0 之前的默认校验机制 | 在数据文件中内嵌哈希值 | 在 V1 的基础上增加了列数据的统计信息 |
| V3 | v6.0.0 及之后的默认校验机制 | 包含元数据，标记数据校验，支持多种哈希算法 | 于 v5.4 版本引入 |

> **注意：**
>
> 上表中的 V1、V2、V3 指 TiFlash 对 DTFile 数据进行校验时采用的校验机制版本，并非 DTFile 存储格式配置项 [`storage.format_version`](/tiflash/tiflash-configuration.md#format_version) 的取值。

DTFile 存储在数据文件夹目录下的 stable 文件夹内。目前启用的格式均为文件夹形式，即具体数据均储存在名字类似 `dmf_<file id>` 的文件夹下的多个子文件中。

### 使用数据校验

TiFlash 支持自动和手动进行数据校验：

- 自动数据校验：

    TiFlash 在读写 DTFile 数据时，会自动进行数据校验。针对不同的 [`storage.format_version`](/tiflash/tiflash-configuration.md#format_version) 的 DTFile，TiFlash 采用的数据校验机制版本不同：

    - 当 `storage.format_version` 为 `2` 时，新生成的 DTFile 使用 V2 校验机制。在 TiFlash v6.0.0 之前，该配置项的默认值为 `2`。
    - 当 `storage.format_version` 为 `3` 或更高时，新生成的 DTFile 使用 V3 校验机制。从 TiFlash v6.0.0 开始，该配置项的默认值为 `3` 或更高，具体取决于 TiFlash 版本。
    - 如需查看当前 TiFlash 版本中 `storage.format_version` 的默认值和可选值，参见 [TiFlash 配置文件](/tiflash/tiflash-configuration.md#format_version)。默认配置经过大量测试，不推荐修改。
- 手动数据校验：

    使用 `dttool inspect` 检查 DTFile 的完整性。详请参见 [DTTool 文档](/tiflash/tiflash-command-line-flags.md#dttool-inspect)。

> **警告：**
>
> 当设置 `storage.format_version` 为 `3` 或更高时，新生成的 DTFile 将使用 V3 校验机制，无法被 v5.4.0 以前的 TiFlash 直接正常读取。从 v5.4.0 开始，TiFlash 可以读取和校验采用 V2 或 V3 校验机制的 DTFile，并根据 DTFile 自身的格式使用相应的校验机制，但不会自动转换已有 DTFile 的文件格式。如需升级或降级 DTFile 的文件格式，需要使用 DTTool 手动迁移，参见 [DTTool migrate](/tiflash/tiflash-command-line-flags.md#dttool-migrate)。

### 校验工具

除了 TiFlash 在读取所需数据时进行的自动校验，在 v5.4.0 版本时还引入了手动检查文件完整性的工具，详情请见 DTTool 的[使用文档](/tiflash/tiflash-command-line-flags.md#dttool-inspect)。
