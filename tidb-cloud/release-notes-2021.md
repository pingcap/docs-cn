---
title: 2021 年 TiDB Cloud 发布说明
summary: 了解 2021 年 TiDB Cloud 的发布说明。
---

# 2021 年 TiDB Cloud 发布说明

本页列出了 2021 年 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 的发布说明。

## 2021 年 12 月 28 日

新功能：

* 支持[将 Apache Parquet 文件从 Amazon S3 或 GCS 导入到 TiDB Cloud](/tidb-cloud/import-parquet-files.md)

Bug 修复：

* 修复了向 TiDB Cloud 导入超过 1000 个文件时发生的导入错误
* 修复了 TiDB Cloud 允许将数据导入到已有数据的现有表的问题

## 2021 年 11 月 30 日

通用变更：

* 将 TiDB Cloud 的开发者层级升级到 [TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)

新功能：

* 支持[为您的 TiDB Cloud 项目添加 VPC CIDR](/tidb-cloud/set-up-vpc-peering-connections.md)

改进：

* 提升开发者层级的监控能力
* 支持将自动备份时间设置为与开发者层级集群的创建时间相同

Bug 修复：

* 修复开发者层级中由于磁盘满导致的 TiKV 崩溃问题
* 修复 HTML 注入漏洞

## 2021 年 11 月 8 日

* 发布 [开发者层级](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)，为您提供 TiDB Cloud 一年的免费试用

    每个开发者层级集群都是一个功能齐全的 TiDB 集群，并包含以下内容：

    * 一个 TiDB 共享节点
    * 一个 TiKV 共享节点（具有 500 MiB 的 OLTP 存储）
    * 一个 TiFlash 共享节点（具有 500 MiB 的 OLAP 存储）

  从[这里](/tidb-cloud/tidb-cloud-quickstart.md)开始。

## 2021 年 10 月 21 日

* 开放个人邮箱账户的用户注册
* 支持[从 Amazon S3 或 GCS 导入或迁移到 TiDB Cloud](/tidb-cloud/import-csv-files.md)

## 2021 年 10 月 11 日

* 支持[查看和导出 TiDB Cloud 的账单明细](/tidb-cloud/tidb-cloud-billing.md#billing-details)，包括每个服务和每个项目的成本
* 修复了 TiDB Cloud 内部功能的几个问题

## 2021 年 9 月 16 日

* 将新部署集群的默认 TiDB 版本从 5.2.0 升级到 5.2.1。 有关 5.2.1 的详细更改，请参阅 [5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1) 发行说明。

## 2021 年 9 月 2 日

* 将新部署集群的默认 TiDB 版本从 5.0.2 升级到 5.2.0。 有关 TiDB 5.1.0 和 5.2.0 功能的详细信息，请参阅 [5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0) 和 [5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0) 发行说明。
* 修复了 TiDB Cloud 内部功能的几个问题。

## 2021 年 8 月 19 日

* 修复了 TiDB Cloud 内部功能的几个问题。此版本不带来任何用户行为的更改。

## 2021 年 8 月 5 日

* 支持组织角色管理。组织所有者可以根据需要配置组织成员的权限。
* 支持组织内多个项目的隔离。组织所有者可以根据需要创建和管理项目，并且项目之间的成员和实例支持网络和权限隔离。
* 优化账单，以显示当月和上个月的每个项目的账单明细。

## 2021 年 7 月 22 日

* 优化添加信用卡的用户体验
* 加强信用卡的安全管理
* 修复集群从备份恢复后无法正常计费的问题

## 2021 年 7 月 6 日

* 将新部署集群的默认 TiDB 版本从 4.0.11 升级到 5.0.2。此次升级带来了显著的性能和功能改进。详情请参见[此处](https://docs.pingcap.com/tidb/stable/release-5.0.0)。

## 2021 年 6 月 25 日

* 修复了 [TiDB Cloud 定价](https://www.pingcap.com/pricing/) 页面上 **选择区域** 功能无法使用的问题

## 2021 年 6 月 24 日

* 修复将 Aurora 快照导入 TiDB 实例时 Parquet 文件的解析错误
* 修复 PoC 用户创建集群并更改集群配置时，预计工时未更新的问题

## 2021 年 6 月 16 日

* 在注册账户时，**中国**已添加到**国家/地区**下拉列表中

## 2021 年 6 月 14 日

* 修复将 Aurora 快照导入 TiDB 实例时挂载 EBS 错误的bug

## 2021 年 5 月 10 日

通用

* TiDB Cloud 现在处于公开预览阶段。您可以[注册](https://tidbcloud.com/signup)并选择以下试用选项之一：

    * 48小时免费试用
    * 2周 PoC 免费试用
    * 预览按需

管理控制台

* 注册流程中增加了邮箱验证和反机器人 reCAPTCHA
* [TiDB Cloud 服务协议](https://pingcap.com/legal/tidb-cloud-services-agreement) 和 [PingCAP 隐私政策](https://pingcap.com/legal/privacy-policy/) 已更新
* 您可以通过在控制台中填写申请表来申请 [PoC](/tidb-cloud/tidb-cloud-poc.md)
* 您可以通过 UI 将示例数据导入到 TiDB Cloud 集群中
* 不允许使用相同名称的集群，以避免混淆
* 您可以通过点击 **支持** 菜单中的 **提供反馈** 来提供反馈
* 数据备份和恢复功能适用于 PoC 和按需试用选项
* 为免费试用和 PoC 添加了积分计算器和积分使用情况仪表板。所有试用选项均免除数据存储和传输成本