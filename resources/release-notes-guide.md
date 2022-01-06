---
title: TiDB Release Notes 写作简要指南
summary: 本文简要介绍如何
---

# TiDB Release Notes 写作简要指南

## 面向对象

## Release notes 写作原则

* 类别明确

* 表意清晰

* 用户视角

包括参考 GitHub issue

### 类别明确

Release notes 可分为以下 3 类：

| 类别                                           | 说明 | 典型示例 |
| :------------------------------------------- | :- | :--- |
| Compatibility change（兼容性更改）                  |    |      |
| Improvement（提升改进）或 Feature enhancement（功能增强） |    |      |
| Bug fix（Bug 修复）                              |    |      |

### 表意完整清晰

### 用户视角

## 示例

| 类别                                | 修改前                                                                     | 说明                                                                                                                                | 修改后                                                                                                                                                                                                              |
| :-------------------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Compatibility change              | copr: cast invalid utf8 string to real bug fix                          | 来源：[tikv/tikv#9870](https://github.com/tikv/tikv/pull/9870) <br/> <ul><li>类别明确：❌</li><li>表意清晰：❌</li><li>用户视角：❌</li></ul> | Before v4.0.16, when TiDB converts an illegal UTF-8 string to a Real type, an error is reported directly. Starting from v4.0.16, TiDB processes the conversion according to the legal UTF-8 prefix in the string |
| Compatibility change              | sink: fix kafka max message size inaccurate issue                       | 来源：[pingcap/tiflow#2962](https://github.com/pingcap/tiflow/issues/2962) <br/> <ul><li>类别明确：✅</li><li>表意清晰：❌</li><li>用户视角：❌</li></ul> | Change the default value of Kafka Sink max-message-bytes to 1 MB to prevent TiCDC from sending too large messages to Kafka clusters                                                                              |
| Compatibility change              | cdc/sink: adjust kafka initialization logic                             | 来源：[pingcap/tiflow#3565](https://github.com/pingcap/tiflow/pull/3565) <br/> <ul><li>类别明确：❌</li><li>表意清晰：❌</li><li>用户视角：❌</li></ul>   | Change the default value of Kafka Sink partition-num to 3 so that TiCDC distributes messages across Kafka partitions more evenly                                                                                 |
| Compatibility change              | cmd: hide --sort-dir in changefeed command. (deprecated warning exists) | 来源：[pingcap/tiflow#1795](https://github.com/pingcap/tiflow/pull/1795) <br/> <ul><li>类别明确：✅</li><li>表意清晰：❌</li><li>用户视角：❌</li></ul>   | Deprecate `--sort-dir` in the `cdc cli changefeed` command. Instead, users can set `--sort-dir` in the `cdc server` command.                                                                                     |
| Improvement 或 Feature enhancement | Not use the stale read request's `start_ts` to update `max_ts` to avoid commit request keep retrying                                                                        |   来源：[tikv/tikv#10451](https://github.com/tikv/tikv/pull/10451) <br/> <ul><li>类别明确：✅</li><li>表意清晰：✅</li><li>用户视角：✅</li></ul>                                                                                                                                |  Avoid excessive commit request retrying by not using the Stale Read request's start_ts to update max_ts                                                                                                                                                                                                                |
| Improvement 或 Feature enhancement |                                                                         |                                                                                                                                   |                                                                                                                                                                                                                  |
| Improvement 或 Feature enhancement |                                                                         |                                                                                                                                   |                                                                                                                                                                                                                  |
| Improvement 或 Feature enhancement |                                                                         |                                                                                                                                   |                                                                                                                                                                                                                  |
| Bug 修复                            |  lock_resolver: avoid pessimistic transactions using resolveLocksForWrite                                                                       |  来源：[tikv/client-go#213](https://github.com/tikv/client-go/pull/213) <br/> <ul><li>类别明确：❌</li><li>表意清晰：✅</li><li>用户视角：❌</li></ul>                                                                                                                                 |  Fix the issue that committing pessimistic transactions might cause write conflict                                                                                                                                      |
| Bug 修复                            |   retry when meeting stablish conn fails                                                                      |  来源：N/A <br/> <ul><li>类别明确：✅</li><li>表意清晰：❌</li><li>用户视角：❌</li></ul>                                                                                                                                 |  Fix the issue of unexpected results when TiFlash fails to establish MPP connections                                                                                                                                                                                                                |
| Bug 修复                            |                                                                         |                                                                                                                                   |                                                                                                                                                                                                                  |
| Bug 修复                            |                                                                         |                                                                                                                                   |                                                                                                                                                                                                                  |
