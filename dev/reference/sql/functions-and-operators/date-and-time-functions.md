---
title: Date and Time Functions
summary: Learn how to use the data and time functions.
category: reference
aliases: ['/docs/sql/date-and-time-functions/']
---

# Date and Time Functions

The usage of date and time functions is similar to MySQL. For more information, see [here](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-types.html).

**Date/Time functions**

| Name                                     | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| [`ADDDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_adddate) | Add time values (intervals) to a date value |
| [`ADDTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_addtime) | Add time                                 |
| [`CONVERT_TZ()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_convert-tz) | Convert from one time zone to another    |
| [`CURDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_curdate) | Return the current date                  |
| [`CURRENT_DATE()`, `CURRENT_DATE`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_current-date) | Synonyms for CURDATE()                   |
| [`CURRENT_TIME()`, `CURRENT_TIME`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_current-time) | Synonyms for CURTIME()                   |
| [`CURRENT_TIMESTAMP()`, `CURRENT_TIMESTAMP`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_current-timestamp) | Synonyms for NOW()                       |
| [`CURTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_curtime) | Return the current time                  |
| [`DATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date) | Extract the date part of a date or datetime expression |
| [`DATE_ADD()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-add) | Add time values (intervals) to a date value |
| [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format) | Format date as specified                 |
| [`DATE_SUB()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-sub) | Subtract a time value (interval) from a date |
| [`DATEDIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_datediff) | Subtract two dates                       |
| [`DAY()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_day) | Synonym for DAYOFMONTH()                 |
| [`DAYNAME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayname) | Return the name of the weekday           |
| [`DAYOFMONTH()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofmonth) | Return the day of the month (0-31)       |
| [`DAYOFWEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofweek) | Return the weekday index of the argument |
| [`DAYOFYEAR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_dayofyear) | Return the day of the year (1-366)       |
| [`EXTRACT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_extract) | Extract part of a date                   |
| [`FROM_DAYS()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_from-days) | Convert a day number to a date           |
| [`FROM_UNIXTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_from-unixtime) | Format Unix timestamp as a date          |
| [`GET_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_get-format) | Return a date format string              |
| [`HOUR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_hour) | Extract the hour                         |
| [`LAST_DAY`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_last-day) | Return the last day of the month for the argument |
| [`LOCALTIME()`, `LOCALTIME`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_localtime) | Synonym for NOW()                        |
| [`LOCALTIMESTAMP`, `LOCALTIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_localtimestamp) | Synonym for NOW()                        |
| [`MAKEDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_makedate) | Create a date from the year and day of year |
| [`MAKETIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_maketime) | Create time from hour, minute, second    |
| [`MICROSECOND()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_microsecond) | Return the microseconds from argument    |
| [`MINUTE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_minute) | Return the minute from the argument      |
| [`MONTH()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_month) | Return the month from the date passed    |
| [`MONTHNAME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_monthname) | Return the name of the month             |
| [`NOW()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_now) | Return the current date and time         |
| [`PERIOD_ADD()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_period-add) | Add a period to a year-month             |
| [`PERIOD_DIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_period-diff) | Return the number of months between periods |
| [`QUARTER()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_quarter) | Return the quarter from a date argument  |
| [`SEC_TO_TIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sec-to-time) | Converts seconds to 'HH:MM:SS' format    |
| [`SECOND()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_second) | Return the second (0-59)                 |
| [`STR_TO_DATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_str-to-date) | Convert a string to a date               |
| [`SUBDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_subdate) | Synonym for DATE_SUB() when invoked with three arguments |
| [`SUBTIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_subtime) | Subtract times                           |
| [`SYSDATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_sysdate) | Return the time at which the function executes |
| [`TIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time) | Extract the time portion of the expression passed |
| [`TIME_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time-format) | Format as time                           |
| [`TIME_TO_SEC()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_time-to-sec) | Return the argument converted to seconds |
| [`TIMEDIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timediff) | Subtract time                            |
| [`TIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timestamp) | With a single argument, this function returns the date or datetime expression; with two arguments, the sum of the arguments |
| [`TIMESTAMPADD()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timestampadd) | Add an interval to a datetime expression |
| [`TIMESTAMPDIFF()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_timestampdiff) | Subtract an interval from a datetime expression |
| [`TO_DAYS()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_to-days) | Return the date argument converted to days |
| [`TO_SECONDS()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_to-seconds) | Return the date or datetime argument converted to seconds since Year 0 |
| [`UNIX_TIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_unix-timestamp) | Return a Unix timestamp                  |
| [`UTC_DATE()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-date) | Return the current UTC date              |
| [`UTC_TIME()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-time) | Return the current UTC time              |
| [`UTC_TIMESTAMP()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_utc-timestamp) | Return the current UTC date and time     |
| [`WEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_week) | Return the week number                   |
| [`WEEKDAY()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_weekday) | Return the weekday index                 |
| [`WEEKOFYEAR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_weekofyear) | Return the calendar week of the date (1-53) |
| [`YEAR()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_year) | Return the year                          |
| [`YEARWEEK()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_yearweek) | Return the year and week                 |

For details, see [here](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html).
