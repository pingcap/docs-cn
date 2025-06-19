---
title: REFERENTIAL_CONSTRAINTS
summary: 了解 `REFERENTIAL_CONSTRAINTS` INFORMATION_SCHEMA 表。
---

# REFERENTIAL_CONSTRAINTS

`REFERENTIAL_CONSTRAINTS` 表提供了表之间的 [`FOREIGN KEY`](/foreign-key.md)（外键）关系信息。

```sql
USE INFORMATION_SCHEMA;
DESC REFERENTIAL_CONSTRAINTS;
```

输出结果如下：

```sql
+---------------------------+--------------+------+------+---------+-------+
| Field                     | Type         | Null | Key  | Default | Extra |
+---------------------------+--------------+------+------+---------+-------+
| CONSTRAINT_CATALOG        | varchar(512) | NO   |      | NULL    |       |
| CONSTRAINT_SCHEMA         | varchar(64)  | NO   |      | NULL    |       |
| CONSTRAINT_NAME           | varchar(64)  | NO   |      | NULL    |       |
| UNIQUE_CONSTRAINT_CATALOG | varchar(512) | NO   |      | NULL    |       |
| UNIQUE_CONSTRAINT_SCHEMA  | varchar(64)  | NO   |      | NULL    |       |
| UNIQUE_CONSTRAINT_NAME    | varchar(64)  | YES  |      | NULL    |       |
| MATCH_OPTION              | varchar(64)  | NO   |      | NULL    |       |
| UPDATE_RULE              | varchar(64)  | NO   |      | NULL    |       |
| DELETE_RULE              | varchar(64)  | NO   |      | NULL    |       |
| TABLE_NAME                | varchar(64)  | NO   |      | NULL    |       |
| REFERENCED_TABLE_NAME     | varchar(64)  | NO   |      | NULL    |       |
+---------------------------+--------------+------+------+---------+-------+
11 rows in set (0.00 sec)
```

```sql
CREATE TABLE test.parent (
  id INT NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (id)
);

CREATE TABLE test.child (
  id INT NOT NULL AUTO_INCREMENT,
  name varchar(255) NOT NULL,
  parent_id INT DEFAULT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES parent (id) ON UPDATE CASCADE ON DELETE RESTRICT
);

SELECT * FROM REFERENTIAL_CONSTRAINTS\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
       CONSTRAINT_CATALOG: def
        CONSTRAINT_SCHEMA: test
          CONSTRAINT_NAME: fk_parent
UNIQUE_CONSTRAINT_CATALOG: def
 UNIQUE_CONSTRAINT_SCHEMA: test
   UNIQUE_CONSTRAINT_NAME: PRIMARY
             MATCH_OPTION: NONE
              UPDATE_RULE: CASCADE
              DELETE_RULE: RESTRICT
               TABLE_NAME: child
    REFERENCED_TABLE_NAME: parent
1 row in set (0.00 sec)
```
