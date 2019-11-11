---
title: 日期和时间函数
category: reference
---

# 日期和时间函数

TiDB 支持使用 MySQL 5.7 中提供的所有[日期和时间函数](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html)。

## 日期时间函数表

| 函数名 | 功能描述 |
| ------ | ---------------------------------------- |
| [`ADDDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_adddate) | 将时间间隔添加到日期上 |
| [`ADDTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_addtime) | 时间数值相加 |
| [`CONVERT_TZ()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_convert-tz) | 转换时区 |
| [`CURDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_curdate) | 返回当前日期 |
| [`CURRENT_DATE()`, `CURRENT_DATE`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_current-date) | 与 CURDATE() 同义 |
| [`CURRENT_TIME()`, `CURRENT_TIME`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_current-time) | 与 CURTIME() 同义 |
| [`CURRENT_TIMESTAMP()`, `CURRENT_TIMESTAMP`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_current-timestamp) | 与 NOW() 同义 |
| [`CURTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_curtime) | 返回当前时间 |
| [`DATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date) | 从日期或日期/时间表达式中提取日期部分|
| [`DATE_ADD()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-add) | 将时间间隔添加到日期上|
| [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format) | 返回满足指定格式的日期/时间 |
| [`DATE_SUB()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-sub) | 从日期减去指定的时间间隔 |
| [`DATEDIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_datediff) | 返回两个日期间隔的天数|
| [`DAY()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_day) | 与 DAYOFMONTH() 同义|
| [`DAYNAME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayname) | 返回星期名称 |
| [`DAYOFMONTH()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofmonth) | 返回参数对应的天数部分(1-31)|
| [`DAYOFWEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofweek) | 返回参数对应的星期下标|
| [`DAYOFYEAR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofyear) | 返回参数代表一年的哪一天 (1-366) |
| [`EXTRACT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_extract) | 提取日期/时间中的单独部分|
| [`FROM_DAYS()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_from-days) | 将天数转化为日期 |
| [`FROM_UNIXTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_from-unixtime) | 将 Unix 时间戳格式化为日期 |
| [`GET_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_get-format) | 返回满足日期格式的字符串 |
| [`HOUR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_hour) | 提取日期/时间表达式中的小时部分 |
| [`LAST_DAY`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_last-day) | 返回参数中月份的最后一天 |
| [`LOCALTIME()`, `LOCALTIME`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_localtime) | 与 NOW() 同义 |
| [`LOCALTIMESTAMP`, `LOCALTIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_localtimestamp) | 与 NOW() 同义 |
| [`MAKEDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_makedate) | 根据给定的年份和一年中的天数生成一个日期 |
| [`MAKETIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_maketime) | 根据给定的时、分、秒生成一个时间 |
| [`MICROSECOND()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_microsecond) | 返回参数的微秒部分|
| [`MINUTE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_minute) | 返回参数的分钟部分|
| [`MONTH()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_month) | 返回参数的月份部分|
| [`MONTHNAME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_monthname) | 返回参数的月份名称|
| [`NOW()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_now) | 返回当前日期和时间|
| [`PERIOD_ADD()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_period-add) | 在年-月表达式上添加一段时间(数个月)|
| [`PERIOD_DIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_period-diff) | 返回间隔的月数|
| [`QUARTER()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_quarter) | 返回参数对应的季度(1-4) |
| [`SEC_TO_TIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sec-to-time) | 将秒数转化为 'HH:MM:SS' 的格式|
| [`SECOND()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_second) | 返回秒数(0-59) |
| [`STR_TO_DATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_str-to-date) | 将字符串转化为日期|
| [`SUBDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_subdate) | 当传入三个参数时作为 DATE_SUB() 的同义|
| [`SUBTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_subtime) | 从一个时间中减去一段时间 |
| [`SYSDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sysdate) | 返回该方法执行时的时间|
| [`TIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time) | 返回参数的时间表达式部分 |
| [`TIME_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time-format) | 格式化时间|
| [`TIME_TO_SEC()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time-to-sec) | 返回参数对应的秒数|
| [`TIMEDIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timediff) | 返回时间间隔 |
| [`TIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timestamp) | 传入一个参数时候,该方法返回日期或日期/时间表达式, 传入两个参数时候, 返回参数的和 |
| [`TIMESTAMPADD()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timestampadd) | 在日期/时间表达式上增加一段时间间隔 |
| [`TIMESTAMPDIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timestampdiff) | 从日期/时间表达式中减去一段时间间隔 |
| [`TO_DAYS()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_to-days) | 将参数转化对应的天数(从第 0 年开始) |
| [`TO_SECONDS()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_to-seconds) | 将日期或日期/时间参数转化为秒数(从第 0 年开始) |
| [`UNIX_TIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_unix-timestamp) | 返回一个 Unix 时间戳|
| [`UTC_DATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-date) | 返回当前的 UTC 日期 |
| [`UTC_TIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-time) | 返回当前的 UTC 时间 |
| [`UTC_TIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-timestamp) | 返回当前的 UTC 日期和时间|
| [`WEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week) | 返回参数所在的一年中的星期数 |
| [`WEEKDAY()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_weekday) | 返回星期下标 |
| [`WEEKOFYEAR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_weekofyear) | 返回参数在日历中对应的一年中的星期数 |
| [`YEAR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_year) | 返回参数对应的年数|
| [`YEARWEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_yearweek) | 返回年数和星期数 |
