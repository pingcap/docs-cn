---
title: 表达式语法
category: user guide
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
```
