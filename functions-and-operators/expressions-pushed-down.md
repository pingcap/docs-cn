---
title: List of Expressions for Pushdown
summary: Learn a list of expressions that can be pushed down to TiKV and the related operations.
aliases: ['/docs/dev/functions-and-operators/expressions-pushed-down/','/docs/dev/reference/sql/functions-and-operators/expressions-pushed-down/']
---

# List of Expressions for Pushdown

When TiDB reads data from TiKV, TiDB tries to push down some expressions (including calculations of functions or operators) to be processed to TiKV. This reduces the amount of transferred data and offloads processing from a single TiDB node. This document introduces the expressions that TiDB already supports pushing down and how to prohibit specific expressions from being pushed down using blocklist.

Tiflash also supports pushdown for the functions and operators [listed on this page](/tiflash/tiflash-supported-pushdown-calculations.md).

## Supported expressions for pushdown to TiKV

| Expression Type | Operations |
| :-------------- | :------------------------------------- |
| [Logical operators](/functions-and-operators/operators.md#logical-operators) | AND (&&), OR (&#124;&#124;), NOT (!), XOR |
| [Bit operators](/functions-and-operators/operators.md#operators) | [`&`][operator_bitwise-and], [`~`][operator_bitwise-invert], [\|][operator_bitwise-or], [`^`][operator_bitwise-xor], [`<<`][operator_left-shift], [`>>`][operator_right-shift] |
| [Comparison functions and operators](/functions-and-operators/operators.md#comparison-functions-and-operators) | [`<`][operator_less-than], [`<=`][operator_less-than-or-equal], [`=`][operator_equal], [`!= (<>)`][operator_not-equal], [`>`][operator_greater-than], [`>=`][operator_greater-than-or-equal], [`<=>`][operator_equal-to], [`BETWEEN ... AND ...`][operator_between], [`COALESCE()`][function_coalesce], [`IN()`][operator_in], [`INTERVAL()`][function_interval], [`IS NOT NULL`][operator_is-not-null], [`IS NOT`][operator_is-not], [`IS NULL`][operator_is-null], [`IS`][operator_is], [`ISNULL()`][function_isnull], [`LIKE`][operator_like], [`NOT BETWEEN ... AND ...`][operator_not-between], [`NOT IN()`][operator_not-in], [`NOT LIKE`][operator_not-like], [`STRCMP()`][function_strcmp] |
| [Numeric functions and operators](/functions-and-operators/numeric-functions-and-operators.md) | [`+`][operator_plus], [`-`][operator_minus], [`*`][operator_times], [`/`][operator_divide], [`DIV`][operator_div], [`% (MOD)`][operator_mod], [`-`][operator_unary-minus], [`ABS()`][function_abs], [`ACOS()`][function_acos], [`ASIN()`][function_asin], [`ATAN()`][function_atan], [`ATAN2(), ATAN()`][function_atan2], [`CEIL()`][function_ceil], [`CEILING()`][function_ceiling], [`CONV()`][function_conv], [`COS()`][function_cos], [`COT()`][function_cot], [`CRC32()`][function_crc32], [`DEGREES()`][function_degrees], [`EXP()`][function_exp], [`FLOOR()`][function_floor], [`LN()`][function_ln], [`LOG()`][function_log], [`LOG10()`][function_log10], [`LOG2()`][function_log2], [`MOD()`][function_mod], [`PI()`][function_pi], [`POW()`][function_pow], [`POWER()`][function_power], [`RADIANS()`][function_radians], [`RAND()`][function_rand], [`ROUND()`][function_round], [`SIGN()`][function_sign], [`SIN()`][function_sin], [`SQRT()`][function_sqrt] |
| [Control flow functions](/functions-and-operators/control-flow-functions.md) | [`CASE`][operator_case], [`IF()`][function_if], [`IFNULL()`][function_ifnull] |
| [JSON functions](/functions-and-operators/json-functions.md) | [JSON_ARRAY([val[, val] ...])][json_array],<br/> [JSON_CONTAINS(target, candidate[, path])][json_contains],<br/> [JSON_EXTRACT(json_doc, path[, path] ...)][json_extract],<br/> [JSON_INSERT(json_doc, path, val[, path, val] ...)][json_insert],<br/> [JSON_LENGTH(json_doc[, path])][json_length],<br/> [JSON_MERGE(json_doc, json_doc[, json_doc] ...)][json_merge],<br/> [JSON_OBJECT([key, val[, key, val] ...])][json_object],<br/> [JSON_REMOVE(json_doc, path[, path] ...)][json_remove],<br/> [JSON_REPLACE(json_doc, path, val[, path, val] ...)][json_replace],<br/> [JSON_SET(json_doc, path, val[, path, val] ...)][json_set],<br/> [JSON_TYPE(json_val)][json_type],<br/> [JSON_UNQUOTE(json_val)][json_unquote],<br/> [JSON_VALID(val)][json_valid] |
| [Date and time functions](/functions-and-operators/date-and-time-functions.md) | [`DATE()`][function_date], [`DATE_FORMAT()`][function_date-format], [`DATEDIFF()`][function_datediff], [`DAYOFMONTH()`][function_dayofmonth], [`DAYOFWEEK()`][function_dayofweek], [`DAYOFYEAR()`][function_dayofyear], [`FROM_DAYS()`][function_from-days], [`HOUR()`][function_hour], [`MAKEDATE()`][function_makedate], [`MAKETIME()`][function_maketime], [`MICROSECOND()`][function_microsecond], [`MINUTE()`][function_minute], [`MONTH()`][function_month], [`MONTHNAME()`][function_monthname], [`PERIOD_ADD()`][function_period-add], [`PERIOD_DIFF()`][function_period-diff], [`SEC_TO_TIME()`][function_sec-to-time], [`SECOND()`][function_second], [`SYSDATE()`][function_sysdate], [`TIME_TO_SEC()`][function_time-to-sec], [`TIMEDIFF()`][function_timediff], [`WEEK()`][function_week], [`WEEKOFYEAR()`][function_weekofyear], [`YEAR()`][function_year] |
| [String functions](/functions-and-operators/string-functions.md) | [`ASCII()`][function_ascii], [`BIT_LENGTH()`][function_bit-length], [`CHAR()`][function_char], [`CHAR_LENGTH()`][function_char-length], [`CONCAT()`][function_concat], [`CONCAT_WS()`][function_concat-ws], [`ELT()`][function_elt], [`FIELD()`][function_field], [`HEX()`][function_hex], [`LENGTH()`][function_length], [`LIKE`][operator_like], [`LTRIM()`][function_ltrim], [`MID()`][function_mid], [`NOT LIKE`][operator_not-like], [`NOT REGEXP`][operator_not-regexp], [`REGEXP`][operator_regexp], [`REPLACE()`][function_replace], [`REVERSE()`][function_reverse], [`RIGHT()`][function_right], [`RTRIM()`][function_rtrim], [`SPACE()`][function_space], [`STRCMP()`][function_strcmp], [`SUBSTR()`][function_substr], [`SUBSTRING()`][function_substring] |
| [Aggregation functions](/functions-and-operators/aggregate-group-by-functions.md#aggregate-group-by-functions) | [`COUNT()`][function_count], [`COUNT(DISTINCT)`][function_count-distinct], [`SUM()`][function_sum], [`AVG()`][function_avg], [`MAX()`][function_max], [`MIN()`][function_min], [`VARIANCE()`][function_variance], [`VAR_POP()`][function_var-pop], [`STD()`][function_std], [`STDDEV()`][function_stddev], [`STDDEV_POP`][function_stddev-pop], [`VAR_SAMP()`][function_var-samp], [`STDDEV_SAMP()`][function_stddev-samp], [`JSON_ARRAYAGG(key)`][json_arrayagg], [`JSON_OBJECTAGG(key, value)`][function_json-objectagg] |
| [Encryption and compression functions](/functions-and-operators/encryption-and-compression-functions.md#encryption-and-compression-functions) | [`MD5()`][function_md5], [`SHA1(), SHA()`][function_sha1], [`UNCOMPRESSED_LENGTH()`][function_uncompressed-length] |
| [Cast functions and operators](/functions-and-operators/cast-functions-and-operators.md#cast-functions-and-operators) | [`CAST()`][function_cast], [`CONVERT()`][function_convert] |
| [Miscellaneous functions](/functions-and-operators/miscellaneous-functions.md#supported-functions) | [`UUID()`][function_uuid] |

## Blocklist specific expressions

If unexpected behavior occurs in the calculation process when pushing down the [supported expressions](#supported-expressions-for-pushdown-to-tikv) or specific data types (**only** the [`ENUM` type](/data-type-string.md#enum-type) and the [`BIT` type](/data-type-numeric.md#bit-type)), you can restore the application quickly by prohibiting the pushdown of the corresponding functions, operators, or data types. Specifically, you can prohibit the functions, operators, or data types from being pushed down by adding them to the blocklist `mysql.expr_pushdown_blacklist`. For details, refer to [Add to the blocklist](/blocklist-control-plan.md#disable-the-pushdown-of-specific-expressions).

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
