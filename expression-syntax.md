---
title: 表达式语法
aliases: ['/docs-cn/v2.1/expression-syntax/','/docs-cn/v2.1/reference/sql/language-structure/expression-syntax/']
---

# 表达式语法 (Expression Syntax)

在 TiDB 中，以下规则是表达式的语法，你可以在 `parser/parser.y` 中找到定义。TiDB 的语法解析是基于 yacc 的。

```
Expression:
      singleAtIdentifier assignmentEq Expression
    | Expression logOr Expression
    | Expression "XOR" Expression
    | Expression logAnd Expression
    | "NOT" Expression
    | Factor IsOrNotOp trueKwd
    | Factor IsOrNotOp falseKwd
    | Factor IsOrNotOp "UNKNOWN"
    | Factor

Factor:
      Factor IsOrNotOp "NULL"
    | Factor CompareOp PredicateExpr
    | Factor CompareOp singleAtIdentifier assignmentEq PredicateExpr
    | Factor CompareOp AnyOrAll SubSelect
    | PredicateExpr

PredicateExpr:
      PrimaryFactor InOrNotOp '(' ExpressionList ')'
    | PrimaryFactor InOrNotOp SubSelect
    | PrimaryFactor BetweenOrNotOp PrimaryFactor "AND" PredicateExpr
    | PrimaryFactor LikeOrNotOp PrimaryExpression LikeEscapeOpt
    | PrimaryFactor RegexpOrNotOp PrimaryExpression
    | PrimaryFactor

<<<<<<< HEAD
PrimaryFactor:
      PrimaryFactor '|' PrimaryFactor
    | PrimaryFactor '&' PrimaryFactor
    | PrimaryFactor "<<" PrimaryFactor
    | PrimaryFactor ">>" PrimaryFactor
    | PrimaryFactor '+' PrimaryFactor
    | PrimaryFactor '-' PrimaryFactor
    | PrimaryFactor '*' PrimaryFactor
    | PrimaryFactor '/' PrimaryFactor
    | PrimaryFactor '%' PrimaryFactor
    | PrimaryFactor "DIV" PrimaryFactor
    | PrimaryFactor "MOD" PrimaryFactor
    | PrimaryFactor '^' PrimaryFactor
    | PrimaryExpression

PrimaryExpression:
      Operand
    | FunctionCallKeyword
    | FunctionCallNonKeyword
    | FunctionCallAgg
    | FunctionCallGeneric
    | Identifier jss stringLit
    | Identifier juss stringLit
    | SubSelect
    | '!' PrimaryExpression
    | '~'  PrimaryExpression
    | '-' PrimaryExpression
    | '+' PrimaryExpression
    | "BINARY" PrimaryExpression
    | PrimaryExpression "COLLATE" StringName
=======
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
>>>>>>> 59ffc3de... sql-statements: use EBNF to render syntax diagrams for ADD, ALTER and ANALYZE statements (#5324)
```
