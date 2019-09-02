---
title: 上游 MySQL 实例配置前置检查
category: reference
---

# 上游 MySQL 实例配置前置检查

本文介绍了 DM 提供的前置检查功能，此功能用于在数据同步任务启动时提前检测出上游 MySQL 实例配置中可能存在的一些错误。

## 使用命令

`check-task` 命令用于对上游 MySQL 实例配置是否满足 DM 要求进行前置检查。

## 检查内容

上下游数据库用户必须具备相应读写权限。当数据同步任务启动时，DM 会自动检查下列权限和配置：

+ 数据库版本

    - 5.5 < MySQL 版本 < 8.0
    - MariaDB 版本 >= 10.1.2

+ MySQL binlog 配置

    - binlog 是否开启（DM 要求 binlog 必须开启）
    - 是否有 `binlog_format=ROW`（DM 只支持 ROW 格式的 binlog 同步）
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
    - 字符集的兼容性不同，详见 [TiDB 支持的字符集](v2.1/reference/sql/character-set.md)

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
