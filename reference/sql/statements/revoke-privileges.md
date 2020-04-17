---
title: REVOKE <privileges>
summary: TiDB 数据库中 REVOKE <privileges> 的使用概况。
category: reference
---

# REVOKE <privileges>

`REVOKE <privileges>` 语句用于删除已有用户的权限。

## 语法图

**GrantStmt:**

![GrantStmt](/media/sqlgram/GrantStmt.png)

**PrivElemList:**

![PrivElemList](/media/sqlgram/PrivElemList.png)

**PrivElem:**

![PrivElem](/media/sqlgram/PrivElem.png)

**PrivType:**

![PrivType](/media/sqlgram/PrivType.png)

**ObjectType:**

![ObjectType](/media/sqlgram/ObjectType.png)

**PrivLevel:**

![PrivLevel](/media/sqlgram/PrivLevel.png)

**UserSpecList:**

![UserSpecList](/media/sqlgram/UserSpecList.png)

## 示例

{{< copyable "sql" >}}

```sql
CREATE USER newuser IDENTIFIED BY 'mypassword';
```

```
Query OK, 1 row affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
GRANT ALL ON test.* TO 'newuser';
```

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'newuser';
```

```
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
REVOKE ALL ON test.* FROM 'newuser';
```

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'newuser';
```

```
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DROP USER newuser;
```

```
Query OK, 0 rows affected (0.14 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR newuser;
```

```
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL 兼容性

`REVOKE <privileges>` 语句与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上提交 [issue](/report-issue.md)。

## 另请参阅

* [GRANT <privileges>](/reference/sql/statements/grant-privileges.md)
* [SHOW GRANTS](/reference/sql/statements/show-grants.md)
* [Privilege Management](/reference/security/privilege-system.md)
