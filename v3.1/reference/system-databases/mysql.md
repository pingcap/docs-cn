---
title: TiDB 系统表
category: reference
aliases: ['/docs-cn/sql/system-database/']
---

# TiDB 系统表

本文档主要介绍 TiDB 支持的系统表。

## 权限系统表

这些系统表里面包含了用户账户以及相应的授权信息：

* `user` 用户账户，全局权限，以及其它一些非权限的列
* `db` 数据库级别的权限
* `tables_priv` 表级的权限
* `columns_priv` 列级的权限

## 服务端帮助信息系统表

* `help_topic` 目前为空

## 统计信息相关系统表

* `stats_buckets` 统计信息的桶
* `stats_histograms` 统计信息的直方图
* `stats_meta` 表的元信息，比如总行数和修改数

## GC Worker 相关系统表

* `gc_delete_range`

## 其它系统表

* `GLOBAL_VARIABLES` 全局系统变量表
* `tidb` 用于 TiDB 在 bootstrap 的时候记录相关版本信息
