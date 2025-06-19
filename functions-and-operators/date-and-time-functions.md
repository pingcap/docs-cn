---
title: 日期和时间函数
summary: 了解如何使用日期和时间函数。
---

# 日期和时间函数

TiDB 支持 MySQL 8.0 中提供的所有[日期和时间函数](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)。

> **注意：**
>
> - MySQL 通常会接受格式不正确的日期和时间值。例如，`'2020-01-01\n\t01:01:01'` 和 `'2020-01_01\n\t01:01'` 会被视为有效的日期和时间值。
> - TiDB 尽最大努力匹配 MySQL 的行为，但可能并非在所有情况下都能完全匹配。建议正确格式化日期，因为对于格式不正确的值的预期行为没有文档说明，而且通常是不一致的。

**日期/时间函数：**

| 名称 | 描述 |
| ---------------------------------------- | ---------------------------------------- |
| [`ADDDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_adddate) | 将时间值（间隔）添加到日期值 |
| [`ADDTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_addtime) | 添加时间 |
| [`CONVERT_TZ()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_convert-tz) | 从一个时区转换到另一个时区 |
| [`CURDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_curdate) | 返回当前日期 |
| [`CURRENT_DATE()`, `CURRENT_DATE`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-date) | CURDATE() 的同义词 |
| [`CURRENT_TIME()`, `CURRENT_TIME`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-time) | CURTIME() 的同义词 |
| [`CURRENT_TIMESTAMP()`, `CURRENT_TIMESTAMP`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_current-timestamp) | NOW() 的同义词 |
| [`CURTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_curtime) | 返回当前时间 |
| [`DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date) | 从日期或日期时间表达式中提取日期部分 |
| [`DATE_ADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-add) | 将时间值（间隔）添加到日期值 |
| [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-format) | 按指定格式格式化日期 |
| [`DATE_SUB()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_date-sub) | 从日期中减去时间值（间隔） |
| [`DATEDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_datediff) | 计算两个日期之差 |
| [`DAY()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_day) | DAYOFMONTH() 的同义词 |
| [`DAYNAME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayname) | 返回星期几的名称 |
| [`DAYOFMONTH()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofmonth) | 返回月份中的日期（0-31） |
| [`DAYOFWEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofweek) | 返回参数的星期索引 |
| [`DAYOFYEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_dayofyear) | 返回一年中的第几天（1-366） |
| [`EXTRACT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_extract) | 提取日期的部分内容 |
| [`FROM_DAYS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_from-days) | 将天数转换为日期 |
| [`FROM_UNIXTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_from-unixtime) | 将 Unix 时间戳格式化为日期 |
| [`GET_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_get-format) | 返回日期格式字符串 |
| [`HOUR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_hour) | 提取小时 |
| [`LAST_DAY`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_last-day) | 返回参数的月份最后一天 |
| [`LOCALTIME()`, `LOCALTIME`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_localtime) | NOW() 的同义词 |
| [`LOCALTIMESTAMP`, `LOCALTIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_localtimestamp) | NOW() 的同义词 |
| [`MAKEDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_makedate) | 从年份和一年中的天数创建日期 |
| [`MAKETIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_maketime) | 从小时、分钟、秒创建时间 |
| [`MICROSECOND()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_microsecond) | 返回参数中的微秒 |
| [`MINUTE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_minute) | 返回参数中的分钟 |
| [`MONTH()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_month) | 返回传入日期的月份 |
| [`MONTHNAME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_monthname) | 返回月份名称 |
| [`NOW()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_now) | 返回当前日期和时间 |
| [`PERIOD_ADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_period-add) | 将周期添加到年月 |
| [`PERIOD_DIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_period-diff) | 返回两个周期之间的月数 |
| [`QUARTER()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_quarter) | 返回日期参数的季度 |
| [`SEC_TO_TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_sec-to-time) | 将秒转换为 'HH:MM:SS' 格式 |
| [`SECOND()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_second) | 返回秒数（0-59） |
| [`STR_TO_DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_str-to-date) | 将字符串转换为日期 |
| [`SUBDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_subdate) | 当使用三个参数调用时，是 DATE_SUB() 的同义词 |
| [`SUBTIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_subtime) | 减去时间 |
| [`SYSDATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_sysdate) | 返回函数执行时的时间 |
| [`TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time) | 提取传入表达式的时间部分 |
| [`TIME_FORMAT()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time-format) | 格式化为时间 |
| [`TIME_TO_SEC()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_time-to-sec) | 返回转换为秒的参数 |
| [`TIMEDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timediff) | 计算时间差 |
| [`TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestamp) | 使用单个参数时，此函数返回日期或日期时间表达式；使用两个参数时，返回参数之和 |
| [`TIMESTAMPADD()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampadd) | 向日期时间表达式添加间隔 |
| [`TIMESTAMPDIFF()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_timestampdiff) | 从日期时间表达式中减去间隔 |
| [`TO_DAYS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_to-days) | 返回转换为天数的日期参数 |
| [`TO_SECONDS()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_to-seconds) | 返回转换为从公元 0 年开始的秒数的日期或日期时间参数 |
| [`UNIX_TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_unix-timestamp) | 返回 Unix 时间戳 |
| [`UTC_DATE()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-date) | 返回当前 UTC 日期 |
| [`UTC_TIME()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-time) | 返回当前 UTC 时间 |
| [`UTC_TIMESTAMP()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_utc-timestamp) | 返回当前 UTC 日期和时间 |
| [`WEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_week) | 返回周数 |
| [`WEEKDAY()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_weekday) | 返回星期索引 |
| [`WEEKOFYEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_weekofyear) | 返回日期的日历周（1-53） |
| [`YEAR()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_year) | 返回年份 |
| [`YEARWEEK()`](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html#function_yearweek) | 返回年份和周 |

详情请参见[日期和时间函数](https://dev.mysql.com/doc/refman/8.0/en/date-and-time-functions.html)。

## MySQL 兼容性

TiDB 支持 `STR_TO_DATE()` 函数，但无法解析所有日期和时间值。此外，以下日期和时间格式选项**尚未实现**：

| 格式 | 描述 |
|--------|---------------------------------------------------------------------------------------|
| "%a"   | 缩写的星期名称（Sun..Sat） |
| "%D"   | 带有英文后缀的月份中的日期（0th, 1st, 2nd, 3rd） |
| "%U"   | 周（00..53），其中星期日是一周的第一天；WEEK() 模式 0 |
| "%u"   | 周（00..53），其中星期一是一周的第一天；WEEK() 模式 1 |
| "%V"   | 周（01..53），其中星期日是一周的第一天；WEEK() 模式 2；与 %X 一起使用 |
| "%v"   | 周（01..53），其中星期一是一周的第一天；WEEK() 模式 3；与 %x 一起使用 |
| "%W"   | 星期名称（Sunday..Saturday） |
| "%w"   | 一周中的第几天（0=Sunday..6=Saturday） |
| "%X"   | 星期日作为一周第一天的周所在的年份，数字，四位。 |
| "%x"   | 星期一作为一周第一天的周所在的年份，数字，四位。 |

更多详情请参见 [issue #30082](https://github.com/pingcap/tidb/issues/30082)。

## 相关系统变量

[`default_week_format`](/system-variables.md#default_week_format) 变量影响 `WEEK()` 函数。
