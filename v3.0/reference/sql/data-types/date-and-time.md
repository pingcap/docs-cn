---
title: Date and Time Types
summary: Learn about the supported date and time types.
category: reference
aliases: ['/docs/sql/date-and-time-types/']
---

# Date and Time Types

TiDB supports the following data types to store temporal values: `DATE`, `TIME`, `DATETIME`, `TIMESTAMP`, and `YEAR`. Each of these types has its own range of valid values, and uses a zero value to indicate that it is an invalid value. In addition, the `TIMESTAMP` and `DATETIME` types can automatically generate new time values on modification.

When dealing with date and time value types, note: 

+ Although TiDB tries to interpret different formats, the date-portion must be in the format of year-month-day (for example, '1998-09-04'), rather than month-day-year or day-month-year.
+ If the year-portion of a date is specified as 2 digits, TiDB converts it based on [specific rules](#two-digit-year-portion-contained-in-the-date).
+ If a numeric value is needed in the context, TiDB automatically converts the date or time value into a numeric type. For example:

    ```sql
    mysql> SELECT NOW(), NOW()+0, NOW(3)+0;
    +---------------------+----------------+--------------------+
    | NOW()               | NOW()+0        | NOW(3)+0           |
    +---------------------+----------------+--------------------+
    | 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
    +---------------------+----------------+--------------------+
    ```
  
+ TiDB might automatically convert invalid values or values beyond the supported range to a zero value of that type. This behavior is dependent on the SQL Mode set. For example:

    ```sql
    mysql> show create table t1;
    +-------+---------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                            |
    +-------+---------------------------------------------------------------------------------------------------------+
    | t1    | CREATE TABLE `t1` (
      `a` time DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
    +-------+---------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
    
    mysql> select @@sql_mode;
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | @@sql_mode                                                                                                                                |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    | ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION |
    +-------------------------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)
  
    mysql> insert into t1 values ('2090-11-32:22:33:44');
    ERROR 1292 (22007): Truncated incorrect time value: '2090-11-32:22:33:44'
    mysql> set @@sql_mode='';                                                                                                                                                                                                                     Query OK, 0 rows affected (0.01 sec)
    
    mysql> insert into t1 values ('2090-11-32:22:33:44');
    Query OK, 1 row affected, 1 warning (0.01 sec)
    
    mysql> select * from t1;
    +----------+
    | a        |
    +----------+
    | 00:00:00 |
    +----------+
    1 row in set (0.01 sec)
    ```

+ Setting different SQL modes can change TiDB behaviors.
+ If the SQL mode `NO_ZERO_DATE` is not enabled, TiDB allows month or day in the columns of `DATE` and `DATETIME` to be zero value, for example, '2009-00-00' or '2009-01-00'. If this date type is to be calculated in a function, for example, in `DATE_SUB()` or `DATE_ADD()`, the result can be incorrect. 
+ By default, TiDB enables the SQL mode `NO_ZERO_DATE`. This mode prevents storing zero values such as '0000-00-00'.

Different types of zero value are shown in the following table:

| Date Type | "Zero" Value |
| :------   |  :----       |
| DATE      | '0000-00-00' |
| TIME      | '00:00:00'   |
| DATETIME  | '0000-00-00 00:00:00' |
| TIMESTAMP | '0000-00-00 00:00:00' |
| YEAR      | 0000         |

Invalid `DATE`, `DATETIME`, `TIMESTAMP` values are automatically converted to the corresponding type of zero value ( '0000-00-00' or '0000-00-00 00:00:00' ) if the SQL mode permits such usage.

### Automatic initialization and update of `TIMESTAMP` and `DATETIME`

Columns with `TIMESTAMP` or `DATETIME` value type can be automatically initialized or updated to the current time.

For any column with `TIMESTAMP` or `DATETIME` value type in the table, you can set the default or auto-update value as current timestamp. 

These properties can be set by setting `DEFAULT CURRENT_TIMESTAMP` and `ON UPDATE CURRENT_TIMESTAMP` when the column is being defined. DEFAULT can also be set as a specific value, such as `DEFAULT 0` or `DEFAULT '2000-01-01 00:00:00'`.

```sql
CREATE TABLE t1 (
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    dt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

The default value for `DATETIME` is `NULL` unless it is specified as `NOT NULL`. For the latter situation, if no default value is set, the default value is be 0.

```sql
CREATE TABLE t1 (
    dt1 DATETIME ON UPDATE CURRENT_TIMESTAMP,         -- default NULL
    dt2 DATETIME NOT NULL ON UPDATE CURRENT_TIMESTAMP -- default 0
);
```

### Decimal part of time value

`DATETIME` and `TIMESTAMP` values can contain a fractional part of up to 6 digits which is accurate to milliseconds. In any column of `DATETIME` or `TIMESTAMP` types, a fractional part is stored instead of being discarded. With a fractional part, the value is in the format of 'YYYY-MM-DD HH:MM:SS[.fraction]', and the fraction ranges from 000000 to 999999. A decimal point must be used to separate the fraction from the rest.

+ Use `type_name(fsp)` to define a column that supports fractional precision, where `type_name` can be `TIME`, `DATETIME` or `TIMESTAMP`. For example,

    ```sql
    CREATE TABLE t1 (t TIME(3), dt DATETIME(6));
    ```

  `fsp` must range from 0 to 6. 

  `0` means there is no fractional part. If `fsp` is omitted, the default is 0.

+ When inserting `TIME`, `DATETIME` or `TIMESTAMP` which contain a fractional part, if the number of digit of the fraction is too few, or too many, rounding might be needed in the situation. For example:

    ```sql
    mysql> CREATE TABLE fractest( c1 TIME(2), c2 DATETIME(2), c3 TIMESTAMP(2) );
    Query OK, 0 rows affected (0.33 sec)
    
    mysql> INSERT INTO fractest VALUES
         > ('17:51:04.777', '2014-09-08 17:51:04.777',   '2014-09-08 17:51:04.777');
    Query OK, 1 row affected (0.03 sec)
    
    mysql> SELECT * FROM fractest;
    +-------------|------------------------|------------------------+
    | c1          | c2                     | c3                     |
    +-------------|------------------------|------------------------+
    | 17:51:04.78 | 2014-09-08 17:51:04.78 | 2014-09-08 17:51:04.78 |
    +-------------|------------------------|------------------------+
    1 row in set (0.00 sec)
    ```

### Conversions between date and time types

Sometimes we need to make conversions between date and time types. But some conversions might lead to information loss. For example, `DATE`, `DATETIME` and `TIMESTAMP` values all have their own respective ranges. `TIMESTAMP` should be no earlier than the year 1970 in UTC time or no later than UTC time '2038-01-19 03:14:07'. Based on this rule, '1968-01-01' is a valid date value of `DATE` or `DATETIME`, but becomes 0 when it is converted to `TIMESTAMP`.

The conversions of `DATE`:

+ When `DATE` is converted to `DATETIME` or `TIMESTAMP`, a time-portion '00:00:00' is added, because DATE does not contain any time information
+ When `DATE` is converted to `TIME`, the result is '00:00:00'

Conversions of `DATETIME` or `TIMESTAMP`:

+ When `DATETIME` or `TIMESTAMP` is converted to `DATE`, the time and fractional part is discarded. For example, '1999-12-31 23:59:59.499' is converted to '1999-12-31'
+ When `DATETIME` or `TIMESTAMP` is converted to TIME, the time-portion is discarded, because `TIME` does not contain any time information

When we convert `TIME` to other time and date formats, the date-portion is automatically specified as `CURRENT_DATE()`. The final converted result is a date that consists of `TIME` and `CURRENT_DATE()`. This is to say that if the value of TIME is beyond the range from '00:00:00' to '23:59:59', the converted date-portion does not indicate the current day.

When `TIME` is converted to `DATE`, the process is similar, and the time-portion is discarded.

Using the `CAST()` function can explicitly convert a value to a `DATE` type. For example:

```sql
date_col = CAST(datetime_col AS DATE)
```

Converting `TIME` and `DATETIME` to numeric format. For example:

```sql
mysql> SELECT CURTIME(), CURTIME()+0, CURTIME(3)+0;
+-----------|-------------|--------------+
| CURTIME() | CURTIME()+0 | CURTIME(3)+0 |
+-----------|-------------|--------------+
| 09:28:00  |       92800 |    92800.887 |
+-----------|-------------|--------------+
mysql> SELECT NOW(), NOW()+0, NOW(3)+0;
+---------------------|----------------|--------------------+
| NOW()               | NOW()+0        | NOW(3)+0           |
+---------------------|----------------|--------------------+
| 2012-08-15 09:28:00 | 20120815092800 | 20120815092800.889 |
+---------------------|----------------|--------------------+
```

### Two-digit year-portion contained in the date

The two-digit year-portion contained in date does not explicitly indicate the actual year and is ambiguous. 

For `DATETIME`, `DATE` and `TIMESTAMP` types, TiDB follows the following rules to eliminate ambiguity: 

- Values between 00 and 69 is converted to a value between 2000 and 2069
- Values between 70 and 99 is converted to a value between 1970 and 1999

These rules also apply to the `YEAR` type, with one exception:

When numeral `00` is inserted to `YEAR(4)`, the result is 0000 rather than 2000. 

If you want the result to be 2000, specify the value to be 2000, '0' or '00'.

The two-digit year-portion might not be properly calculated in some functions such  `MIN()` and  `MAX()`. For these functions, the four-digit format suites better.

## Supported types

### `DATE` type

`DATE` only contains date-portion and no time-portion, displayed in `YYYY-MM-DD` format. The supported range is '1000-01-01' to '9999-12-31':

```sql
DATE
```

### `TIME` type

For the `TIME` type, the format is `HH:MM:SS[.fraction]` and valid values range from '-838:59:59.000000' to '838:59:59.000000'. `TIME` is used not only to indicate the time within a day but also to indicate the time interval between 2 events.  An optional `fsp` value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0:

```sql
TIME[(fsp)]
```

> **Note:**
> 
> Pay attention to the abbreviated form of `TIME`. For example, '11:12' means '11:12:00' instead of '00:11:12'. However, '1112' means '00:11:12'. These differences are caused by the presence or absence of the `:` character.

### `DATETIME` type

`DATETIME` contains both date-portion and time-portion. Valid values range from '1000-01-01 00:00:00.000000' to '9999-12-31 23:59:59.999999'.

TiDB displays `DATETIME` values in `YYYY-MM-DD HH:MM:SS[.fraction]` format, but permits assignment of values to `DATETIME` columns using either strings or numbers.  An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0:

```sql
DATETIME[(fsp)]
```

### `TIMESTAMP` type

`TIMESTAMP` contains both date-portion and time-portion. Valid values range from '1970-01-01 00:00:01.000000' to '2038-01-19 03:14:07.999999' in UTC time. An optional fsp value in the range from 0 to 6 may be given to specify fractional seconds precision. If omitted, the default precision is 0.

In `TIMESTAMP`, zero is not permitted to appear in the month-portion or day-portion. The only exception is zero value itself '0000-00-00 00:00:00'.

```sql
TIMESTAMP[(fsp)]
```

#### Timezone Handling

When `TIMESTAMP` is to be stored, TiDB converts the `TIMESTAMP` value from the current time zone to UTC time zone. When `TIMESTAMP`  is to be retrieved, TiDB converts the stored `TIMESTAMP` value from UTC time zone to the current time zone (Note: `DATETIME` is not handled in this way). The default time zone for each connection is the server's local time zone, which can be modified by the environment variable `time_zone`.

> **Warning:**
> 
> As in MySQL, the `TIMESTAMP` data type suffers from the [Year 2038 Problem](https://en.wikipedia.org/wiki/Year_2038_problem). For storing values that may span beyond 2038, please consider using the `DATETIME` type instead.

### `YEAR` type

The `YEAR` type is specified in the format 'YYYY'. Supported values range from 1901 to 2155, or the zero value of 0000:

```sql
YEAR[(4)]
```

`YEAR` follows the following format rules:

+ Four-digit numeral ranges from 1901 to 2155
+ Four-digit string ranges from '1901' to '2155'
+ One-digit or two-digit numeral ranges from 1 to 99. Accordingly, 1-69 is converted to 2001-2069 and 70-99 is converted to 1970-1999
+ One-digit or two-digit string ranges from '0' to '99'
+ Value 0 is taken as 0000 whereas the string '0' or '00' is taken as 2000

Invalid `YEAR` value is automatically converted to 0000 (if users are not using the `NO_ZERO_DATE` SQL mode).
