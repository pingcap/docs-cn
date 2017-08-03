---
title: TiKV
category: faq-product
---

# TiKV

## 为什么 TiKV 数据目录不见了

TiKV 的 `--data-dir` 参数默认值为 `/tmp/tikv/store`，在某些虚拟机中，重启操作系统会删除 /tmp 目录下的数据，推荐通过 `--data-dir` 参数显式设置 TiKV 数据目录。

## TiKV 启动报错：cluster ID mismatch

TiKV 本地存储的 cluster ID 和指定的 PD 的 cluster ID 不一致。在部署新的 PD 集群的时候，PD 会随机生成一个 cluster ID，TiKV 第一次初始化的时候会从 PD 获取 cluster ID 存储在本地，下次启动的时候会检查本地的 cluster ID 与 PD 的 cluster ID 是否一致，如果不一致则会报错并退出。出现这个错误一个常见的原因是，用户原先部署了一个集群，后来把 PD 的数据删除了并且重新部署了新的 PD，但是 TiKV 还是使用旧的数据重启连到新的 PD 上，就会报这个错误。

## TiKV 启动报错：duplicated store address

启动参数中的地址已经被其他的 TiKV 注册在 PD 集群中了。造成该错误的常见情况：TiKV `--data-dir` 指定的路径下没有数据文件夹时（删除或移动后没有更新 `--data-dir`），用之前参数重新启动该 TiKV。请尝试用 pdctl 的 [store 删除](https://github.com/pingcap/pd/tree/master/pdctl#store-delete-store_id)功能，删除之前的 store, 然后重新启动 TiKV 即可。


## 按照 TIDB 的 key 设定，会不会很长？
rocksdb 对于 key 有压缩。

