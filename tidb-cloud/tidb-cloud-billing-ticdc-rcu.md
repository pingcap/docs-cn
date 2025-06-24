---
title: 变更数据捕获计费
summary: 了解 TiDB Cloud 中变更数据捕获的计费方式。
aliases: ['/tidbcloud/tidb-cloud-billing-tcu']
---

# 变更数据捕获计费

## RCU 成本

TiDB Cloud 使用 TiCDC 复制容量单位（RCU）来衡量[变更数据捕获](/tidb-cloud/changefeed-overview.md)的容量。当你为集群[创建变更数据捕获](/tidb-cloud/changefeed-overview.md#create-a-changefeed)时，你可以选择适当的规格。RCU 越高，复制性能越好。你将为这些 TiCDC 变更数据捕获 RCU 付费。

### TiCDC RCU 数量

下表列出了变更数据捕获的规格和相应的复制性能：

| 规格 | 最大复制性能 |
|---------------|---------------------------------|
| 2 RCU        | 5,000 行/秒                    |
| 4 RCU        | 10,000 行/秒                   |
| 8 RCU        | 20,000 行/秒                   |
| 16 RCU       | 40,000 行/秒                   |
| 24 RCU       | 60,000 行/秒                   |
| 32 RCU       | 80,000 行/秒                   |
| 40 RCU       | 100,000 行/秒                  |

> **注意：**
>
> 上述性能数据仅供参考，在不同场景下可能会有所不同。强烈建议你在生产环境中使用变更数据捕获功能之前进行实际工作负载测试。如需进一步帮助，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

### 价格

要了解 TiDB Cloud 支持的区域和每个 TiCDC RCU 的价格，请参见[变更数据捕获成本](https://www.pingcap.com/tidb-cloud-pricing-details/#changefeed-cost)。

## 私有数据链路成本

如果你选择 **Private Link** 或 **Private Service Connect** 网络连接方式，将产生额外的**私有数据链路**成本。这些费用属于[数据传输成本](https://www.pingcap.com/tidb-dedicated-pricing-details/#data-transfer-cost)类别。

**私有数据链路**的价格为 **$0.01/GiB**，与 [AWS Interface Endpoint 定价](https://aws.amazon.com/privatelink/pricing/#Interface_Endpoint_pricing)的**数据处理**、[Google Cloud Private Service Connect 定价](https://cloud.google.com/vpc/pricing#psc-forwarding-rules)的**消费者数据处理**以及 [Azure Private Link 定价](https://azure.microsoft.com/en-us/pricing/details/private-link/)的**入站/出站数据处理**相同。
