---
title: Oracle 与 TiDB 函数对照表
summary: 了解 Oracle 与 TiDB 函数对照表。
---

# Oracle 与 TiDB 函数对照表

本文档提供了 Oracle 与 TiDB 的函数对照表，方便你根据 Oracle 函数查找对应的 TiDB 函数。

| 函数 | Oracle 语法 | TiDB 语法 | 说明 |
|---|---|---|---|
| 转换表字段值数据类型 | <li>`TO_NUMBER(key)`</li><li>`TO_CHAR(key)`</li> | `CONVERT(key,dataType)` | TiDB 支持转换 `BINARY`、`CHAR`、`DATE`、`DATETIME`、`TIME`、`SIGNED INTEGER`、`UNSIGNED INTEGER` 和 `DECIMAL` 类型。 |
| 日期类型转换为字符串类型 | <li>`TO_CHAR(sysdate,'yyyy-MM-dd hh24:mi:ss')`</li> <li>`TO_CHAR(sysdate,'yyyy-MM-dd')`</li>      | <li>`DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s')`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | TiDB 的年月日时分秒字符大小写必须严格按要求写。 |
| 字符串类型转换为日期类型 | <li>`TO_DATE('2021-05-28 17:31:37','yyyy-MM-dd hh24:mi:ss')`</li><li>`TO_DATE('2021-05-28','yyyy-MM-dd hh24:mi:ss')`</li> | <li>`STR_TO_DATE('2021-05-28 17:31:37','%Y-%m-%d %H:%i:%s')`</li><li>`STR_TO_DATE('2021-05-28','%Y-%m-%d%T')` </li> | TiDB 的年月日时分秒字符大小写必须严格按要求写。 |
| 获取系统当前时间（精确到秒）| `SYSDATE` | `NOW()` | |
| 获取两个日期 `date1` 和 `date2` 相差的天数（精确到天）| `date1 - date2` | `DATEDIFF(date1, date2)` | |
| 日期数据 +/- n 天 | `DATEVAL + n` | `DATE_ADD(dateVal,INTERVAL n DAY)` | 日期数据增加 `n` 天，`n` 可为负数 |
| 日期数据 +/- n 月 | `ADD_MONTHS(dateVal,n)`| `DATE_ADD(dateVal,INTERVAL n MONTH)` | 日期数据增加 `n` 月，`n` 可为负数。 |
| 获取日期到日 | `TRUNC(sysdate)` | <li>`CAST(now() as date)`</li><li>`DATE_FORMAT(now(),'%Y-%m-%d')`</li> | <li>获取时间格式（2019-07-26 00:00:00）的返回值。Oracle 中的 `TRUNC(sysdate)` 只是截取到日，不会截取到时分秒。而 TiDB 中与之对应的截取日写法是 `CAST(now() as date)`。</li><li>`CAST` 与 `DATE_FORMAT` 结果一致。</li> |
| 获取日期当月第一天 | `TRUNC(sysdate,'mm')` | `DATE_ADD(curdate(),interval -day(curdate())+1 day)`  | |
| 截取数据 | `TRUNC(2.136)` => 2<br/> `TRUNC(2.136,2)` => 2.14 | `TRUNCATE(2.136,0)` => 2<br/> `TRUNCATE(2.136,2)` => 2.14 | 数据精度保留，直接截取相应小数位，不涉及四舍五入。 |
| 拼接字符串 `a` 和 `b` | a' \|\| 'b' | `CONCAT('a','b')` | |
| 删除语句中对表加别名 | `DELETE FROM test t WHERE t.xxx = xxx;` | `DELETE FROM test WHERE xxx = xxx;` | TiDB 不支持删除语句中为表起别名。 |
| 获取序列下一个值 | `SEQUENCENAME.NEXTVAL` | `NEXTVAL(sequenceName)` | |
| 左/右外连接 | `SELECT * FROM a, b WHERE a.id = b.id(+);`<br/>`SELECT * FROM a, b WHERE a.id(+) = b.id;` | `SELECT * FROM a LEFT JOIN b ON a.id = b.id;`<br/>`SELECT * FROM a RIGHT JOIN b ON a.id = b.id;` | 关联查询时，TiDB 不支持使用 (+) 实现左/右关联，只能通过 `LEFT/RIGHT JOIN` 实现。|
| 获取随机序列值 | `SYS_GUID()` | `UUID()` | TiDB 返回一个通用唯一识别码 (UUID)。|
| `NVL()` 函数 | `NVL(key,val)` | `IFNULL(key,val)` | 如果该字段值为空，则返回 val 值，否则返回该字段的值。 |
| `NVL2()` 函数 | `NVL2(key, val1, val2)`  | `if(key is null, val1, val2)` | 如果该字段值非 NULL，则返回 val1 值，否则返回 val2 值。       |
| `DECODE()` 函数 | <li>`DECODE(key,val1,val2,val3)`</li><li>`DECODE(value,if1,val1,if2,val2,...,ifn,valn,val)`</li> | <li>`IF(key=val1,val2,val3)`</li><li>`CASE WHEN value=if1 THEN val1 WHEN value=if2 THEN val2,,,WHEN value=ifn THEN valn ELSE val END`</li> | <li>如果该字段值对于 val1，则返回 val2，否则返回 val3。</li><li>当该字段值等于条件 1 时，返回 val1，等于条件 2 时，返回 val2… </li> |
| 获取字符串长度 | `LENGTH(str)` | `CHAR_LENGTH(str)` | |
| 截取字符串 | `SUBSTR('abcdefg',0,2)` => ab<br/> `SUBSTR('abcdefg',1,2)` => ab | `SUBSTRING('abcdefg',0,2)` => 空<br/>`SUBSTRING('abcdefg',1,2)` => ab | Oracle 中起始位置 0 与 1 作用一样，TiDB 中 0 开始截取为空，若需从头开始截全，则应从 1 开始，TiDB 支持 SUBSTRING 和 SUBSTR 函数，作用相同，不用修改。但是注意 TiDB 的下表必须从 1 开始。 |
| 字符查找函数 INSTR | `INSTR('abcdefg','b',1,1)` | `INSTR('abcdefg','b')` | 从字符串 'abcdefg' 第 1 个字符开始查询，返回 'b' 字符串第 1 次出现按的位置。 |
| 字符查找函数 INSTR | `INSTR('stst','s',1,2)` | `LENGTH(SUBSTRING_INDEX('stst','s',2))+1` | 从字符串 'stst' 第一个字符开始查找，返回 's' 字符第 2 次出现的位置，查找非第一次出现的位置时使用。 |
| 字符查找函数 | `INSTR('abcabc','b',2,1)` | `LOCATE('b','abcabc',2)` | 字符查找函数。从字符串 `abcabc` 第 2 个字符开始查询，返回 `b` 字符串第 1 次出现按的位置。 |
| 字符串引号识别区别 | 'a' | 'a' / "a" | Oracle 只能识别单引号，TiDB 能识别单引号与双引号。 |
| NULL 与空串区别 | 不区分 NULL 和 '' | 区分 NULL 和 '' | Oracle 空串就是 NULL，TiDB 需要把空串转换为 NULL 数据。TiDB 中 NULL 和 '' 是有区别的。 |
| 插入本表中查询出来的数据 | `INSERT INTO table1 VALUES (feild1,(SELECT feild2 FROM table1 WHERE...))` | `INSERT INTO table1 VALUES（feild1,(SELECT T.fields2 FROM table1 T WHERE...)` | TiDB 不支持在同一个表中先查这个表再更新该表。 |
| 获取日期之间间隔月份 | `MONTHS_BETWEEN(enddate,sysdate)` | `TIMESTAMPDIFF(MONTH,sysdate,enddate)` |  `MONTHS_BETWEEN` 函数返回两个日期之间的月份值，可以用 `TIMESTAMPDIFF` 替换，但是结果上会有误差，`TIMESTAMPDIFF` 只保留整数月，应该测试后按照业务看是否替换，另外注意参数位置相反。 |
| 限制取前 n 条数据 | `ROWNUM <= 10` | `LIMIT 10` | Oracle 中的 `ROWNUM` 可以使用 `LIMIT` 等价代替。Hibernate Query Language (HQL) 方式运行带 `LIMIT` 的 SQL 语句会出现错误，需要将 Hibernate 的运行方式改为 SQL 方式运行。 |
| UPDATE 语句 | `UPDATE test1 SET(test1.name,test1.age)= (SELECT test2.name,test2.age FROM test2 WHERE test2.id=test1.id)` | `UPDATE test1,test2 SET test1.name=test2.name,test1.age=test2.age WHERE test1.id=test2.id` | TiDB 在多表更新的时候，需要在 `SET` 的时候把具体的字段更新关系都列出来。 |
| 派生表别名 | `SELECT * FROM (SELECT * FROM test)` | `SELECT * FROM (SELECT * FROM test)` t | TiDB 多表查询的时候，每一个派生出来的表都必须有一个自己的别名。 |
| 差集运算 | `SELECT * FROM t1 MINUS SELECT * FROM t2;` | `SELECT * FROM t1 EXCEPT SELECT * FROM t2;` | TiDB 不支持 `MINUS`，需要改写为 `EXCEPT`。 |
| 空值取别名 | `SELECT null AS xx FROM dual` | `SELECT '' AS xx FROM dual` | NULL 与 '' 在 TiDB 中含义不同。Oracle 中 NULL 在 TiDB 中需要改写为 ''。|
| 注释 |  `--注释` |  `-- 注释` | Oracle 的 `--` 后面不需要空格，TiDB 的 `--` 后面需要有一个空格。|
| 列转行函数 | `LISTAGG(concat(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY  DIMENSIONNAME)` | `GROUP_CONCAT(concat(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***')` | Oracle 中的 `LISTAGG` 需要改写为 TiDB 的 `GROUP_CONCAT` 函数；将一列字段合并为一行并根据 `***` 符号进行分割。 |
| 分页查询 | `SELECT * FROM tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY` | `SELECT * FROM tables LIMIT 2000 OFFSET 0` | Oracle 中 `OFFSET m` 表示跳过 `m` 行数据，`FETCH NEXT n ROWS ONLY` 表示取 `n` 条数据。TiDB 使用 `LIMIT n OFFSET m` 等价改写 `OFFSET m ROWS FETCH NEXT n ROWS ONLY`。 |
| 获取当前时间（精确到微秒）| `SYSTIMESTAMP` | `CURRENT_TIMESTAMP(6)` | |
| ASCII 值转化为对应字符 | `CHR(n)` | `CHAR(n)` | Oracle 中制表符 `CHR(9)`/换行符 `CHR(10)`/回车符 `CHR(13)` 对应 TiDB 中的 `CHAR(9)`/`CHAR(10)`/`CHAR(13)`。 |
| Oracle 和 TiDB 排序 NULL 的顺序不同 | `ORDER BY COLUM ASC NULLS FIRST` | `ORDER BY COLUM ASC` | Oracle 实现方式：`ORDER BY COLUM ASC` 时，NULL 默认被放在最后；ORDER BY COLUM DESC 时，NULL 默认被放在最前。NULLS FIRST 时，强制 NULL 放在最前，非 NULL 的仍然按声明顺序 [ASC\|DESC] 进行排序。NULLS LAST 时，强制 NULL 放在最后，非 NULL 的仍然按声明顺序 [ASC\|DESC] 进行排序。<br/>MySQL 和 TiDB 的实现方式：ORDER BY COLUM ASC 时，NULL 默认被放在最前。`ORDER BY COLUM DESC` 时，NULL 默认被放在最后。<br/>`O：SELECT * FROM t1 ORDER BY name NULLS FIRST;` 等价于 `T：SELECT * FROM t1 ORDER BY NAME ;` 。<br/>`O：SELECT * FROM t1 ORDER BY name DESC NULLS LAST;` 等价于 `T：SELECT * FROM t1 ORDER BY NAME DESC;`。<br/>`O：SELECT * FROM t1 ORDER BY NAME DESC NULLS FIRST;` 等价于 `T：SELECT * FROM t1 ORDER BY ISNULL(name) DESC, name DESC;`。<br/>`O：SELECT * FROM t1 ORDER BY name ASC NULLS LAST;` 等价于 `T：SELECT * FROM t1 ORDER BY ISNULL(name), name;` |
