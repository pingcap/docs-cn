---
title: 列级脱敏策略
summary: 本文介绍如何使用列级脱敏策略来保护 TiDB 中的敏感数据。
aliases: ['/docs/dev/column-level-masking-policy/']
---

# 列级脱敏策略

列级脱敏策略是一项安全功能，允许你在列级别应用脱敏规则来保护敏感数据。当对列应用脱敏策略时，TiDB 会根据定义的规则自动对返回给用户的数据进行脱敏，而原始数据在存储中保持不变。

此功能对于满足 PCI-DSS（支付卡行业数据安全标准）等合规要求以及数据隐私法规（如 GDPR - 通用数据保护条例、CCPA - 加州消费者隐私法案）特别有用，这些法规要求严格控制谁可以查看信用卡号、个人标识符和其他机密信息等敏感信息。

## 概述

脱敏策略绑定到表列，并在查询结果时进行评估。策略使用 SQL 表达式根据当前用户身份或角色来确定如何对数据进行脱敏。

主要特性：

- **结果时脱敏**：数据在返回给客户端时进行脱敏，而不是以脱敏形式存储
- **支持用户/角色**：不同用户可以根据其权限看到不同级别的数据
- **灵活的表达式**：使用 SQL `CASE WHEN` 表达式定义复杂的脱敏逻辑
- **内置函数**：用于常见脱敏模式的预定义函数
- **可选限制**：控制脱敏数据是否可用于某些操作

## 所需权限

要管理脱敏策略，用户需要以下动态权限：

| 权限 | 描述 |
|-----------|-------------|
| `CREATE MASKING POLICY` | 创建新的脱敏策略 |
| `ALTER MASKING POLICY` | 修改现有策略（启用/禁用、更改表达式等） |
| `DROP MASKING POLICY` | 删除脱敏策略 |

可以使用 `GRANT` 语句授予这些权限：

{{< copyable "sql" >}}

```sql
GRANT CREATE MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT ALTER MASKING POLICY ON *.* TO 'security_admin'@'%';
GRANT DROP MASKING POLICY ON *.* TO 'security_admin'@'%';
```

## 创建脱敏策略

### 基本语法

{{< copyable "sql" >}}

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
- `RESTRICT ON`：可选。指定对于无法访问未脱敏数据的用户应阻止的操作
- `ENABLE | DISABLE`：可选。策略是否处于活动状态。默认为 `ENABLE`。

### 示例：基于用户身份进行脱敏

{{< copyable "sql" >}}

```sql
-- 创建包含敏感数据的表
CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), credit_card VARCHAR(20));
INSERT INTO customers VALUES (1, 'Alice', 'alice@example.com', '4532111111111111');

-- 创建脱敏策略，仅向特定用户显示完整的信用卡号
CREATE MASKING POLICY cc_mask_policy ON customers(credit_card)
  AS CASE
      WHEN current_user() IN ('root@%', 'admin@%')
        THEN credit_card
      ELSE MASK_PARTIAL(credit_card, 4, 4, '*')
    END
  ENABLE;
```

使用此策略：
- 用户 `root@%` 和 `admin@%` 可以看到完整的信用卡号：`4532111111111111`
- 其他用户看到脱敏版本：`4532********1111`

## 内置脱敏函数

TiDB 提供了四个用于常见数据脱敏模式的内置函数：

### MASK_PARTIAL

**函数与语法**

```sql
MASK_PARTIAL(column, preserve_left, preserve_right, mask_char)
```

**逻辑与数据类型**

- **逻辑**：通过遮蔽中间部分同时保留开头和结尾指定数量的字符，为字符串数据的部分脱敏提供细粒度控制。
- **类型**：VARCHAR、CHAR、TEXT 系列、BLOB 系列

**使用场景与示例**

- **场景**：脱敏信用卡、电话号码或电子邮件的中间数字，同时保留两端用于识别的字符。

{{< copyable "sql" >}}

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
MASK_PARTIAL(email, 1, 7, '*')
-- 输入：  'alice@example.com'
-- 结果：  'a********e.com'

-- SSN：显示前 3 位和后 4 位
MASK_PARTIAL(ssn, 3, 4, '*')
-- 输入：  '123456789'
-- 结果：  '123**6789'
```

### MASK_FULL

**函数与语法**

```sql
MASK_FULL(column)
```

**逻辑与数据类型**

- **逻辑**：使用特定类型的默认掩码字符替换整个值。
- **类型**：字符串、日期/DATETIME/TIMESTAMP、Duration、YEAR
  - **字符串** → 返回相同长度的字符串，所有字符替换为 `'X'`
  - **日期/DATETIME/TIMESTAMP** → 返回 `1970-01-01`（保留原始类型和小数秒精度）
  - **Duration** → 返回 `00:00:00`
  - **YEAR** → 返回 `1970`

**使用场景与示例**

- **场景**：完全隐藏敏感 ID、电话号码或整个日期值。

{{< copyable "sql" >}}

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

**函数与语法**

```sql
MASK_NULL(column)
```

**逻辑与数据类型**

- **逻辑**：最严格的方法；始终返回字面量 NULL，同时保持列元数据。
- **类型**：所有支持的类型（字符串、日期/时间、数值）

**使用场景与示例**

- **场景**：完全隐藏薪资、密钥或其他高度敏感的数据，不允许任何部分披露。

{{< copyable "sql" >}}

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

**函数与语法**

```sql
MASK_DATE(column, date_literal)
```

**逻辑与数据类型**

- **逻辑**：类型感知操作符，用于日期组件的部分脱敏。使用指定的字面量替换日期，同时保留原始列类型。
- **类型**：DATE、DATETIME、TIMESTAMP
- **占位符**：`date_literal` 遵循格式 `'YYYY-MM-DD'`，其中 Y/M/D 组件可以保留或作为固定值进行脱敏
- **时间组件**：小时、分钟和秒重置为 `00:00:00`

**使用场景与示例**

- **场景**：保留年份用于趋势分析，或将出生日期通用化为标准日期（如 1 月 1 日）。

{{< copyable "sql" >}}

```sql
-- 仅保留年份（设置为 1 月 1 日）
MASK_DATE(birth_date, '1985-01-01')
-- 输入：  '1985-03-15'
-- 结果：  '1985-01-01'

-- 保留年份，通用化月份和日期
MASK_DATE(hire_date, '2020-01-01')
-- 输入：  '2020-06-15'
-- 结果：  '2020-01-01'

-- 对于 DATETIME，保留类型但重置时间
MASK_DATE(created_at, '2020-01-01')
-- 输入：  '2020-06-15 14:30:45'
-- 结果：  '2020-01-01 00:00:00'
```

**完整示例：**

{{< copyable "sql" >}}

```sql
-- 对出生日期进行脱敏，仅显示年份
CREATE MASKING POLICY dob_mask ON customers(dob)
  AS CASE
      WHEN current_user() = 'hr_admin@%' THEN dob
      ELSE MASK_DATE(dob, '1985-01-01')
    END
  ENABLE;
```

## 基于用户和角色的条件脱敏

### 使用 current_user()

你可以在脱敏表达式中使用 `current_user()` 来检查登录用户：

{{< copyable "sql" >}}

```sql
CREATE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN current_user() = 'support_user@%' THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

### 使用 current_role()

对于基于角色的访问控制，使用 `current_role()`：

{{< copyable "sql" >}}

```sql
-- 为可以查看未脱敏数据的用户创建角色
CREATE ROLE data_viewer;

-- 基于角色创建脱敏策略
CREATE MASKING POLICY ssn_mask ON customers(ssn)
  AS CASE
      WHEN current_role() = 'data_viewer@%' THEN ssn
      ELSE MASK_PARTIAL(ssn, 3, 4, '*')
    END
  ENABLE;

-- 将角色授予授权用户
GRANT data_viewer TO 'analyst'@'%';

-- 用户必须激活角色才能查看未脱敏的数据
SET ROLE data_viewer;
```

## RESTRICT ON 语义

`RESTRICT ON` 子句允许你控制脱敏数据是否可用于某些操作。这通过防止通过特定 SQL 操作进行数据泄露提供了额外的安全性。

### 支持的操作

| 操作 | 描述 |
|-----------|-------------|
| `INSERT_INTO_SELECT` | 阻止通过 `INSERT ... SELECT` 将脱敏数据插入另一个表 |
| `UPDATE_SELECT` | 阻止通过 `UPDATE ... SET = (SELECT ...)` 使用脱敏数据进行更新 |
| `DELETE_SELECT` | 阻止通过 `DELETE ... WHERE ... IN (SELECT ...)` 基于脱敏数据进行删除 |
| `CTAS` | 阻止使用脱敏数据进行 Create Table As Select |
| `NONE` | 无限制（默认） |

### 示例：使用 RESTRICT ON

{{< copyable "sql" >}}

```sql
-- 创建带有限制的策略
CREATE MASKING POLICY sensitive_mask ON sensitive_data(value)
  AS CASE
      WHEN current_user() = 'admin@%' THEN value
      ELSE MASK_FULL(value)
    END
  RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT)
  ENABLE;

-- 普通用户在尝试以下操作时会收到错误：
-- 1. 将脱敏数据复制到另一个表
INSERT INTO other_table SELECT value FROM sensitive_data;  -- 错误

-- 2. 使用脱敏数据进行更新
UPDATE some_table SET x = (SELECT value FROM sensitive_data);  -- 错误

-- 3. 使用脱敏数据进行删除
DELETE FROM some_table WHERE x IN (SELECT value FROM sensitive_data);  -- 错误
```

## 管理脱敏策略

### 查看脱敏策略

使用 `SHOW MASKING POLICIES` 查看表上的策略：

{{< copyable "sql" >}}

```sql
-- 显示表的所有脱敏策略
SHOW MASKING POLICIES FOR customers;

-- 显示特定列的策略
SHOW MASKING POLICIES FOR customers WHERE column_name = 'credit_card';

-- 显示包括脱敏策略信息的表创建语句
SHOW CREATE TABLE customers;
```

### 启用或禁用策略

{{< copyable "sql" >}}

```sql
-- 临时禁用策略
ALTER TABLE customers DISABLE MASKING POLICY cc_mask_policy;

-- 重新启用已禁用的策略
ALTER TABLE customers ENABLE MASKING POLICY cc_mask_policy;
```

### 修改策略表达式

{{< copyable "sql" >}}

```sql
-- 更改脱敏表达式
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET EXPRESSION = CASE
                    WHEN current_user() IN ('root@%', 'manager@%')
                      THEN credit_card
                    ELSE MASK_PARTIAL(credit_card, 4, 4, 'X')
                  END;
```

### 修改 RESTRICT ON 设置

{{< copyable "sql" >}}

```sql
-- 为策略添加限制
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON (INSERT_INTO_SELECT, UPDATE_SELECT, DELETE_SELECT);

-- 移除所有限制
ALTER TABLE customers MODIFY MASKING POLICY cc_mask_policy
  SET RESTRICT ON NONE;
```

### 删除脱敏策略

{{< copyable "sql" >}}

```sql
-- 从列中删除脱敏策略
ALTER TABLE customers DROP MASKING POLICY cc_mask_policy;
```

## 使用 CREATE OR REPLACE

要更新现有策略，使用 `CREATE OR REPLACE`：

{{< copyable "sql" >}}

```sql
-- 使用新规则创建或替换策略
CREATE OR REPLACE MASKING POLICY email_mask ON customers(email)
  AS CASE
      WHEN current_user() IN ('admin@%', 'support@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;
```

## 行为注意事项

### 结果时脱敏

脱敏策略在**结果时**应用，这意味着：

1. **存储不变**：原始数据存储时未经修改
2. **查询处理使用原始值**：`JOIN`、`WHERE`、`GROUP BY`、`HAVING`、`ORDER BY` 等操作都使用原始值
3. **仅输出被脱敏**：返回给客户端的数据根据策略进行脱敏

理解这一点很重要：

{{< copyable "sql" >}}

```sql
-- 创建脱敏邮箱列
CREATE MASKING POLICY email_mask ON users(email)
  AS CASE
      WHEN current_user() = 'admin@%' THEN email
      ELSE MASK_FULL(email)
    END
  ENABLE;

-- 即使用户看到脱敏数据，过滤仍然有效
SELECT * FROM users WHERE email = 'user@example.com';
-- 即使显示的邮箱被脱敏，这也会返回该行
```

### 支持的列类型

脱敏策略支持以下列类型：

- **字符串类型**：`VARCHAR`、`CHAR`、`TEXT` 及其变体
- **二进制类型**：`BINARY`、`VARBINARY`、`BLOB`
- **日期/时间类型**：`DATE`、`TIME`、`DATETIME`、`TIMESTAMP`、`YEAR`

对于 `LONGTEXT` 和大型 `BLOB` 类型，仅支持 `MASK_FULL` 和 `MASK_NULL`。

### 限制

以下情况**不支持**：

- 视图上的脱敏策略
- 生成列上的脱敏策略
- 临时表上的脱敏策略
- 系统表上的脱敏策略
- 在脱敏策略处于活动状态时修改列类型或长度（先删除策略）

### 级联行为

当删除具有脱敏策略的列或表时，策略会自动从系统中删除。当重命名列或表时，脱敏策略仍然绑定到它。

## 完整示例

以下是一个展示典型工作流的完整示例：

{{< copyable "sql" >}}

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
      WHEN current_user() IN ('hr_admin@%', 'hr_viewer@%') THEN email
      ELSE MASK_PARTIAL(email, 1, 7, '*')
    END
  ENABLE;

-- 薪资：仅向具有 salary_access 角色的人显示
CREATE MASKING POLICY salary_policy ON employees(salary)
  AS CASE
      WHEN current_role() = 'salary_access' THEN salary
      ELSE NULL
    END
  ENABLE;

-- SSN：严格脱敏，限制复制操作
CREATE MASKING POLICY ssn_policy ON employees(ssn)
  AS CASE
      WHEN current_user() = 'hr_admin@%' THEN ssn
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

列级脱敏策略是 TiDB 特有的功能，与 MySQL **不兼容**。语法和行为是 TiDB 独有的。

使用 BR（备份与恢复）或 TiCDC 等工具复制数据时：

1. 脱敏策略 DDL 语句会被复制
2. 必须在目标集群上单独创建用户和角色定义
3. 目标集群必须具有相同的用户/角色才能使脱敏正常工作

## 参见

- [基于角色的访问控制](/role-based-access-control.md)
- [权限管理](/privilege-management.md)
- [用户账户管理](/user-account-management.md)
