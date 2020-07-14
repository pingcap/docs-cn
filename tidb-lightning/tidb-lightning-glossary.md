---
title: TiDB Lightning Glossary
summary: List of special terms used in TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-glossary/','/docs/dev/reference/tools/tidb-lightning/glossary/']
---

# TiDB Lightning Glossary

This page explains the special terms used in TiDB Lightning's logs, monitoring, configurations, and documentation.

<!-- A -->

## A

### Analyze

An operation to rebuild the [statistics](/statistics.md) information of a TiDB table, i.e. running the [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) statement.

Because TiDB Lightning imports data without going through TiDB, the statistics information is not automatically updated. Therefore, TiDB Lightning explicitly analyzes every table after importing. This step can be omitted by setting the `post-restore.analyze` configuration to `false`.

### `AUTO_INCREMENT_ID`

Every table has an associated `AUTO_INCREMENT_ID` counter to provide the default value of an auto-incrementing column. In TiDB, this counter is additionally used to assign row IDs.

Because TiDB Lightning imports data without going through TiDB, the `AUTO_INCREMENT_ID` counter is not automatically updated. Therefore, TiDB Lightning explicitly alters `AUTO_INCREMENT_ID` to a valid value. This step is always performed, even if the table has no `AUTO_INCREMENT` columns.

<!-- B -->

## B

### Back end

Back end is the destination where TiDB Lightning sends the parsed result. Also spelled as "backend".

See [TiDB Lightning TiDB-backend](/tidb-lightning/tidb-lightning-tidb-backend.md) for details.

<!-- C -->

## C

### Checkpoint

TiDB Lightning continuously saves its progress into a local file or a remote database while importing. This allows it to resume from an intermediate state should it crashes in the process. See the [Checkpoints](/tidb-lightning/tidb-lightning-checkpoints.md) section for details.

### Checksum

In TiDB Lightning, the checksum of a table is a set of 3 numbers calculated from the content of each KV pair in that table. These numbers are respectively:

* the number of KV pairs,
* total length of all KV pairs, and
* the bitwise-XOR of [CRC-64-ECMA](https://en.wikipedia.org/wiki/Cyclic_redundancy_check) value each pair.

TiDB Lightning [validates the imported data](/tidb-lightning/tidb-lightning-faq.md#how-to-ensure-the-integrity-of-the-imported-data) by comparing the [local](/tidb-lightning/tidb-lightning-glossary.md#local-checksum) and [remote checksums](/tidb-lightning/tidb-lightning-glossary.md#remote-checksum) of every table. The program would stop if any pair does not match. You can skip this check by setting the `post-restore.checksum` configuration to `false`.

See also the [Troubleshooting guide](/troubleshoot-tidb-lightning.md#checksum-failed-checksum-mismatched-remote-vs-local) for how to properly handle checksum mismatch.

### Chunk

A continuous range of source data, normally equivalent to a single file in the data source.

When a file is too large, Lightning may split a file into multiple chunks.

### Compaction

An operation that merges multiple small SST files into one large SST file, and cleans up the deleted entries. TiKV automatically compacts data in background while TiDB Lightning is importing.

> **Note:**
>
> For legacy reasons, you can still configure TiDB Lightning to explicitly trigger a compaction every time a table is imported. However, this is not recommended and the corresponding settings are disabled by default.

See [RocksDB's wiki page on Compaction](https://github.com/facebook/rocksdb/wiki/Compaction) for its technical details.

<!-- D -->

## D

### Data engine

An [engine](/tidb-lightning/tidb-lightning-glossary.md#engine) for sorting actual row data.

When a table is very large, its data is placed into multiple data engines to improve task pipelining and save space of TiKV Importer. By default, a new data engine is opened for every 100 GB of SQL data, which can be configured through the `mydumper.batch-size` setting.

TiDB Lightning processes multiple data engines concurrently. This is controlled by the `lightning.table-concurrency` setting.

<!-- E -->

## E

### Engine

In TiKV Importer, an engine is a RocksDB instance for sorting KV pairs.

TiDB Lightning transfers data to TiKV Importer through engines. It first opens an engine, sends KV pairs to it (with no particular order), and finally closes the engine. The engine sorts the received KV pairs after it is closed. These closed engines can then be further uploaded to the TiKV stores for ingestion.

Engines use TiKV Importer's `import-dir` as temporary storage, which are sometimes referred to as "engine files".

See also [data engine](/tidb-lightning/tidb-lightning-glossary.md#data-engine) and [index engine](/tidb-lightning/tidb-lightning-glossary.md#index-engine).

<!-- F -->

## F

### Filter

A configuration list that specifies which tables to be imported or excluded.

See [Table Filter](/table-filter.md) for details.

<!-- I -->

## I

### Import mode

A configuration that optimizes TiKV for writing at the cost of degraded read speed and space usage.

TiDB Lightning automatically switches to and off the import mode while running. However, if TiKV gets stuck in import mode, you can use `tidb-lightning-ctl` to [force revert](/tidb-lightning/tidb-lightning-faq.md#why-my-tidb-cluster-is-using-lots-of-cpu-resources-and-running-very-slowly-after-using-tidb-lightning) to [normal mode](/tidb-lightning/tidb-lightning-glossary.md#normal-mode).

### Index engine

An [engine](/tidb-lightning/tidb-lightning-glossary.md#engine) for sorting indices.

Regardless of number of indices, every table is associated with exactly one index engine.

TiDB Lightning processes multiple index engines concurrently. This is controlled by the `lightning.index-concurrency` setting. Since every table has exactly one index engine, this also configures the maximum number of tables to process at the same time.

### Ingest

An operation which inserts the entire content of an [SST file](/tidb-lightning/tidb-lightning-glossary.md#sst-file) into the RocksDB (TiKV) store.

Ingestion is a very fast operation compared with inserting KV pairs one by one. This operation is the determinant factor for the performance of TiDB Lightning.

See [RocksDB's wiki page on Creating and Ingesting SST files](https://github.com/facebook/rocksdb/wiki/Creating-and-Ingesting-SST-files) for its technical details.

<!-- K -->

## K

### KV pair

Abbreviation of "key-value pair".

### KV encoder

A routine which parses SQL or CSV rows to KV pairs. Multiple KV encoders run in parallel to speed up processing.

<!-- L -->

## L

### Local checksum

The [checksum](/tidb-lightning/tidb-lightning-glossary.md#checksum) of a table calculated by TiDB Lightning itself before sending the KV pairs to TiKV Importer.

<!-- N -->

## N

### Normal mode

The mode where [import mode](/tidb-lightning/tidb-lightning-glossary.md#import-mode) is disabled.

<!-- P -->

## P

### Post-processing

The period of time after the entire data source is parsed and sent to TiKV Importer. TiDB Lightning is waiting for TiKV Importer to upload and [ingest](/tidb-lightning/tidb-lightning-glossary.md#ingest) the [SST files](/tidb-lightning/tidb-lightning-glossary.md#sst-file).

<!-- R -->

## R

### Remote checksum

The [checksum](/tidb-lightning/tidb-lightning-glossary.md#checksum) of a table calculated by TiDB after it has been imported.

<!-- S -->

## S

### Scattering

An operation that randomly reassigns the leader and the peers of a [Region](/glossary.md#regionpeerraft-group). Scattering ensures that the imported data are distributed evenly among TiKV stores. This reduces stress on PD.

### Splitting

An engine is typically very large (around 100 GB), which is not friendly to TiKV if treated as a single [region](/glossary.md#regionpeerraft-group). TiKV Importer splits an engine into multiple small [SST files](/tidb-lightning/tidb-lightning-glossary.md#sst-file) (configurable by TiKV Importer's `import.region-split-size` setting) before uploading.

### SST file

SST is the abbreviation of "sorted string table". An SST file is RocksDB's (and thus TiKV's) native storage format of a collection of KV pairs.

TiKV Importer produces SST files from a closed [engine](/tidb-lightning/tidb-lightning-glossary.md#engine). These SST files are uploaded and then [ingested](/tidb-lightning/tidb-lightning-glossary.md#ingest) into TiKV stores.
