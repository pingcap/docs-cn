---
title: 日志脱敏
summary: 了解 TiDB 各组件中的日志脱敏
---

# 日志脱敏

TiDB 在提供详细的日志信息时，可能会把数据库敏感的数据（例如用户数据）打印出来，造成数据安全方面的风险。因此 TiDB、TiKV、PD 各组件提供一个了配置项开关，打开开关后，将隐藏日志中包含的用户数据值。各组件相关的配置开关如下所示。

## TiDB 侧

TiDB 侧的日志脱敏需要将 [`global.tidb_redact_log`](/system-variables.md#tidb_redact_log) 的值设为 `1`。该变量值默认为 `0`，即关闭脱敏。

## TiKV 侧

TiKV 侧的日志脱敏需要将 [`security.redact-info-log`](/tikv-configuration-file.md#redact-info-log-从-v408-版本开始引入) 的值设为 `true`。该配置项值默认为 `false`，即关闭脱敏。

## PD 侧

PD 侧的日志脱敏需要将 [`security.redact-info-log`](/pd-configuration-file.md#redact-info-log-从-v500rc-版本开始引入) 的值设为 `true`。该配置项值默认为 `false`，即关闭脱敏。
