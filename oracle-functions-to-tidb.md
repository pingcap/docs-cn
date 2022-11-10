---
title: Comparisons between Functions and Syntax of Oracle and TiDB
summary: Learn the comparisons between functions and syntax of Oracle and TiDB.
---

# Comparisons between Functions and Syntax of Oracle and TiDB

This document describes the comparisons between functions and syntax of Oracle and TiDB. It helps you find the corresponding TiDB functions based on the Oracle functions, and understand the syntax differences between Oracle and TiDB.

> **Note:**
>
> The functions and syntax in this document are based on Oracle 12.2.0.1.0 and TiDB v5.4.0. They might be different in other versions.

## Comparisons of functions

The following table shows the comparisons between some Oracle and TiDB functions.

| Function | Oracle syntax | TiDB syntax | Note |
|---|---|---|---|
| Cast a value as a certain type | <li>`TO_NUMBER(key)`</li><li>`TO_CHAR(key)`</li> | `CONVERT(key,dataType)` | TiDB supports casting a value as one of the following types: `BINARY`, `CHAR`, `DATE`, `DATETIME`, `TIME`, `SIGNED INTEGER`, `UNSIGNED INTEGER` and `DECIMAL`. |
| Convert a date to a string | <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd hh24:mi:ss')`</li> <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd')`</li> | <li>`DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s')`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | The format string of TiDB is case-sensitive. |
| Convert a string to a date | <li>`TO_DATE('2021-05-28 17:31:37','yyyy-MM-dd hh24:mi:ss')`</li><li>`TO_DATE('2021-05-28','yyyy-MM-dd hh24:mi:ss')`</li> | <li>`STR_TO_DATE('2021-05-28 17:31:37','%Y-%m-%d %H:%i:%s')`</li><li>`STR_TO_DATE('2021-05-28','%Y-%m-%d%T')` </li> | The format string of TiDB is case-sensitive. |
| Get the current system time in second precision | `SYSDATE` | `NOW()` | |
| Get the current system time in microsecond precision | `SYSTIMESTAMP` | `CURRENT_TIMESTAMP(6)` | |
| Get the number of days between two dates | `date1 - date2` | `DATEDIFF(date1, date2)` | |
| Get the number of months between two dates | `MONTHS_BETWEEN(ENDDATE,SYSDATE)` | `TIMESTAMPDIFF(MONTH,SYSDATE,ENDDATE)` | The results of `MONTHS_BETWEEN()` in Oracle and `TIMESTAMPDIFF()` in TiDB are different. `TIMESTAMPDIFF()` returns an integer. Note that the parameters in the two functions are swapped. |
| Add `n` days to a date | `DATEVAL + n` | `DATE_ADD(dateVal,INTERVAL n DAY)` | `n` can be a negative value.|
| Add `n` months to a date | `ADD_MONTHS(dateVal,n)`| `DATE_ADD(dateVal,INTERVAL n MONTH)` | `n` can be a negative value. |
| Get the day of a date | `TRUNC(SYSDATE)` | <li>`CAST(NOW() AS DATE)`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | In TiDB, `CAST` and `DATE_FORMAT` return the same result. |
| Get the month of a date | `TRUNC(SYSDATE,'mm')` | `DATE_ADD(CURDATE(),interval - day(CURDATE()) + 1 day)`  | |
| Truncate a value | `TRUNC(2.136) = 2`<br/> `TRUNC(2.136,2) = 2.13` | `TRUNCATE(2.136,0) = 2`<br/> `TRUNCATE(2.136,2) = 2.13` | Data precision is preserved. Truncate the corresponding decimal places without rounding. |
| Get the next value in a sequence | `sequence_name.NEXTVAL` | `NEXTVAL(sequence_name)` | |
| Get a random sequence value | `SYS_GUID()` | `UUID()` | TiDB returns a Universal Unique Identifier (UUID). |
| Left join or right join | `SELECT * FROM a, b WHERE a.id = b.id(+);`<br/>`SELECT * FROM a, b WHERE a.id(+) = b.id;` | `SELECT * FROM a LEFT JOIN b ON a.id = b.id;`<br/>`SELECT * FROM a RIGHT JOIN b ON a.id = b.id;` | In a correlated query, TiDB does not support using (+) to left join or right join. You can use `LEFT JOIN` or `RIGHT JOIN` instead. |
| `NVL()` | `NVL(key,val)` | `IFNULL(key,val)` | If the value of the field is `NULL`, it returns `val`; otherwise, it returns the value of the field.  |
| `NVL2()` | `NVL2(key, val1, val2)` | `IF(key is NULL, val1, val2)` | If the value of the field is not `NULL`, it returns `val1`; otherwise, it returns `val2`. |
| `DECODE()` | <li>`DECODE(key,val1,val2,val3)`</li><li>`DECODE(value,if1,val1,if2,val2,...,ifn,valn,val)`</li> | <li>`IF(key=val1,val2,val3)`</li><li>`CASE WHEN value=if1 THEN val1 WHEN value=if2 THEN val2,...,WHEN value=ifn THEN valn ELSE val END`</li> | <li>If the value of the field is `val1`, then it returns `val2`; otherwise it returns `val3`. </li><li>When the value of the field satisfies condition 1 (`if1`), it returns `val1`. When it satisfies condition 2 (`if2`), it returns `val2`. When it satisfies condition 3 (`if3`), it returns `val3`.</li> |
| Concatenate the string `a` and `b` | <code>'a' \|\| 'b'</code> | `CONCAT('a','b')` | |
| Get the length of a string | `LENGTH(str)` | `CHAR_LENGTH(str)` | |
| Get the substring as specified | `SUBSTR('abcdefg',0,2) = 'ab'`<br/> `SUBSTR('abcdefg',1,2) = 'ab'` | `SUBSTRING('abcdefg',0,2) = ''`<br/>`SUBSTRING('abcdefg',1,2) = 'ab'` | <li>In Oracle, the starting position 0 has the same effect as 1. </li><li>In TiDB, the starting position 0 returns an empty string. If you want to get a substring from the beginning, the starting position should be 1.</li> |
| Get the position of a substring | `INSTR('abcdefg','b',1,1)` | `INSTR('abcdefg','b')` | Search from the first character of `'abcdefg'` and return the position of the first occurrence of `'b'`. |
| Get the position of a substring | `INSTR('stst','s',1,2)` | `LENGTH(SUBSTRING_INDEX('stst','s',2)) + 1` | Search from the first character of `'stst'` and return the position of the second occurrence of `'s'`. |
| Get the position of a substring | `INSTR('abcabc','b',2,1)` | `LOCATE('b','abcabc',2)` | Search from the second character of `abcabc` and return the position of the first occurrence of `b`. |
| Concatenate values of a column | `LISTAGG(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY DIMENSIONNAME)` | `GROUP_CONCAT(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***')` | Concatenate values of a specified column to one row with the `***` delimiter. |
| Convert an ASCII code to a character | `CHR(n)` | `CHAR(n)` | The Tab (`CHR(9)`), LF (`CHR(10)`), and CR (`CHR(13)`) characters in Oracle correspond to `CHAR(9)`, `CHAR(10)`, and `CHAR(13)` in TiDB. |

## Comparisons of syntax

This section describes some syntax differences between Oracle and TiDB.

### String syntax

In Oracle, a string can only be enclosed in single quotes (''). For example `'a'`.

In TiDB, a string can be enclosed in single quotes ('') or double quotes (""). For example, `'a'` and `"a"`.

### Difference between `NULL` and an empty string

Oracle does not distinguish between `NULL` and an empty string `''`, that is, `NULL` is equivalent to `''`.

TiDB distinguishes between `NULL` and an empty string `''`.

### Read and write to the same table in an `INSERT` statement

Oracle supports reading and writing to the same table in an `INSERT` statement. For example:

```sql
INSERT INTO table1 VALUES (feild1,(SELECT feild2 FROM table1 WHERE...))
```

TiDB does not support reading and writing to the same table in a `INSERT` statement. For example:

```sql
INSERT INTO table1 VALUES (feild1,(SELECT T.fields2 FROM table1 T WHERE...))
```

### Get the first n rows from a query

In Oracle, to get the first n rows from a query, you can use the `ROWNUM <= n` clause. For example `ROWNUM <= 10`.

In TiDB, to get the first n rows from a query, you can use the `LIMIT n` clause. For example `LIMIT 10`. The Hibernate Query Language (HQL) running SQL statements with `LIMIT` results in an error. You need to change the Hibernate statements to SQL statements.

### Update multiple tables in an `UPDATE` statement

In Oracle, it is not necessary to list the specific field update relationship when updating multiple tables. For example:

```sql
UPDATE test1 SET(test1.name,test1.age) = (SELECT test2.name,test2.age FROM test2 WHERE test2.id=test1.id)
```

In TiDB, when updating multiple tables, you need to list all the specific field update relationships in `SET`. For example:

```sql
UPDATE test1,test2 SET test1.name=test2.name,test1.age=test2.age WHERE test1.id=test2.id
```

### Derived table alias

In Oracle, when querying multiple tables, it is unnecessary to add an alias to the derived table. For example:

```sql
SELECT * FROM (SELECT * FROM test)
```

In TiDB, when querying multiple tables, every derived table must have its own alias. For example:

```sql
SELECT * FROM (SELECT * FROM test) t
```

### Set operations

In Oracle, to get the rows that are in the first query result but not in the second, you can use the `MINUS` set operation. For example:

```sql
SELECT * FROM t1 MINUS SELECT * FROM t2
```

TiDB does not support the `MINUS` operation. You can use the `EXCEPT` set operation. For example:

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2
```

### Comment syntax

In Oracle, the comment syntax is `--Comment`.

In TiDB, the comment syntax is `-- Comment`. Note that there is a white space after `--` in TiDB.

### Pagination

In Oracle, you can use the `OFFSET m ROWS` to skip `m` rows and use the `FETCH NEXT n ROWS ONLY`to fetch `n` rows. For example:

```sql
SELECT * FROM tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY
```

In TiDB, you can use the `LIMIT n OFFSET m` to replace `OFFSET m ROWS FETCH NEXT n ROWS ONLY`. For example:

```sql
SELECT * FROM tables LIMIT 2000 OFFSET 0
```

### Sorting order on `NULL` values

In Oracle, `NULL` values are sorted by the `ORDER BY` clause in the following cases:

- In the `ORDER BY column ASC` statement, `NULL` values are returned last.

- In the `ORDER BY column DESC` statement, `NULL` values are returned first.

- In the `ORDER BY column [ASC|DESC] NULLS FIRST` statement, `NULL` values are returned before non-NULL values. Non-NULL values are returned in ascending order or descending order specified in `ASC|DESC`.

- In the `ORDER BY column [ASC|DESC] NULLS LAST` statement, `NULL` values are returned after non-NULL values. Non-NULL values are returned in ascending order or descending order specified in `ASC|DESC`.

In TiDB, `NULL` values are sorted by the `ORDER BY` clause in the following cases:

- In the `ORDER BY column ASC` statement, `NULL` values are returned first.

- In the `ORDER BY column DESC` statement, `NULL` values are returned last.

The following table shows some examples of equivalent `ORDER BY` statements in Oracle and TiDB:

| `ORDER BY` in Oracle | Equivalent statements in TiDB |
| :------------------- | :----------------- |
| `SELECT * FROM t1 ORDER BY name NULLS FIRST;`      | `SELECT * FROM t1 ORDER BY name;`  |
| `SELECT * FROM t1 ORDER BY name DESC NULLS LAST;`  | `SELECT * FROM t1 ORDER BY name DESC;` |
| `SELECT * FROM t1 ORDER BY name DESC NULLS FIRST;` | `SELECT * FROM t1 ORDER BY ISNULL(name) DESC, name DESC;` |
| `SELECT * FROM t1 ORDER BY name ASC NULLS LAST;`   | `SELECT * FROM t1 ORDER BY ISNULL(name), name;` |
