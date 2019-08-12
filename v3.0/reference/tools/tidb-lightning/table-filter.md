---
title: TiDB Lightning 表库过滤
summary: 使用黑白名单把一些表剔出要导入的范围。
category: reference
aliases: ['/docs-cn/tools/lightning/filter/','/docs-cn/dev/reference/tools/tidb-lightning/filter/']
---

# TiDB Lightning 表库过滤

TiDB Lightning 支持使用黑名单和白名单来过滤掉某些数据库和表。这可以用来跳过一些用作暂存、毋须迁移的表，或用来手动切分数据源，让多机同时导入。

这些过滤规则与 MySQL 的 `replication-rules-db`/`replication-rules-table` 类似。

## 过滤数据库

```toml
[black-white-list]
do-dbs = ["pattern1", "pattern2", "pattern3"]
ignore-dbs = ["pattern4", "pattern5"]
```

* 如果 `[black-white-list]` 下的 `do-dbs` 列表不为空，
    * 如数据库名称匹配 `do-dbs` 列表中**任何**一项，则数据库会被导入。
    * 否则，数据库会被略过。
* 否则，如果数据库名称匹配 `ignore-dbs` 列表中**任何**一项，数据库会被略过。
* 如果数据库名称**同时**匹配 `do-dbs` 和 `ignore-dbs` 列表，数据库会被导入。

如果匹配项首字符为 `~`，它会被解析为 [Go 语言的正则表达式](https://golang.org/pkg/regexp/syntax/#hdr-Syntax)。否则会视为普通的字串来匹配数据库名称。

## 过滤表

```toml
[[black-white-list.do-tables]]
db-name = "db-pattern-1"
tbl-name = "table-pattern-1"

[[black-white-list.do-tables]]
db-name = "db-pattern-2"
tbl-name = "table-pattern-2"

[[black-white-list.do-tables]]
db-name = "db-pattern-3"
tbl-name = "table-pattern-3"

[[black-white-list.ignore-tables]]
db-name = "db-pattern-4"
tbl-name = "table-pattern-4"

[[black-white-list.ignore-tables]]
db-name = "db-pattern-5"
tbl-name = "table-pattern-5"
```

* 如果 `do-tables` 列表不为空，
    * 如果表的限定名称匹配 `do-tables` 列表中**任何**一对，则表会被导入。
    * 否则，表会被略过。
* 否则，如果表的限定名称匹配 `ignore-tables` 列表中**任何**一对，表会被略过。
* 如果表的限定名称**同时**匹配 `do-tables` 和 `ignore-tables` 列表，表会被导入。

> **注意：**
>
> Lightning 会先执行数据库过滤规则，之后才执行表的过滤规则。所以，如果一个数据库已被 `ignore-dbs` 略过，即使其下的表匹配 `do-tables` 也不会再被导入。

## 例子

以下例子演示过滤规则的操作原理。假设数据源包含这些表：

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
`admin`.`secrets`
```

我们使用以下设置：

```toml
[black-white-list]
do-dbs = [
    "forum_backup_2018",            # 规则 A
    "~^(logs|forum)$",              # 规则 B
]
ignore-dbs = [
    "~^forum_backup_",              # 规则 C
]

[[black-white-list.do-tables]]      # 规则 D
db-name = "logs"
tbl-name = "~_2018$"

[[black-white-list.ignore-tables]]  # 规则 E
db-name = "~.*"
tbl-name = "~^messages.*"

[[black-white-list.do-tables]]      # 规则 F
db-name = "~^forum.*"
tbl-name = "messages"
```

首先进行数据库过滤：

| 数据库                     | 结果          |
|---------------------------|--------------|
| `` `logs` ``              | 导入（规则 B） |
| `` `forum` ``             | 导入（规则 B） |
| `` `forum_backup_2016` `` | 略过（规则 C） |
| `` `forum_backup_2017` `` | 略过（规则 C） |
| `` `forum_backup_2018` `` | 导入（规则 A）（不会考虑规则 C） |
| `` `admin` ``             | 略过（`do-dbs` 不为空，且没有匹配的项目） |

然后进行表过滤：

| 表                                   | 结果          |
|--------------------------------------|--------------|
| `` `logs`.`messages_2016` ``         | 略过（规则 E） |
| `` `logs`.`messages_2017` ``         | 略过（规则 E） |
| `` `logs`.`messages_2018` ``         | 导入（规则 D）（不会考虑规则 E） |
| `` `forum`.`users` ``                | 略过（`do-tables` 不为空，且没有匹配的项目） |
| `` `forum`.`messages` ``             | 导入（规则 F）（不会考虑规则 E） |
| `` `forum_backup_2016`.`messages` `` | 略过（数据库已被剔除） |
| `` `forum_backup_2017`.`messages` `` | 略过（数据库已被剔除） |
| `` `forum_backup_2018`.`messages` `` | 导入（规则 F）（不会考虑规则 E） |
| `` `admin`.`secrets` ``              | 略过（数据库已被剔除） |
