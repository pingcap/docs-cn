---
title: 使用 TTL (Time to Live) 定期删除过期数据
summary: 了解如何利用 TiDB 的 TTL 功能自动定期删除过期数据。
---

# 使用 TTL (Time to Live) 定期删除过期数据

在应用开发中，一些数据通常只在特定时间内具有价值。例如，验证码通常只需保留几分钟，短链接可能仅在活动期间有效，而访问日志或中间计算结果往往只需保存几个月。

TiDB 的 [TTL (Time to Live)](/time-to-live.md) 功能提供了一种行级别的生命周期控制策略，能帮助你**自动、定期**地删除这些过期数据，而无需编写复杂的定时任务脚本。

## 适用场景

TTL 旨在解决“过期后不再具有业务价值”的数据清理问题，适合以下场景：

- 定期删除验证码、短网址记录
- 定期删除不需要的历史订单
- 自动删除计算的中间结果

> **注意：**
>
> TTL 任务在后台周期执行，因此不保证数据在过期后立即被删除。

## 快速上手

你可以在建表时直接配置 TTL 属性，也可以对现有表进行修改。以下章节列出了使用 TTL 定期删除过期数据的基本示例。完整的示例和 TTL 使用限制，以及 TTL 与其他工具或功能的兼容性请参考 [TTL (Time to Live)](/time-to-live.md)。

### 创建带 TTL 的表

如需创建一个存储即时消息的表 `app_messages`，并且希望消息在创建 3 个月后自动删除，可以执行以下语句：

```sql
CREATE TABLE app_messages (
    id BIGINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    msg_content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) TTL = `created_at` + INTERVAL 3 MONTH;
```

其中，`TTL = ...` 用于定义过期策略，`created_at` 表示数据的创建时间，`INTERVAL 3 MONTH` 设置了表中行的最长存活时间为 3 个月。

### 为现有表增加 TTL

当你已经有一张表 `app_logs`，如需为该表新增自动清理功能（例如只保留 1 个月的数据），可以执行以下语句：

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 1 MONTH;
```

### 调整 TTL 时长

如需调整表 `app_logs` 的 TTL 时长，可以执行以下语句：

```sql
ALTER TABLE app_logs TTL = `created_at` + INTERVAL 6 MONTH;
```

### 关闭 TTL 功能

如需关闭表 `app_logs` 的 TTL 功能，可以执行以下语句：

```sql
ALTER TABLE app_logs TTL_ENABLE = 'OFF';
```

## 另请参阅

- [TTL (Time to Live)](/time-to-live.md)
