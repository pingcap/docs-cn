---
title: 关键字和保留字
category: reference
aliases: ['/docs-cn/sql/keywords-and-reserved-words/']
---

# 关键字和保留字

关键字在 SQL 中有特殊的意义， 例如 `SELECT`，`UPDATE`，`DELETE`，在作为表名跟函数名的时候，需要特殊对待，例如作为表名，保留字需要被反引号包住：

```sql
mysql> CREATE TABLE select (a INT);
ERROR 1105 (HY000): line 0 column 19 near " (a INT)" (total length 27)
mysql> CREATE TABLE `select` (a INT);
Query OK, 0 rows affected (0.09 sec)
```

`BEGIN` 和 `END` 是关键字， 但不是保留字，所以不需要反引号：

```sql
mysql> CREATE TABLE `select` (BEGIN int, END int);
Query OK, 0 rows affected (0.09 sec)
```

有一种特殊情况， 如果使用了限定符 `.`，那么也不需要用反引号：

```sql
mysql> CREATE TABLE test.select (BEGIN int, END int);
Query OK, 0 rows affected (0.08 sec)
```

下表列出了在 TiDB 中的关键字跟保留字，保留字用 (R) 来标识：

| ACTION                  | ADD (R)            | ADDDATE                |
|:------------------------|:-------------------|:-----------------------|
| ADMIN                   | AFTER              | ALL (R)                |
| ALTER (R)               | ALWAYS             | ANALYZE(R)             |
| AND (R)                 | ANY                | AS (R)                 |
| ASC (R)                 | ASCII              | AUTO_INCREMENT         |
| AVG                     | AVG_ROW_LENGTH     | BEGIN                  |
| BETWEEN (R)             | BIGINT (R)         | BINARY (R)             |
| BINLOG                  | BIT                | BIT_XOR                |
| BLOB (R)                | BOOL               | BOOLEAN                |
| BOTH (R)                | BTREE              | BY (R)                 |
| BYTE                    | CASCADE (R)        | CASE (R)               |
| CAST                    | CHANGE (R)         | CHAR (R)               |
| CHARACTER (R)           | CHARSET            | CHECK (R)              |
| CHECKSUM                | COALESCE           | COLLATE (R)            |
| COLLATION               | COLUMN (R)         | COLUMNS                |
| COMMENT                 | COMMIT             | COMMITTED              |
| COMPACT                 | COMPRESSED         | COMPRESSION            |
| CONNECTION              | CONSISTENT         | CONSTRAINT (R)         |
| CONVERT (R)             | COUNT              | CREATE (R)             |
| CROSS (R)               | CURRENT_DATE (R)   | CURRENT_TIME (R)       |
| CURRENT_TIMESTAMP (R)   | CURRENT_USER (R)   | CURTIME                |
| DATA                    | DATABASE (R)       | DATABASES (R)          |
| DATE                    | DATE_ADD           | DATE_SUB               |
| DATETIME                | DAY                | DAY_HOUR (R)           |
| DAY_MICROSECOND (R)     | DAY_MINUTE (R)     | DAY_SECOND (R)         |
| DDL                     | DEALLOCATE         | DEC                    |
| DECIMAL (R)             | DEFAULT (R)        | DELAY_KEY_WRITE        |
| DELAYED (R)             | DELETE (R)         | DESC (R)               |
| DESCRIBE (R)            | DISABLE            | DISTINCT (R)           |
| DISTINCTROW (R)         | DIV (R)            | DO                     |
| DOUBLE (R)              | DROP (R)           | DUAL (R)               |
| DUPLICATE               | DYNAMIC            | ELSE (R)               |
| ENABLE                  | ENCLOSED           | END                    |
| ENGINE                  | ENGINES            | ENUM                   |
| ESCAPE                  | ESCAPED            | EVENTS                 |
| EXCLUSIVE               | EXECUTE            | EXISTS                 |
| EXPLAIN (R)             | EXTRACT            | FALSE (R)              |
| FIELDS                  | FIRST              | FIXED                  |
| FLOAT (R)               | FLUSH              | FOR (R)                |
| FORCE (R)               | FOREIGN (R)        | FORMAT                 |
| FROM (R)                | FULL               | FULLTEXT (R)           |
| FUNCTION                | GENERATED (R)      | GET_FORMAT             |
| GLOBAL                  | GRANT (R)          | GRANTS                 |
| GROUP (R)               | GROUP_CONCAT       | HASH                   |
| HAVING (R)              | HIGH_PRIORITY (R)  | HOUR                   |
| HOUR_MICROSECOND (R)    | HOUR_MINUTE (R)    | HOUR_SECOND (R)        |
| IDENTIFIED              | IF (R)             | IGNORE (R)             |
| IN (R)                  | INDEX (R)          | INDEXES                |
| INFILE (R)              | INNER (R)          | INSERT (R)             |
| INT (R)                 | INTEGER (R)        | INTERVAL (R)           |
| INTO (R)                | IS (R)             | ISOLATION              |
| JOBS                    | JOIN (R)           | JSON                   |
| KEY (R)                 | KEY_BLOCK_SIZE     | KEYS (R)               |
| KILL (R)                | LEADING (R)        | LEFT (R)               |
| LESS                    | LEVEL              | LIKE (R)               |
| LIMIT (R)               | LINES (R)          | LOAD (R)               |
| LOCAL                   | LOCALTIME (R)      | LOCALTIMESTAMP (R)     |
| LOCK (R)                | LONGBLOB (R)       | LONGTEXT (R)           |
| LOW_PRIORITY (R)        | MAX                | MAX_ROWS               |
| MAXVALUE (R)            | MEDIUMBLOB (R)     | MEDIUMINT (R)          |
| MEDIUMTEXT (R)          | MICROSECOND        | MIN                    |
| MIN_ROWS                | MINUTE             | MINUTE_MICROSECOND (R) |
| MINUTE_SECOND (R)       | MIN                | MIN_ROWS               |
| MINUTE                  | MINUTE_MICROSECOND | MINUTE_SECOND          |
| MOD (R)                 | MODE               | MODIRY                 |
| MONTH                   | NAMES              | NATIONAL               |
| NATURAL (R)             | NO                 | NO_WRITE_TO_BINLOG (R) |
| NONE                    | NOT (R)            | NOW                    |
| NULL (R)                | NUMERIC (R)        | NVARCHAR (R)           |
| OFFSET                  | ON (R)             | ONLY                   |
| OPTION (R)              | OR (R)             | ORDER (R)              |
| OUTER (R)               | PARTITION (R)      | PARTITIONS             |
| PASSWORD                | PLUGINS            | POSITION               |
| PRECISION (R)           | PREPARE            | PRIMARY (R)            |
| PRIVILEGES              | PROCEDURE (R)      | PROCESS                |
| PROCESSLIST             | QUARTER            | QUERY                  |
| QUICK                   | RANGE (R)          | READ (R)               |
| REAL (R)                | REDUNDANT          | REFERENCES (R)         |
| REGEXP (R)              | RENAME (R)         | REPEAT (R)             |
| REPEATABLE              | REPLACE (R)        | RESTRICT (R)           |
| REVERSE                 | REVOKE (R)         | RIGHT (R)              |
| RLIKE (R)               | ROLLBACK           | ROW                    |
| ROW_COUNT               | ROW_FORMAT         | SCHEMA                 |
| SCHEMAS                 | SECOND             | SECOND_MICROSECOND (R) |
| SELECT (R)              | SERIALIZABLE       | SESSION                |
| SET (R)                 | SHARE              | SHARED                 |
| SHOW (R)                | SIGNED             | SMALLINT (R)           |
| SNAPSHOT                | SOME               | SQL_CACHE              |
| SQL_CALC_FOUND_ROWS (R) | SQL_NO_CACHE       | START                  |
| STARTING (R)            | STATS              | STATS_BUCKETS          |
| STATS_HISTOGRAMS        | STATS_META         | STATS_PERSISTENT       |
| STATUS                  | STORED (R)         | SUBDATE                |
| SUBSTR                  | SUBSTRING          | SUM                    |
| SUPER                   | TABLE (R)          | TABLES                 |
| TERMINATED (R)          | TEXT               | THAN                   |
| THEN (R)                | TIDB               | TIDB_INLJ              |
| TIDB_SMJ                | TIME               | TIMESTAMP              |
| TIMESTAMPADD            | TIMESTAMPDIFF      | TINYBLOB (R)           |
| TINYINT (R)             | TINYTEXT (R)       | TO (R)                 |
| TRAILING (R)            | TRANSACTION        | TRIGGER (R)            |
| TRIGGERS                | TRIM               | TRUE (R)               |
| TRUNCATE                | UNCOMMITTED        | UNION (R)              |
| UNIQUE (R)              | UNKNOWN            | UNLOCK (R)             |
| UNSIGNED (R)            | UPDATE (R)         | USE (R)                |
| USER                    | USING (R)          | UTC_DATE (R)           |
| UTC_TIME (R)            | UTC_TIMESTAMP (R)  | VALUE                  |
| VALUES (R)              | VARBINARY (R)      | VARCHAR (R)            |
| VARIABLES               | VIEW               | VIRTUAL (R)            |
| WARNINGS                | WEEK               | WHEN (R)               |
| WHERE (R)               | WITH (R)           | WRITE (R)              |
| XOR (R)                 | YEAR               | YEAR_MONTH (R) |       |
| ZEROFILL (R)            |                    |                        |
