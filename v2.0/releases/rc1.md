---
title: TiDB RC1 Release Notes
category: Releases
---

# TiDB RC1 Release Notes

2016 年 12 月 23 日，分布式关系型数据库 TiDB 正式发布 RC1。

## TiKV

    + 提升写入速度
    + 降低磁盘空间占用
    + 支持百 TB 级别数据
    + 提升稳定性，集群规模支持 200 个节点
    + 提供 Raw KV API，以及 Golang client

## PD

    + PD 调度策略框架优化，策略更加灵活合理
    + 添加 label 支持，支持跨 DC 调度
    + 提供 PD Controler，方便操作 PD 集群

## TiDB

    + SQL 查询优化器
        - 支持 eager aggregate
        - 更详细的 explain 信息
        - union 算子并行化
        - 子查询性能优化
        - 条件下推优化
        - 优化 CBO 框架
    + 重构 time 相关类型的实现，提升和 MySQL 的兼容性
    + 支持更多的 MySQL 内建函数
    + Add Index 语句提速
    + 支持用 change column 语句修改列名；支持使用 Alter table 的 modify column 和 change column 完成部分列类型转换

## 工具

    + Loader：兼容 Percona 的 mydumper 数据格式，提供多线程导入、出错重试、断点续传等功能，并且针对 TiDB 有优化
    + 开发完成一键部署工具
