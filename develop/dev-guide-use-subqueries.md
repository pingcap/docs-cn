---
title: Subquery
summary: Learn how to use subquery in TiDB.
---

# Subquery

This document introduces subquery statements and categories in TiDB.

## Overview

An subquery is a query within another SQL query. With subquery, the query result can be used in another query.

The following takes the [Bookshop](/develop/dev-guide-bookshop-schema-design.md) application as an example to introduce subquery.

## Subquery statement

In most cases, there are five types of subqueries:

- Scalar Subquery, such as `SELECT (SELECT s1 FROM t2) FROM t1`.
- Derived Tables, such as `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`.
- Existential Test, such as `WHERE NOT EXISTS(SELECT ... FROM t2)`, `WHERE t1.a IN (SELECT ... FROM t2)`.
- Quantified Comparison, such as `WHERE t1.a = ANY(SELECT ... FROM t2)`, `WHERE t1.a = ANY(SELECT ... FROM t2)`.
- Subquery as a comparison operator operand, such as `WHERE t1.a > (SELECT ... FROM t2)`.

## Category of subquery

The subquery can be categorized as [Correlated Subquery](https://en.wikipedia.org/wiki/Correlated_subquery) and Self-contained Subquery. TiDB treats these two types differently.

Whether a subquery is correlated or not depends on whether it refers to columns used in its outer query.

### Self-contained subquery

For a self-contained subquery that uses subquery as operand of comparison operators (`>`, `>=`, `<` , `<=` , `=` , or `! =`), the inner subquery queries only once, and TiDB rewrites it as a constant during the execution plan phase.

For example, to query authors in the `authors` table whose age is greater than the average age, you can use a subquery as a comparison operator operand.

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

The inner subquery is executed before TiDB executes the above query:

```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

Suppose the result of the query is 34, that is, the average age is 34, and 34 will be used as a constant to replace the original subquery.

```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

The result is as follows:

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

For self-contained subqueries such as Existential Test and Quantified Comparison, TiDB rewrites and replaces them with equivalent queries for better performance. For more information, see [Subquery Related Optimizations](/subquery-optimization.md).

### Correlated subquery

For correlated subquery, because the inner subquery references the columns from the outer query, each subquery is executed once for each row of the outer query. That is, assuming that the outer query gets 10 million results, the subquery will also be executed 10 million times, which will consume more time and resources.

Therefore, in the process of processing, TiDB will try to [Decorrelate of Correlated Subquery](/correlated-subquery-optimization.md) to improve the query efficiency at the execution plan level.

The following statement is to query authors who are older than the average age of other authors of the same gender.

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

TiDB rewrites it to an equivalent `join` query:

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

As a best practice, in actual development, it is recommended to avoid querying through a correlated subquery if you can write another equivalent query with better performance.

## Read more

- [Subquery Related Optimizations](/subquery-optimization.md)
- [Decorrelation of Correlated Subquery](/correlated-subquery-optimization.md)
- [Subquery Optimization in TiDB](https://en.pingcap.com/blog/subquery-optimization-in-tidb/)
