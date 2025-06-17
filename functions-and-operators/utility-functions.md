---
title: Utility Functions
summary: 了解 TiDB 中的效用函数。
---

# 效用函数

本文介绍了 TiDB 支持的效用函数。

## `FORMAT_BYTES()`

`FORMAT_BYTES()` 函数用于将字节数格式化为易于阅读的形式。

```sql
SELECT FORMAT_BYTES(10*1024*1024);
```

```
+----------------------------+
| FORMAT_BYTES(10*1024*1024) |
+----------------------------+
| 10.00 MiB                  |
+----------------------------+
1 row in set (0.001 sec)
```

## `FORMAT_NANO_TIME()`

`FORMAT_NANO_TIME()` 函数用于将纳秒数格式化为易于阅读的形式。

```sql
SELECT FORMAT_NANO_TIME(1000000);
```

```
+---------------------------+
| FORMAT_NANO_TIME(1000000) |
+---------------------------+
| 1.00 ms                   |
+---------------------------+
1 row in set (0.001 sec)
```
