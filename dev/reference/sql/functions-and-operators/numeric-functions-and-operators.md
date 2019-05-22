---
title: 数值函数与操作符
category: reference
aliases: ['/docs-cn/sql/numeric-functions-and-operators/']
---

# 数值函数与操作符

## 算术操作符

| 操作符名     | 功能描述                       |
|:-------------|:--------------------------------|
| [`+`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus)        | 加号                 |
| [`-`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus)       | 减号                    |
| [`*`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times)       | 乘号           |
| [`/`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide)      | 除号                 |
| [`DIV`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div)       | 整数除法                  |
| [`%`, `MOD`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod)  | 模运算，取余                   |
| [`-`](https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus) | 更改参数符号   |

## 数学函数

| 函数名                                                                                                      | 功能描述                                                       |
|:----------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------|
| [`POW()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pow)               | 返回参数的指定乘方的结果值                 |
| [`POWER()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_power)           | 返回参数的指定乘方的结果值                 |
| [`EXP()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_exp)               | 返回 e（自然对数的底）的指定乘方后的值                                         |
| [`SQRT()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sqrt)             | 返回非负数的二次方根                          |
| [`LN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ln)                 | 返回参数的自然对数                   |
| [`LOG()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log)               | 返回第一个参数的自然对数                |
| [`LOG2()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log2)             | 返回参数以 2 为底的对数                       |
| [`LOG10()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log10)           | 返回参数以 10 为底的对数                    |
| [`PI()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pi)                 | 返回 pi 的值                                           |
| [`TAN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_tan)               | 返回参数的正切值   |
| [`COT()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cot)               | 返回参数的余切值                                              |
| [`SIN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sin)               | 返回参数的正弦值                       |
| [`COS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cos)               | 返回参数的余弦值                                                 |
| [`ATAN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan)             | 返回参数的反正切值                                            |
| [`ATAN2(), ATAN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan2)   | 返回两个参数的反正切值                  |
| [`ASIN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_asin)             | 返回参数的反正弦值                                               |
| [`ACOS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_acos)             | 返回参数的反余弦值                                             |
| [`RADIANS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_radians)       | 返回由度转化为弧度的参数                  |
| [`DEGREES()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_degrees)       | 返回由弧度转化为度的参数              |
| [`MOD()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_mod)               | 返回余数                                              |
| [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs)               | 返回参数的绝对值                                         |
| [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil)             | 返回不小于参数的最小整数值   |
| [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling)       | 返回不小于参数的最小整数值  |
| [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor)           | 返回不大于参数的最大整数值    |
| [`ROUND()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_round)           | 返回参数最近似的整数或指定小数位数的数值                                                |
| [`RAND()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_rand)             | 返回一个随机浮点值    |
| [`SIGN()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sign)             | 返回参数的符号      |
| [`CONV()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_conv)             | 不同数基间转换数字，返回数字的字符串表示   |
| [`TRUNCATE()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_truncate)     | 返回被舍位至指定小数位数的数字     |
| [`CRC32()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_crc32)           | 计算循环冗余码校验值并返回一个 32 位无符号值                     |
