---
title: The TiDB Server
summary: Learn about the basic management functions of the TiDB cluster.
category: user guide
---

# The TiDB Server

TiDB refers to the TiDB database management system. This document describes the basic management functions of the TiDB cluster.

## TiDB cluster startup configuration

You can set the service parameters using the command line or the configuration file, or both. The priority of the command line parameters is higher than the configuration file. If the same parameter is set in both ways, TiDB uses the value set using command line parameters. For more information, see [The TiDB Command Options](../sql/server-command-option.md).

## TiDB system variable

TiDB is compatible with MySQL system variables, and defines some unique system variables to adjust the database behavior. For more information, see [TiDB Specific System Variables](../sql/tidb-specific.md).

## TiDB system table

Similar to MySQL, TiDB also has system tables that store the information needed when TiDB runs. For more information, see [The TiDB System Database](../sql/system-database.md).

## TiDB data directory

The TiDB data is stored in the storage engine and the data directory depends on the storage engine used. For more information about how to choose the storage engine, see the [TiDB startup parameters document](../op-guide/configuration.md#store).

When you use the local storage engine, the data is stored on the local hard disk and the directory location is controlled by the [`path`](../op-guide/configuration.md#path) parameter.

When you use the TiKV storage engine, the data is stored on the TiKV node and the directory location is controlled by the [`data-dir`](../op-guide/configuration.md#data-dir-1) parameter.

## TiDB server logs

The three components of the TiDB cluster (`tidb-server`, ` tikv-server` and `pd-server`) outputs the logs to standard errors by default. In each of the three components, you can set the `--log-file` [startup parameter](../op-guide/configuration.md) (or the configuration item in the configuration file) and output the log into a file.

You can adjust the log behavior using the configuration file. For more details, see the configuration file description of each component. For example, the [`tidb-server` log configuration item](https://github.com/pingcap/tidb/blob/master/config/config.toml.example#L46).
