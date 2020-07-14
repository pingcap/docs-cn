---
title: Common Misuses of TiDB Lightning
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-misuse-handling/','/docs/dev/reference/tools/error-case-handling/lightning-misuse-handling/']
---

# Common Misuses of TiDB Lightning

This document introduces common error scenarios in using [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md), and also provides their reasons and solutions.

## Error: `checksum mismatched remote vs local`

The following error is reported during data import:

```log
Error: checksum mismatched remote vs local => (checksum: 3828723015727756136 vs 7895534721177712659) (total_kvs: 1221416844 vs 1501500000) (total_bytes:237660308510 vs 292158203078)
```

### Reasons

* TiDB Lightning was used to import data previously, and the corresponding [`checkpoint`](/tidb-lightning/tidb-lightning-checkpoints.md) data was not cleaned up. To confirm this, you can check the log at the first launch of TiDB Lightning:

    * When `[checkpoint] driver = file`, if the log that marks the beginning of data import using TiDB Lightning shows `open checkpoint file failed, going to create a new one`, then the `checkpoint` is cleaned correctly. Otherwise, the remaining data might lead to imported data missing.
    * When `[checkpoint] driver = mysql`, you can run `curl http://{TiDBIP}:10080/schema/{checkpoint.schema}/{checkpoint.table}` through TiDB API to query the creation time of `checkpoint table`. Then you can confirm whether the `checkpoint` is cleaned correctly.

* There is conflicting data from the data source imported by TiDB Lightning.
    * Data in different rows have the same primary key or unique key.

### Solutions

* Delete data from tables with `checksum mismatch` error.

    ```
    tidb-lightning-ctl --config conf/tidb-lightning.toml --checkpoint-error-destroy=all
    ```

* Find a way to detect whether there is conflicting data in the data source. TiDB Lightning generally processes large amounts of data, so currently there is no effective conflict detection mechanism or solution yet.