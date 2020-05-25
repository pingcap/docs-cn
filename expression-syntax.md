---
title: 表达式语法
summary: 本文列出 TiDB 的表达式语法。
category: reference
aliases: ['/docs-cn/dev/reference/sql/language-structure/expression-syntax/']
---

# 表达式语法 (Expression Syntax)

在 TiDB 中，以下规则是表达式的语法，详情可参考 [TiDB SQL 语法](https://pingcap.github.io/sqlgram/#Expression)。

```
Expression ::=
  singleAtIdentifier assignmentEq Expression
| Expression logOr Expression
| Expression "XOR" Expression
| Expression logAnd Expression
| "NOT" Expression
| "MATCH" '(' ColumnNameList ')' "AGAINST" '(' BitExpr FulltextSearchModifierOpt ')'
| BoolPri IsOrNotOp trueKwd
| BoolPri IsOrNotOp falseKwd
| BoolPri IsOrNotOp "UNKNOWN"
| BoolPri

BitExpr ::=
  BitExpr '|' BitExpr
| BitExpr '&' BitExpr
| BitExpr "<<" BitExpr
| BitExpr ">>" BitExpr
| BitExpr '+' BitExpr
| BitExpr '-' BitExpr
| BitExpr '+' "INTERVAL" Expression TimeUnit
| BitExpr '-' "INTERVAL" Expression TimeUnit
| BitExpr '*' BitExpr
| BitExpr '/' BitExpr
| BitExpr '%' BitExpr
| BitExpr "DIV" BitExpr
| BitExpr "MOD" BitExpr
| BitExpr '^' BitExpr
| SimpleExpr

FulltextSearchModifierOpt ::=

| "IN" "NATURAL" "LANGUAGE" "MODE"
| "IN" "NATURAL" "LANGUAGE" "MODE" "WITH" "QUERY" "EXPANSION"
| "IN" "BOOLEAN" "MODE"
| "WITH" "QUERY" "EXPANSION"

BoolPri ::=
  BoolPri IsOrNotOp "NULL"
| BoolPri CompareOp PredicateExpr
| BoolPri CompareOp AnyOrAll SubSelect
| BoolPri CompareOp singleAtIdentifier assignmentEq PredicateExpr
| PredicateExpr

IsOrNotOp ::=
  "IS"
| "IS" "NOT"

SimpleExpr ::=
  SimpleIdent
| FunctionCallKeyword
| FunctionCallNonKeyword
| FunctionCallGeneric
| SimpleExpr "COLLATE" CollationName
| WindowFuncCall
| Literal
| paramMarker
| Variable
| SumExpr
| '!' SimpleExpr
| '~' SimpleExpr
| '-' SimpleExpr
| '+' SimpleExpr
| SimpleExpr pipes SimpleExpr
| not2 SimpleExpr
| SubSelect
| '(' Expression ')'
| '(' ExpressionList ',' Expression ')'
| "ROW" '(' ExpressionList ',' Expression ')'
| "EXISTS" SubSelect
| "BINARY" SimpleExpr
| builtinCast '(' Expression "AS" CastType ')'
| "CASE" ExpressionOpt WhenClauseList ElseOpt "END"
| "CONVERT" '(' Expression ',' CastType ')'
| "CONVERT" '(' Expression "USING" CharsetName ')'
| "DEFAULT" '(' SimpleIdent ')'
| "VALUES" '(' SimpleIdent ')'
| SimpleIdent jss stringLit
| SimpleIdent juss stringLit

CompareOp ::=
  ">="
| '>'
| "<="
| '<'
| "!="
| "<>"
| "="
| "<=>"

PredicateExpr ::=
  BitExpr InOrNotOp '(' ExpressionList ')'
| BitExpr InOrNotOp SubSelect
| BitExpr BetweenOrNotOp BitExpr "AND" PredicateExpr
| BitExpr LikeOrNotOp SimpleExpr LikeEscapeOpt
| BitExpr RegexpOrNotOp SimpleExpr
| BitExpr

AnyOrAll ::=
  "ANY"
| "SOME"
| "ALL"

SubSelect ::=
  '(' SelectStmt ')'
| '(' UnionStmt ')'

SimpleIdent ::=
  Identifier
| Identifier '.' Identifier
| '.' Identifier '.' Identifier
| Identifier '.' Identifier '.' Identifier

Literal ::=
  "FALSE"
| "NULL"
| "TRUE"
| floatLit
| decLit
| intLit
| StringLiteral
| "UNDERSCORE_CHARSET" stringLit
| hexLit
| bitLit

Variable ::=
  SystemVariable
| UserVariable

SumExpr ::=
  "AVG" '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinBitAnd '(' Expression ')' OptWindowingClause
| builtinBitAnd '(' "ALL" Expression ')' OptWindowingClause
| builtinBitOr '(' Expression ')' OptWindowingClause
| builtinBitOr '(' "ALL" Expression ')' OptWindowingClause
| builtinBitXor '(' Expression ')' OptWindowingClause
| builtinBitXor '(' "ALL" Expression ')' OptWindowingClause
| builtinCount '(' DistinctKwd ExpressionList ')'
| builtinCount '(' "ALL" Expression ')' OptWindowingClause
| builtinCount '(' Expression ')' OptWindowingClause
| builtinCount '(' '*' ')' OptWindowingClause
| builtinGroupConcat '(' BuggyDefaultFalseDistinctOpt ExpressionList OrderByOptional OptGConcatSeparator ')' OptWindowingClause
| builtinMax '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinMin '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinSum '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinStddevPop '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinStddevSamp '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinVarPop '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| builtinVarSamp '(' BuggyDefaultFalseDistinctOpt Expression ')' OptWindowingClause
| "JSON_OBJECTAGG" '(' Expression ',' Expression ')' OptWindowingClause
| "JSON_OBJECTAGG" '(' "ALL" Expression ',' Expression ')' OptWindowingClause
| "JSON_OBJECTAGG" '(' Expression ',' "ALL" Expression ')' OptWindowingClause
| "JSON_OBJECTAGG" '(' "ALL" Expression ',' "ALL" Expression ')' OptWindowingClause
```
