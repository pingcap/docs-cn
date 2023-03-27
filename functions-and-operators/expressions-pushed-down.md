---
title: 下推到 TiKV 的表达式列表
summary: TiDB 中下推到 TiKV 的表达式列表及相关设置。
aliases: ['/docs-cn/dev/functions-and-operators/expressions-pushed-down/','/docs-cn/dev/reference/sql/functions-and-operators/expressions-pushed-down/']
---

# 下推到 TiKV 的表达式列表

当 TiDB 从 TiKV 中读取数据的时候，TiDB 会尽量下推一些表达式运算到 TiKV 中，从而减少数据传输量以及 TiDB 单一节点的计算压力。本文将介绍 TiDB 已支持下推的表达式，以及如何禁止下推特定表达式。

TiFlash 也支持[本页](/tiflash/tiflash-supported-pushdown-calculations.md)列出的函数和算子下推。

## 已支持下推的表达式列表

| 表达式分类 | 具体操作 |
| :-------------- | :------------------------------------- |
| [逻辑运算](/functions-and-operators/operators.md#逻辑操作符) | AND (&&), OR (&#124;&#124;), NOT (!), XOR |
| [位运算](/functions-and-operators/operators.md#操作符) | [<code>&</code>][operator_bitwise-and], [<code>~</code>][operator_bitwise-invert], [\|][operator_bitwise-or], [<code>^</code>][operator_bitwise-xor], [<code><<</code>][operator_left-shift], [<code>>></code>][operator_right-shift] |
| [比较运算](/functions-and-operators/operators.md#比较方法和操作符) | [<code><</code>][operator_less-than], [<code><=</code>][operator_less-than-or-equal], [<code>=</code>][operator_equal], [<code>!= (<\>)</code>][operator_not-equal], [<code>></code>][operator_greater-than], [<code>>=</code>][operator_greater-than-or-equal], [<code><=></code>][operator_equal-to], [<code>BETWEEN ... AND ...</code>][operator_between], [<code>COALESCE()</code>][function_coalesce], [<code>IN()</code>][operator_in], [<code>INTERVAL()</code>][function_interval], [<code>IS NOT NULL</code>][operator_is-not-null], [<code>IS NOT</code>][operator_is-not], [<code>IS NULL</code>][operator_is-null], [<code>IS</code>][operator_is], [<code>ISNULL()</code>][function_isnull], [<code>LIKE</code>][operator_like], [<code>NOT BETWEEN ... AND ...</code>][operator_not-between], [<code>NOT IN()</code>][operator_not-in], [<code>NOT LIKE</code>][operator_not-like], [<code>STRCMP()</code>][function_strcmp] |
| [数值运算](/functions-and-operators/numeric-functions-and-operators.md) | [<code>+</code>][operator_plus], [<code>-</code>][operator_minus], [<code>*</code>][operator_times], [<code>/</code>][operator_divide], [<code>DIV</code>][operator_div], [<code>% (MOD)</code>][operator_mod], [<code>-</code>][operator_unary-minus], [<code>ABS()</code>][function_abs], [<code>ACOS()</code>][function_acos], [<code>ASIN()</code>][function_asin], [<code>ATAN()</code>][function_atan], [<code>ATAN2(), ATAN()</code>][function_atan2], [<code>CEIL()</code>][function_ceil], [<code>CEILING()</code>][function_ceiling], [<code>CONV()</code>][function_conv], [<code>COS()</code>][function_cos], [<code>COT()</code>][function_cot], [<code>CRC32()</code>][function_crc32], [<code>DEGREES()</code>][function_degrees], [<code>EXP()</code>][function_exp], [<code>FLOOR()</code>][function_floor], [<code>LN()</code>][function_ln], [<code>LOG()</code>][function_log], [<code>LOG10()</code>][function_log10], [<code>LOG2()</code>][function_log2], [<code>MOD()</code>][function_mod], [<code>PI()</code>][function_pi], [<code>POW()</code>][function_pow], [<code>POWER()</code>][function_power], [<code>RADIANS()</code>][function_radians], [<code>RAND()</code>][function_rand], [<code>ROUND()</code>][function_round], [<code>SIGN()</code>][function_sign], [<code>SIN()</code>][function_sin], [<code>SQRT()</code>][function_sqrt] |
| [控制流运算](/functions-and-operators/control-flow-functions.md) | [<code>CASE</code>][operator_case], [<code>IF()</code>][function_if], [<code>IFNULL()</code>][function_ifnull] |
| [JSON 运算](/functions-and-operators/json-functions.md) | [JSON_ARRAY([val[, val] ...])][json_array],<br/> [JSON_CONTAINS(target, candidate[, path])][json_contains],<br/> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br/> [JSON_LENGTH(json_doc[, path])][json_length],<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br/> [JSON_OBJECT([key, val[, key, val] ...])][json_object],<br/> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove],<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br/> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br/> [JSON_TYPE(json_val)][json_type],<br/> [JSON_UNQUOTE(json_val)][json_unquote],<br/> [JSON_VALID(val)][json_valid] |
| [日期运算](/functions-and-operators/date-and-time-functions.md) | [<code>DATE()</code>][function_date], [<code>DATE_FORMAT()</code>][function_date-format], [<code>DATEDIFF()</code>][function_datediff], [<code>DAYOFMONTH()</code>][function_dayofmonth], [<code>DAYOFWEEK()</code>][function_dayofweek], [<code>DAYOFYEAR()</code>][function_dayofyear], [<code>FROM_DAYS()</code>][function_from-days], [<code>HOUR()</code>][function_hour], [<code>MAKEDATE()</code>][function_makedate], [<code>MAKETIME()</code>][function_maketime], [<code>MICROSECOND()</code>][function_microsecond], [<code>MINUTE()</code>][function_minute], [<code>MONTH()</code>][function_month], [<code>MONTHNAME()</code>][function_monthname], [<code>PERIOD_ADD()</code>][function_period-add], [<code>PERIOD_DIFF()</code>][function_period-diff], [<code>SEC_TO_TIME()</code>][function_sec-to-time], [<code>SECOND()</code>][function_second], [<code>SYSDATE()</code>][function_sysdate], [<code>TIME_TO_SEC()</code>][function_time-to-sec], [<code>TIMEDIFF()</code>][function_timediff], [<code>WEEK()</code>][function_week], [<code>WEEKOFYEAR()</code>][function_weekofyear], [<code>YEAR()</code>][function_year] |
| [字符串函数](/functions-and-operators/string-functions.md) | [<code>ASCII()</code>][function_ascii], [<code>BIT_LENGTH()</code>][function_bit-length], [<code>CHAR()</code>][function_char], [<code>CHAR_LENGTH()</code>][function_char-length], [<code>CONCAT()</code>][function_concat], [<code>CONCAT_WS()</code>][function_concat-ws], [<code>ELT()</code>][function_elt], [<code>FIELD()</code>][function_field], [<code>HEX()</code>][function_hex], [<code>LENGTH()</code>][function_length], [<code>LIKE</code>][operator_like], [<code>LTRIM()</code>][function_ltrim], [<code>MID()</code>][function_mid], [<code>NOT LIKE</code>][operator_not-like], [<code>NOT REGEXP</code>][operator_not-regexp], [<code>REGEXP</code>][operator_regexp], [<code>REPLACE()</code>][function_replace], [<code>REVERSE()</code>][function_reverse], [<code>RIGHT()</code>][function_right], [<code>RTRIM()</code>][function_rtrim], [<code>SPACE()</code>][function_space], [<code>STRCMP()</code>][function_strcmp], [<code>SUBSTR()</code>][function_substr], [<code>SUBSTRING()</code>][function_substring] |
| [聚合函数](/functions-and-operators/aggregate-group-by-functions.md#group-by-聚合函数) | [<code>COUNT()</code>][function_count], [<code>COUNT(DISTINCT)</code>][function_count-distinct], [<code>SUM()</code>][function_sum], [<code>AVG()</code>][function_avg], [<code>MAX()</code>][function_max], [<code>MIN()</code>][function_min], [<code>VARIANCE()</code>][function_variance], [<code>VAR_POP()</code>][function_var-pop], [<code>STD()</code>][function_std], [<code>STDDEV()</code>][function_stddev], [<code>STDDEV_POP</code>][function_stddev-pop], [<code>VAR_SAMP()</code>][function_var-samp], [<code>STDDEV_SAMP()</code>][function_stddev-samp], [<code>JSON_ARRAYAGG(key)</code>][json_arrayagg], [<code>JSON_OBJECTAGG(key, value)</code>][function_json-objectagg] |
| [加密和压缩函数](/functions-and-operators/encryption-and-compression-functions.md#加密和压缩函数) | [<code>MD5()</code>][function_md5], [<code>SHA1(), SHA()</code>][function_sha1], [<code>UNCOMPRESSED_LENGTH()</code>][function_uncompressed-length] |
| [Cast 函数](/functions-and-operators/cast-functions-and-operators.md#cast-函数和操作符) | [<code>CAST()</code>][function_cast], [<code>CONVERT()</code>][function_convert] |
| [其他函数](/functions-and-operators/miscellaneous-functions.md#支持的函数) | [<code>UUID()</code>][function_uuid] |

## 禁止特定表达式下推

当[已支持下推的表达式列表](#已支持下推的表达式列表)中的函数和运算符，或特定的数据类型（**仅限** [`ENUM` 类型](/data-type-string.md#enum-类型)和 [`BIT` 类型](/data-type-numeric.md#bit-类型)）的计算过程因下推而出现异常时，你可以使用黑名单功能禁止其下推，从而快速恢复 TiDB 业务。具体而言，你可以将函数名、运算符名，或数据列类型加入黑名单 `mysql.expr_pushdown_blacklist` 中，以禁止特定表达式下推。具体方法，请参阅[表达式下推黑名单](/blocklist-control-plan.md#禁止特定表达式下推)。

[function_abs]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs

[function_acos]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_acos

[function_ascii]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ascii

[function_asin]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_asin

[function_atan]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan

[function_atan2]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_atan2

[function_avg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_avg

[function_bit-length]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_bit-length

[function_cast]: https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_cast

[function_ceil]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil

[function_ceiling]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling

[function_char-length]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char-length

[function_char]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_char

[function_coalesce]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce

[function_concat-ws]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat-ws

[function_concat]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_concat

[function_conv]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_conv

[function_convert]: https://dev.mysql.com/doc/refman/5.7/en/cast-functions.html#function_convert

[function_cos]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cos

[function_cot]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_cot

[function_count-distinct]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_count-distinct

[function_count]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_count

[function_crc32]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_crc32

[function_date-format]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format

[function_date]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date

[function_datediff]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_datediff

[function_dayofmonth]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofmonth

[function_dayofweek]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofweek

[function_dayofyear]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofyear

[function_degrees]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_degrees

[function_elt]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_elt

[function_exp]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_exp

[function_field]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_field

[function_floor]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor

[function_from-days]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_from-days

[function_hex]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_hex

[function_hour]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_hour

[function_if]: https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#function_if

[function_ifnull]: https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#function_ifnull

[function_interval]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_interval

[function_isnull]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_isnull

[function_json-objectagg]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-objectagg

[function_length]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_length

[function_ln]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ln

[function_log]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log

[function_log10]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log10

[function_log2]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_log2

[function_ltrim]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_ltrim

[function_makedate]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_makedate

[function_maketime]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_maketime

[function_max]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_max

[function_md5]: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_md5

[function_microsecond]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_microsecond

[function_mid]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_mid

[function_min]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_min

[function_minute]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_minute

[function_mod]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_mod

[function_month]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_month

[function_monthname]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_monthname

[function_period-add]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_period-add

[function_period-diff]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_period-diff

[function_pi]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pi

[function_pow]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_pow

[function_power]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_power

[function_radians]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_radians

[function_rand]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_rand

[function_replace]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_replace

[function_reverse]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_reverse

[function_right]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_right

[function_round]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_round

[function_rtrim]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_rtrim

[function_sec-to-time]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sec-to-time

[function_second]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_second

[function_sha1]: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_sha1

[function_sign]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sign

[function_sin]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sin

[function_space]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_space

[function_sqrt]: https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_sqrt

[function_std]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_std

[function_stddev-pop]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_stddev-pop

[function_stddev-samp]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_stddev-samp

[function_stddev]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_stddev

[function_strcmp]: https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#function_strcmp

[function_substr]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substr

[function_substring]: https://dev.mysql.com/doc/refman/5.7/en/string-functions.html#function_substring

[function_sum]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_sum

[function_sysdate]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sysdate

[function_time-to-sec]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time-to-sec

[function_timediff]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timediff

[function_uncompressed-length]: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length

[function_uuid]: https://dev.mysql.com/doc/refman/5.7/en/miscellaneous-functions.html#function_uuid

[function_var-pop]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_var-pop

[function_var-samp]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_var-samp

[function_variance]: https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_variance

[function_week]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week

[function_weekofyear]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_weekofyear

[function_year]: https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_year

[json_array]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array

[json_arrayagg]:https://dev.mysql.com/doc/refman/5.7/en/aggregate-functions.html#function_json-arrayagg

[json_contains]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-contains

[json_extract]: https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract

[json_insert]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert

[json_length]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-length

[json_merge]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge

[json_object]: https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object

[json_remove]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove

[json_replace]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace

[json_set]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set

[json_type]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type

[json_unquote]: https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote

[json_valid]: https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-valid

[operator_between]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_between

[operator_bitwise-and]: https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-and

[operator_bitwise-invert]: https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-invert

[operator_bitwise-or]: https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-or

[operator_bitwise-xor]: https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_bitwise-xor

[operator_case]: https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#operator_case

[operator_div]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_div

[operator_divide]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_divide

[operator_equal-to]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to

[operator_equal]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal

[operator_greater-than-or-equal]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than-or-equal

[operator_greater-than]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_greater-than

[operator_in]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_in

[operator_is-not-null]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not-null

[operator_is-not]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-not

[operator_is-null]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is-null

[operator_is]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_is

[operator_left-shift]: https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_left-shift

[operator_less-than-or-equal]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than-or-equal

[operator_less-than]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_less-than

[operator_like]: https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_like

[operator_minus]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_minus

[operator_mod]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_mod

[operator_not-between]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-between

[operator_not-equal]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-equal

[operator_not-in]: https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_not-in

[operator_not-like]: https://dev.mysql.com/doc/refman/5.7/en/string-comparison-functions.html#operator_not-like

[operator_not-regexp]: https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_not-regexp

[operator_plus]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_plus

[operator_regexp]: https://dev.mysql.com/doc/refman/5.7/en/regexp.html#operator_regexp

[operator_right-shift]: https://dev.mysql.com/doc/refman/5.7/en/bit-functions.html#operator_right-shift

[operator_times]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_times

[operator_unary-minus]: https://dev.mysql.com/doc/refman/5.7/en/arithmetic-functions.html#operator_unary-minus
