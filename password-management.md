---
title: TiDB 密码管理
summary: 了解 TiDB 的用户密码管理机制。
---

# TiDB 密码管理

为了保护用户密码的安全，从 TiDB v6.5.0 开始支持密码管理能力：

- 密码复杂度策略：要求用户设置强密码，以防止出现空密码、弱密码。
- 密码过期策略：要求用户定期修改密码。
- 密码重用策略：限制用户重复使用旧密码。
- 密码连续错误限制登录策略：连续多次密码错误导致登录失败后，临时锁定用户，限制该用户继续尝试登录。

## TiDB 身份验证凭据存储

密码作为一种用户身份凭据，在用户登录到服务端时用于身份验证，确保用户身份的合法性。本文中描述的密码是指由 TiDB 生成、存储、验证的内部凭据，TiDB 将用户密码被存储到 `mysql.user` 系统表中，以下身份验证插件涉及本文的密码管理功能：

- `mysql_native_password`
- `caching_sha2_password`
- `tidb_sm3_password`

有关 TiDB 支持身份验证插件的更多信息，请查看[`可用的身份验证插件`](/security-compatibility-with-mysql.md#可用的身份验证插件)。

## 密码复杂度策略

在 TiDB 中，密码复杂度检查默认未开启。通过配置密码复杂度相关的系统变量，你可以开启密码复杂度检查，并确保为账户设置的密码符合密码复杂度策略。

密码复杂度策略支持以下功能：

- 对采用明文方式设置用户密码的 SQL 语句（包括 `CREATE USER`、`ALTER USER`、`SET PASSWORD` ），系统会根据密码复杂度策略检查该密码，如果该密码不符合要求，则拒绝该密码。
- 可以使用 SQL 函数 [`VALIDATE_PASSWORD_STRENGTH()`](/functions-and-operators/encryption-and-compression-functions.md#validate_password_strength) 评估给定密码的强度。

> **注意：**
>
> - 对于 `CREATE USER` 语句，即使该账户最初被锁定，也必须提供满足密码复杂度策略的密码，否则将账户解锁后，该账户可以使用不符合密码复杂度策略的密码访问 TiDB。
> - 对密码复杂度策略的变更不影响已存在的密码，只会对新设置的密码产生影响。

通过以下 SQL 语句，你可以查看所有密码复杂度策略相关的系统变量：

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

关于这些变量的详细解释，请查阅[系统变量文档](/system-variables.md#validate_passwordcheck_user_name-从-v650-版本开始引入)。

### 配置密码复杂度策略

密码复杂度策略相关的系统变量的配置方式如下：

开启密码复杂度策略检查：

```sql
SET GLOBAL validate_password.enable = ON;
```

设置不允许密码与当前用户名相同：

```sql
SET GLOBAL validate_password.check_user_name = ON;
```

设置密码复杂度的检查等级为 `LOW`：

```sql
SET GLOBAL validate_password.policy = LOW;
```

设置密码最小长度为 10：

```sql
SET GLOBAL validate_password.length = 10;
```

设置密码中至少含有 2 个数字，至少含有 1 个大写和小写字符，至少含有 1 个特殊字符：

```sql
SET GLOBAL validate_password.number_count = 2;
SET GLOBAL validate_password.mixed_case_count = 1;
SET GLOBAL validate_password.special_char_count = 1;
```

设置密码字典功能，要求密码中不允许包含 `mysql` 或 `abcd`：

```sql
SET GLOBAL validate_password.dictionary = 'mysql;abcd';
```

> **注意：**
>
> - `validate_password.dictionary` 是一个长字符串，长度不超过 1024，字符串内容可包含一个或多个在密码中不允许出现的单词，每个单词之间采用英文分号（`;`）分隔。
> - 密码字典功能进行单词比较时，不区字符分大小写。

### 密码复杂度检查示例

配置系统变量 `validate_password.enable = ON` 后，TiDB 将开启密码复杂度检查。以下为一些典型的检查示例：

按照默认密码复杂度策略，检测用户明文密码，若设置的密码不符合复杂度策略要求，则设置失败。

```sql
ALTER USER 'test'@'localhost' IDENTIFIED BY 'abc';
ERROR 1819 (HY000): Require Password Length: 8
```

TiDB 进行密码复杂度检查时，不检查散列后的密码。

```sql
ALTER USER 'test'@'localhost' IDENTIFIED WITH mysql_native_password AS '*0D3CED9BEC10A777AEC23CCC353A8C08A633045E';
Query OK, 0 rows affected (0.01 sec)
```

创建一个最初被锁定的账户时，也必须设置符合密码复杂度策略的密码，否则创建失败。

```sql
CREATE USER 'user02'@'localhost' ACCOUNT LOCK;
ERROR 1819 (HY000): Require Password Length: 8
```

### 密码强度评估函数

使用 [`VALIDATE_PASSWORD_STRENGTH()`](/functions-and-operators/encryption-and-compression-functions.md#validate_password_strength) 函数评估给定密码的强度，该函数接受一个密码参数，并返回一个从 0（弱）到 100（强）的整数。

> **注意：**
>
> 密码强度是基于当前已配置的密码复杂度策略进行评估的，密码复杂度配置改变后，同一个密码的评估结果可能与之前不同。

[`VALIDATE_PASSWORD_STRENGTH()`](/functions-and-operators/encryption-and-compression-functions.md#validate_password_strength) 函数使用示例如下：

```sql
SELECT VALIDATE_PASSWORD_STRENGTH('weak');
+------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('weak') |
+------------------------------------+
|                                 25 |
+------------------------------------+
1 row in set (0.01 sec)

SELECT VALIDATE_PASSWORD_STRENGTH('lessweak$_@123');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('lessweak$_@123') |
+----------------------------------------------+
|                                           50 |
+----------------------------------------------+
1 row in set (0.01 sec)

SELECT VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!');
+----------------------------------------------+
| VALIDATE_PASSWORD_STRENGTH('N0Tweak$_@123!') |
+----------------------------------------------+
|                                          100 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

## 密码过期策略

TiDB 支持通过设置密码过期策略，要求用户定期修改密码，从而提高密码的安全性。可以手动将指定账户的密码设置为过期，也可以建立密码自动过期策略。自动过期策略分为全局级别和账户级别，管理员可以在全局级别建立密码过期策略，也可以使用账户级别密码过期策略覆盖全局级别策略。设置密码过期策略的权限要求如下：

- 具有 `SUPER` 或者 `CREATE USER` 权限的数据库管理员可以手动设置密码过期。
- 具有 `SUPER` 或者 `CREATE USER` 权限的数据库管理员可以设置账户级别自动密码过期策略。
- 具有 `SUPER` 或者 `SYSTEM_VARIABLES_ADMIN` 权限的数据库管理员可以设置全局级别自动密码过期策略。

### 手动密码过期

要手动设置账户密码过期，请使用 `CREATE USER` 或 `ALTER USER` 语句。

```sql
ALTER USER 'test'@'localhost' PASSWORD EXPIRE;
```

当账户密码被管理员手动设置过期后，必须修改该账户密码才能解除密码过期，不支持取消手动过期。

对于通过 `CREATE ROLE` 语句创建的角色，由于角色不需要设置密码，所以该角色对应的密码字段为空，此时对应的 `password_expired` 属性为 `'Y'`，即该角色的密码处于手动过期状态。如此设计的目的是防止出现角色锁定状态被解除后，该角色以空密码登录到 TiDB，当该角色被 `ALTER USER ... ACCOUNT UNLOCK` 命令解锁后，此时该角色处于可登录的状态，但是密码为空；因此 TiDB 通过 `password_expired` 属性，使得角色的密码处于手动过期状态，从而强制要求为该角色设置一个有效的密码。

```sql
CREATE ROLE testrole;
Query OK, 0 rows affected (0.01 sec)

SELECT user,password_expired,Account_locked FROM mysql.user WHERE user = 'testrole';
+----------+------------------+----------------+
| user     | password_expired | Account_locked |
+----------+------------------+----------------+
| testrole | Y                | Y              |
+----------+------------------+----------------+
1 row in set (0.02 sec)
```

### 自动密码过期

自动密码过期是基于**密码使用期限**和**密码被允许的生存期**来判断的。

- 密码使用期限：从最近一次密码更改日期到当前日期的时间间隔。系统表 `mysql.user` 中会记录最近一次修改密码的时间。
- 密码被允许的生存期：一个密码被设置后，其可以正常用于登录 TiDB 的天数。

如果密码使用期限大于其被允许的生存期，服务器会自动将密码视为已过期。

TiDB 支持在全局级别和账户级别设置自动密码过期：

- 全局级别自动密码过期

    你可以设置系统变量 [`default_password_lifetime`](/system-variables.md#default_password_lifetime-从-v650-版本开始引入) 来控制密码生存期。该变量默认值为 0，表示禁用自动密码过期。如果设置该变量的值为正整数 N，则表示允许的密码生存期为 N 天，即必须在 N 天之内更改密码。

    全局自动密码过期策略适用于所有未设置账户级别覆盖的账户。

    以下示例建立全局自动密码过期策略，密码有效期为 180 天：

    ```sql
    SET GLOBAL default_password_lifetime = 180;
    ```

- 账户级别自动密码过期

    要为个人账户建立自动密码过期策略，请使用 `CREATE USER` 或 `ALTER USER` 语句的 `PASSWORD EXPIRE` 选项。

    以下示例要求用户密码每 90 天更改一次：

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE INTERVAL 90 DAY;
    ```

    在账户级别禁用自动密码过期策略：

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE NEVER;
    ```

    移除指定账户的账户级别自动密码过期策略，使其遵循于全局自动密码过期策略：

    ```sql
    CREATE USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ALTER USER 'test'@'localhost' PASSWORD EXPIRE DEFAULT;
    ```

### 密码过期策略检查机制

当客户端连接成功后，服务端将按顺序进行以下检查，判断账号密码是否过期：

1. 服务器检查密码是否已手动过期。
2. 若密码没有手动过期，服务器根据自动密码过期策略检查密码使用期限是否大于其允许的生存期。如果是，服务器认为密码已过期。

### 密码过期处理机制

TiDB 支持密码过期策略控制。当密码过期后，服务器要么断开客户端的连接，要么将客户端限制为“沙盒模式”。“沙盒模式”下，TiDB 服务端接受密码过期账户的连接，但是连接成功后只允许该用户执行重置密码的操作。

TiDB 服务端可以控制是否将密码已过期用户的连接限制为“沙盒模式”。你可以在 TiDB 配置文件中的 `[security]` 部分，配置 [`disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-从-v650-版本开始引入) 选项：

```toml
[security]
disconnect-on-expired-password = true
```

- 默认情况下，`disconnect-on-expired-password` 为 `true`，表示当密码过期后，服务器将直接断开客户端的连接。
- 如果配置 `disconnect-on-expired-password` 为 `false`，则服务端处于沙盒模式，服务端允许用户建立连接，但只能执行密码重置操作，密码重置后将允许用户正常执行各类 SQL 语句。

当 `disconnect-on-expired-password` 为 `true` 时，TiDB 将拒绝密码已过期用户的连接，此时可以通过如下方法修改密码：

- 普通用户密码过期，可以由管理员用户通过 SQL 语句修改该用户的密码。
- 管理员密码过期，可以由其他管理员用户通过 SQL 语句修改该用户的密码。
- 如果管理员密码过期，且无法寻求其他管理员帮助修改该用户的密码，此时可以采用 `skip-grant-table` 机制修改该用户密码，具体可参看[忘记密码流程](/user-account-management.md#忘记-root-密码)。

## 密码重用策略

TiDB 支持限制重复使用以前的密码。密码重用策略可以基于密码更改的次数或经过的时间，也可以同时基于两者。密码重用策略分为全局级别和账户级别。你可以在全局级别建立密码重用策略，也可以使用账户级别密码重用策略覆盖全局策略。

TiDB 会记录账户的历史密码，并限制从该历史记录中选择新密码：

- 如果密码重用策略基于密码更改次数，则新密码不得与指定数量的历史密码相同。例如，如果密码的最小更改次数设置为 3，则新密码不能与最近 3 个密码中的任何一个相同。
- 如果密码重用策略基于经过的时间，则新密码不得与历史记录中指定天数内使用过的密码相同。例如，如果密码重用间隔设置为 60，则新密码不能与最近 60 天内使用过的密码相同。

> **注意：**
>
> 空密码不计入密码历史记录，可以随时重复使用。

### 全局级别密码重用策略

要在全局范围内建立密码重用策略，请使用 [`password_history`](/system-variables.md#password_history-从-v650-版本开始引入) 和 [`password_reuse_interval`](/system-variables.md#password_reuse_interval-从-v650-版本开始引入) 系统变量。

例如，建立全局密码重用策略，禁止重复使用最近 6 个密码或最近 365 天的密码：

```sql
SET GLOBAL password_history = 6;
SET GLOBAL password_reuse_interval = 365;
```

全局密码重用策略适用于所有未在账户级别设置过密码重用策略的账户。

### 账户级别密码重用策略

要建立账户级别密码重用策略，请使用 `CREATE USER` 或 `ALTER USER` 语句的 `PASSWORD HISTORY` 和 `PASSWORD REUSE INTERVAL` 选项。

示例：

禁止重复使用最近 5 次使用过的密码：

```sql
CREATE USER 'test'@'localhost' PASSWORD HISTORY 5;
ALTER USER 'test'@'localhost' PASSWORD HISTORY 5;
```

禁止重复使用最近 365 天内使用过的密码：

```sql
CREATE USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost' PASSWORD REUSE INTERVAL 365 DAY;
```

如需组合两种类型的重用策略，请一起使用 `PASSWORD HISTORY` 和 `PASSWORD REUSE INTERVAL`：

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY 5
  PASSWORD REUSE INTERVAL 365 DAY;
```

移除指定账户的账户级别密码重用策略，使其遵循于全局密码重用策略：

```sql
CREATE USER 'test'@'localhost'
  PASSWORD HISTORY DEFAULT
  PASSWORD REUSE INTERVAL DEFAULT;
ALTER USER 'test'@'localhost'
  PASSWORD HISTORY DEFAULT
  PASSWORD REUSE INTERVAL DEFAULT;
```

> **注意：**
>
> - 如果多次设置密码重用策略，则最后一次设置的值生效。
> - `PASSWORD HISTORY` 和 `PASSWORD REUSE INTERVAL` 选项的默认值为 0，表示禁用该项重用策略。
> - 在修改用户名时，TiDB 会将 `mysql.password_history` 系统表中原用户名的历史密码记录迁移到新用户名的记录中。

## 密码连续错误限制登录策略

TiDB 支持限制账户持续尝试登录，防止用户密码被暴力破解。当账户连续登录失败次数过多时，账户将被临时锁定。

> **注意：**
>
> - 只支持账户级别的密码连续错误限制登录策略，不支持全局级别的策略。
> - 登录失败是指客户端在连接尝试期间未能提供正确的密码，不包括由于未知用户或网络问题等原因而导致的连接失败。
> - 对用户启用密码连续错误限制登录策略后，将增加该用户登录时的检查步骤，此时会影响该用户登录相关操作的性能，尤其是高并发登录场景。

### 配置密码连续错误限制登录策略

每个账户的登录失败次数和锁定时间是可配置的，你可以使用 `CREATE USER`、`ALTER USER` 语句的 `FAILED_LOGIN_ATTEMPTS` 和 `PASSWORD_LOCK_TIME` 选项。`FAILED_LOGIN_ATTEMPTS` 和 `PASSWORD_LOCK_TIME` 选项的可设置值如下：

- `FAILED_LOGIN_ATTEMPTS`：N。表示连续登录失败 N 次后，账户将被临时锁定。N 取值范围为 0 到 32767。
- `PASSWORD_LOCK_TIME`：N | UNBOUNDED。N 表示登录失败后，账户将被临时锁定 N 天。UNBOUNDED 表明锁定时间无限期，账户必须被手动解锁。N 取值范围为 0 到 32767。

> **注意：**
>
> - 允许单条 SQL 语句只设置 `FAILED_LOGIN_ATTEMPTS` 或 `PASSWORD_LOCK_TIME` 中的一个选项，这时密码连续错误限制登录策略不会实质生效。
> - 只有当账户的 `FAILED_LOGIN_ATTEMPTS` 和 `PASSWORD_LOCK_TIME` 都不为 0 时，系统才会跟踪该账户的失败登录次数并执行临时锁定。

配置密码连续错误限制登录策略的示例如下：

新建一个用户，并配置密码连续错误限制登录策略，当该用户密码连续错误 3 次时，临时锁定 3 天：

```sql
CREATE USER 'test1'@'localhost' IDENTIFIED BY 'password' FAILED_LOGIN_ATTEMPTS 3 PASSWORD_LOCK_TIME 3;
```

修改用户的密码连续错误限制登录策略，当该用户密码连续错误 4 次时，无限期锁定，直到账户被手动解锁：

```sql
ALTER USER 'test2'@'localhost' FAILED_LOGIN_ATTEMPTS 4 PASSWORD_LOCK_TIME UNBOUNDED;
```

关闭用户的密码连续错误限制登录策略：

```sql
ALTER USER 'test3'@'localhost' FAILED_LOGIN_ATTEMPTS 0 PASSWORD_LOCK_TIME 0;
```

### 锁定账户解锁

在以下场景中，TiDB 将重置用户密码连续错误次数的计数：

- 对该用户执行 `ALTER USER ... ACCOUNT UNLOCK` 解锁命令时。
- 该用户登录成功时。

当用户因密码连续多次错误触发账户锁定后，以下情况下可以解锁账户：

- 该用户锁定时间结束，这种情况下，用户的自动锁定标识将在下次登录尝试时重置。
- 对该用户执行 `ALTER USER ... ACCOUNT UNLOCK` 解锁命令时。

> **注意：**
>
> 当用户因密码连续失败次数达到设定值而被自动锁定时，如果修改该账户的密码连续错误限制登录策略，需要注意：
>
> - 修改该用户的登录失败次数 `FAILED_LOGIN_ATTEMPTS`，用户的自动锁定状态不会改变。修改后的连续登录失败次数，将在用户解锁后再次尝试登录时生效。
> - 修改该用户的锁定时间 `PASSWORD_LOCK_TIME`，用户的自动锁定状态不会改变。修改后的用户锁定时间，将在账户再次登录尝试时检查是否满足此时的锁定时间要求，如果锁定时间结束就会解锁该用户。
