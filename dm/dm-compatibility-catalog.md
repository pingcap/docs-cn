---
title: TiDB Data Migration 兼容性目录
summary: 了解 DM 各版本与上下游各类型数据库的兼容关系
---

# TiDB Data Migration 兼容性目录

DM 数据同步软件支持从不同类型的数据源迁移到 TiDB 集群。针对各种类型，产品支持程度可以分为三个级别：

- **GA**。正式支持，指该场景经过验证，并且通过完整的测试流程；
- **Experimental**。实验性支持，即虽然通过部分验证，但测试尚未覆盖所有预设场景或使用者较少，存在少量场景下可能出错的风险；
- **Unknown**。未知，DM 在迭代过程中尽量保证 MySQL 协议的兼容性，但由于资源限制，无法测试所有 MySQL 衍生版本。因此虽然技术原理上是兼容的，但是并未经完整测试，因此需要使用前自行验证；
- **Incompatible**。 不兼容的，指已发现明确存在无法兼容的情况，建议不要在生产环境中使用。

## 数据源

|数据源|级别|
|-|-|
|MySQL ≤ 5.5|Unknown|
|MySQL 5.6|GA|
|MySQL 5.7|GA|
|MySQL 8.0|GA|
|MariaDB ＜ 10.1.2|Incompatible|
|MariaDB 10.1.2 ~ 10.5.10|Experimental|
|MariaDB ≥ 10.5.10|Incompatible|

## 目标数据库

|数据源|级别|
|-|-|
|TiDB 3.x|GA|
|TiDB 4.x|GA|
|TiDB 5.0|GA|
|TiDB 5.1|GA|
|TiDB 5.2|GA|
|TiDB 5.3|GA|
|TiDB 5.4|GA|
|MySQL|Unknown|
|MariaDB|Unknown|
