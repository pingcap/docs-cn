---
title: TiFlash Command-line Flags
summary: Learn the command-line startup flags of TiFlash.
aliases: ['/docs/dev/tiflash/tiflash-command-line-flags/']
---

# TiFlash Command-Line Flags

This document introduces the command-line flags that you can use when you launch TiFlash.

## `server --config-file`

+ Specifies the path of the TiFlash configuration file
+ Default: ""
+ You must specify the configuration file. For detailed configuration items, refer to [TiFlash configuration parameters](/tiflash/tiflash-configuration.md).

## `dttool migrate`

- Migrates the file format of DTFile (for testing or downgrading). Data is migrated in the unit of a single DTFile. If you want to migrate the whole table, you need to locate all the paths similar to `<data dir>/t_<table id>/stable/dmf_<file id>` and migrate them one by one. You can use scripts to automate the migration.

- User scenarios:

    - If you need to downgrade TiFlash from a version >= v5.4.0 that has enabled data validation to a version < v5.4.0, you can use this tool to downgrade the data format of the DTFile.
    - If you upgrade TiFlash to a version >= v5.4.0, and if you hope to enable data validation for existing data, you can use this tool to upgrade the data format of the DTFile.
    - Test the space usage and read speed of the DTFile in different configurations.
    - If you need to downgrade TiFlash from a version >= v7.3.0 that has enabled small file merging (that is, `storage.format_version` >= 5) to a version < v7.3.0, you can use this tool to downgrade the data format of the DTFile.

- Parameters:
    - `--imitative`: When you do not use the encryption feature of the DTFile, you can use this flag to avoid using the configuration file and connecting to PD.
    - `--version`: The target version of DTFile. The value options are `1`, `2` (default), and `3`. `1` is the old version, `2` is the version corresponding to the new checksum, and `3` is the version that supports merging small files.
    - `--algorithm`: The hash algorithm used for data validation. The value options are `xxh3` (default), `city128`, `crc32`, `crc64`, and `none`. This parameter is effective only when `version` is `2`.
    - `--frame`: The size of the validation frame. The default value is `1048576`. This parameter is effective only when `version` is `2`.
    - `--compression`: The target compression algorithm. The value options are `LZ4` (default), `LZ4HC`, `zstd`, and `none`.
    - `--level`: The target compression level. If not specified, the recommended compression level is used by default according to the compression algorithm. If `compression` is set to `LZ4` or `zstd`, the default level is 1. If `compression` is set to `LZ4HC`, the default level is 9. 
    - `--config-file`: The configuration file of `dttool migrate` is the same as the [configuration file of `server`](/tiflash/tiflash-command-line-flags.md#server---config-file). For more information, see `--imitative`.
    - `--file-id`: The ID of the DTFile. For example, the ID of the DTFile `dmf_123` is `123`.
    - `--workdir`: The parent directory of `dmf_xxx`.
    - `--dry`: The dry run mode. Only the migration process is output.
    - `--nokeep`: Does not keep the original data. When this option is not enabled, `dmf_xxx.old` files are created.

> **Warning:**
>
> TiFlash can read DTFile that uses custom compression algorithms and compression levels. However, only the `lz4` algorithm with the default compression level is officially supported. Custom compression parameters have not been thoroughly tested and are only experimental.

> **Note:**
>
> For security reasons, DTTool attempts to add a lock to the working directory in the migration mode. Therefore, in the same directory, only one DTTool can perform the migration task at the same time. If you forcibly stop DTTool where the lock is not released, then when you try to rerun DTTool later, it might refuse to perform the migration task.
>
> If you encounter this situation, and if you are aware that removing the LOCK file does not cause any data corruption, you can manually delete the LOCK file in the working directory to release the lock.

## `dttool bench`

- Provides a basic I/O speed test for the DTFile.
- Parameters:

    - `--version`: The version of DTFile. See [`--version` in `dttool migrate`](#dttool-migrate).
    - `--algorithm`: The hash algorithm used for data validation. See [`--algorithm` in `dttool migrate`](#dttool-migrate).
    - `--frame`: The size of the validation frame. See [`--frame` in `dttool migrate`](#dttool-migrate).
    - `--column`: The columns of the table to be tested. The default value is `100`.
    - `--size`: The rows of the table to be tested. The default value is `1000`.
    - `--field`: The field length limit of the table to be tested. The default value is `1024`.
    - `--random`: The random seed. If you do not specify this parameter, the random seed is drawn from the system entropy pool.
    - `--encryption`: Enables the encryption feature.
    - `--repeat`: The number of times to repeat the test. The default value is `5`.
    - `--workdir`: The temporary data directory, which points to a path in the file system to be tested. The default value is `/tmp/test`.

## `dttool inspect`

- Checks the integrity of the DTFile. Data validation is performed in the unit of a single DTFile. If you want to validate the whole table, you need to locate all the paths similar to `<data dir>/t_<table id>/stable/dmf_<file id>` and validate them one by one. You can use scripts to automate the validation.

- User scenarios:

    - After you perform a format upgrade or downgrade, you can validate the data integrity of the DTFile.
    - After you migrate the DTFile to a new environment, you can validate the data integrity of the DTFile.

- Parameters:

    - `--config-file`: The configuration file of `dttool bench`. See [`--config-file` in `dttool migrate`](#dttool-migrate).
    - `--check`: Performs hash validation.
    - `--file-id`: The ID of the DTFile. See [`--file-id` in `dttool migrate`](#dttool-migrate).
    - `--imitative`: Imitates the database context. See [`--imitative` in `dttool migrate`](#dttool-migrate).
    - `--workdir`: The data directory. See [`--workdir` in `dttool migrate`](#dttool-migrate).
