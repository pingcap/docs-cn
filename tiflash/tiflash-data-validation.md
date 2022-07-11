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

TiFlash 的数据校验功能基于 DTFile（即 DeltaTree File）提供。DTFile 是 TiFlash 落盘数据的存储文件，共有三版格式：

| 版本 | 状态 | 校验机制 | 备注 |
| :-- | :-- | :-- |:-- |
| V1 | 已废弃 | 在数据文件中内嵌哈希值 | |
| V2 | v6.0.0 之前的默认格式 | 在数据文件中内嵌哈希值 | 在 V1 的基础上增加了列数据的统计信息 |
| V3 | v6.0.0 及之后的默认格式 | 包含元数据，标记数据校验，支持多种哈希算法 | 于 v5.4 版本引入 |

DTFile 存储在数据文件夹目录下的 stable 文件夹内。目前启用的格式均为文件夹形式，即具体数据均储存在名字类似 `dmf_<file id>` 的文件夹下的多个子文件中。

### 使用数据校验

TiFlash 支持自动和手动进行数据校验：

- 自动数据校验 （`storage.format_version` 配置项）：
    - v6.0.0 之后默认使用 DTFile V3 版本校验机制。
    - v6.0.0 之前默认使用 DTFile V2 版本校验机制。
    - 如需切换版本校验机制，参见 [TiFlash 配置文件](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)。默认配置经过大量测试，不推荐修改。
- 手动数据校验，参见 [DTTool 使用文档](/tiflash/tiflash-command-line-flags.md#dttool-inspect)。

> **警告：**
>
> 设置使用 V3 版本后，新生成的 DTFile 将无法被 v5.4.0 以前 TiFlash 直接正常读取。v5.4.0 后 TiFlash 同时支持 V2，V3 版本，不会主动进行版本的升降级。如果需要迁移到新的版本，或者需要回退到旧的版本，需要手动使用 DTTool 进行[版本切换](/tiflash/tiflash-command-line-flags.md#dttool-migrate)。

### 校验工具

除了 TiFlash 在读取所需数据时进行的自动校验，在 v5.4.0 版本时还引入了手动检查文件完整性的工具，详情请见 DTTool 的[使用文档](/tiflash/tiflash-command-line-flags.md#dttool-inspect)。
