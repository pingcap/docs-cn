---
title: 列级脱敏策略
summary: 本文介绍如何使用列级脱敏策略来保护 TiDB 中的敏感数据。
---

# 列级脱敏策略

列级脱敏策略是 TiDB 中的一项安全功能，允许你为表中的指定列创建脱敏规则来保护敏感数据。当对列应用脱敏策略时，TiDB 会按照定义的规则自动对返回给用户的查询结果数据进行脱敏，而原始数据在存储中保持不变。

列级脱敏策略适用于需要限制敏感数据可见性的场景，例如控制信用卡号、身份证号、电话号码、电子邮件地址、出生日期等敏感信息的访问范围。此功能也有助于满足 PCI DSS（支付卡行业数据安全标准）等合规要求，以及 GDPR（通用数据保护条例）、CCPA（加州消费者隐私法案）等数据隐私法规中对敏感数据访问控制的要求。

## 概述

脱敏策略绑定到表中的单个列。每个列最多只能绑定一个脱敏策略。策略表达式通常使用 SQL `CASE WHEN` 表达式，并结合 `CURRENT_USER()` 或 `CURRENT_ROLE()` 判断当前会话是否可以查看原始值。

主要特性：

- **结果阶段脱敏**：TiDB 在返回查询结果到客户端时应用脱敏逻辑，而不修改原始数据
- **基于用户或角色控制可见性**：不同用户或不同角色可以根据其权限看到不同级别的数据。
- **支持表达式脱敏**：可以使用 SQL `CASE WHEN` 表达式定义灵活的脱敏逻辑。
- **提供内置脱敏函数**：支持完整脱敏、部分脱敏、返回 `NULL`、日期替换等常见脱敏方式。
- **支持操作限制**：可以使用 `RESTRICT ON` 阻止某些语句将脱敏数据复制或写入其他表。

## 所需权限

要管理脱敏策略，用户需要以下动态权限：

| 权限 | 描述 |
|-----------|-------------|
| `CREATE MASKING POLICY` | 创建新的脱敏策略 |
| `ALTER MASKING POLICY` | 修改现有策略（启用/禁用、更改表达式等） |
| `DROP MASKING POLICY` | 删除脱敏策略 |

可以使用 `GRANT` 语句授予这些权限：

```sql
GRANT CREATE MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT ALTER MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT DROP MASKING POLICY ON *.* TO 'security_admin'@'%';
```

## 创建脱敏策略

### 基本语法

```sql
CREATE [OR REPLACE] MASKING POLICY [IF NOT EXISTS] <policy_name>
  ON <table_name> (<column_name>)
  AS <masking_expression>
  [RESTRICT ON <operation_list>]
  [ENABLE | DISABLE];
```

参数说明：

- `policy_name`：脱敏策略的名称（在表内必须唯一）
- `table_name`：包含要脱敏列的表名
- `column_name`：要应用脱敏策略的列名
- `masking_expression`：定义脱敏逻辑的 SQL 表达式
- `RESTRICT ON`：可选，用于阻止只能看到该列脱敏值的用户执行指定操作。例如，阻止这类用户通过 `INSERT ... SELECT`、`CREATE TABLE ... AS SELECT` 等语句将该列的数据写入其他表，从而避免脱敏策略被绕过。
- `ENABLE | DISABLE`：可选。指定策略创建后是否立即启用。默认为 `ENABLE`。

### 示例：基于用户身份脱敏信用卡号

```sql
-- 创建包含敏感数据的表
CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), credit_card VARCHAR(20));
INSERT INTO customers VALUES (1, 'Alice', 'alice@example.com', '4532111111111111');

-- 创建脱敏策略，仅向特定用户显示完整的信用卡号
CREATE MASKING POLICY cc_mask_policy ON customers(credit_card)
  AS CASE
      WHEN CURRENT_USER() IN ('root@%', 'admin@%')
        THEN credit_card
      ELSE MASK_PARTIAL(credit_card, 4, 4, '*')
    END
  ENABLE;
```

使用此策略后：

- 用户 `root@%` 和 `admin@%` 可以看到完整的信用卡号：`4532111111111111`
- 其他用户看到脱敏后的信用卡号：`4532********1111`

## 内置脱敏函数

TiDB 提供以下内置函数，用于常见的数据脱敏模式。

- `MASK_PARTIAL()`
- `MASK_FULL()`
- `MASK_NULL()`
- `MASK_DATE()`

### MASK_PARTIAL

`MASK_PARTIAL()` 用于对字符串的一部分进行脱敏。

**语法**

```sql
MASK_PARTIAL(column, preserve_left, preserve_right, mask_char)
```

参数说明如下：

- `column`：要脱敏的字符串列。
- `preserve_left`：保留字符串开头指定数量的字符。
- `preserve_right`：保留字符串结尾指定数量的字符。
- `mask_char`：用于遮蔽的脱敏字符，例如 `'*'` 或 `'X'`。

**逻辑与数据类型**

- **逻辑**：通过遮蔽中间部分同时保留开头和结尾指定数量的字符，为字符串数据的部分脱敏提供细粒度控制。
- **类型**：VARCHAR、CHAR、TEXT 及其变体、BLOB 及其变体

**使用场景与示例**

- **场景**：脱敏信用卡、电话号码或电子邮件的中间数字，同时保留两端用于识别的字符。

```sql
-- 信用卡：显示前 4 位和后 4 位
MASK_PARTIAL(credit_card, 4, 4, '*')
-- 输入：  '4532111111111111'
-- 结果：  '4532********1111'

-- 电话：显示前 3 位和后 4 位
MASK_PARTIAL(phone, 3, 4, '*')
-- 输入：  '13812345678'
-- 结果：  '138****5678'

-- 邮箱：显示第一个字符和域名
MASK_PARTIAL(email, 1, 12, '*')
-- 输入：  'alice@example.com'
-- 结果：  'a****@example.com'

-- SSN：显示前 3 位和后 4 位
MASK_PARTIAL(ssn, 3, 4, '*')
-- 输入：  '123456789'
-- 结果：  '123**6789'
```

### MASK_FULL

`MASK_FULL()` 用于完整脱敏一个值。

**语法**

```sql
MASK_FULL(column)
```

**逻辑与数据类型**

- **逻辑**：使用特定类型的默认掩码字符替换整个值。
- **类型**：字符串、日期/DATETIME/TIMESTAMP、Duration、YEAR
- **返回规则**
    - **字符串** → 返回相同长度的字符串，所有字符替换为 `'X'`
    - **日期/DATETIME/TIMESTAMP** → 返回 `1970-01-01`（保留原始类型和小数秒精度）
    - **Duration** → 返回 `00:00:00`
    - **YEAR** → 返回 `1970`

**使用场景与示例**

- **场景**：完全隐藏敏感 ID、电话号码或整个日期值。

```sql
-- 字符串：用 'X' 替换所有字符
MASK_FULL(customer_id)
-- 输入：  'CUST12345'
-- 结果：  'XXXXXXXXX'

-- 字符串：完全隐藏邮箱
MASK_FULL(email)
-- 输入：  'alice@example.com'
-- 结果：  'XXXXXXXXXXXXXXXX'

-- 日期：替换为默认日期
MASK_FULL(birth_date)
-- 输入：  '1985-03-15'
-- 结果：  '1970-01-01'
```

### MASK_NULL

`MASK_NULL()` 用于将值脱敏为 `NULL`。

**语法**

```sql
MASK_NULL(column)
```

**逻辑与数据类型**

- **逻辑**：最严格的方法；始终返回字面量 NULL，同时保持列元数据。
- **类型**：[所有支持的列类型](#支持的列类型)（字符串、日期/时间、数值）

**使用场景与示例**

- **场景**：完全隐藏薪资、密钥或其他高度敏感的数据，不允许任何部分披露。

```sql
-- 完全隐藏薪资
MASK_NULL(salary)
-- 输入：  85000.00
-- 结果：  NULL

-- 隐藏 API 密钥
MASK_NULL(api_key)
-- 输入：  'sk_live_1234567890abcdef'
-- 结果：  NULL
```

### MASK_DATE

`MASK_DATE()` 用于将日期或时间值替换为指定的日期字面量。

**语法**

```sql
MASK_DATE(column, date_literal)
```

参数说明如下：

- `column`：要脱敏的列。
- `date_literal`：用于替换原值的日期，格式为 `'YYYY-MM-DD'`，其中 Y/M/D 组件可以保留或作为固定值进行脱敏。

**逻辑与数据类型**

- **逻辑**：类型感知操作符，用于日期组件的部分脱敏。使用指定的字面量替换日期，同时保留原始列类型。
- **类型**：DATE、DATETIME、TIMESTAMP
- **返回规则**
    - 对于 `DATE`，返回指定的日期。
    - 对于 `DATETIME` 或 `TIMESTAMP`，返回指定日期的零点时间，即 `YYYY-MM-DD 00:00:00`，并保留原始类型和小数秒精度。

**使用场景与示例**

- **场景**：保留年份用于趋势分析，或将出生日期替换为固定日期（如 1 月 1 日）。

```sql
-- 仅保留年份（设置为 1 月 1 日）
MASK_DATE(birth_date, '1985-01-01')
-- 输入：  '1985-03-15'
-- 结果：  '1985-01-01'

-- 保留年份，替换月份和日期为固定日期
MASK_DATE(hire_date, '2020-01-01')
-- 输入：  '2020-06-15'
-- 结果：  '2020-01-01'

-- 对于 DATETIME，保留类型但重置时间
MASK_DATE(created_at, '2020-01-01')
-- 输入：  '2020-06-15 14:30:45'
-- 结果：  '2020-01-01 00:00:00'
```

**完整示例：**

```sql
-- 对出生日期进行脱敏，仅显示年份
CREATE MASKING POLICY dob_mask ON customers(dob)
  AS CASE
      WHEN CURRENT_USER() = 'hr_admin@%' THEN dob
      ELSE MASK_DATE(dob, '1985-01-01')
    END
  ENABLE;
```

## 基于用户和角色的条件脱敏

### 使用 CURRENT_USER()

你可以在脱敏表达式中使用 `CURRENT_USER()` 判断当前会话对应的用户账号。

```sql
CREATE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN CURRENT_USER() = 'support_user@%' THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

### 使用 CURRENT_ROLE()

对于基于角色的访问控制，使用 `CURRENT_ROLE()`：

```sql
-- 为可以查看未脱敏数据的用户创建角色
CREATE ROLE data_viewer;

-- 基于角色创建脱敏策略
CREATE MASKING POLICY ssn_mask ON employees(ssn)
  AS CASE
      WHEN CURRENT_ROLE() = '`data_viewer`@`%`' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  ENABLE;

-- 将角色授予授权用户
GRANT data_viewer TO 'analyst'@'%';

-- 用户需要先激活角色，才能按照角色条件查看未脱敏数据：
SET ROLE data_viewer;
```

> **注意：**
>
> `CURRENT_USER()` 和 `CURRENT_ROLE()` 的返回格式不同。该行为并非 bug，与 MySQL 一致，详见 [#67227](https://github.com/pingcap/tidb/issues/67227)。
>
> - `CURRENT_USER()` 通常返回 `'user_name@host_name'`，例如 `'analyst@%'`。
> - `CURRENT_ROLE()` 返回当前激活的角色，格式通常包含反引号，例如 ``'`data_viewer`@`%`'``。如果没有激活任何角色，返回 `'NONE'`。

## `RESTRICT ON` 语义

`RESTRICT ON` 子句允许你控制脱敏数据是否可用于某些操作。通过该子句，你可以防止看到脱敏值的用户通过特定 SQL 操作复制或使用受保护列的数据，从而避免敏感信息泄露。

### 支持的操作

| 操作 | 描述 |
|-----------|-------------|
| `INSERT_INTO_SELECT` | 阻止通过 `INSERT ... SELECT` 将受保护列的数据插入其他表 |
| `UPDATE_SELECT` | 阻止通过 `UPDATE ... SET ... = (SELECT ...)` 使用受保护列的数据更新其他表 |
| `DELETE_SELECT` | 阻止通过 `DELETE ... WHERE ... (SELECT ...)` 使用受保护列的数据作为条件删除数据 |
| `CTAS` | 阻止通过 `CREATE TABLE ... AS SELECT` 使用受保护列的数据创建新表 |
| `NONE` | 不限制上述操作，默认值 |

### 示例：使用 RESTRICT ON

```sql
-- 创建带有限制的策略
CREATE MASKING POLICY sensitive_mask ON sensitive_data(value)
  AS CASE
      WHEN CURRENT_USER() = 'admin@%' THEN value
      ELSE MASK_FULL(value)
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT)
  ENABLE;

-- 普通用户在尝试以下操作时，TiDB 会返回错误：
-- 1. 将受保护列的数据复制到另一个表
INSERT INTO other_table SELECT value FROM sensitive_data;  -- 错误

-- 2. 使用受保护列的数据更新另一个表
UPDATE some_table SET x = (SELECT value FROM sensitive_data);  -- 错误

-- 3. 使用受保护列的数据作为删除条件
DELETE FROM some_table WHERE x IN (SELECT value FROM sensitive_data);  -- 错误
```

## 管理脱敏策略

### 查看脱敏策略

使用 `SHOW MASKING POLICIES` 查看表上的策略：

```sql
-- 查看指定表上的所有脱敏策略
SHOW MASKING POLICIES FOR customers;

-- 查看特定列上的策略
SHOW MASKING POLICIES FOR customers WHERE column_name = 'credit_card';

-- 查看包括脱敏策略信息的表创建语句
SHOW CREATE TABLE customers;
```

### 启用或禁用策略

```sql
-- 临时禁用策略
ALTER TABLE customers DISABLE MASKING POLICY cc_mask_policy;

-- 重新启用已禁用的策略
ALTER TABLE customers ENABLE MASKING POLICY cc_mask_policy;
```

### 修改策略表达式

```sql
-- 更改脱敏表达式
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET EXPRESSION = CASE
                    WHEN CURRENT_USER() IN ('root@%', 'manager@%')
                      THEN credit_card
                    ELSE MASK_PARTIAL(credit_card, 4, 4, 'X')
                  END;
```

### 修改 RESTRICT ON 设置

```sql
-- 为策略添加限制
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT);

-- 移除所有限制
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON NONE;
```

### 删除脱敏策略

```sql
-- 从列中删除脱敏策略
ALTER TABLE customers DROP MASKING POLICY cc_mask_policy;
```

## 使用 CREATE OR REPLACE

要创建策略或替换已有策略，可以使用 `CREATE OR REPLACE MASKING POLICY`：

```sql
-- 使用新规则创建或替换策略
CREATE OR REPLACE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN CURRENT_USER() IN ('admin@%', 'support@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

如果同名策略已经存在，TiDB 会使用新的定义替换原有策略。

## 行为注意事项

### 结果阶段脱敏

TiDB 在查询结果阶段应用脱敏策略，这意味着：

1. **存储中的原始数据不变**：脱敏策略不会修改表中存储的值。
2. **查询处理使用原始值**：`JOIN`、`WHERE`、`GROUP BY`、`HAVING`、`ORDER BY` 等操作仍基于原始值计算。
3. **仅查询返回的结果使用脱敏值**：TiDB 会在最终结果返回给客户端前，根据策略表达式对列值或引用该列的返回表达式结果进行脱敏。

理解这一点很重要：

```sql
-- 创建脱敏邮箱列
CREATE MASKING POLICY email_mask ON users(email)
  AS CASE
      WHEN CURRENT_USER() = 'admin@%' THEN email
      ELSE MASK_FULL(email)
    END
  ENABLE;

-- 即使用户在 Where 条件输入未脱敏数据，过滤仍然有效
SELECT * FROM users WHERE email = 'user@example.com';
-- 即使显示的邮箱被脱敏，这也会返回该行
```

### 支持的列类型

脱敏策略支持以下列类型：

- **字符串类型**：`VARCHAR`、`CHAR`、`TEXT` 及其变体
- **二进制类型**：`BINARY`、`VARBINARY`、`BLOB`
- **日期和时间类型**：`DATE`、`TIME`、`DATETIME`、`TIMESTAMP`、`YEAR`

对于 `LONGTEXT` 和大型 `BLOB` 类型，仅支持使用 `MASK_FULL()` 或 `MASK_NULL()` 进行完整脱敏或返回 `NULL`。

### 限制

以下对象或场景不支持创建脱敏策略：

- 视图
- 生成列
- 临时表
- 系统表

此外，如果列上存在脱敏策略，TiDB 会阻止修改该列的类型、长度或精度。要修改列定义，需要先删除该列上的脱敏策略，完成列变更后再重新创建策略。

TiDB 不支持直接在视图上创建脱敏策略。但如果视图引用的原始表中的列已经绑定脱敏策略，通过视图查询这些列时，仍会应用原始表上的脱敏策略。

### 级联行为

当删除带有脱敏策略的列或表时，TiDB 会同步删除列或表相关的脱敏策略。当重命名表或列时，脱敏策略仍然绑定到重命名后的表或列。

## 完整示例

以下是一个展示典型工作流的完整示例：

```sql
-- 1. 创建表
CREATE TABLE employees (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100),
  salary DECIMAL(10,2),
  ssn VARCHAR(11)
);

INSERT INTO employees VALUES
  (1, 'John Doe', 'john.doe@company.com', 75000.00, '123456789'),
  (2, 'Jane Smith', 'jane.smith@company.com', 85000.00, '987654321');

-- 2. 创建用户
CREATE USER hr_admin;
CREATE USER hr_viewer;
CREATE USER regular_user;

GRANT SELECT ON employees TO hr_admin, hr_viewer, regular_user;

-- 3. 创建角色
CREATE ROLE salary_access;

-- 4. 创建脱敏策略
-- 邮箱：向 HR 人员显示，其他人部分显示
CREATE MASKING POLICY email_policy ON employees(email)
  AS CASE
      WHEN CURRENT_USER() IN ('hr_admin@%', 'hr_viewer@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;

-- 薪资：仅向具有 salary_access 角色的人显示
CREATE MASKING POLICY salary_policy ON employees(salary)
  AS CASE
      WHEN CURRENT_ROLE() = 'salary_access' THEN salary
      ELSE NULL
    END
  ENABLE;

-- SSN：严格脱敏，限制复制操作
CREATE MASKING POLICY ssn_policy ON employees(ssn)
  AS CASE
      WHEN CURRENT_USER() = 'hr_admin@%' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT)
  ENABLE;

-- 5. 授予角色
GRANT salary_access TO hr_admin;

-- 6. 测试策略
-- 以 regular_user 连接 - 看到脱敏数据
-- 以 hr_viewer 连接 - 看到邮箱但薪资被脱敏
-- 以 hr_admin 连接并使用 SET ROLE salary_access - 看到所有数据
```

## MySQL 兼容性

列级脱敏策略是 TiDB 特有的功能，与 MySQL 不兼容。相关 DDL 语法、内置脱敏函数和运行时行为均为 TiDB 扩展。

如果需要使用 BR（备份与恢复）或 TiCDC 等工具在不同 TiDB 集群之间迁移或复制带有脱敏策略的表，请注意以下事项：

1. 确认目标集群的 TiDB 版本和复制数据所用的工具版本（BR 和 TiCDC）均支持列级脱敏策略。
2. 脱敏策略 DDL 会被复制到目标集群，但用户和角色定义必须在目标集群上单独创建。
3. 如果策略表达式依赖 `CURRENT_USER()` 或 `CURRENT_ROLE()`，目标集群需要具有对应的用户或角色，否则脱敏行为可能与源集群不同。

## 参见

- [基于角色的访问控制](/role-based-access-control.md)
- [权限管理](/privilege-management.md)
- [用户账户管理](/user-account-management.md)
