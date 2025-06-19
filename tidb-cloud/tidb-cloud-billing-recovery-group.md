---
title: 恢复组计费
summary: 了解 TiDB Cloud 中恢复组的计费方式。
---

# 恢复组计费

TiDB Cloud 根据恢复组主集群中 TiKV 节点的部署大小对恢复组进行计费。当你为集群[创建恢复组](/tidb-cloud/recovery-group-get-started.md)时，你可以选择恢复组的主集群。TiKV 配置越大，恢复组保护的成本就越高。

TiDB Cloud 还按每 GiB 的数据处理量收费。数据处理价格因数据是复制到另一个区域的次要集群还是同一区域内的次要集群而异。

## 定价

要了解 TiDB Cloud 恢复组支持的区域和定价，请参阅[恢复组成本](https://www.pingcap.com/tidb-cloud-pricing-details/#recovery-group-cost)。
