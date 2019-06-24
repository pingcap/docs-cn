---
title: 其他函数
category: user guide
---

# 其他函数

| 函数名 | 功能描述  |
|:------|:-----------|
| [`ANY_VALUE()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_any-value) | 在 `ONLY_FULL_GROUP_BY` 模式下，防止带有 `GROUP BY` 的语句报错  |
| [`SLEEP()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_sleep)  | 休眠指定秒数   |
| [`UUID()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid) | 返回通用唯一识别码 (UUID)   |
| [`VALUES()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_values)    | 定义 `INSERT` 过程中要用到的值  |
| [`INET_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-aton)  | 将 IP 地址转换为数值   |
| [`INET_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet-ntoa)  | 将数值转换为 IP 地址   |
| [`INET6_ATON()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-aton)  | 将 IPv6 地址转换为数值    |
| [`INET6_NTOA()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_inet6-ntoa)  | 将数值转换为 IPv6 地址  |
| [`IS_IPV4()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4)   | 判断参数是否为 IPv4 地址   |
| [`IS_IPV4_COMPAT()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-compat)    | 判断参数是否为兼容 IPv4 的地址   |
| [`IS_IPV4_MAPPED()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv4-mapped)    | 判断参数是否为 IPv4 映射的地址   |
| [`IS_IPV6()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_is-ipv6)    | 判断参数是否为 IPv6 地址    |
| [`GET_LOCK()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_get-lock)    | 获取命名锁，TiDB     出于兼容性支持这个函数，实际上不会做任何操作，这点和 MySQL 有区别 |
| [`RELEASE_LOCK()`](https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_release-lock)  | 释放命名锁     |
