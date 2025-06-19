---
title: 子查询
summary: 了解如何在 TiDB 中使用子查询。
---

# 子查询

本文档介绍 TiDB 中的子查询语句和类别。

## 概述

子查询是在另一个 SQL 查询中的查询。通过子查询，查询结果可以在另一个查询中使用。

以下以 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用程序为例介绍子查询。

## 子查询语句

在大多数情况下，有五种类型的子查询：

- 标量子查询，例如 `SELECT (SELECT s1 FROM t2) FROM t1`。
- 派生表，例如 `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`。
- 存在性测试，例如 `WHERE NOT EXISTS(SELECT ... FROM t2)`，`WHERE t1.a IN (SELECT ... FROM t2)`。
- 量化比较，例如 `WHERE t1.a = ANY(SELECT ... FROM t2)`，`WHERE t1.a = ANY(SELECT ... FROM t2)`。
- 作为比较运算符操作数的子查询，例如 `WHERE t1.a > (SELECT ... FROM t2)`。

## 子查询类别

子查询可以分为[相关子查询](https://en.wikipedia.org/wiki/Correlated_subquery)和独立子查询。TiDB 对这两种类型的处理方式不同。

子查询是相关的还是独立的取决于它是否引用了外部查询中使用的列。

### 独立子查询

对于使用子查询作为比较运算符（`>`、`>=`、`<`、`<=`、`=` 或 `!=`）操作数的独立子查询，内部子查询只查询一次，TiDB 在执行计划阶段将其重写为常量。

例如，要查询 `authors` 表中年龄大于平均年龄的作者，你可以使用子查询作为比较运算符的操作数。

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

在 TiDB 执行上述查询之前，内部子查询会先执行：

```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

假设查询结果为 34，即平均年龄为 34，34 将作为常量替换原始子查询。

```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

结果如下：

```
+--------+-------------------+--------+------------+------------+
| id     | name              | gender | birth_year | death_year |
+--------+-------------------+--------+------------+------------+
| 13514  | Kennith Kautzer   | 1      | 1956       | 2018       |
| 13748  | Dillon Langosh    | 1      | 1985       | NULL       |
| 99184  | Giovanny Emmerich | 1      | 1954       | 2012       |
| 180191 | Myrtie Robel      | 1      | 1958       | 2009       |
| 200969 | Iva Renner        | 0      | 1977       | NULL       |
| 209671 | Abraham Ortiz     | 0      | 1943       | 2016       |
| 229908 | Wellington Wiza   | 1      | 1932       | 1969       |
| 306642 | Markus Crona      | 0      | 1969       | NULL       |
| 317018 | Ellis McCullough  | 0      | 1969       | 2014       |
| 322369 | Mozelle Hand      | 0      | 1942       | 1977       |
| 325946 | Elta Flatley      | 0      | 1933       | 1986       |
| 361692 | Otho Langosh      | 1      | 1931       | 1997       |
| 421294 | Karelle VonRueden | 0      | 1977       | NULL       |
...
```

对于存在性测试和量化比较等独立子查询，TiDB 会将其重写并替换为等效查询以获得更好的性能。更多信息，请参阅[子查询相关优化](/subquery-optimization.md)。

### 相关子查询

对于相关子查询，由于内部子查询引用了外部查询的列，每个子查询都会为外部查询的每一行执行一次。也就是说，假设外部查询得到 1000 万个结果，子查询也会执行 1000 万次，这将消耗更多的时间和资源。

因此，在处理过程中，TiDB 会尝试在执行计划层面[去关联化相关子查询](/correlated-subquery-optimization.md)以提高查询效率。

以下语句用于查询年龄大于同性别其他作者平均年龄的作者。

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(
            IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
        ) AS average_age
    FROM
        authors a2
    WHERE a1.gender = a2.gender
);
```

TiDB 将其重写为等效的 `join` 查询：

```sql
SELECT *
FROM
    authors a1,
    (
        SELECT
            gender, AVG(
                IFNULL(a2.death_year, YEAR(NOW())) - IFNULL(a2.birth_year, YEAR(NOW()))
            ) AS average_age
        FROM
            authors a2
        GROUP BY gender
    ) a2
WHERE
    a1.gender = a2.gender
    AND (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > a2.average_age;
```

作为最佳实践，在实际开发中，如果可以使用另一个具有更好性能的等效查询，建议避免通过相关子查询进行查询。

## 阅读更多

- [子查询相关优化](/subquery-optimization.md)
- [相关子查询的去关联化](/correlated-subquery-optimization.md)
- [TiDB 中的子查询优化](https://www.pingcap.com/blog/subquery-optimization-in-tidb/)

## 需要帮助？

<CustomContent platform="tidb">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](/support.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

在 [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 或 [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap-docs) 上询问社区，或[提交支持工单](https://tidb.support.pingcap.com/)。

</CustomContent>
