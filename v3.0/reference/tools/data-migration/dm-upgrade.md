---
title: DM 版本升级
category: reference
aliases: ['/docs-cn/tools/dm/dm-upgrade/']
---

# DM 版本升级

本文档主要介绍各不完全兼容的 DM (Data Migration) 版本间的升级操作步骤。

假设依时间先后顺序存在 V-A、V-B、V-C 3 个互不兼容的版本，现在需要从 V-A 升级到 V-C。定义从 V-A 升级到 V-B 的操作为 Upgrade-A-B，从 V-B 升级到 V-C 的操作为 Upgrade-B-C。

- 如果 Upgrade-A-B 与 Upgrade-B-C 之间存在交叠（如同一个配置项的不同变更），则推荐先执行 Upgrade-A-B 升级到 V-B，升级完成后再执行 Upgrade-B-C 升级到 V-C。
- 如果 Upgrade-A-B 与 Upgrade-B-C 之间不存在交叠，则可将 Upgrade-A-B 与 Upgrade-B-C 的操作合并为 Upgrade-A-C，执行后直接从 V-A 升级到 V-C。

> **注意：**
>
> - 若无特殊说明，各版本的升级操作均为从前一个有升级指引的版本向当前版本升级。
> - 若无特殊说明，各升级操作示例均假定已经下载了对应版本的 DM 和 DM-Ansible 且 DM binary 存在于 DM-Ansible 的相应目录中（下载 DM binary 可以参考[更新组件版本](/v3.0/reference/tools/data-migration/cluster-operations.md#更新组件版本)）。
> - 若无特殊说明，各升级操作示例均假定升级前已停止所有同步任务，升级完成后手动重新启动所有同步任务。
> - 以下版本升级指引逆序展示。

## 升级到 v1.0.0-10-geb2889c9 (1.0 GA)

### 版本信息

```bash
Release Version: v1.0.0-10-geb2889c9
Git Commit Hash: eb2889c9dcfbff6653be9c8720a32998b4627db9
Git Branch: release-1.0
UTC Build Time: 2019-09-06 03:18:48
Go Version: go version go1.12 linux/amd64
```

### 主要变更

- 常见的异常场景支持自动尝试恢复同步任务
- 提升 DDL 语法兼容性
- 修复上游数据库连接异常时可能丢失数据的 bug

### 升级操作示例

1. 下载新版本 DM-Ansible, 确认 `inventory.ini` 文件中 `dm_version = v1.0.0`
2. 执行 `ansible-playbook local_prepare.yml` 下载新的 DM binary 到本地
3. 执行 `ansible-playbook rolling_update.yml` 滚动升级 DM 集群组件
4. 执行 `ansible-playbook rolling_update_monitor.yml` 滚动升级 DM 监控组件

> **注意：**
>
> 更新至 DM 1.0 GA 版本时，需要确保 DM 所有组件 (dmctl/DM-master/DM-worker) 同时升级。不支持部分组件升级使用。

## 升级到 v1.0.0-rc.1-12-gaa39ff9

### 版本信息

```bash
Release Version: v1.0.0-rc.1-12-gaa39ff9
Git Commit Hash: aa39ff981dfb3e8c0fa4180127246b253604cc34
Git Branch: dm-master
UTC Build Time: 2019-07-24 02:26:08
Go Version: go version go1.11.2 linux/amd64
```

### 主要变更

从此版本开始，将对所有的配置进行严格检查，遇到不识别的配置会报错，以确保用户始终准确地了解自己的配置。

### 升级操作示例

启动 DM-master 或 DM-worker 前，必须确保已经删除废弃的配置信息，且没有多余的配置项，否则会启动失败。可根据失败信息删除多余的配置。
可能遗留的废弃配置:

- `dm-worker.toml` 中的 `meta-file`
- `task.yaml` 中的 `mysql-instances` 中的 `server-id`