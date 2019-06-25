---
title: Miscellaneous Functions
summary: Learn about miscellaneous functions in TiDB.
category: reference
---

# Miscellaneous Functions

TiDB supports most of the [miscellaneous functions](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html) available in MySQL 5.7.

## Supported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value)              | Suppress `ONLY_FULL_GROUP_BY` value rejection       |
| [`DEFAULT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_default)                  | Returns the default value for a table column      |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton)              | Return the numeric value of an IP address         |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa)              | Return the IP address from a numeric value        |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton)            | Return the numeric value of an IPv6 address       |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa)            | Return the IPv6 address from a numeric value      |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4)                  | Whether argument is an IPv4 address               |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat)    | Whether argument is an IPv4-compatible address    |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped)    | Whether argument is an IPv4-mapped address        |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6)                  | Whether argument is an IPv6 address               |
| [`NAME_CONST()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_name-const)            | Can be used to rename a column name               |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep)                      | Sleep for a number of seconds                     |
| [`UUID()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid)                        | Return a Universal Unique Identifier (UUID)       |
| [`VALUES()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values)                    | Defines the values to be used during an INSERT    |

## Unsupported functions

| Name | Description  |
|:------------|:-----------------------------------------------------------------------------------------------|
| [`GET_LOCK()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_get-lock)                | Get a named lock [TiDB #10929](https://github.com/pingcap/tidb/issues/10929) |
| [`RELEASE_LOCK()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_release-lock)        | Releases the named lock [TiDB #10929](https://github.com/pingcap/tidb/issues/10929) |
| [`UUID_SHORT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid-short)            | Provides a UUID that is unique given certain assumptions not present in TiDB [TiDB #4620](https://github.com/pingcap/tidb/issues/4620) |
| [`MASTER_WAIT_POS()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_master-pos-wait)  | Relates to MySQL replication |

