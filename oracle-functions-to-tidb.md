---
title: Oracle 与 TiDB 函数和语法差异对照
summary: 了解 Oracle 与 TiDB 函数和语法差异对照。
---

# Oracle 与 TiDB 函数和语法差异对照

本文档提供了 Oracle 与 TiDB 的函数和语法差异对照，方便你根据 Oracle 函数查找对应的 TiDB 函数，了解 Oracle 与 TiDB 语法差异。

> **注意：**
>
> 本文的内容是基于 Oracle 12.2.0.1.0 和 TiDB v5.4.0，其他版本可能存在差异。

## 函数对照表

下表列出了 Oracle 与 TiDB 部分函数的对照表。

| 函数 | Oracle 语法 | TiDB 语法 | 说明 |
|---|---|---|---|
| 转换数据类型 | <li>`TO_NUMBER(key)`</li><li>`TO_CHAR(key)`</li> | `CONVERT(key,dataType)` | TiDB 支持转换为下面类型：`BINARY`、`CHAR`、`DATE`、`DATETIME`、`TIME`、`SIGNED INTEGER`、`UNSIGNED INTEGER` 和 `DECIMAL`。 |
| 日期类型转换为字符串类型 | <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd hh24:mi:ss')`</li> <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd')`</li> | <li>`DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s')`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | TiDB 的格式化字符串大小写敏感。 |
| 字符串类型转换为日期类型 | <li>`TO_DATE('2021-05-28 17:31:37','yyyy-MM-dd hh24:mi:ss')`</li><li>`TO_DATE('2021-05-28','yyyy-MM-dd hh24:mi:ss')`</li> | <li>`STR_TO_DATE('2021-05-28 17:31:37','%Y-%m-%d %H:%i:%s')`</li><li>`STR_TO_DATE('2021-05-28','%Y-%m-%d%T')` </li> | TiDB 的格式化字符串大小写敏感。 |
| 获取系统当前时间（精确到秒）| `SYSDATE` | `NOW()` | |
| 获取当前时间（精确到微秒）| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP(6)` | |
| 获取两个日期相差的天数 | `date1 - date2` | `DATEDIFF(date1, date2)` | |
| 获取两个日期间隔月份 | `MONTHS_BETWEEN(ENDDATE,SYSDATE)` | `TIMESTAMPDIFF(MONTH,SYSDATE,ENDDATE)` | Oracle 中 `MONTHS_BETWEEN()` 函数与 TiDB 中 `TIMESTAMPDIFF()` 函数的结果会有误差。`TIMESTAMPDIFF()` 只保留整数月。使用时需要注意，两个函数的参数位置相反。 |
| 日期增加/减少 n 天 | `DATEVAL + n` | `DATE_ADD(dateVal,INTERVAL n DAY)` | `n` 可为负数。|
| 日期增加/减少 n 月 | `ADD_MONTHS(dateVal,n)`| `DATE_ADD(dateVal,INTERVAL n MONTH)` | `n` 可为负数。|
| 获取日期到日 | `TRUNC(SYSDATE)` | <li>`CAST(NOW() AS DATE)`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | TiDB 中 `CAST` 与 `DATE_FORMAT` 结果一致。|
| 获取日期当月第一天 | `TRUNC(SYSDATE,'mm')` | `DATE_ADD(CURDATE(),interval - day(CURDATE()) + 1 day)`  | |
| 截取数据 | `TRUNC(2.136) = 2`<br/> `TRUNC(2.136,2) = 2.13` | `TRUNCATE(2.136,0) = 2`<br/> `TRUNCATE(2.136,2) = 2.13` | 数据精度保留，直接截取相应小数位，不涉及四舍五入。 |
| 获取序列下一个值 | `sequence_name.NEXTVAL` | `NEXTVAL(sequence_name)` | |
| 获取随机序列值 | `SYS_GUID()` | `UUID()` | TiDB 返回一个通用唯一识别码 (UUID)。|
| 左/右外连接 | `SELECT * FROM a, b WHERE a.id = b.id(+);`<br/>`SELECT * FROM a, b WHERE a.id(+) = b.id;` | `SELECT * FROM a LEFT JOIN b ON a.id = b.id;`<br/>`SELECT * FROM a RIGHT JOIN b ON a.id = b.id;` | 关联查询时，TiDB 不支持使用 (+) 实现左/右关联，只能通过 `LEFT JOIN` 或 `RIGHT JOIN` 实现。|
| `NVL()` | `NVL(key,val)` | `IFNULL(key,val)` | 如果该字段值为 `NULL`，则返回 val 值，否则返回该字段的值。 |
| `NVL2()` | `NVL2(key, val1, val2)`  | `IF(key is NOT NULL, val1, val2)` | 如果该字段值非 `NULL`，则返回 val1 值，否则返回 val2 值。|
| `DECODE()` | <li>`DECODE(key,val1,val2,val3)`</li><li>`DECODE(value,if1,val1,if2,val2,...,ifn,valn,val)`</li> | <li>`IF(key=val1,val2,val3)`</li><li>`CASE WHEN value=if1 THEN val1 WHEN value=if2 THEN val2,...,WHEN value=ifn THEN valn ELSE val END`</li> | <li>如果该字段值等于 val1，则返回 val2，否则返回 val3。</li><li>当该字段值满足条件 1 (if1) 时，返回 val1，满足条件 2 (if2) 时，返回 val2，满足条件 3 (if3) 时，返回 val3。</li> |
| 拼接字符串 `a` 和 `b` | <code>'a' \|\| 'b'</code>  | `CONCAT('a','b')` | |
| 获取字符串长度 | `LENGTH(str)` | `CHAR_LENGTH(str)` | |
| 获取子串 | `SUBSTR('abcdefg',0,2) = 'ab'`<br/> `SUBSTR('abcdefg',1,2) = 'ab'` | `SUBSTRING('abcdefg',0,2) = ''`<br/>`SUBSTRING('abcdefg',1,2) = 'ab'` | <li>Oracle 中起始位置 0 与 1 作用一样。</li><li>TiDB 中 0 开始获取的子串为空，若需从字符串的起始位置开始，则应从 1 开始。</li> |
| 字符串在源字符串中的位置 | `INSTR('abcdefg','b',1,1)` | `INSTR('abcdefg','b')` | 从字符串 `'abcdefg'` 第一个字符开始查询，返回 `'b'` 字符串第一次出现的位置。 |
| 字符串在源字符串中的位置 | `INSTR('stst','s',1,2)` | `LENGTH(SUBSTRING_INDEX('stst','s',2)) + 1` | 从字符串 `'stst'` 第一个字符开始查找，返回 `'s'` 字符第二次出现的位置。 |
| 字符串在源字符串中的位置 | `INSTR('abcabc','b',2,1)` | `LOCATE('b','abcabc',2)` | 从字符串 `'abcabc'` 第二个字符开始查询，返回 `'b'` 字符第一次出现的位置。 |
| 列合并为行 | `LISTAGG(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY  DIMENSIONNAME)` | `GROUP_CONCAT(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***')` | 将一列字段合并为一行并根据 `***` 符号进行分割。 |
| ASCII 值转化为对应字符 | `CHR(n)` | `CHAR(n)` | Oracle 中制表符 (`CHR(9)`)、换行符 (`CHR(10)`)、回车符 (`CHR(13)`) 对应 TiDB 中的 `CHAR(9)`、`CHAR(10)`、`CHAR(13)`。 |

## 语法差异

本节介绍 Oracle 部分语法与 TiDB 的差异。

### 字符串语法

Oracle 中字符串只能使用单引号 ('')。例如 `'a'`。

TiDB 中字符串可以使用单引号 ('') 或双引号 ("")。例如 `'a'` 或 `"a"`。

### `NULL` 与空字符串的区分

Oracle 中不区分 `NULL` 和空字符串 `''`，即 `NULL` 与 `''` 是等价的。

TiDB 中区分 `NULL` 和空字符串 `''`。

### `INSERT` 语句中读写同一张表

Oracle 支持 `INSERT` 语句中读写同一张表。例如：

```sql
INSERT INTO table1 VALUES (field1,(SELECT field2 FROM table1 WHERE...))
```

TiDB 不支持 `INSERT` 语句中读写同一张表。例如：

```sql
INSERT INTO table1 VALUES (field1,(SELECT T.fields2 FROM table1 T WHERE...))
```

### 获取前 n 行数据

Oracle 通过 `ROWNUM <= n` 获取前 n 行数据。例如，`ROWNUM <= 10`。

TiDB 通过 `LIMIT n` 获取前 n 行数据。例如，`LIMIT 10`。Hibernate Query Language (HQL) 方式运行带 `LIMIT` 的 SQL 语句会出现错误，需要将 Hibernate 的运行方式改为 SQL 方式运行。

### `UPDATE` 语句多表更新

Oracle 多表更新时不需要列出具体的字段更新关系。例如：

```sql
UPDATE test1 SET(test1.name,test1.age) = (SELECT test2.name,test2.age FROM test2 WHERE test2.id=test1.id)
```

TiDB 多表更新时需要在 `SET` 时把具体的字段更新关系都列出来。例如：

```sql
UPDATE test1,test2 SET test1.name=test2.name,test1.age=test2.age WHERE test1.id=test2.id
```

### 派生表别名

Oracle 多表查询时，派生表可以不起别名。例如：

```sql
SELECT * FROM (SELECT * FROM test)
```

TiDB 多表查询时，每一个派生出来的表都必须有一个自己的别名。例如：

```sql
SELECT * FROM (SELECT * FROM test) t
```

### 差集运算

Oracle 使用 `MINUS` 进行差集运算。例如：

```sql
SELECT * FROM t1 MINUS SELECT * FROM t2
```

TiDB 不支持 `MINUS`，需要改写为 `EXCEPT` 进行差集运算。例如：

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2
```

### 注释语法

Oracle 中注释语法为 `--注释`，其中 `--` 后面不需要空格。

TiDB 中注释语法为 `-- 注释`，其中 `--` 后面需要有一个空格。

### 分页查询

Oracle 分页查询时 `OFFSET m` 表示跳过 `m` 行数据，`FETCH NEXT n ROWS ONLY` 表示取 `n` 条数据。例如：

```sql
SELECT * FROM tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY
```

TiDB 使用 `LIMIT n OFFSET m` 等价改写 `OFFSET m ROWS FETCH NEXT n ROWS ONLY`。例如：

```sql
SELECT * FROM tables LIMIT 2000 OFFSET 0
```

### `ORDER BY` 语句对 `NULL` 的排序规则

Oracle 中 `ORDER BY` 语句对 `NULL` 的排序规则：

- `ORDER BY COLUMN ASC` 时，`NULL` 默认被放在最后。

- `ORDER BY COLUMN DESC` 时，`NULL` 默认被放在最前。

- `ORDER BY COLUMN [ASC|DESC] NULLS FIRST` 时，强制 `NULL` 放在最前，非 `NULL` 的值仍然按声明顺序 `ASC|DESC` 进行排序。

- `ORDER BY COLUMN [ASC|DESC] NULLS LAST` 时，强制 `NULL` 放在最后，非 `NULL` 的值仍然按声明顺序 `ASC|DESC` 进行排序。

TiDB 中 `ORDER BY` 语句对 `NULL` 的排序规则：

- `ORDER BY COLUMN ASC` 时，`NULL` 默认被放在最前。

- `ORDER BY COLUMN DESC` 时，`NULL` 默认被放在最后。

下表是 Oracle 与 TiDB 中等价 `ORDER BY` 语句示例：

| Oracle 中的 `ORDER BY` | TiDB 中的 `ORDER BY`|
| :------------------- | :----------------- |
| `SELECT * FROM t1 ORDER BY name NULLS FIRST;`      | `SELECT * FROM t1 ORDER BY name;`                         |
| `SELECT * FROM t1 ORDER BY name DESC NULLS LAST;`  | `SELECT * FROM t1 ORDER BY name DESC;`                    |
| `SELECT * FROM t1 ORDER BY name DESC NULLS FIRST;` | `SELECT * FROM t1 ORDER BY ISNULL(name) DESC, name DESC;` |
| `SELECT * FROM t1 ORDER BY name ASC NULLS LAST;`   | `SELECT * FROM t1 ORDER BY ISNULL(name), name;`           |
