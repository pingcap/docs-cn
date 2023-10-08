---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
aliases: ['/docs/dev/functions-and-operators/miscellaneous-functions/','/docs/dev/reference/sql/functions-and-operators/miscellaneous-functions/']
---

# Miscellaneous Functions

TiDB supports most of the [miscellaneous functions](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html) available in MySQL 5.7.

## Supported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_any-value)              | Suppress `ONLY_FULL_GROUP_BY` value rejection     |
| [`BIN_TO_UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_bin-to-uuid)          | Convert UUID from binary format to text format    |
| [`DEFAULT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_default)                  | Returns the default value for a table column      |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet-aton)              | Return the numeric value of an IP address         |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet-ntoa)              | Return the IP address from a numeric value        |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet6-aton)            | Return the numeric value of an IPv6 address       |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_inet6-ntoa)            | Return the IPv6 address from a numeric value      |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv4)                  | Whether argument is an IPv4 address               |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv4-compat)    | Whether argument is an IPv4-compatible address    |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv4-mapped)    | Whether argument is an IPv4-mapped address        |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_is-ipv6)                  | Whether argument is an IPv6 address               |
| [`NAME_CONST()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_name-const)            | Can be used to rename a column name               |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_sleep)                      | Sleep for a number of seconds. Note that for [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters, the `SLEEP()` function has a limitation wherein it can only support a maximum sleep time of 300 seconds.       |
| [`UUID()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid)                        | Return a Universal Unique Identifier (UUID)       |
| [`UUID_TO_BIN()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-to-bin)          | Convert UUID from text format to binary format    |
| [`VALUES()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_values)                    | Defines the values to be used during an INSERT    |

## Unsupported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_uuid-short)            | Provides a UUID that is unique given certain assumptions not present in TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |
| [`MASTER_WAIT_POS()`](https://dev.mysql.com/doc/refman/8.0/en/miscellaneous-functions.html#function_master-pos-wait)  | Relates to MySQL replication |
