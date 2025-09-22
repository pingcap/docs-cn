---
title: TiDB Data Migration 兼容性目录
summary: 了解 TiDB Data Migration (DM) 各版本与上下游各类型数据库的兼容关系。
---

# TiDB Data Migration 兼容性目录

TiDB Data Migration (DM) 数据迁移工具可以将数据从不同类型的数据源迁移到 TiDB 集群。针对各种数据源类型，DM 定义了以下四种兼容性级别：

- **正式支持 (GA)**：该场景已经过验证，并且通过了完整的测试流程。
- **实验支持**：常见的应用场景已验证，但覆盖范围有限，或仅涉及少量用户。可能会偶发问题，因此需要在你的具体场景中验证兼容性。
- **未测试**：DM 尽量保证兼容 MySQL 协议和 binlog，但并非所有 MySQL 分支或版本都包含在 DM 的测试矩阵中。如果某个分支或版本使用了与 MySQL 兼容的协议和 binlog 格式，理论上应能正常工作，但在使用前必须在你自己的环境中验证兼容性。
- **不兼容**：DM 存在已知不兼容的情况，不建议在生产环境中使用。

## 数据源

| 数据源 |级别 | 说明 |
| - | - | - |
| MySQL ≤ 5.5 | 未测试 |
| MySQL 5.6 | 正式支持 | |
| MySQL 5.7 | 正式支持 | |
| MySQL 8.0 | 正式支持 | 不支持 binlog 事务压缩 [Transaction_payload_event](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)。 |
| MariaDB < 10.1.2 | 不兼容 | 与时间类型的 binlog 不兼容。 |
| MariaDB 10.1.2 ~ 10.5.10 | 实验支持 | |
| MariaDB > 10.5.10 | 未测试 | 在绕过[前置检查](/dm/dm-precheck.md)后，理论上大多数情况下可以正常工作。参见 [MariaDB 说明](#mariadb-说明)。 |

### 与外键 CASCADE 操作的不兼容性

- DM 会在目标端创建外键约束，但在应用事务时不会强制执行，因为 DM 设置了会话变量 [`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks)。
- DM 默认**不**支持 `ON DELETE CASCADE` 和 `ON UPDATE CASCADE` 行为，并且不推荐通过 DM 任务会话变量启用 `foreign_key_checks`。如果你的负载依赖于级联操作，**不要假设**级联效果会被复制。

### MariaDB 说明

- 对于 MariaDB **10.5.11 及更高版本**，由于权限名称发生变化（例如 `BINLOG MONITOR`、`REPLICATION SLAVE ADMIN`、`REPLICATION MASTER ADMIN`），DM 前置检查会失败。报错信息显示为 `[code=26005] fail to check synchronization configuration`，出现在复制权限、导出权限和导出连接数检查中。
- 你可以通过在 DM 任务中添加 `ignore-checking-items: ["all"]` 来**绕过前置检查**。详情参见 [DM 前置检查](/dm/dm-precheck.md)。

## 目标数据库

> **警告：**
>
> 不建议使用 DM v5.3.0。在 DM v5.3.0 中启用 GTID 复制但未启用 relay log 时，尽管概率较低，但可能会导致数据复制失败。

| 目标数据库 | 级别 | DM 版本 |
| - | - | - |
| TiDB 8.x | 正式支持 | 最低 5.3.1 |
| TiDB 7.x | 正式支持 | 最低 5.3.1 |
| TiDB 6.x | 正式支持 | 最低 5.3.1 |
| TiDB 5.4 | 正式支持 | 最低 5.3.1 |
| TiDB 5.3 | 正式支持 | 最低 5.3.1 |
| TiDB 5.2 | 正式支持 | 最低 2.0.7，建议 5.4 版本 |
| TiDB 5.1 | 正式支持 | 最低 2.0.4，建议 5.4 版本 |
| TiDB 5.0 | 正式支持 | 最低 2.0.4，建议 5.4 版本 |
| TiDB 4.x | 正式支持 | 最低 2.0.1，建议 2.0.7 版本 |
| TiDB 3.x | 正式支持 | 最低 2.0.1，建议 2.0.7 版本 |
| MySQL | 实验支持 | |
| MariaDB | 实验支持 | |
