---
title: 数据迁移概述
category: how-to
---

# 数据迁移概述

本文档介绍了 TiDB 提供的数据迁移工具，以及不同迁移场景下如何选择迁移工具，从而将数据从 MySQL 或 CSV 数据源迁移到 TiDB。

## 迁移工具

在上述数据迁移过程中会用到如下工具：

- [Mydumper](/v2.1/reference/tools/mydumper.md)：用于从 MySQL 导出数据。建议使用 Mydumper，而非 mysqldump。
- [Loader](/v2.1/reference/tools/loader.md)：用于将 Mydumper 导出格式的数据导入到 TiDB。
- [Syncer](/v2.1/reference/tools/syncer.md)：用于将数据从 MySQL 增量同步到 TiDB。
- [DM (Data Migration)](/v2.1/reference/tools/data-migration/overview.md)：集成了 Mydumper、Loader、Syncer 的功能，支持 MySQL 数据的全量导出和到 TiDB 的全量导入，还支持 MySQL binlog 数据到 TiDB 的增量同步。
- [TiDB Lightning](/v2.1/reference/tools/tidb-lightning/overview.md)：用于将全量数据高速导入到 TiDB 集群。例如，如果要导入超过 1TiB 的数据，使用 Loader 往往需花费几十个小时，而使用 TiDB-Lightning 的导入速度至少是 Loader 的三倍。

## 迁移场景

本小节将通过几个示例场景来说明如何选择和使用 TiDB 的迁移工具。

### MySQL 数据的全量迁移

要将数据从 MySQL 全量迁移至 TiDB，可以采用以下三种方案中一种：

- **Mydumper + Loader**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 Loader 将数据导入至 TiDB。
- **Mydumper + TiDB Lightning**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 TiDB Lightning 将数据导入至 TiDB。
- **DM**：直接使用 DM 将数据从 MySQL 导出，然后将数据导入至 TiDB。

详细操作参见 [MySQL 数据到 TiDB 的全量迁移](/v2.1/how-to/migrate/from-mysql.md)。

### MySQL 数据的全量迁移和增量同步

- **Mydumper + Loader + Syncer**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 Loader 将数据导入至 TiDB，再使用 Syncer 将 MySQL binlog 数据增量同步至 TiDB。
- **Mydumper + TiDB Lightning + Syncer**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 TiDB Lightning 将数据导入至 TiDB，再使用 Syncer 将 MySQL binlog 数据增量同步至 TiDB。
- **DM**：先使用 DM 将数据从 MySQL 全量迁移至 TiDB，然后使用 DM 将 MySQL binlog 数据增量同步至 TiDB。

详细操作参见 [MySQL 数据到 TiDB 的增量同步](/v2.1/how-to/migrate/incrementally-from-mysql.md)。

> **注意：**
>
> 在将 MySQL binlog 数据增量同步至 TiDB 前，需要[在 MySQL 中开启 binlog 功能](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)，并且 binlog 必须[使用 `ROW` 格式](https://dev.mysql.com/doc/refman/5.7/en/binary-log-formats.html)。

### 非 MySQL 数据源的数据迁移

如果源数据库不是 MySQL，建议采用以下步骤进行数据迁移：

1. 将数据导出为 CSV 格式。
2. 使用 TiDB Lightning 将 CSV 格式的数据导入 TiDB。

详细操作参见[使用 TiDB Lightning 迁移 CSV 数据](/v2.1/reference/tools/tidb-lightning/csv.md)。
