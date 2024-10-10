---
title: QUERY WATCH
summary: TiDB 数据库中 QUERY WATCH 的使用概况。
---

# QUERY WATCH

`QUERY WATCH` 语句用于在资源组中手动管理 Runaway Queries 监控列表。

## 语法图

```ebnf+diagram
AddQueryWatchStmt ::=
    "QUERY" "WATCH" "ADD" QueryWatchOptionList

QueryWatchOptionList ::=
    QueryWatchOption
|   QueryWatchOptionList QueryWatchOption
|   QueryWatchOptionList ',' QueryWatchOption

QueryWatchOption ::=
    "RESOURCE" "GROUP" ResourceGroupName
|   "RESOURCE" "GROUP" UserVariable
|   "ACTION" EqOpt ResourceGroupRunawayActionOption
|   QueryWatchTextOption

ResourceGroupName ::=
    Identifier
|   "DEFAULT"

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL
|   "SWITCH_GROUP" '(' ResourceGroupName ')'

QueryWatchTextOption ::=
    "SQL" "DIGEST" SimpleExpr
|   "PLAN" "DIGEST" SimpleExpr
|   "SQL" "TEXT" ResourceGroupRunawayWatchOption "TO" SimpleExpr

ResourceGroupRunawayWatchOption ::=
    "EXACT"
|   "SIMILAR"
|   "PLAN"

DropQueryWatchStmt ::=
    "QUERY" "WATCH" "REMOVE" NUM
```

## 参数说明

详见 [`QUERY WATCH` 语句说明](/tidb-resource-control.md#query-watch-语句说明)。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [Runaway Queries](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)
