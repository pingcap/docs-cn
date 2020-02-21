---
title: Common Misuses During Full Data Import
category: reference
---

# Common Misuses During Full Data Import

This document introduces the common error scenarios in using [Loader](/reference/tools/loader.md) or [TiDB Data Migration](/reference/tools/data-migration/overview.md) (DM) during the full data import process, and also provides their reasons and solutions.

## Error: ```Try adjusting the `max_allowed_packet` variable```

The following error is reported during full data import:

```
packet for query is too large. Try adjusting the 'max_allowed_packet' variable
```

### Reasons

* Both MySQL client and MySQL/TiDB Server have `max_allowed_packet` quotas. If any of the `max_allowed_packet` quotas is violated, the client receives a corresponding error message. Currently, the latest version of Syncer, Loader, DM, and TiDB Server all have a default `max_allowed_packet` quota of `64M`.
    * Please use the latest version, or the latest stable version of the tool. See the [download page](/reference/tools/download.md).
* The full data import processing module in Loader or DM does not support splitting `dump sqls` files.

### Solutions

* For the above reasons, it is recommended to use the `-s, --statement-size` option which Mydumper offers to control the size of `Insert Statement`: `Attempted size of INSERT statement in bytes, default 1000000`.

    According to the default configuration of `--statement-size`, the size of `Insert Statement` that Mydumper generates is as close as `1M`. This default configuration ensures that this error will not occur in most cases.

    Sometimes the following `WARN` log appears during the dump process. The `WARN` log itself does not affect the dump process but indicates that the dumped table might be a wide table.

    ```
    Row bigger than statement_size for xxx
    ```

* If a single row of a wide table exceeds 64M, you need to modify and enable the following two configurations:
    * Execute `set @@global.max_allowed_packet=134217728` (`134217728 = 128M`) in TiDB Server.
    * Add the configuration like `max-allowed-packet=128M` to the Loader configuration file or DB configuration in DM task configuration file, and then restart the progress or task.