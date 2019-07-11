---
title: SQL Mode
category: reference
---

# SQL 模式

TiDB 服务器采用不同 SQL 模式来操作，且不同客户端可以应用不同模式。SQL 模式定义 TiDB 支持哪些 SQL 语法及执行哪种数据验证检查.

TiDB 启动之前采用修改 `--sql-mode="modes"` 配项设置 SQL 模式。

TiDB 启动之后采用 `SET [ SESSION | GLOBAL ] sql_mode='modes'`设置 SQL 模式。设置 GLOBAL 级别的 SQL 模式时用户需要有 SUPER 权限，并且只会影响到从设置 SQL 模式开始后续新建立的连接（注：老连接不受影响)。 SESSION 级别的 SQL 模式的变化只会影响当前的客户端。

Modes 是用逗号 (', ') 间隔开的一系列不同的模式。使用 `SELECT @@sql_mode` 语句查询当前 SQL 模式，SQL 模式默认值：""。

## 重要的 sql_mode 值

* ANSI: 符合标准 SQL ，对数据进行校验，如果不符合定义类型或长度，对数据类型调整或截断保存，且返回warning警告。
* STRICT_TRANS_TABLES:  严格模式，对数据进严格校验，但数据出现错误时，插入到表中，并且返回错误。
* TRADITIONAL: 采用此模式使 TiDB 的行为象 "传统" SQL 数据库系统，当在列中插入不正确的值时“给出错误而不是警告”，一旦发现错误立即放弃INSERT/UPDATE。

## SQL mode 列表，如下

| 名称 | 含义 |
| --- | --- |
| PIPES_AS_CONCAT | 将 "\|\|" 视为字符串连接操作符（＋）(同CONCAT())，而不视为OR（支持) |
| ANSI_QUOTES | 将 `"` 视为识别符，如果启用 ANSI_QUOTES，只单引号内的会被认为是 String Literals，双引号被解释为识别符，因此不能用双引号来引用字符串（支持）|
| IGNORE_SPACE | 若开启该模式，系统忽略空格。例如：“user” 和 “user “ 是相同的（支持）|
| ONLY_FULL_GROUP_BY | 如果 GROUP BY 出现的列并没有在 SELECT，HAVING，ORDER BY 中出现，此 SQL 不合法，因为不在 GROUP BY 中的列被查询展示出来不符合正常现象 （支持) |
| NO_UNSIGNED_SUBTRACTION | 在减运算中，如果某个操作数没有符号，不要将结果标记为UNSIGNED （支持）|
| NO_DIR_IN_CREATE | 创建表时，忽视所有 INDEX DIRECTORY 和 DATA DIRECTORY 指令，该选项仅对从复制服务器有用 （仅语法支持）|
| NO_KEY_OPTIONS | 使用 SHOW CREATE TABLE 时不会输出 MySQL 特有的语法部分，如 ENGINE ，使用 mysqldump 跨DB种类迁移的时需要考虑此选项（仅语法支持）|
| NO_FIELD_OPTIONS | 使用 SHOW CREATE TABLE 时不会输出 MySQL 特有的语法部分，如 ENGINE ，使用 mysqldump 跨DB种类迁移的时需要考虑此选项（仅语法支持）|
| NO_TABLE_OPTIONS | 使用 SHOW CREATE TABLE 时不会输出 MySQL 特有的语法部分，如 ENGINE ，使用 mysqldump 跨DB种类迁移的时需要考虑此选项（仅语法支持）|
| NO_AUTO_VALUE_ON_ZERO | 若启用该模式，在AUTO_INCREMENT列的处理传入的值是 0 或者具体数值时系统直接将该值写入此列，传入 NULL 时系统自动生成下一个序列号（支持）|
| NO_BACKSLASH_ESCAPES | 若启用该模式，`\` 反斜杠符号仅代表它自己（支持）|
| STRICT_TRANS_TABLES | 对于事务存储引擎启用严格模式，insert非法值之后，回滚整条语句（支持）|
| STRICT_ALL_TABLES | 对于事务型表，写入非法值之后，回滚整个事务语句（支持）|
| NO_ZERO_IN_DATE | 在严格模式，不接受月或日部分为0的日期。如果使用IGNORE选项，我们为类似的日期插入'0000-00-00'。在非严格模式，可以接受该日期，但会生成警告 （支持）
| NO_ZERO_DATE | 在严格模式，不要将 '0000-00-00'做为合法日期。你仍然可以用IGNORE选项插入零日期。在非严格模式，可以接受该日期，但会生成警告 （支持）|
| ALLOW_INVALID_DATES | 不检查全部日期的合法性，仅检查月份值在 1 到 12 及 日期值在 1 到31 之间，仅适用于 DATE 和 DATATIME 列，TIMESTAMP 列需要全部检查其合法性 （支持）|
| ERROR_FOR_DIVISION_BY_ZERO | 若启用该模式，在 INSERT 或 UPDATE 过程中，被除数为 0 值时，系统产生错误 <br> 若未启用该模式，被除数为 0 值时，系统产生警告，并用 NULL 代替 （支持） |
| NO_AUTO_CREATE_USER | 防止GRANT自动创建新用户，但指定密码除外 （支持）|
| HIGH_NOT_PRECEDENCE | NOT 操作符的优先级是表达式。例如： NOT a BETWEEN b AND c 被解释为 NOT (a BETWEEN b AND c)。在部份旧版本MySQL中， 表达式被解释为(NOT a) BETWEEN b AND c (支持) |
| NO_ENGINE_SUBSTITUTION | 如果需要的存储引擎被禁用或未编译，可以防止自动替换存储引擎 （仅语法支持）|
| PAD_CHAR_TO_FULL_LENGTH | 若启用该模式，系统对于 CHAR 类型不会截断尾部空格（支持）|
| REAL_AS_FLOAT | 将REAL视为FLOAT的同义词，而不是DOUBLE的同义词 （支持）|
| POSTGRESQL | 等同于 PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE、NO_KEY_OPTIONS、NO_TABLE_OPTIONS、NO_FIELD_OPTIONS （支持）|
| MSSQL | 等同于 PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE、NO_KEY_OPTIONS、NO_TABLE_OPTIONS、 NO_FIELD_OPTIONS （支持）|
| DB2 | 等同于 PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE、NO_KEY_OPTIONS、NO_TABLE_OPTIONS、NO_FIELD_OPTIONS （支持）|
| MAXDB | 等同于 PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE、NO_KEY_OPTIONS、NO_TABLE_OPTIONS、NO_FIELD_OPTIONS、NO_AUTO_CREATE_USER （支持）|
| MySQL323 | 等同于 NO_FIELD_OPTIONS、HIGH_NOT_PRECEDENCE (支持)|
| MYSQL40 | 等同于 NO_FIELD_OPTIONS、HIGH_NOT_PRECEDENCE （支持）|
| ANSI | 等同于 REAL_AS_FLOAT、PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE （支持）|
| TRADITIONAL | 等同于 STRICT_TRANS_TABLES、STRICT_ALL_TABLES、NO_ZERO_IN_DATE、NO_ZERO_DATE、ERROR_FOR_DIVISION_BY_ZERO、NO_AUTO_CREATE_USER(支持) |
| ORACLE | 等同于 PIPES_AS_CONCAT、ANSI_QUOTES、IGNORE_SPACE、NO_KEY_OPTIONS、NO_TABLE_OPTIONS、NO_FIELD_OPTIONS、NO_AUTO_CREATE_USER （支持）|
