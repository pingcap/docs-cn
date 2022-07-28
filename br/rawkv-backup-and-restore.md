---
title: Back Up and Restore RawKV
summary: Learn how to back up and restore RawKV using BR.
---

# Back Up and Restore RawKV

> **Warning:**
>
> This feature is deprecated since TiDB v6.2.0.

TiKV and PD can constitute a KV database when used without TiDB, which is called RawKV. Backup & Restore (BR) supports data backup and restore for products that use RawKV. This document describes how to back up and restore RawKV.

## Back up RawKV

In some scenarios, TiKV might run independently of TiDB. Given that, BR supports bypassing the TiDB layer and backing up data in TiKV.

{{< copyable "shell-regular" >}}

```shell
br backup raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --ratelimit 128 \
    --end 3130303030303030 \
    --format hex \
    --cf default
```

The preceding command backs up all keys between `[0x31, 0x3130303030303030)` in the default CF to `$BACKUP_DIR`.

In this command, the values of `--start` and `--end` are decoded using the format specified by `--format` before being sent to TiKV. Currently, the following formats are available:

- "raw": The input string is directly encoded as a key in binary format.
- "hex": The default encoding format. The input string is treated as a hexadecimal number.
- "escaped": First escape (backslash) the input string, and then encode it into binary format, for example, `abc\xFF\x00\r\n`.

> **Note:**
>
> - If you use the local storage, you **should** copy all back up SST files to every TiKV node in the path specified by `--storage`. Even if each TiKV node eventually only needs to read a part of the SST files, they all need full access to the complete archive because:
>
>     - Data is replicated into multiple peers. When ingesting SSTs, these files have to be present on all peers. This is unlike backup where reading from a single node is enough.
>     - Where each peer is scattered to during restoration is random. You have no idea in advance which node will read which file.
>
> - These can be avoided using shared storage, for example, mounting an NFS on the local path, or using S3. With network storage, every node can automatically read every SST file. In this case, the preceding caveats no longer apply.
> - Also, note that you can only run one restoration operation for a single cluster at the same time. Otherwise, unexpected behaviors might occur. For details, see [FAQs](/br/backup-and-restore-faq.md#can-i-use-multiple-br-processes-at-the-same-time-to-restore-the-data-of-a-single-cluster).

## Restore RawKV

Similar to [backing up RawKV](#back-up-rawkv), you can run the following command to restore RawKV:

{{< copyable "shell-regular" >}}

```shell
br restore raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --end 3130303030303030 \
    --ratelimit 128 \
    --format hex \
    --cf default
```

In this example, all the backed up keys in the range `[0x31, 0x3130303030303030)` are restored to the TiKV cluster. The coding formats of these keys are identical to that of keys during the backup process.
