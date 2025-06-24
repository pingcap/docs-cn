---
title: 表达式语法
summary: 了解 TiDB 中的表达式语法。
---

# 表达式语法

表达式是一个或多个值、运算符或函数的组合。在 TiDB 中，表达式主要用于 `SELECT` 语句的各个子句中，包括 Group by 子句、Where 子句、Having 子句、Join 条件和窗口函数。此外，一些 DDL 语句也使用表达式，例如在创建表时设置默认值、列和分区规则。

表达式可以分为以下类型：

- 标识符。参考[架构对象名称](/schema-object-names.md)。

- 谓词、数值、字符串、日期表达式。这些类型的[字面值](/literal-values.md)也是表达式。

- 函数调用和窗口函数。参考[函数和操作符概览](/functions-and-operators/functions-and-operators-overview.md)和[窗口函数](/functions-and-operators/window-functions.md)。

- 参数标记（`?`）、系统变量、用户变量和 CASE 表达式。

以下规则是表达式语法，基于 TiDB 解析器的 [`parser.y`](https://github.com/pingcap/tidb/blob/release-8.1/pkg/parser/parser.y) 规则。

```ebnf+diagram
Expression ::=
    ( singleAtIdentifier assignmentEq | 'NOT' | Expression ( logOr | 'XOR' | logAnd ) ) Expression
|   'MATCH' '(' ColumnNameList ')' 'AGAINST' '(' BitExpr FulltextSearchModifierOpt ')'
|   PredicateExpr ( IsOrNotOp 'NULL' | CompareOp ( ( singleAtIdentifier assignmentEq )? PredicateExpr | AnyOrAll SubSelect ) )* ( IsOrNotOp ( trueKwd | falseKwd | 'UNKNOWN' ) )?

PredicateExpr ::=
    BitExpr ( BetweenOrNotOp BitExpr 'AND' BitExpr )* ( InOrNotOp ( '(' ExpressionList ')' | SubSelect ) | LikeOrNotOp SimpleExpr LikeEscapeOpt | RegexpOrNotOp SimpleExpr )?

BitExpr ::=
    BitExpr ( ( '|' | '&' | '<<' | '>>' | '*' | '/' | '%' | 'DIV' | 'MOD' | '^' ) BitExpr | ( '+' | '-' ) ( BitExpr | "INTERVAL" Expression TimeUnit ) )
|   SimpleExpr

SimpleExpr ::=
    SimpleIdent ( ( '->' | '->>' ) stringLit )?
|   FunctionCallKeyword
|   FunctionCallNonKeyword
|   FunctionCallGeneric
|   SimpleExpr ( 'COLLATE' CollationName | pipes SimpleExpr )
|   WindowFuncCall
|   Literal
|   paramMarker
|   Variable
|   SumExpr
|   ( '!' | '~' | '-' | '+' | 'NOT' | 'BINARY' ) SimpleExpr
|   'EXISTS'? SubSelect
|   ( ( '(' ( ExpressionList ',' )? | 'ROW' '(' ExpressionList ',' ) Expression | builtinCast '(' Expression 'AS' CastType | ( 'DEFAULT' | 'VALUES' ) '(' SimpleIdent | 'CONVERT' '(' Expression ( ',' CastType | 'USING' CharsetName ) ) ')'
|   'CASE' ExpressionOpt WhenClause+ ElseOpt 'END'
```
