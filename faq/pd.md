---
title: PD
category: faq-product
---

# PD

## 访问 PD 报错：TiKV cluster is not bootstrapped

PD 的大部分 API 需要在初始化 TiKV 集群以后才能使用，如果在部署新集群的时候只启动了 PD，还没有启动 TiKV，这时候访问 PD 就会报这个错误。遇到这个错误应该先把要部署的 TiKV 启动起来，TiKV 会自动完成初始化工作，然后就可以正常访问 PD 。

## PD 启动报错：etcd cluster ID mismatch

PD 启动参数中的 `--initial-cluster` 包含了某个不属于该集群的成员。遇到这个错误时请检查各个成员的所属集群，剔除错误的成员后即可正常启动。

## 更改 PD 的启动参数

当想更改 PD 的 `--client-url`，`--advertise-client-url` 或 `--name` 时，只要用更新后的参数重新启动该 PD 就可以了。当更改的参数是 `--peer-url` 或 `--advertise-peer-url` 时，有以下几种情况需要区别处理：

 - 之前的启动参数中有 `--advertise-peer-url`，但只想更新 `--peer-url`：用更新后的参数重启即可。
 - 之前的启动参数中没有 `--advertise-peer-url`：先[用 etcdctl 更新该 PD 的信息](https://coreos.com/etcd/docs/latest/op-guide/runtime-configuration.html#update-a-member)，之后再用更新后的参数重启即可。

## PD 能容忍的时间同步误差是多少？

理论上误差越小越好，切换 leader 的时候如果时钟回退就会卡住直到追上之前的 leader 。这个容忍是业务上的 ，PD 多长的误差都能容忍。 但是误差越大，主从切换的时候 ，停止服务的时间越长。