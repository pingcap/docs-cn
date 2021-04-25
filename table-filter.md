---
title: 表库过滤
summary: 在 TiDB 生态工具中使用表库过滤功能。
---

# 表库过滤

TiDB 生态工具默认情况下作用于所有数据库，但实际使用中，往往只需要作用于其中的部分子集。例如，用户只想处理 `foo*` 和 `bar*` 形式的表，而无需对其他表进行操作。

从 TiDB 4.0 起，所有 TiDB 生态系统工具都使用一个通用的过滤语法来定义子集。本文档介绍如何使用表库过滤功能。

## 使用表库过滤

### 命令行

在命令行中使用多个 `-f` 或 `--filter` 参数，即可在 TiDB 生态工具中应用表库过滤规则。每个过滤规则均采用 `db.table` 形式，支持通配符（详情见[下一节](#使用通配符)）。以下为各个工具中的使用示例：

* [BR](/br/backup-and-restore-tool.md)：

    {{< copyable "shell-regular" >}}

    ```shell
    ./br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    #                ^~~~~~~~~~~~~~~~~~~~~~~
    ./br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    #                 ^~~~~~~~~~~~~~~~~~~~~~~
    ```

* [Dumpling](/backup-and-restore-using-dumpling-lightning.md)：

    {{< copyable "shell-regular" >}}

    ```shell
    ./dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    #          ^~~~~~~~~~~~~~~~~~~~~~~
    ```

* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：

    {{< copyable "shell-regular" >}}

    ```shell
    ./tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    #                ^~~~~~~~~~~~~~~~~~~~~~~
    ```

### TOML 配置文件

在 TOML 文件中，表库过滤规则以[字符串数组](https://toml.io/cn/v1.0.0-rc.1#%E6%95%B0%E7%BB%84)的形式指定。以下为各个工具中的使用示例：

* TiDB Lightning：

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

* [TiCDC](/ticdc/ticdc-overview.md)：

    ```toml
    [filter]
    rules = ['foo*.*', 'bar*.*']

    [[sink.dispatchers]]
    matcher = ['db1.*', 'db2.*', 'db3.*']
    dispatcher = 'ts'
    ```

## 表库过滤语法

### 直接使用表名

每条表库过滤规则由“库”和“表”组成，两部分之间以英文句号 (`.`) 分隔。只有表名与规则完全相符的表才会被接受。

```
db1.tbl1
db2.tbl2
db3.tbl3
```

表名只由有效的[标识符](/schema-object-names.md)组成，例如：

* 数字（`0` 到 `9`）
* 字母（`a` 到 `z`，`A` 到 `Z`）
* `$`
* `_`
* 非 ASCII 字符（`U+0080` 到 `U+10FFFF`）

其他 ASCII 字符均为保留字。部分标点符号有特殊含义，详情见下一节。

### 使用通配符

表名的两个部分均支持使用通配符（详情见 [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13)）。

* `*`：匹配零个或多个字符。
* `?`：匹配一个字符。
* `[a-z]`：匹配 “a” 和 “z” 之间的一个字符。
* `[!a-z]`：匹配不在 “a” 和 “z” 之间的一个字符。

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

此处，“字符”指的是一个 Unicode 码位，例如：

* `U+00E9` (é) 是 1 个字符。
* `U+0065 U+0301` (é) 是 2 个字符。
* `U+1F926 U+1F3FF U+200D U+2640 U+FE0F` (🤦🏿‍♀️) 是 5 个字符。

### 使用文件导入

如需导入一个文件作为过滤规则，请在规则的开头加上一个 “@” 来指定文件名。库表过滤解析器将导入文件中的每一行都解析为一条额外的过滤规则。

例如，`config/filter.txt` 文件有以下内容：

```
employees.*
*.WorkOrder
```

以下两条表库过滤命令是等价的：

```bash
./dumpling -f '@config/filter.txt'
./dumpling -f 'employees.*' -f '*.WorkOrder'
```

导入的文件里不能使用过滤规则导入另一个文件。

### 注释与空行

导入的过滤规则文件中，每一行开头和结尾的空格都会被去除。此外，空行（空字符串）也将被忽略。

行首的 `#` 表示该行是注释，会被忽略。而不在行首的 `#` 则会被认为是语法错误。

```
# 这是一行注释
db.table   # 这一部分不是注释，且可能引起错误
```

### 排除规则

在一条过滤规则的开头加上 `!`，则表示符合这条规则的表不会被 TiDB 生态工具处理。通过应用排除规则，库表过滤可以作为屏蔽名单来使用。

```
*.*
#^ 注意：必须先添加 *.* 规则来包括所有表
!*.Password
!employees.salaries
```

### 转义字符

如果需要将特殊字符转化为标识符，可以在特殊字符前加上反斜杠 `\`。

```
db\.with\.dots.*
```

为了简化语法并向上兼容，**不支持**下列字符序列：

- 在行尾去除空格后使用 `\`（使用 `[ ]` 来匹配行尾的空格）。
- 在 `\` 后使用数字或字母 (`[0-9a-zA-Z]`)。特别是类似 C 的转义序列，如 `\0`、`\r`、`\n`、`\t` 等序列，目前在表库过滤规则中无意义。

### 引号包裹的标识符

除了 `\` 之外，还可以用 `"` 和 `` ` `` 来控制特殊字符。

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

也可以通过输入两次引号，将引号包含在标识符内。

```
"foo""bar".`foo``bar`
# 等价于：
foo\"bar.foo\`bar
```

用引号包裹的标识符不可以跨越多行。

用引号只包裹标识符的一部分是无效的，例如：

```
"this is "invalid*.*
```

### 正则表达式

如果你需要使用较复杂的过滤规则，可以将每个匹配模型写为正则表达式，以 `/` 为分隔符：

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

这类正则表示使用 [Go dialect](https://pkg.go.dev/regexp/syntax?tab=doc)。只要标识符中有一个子字符串与正则表达式匹配，则视为匹配该模型。例如，`/b/` 匹配 `db01`。

> **注意：**
>
> 正则表达式中的每一个 `/` 都需要转义为 `\/`，包括在 `[...]` 里面的 `/`。不允许在 `\Q...\E` 之间放置一个未转义的 `/`。

## 使用多个过滤规则

当表的名称与过滤列表中所有规则均不匹配时，默认情况下这些表被忽略。

要建立一个屏蔽名单，必须使用显式的 `*.*` 作为第一条过滤规则，否则所有表均被排除。

```bash
# 所有表均被过滤掉
./dumpling -f '!*.Password'

# 只有 “Password” 表被过滤掉，其余表仍保留
./dumpling -f '*.*' -f '!*.Password'
```

如果一个表的名称与过滤列表中的多个规则匹配，则以最后匹配的规则为准。例如：

```
# rule 1
employees.*
# rule 2
!*.dep*
# rule 3
*.departments
```

过滤结果如下：

| 表名            | 规则 1 | 规则 2 | 规则 3 | 结果          |
|-----------------------|--------|--------|--------|------------------|
| irrelevant.table      |        |        |        | 默认（拒绝） |
| employees.employees   | ✓      |        |        | 规则 1（接受）  |
| employees.dept_emp    | ✓      | ✓      |        | 规则 2（拒绝）  |
| employees.departments | ✓      | ✓      | ✓      | 规则 3（接受）  |
| else.departments      |        | ✓      | ✓      | 规则 3（接受）  |

> **注意：**
>
> 在 TiDB 生态工具的默认配置中，系统库总是被排除。系统库有以下六个：
>
> * `INFORMATION_SCHEMA`
> * `PERFORMANCE_SCHEMA`
> * `METRICS_SCHEMA`
> * `INSPECTION_SCHEMA`
> * `mysql`
> * `sys`
