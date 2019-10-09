---
title: 从 MySQL 迁移数据
category: how-to
---

# 从 MySQL 迁移数据

## MySQL 数据的全量迁移

要将数据从 MySQL 全量迁移至 TiDB，可以采用以下三种方案中一种：

- **DM**：直接使用 DM 将数据从 MySQL 导出，然后将数据导入至 TiDB。一般场景推荐使用 DM。
- **Mydumper + TiDB Lightning**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 TiDB Lightning 将数据导入至 TiDB。仅在全量数据在 T 级别以上以及对全量数据的导入速度有较高要求的场景下推荐使用该方案。
- **Mydumper + Loader**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 Loader 将数据导入至 TiDB。适合在数据量较少的场景及测试环境中使用该方案，详细操作参见 [MySQL 数据到 TiDB 的全量迁移](/dev/how-to/migrate/full-from-mysql.md)。

## MySQL 数据的全量迁移和增量同步

- **DM**：先使用 DM 将数据从 MySQL 全量迁移至 TiDB，然后使用 DM 将 MySQL binlog 数据增量同步至 TiDB。一般场景推荐使用 DM。
- **Mydumper + TiDB Lightning + DM**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 TiDB Lightning 将数据导入至 TiDB，再使用 DM 创建增量同步任务将 MySQL binlog 数据同步至 TiDB。仅在全量数据在 T 级别以上以及对全量数据的导入速度有较高要求的场景下推荐使用该方案。
- **Mydumper + Loader + Syncer**：先使用 Mydumper 将数据从 MySQL 导出，然后使用 Loader 将数据导入至 TiDB，再使用 Syncer 将 MySQL binlog 数据增量同步至 TiDB。适合在数据量较少的场景及测试环境中使用该方案，详细操作参见 [MySQL 数据到 TiDB 的增量同步](/dev/how-to/migrate/incrementally-from-mysql.md)。

> **注意：**
>
> 在将 MySQL binlog 数据增量同步至 TiDB 前，需要[在 MySQL 中开启 binlog 功能](http://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html)，并且 binlog 必须[使用 `ROW` 格式](https://dev.mysql.com/doc/refman/5.7/en/binary-log-formats.html)。
