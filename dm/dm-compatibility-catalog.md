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
| MySQL ≤ 5.5              | 未测试              |      |
| MySQL 5.6                | 正式支持            |      |
| MySQL 5.7                | 正式支持            |      |
| MySQL 8.0                | 正式支持            | 不支持 [binlog 事务压缩 (`Transaction_payload_event`)](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)。 |
| MySQL 8.1 ~ 8.3          | 未测试              | 不支持 [binlog 事务压缩 (`Transaction_payload_event`)](https://dev.mysql.com/doc/refman/8.0/en/binary-log-transaction-compression.html)。     |
| MySQL 8.4                | 实验支持（适用于从 v8.5.6 起的 TiDB 版本） | 不支持 [binlog 事务压缩 (`Transaction_payload_event`)](https://dev.mysql.com/doc/refman/8.4/en/binary-log-transaction-compression.html)。 |
| MySQL 9.x                | 未测试              |      |
| MariaDB < 10.1.2         | 不兼容              | 与时间类型的 binlog 不兼容。 |
| MariaDB 10.1.2 ~ 10.5.10 | 实验支持            |      |
| MariaDB > 10.5.10        | 未测试              | 在绕过[前置检查](/dm/dm-precheck.md)后，理论上大多数情况下可以正常工作。参见 [MariaDB 说明](#mariadb-说明)。 |

### 外键 `CASCADE` 操作

> **警告：**
>
> 该功能为实验特性。不建议在生产环境中使用。该功能可能会在未事先通知的情况下发生变化或删除。如果发现 bug，请在 GitHub 上提 [issue](https://github.com/pingcap/tiflow/issues) 反馈。

从 v8.5.6 开始，DM 以**实验特性**支持同步包含外键约束的表。该支持包括以下改进：

- **安全模式**：在安全模式执行期间，DM 会在每个批次中设置 `foreign_key_checks=0`，并对未修改主键或唯一键值的 `UPDATE` 语句跳过冗余的 `DELETE` 步骤。这可以防止 `REPLACE INTO`（其内部执行为 `DELETE` + `INSERT`）在子表行上触发非预期的 `ON DELETE CASCADE` 效果。详情参见 [DM 安全模式](/dm/dm-safe-mode.md#外键处理-从-v856-版本开始引入)。
- **多 worker 因果关系**：当 `worker-count > 1` 时，DM 会在任务启动时从下游 schema 中读取外键关系并注入因果键。这可确保父表行的 DML 操作先于其依赖的子表行操作完成，从而在多个 worker 之间保持 binlog 顺序。

同步包含外键约束的表存在以下限制：

- 在安全模式下，DM 不支持修改主键或唯一键值的 `UPDATE` 语句。任务会暂停，并报错：`safe-mode update with foreign_key_checks=1 and PK/UK changes is not supported`。如需同步此类语句，请将 `safe-mode` 设置为 `false`。
- 当 `foreign_key_checks=1` 时，DM 不支持在同步过程中执行创建、修改或删除外键约束的 DDL 语句。
- 当 `worker-count > 1` 时，不支持表路由。如果对包含外键的表使用表路由，请将 `worker-count` 设置为 `1`。
- 黑白名单过滤 (Block & Allow List) 必须包含外键依赖链中的所有祖先表。如果祖先表被过滤，在增量复制期间任务会报错并暂停。
- 源端与下游的外键元数据必须保持一致。如果检测到不一致，请运行 `binlog-schema update --from-target` 以重新同步元数据。
- 当 `UPDATE` 修改主键或唯一键值时，安全模式下无法正确同步 `ON UPDATE CASCADE`。这是因为 DM 会将此类语句改写为 `DELETE` + `REPLACE`，从而触发 `ON DELETE` 行为而不是 `ON UPDATE` 行为。在这种情况下，DM 会拒绝该语句并暂停任务。未修改键值的 `UPDATE` 语句可以被正确同步。

在 v8.5.6 之前的版本中，DM 会在下游创建外键约束，但由于其将会话变量 [`foreign_key_checks=OFF`](/system-variables.md#foreign_key_checks)，这些约束不会被强制执行。因此，级联操作不会被同步到下游。

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
