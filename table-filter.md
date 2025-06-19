---
title: 表过滤器
summary: TiDB 工具中表过滤器功能的使用。
---

# 表过滤器

TiDB 迁移工具默认操作所有数据库，但通常只需要处理其中的一部分。例如，你可能只想处理形如 `foo*` 和 `bar*` 的 schema，而不需要其他的。

从 TiDB 4.0 开始，所有 TiDB 迁移工具共享一个通用的过滤器语法来定义子集。本文描述如何使用表过滤器功能。

## 使用方法

### 命令行界面

可以使用多个 `-f` 或 `--filter` 命令行参数对工具应用表过滤器。每个过滤器的形式为 `db.table`，其中每个部分都可以是通配符（在[下一节](#通配符)中进一步解释）。以下列出了示例用法。

<CustomContent platform="tidb">

* [BR](/br/backup-and-restore-overview.md)：

    ```shell
    tiup br backup full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

    ```shell
    tiup br restore full -f 'foo*.*' -f 'bar*.*' -s 'local:///tmp/backup'
    ```

</CustomContent>

* [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)：

    ```shell
    tiup dumpling -f 'foo*.*' -f 'bar*.*' -P 3306 -o /tmp/data/
    ```

<CustomContent platform="tidb">

* [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)：

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

<CustomContent platform="tidb-cloud">

* [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)：

    ```shell
    tiup tidb-lightning -f 'foo*.*' -f 'bar*.*' -d /tmp/data/ --backend tidb
    ```

</CustomContent>

### TOML 配置文件

TOML 文件中的表过滤器被指定为[字符串数组](https://toml.io/en/v1.0.0-rc.1#section-15)。以下列出了示例用法。

* TiDB Lightning：

    ```toml
    [mydumper]
    filter = ['foo*.*', 'bar*.*']
    ```

<CustomContent platform="tidb">

* [TiCDC](/ticdc/ticdc-overview.md)：

    ```toml
    [filter]
    rules = ['foo*.*', 'bar*.*']

    [[sink.dispatchers]]
    matcher = ['db1.*', 'db2.*', 'db3.*']
    dispatcher = 'ts'
    ```

</CustomContent>

## 语法

### 普通表名

每个表过滤器规则由一个"schema 模式"和一个"表模式"组成，用点号 (`.`) 分隔。完全限定名称匹配规则的表会被接受。

```
db1.tbl1
db2.tbl2
db3.tbl3
```

普通名称必须只包含有效的[标识符字符](/schema-object-names.md)，例如：

* 数字（`0` 到 `9`）
* 字母（`a` 到 `z`，`A` 到 `Z`）
* `$`
* `_`
* 非 ASCII 字符（U+0080 到 U+10FFFF）

所有其他 ASCII 字符都是保留的。某些标点符号具有特殊含义，将在下一节中描述。

### 通配符

名称的每个部分都可以是 [fnmatch(3)](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_13) 中描述的通配符符号：

* `*` — 匹配零个或多个字符
* `?` — 匹配一个字符
* `[a-z]` — 匹配一个在 "a" 到 "z" 范围内的字符（包含边界）
* `[!a-z]` — 匹配一个不在 "a" 到 "z" 范围内的字符

```
db[0-9].tbl[0-9a-f][0-9a-f]
data.*
*.backup_*
```

这里的"字符"指 Unicode 码点，例如：

* U+00E9 (é) 是 1 个字符。
* U+0065 U+0301 (é) 是 2 个字符。
* U+1F926 U+1F3FF U+200D U+2640 U+FE0F (🤦🏿‍♀️) 是 5 个字符。

### 文件导入

要将文件作为过滤器规则导入，在规则开头加上 `@` 来指定文件名。表过滤器解析器将导入文件的每一行作为额外的过滤器规则。

例如，如果文件 `config/filter.txt` 有以下内容：

```
employees.*
*.WorkOrder
```

以下两种调用方式是等效的：

```bash
tiup dumpling -f '@config/filter.txt'
tiup dumpling -f 'employees.*' -f '*.WorkOrder'
```

过滤器文件不能再导入其他文件。

### 注释和空行

在过滤器文件中，每行的前导和尾随空白都会被删除。此外，空行（空字符串）会被忽略。

行首的 `#` 标记为注释并被忽略。不在行首的 `#` 被视为语法错误。

```
# 这行是注释
db.table   # 但这部分不是注释，可能会导致错误
```

### 排除

规则开头的 `!` 表示其后的模式用于排除表不被处理。这实际上将过滤器转变为阻止列表。

```
*.*
#^ 注意：必须先添加 *.* 以包含所有表
!*.Password
!employees.salaries
```

### 转义字符

要将特殊字符转换为标识符字符，在其前面加上反斜杠 `\`。

```
db\.with\.dots.*
```

为了简单和未来的兼容性，以下序列是禁止的：

* 在删除空白后行尾的 `\`（使用 `[ ]` 来匹配行尾的字面空白）。
* `\` 后跟任何 ASCII 字母数字字符（`[0-9a-zA-Z]`）。特别是，C 风格的转义序列如 `\0`、`\r`、`\n` 和 `\t` 目前没有意义。

### 引用标识符

除了 `\`，特殊字符也可以通过使用 `"` 或 `` ` `` 引用来抑制。

```
"db.with.dots"."tbl\1"
`db.with.dots`.`tbl\2`
```

引号可以通过在标识符中重复自身来包含。

```
"foo""bar".`foo``bar`
# 等效于：
foo\"bar.foo\`bar
```

引用的标识符不能跨多行。

部分引用标识符是无效的：

```
"this is "invalid*.*
```

### 正则表达式

如果需要非常复杂的规则，每个模式可以写成用 `/` 分隔的正则表达式：

```
/^db\d{2,}$/./^tbl\d{2,}$/
```

这些正则表达式使用 [Go 方言](https://pkg.go.dev/regexp/syntax?tab=doc)。如果标识符包含匹配正则表达式的子字符串，则该模式匹配。例如，`/b/` 匹配 `db01`。

> **注意：**
>
> 正则表达式中的每个 `/` 都必须转义为 `\/`，包括在 `[…]` 内。你不能在 `\Q…\E` 之间放置未转义的 `/`。

## 多个规则

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节不适用于 TiDB Cloud。目前，TiDB Cloud 仅支持一个表过滤器规则。

</CustomContent>

当表名不匹配过滤器列表中的任何规则时，默认行为是忽略这些未匹配的表。

要构建阻止列表，必须将 `*.*` 作为第一条规则显式使用，否则所有表都将被排除。

```bash
# 每个表都会被过滤掉
tiup dumpling -f '!*.Password'

# 只有 "Password" 表被过滤掉，其余的都包含在内
tiup dumpling -f '*.*' -f '!*.Password'
```

在过滤器列表中，如果表名匹配多个模式，最后一个匹配决定结果。例如：

```
# 规则 1
employees.*
# 规则 2
!*.dep*
# 规则 3
*.departments
```

过滤结果如下：

| 表名                  | 规则 1 | 规则 2 | 规则 3 | 结果             |
|-----------------------|--------|--------|--------|------------------|
| irrelevant.table      |        |        |        | 默认（拒绝）     |
| employees.employees   | ✓      |        |        | 规则 1（接受）   |
| employees.dept_emp    | ✓      | ✓      |        | 规则 2（拒绝）   |
| employees.departments | ✓      | ✓      | ✓      | 规则 3（接受）   |
| else.departments      |        | ✓      | ✓      | 规则 3（接受）   |

> **注意：**
>
> 在 TiDB 工具中，系统 schema 在默认配置中始终被排除。系统 schema 包括：
>
> * `INFORMATION_SCHEMA`
> * `PERFORMANCE_SCHEMA`
> * `METRICS_SCHEMA`
> * `INSPECTION_SCHEMA`
> * `mysql`
> * `sys`
