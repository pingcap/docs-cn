---
title: TiDB 3.1 Beta Release Notes
aliases: ['/docs/dev/releases/release-3.1.0-beta/','/docs/dev/releases/3.1.0-beta/']
summary: TiDB 3.1 Beta was released on December 20, 2019. It includes SQL Optimizer improvements and supports the Follower Read feature. TiKV now supports distributed backup and restore, as well as the Follower Read feature. PD also supports distributed backup and restore.
---

# TiDB 3.1 Beta Release Notes

Release date: December 20, 2019

TiDB version: 3.1.0-beta

TiDB Ansible version: 3.1.0-beta

## TiDB

+ SQL Optimizer
    - Enrich SQL hints [#12192](https://github.com/pingcap/tidb/pull/12192)
+ New feature
    - Support the Follower Read feature [#12535](https://github.com/pingcap/tidb/pull/12535)

## TiKV

- Support the distributed backup and restore feature [#5532](https://github.com/tikv/tikv/pull/5532)
- Support the Follower Read feature [#5562](https://github.com/tikv/tikv/pull/5562)

## PD

- Support the distributed backup and restore feature [#1896](https://github.com/pingcap/pd/pull/1896)