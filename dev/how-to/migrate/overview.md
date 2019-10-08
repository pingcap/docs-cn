---
title: 数据迁移概述
category: how-to
---

# 数据迁移概述

本文档介绍了 TiDB 提供的数据迁移工具，以及不同迁移场景下如何选择迁移工具，从而将数据从 MySQL 或 CSV 数据源迁移到 TiDB。

## 迁移工具

在上述数据迁移过程中会用到如下工具：

- [DM (Data Migration)](/dev/reference/tools/data-migration/overview.md)：集成了 Mydumper、Loader、Syncer 的功能，支持 MySQL 数据的全量导出和到 TiDB 的全量导入，还支持 MySQL binlog 数据到 TiDB 的增量同步。
- [TiDB Lightning](/dev/reference/tools/tidb-lightning/overview.md)：用于将全量数据高速导入到 TiDB 集群。例如，如果要导入超过 1TiB 的数据，使用 Loader 往往需花费几十个小时，而使用 TiDB-Lightning 的导入速度至少是 Loader 的三倍。
- [Mydumper](/dev/reference/tools/mydumper.md)：用于从 MySQL 导出数据。建议使用 Mydumper，而非 mysqldump。
- [Loader](/dev/reference/tools/loader.md)：用于将 Mydumper 导出格式的数据导入到 TiDB。
- [Syncer](/dev/reference/tools/syncer.md)：用于将数据从 MySQL 增量同步到 TiDB。

## 迁移场景

本小节将通过几个示例场景来说明如何选择和使用 TiDB 的迁移工具。

### MySQL 数据源的数据迁移

DM 集成了全量备份、全量恢复、增量备份以及增量同步功能，且对 MySQL 分库分表场景有很好的支持，因此一般情况下推荐使用 DM 迁移 MySQL 的数据，只有在一些特殊场景下推荐使用其他工具，例如：

- 全量数据在 T 级别以上且对全量数据的导入速度有较高要求的场景下，可以使用 Mydumper + TiDB Lightning 做全量数据导入，再使用 DM 创建增量模式的任务同步增量数据。
- 测试环境且数据量较少，可以使用 Mydumper、Loader、Syncer 做数据的迁移。

具体的迁移方案参见 [从 MySQL 迁移数据](/dev/how-to/migrate/from-mysql.md)

### 非 MySQL 数据源的数据迁移

如果源数据库不是 MySQL，建议采用以下步骤进行数据迁移：

1. 将数据导出为 CSV 格式。
2. 使用 TiDB Lightning 将 CSV 格式的数据导入 TiDB。

详细操作参见[使用 TiDB Lightning 迁移 CSV 数据](/dev/reference/tools/tidb-lightning/csv.md)。
