---
title: Boolean Literals
category: user guide
---

# Boolean Literals

常量 `TRUE` 和 `FALSE` 等于 1 和 0，它是大小写不敏感的。

```sql
mysql> SELECT TRUE, true, tRuE, FALSE, FaLsE, false;
+------+------+------+-------+-------+-------+
| TRUE | true | tRuE | FALSE | FaLsE | false |
+------+------+------+-------+-------+-------+
|    1 |    1 |    1 |     0 |     0 |     0 |
+------+------+------+-------+-------+-------+
1 row in set (0.00 sec)
```
