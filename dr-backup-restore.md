---
title: DR Solution Based on BR
summary: Learn how to implement disaster recovery based on TiDB's backup and restore feature.
---

# DR Solution Based on BR

A TiDB cluster has multiple replicas, which allows it to tolerate the failure of a single data center or region and continue to provide services. In the case of a natural disaster, software vulnerability, hardware failure, virus attack, or misoperations, which impacts an area larger than a single data center or region, TiDB's Backup & Restore (BR) feature can back up data to an independent disaster recovery (DR) storage device to protect user data from damage. Compared with other DR solutions, the BR feature is more flexible, reliable, recoverable, and cost-effective:

- Flexibility: You can back up data any time with any frequency. This makes backup and restore flexible and better adapts to different business scenarios.
- Reliability: Backup data is usually stored on an independent storage device and this means enhanced data security.
- Recoverability: Any loss or damage to the original data caused by any unexpected situation can be recovered by restoring the backup data. This makes the BR feature highly recoverable and ensures the normal use of your database.
- Cost effectiveness: You can get your database protected using BR without spending too much.

Generally speaking, BR is the last resort for data safety. It improves the safety and reliability of the databases without requiring too much cost. BR protects data in various unexpected situations so that you can use the database safely without worrying about the risk of data loss or damage.

## Perform backup and restore

![BR log backup and PITR architecture](/media/dr/dr-backup-and-restore.png)

As shown in the preceding architecture, you can back up data to a DR storage device located in other regions, and recover data from the backup data as needed. This means that the cluster can tolerate the failure of a single region with a Recovery Point Objective (RPO) of up to 5 minutes and a Recovery Time Objective (RTO) between tens of minutes and a few hours. However, if the database size is large, the RTO might be longer.

> **Note:**
>
> The term "region" in this document means a physical location.

Meanwhile, TiDB provides backup and restore based on block storage snapshots. This feature reduces the recovery time to hours or even less than one hour. TiDB is continuously improving and optimizing the backup and restore capabilities so as to provide you better services.

TiDB also provides detailed documentation to help you understand how to use the backup and restore feature in DR scenarios. Among them,

- [Usage Overview of TiDB Backup and Restore](/br/br-use-overview.md) is an overview of the BR feature, including the backup strategy and the organization of backup data.
- [Backup & Restore FAQs](/faq/backup-and-restore-faq.md) lists the frequently asked questions (FAQs) and the solutions of TiDB Backup & Restore (BR).
- [Overview of TiDB Backup & Restore Architecture](/br/backup-and-restore-design.md) describes the design architecture of the BR feature, including the backup and restore processes and the design of backup files.
