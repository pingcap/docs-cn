---
title: Enable Encryption for Disk Spill
summary: Learn how to enable encryption for disk spill in TiDB.
---

# Enable Encryption for Disk Spill

When the `oom-use-tmp-storage` configuration item is set to `true`, if the memory usage of a single SQL statement exceeds the limit of `mem-quota-query` setting, some operators can save the intermediate results during execution as a temporary file to the disk and delete the file after the query is completed.

You can enable encryption for disk spill to prevent attackers from accessing data by reading these temporary files.

## Configure

To enable encryption for the disk spill files, you can configure the item [`spilled-file-encryption-method`](/tidb-configuration-file.md#spilled-file-encryption-method) in the `[security]` section of the TiDB configuration file.

```toml
[security]
spilled-file-encryption-method = "aes128-ctr"
```

Value options for `spilled-file-encryption-method` are `aes128-ctr` and `plaintext`. The default value is `plaintext`, which means that encryption is disabled.
