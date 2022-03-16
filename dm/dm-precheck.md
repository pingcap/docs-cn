---
title: 上游 MySQL 实例配置前置检查
summary: 了解上游 MySQL 实例配置前置检查。
---

# 上游 MySQL 实例配置前置检查

本文介绍了 DM 提供的前置检查功能，此功能用于在数据迁移任务启动时提前检测出上游 MySQL 实例配置中可能存在的一些错误。

## 使用命令

`check-task` 命令用于对上游 MySQL 实例配置是否满足 DM 要求进行前置检查。

## 检查内容

上下游数据库用户必须具备相应读写权限。当数据迁移任务启动时，DM 会自动检查下列权限和配置：

+ 数据库版本

    - MySQL 版本 > 5.5
    - MariaDB 版本 >= 10.1.2

    > **警告：**
    >
    > 支持从 MySQL v8.0 迁移数据是 DM v2.0 及以上版本的实验特性，不建议在生产环境下使用。

+ 数据库配置

    - 是否设置 `server_id`

+ MySQL binlog 配置

    - binlog 是否开启（DM 要求 binlog 必须开启）
    - 是否有 `binlog_format=ROW`（DM 只支持 ROW 格式的 binlog 迁移）
    - 是否有 `binlog_row_image=FULL`（DM 只支持 `binlog_row_image=FULL`）

+ 上游 MySQL 实例用户的权限

    DM 配置中的 MySQL 用户至少需要具备以下权限：

    - REPLICATION SLAVE
    - REPLICATION CLIENT
    - RELOAD
    - SELECT

+ 上游 MySQL 表结构的兼容性

    TiDB 和 MySQL 的兼容性存在以下一些区别：

    - TiDB 不支持外键
    - 字符集的兼容性不同，详见 TiDB 支持的字符集

    DM 还会检查上游表中是否存在主键或唯一键约束，在 v1.0.7 版本引入。

+ 上游 MySQL 多实例分库分表的一致性

    + 所有分表的表结构是否一致，检查内容包括：

        - Column 数量
        - Column 名称
        - Column 位置
        - Column 类型
        - 主键
        - 唯一索引

    + 分表中自增主键冲突检查

        - 在两种情况下会造成检查失败：

            - 分表存在自增主键，且自增主键 column 类型不为 bigint
            - 分表存在自增主键，自增主键 column 类型为 bigint，但没有为其配置列值转换

        - 其他情况下检查将成功

### 关闭检查项

DM 会根据任务类型进行相应检查，用户可以在任务配置文件中使用 `ignore-checking-items` 配置关闭检查。`ignore-checking-items` 是一个列表，其中可能的取值包括：

| 取值   | 含义   |
| :----  | :-----|
| all | 关闭所有检查 |
| dump_privilege | 关闭检查上游 MySQL 实例用户的 dump 相关权限 |
| replication_privilege | 关闭检查上游 MySQL 实例用户的 replication 相关权限 |
| version | 关闭检查上游数据库版本 |
| server_id | 关闭检查上游数据库是否设置 server_id |
| binlog_enable | 关闭检查上游数据库是否已启用 binlog |
| binlog_format | 关闭检查上游数据库 binlog 格式是否为 ROW |
| binlog_row_image | 关闭检查上游数据库 binlog_row_image 是否为 FULL|
| table_schema | 关闭检查上游 MySQL 表结构的兼容性 |
| schema_of_shard_tables | 关闭检查上游 MySQL 多实例分库分表的表结构一致性 |
| auto_increment_ID | 关闭检查上游 MySQL 多实例分库分表的自增主键冲突 |
