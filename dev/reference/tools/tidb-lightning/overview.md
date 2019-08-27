---
title: TiDB Lightning Overview
summary: Learn about Lightning and the whole architecture.
category: reference
---

# TiDB Lightning Overview

[TiDB Lightning](https://github.com/pingcap/tidb-lightning) is a tool used for fast full import of large amounts of data into a TiDB cluster. Currently, TiDB Lightning supports reading SQL dump exported via Mydumper or CSV data source. You can use it in the following two scenarios:

- Importing **large amounts** of **new** data **quickly**
- Back up and restore all the data

## TiDB Lightning architecture

The TiDB Lightning tool set consists of two components:

- **`tidb-lightning`** (the "front end") reads the data source and imports the database structure into the TiDB cluster, and also transforms the data into Key-Value (KV) pairs and sends them to `tikv-importer`.

- **`tikv-importer`** (the "back end") combines and sorts the KV pairs and then imports these sorted pairs as a whole into the TiKV cluster.

![Architecture of TiDB Lightning tool set](/media/tidb-lightning-architecture.png)

The complete import process is as follows:

1. Before importing, `tidb-lightning` switches the TiKV cluster to "import mode", which optimizes the cluster for writing and disables automatic compaction.

2. `tidb-lightning` creates the skeleton of all tables from the data source.

3. Each table is split into multiple continuous *batches*, so that data from a huge table (200 GB+) can be delivered incrementally.

4. For each batch, `tidb-lightning` informs `tikv-importer` via gRPC to create *engine files* to store KV pairs. `tidb-lightning` then reads the data source in parallel, transforms each row into KV pairs according to the TiDB rules, and sends them to `tikv-importer`'s engine files.

5. Once a complete engine file is written, `tikv-importer` divides and schedules these data and imports them into the target TiKV cluster.

    There are two kinds of engine files: *data engines* and *index engines*, each corresponding to two kinds of KV pairs: the row data and secondary indices. Normally, the row data are entirely sorted in the data source, while the secondary indices are out of order. Because of this, the data engines are uploaded as soon as a batch is completed, while the index engines are imported only after all batches of the entire table are encoded.

6. After all engines associated to a table are imported, `tidb-lightning` performs a checksum comparison between the local data source and those calculated from the cluster, to ensure there is no data corruption in the process, and tells TiDB to `ANALYZE` all imported tables, to prepare for optimal query planning.

7. Finally, `tidb-lightning` switches the TiKV cluster back to "normal mode", so the cluster resumes normal services.
