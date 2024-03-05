---
title: TiDB Data Migration 命令行参数
summary: 介绍 DM 各组件的主要命令行参数。
aliases: ['/docs-cn/tidb-data-migration/dev/command-line-flags/']
---

# TiDB Data Migration 命令行参数

本文档介绍 TiDB Data Migration (DM) 中各组件的主要命令行参数。

## DM-master

### `--advertise-addr`

- DM-master 用于接收客户端请求的外部地址
- 默认值为 `"{master-addr}"`
- 可选参数，可以为 `"域名:port"` 的形式

### `--advertise-peer-urls`

- DM-master 节点间通信的外部连接地址
- 默认值为 `"{peer-urls}"`
- 可选参数，可以为 `"http(s)://域名:port"` 的形式

### `--config`

- DM-master 配置文件路径
- 默认值为 `""`
- 可选参数

### `--data-dir`

- DM-master 用于存储自身数据的目录
- 默认值为 `"default.{name}"`
- 可选参数

### `--initial-cluster`

- 用于 bootstrap DM-master 集群的 `"{节点名}={外部地址}"` 列表
- 默认值为 `"{name}={advertise-peer-urls}"`
- 在未指定 `join` 参数时需要指定该参数。一个 3 节点集群的配置示例为 `"dm-master-1=http://172.16.15.11:8291,dm-master-2=http://172.16.15.12:8291,dm-master-3=http://172.16.15.13:8291"`

### `--join`

- DM-master 节点加入到已有集群时，已有集群的 `advertise-addr` 地址列表
- 默认值为 `""`
- 未指定 `initial-cluster` 参数时需要指定该参数。一个新节点加入到一个已有 2 个节点的集群的示例为 `"172.16.15.11:8261,172.16.15.12:8261"`

### `--log-file`

- log 输出文件名
- 默认值为 `""`
- 可选参数

### `-L`

- log 级别
- 默认值为 `"info"`
- 可选参数

### `--master-addr`

- DM-master 监听客户端请求的地址
- 默认值为 `""`
- 必选参数

### `--name`

- DM-master 节点名称
- 默认值为 `"dm-master-{hostname}"`
- 必选参数

### `--peer-urls`

- DM-master 节点间通信的监听地址
- 默认值为 `"http://127.0.0.1:8291"`
- 必选参数

### `--secret-key-path`

- 自定义加解密密钥路径
- 默认值为 `""`
- 可选参数

## DM-worker

### `--advertise-addr`

- DM-worker 用于接受客户端请求的外部地址
- 默认值为 `"{worker-addr}"`
- 可选参数，可以为 `"域名:port"` 的形式

### `--config`

- DM-worker 配置文件路径
- 默认值为 `""`
- 可选参数

### `--join`

- DM-worker 注册到集群时，相应集群的 DM-master 节点的 `{advertise-addr}` 列表
- 默认值为 `""`
- 必选参数，一个 3 DM-master 节点的集群配置示例为 `"172.16.15.11:8261,172.16.15.12:8261,172.16.15.13:8261"`

### `--log-file`

- log 输出文件名
- 默认值为 `""`
- 可选参数

### `-L`

- log 级别
- 默认值为 `"info"`
- 可选参数

### `--name`

- DM-worker 节点名称
- 默认值为 `"{advertise-addr}"`
- 必选参数

### `--worker-addr`

- DM-worker 监听客户端请求的地址
- 默认值为 `""`
- 必选参数

## dmctl

### `--config`

- dmctl 配置文件路径
- 默认值为 `""`
- 可选参数

### `--master-addr`

- dmctl 要连接的集群的任意 DM-master 节点的 `{advertise-addr}`
- 默认值为 `""`
- 需要与 DM-master 交互时为必选参数
