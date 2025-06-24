---
title: 数值函数和运算符
summary: 了解数值函数和运算符。
---

# 数值函数和运算符

TiDB 支持 MySQL 8.0 中提供的所有[数值函数和运算符](https://dev.mysql.com/doc/refman/8.0/en/numeric-functions.html)。

## 算术运算符

| 名称                                                                                          | 描述                       |
|:----------------------------------------------------------------------------------------------|:----------------------------------|
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)        | 加法运算符                 |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus)       | 减法运算符                    |
| [`*`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_times)       | 乘法运算符           |
| [`/`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_divide)      | 除法运算符                 |
| [`DIV`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_div)       | 整数除法                  |
| [`%`, `MOD`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_mod)  | 取模运算符                   |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_unary-minus) | 改变参数的符号   |

## 数学函数

| 名称                                                                                                      | 描述                                                       |
|:----------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------|
| [`ABS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_abs)               | 返回绝对值                                         |
| [`ACOS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_acos)             | 返回反余弦值                                             |
| [`ASIN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_asin)             | 返回反正弦值                                               |
| [`ATAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_atan)             | 返回反正切值                                            |
| [`ATAN2(), ATAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_atan2)   | 返回两个参数的反正切值                       |
| [`CEIL()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ceil)             | 返回不小于参数的最小整数值      |
| [`CEILING()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ceiling)       | 返回不小于参数的最小整数值      |
| [`CONV()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_conv)             | 在不同进制之间转换数字                    |
| [`COS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_cos)               | 返回余弦值                                                 |
| [`COT()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_cot)               | 返回余切值                                              |
| [`CRC32()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_crc32)           | 计算循环冗余校验值                           |
| [`DEGREES()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_degrees)       | 将弧度转换为角度                                        |
| [`EXP()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_exp)               | 返回 e 的幂                                             |
| [`FLOOR()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_floor)           | 返回不大于参数的最大整数值    |
| [`LN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_ln)                 | 返回参数的自然对数                      |
| [`LOG()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log)               | 返回第一个参数的自然对数                |
| [`LOG10()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log10)           | 返回参数的以 10 为底的对数                      |
| [`LOG2()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_log2)             | 返回参数的以 2 为底的对数                       |
| [`MOD()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_mod)               | 返回余数                                              |
| [`PI()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_pi)                 | 返回圆周率值                                            |
| [`POW()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_pow)               | 返回参数的指定次幂                 |
| [`POWER()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_power)           | 返回参数的指定次幂                 |
| [`RADIANS()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_radians)       | 将参数转换为弧度                              |
| [`RAND()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_rand)             | 返回随机浮点值                              |
| [`ROUND()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_round)           | 对参数进行四舍五入                                                |
| [`SIGN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sign)             | 返回参数的符号                                   |
| [`SIN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sin)               | 返回参数的正弦值                                   |
| [`SQRT()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_sqrt)             | 返回参数的平方根                            |
| [`TAN()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_tan)               | 返回参数的正切值                                |
| [`TRUNCATE()`](https://dev.mysql.com/doc/refman/8.0/en/mathematical-functions.html#function_truncate)     | 截断到指定的小数位数                    |

## 相关系统变量

[`div_precision_increment`](/system-variables.md#div_precision_increment-new-in-v800) 用于设置 `/` 运算符的精度。
