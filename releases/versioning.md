---
title: TiDB 版本规则
summary: 了解 TiDB 版本发布的规则。
---

# TiDB 版本规则

<Important>
建议始终升级到当前系列的最新补丁版本。
</Important>

TiDB 提供两个版本系列：

- 长期支持版本
- 开发里程碑版本（自 TiDB v6.0.0 起引入）

关于对 TiDB 版本提供支持服务的标准和规则，参见 [TiDB 版本周期支持策略](https://pingkai.cn/tidb-release-support-policy)。

## 版本命名

TiDB 版本的命名方式为 `X.Y.Z`。`X.Y` 代表一个版本系列。

- 从 TiDB 1.0 起，`X` 每年依次递增，X 的递增代表引入新的功能和改进。
- `Y` 从 0 开始依次递增，Y 的递增代表引入新的功能和改进。
- 一个版本系列首次发版时 `Z` 默认为 0，后续发补丁版本时 `Z` 从 1 开始依次递增。

TiDB v5.0.0 及其之前的版本命名规则，请查看[历史版本](#不再沿用的历史版本号)。

## 长期支持版本

长期支持版本 (Long-Term Support Releases, LTS) 约每六个月发布一次，会引入新功能、改进、缺陷修复和安全漏洞修复。

LTS 命名方式为 `X.Y.Z`，`Z` 默认为 0。

示例版本:

- 6.1.0
- 5.4.0

在 LTS 生命周期内会按需发布补丁版本 (Patch Release)。补丁版本主要包含 bug 修复、安全漏洞修复，不会包含新的功能。

补丁版本命名方式为 `X.Y.Z`。其中，系列版本号 `X.Y` 与对应的 LTS 保持一致，补丁版本号 `Z` 从 1 开始依次递增。

示例版本:

- 6.1.1

<Note>
v5.1.0、v5.2.0、v5.3.0、v5.4.0 发布周期仅间隔两个月，但均为 LTS，提供对应补丁版本。
</Note>

## 开发里程碑版本

开发里程碑版本 (Development Milestone Releases, DMR) 约每两个月发布一次。如遇 LTS 发版，DMR 发版时间顺延两个月。DMR 会引入新的功能、改进和修复。但 TiDB 不提供基于 DMR 的补丁版本，如有相关 bug 会在后续版本系列中陆续修复。

DMR 命名方式为 `X.Y.Z`，`Z` 默认为 0，并添加后缀 `-DMR`。

示例版本:

- 6.0.0-DMR

## TiDB 工具版本

一部分 TiDB 工具与 TiDB server 共同发布，使用相同的版本号体系，例如 TiDB Lightning。一部分 TiDB 工具与 TiDB server 分开发布，并使用独立的版本号体系，例如 TiUP 和 TiDB Operator。

## 不再沿用的历史版本号

### 正式发布版本

正式发布版本 (General Availability Releases, GA) 是 TiDB 当前系列版本的稳定版本，在候选发布版本 (Release Candidate Releases, RC) 之后发布，能够用于生产部署。

示例版本：

- 1.0
- 2.1 GA
- 5.0 GA

### 候选发布版本

候选发布版本 (Release Candidate Releases, RC) 会引入新的功能和改进。RC 版本可用于早期测试，较公开测试版本的稳定性有较大改善，其稳定性足以开始测试，但不适合用于生产部署。

示例版本：

- RC1
- 2.0-RC1
- 3.0.0-rc.1

### 公开测试版本

公开测试版本 (Beta Releases) 会引入新的功能和改进，相对于内部测试版本已有了很大的改进，消除了严重的错误，但还是存在着一些 bug，提供给尝鲜用户，可以用于测试最新的功能。

示例版本：

- 1.1 Beta
- 2.1 Beta
- 4.0.0-beta.1

### 内部测试版本

内部测试版本 (Alpha Releases) 是内部测试版，会引入新的功能和改进。Alpha 版是当前系列版本的最初版本。Alpha 版可能存在一些 bug，提供给尝鲜用户，可以用于测试最新的功能。

示例版本：

- 1.1 Alpha
