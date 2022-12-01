---
title: 备份与恢复 RawKV 数据
summary: 了解如何使用 br 命令行工具备份和恢复 RawKV 数据。
---

# 备份与恢复 RawKV 数据

TiKV 可以独立于 TiDB，与 PD 构成 KV 数据库，此时的产品形态为 RawKV。

TiKV-BR 工具支持对使用 RawKV 的产品进行备份和恢复，也支持将 TiKV 集群中的数据从 `API V1` 备份为 `API V2` 格式， 以实现 TiKV 集群 [`api-version`](https://docs.pingcap.com/zh/tidb/v6.4/tikv-configuration-file#api-version-%E4%BB%8E-v610-%E7%89%88%E6%9C%AC%E5%BC%80%E5%A7%8B%E5%BC%95%E5%85%A5) 的升级。

更多信息，请参考[TiKV-BR 用户文档]( https://tikv.org/docs/dev/concepts/explore-tikv-features/backup-restore/ )。
