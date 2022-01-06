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

### 表意清晰

### 用户视角

## 示例

| 类别                                | 修改前                                                | 修改后 | 说明 |
| :-------------------------------- | :------------------------------------------------- | :-- | :- |
| Compatibility change              |  copr: cast invalid utf8 string to real bug fix |   Before v4.0.16, when TiDB converts an illegal UTF-8 string to a Real type, an error is reported directly. Starting from v4.0.16, TiDB processes the conversion according to the legal UTF-8 prefix in the string  | 来源：[tikv/tikv#9870](https://github.com/tikv/tikv/pull/9870) <br/> <ul><li>描述过于简略，表意不完整</li><li>该改动涉及用户可感知的代码行为改动，会造成兼容性变化，但是未在 release notes 中体现出来</li></ul>   |
| Compatibility change              |   sink: fix kafka max message size inaccurate issue                                                |  Change the default value of Kafka Sink max-message-bytes to 1 MB to prevent TiCDC from sending too large messages to Kafka clusters   |  来源：[pingcap/tiflow#2962](https://github.com/pingcap/tiflow/issues/2962) <br/> <ul><li>描述过于简略，表意不完整</li><li>该改动修改了参数默认值，造成兼容性更改，但是未在 release notes 中体现出来</li></ul> |
| Compatibility change              |  cdc/sink: adjust kafka initialization logic                                                  |  Change the default value of Kafka Sink partition-num to 3 so that TiCDC distributes messages across Kafka partitions more evenly   | 来源：[pingcap/tiflow#3565](https://github.com/pingcap/tiflow/pull/3565) <br/> <ul><li>描述过于简略，表意不完整</li><li>该改动修改了参数默认值，造成兼容性更改，但是未在 release notes 中体现出来</li></ul>   |
| Compatibility change              |  cmd: hide --sort-dir in changefeed command. (deprecated warning exists)                                                | Deprecate `--sort-dir` in the `cdc cli changefeed` command. Instead, users can set `--sort-dir` in the `cdc server` command.    |  来源：[pingcap/tiflow#1795](https://github.com/pingcap/tiflow/pull/1795) <br/> <ul><li>描述过于简略，表意不完整</li><li>该改动修改了参数默认值，造成兼容性更改，但是未在 release notes 中体现出来</li></ul>  |
| Improvement 或 Feature enhancement |                                                    |     |    |
| Improvement 或 Feature enhancement |                                                   |     |    |
| Improvement 或 Feature enhancement |                                                    |     |    |
| Improvement 或 Feature enhancement |                                                   |     |    |
| Bug 修复                            |                                                    |     |    |
| Bug 修复                            |                                                   |     |    |
| Bug 修复                            |                                                    |     |    |
| Bug 修复                            |                                                   |     |    |
