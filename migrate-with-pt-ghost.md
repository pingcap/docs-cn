---
title: 上游使用 pt-osc/gh-ost 工具的持续同步场景
summary: 介绍在使用 DM 持续增量数据同步，上游使用 pt-osc/gh-ost 工具进行在线 DDL 变更时 DM 的处理方式和注意事项。
---

# 上游使用 pt-osc/gh-ost 工具的持续同步场景

在生产业务中执行 DDL 时，产生的锁表操作会一定程度阻塞数据库的读取或者写入。为了把对读写的影响降到最低，用户往往会选择 online DDL 工具执行 DDL。常见的 Online DDL 工具有 [gh-ost](https://github.com/github/gh-ost) 和 [pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)。

在使用 DM 完成 MySQL 到 TiDB 的数据迁移时，可以开启`online-ddl`配置，实现 DM 工具与 gh-ost 或 pt-osc 的协同。

具体迁移操作可参考已有数据迁移场景：

- [从小数据量 MySQL 迁移数据到 TiDB](/migrate-small-mysql-to-tidb.md)
- [从大数据量 MySQL 迁移数据到 TiDB](/migrate-large-mysql-to-tidb.md)
- [从小数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [从大数据量分库分表 MySQL 合并迁移数据到 TiDB](/migrate-large-mysql-shards-to-tidb.md)

## 开启 DM 的 online-ddl 特性

配置 DM 的任务配置文件时，将全局参数的`online-ddl`设置为 true，具体配置示例如下图：

```yaml
# ----------- 全局配置 -----------
## ********* 基本信息配置 *********
name: test                      # 任务名称，需要全局唯一
task-mode: all                  # 任务模式，可设为 "full"、"incremental"、"all"
shard-mode: "pessimistic"       # 如果为分库分表合并任务则需要配置该项。默认使用悲观协调模式 "pessimistic"，在深入了解乐观协调模式的原理和使用限制后，也可以设置为乐观协调模式 "optimistic"
meta-schema: "dm_meta"          # 下游储存 `meta` 信息的数据库
online-ddl: true                # 开启 DM 的 online DDL 支持特性。兼容上游使用 gh-ost 、pt-osc 两种工具的自动处理
```

## 开启 online-ddl 的影响

当开启`online-ddl`特性后，DM 同步 gh-ost 或 pt-osc 工具所产生的 DDL 语句将会发生一些变化：

上游 gh-ost 或 pt-osc 工具工作流如下：

- 根据 DDL 目标表 (real table) 的表结构新建一张镜像表 (ghost table)；
- 在镜像表上应用变更 DDL；
- 将 DDL 目标表的数据同步到镜像表；
- 在目标表与镜像表数据一致后，通过 RENAME 语句使镜像表替换掉目标表。

`online-ddl=true` 时 DM 的同步方式：

- 不在下游新建镜像表 (ghost table)；
- 记录变更 DDL；
- 仅从镜像表同步数据；
- 在下游执行 DDL 变更。

![dm-online-ddl](/media/dm/dm-online-ddl.png)

这些变化将带来一些好处：

- 下游 TiDB 无需创建和同步镜像表，节约相应存储空间和网络传输等开销；
- 在分库分表合并场景下，自动忽略各分表镜像表的 RENAME 操作，保证同步正确性。

如果您想深入了解其实现原理，请阅读以下两篇技术博客：

- [DM 源码阅读系列文章（八）Online Schema Change 迁移支持](https://pingcap.com/blog-cn/dm-source-code-reading-8/#dm-源码阅读系列文章八online-schema-change-迁移支持)
- [TiDB Online Schema Change 原理](https://pingcap.com/zh/blog/tidb-source-code-reading-17)

## 探索更多

- [DM 与 online DDL 工具协作细节](/dm/feature-online-ddl.md#dm-与-online-ddl-工具协作细节)
