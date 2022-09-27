---
title: Oracle 与 TiDB 函数对照表
summary: 了解 Oracle 与 TiDB 函数对照表。
---

| 序号 | 语法差异 | Oracle 用法 | TiDB 用法 | 说明 |
|---|---|---|---|---|
| 1 | 数据类型转换函数 | to_number(key) | convert(key, dataType) | 转换表字段值数据类型（TiDB支持BINARY、CHAR、DATE、DATETIME、TIME、SIGNED INTEGER、UNSIGNED   INTEGER、DECIMAL） |
| 2 | 数据类型转换函数 | to_char(key) | convert(key, dataType) | 转换表字段值数据类型（TiDB支持BINARY、CHAR、DATE、DATETIME、TIME、SIGNED INTEGER、UNSIGNED INTEGER、DECIMAL） |
| 3 | 日期转换字符串函数 | to_char(sysdate,'yyyy-MM-dd   hh24:mi:ss')       | date_format(now(),   '%Y-%m-%d %H:%i:%s') | 日期类型转换字符型函数，TiDB年月日时分秒字符大小写必须严格按要求走。（年月日时分秒格式）（将原来的修改为date_formate修改为了修改为date_format） |
| 4 | 日期转换字符串函数 | to_char(sysdate,   'yyyy-MM-dd')       | date_format(now(),   '%Y-%m-%d') | 日期类型转换字符型函数。TiDB年月日时分秒字符大小写必须严格按要求走。（年月日格式）（将原来的修改为date_formate修改为了修改为date_format） |
| 5 | 字符串转换日期函数 | to_date('2021-05-28   17:31:37', 'yyyy-MM-dd hh24:mi:ss') | str_to_date('2021-05-28   17:31:37', '%Y-%m-%d %H:%i:%s') | 字符型转换日期型函数,TiDB年月日时分秒字符大小写必须严格按要求走。 |
| 6 | 字符串转换日期函数 | to_date('2021-05-28',   'yyyy-MM-dd hh24:mi:ss')       | str_to_date('2021-05-28',   '%Y-%m-%d%T') | 字符型转换日期型函数，TiDB年月日时分秒字符大小写必须严格按要求走 |
| 7 | Sysdate   关键字 | SYSDATE | NOW() | 获取系统当前时间 |
| 8 | 获取两个日期相差的天数 | date1   - date2 | datediff(date1,   date2) | 获取date1   - date2 两个日期之间相差的天数(只能精确到天) |
| 9 | 日期数据   +/- n 天 | dateVal   + n | date_add(dateVal,   INTERVAL n DAY) | 日期数据增加n天，n可为负数 |
| 10 | 日期数据   +/- n 月      date_add() 函数替换 add_months() 函数 | add_months(dateVal,   1) | date_add(dateVal,   INTERVAL n MONTH) | 日期数据增加n月，n可为负数 |
| 11 | TRUNC()函数 | TRUNC(sysdate) | cast(now()   as date) | 获取时间的（2019-07-26   00:00:00）格式返回值      （首先oracle中的TRUNC(sysdate)只是截取到日，不会截取到时分秒，而TiDB中与之对应的截取日写法是   cast(now() as date)） |
| 12 | TRUNC()函数 | TRUNC(sysdate) | date_format(now(),'%Y-%m-%d') | cast数据库执行正常，程序中报错，可修改为date_format |
| 13 | TRUNC()函数 | Trunc(sysdate,'mm') | date_add(curdate(),interval   -day(curdate())+1 day)  | 获取当月第一天 |
| 14 | TRUNC   函数 | TRUNC(2.136)   => 2      TRUNC(2.136, 2) => 2.14 | TRUNCATE(2.136,   0) => 2      TRUNCATE(2.136, 2) => 2.14 | 数据精度保留，直接截取相应小数位，不涉及四舍五入 |
| 15 | 字符串连接 | a'   \|\| 'b' | CONCAT('a',   'b') | 字符串拼接 |
| 16 | DELETE关键字 | DELETE   FROM tName t WWHER t.xxx = xxx; | DELETE   FROM table_name  WHERE xxx = xxx; | 删除语句，TIDB不支持删除语句中对表起别名（有问题，tidb支持这种表别名写法） |
| 17 | 获取序列值 | sequenceName.nextVal | NEXTVAL(sequenceName) | 获取序列下一个值 |
| 18 | 左/右关联 | SELECT \* FROM taba, tabb WHERE taba.id = tabb.id(+); SELECT \* FROM taba, tabb WHERE taba.id(+) = tabb.id; | SELECT \* FROM taba LEFT JOIN tabb ON   taba.id = tabb.id; SELECT \* FROM taba RIGHT JOIN tabb ON taba.id = tabb.id;       | 关联查询时，TIDB不支持使用(+)实现左/右关联，只能通过left/right   join 实现（原来例子中写反了左外连接和右外连接的顺序） |
| 19 | 获取随机序列值 | SYS_GUID() | UUID() | 返回一个通用唯一识别码   (UUID) |
| 20 | nvl()函数 | nvl(key,   val) | ifnull(key,   val) | 如果该字段值为空，则返回val值，否则返回该字段的值 |
| 21 | nal2()函数   nvl2() | nvl(key,   val1, val2) nvl2() | if(key   is null, val1, val2) | 如果该字段值非NULL，则返回val1值，否则返回val2值       |
| 22 | decode()函数 | DECODE(key,   val1, val2, val3) | if(key   = val1, val2, val3) | 如果该字段值对于val1，则返回val2，反之返回val3 |
| 23 | decode()函数 | DECODE(value,   if1, val1, if2,val2,...,ifn, valn, val) | case   when value=if1 then val1 when value=if2 then val2,,,when value=ifn then valn   else val end | 当该字段值等于条件1时，返回val1，等于条件2时，返回val2… |
| 24 | 获取字符串长度 | length(str) | char_length(str) | 获取字符串长度 |
| 25 | 截取字符串函数 | substr('abcdefg',   0, 2) => ab      substr('abcdefg', 1, 2) => ab | substring('abcdefg',   0, 2) => 空      substring('abcdefg', 1, 2) => ab | 截取字符串，Oracl中起始位置0与1作用一样，TIDB中0开始截取为空，若需从头开始截全，则应从1开始，TIDB支持subString和subStr函数，作用相同，不用修改，但是要注意开始下标，TIDB必须从1开始 |
| 26 | 字符查找函数instr | instr('abcdefg',   'b', 1, 1) | instr('abcdefg',   'b') | 字符查找函数。从字符串’abcabc’第1个字符开始查询，返回‘b‘字符串第1次出现按的位置。 |
| 27 | 字符查找函数instr | instr('stst',   's', 1, 2) | LENGTH(SUBSTRING_INDEX('stst','s',2))+1 | 字符查找函数。从字符串'stst'第一个字符开始查找，返回's'字符第2次出现的位置，查找非第一次出现的位置时使用。 |
| 28 | 字符查找函数 | instr(‘abcabc’,   'b', 2, 1) | LOCATE(’b’，'abcabc’,2) | 字符查找函数。从字符串’abcabc’第2个字符开始查询，返回‘b‘字符串第1次出现按的位置 |
| 29 | 字符串引号识别区别 |  'a' |  'a' / "a" | ORACLE只能识别单引号，TIDB能识别单引号与双引号 |
| 30 | number数据类型精度问题 | 　 | 　 | 需要注意的数据类型：number   不手动写精度和标度，既可以支持小数也可以支持整型，需要单独判断。      （number可以转成decimal或者bigint） |
| 31 | null   与 空串处理 | 不区分null   和 '' | 区分null   和 '' | Oracle   空串就是 null ，TiDB 需要把空串转换为 null 数据。      （确实是TiDB中 null和''是有区别的） |
| 32 | 是否支持插入本表中查询出来的数据 | insert   into table1 values（字段1，（select 字段2 from table1 where...）） | insert   into table1 values（字段1，（select T.字段2 from table1 T where...） | TiDB不支持在同一个表中先查这个表在更新这个表      （TiDBb不支持这样的语法） |
| 33 | months_between(enddate,sysdate） | months_between(enddate,sysdate） | TIMESTAMPDIFF   (MONTH,  sysdate,enddate) |  Months_between函数返回两个日期之间的月份值，可以用TIMESTAMPDIFF替换，但是结果上会有误差，TIMESTAMPDIFF只保留整数月，应该测试后按照业务看是否替换，另外注意参数位置相反。 |
| 34 | Rowunm | Rownum   <= 10 | limit   10 | 可以使用limit等价代替   如：      Rownum=1 使用limit 1替换,hql方式运行带limit的sql语句会出现错误，需要将hibernate的运行方式改为sql方式运行 |
| 35 | update语句写法差异 | update   test1       set (test1.name,test1.age)=      (select test2.name,test2.age from test2 where test2.id=test1.id) | update   test1,test2       set test1.name=test2.name,test1.age=test2.age      where test1.id=test2.id | tidb在多表更新的时候，需要在set   的时候 把具体的字段更新关系都列出来 |
| 36 | 派生表别名 | select \* from (select \* from test) | select \* from (select \* from test) t | tidb多表查询的时候，每一个派生出来的表都必须有一个自己的别名 |
| 37 | minus差集运算 | select \* from t1 minus select \* from t2; | select \* from t1 except select \* from t2; | tidb不支持minus，需要改写为except |
| 38 | select   null as xx from dual | select   null as xx from dual | select '' as xx from dual | TIDB数据库下，sql中字段直接为null   as的，在程序中运行会导致报错，需要改成''。null与''在tidb中含义不同。 |
| 39 | decimal字段在hibernate中返回类型差异 | 0.00000000   在oracle中返回0 | 0.00000000在oracle中返回科学计数法 | TIDB中小数类型如：0.00000000返回到程序中后还是0.00000000，导致在BIGDECIMAL进行科学计数法后会变成0E-8,而ORACLE则是直接返回为0 |
| 40 | 注释差异 |  --注释 |  -- 注释 | ORACLE--后面不需要空格，TIDB的--后需要有一个空格 |
| 41 | 列转行函数差异 | listagg(concat(E.dimensionid,'---',E.DIMENSIONNAME),'***')   within GROUP(ORDER BY  DIMENSIONNAME) | GROUP_CONCAT(concat(E.dimensionid,'---',E.DIMENSIONNAME)   ORDER BY DIMENSIONNAME SEPARATOR '***') | oracle中的listagg需要改写为TiDB的group_concat函数；将一列字段合并为一行并根据***符号进行分割 |
| 42 | 分页查询 | select \* from tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY | select \* from tables limit 2000 offset 0 | 分页查询，offset   m表示跳过m行数据，FETCH NEXT n ROWS ONLY表示取n条数据，TiDB使用limit n offset m进行等价改写 |
| 43 | 获取当前时间systimestamp | systimestamp | CURRENT_TIMESTAMP(6) | 获取当前时间，时间值带微秒。 |
| 44 | 特殊字符ACSII码值 | chr(n) | char(n) | ACSII值转换函数，可将ACSII值转换为对应的字符,oracle中制表符   chr(9)/换行符 chr(10)/回车符 chr(13)对应tidb中的char(9)/char(10)/char(13) |
| 45 | Oracle和TIDB排序null的顺序不同 | order   by colum asc nulls first | order   by colum asc | 【MySql&TiDB 结论】order by colum asc 时，null默认被放在最前, order by colum desc 时，null默认被放在最后。O：select \* from t1 order by name nulls first; 等价于 T：select \* from t1 order by NAME ; O：select \* from t1 order by name desc nulls last; 等价于 T：select \* from t1 order by name desc; O：select * from t1 order by name desc nulls first; 等价于 T：select \* from t1 order by  isnull(name) desc, name desc; O：select \* from t1 order by name asc nulls last; 等价于 T：select \* from t1 order by  isnull(name) ,name; |
