---
title: TiFlash Data Validation
summary: Learn the data validation mechanism and tools for TiFlash.
---

# TiFlash Data validation

This document introduces the data validation mechanism and tools for TiFlash.

Data corruptions are usually caused by serious hardware failures. In such cases, even if you attempt to manually recover data, your data become less reliable.

To ensure data integrity, by default, TiFlash performs basic data validation on data files, using the `City128` algorithm. In the event of any data validation failure, TiFlash immediately reports an error and exits, avoiding secondary disasters caused by inconsistent data. At this time, you need to manually intervene and replicate the data again before you can restore the TiFlash node.

Starting from v5.4.0, TiFlash introduces more advanced data validation features. TiFlash uses the `XXH3` algorithm by default and allows you to customize the validation frame and algorithm.

## Validation mechanism

The validation mechanism builds upon the DeltaTree File (DTFile). DTFile is the storage file that persists TiFlash data. DTFile has three formats:

| Version | State | Validation mechanism | Notes |
| :-- | :-- | :-- |:-- |
| V1 | Deprecated | Hashes are embedded in data files. | |
| V2 | Default for versions < v6.0.0 | Hashes are embedded in data files. | Compared to V1, V2 adds statistics of column data. |
| V3 | Default for versions >= v6.0.0 | V3 contains metadata and token data checksum, and supports multiple hash algorithms. | New in v5.4.0. |

DTFile is stored in the `stable` folder in the data file directory. All formats currently enabled are in folder format, which means the data is stored in multiple files under a folder with a name like `dmf_<file id>`.

### Use data validation

TiFlash supports both automatic and manual data validation:

* Automatic data validation:
    * v6.0.0 and later versions use the V3 validation mechanism by default.
    * Versions earlier than v6.0.0 use the V2 validation mechanism by default.
    * To manually switch the validation mechanism, refer to [TiFlash configuration file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). However, the default configuration is verified by tests and therefore recommended.
* Manual data validation. Refer to [`DTTool inspect`](/tiflash/tiflash-command-line-flags.md#dttool-inspect).

> **Warning:**
>
> After you enable the V3 validation mechanism, the newly generated DTFile cannot be directly read by TiFlash earlier than v5.4.0. Since v5.4.0, TiFlash supports both V2 and V3 and does not actively upgrade or downgrade versions. If you need to upgrade or downgrade versions for existing files, you need to manually [switch versions](/tiflash/tiflash-command-line-flags.md#dttool-migrate).

### Validation tool

In addition to automatic data validation performed when TiFlash reads data, a tool for manually checking data integrity is introduced in v5.4.0. For details, refer to [DTTool](/tiflash/tiflash-command-line-flags.md#dttool-inspect).
