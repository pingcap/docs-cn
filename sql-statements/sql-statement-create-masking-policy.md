---
title: CREATE MASKING POLICY
summary: TiDB 数据库中 CREATE MASKING POLICY 的使用概况。
---

# CREATE MASKING POLICY

`CREATE MASKING POLICY` 用于为表中的列创建[数据脱敏策略](/column-level-masking-policy.md)。启用列脱敏策略后，TiDB 在返回查询结果时会根据策略定义对相应列的结果进行脱敏，从而防止敏感数据被未授权用户查看。

脱敏策略绑定到表中的列上，你可以在脱敏表达式中使用 `CURRENT_USER()` 或 `CURRENT_ROLE()` 函数，实现基于用户身份或角色的条件脱敏。

## 所需权限

创建脱敏策略需要拥有目标表所在数据库的 `CREATE MASKING POLICY` 权限（或者 `SUPER` 权限）。

## 语法图

```ebnf+diagram
CreateMaskingPolicyStmt ::=
    'CREATE' OrReplace 'MASKING' 'POLICY' IfNotExists PolicyName 'ON' TableName '(' Identifier ')' 'AS' Expression MaskingPolicyRestrictOnOpt MaskingPolicyStateOpt

PolicyName ::=
    Identifier

MaskingPolicyRestrictOnOpt ::=
    ( 'RESTRICT' 'ON' '(' MaskingPolicyRestrictOperationList ')' )?
|   'RESTRICT' 'ON' 'NONE'

MaskingPolicyRestrictOperationList ::=
    MaskingPolicyRestrictOperation ( ',' MaskingPolicyRestrictOperation )*

MaskingPolicyRestrictOperation ::=
    Identifier

MaskingPolicyStateOpt ::=
    ( 'ENABLE' | 'DISABLE' )?
```

## 语法说明

| 语法元素 | 说明 |
| -------- | ---- |
| `PolicyName` | 脱敏策略的名称，在同一个表内必须唯一。 |
| `TableName` | 目标表的名称。 |
| `Identifier`（括号内） | 目标列的名称。每个列最多只能绑定一个脱敏策略。 |
| `Expression` | 脱敏表达式。可以使用内置脱敏函数（如 `MASK_FULL`、`MASK_PARTIAL`、`MASK_NULL`、`MASK_DATE`），也可以使用包含 `CURRENT_USER()` 或 `CURRENT_ROLE()` 的自定义表达式来实现基于身份的条件脱敏。 |
| `RESTRICT ON (...)` | 可选。限制在脱敏列上进行特定的操作，防止通过这些操作间接获取原始数据。可限制的操作包括 `INSERT INTO SELECT`、`UPDATE SELECT`、`DELETE SELECT`、`CTAS`。 |
| `ENABLE` \| `DISABLE` | 可选。指定策略创建后是否立即启用。默认为 `ENABLE`。 |

### 内置脱敏函数

| 函数 | 说明 | 示例 |
| ---- | ---- | ---- |
| `MASK_FULL(col)` | 完全掩码。将列值替换为固定长度的掩码字符。 | `MASK_FULL(ssn)` → `'XXXXXXXXX'` |
| `MASK_PARTIAL(col, prefix_len, suffix_len, mask_char)` | 部分掩码。保留列值的前 `prefix_len` 个和后 `suffix_len` 个字符，中间用 `mask_char` 替换。 | `MASK_PARTIAL(phone, 3, 3, '*')` → `'123****890'` |
| `MASK_NULL(col)` | 空值掩码。将列值替换为 `NULL`。 | `MASK_NULL(salary)` → `NULL` |
| `MASK_DATE(col, date_literal)` | 日期掩码。将日期列值替换为固定的日期字面量。 | `MASK_DATE(birth_date, '1970-01-01')` → `'1970-01-01'` |

## 示例

### 创建一个部分脱敏策略

以下示例创建一个脱敏策略，对 `contacts` 表的 `phone` 列进行部分脱敏，保留前 3 个字符和后 3 个字符，其余部分使用 `*` 替换：

```sql
CREATE TABLE contacts (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  phone VARCHAR(20)
);

CREATE MASKING POLICY p_mask_phone
  ON contacts(phone)
  AS MASK_PARTIAL(phone, 3, 3, '*') ENABLE;
```

```
Query OK, 0 rows affected (0.10 sec)
```

插入数据并查询：

```sql
INSERT INTO contacts VALUES (1, 'Alice', '1234567890');
SELECT phone FROM contacts WHERE id = 1;
```

```
Query OK, 1 row affected (0.01 sec)

+-------------+
| phone       |
+-------------+
| 123****890  |
+-------------+
1 row in set (0.00 sec)
```

### 创建一个完全脱敏策略

以下示例创建一个脱敏策略，对 `employees` 表的 `ssn` 列进行完全脱敏：

```sql
CREATE MASKING POLICY p_mask_ssn
  ON employees(ssn)
  AS MASK_FULL(ssn) ENABLE;
```

### 创建一个带操作限制的脱敏策略

以下示例创建一个脱敏策略，同时限制脱敏列不能用于 `INSERT INTO SELECT` 和 `CTAS` 操作：

```sql
CREATE MASKING POLICY p_mask_credit_card
  ON users(credit_card)
  AS MASK_FULL(credit_card)
  RESTRICT ON (INSERT INTO SELECT, CTAS) ENABLE;
```

### 创建一个条件脱敏策略

以下示例创建一个基于角色的条件脱敏策略。只有拥有 `hr_manager` 或 `ceo` 角色的用户可以查看原始数据，其他用户只能看到脱敏结果：

```sql
CREATE MASKING POLICY p_mask_salary
  ON employees(salary)
  AS IF(CURRENT_ROLE() IN ('hr_manager', 'ceo'), salary, MASK_NULL(salary)) ENABLE;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
* [SHOW MASKING POLICIES](/sql-statements/sql-statement-show-masking-policies.md)