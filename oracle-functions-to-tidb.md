---
title: Oracle 与 TiDB 函数对照表
summary: 了解 Oracle 与 TiDB 函数对照表。
---

# Oracle 与 TiDB 函数对照表

本文档提供了 Oracle 与 TiDB 的函数对照表，方便你根据 Oracle 函数查找对应的 TiDB 函数。

| 序号 | 语法差异点 | Oracle | TiDB  | 说明 |
|---|---|---|---|---|
| 1 | 数据类型转换函数 | to_number(key) | convert(key, dataType) | 转换表字段值数据类型，TiDB 支持 BINARY、CHAR、DATE、DATETIME、TIME、SIGNED INTEGER、UNSIGNED INTEGER、DECIMAL。 |
| 2 | 数据类型转换函数 | to_char(key) | convert(key, dataType) | 转换表字段值数据类型，TiDB 支持 BINARY、CHAR、DATE、DATETIME、TIME、SIGNED INTEGER、UNSIGNED INTEGER、DECIMAL。 |
| 3 | 日期转换字符串函数 | to_char(sysdate,'yyyy-MM-dd hh24:mi:ss')       | date_format(now(), '%Y-%m-%d %H:%i:%s') | 日期类型转换字符型函数，TiDB 的年月日时分秒字符大小写必须严格按要求写。 |
| 4 | 日期转换字符串函数 | to_char(sysdate, 'yyyy-MM-dd')       | date_format(now(), '%Y-%m-%d') | 日期类型转换字符型函数。TiDB 的年月日时分秒字符大小写必须严格按要求走写。 |
| 5 | 字符串转换日期函数 | to_date('2021-05-28 17:31:37', 'yyyy-MM-dd hh24:mi:ss') | str_to_date('2021-05-28   17:31:37', '%Y-%m-%d %H:%i:%s') | 字符型转换日期型函数，TiDB 的年月日时分秒字符大小写必须严格按要求写。 |
| 6 | 字符串转换日期函数 | to_date('2021-05-28',   'yyyy-MM-dd hh24:mi:ss')       | str_to_date('2021-05-28',   '%Y-%m-%d%T') | 字符型转换日期型函数，TiDB 年月日时分秒字符大小写必须严格按要求写。 |
| 7 | Sysdate 关键字 | SYSDATE | NOW() | 获取系统当前时间。 |
| 8 | 获取两个日期相差的天数 | date1 - date2 | datediff(date1, date2) | 获取 date1 - date2 两个日期之间相差的天数，只能精确到天。 |
| 9 | 日期数据 +/- n 天 | dateVal + n | date_add(dateVal, INTERVAL n DAY) | 日期数据增加 `n` 天，`n` 可为负数 |
| 10 | 日期数据 +/- n 月 date_add() 函数替换 add_months() 函数 | add_months(dateVal, 1) | date_add(dateVal,   INTERVAL n MONTH) | 日期数据增加 `n` 月，`n` 可为负数。 |
| 11 | TRUNC()函数 | TRUNC(sysdate) | cast(now() as date) | 获取时间的（2019-07-26 00:00:00）格式返回值。Oracle 中的 TRUNC(sysdate) 只是截取到日，不会截取到时分秒，而 TiDB 中与之对应的截取日写法是 cast(now() as date)。 |
| 12 | TRUNC()函数 | TRUNC(sysdate) | date_format(now(),'%Y-%m-%d') | cast 与 date_format 结果一致。 |
| 13 | TRUNC()函数 | Trunc(sysdate,'mm') | date_add(curdate(),interval -day(curdate())+1 day)  | 获取当月第一天。 |
| 14 | TRUNC 函数 | TRUNC(2.136) => 2 TRUNC(2.136, 2) => 2.14 | TRUNCATE(2.136, 0) => 2 TRUNCATE(2.136, 2) => 2.14 | 数据精度保留，直接截取相应小数位，不涉及四舍五入。 |
| 15 | 字符串连接 | a' \|\| 'b' | CONCAT('a', 'b') | 字符串拼接。 |
| 16 | DELETE关键字 | DELETE   FROM tName t WWHER t.xxx = xxx; | DELETE FROM table_name WHERE xxx = xxx; | 删除语句，TiDB 不支持删除语句中对表起别名。 |
| 17 | 获取序列值 | sequenceName.nextVal | NEXTVAL(sequenceName) | 获取序列的下一个值。 |
| 18 | 左/右关联 | SELECT \* FROM taba, tabb WHERE taba.id = tabb.id(+); SELECT \* FROM taba, tabb WHERE taba.id(+) = tabb.id; | SELECT \* FROM taba LEFT JOIN tabb ON taba.id = tabb.id; SELECT \* FROM taba RIGHT JOIN tabb ON taba.id = tabb.id;       | 关联查询时，TiDB 不支持使用 (+) 实现左/右关联，只能通过 left/right join 实现。 |
| 19 | 获取随机序列值 | SYS_GUID() | UUID() | 返回一个通用唯一识别码 (UUID)。 |
| 20 | nvl()函数 | nvl(key, val) | ifnull(key, val) | 如果该字段值为空，则返回 val 值，否则返回该字段的值。 |
| 21 | nal2()函数 nvl2() | nvl(key, val1, val2) nvl2() | if(key is null, val1, val2) | 如果该字段值非 NULL，则返回 val1 值，否则返回 val2 值。       |
| 22 | decode()函数 | DECODE(key, val1, val2, val3) | if(key = val1, val2, val3) | 如果该字段值对于 val1，则返回 val2，反之返回 val3。 |
| 23 | decode()函数 | DECODE(value, if1, val1, if2,val2,...,ifn, valn, val) | case when value=if1 then val1 when value=if2 then val2,,,when value=ifn then valn else val end | 当该字段值等于条件 1 时，返回 val1，等于条件 2 时，返回 val2… |
| 24 | 获取字符串长度 | length(str) | char_length(str) | 获取字符串长度。 |
| 25 | 截取字符串函数 | substr('abcdefg', 0, 2) => ab substr('abcdefg', 1, 2) => ab | substring('abcdefg', 0, 2) => 空 substring('abcdefg', 1, 2) => ab | 截取字符串，Oracle 中起始位置 0 与 1 作用一样，TiDB 中 0 开始截取为空，若需从头开始截全，则应从 1 开始，TiDB 支持 subString 和 subStr 函数，作用相同，不用修改。但是要注意下标，TiDB 必须从 1 开始。 |
| 26 | 字符查找函数 instr | instr('abcdefg', 'b', 1, 1) | instr('abcdefg', 'b') | 字符查找函数。从字符串 ’abcdefg’ 第 1 个字符开始查询，返回 ‘b‘ 字符串第 1 次出现按的位置。 |
| 27 | 字符查找函数 instr | instr('stst', 's', 1, 2) | LENGTH(SUBSTRING_INDEX('stst','s',2))+1 | 字符查找函数。从字符串 'stst' 第一个字符开始查找，返回 's' 字符第 2 次出现的位置，查找非第一次出现的位置时使用。 |
| 28 | 字符查找函数 | instr(‘abcabc’, 'b', 2, 1) | LOCATE(’b’，'abcabc’,2) | 字符查找函数。从字符串 ’abcabc’ 第 2 个字符开始查询，返回 ‘b‘ 字符串第 1 次出现按的位置。 |
| 29 | 字符串引号识别区别 | 'a' | 'a' / "a" | Oracle 只能识别单引号，TiDB 能识别单引号与双引号。 |
| 30 | null 与空串区别 | 不区分 null 和 '' | 区分 null 和 '' | Oracle 空串就是 null，TiDB 需要把空串转换为 null 数据。TiDB 中 null 和 '' 是有区别的。 |
| 31 | 是否支持插入本表中查询出来的数据 | insert into table1 values（字段1，（select 字段2 from table1 where...）） | insert into table1 values（字段1，（select T.字段2 from table1 T where...） | TiDB 不支持在同一个表中先查这个表再更新该表。 |
| 32 | 获取日期之间间隔月份 | months_between(enddate,sysdate） | TIMESTAMPDIFF (MONTH, sysdate,enddate) |  Months_between 函数返回两个日期之间的月份值，可以用 TIMESTAMPDIFF 替换，但是结果上会有误差，TIMESTAMPDIFF 只保留整数月，应该测试后按照业务看是否替换，另外注意参数位置相反。 |
| 33 | 限制取前 n 条数据 | Rownum <= 10 | limit 10 | 可以使用 limit 等价代替，如：Rownum=1 使用 limit 1 替换，hql 方式运行带 limit 的 SQL 语句会出现错误，需要将 hibernate 的运行方式改为 SQL 方式运行。 |
| 34 | update 语句写法差异 | update test1 set (test1.name,test1.age)= (select test2.name,test2.age from test2 where test2.id=test1.id) | update test1,test2 set test1.name=test2.name,test1.age=test2.age where test1.id=test2.id | TiDB 在多表更新的时候，需要在 set 的时候把具体的字段更新关系都列出来。 |
| 35 | 派生表别名 | select \* from (select \* from test) | select \* from (select \* from test) t | TiDB 多表查询的时候，每一个派生出来的表都必须有一个自己的别名。 |
| 36 | minus 差集运算 | select \* from t1 minus select \* from t2; | select \* from t1 except select \* from t2; | TiDB 不支持 minus，需要改写为 except。 |
| 37 | 空值取别名差异 | select null as xx from dual | select '' as xx from dual | TiDB 数据库下，SQL 中字段直接为 null as 的，在程序中运行会导致报错，需要改成 ''。null 与 '' 在 TiDB 中含义不同。 |
| 38 | 注释差异 |  --注释 |  -- 注释 | Oracle 的 -- 后面不需要空格，TiDB 的 -- 后面则需要有一个空格。 |
| 39 | 列转行函数差异 | listagg(concat(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY  DIMENSIONNAME) | GROUP_CONCAT(concat(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***') | Oracle 中的 listagg 需要改写为 TiDB 的 group_concat 函数；将一列字段合并为一行并根据 *** 符号进行分割。 |
| 40 | 分页查询 | select \* from tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY | select \* from tables limit 2000 offset 0 | 分页查询，offset m 表示跳过 m 行数据，FETCH NEXT n ROWS ONLY 表示取 n 条数据，TiDB 使用 limit n offset m 进行等价改写。 |
| 41 | 获取当前时间 systimestamp | systimestamp | CURRENT_TIMESTAMP(6) | 获取当前时间，时间值带微秒。 |
| 42 | 特殊字符 ASCII 码值 | chr(n) | char(n) | ASCII 值转换函数，可将 ASCII 值转换为对应的字符, Oracle 中制表符 chr(9)/换行符 chr(10)/回车符 chr(13) 对应 TiDB 中的 char(9)/char(10)/char(13)。 |
| 43 | Oracle 和 TiDB 排序 null 的顺序不同 | order by colum asc nulls first | order by colum asc | Oracle 结论：order by colum asc 时，null默认被放在最后；order by colum desc 时，null 默认被放在最前。nulls first 时，强制 null 放在最前，非 null 的仍然按声明顺序 [asc|desc] 进行排序。nulls last 时，强制 null 放在最后，非 null 的仍然按声明顺序 [asc|desc] 进行排序。MySql&TiDB 结论：order by colum asc 时，null默认被放在最前。order by colum desc 时，null 默认被放在最后。`O：select * from t1 order by name nulls first;` 等价于 `T：select * from t1 order by NAME ;` 。`O：select * from t1 order by name desc nulls last;` 等价于 `T：select * from t1 order by name desc;`。 `O：select * from t1 order by name desc nulls first;` 等价于 `T：select * from t1 order by  isnull(name) desc ,name desc;`。`O：select * from t1 order by name asc nulls last;` 等价于 `T：select * from t1 order by  isnull(name) ,name;` |
