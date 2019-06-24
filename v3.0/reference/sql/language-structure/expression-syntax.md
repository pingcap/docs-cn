---
title: Expression Syntax
summary: Learn about the expression syntax in TiDB.
category: reference
aliases: ['/docs/sql/expression-syntax/']
---

# Expression Syntax

The following rules define the expression syntax in TiDB. You can find the definition in `parser/parser.y`. The syntax parsing in TiDB is based on Yacc.

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
