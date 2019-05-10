---
title: TiDB-Lightning Overview
summary: Learn about Lightning and the whole architecture.
category: tools
---

# TiDB-Lightning Overview

TiDB-Lightning is a tool used for fast full import of large amounts of data into a TiDB cluster. Currently, TiDB-Lightning supports reading SQL dump exported via mydumper. You can use it in the following two scenarios:

- Importing **large amounts** of **new** data **quickly**
- Back up and restore all the data

## TiDB-Lightning architecture

The TiDB-Lightning tool set consists of two components:

- **`tidb-lightning`** (the "front end") reads the SQL dump and imports the database structure into the TiDB cluster, and also transforms the data into Key-Value (KV) pairs and sends them to `tikv-importer`.

- **`tikv-importer`** (the "back end") combines and sorts the KV pairs and then imports these sorted pairs as a whole into the TiKV cluster.

![Architecture of TiDB-Lightning tool set](/media/tidb-lightning-architecture.png)

The complete import process is as follows:

1. Before importing, `tidb-lightning` switches the TiKV cluster to "import mode", which optimizes the cluster for writing and disables automatic compaction.

2. `tidb-lightning` creates the skeleton of all tables from the data source.

3. For each table, `tidb-lightning` informs `tikv-importer` via gRPC to create an *engine file* to store KV pairs. `tidb-lightning` then reads the SQL dump in parallel, transforms the data into KV pairs according to the TiDB rules, and sends them to `tikv-importer`'s engine files.

4. Once a full table of KV pairs are received, `tikv-importer` divides and schedules these data and imports them into the target TiKV cluster.

5. `tidb-lightning` then performs a checksum comparison between the local data source and those calculated from the cluster, to ensure there is no data corruption in the process, and tells TiDB to `ANALYZE` all imported tables, to prepare for optimal query planning.

6. After all tables are imported, `tidb-lightning` performs a global compaction on the TiKV cluster.

7. Finally, `tidb-lightning` switches the TiKV cluster back to "normal mode", so the cluster resumes normal services.