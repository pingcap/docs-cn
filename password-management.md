---
title: TiDB Password Management
summary: Learn the mechanism of user password management in TiDB.
---

# TiDB Password Management

To protect the security of user passwords, TiDB supports the following password management policies starting from v6.5.0:

- Password complexity policy: require users to set strong passwords to prevent empty and weak passwords.
- Password expiration policy: require users to change their passwords periodically.
- Password reuse policy: prevent users from reusing old passwords.
- Failed-login tracking and temporary account locking policy: temporarily lock a user account to prevent the same user from trying to log in after multiple login failures caused by wrong passwords.

## TiDB authentication credential storage

To ensure the authenticity of user identity, TiDB uses passwords as credentials to authenticate users when they log in to the TiDB server.

The *password* described in this document refers to the internal credentials generated, stored, and verified by TiDB. TiDB stores user passwords in the `mysql.user` system table.

The following authentication plugins are related to TiDB password management:

- `mysql_native_password`
- `caching_sha2_password`
- `tidb_sm3_password`

For more information about TiDB authentication plugins, see [Authentication plugin status](/security-compatibility-with-mysql.md#authentication-plugin-status).

## Password complexity policy

Password complexity check is disabled by default in TiDB. By configuring system variables related to password complexity, you can enable the password complexity check and make sure the user passwords comply with the password complexity policy.

The password complexity policy has the following features:

- For SQL statements that set user passwords in plaintext (including `CREATE USER`, `ALTER USER`, and `SET PASSWORD`), TiDB checks the passwords against the password complexity policy. If a password does not meet the requirements, the password is rejected.
- You can use the SQL function [`VALIDATE_PASSWORD_STRENGTH()`](https://dev.mysql.com/doc/refman/8.0/en/encryption-functions.html#function_validate-password-strength) to validate the password strength.

> **Note:**
>
> - For the `CREATE USER` statement, even if you can lock the account upon creation, you must set an acceptable password. Otherwise, when the account is unlocked, this account can log in to TiDB using a password that does not comply with the password complexity policy.
> - The modification to the password complexity policy does not affect the passwords that already exist and only affects the newly set passwords.

You can view all system variables related to the password complexity policy by executing the following SQL statement:

```sql
mysql> SHOW VARIABLES LIKE 'validate_password.%';

+--------------------------------------+--------+
| Variable_name                        | Value  |
+--------------------------------------+--------+
| validate_password.check_user_name    | ON     |
| validate_password.dictionary         |        |
| validate_password.enable             | OFF    |
| validate_password.length             | 8      |
| validate_password.mixed_case_count   | 1      |
| validate_password.number_count       | 1      |
| validate_password.policy             | MEDIUM |
| validate_password.special_char_count | 1      |
+--------------------------------------+--------+
8 rows in set (0.00 sec)
```

For a detailed description of each system variable, see [System Variables](/system-variables.md#validate_passwordcheck_user_name-new-in-v650).

### Configure password complexity policy

This section shows examples of configuring system variables related to the password complexity policy.

Enable the password complexity check:

```sql
SET GLOBAL validate_password.enable = ON;
```

Do not allow users to use a password that is the same as the user name:

```sql
SET GLOBAL validate_password.check_user_name = ON;
```

Set the password complexity level to `LOW`:

```sql
SET GLOBAL validate_password.policy = LOW;
```

Set the minimum password length to `10`:

```sql
SET GLOBAL validate_password.length = 10;
```

Require a password to contain at least two numbers, one uppercase letter, one lowercase letter, and one special character:

```sql
SET GLOBAL validate_password.number_count = 2;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.special_char_count = 1;
```

Enable the dictionary check that prevents a password from containing words like `mysql` or `abcd`:

```sql
SET GLOBAL validate_password.dictionary = 'mysql;abcd';
```

> **Note:**
>
> - The value of `validate_password.dictionary` is a string, no longer than 1024 characters. It contains a list of words that must not exist in the password. Each word is separated by semicolon (`;`).
> - The dictionary check is case-insensitive.

### Password complexity check examples

When the system variable `validate_password.enable` is set to `ON`, TiDB enables the password complexity check. The following are examples of the check results:

TiDB checks the user's plaintext password against the default password complexity policy. If the set password does not meet the policy, the password is rejected.

```sql
mysql> ALTER USER 'test'@'localhost' IDENTIFIED BY 'abc';
ERROR 1819 (HY000): Require Password Length: 8
```

TiDB does not check the hashed password against the password complexity policy.

```sql
mysql> ALTER USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password AS '*0D3CED9BEC10A777AEC23CCC353A8C08A633045E';
Query OK, 0 rows affected (0.01 sec)
```

When creating an account initially locked, you must also set a password that matches the password complexity policy, or the creation will fail.

```sql
mysql> CREATE USER 'user02'@'localhost' ACCOUNT LOCK;
ERROR 1819 (HY000): Require Password Length: 8
```

### Password strength validation function

To check the password strength, you can use the `VALIDATE_PASSWORD_STRENGTH()` function. This function accepts a password argument and returns an integer from 0 (weak) to 100 (strong).

> **Note:**
>
> This function evaluates the password strength based on the current password complexity policy. If the password complexity policy is changed, the same password might get different evaluation results.

The following example shows how to use the `VALIDATE_PASSWORD_STRENGTH()` function:

```sql
mysql> SELECT VALIDATE_PASSWORD_STRENGTH('weak');
+------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('weak') |
+------------------------------------+
|                                 25 |
+------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VALIDATE_PASSWORD_STRENGTH('lessweak$_@123');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('lessweak$_@123') |
+----------------------------------------------+
|                                           50 |
+----------------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!') |
+----------------------------------------------+
|                                          100 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

## Password expiration policy

TiDB supports configuring a password expiration policy so that users must change their passwords periodically to improve password security. You can manually make account passwords expire or establish a policy for automatic password expiration.

The automatic password expiration policy can be set at the global level and at the account level. As a database administrator, you can establish an automatic password expiration policy at the global level, and also use an account-level policy to override the global policy.

The privileges for setting the password expiration policy are as follows:

- Database administrator with `SUPER` or `CREATE USER` privileges can manually make passwords expire.
- Database administrator with `SUPER` or `CREATE USER` privileges can set the account-level password expiration policy.
- Database administrator with `SUPER` or `SYSTEM_VARIABLES_ADMINR` privileges can set the global-level password expiration policy.

### Manual expiration

To manually make an account password expire, use the `CREATE USER` or `ALTER USER` statements.

```sql
ALTER USER 'test'@'localhost' PASSWORD EXPIRE;
```

When the account password is set to expire by a database administrator, you must change the password before you can log in to TiDB. The manual expiration cannot be revoked.

For roles created using the `CREATE ROLE` statement, since the role does not require a password, the password field for the role is empty. In such case, TiDB sets the `password_expired` attribute to `'Y'`, which means that the role's password is manually expired. The purpose of this design is to prevent the role from being unlocked and logged into TiDB with an empty password. When the role is unlocked by the `ALTER USER ... ACCOUNT UNLOCK` statement, you can log in with this account even though the password is empty. Therefore, TiDB makes the password manually expired using the `password_expired` attribute so that the user must set a valid password for the account.

```sql
mysql> CREATE ROLE testrole;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT user,password_expired,Account_locked FROM mysql.user WHERE user = 'testrole';
+----------+------------------+----------------+
| user     | password_expired | Account_locked |
+----------+------------------+----------------+
| testrole | Y                | Y              |
+----------+------------------+----------------+
1 row in set (0.02 sec)
```

### Automatic expiration

Automatic password expiration is based on the **password age** and the **password lifetime**.

- Password age: the time interval from the last password change date to the current date. The time of the last password change is recorded in the `mysql.user` system table.
- Password lifetime: the number of days the password can be used to log in to TiDB.

If a password is used for a longer period than it is allowed to live, the server automatically treats the password as expired.

TiDB supports automatic password expiration at the global level and at the account level.

- The global level

    You can set the system variable [`default_password_lifetime`](/system-variables.md#default_password_lifetime-new-in-v650) to control the password lifetime. The default value `0` indicates that the password never expires. If this system variable is set to a positive integer `N`, it means that the password lifetime is `N` days, and you must change your password every `N` days.

    The global automatic password expiration policy applies to all accounts that do not have an account-level override.

    The following example establishes a global automatic password expiration policy with a password lifetime of 180 days:

    ```sql
    SET GLOBAL default_password_lifetime = 180;
    ```

- The account level

    To establish an automatic password expiration policy for an individual account, use the `PASSWORD EXPIRE` option in the `CREATE USER` or `ALTER USER` statement.

    The following examples require that the user password is changed every 90 days:

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
    ```

    The following examples disable the automatic password expiration policy for an individual account:

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
    ```

    Remove the account-level automatic password expiration policy for a specified account so that it follows the global automatic password expiration policy:

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ```

### Password expiration check mechanism

When a client connects to the TiDB server, the server checks whether the password is expired in the following order:

1. The server checks whether the password has been set as expired manually.
2. If the password is not manually expired, the server checks whether the password age is longer than its configured lifetime. If so, the server treats the password as expired.

### Handle an expired password

You can control the behavior of the TiDB server for password expiration. When a password is expired, the server either disconnects the client or restricts the client to the "sandbox mode". In a "sandbox mode", the TiDB server allows connections from the expired account. However, in such connections, the user is only allowed to reset the password.

The TiDB server can control whether to restrict the user with an expired password in the "sandbox mode". To control the behavior of the TiDB server when a password is expired, configure the [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) parameter in the TiDB configuration file:

```toml
[security]
disconnect-on-expired-password = true
```

- If `disconnect-on-expired-password` is set to `true` (default), the server disconnects the client when the password is expired.
- If `disconnect-on-expired-password` is set to `false`, the server enables the "sandbox mode" and allows the user to connect to the server. However, the user can only reset the password. After the password is reset, the user can execute SQL statements normally.

When `disconnect-on-expired-password` is enabled, if an account password is expired, TiDB rejects the connection from the account. In such cases, you can modify the password in the following ways:

- If the password for a normal account is expired, the administrator can change the password for the account by using SQL statements.
- If the password for an administrator account is expired, another administrator can change the password for the account by using SQL statements.
- If the password for an administrator account is expired and no other administrator is available to help change the password, you can use the `skip-grant-table` mechanism to change the password for the account. For details, see [Forgot password process](/user-account-management.md#forget-the-root-password).

## Password reuse policy

TiDB can limit the reuse of previous passwords. The password reuse policy can be based on the number of password changes or time elapsed, or both.

The password reuse policy can be set at the global level and at the account level. You can establish a password reuse policy at the global level, and also use an account-level policy to override the global policy.

TiDB records the password history for an account and limits the selection of a new password from the history:

- If a password reuse policy is based on the number of password changes, a new password must not be the same as any of the specified number of most recent passwords. For example, if the minimum number of password changes is set to `3`, the new password cannot be the same as any of the previous 3 passwords.
- If a password reuse policy is based on time elapsed, a new password must not be the same as any of the passwords used within the specified number of days. For example, if the password reuse interval is set to `60`, the new password cannot be the same as any of the passwords used within the last 60 days.

> **Note:**
>
> Empty passwords are not recorded in the password history and can be reused at any time.

### Global-level password reuse policy

To establish a global password reuse policy, use the [`password_history`](/system-variables.md#password_history-new-in-v650) and [`password_reuse_interval`](/system-variables.md#password_reuse_interval-new-in-v650) system variables.

For example, to establish a global password reuse policy that prohibits the reuse of the last 6 passwords and passwords used within the last 365 days:

```sql
SET GLOBAL password_history = 6;
SET GLOBAL password_reuse_interval = 365;
```

The global password reuse policy applies to all accounts that do not have an account-level override.

### Account-level password reuse policy

To establish an account-level password reuse policy, use the `PASSWORD HISTORY` and `PASSWORD REUSE INTERVAL` options in the `CREATE USER` or `ALTER USER` statement.

For example:

To prohibit the reuse of the last 5 passwords:

```sql
CREATE USER 'test'@'localhost' PASSWORD HISTORY 5;
ALTER USER 'test'@'localhost' PASSWORD HISTORY 5;
```

To prohibit the reuse of passwords used within the last 365 days:

```sql
CREATE USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
```

To combine the two types of reuse policies, use both `PASSWORD HISTORY` and `PASSWORD REUSE INTERVAL`:

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
```

To remove the account-level password reuse policy for a specified account so that it follows the global password reuse policy:

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY DEFAULT
  PASSWORD REUSE INTERVAL DEFAULT;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY DEFAULT
  PASSWORD REUSE INTERVAL DEFAULT;
```

> **Note:**
>
> - If you set the password reuse policy multiple times, the last set value takes effect.
> - The default value of the `PASSWORD HISTORY` and `PASSWORD REUSE INTERVAL` options is 0, which means that the reuse policy is disabled.
> - When you modify a username, TiDB migrates the corresponding password history in the `mysql.password_history` system table from the original username to the new username.

## Failed-login tracking and temporary account locking policy

TiDB can track the number of failed login attempts for an account. To prevent the password from being cracked by brute force, TiDB can lock the account after a specified number of failed login attempts.

> **Note:**
>
> - TiDB only supports failed-login tracking and temporary account locking at the account level, but not at the global level.
> - Failed-login means that the client fails to provide the correct password during the connection attempt, and does not include connection failures due to unknown users or network issues.
> - When you enable the failed-login tracking and temporary account locking for an account, the account is subject to additional checks when the account attempts to log in. This affects the performance of the login operation, especially in high-concurrency login scenarios.

### Configure the login failure tracking policy

You can configure the number of failed login attempts and the lock time for each account by using the `FAILED_LOGIN_ATTEMPTS` and `PASSWORD_LOCK_TIME` options in the `CREATE USER` or `ALTER USER` statement. The available value options are as follows:

- `FAILED_LOGIN_ATTEMPTS`: N. The account is temporarily locked after `N` consecutive login failures. The value of N ranges from 0 to 32767.
- `PASSWORD_LOCK_TIME`: N | UNBOUNDED.
    - N means that the account will be temporarily locked for `N` days after consecutive failed login attempts. The value of N ranges from 0 to 32767.
    - `UNBOUNDED` means that the lock time is unlimited and the account must be manually unlocked. The value of N ranges from 0 to 32767.

> **Note:**
>
> - You can configure only `FAILED_LOGIN_ATTEMPTS` or `PASSWORD_LOCK_TIME` in a single SQL statement. In this case, the account locking does not take effect.
> - The account locking takes effect only when both `FAILED_LOGIN_ATTEMPTS` and `PASSWORD_LOCK_TIME` are not 0.

You can configure the account locking policy as follows:

Create a user and configure the account locking policy. When the password is entered incorrectly for 3 consecutive times, the account will be temporarily locked for 3 days:

```sql
CREATE USER 'test1'@'localhost' IDENTIFIED BY 'password' FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 3;
```

Modify the account locking policy for an existing user. When the password is entered incorrectly for 4 consecutive times, the account will be locked indefinitely until it is manually unlocked:

```sql
ALTER USER 'test2'@'localhost' FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME UNBOUNDED;
```

Disable the account locking policy for an existing user:

```sql
ALTER USER 'test3'@'localhost' FAILED_LOGIN_ATTEMPTS 0 PASSWORD_LOCK_TIME 0;
```

### Unlock the locked account

In the following scenarios, the count of consecutive password errors can be reset:

- When you execute the `ALTER USER ... ACCOUNT UNLOCK` statement.
- When you log in successfully.

In the following scenarios, the locked account can be unlocked:

- When the lock time ends, the automatic lock flag of the account will be reset at the next login attempt.
- When you execute the `ALTER USER ... ACCOUNT UNLOCK` statement.

> **Note:**
>
> When an account is locked due to consecutive login failures, modifying the account locking policy has the following effects:
>
> - When you modify `FAILED_LOGIN_ATTEMPTS`, the lock status of the account does not change. The modified `FAILED_LOGIN_ATTEMPTS` takes effect after the account is unlocked and attempts to log in again.
> - When you modify `PASSWORD_LOCK_TIME`, the lock status of the account does not change. The modified `PASSWORD_LOCK_TIME` takes effect when the account attempts to log in again. At that time, TiDB checks whether the new lock time has reached. If yes, TiDB will unlock the user.
