---
title: 子查询
summary: 介绍 TiDB 子查询功能。
---

# 子查询

本章将介绍 TiDB 中的子查询功能。

## 概述

子查询是嵌套在另一个查询中的 SQL 表达式，借助子查询，可以在一个查询当中使用另外一个查询的查询结果。

下面将以 [Bookshop](/develop/dev-guide-bookshop-schema-design.md) 应用为例对子查询展开介绍：

## 子查询语句

通常情况下，子查询语句分为如下几种形式：

- 标量子查询（Scalar Subquery），如 `SELECT (SELECT s1 FROM t2) FROM t1`。
- 派生表（Derived Tables），如 `SELECT t1.s1 FROM (SELECT s1 FROM t2) t1`。
- 存在性测试（Existential Test），如 `WHERE NOT EXISTS(SELECT ... FROM t2)`，`WHERE t1.a IN (SELECT ... FROM t2)`。
- 集合比较（Quantified Comparison），如 `WHERE t1.a = ANY(SELECT ... FROM t2)`。
- 作为比较运算符操作数的子查询, 如 `WHERE t1.a > (SELECT ... FROM t2)`。

## 子查询的分类

一般来说，可以将子查询分为关联子查询（[Correlated Subquery](https://en.wikipedia.org/wiki/Correlated_subquery)）和无关联子查询 (Self-contained Subquery) 两大类，TiDB 对于这两类子查询的处理方式是不一样的。

判断是否为关联子查询的依据在于子查询当中是否引用了外层查询的列。

### 无关联子查询

对于将子查询作为比较运算符 (`>` / `>=`/ `<` / `<=` / `=` / `!=`) 操作数的这类无关联子查询而言，内层子查询只需要进行一次查询，TiDB 在生成执行计划阶段会将内层子查询改写为常量。

例如，想要查找 `authors` 表当中年龄大于总体平均年龄的作家，可以通过将子查询作为比较操作符的操作数来实现：

```sql
SELECT * FROM authors a1 WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > (
    SELECT
        AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age
    FROM
        authors a2
)
```

在 TiDB 执行上述查询的时候会先执行一次内层子查询：

```sql
SELECT AVG(IFNULL(a2.death_year, YEAR(NOW())) - a2.birth_year) AS average_age FROM authors a2;
```

假设查询得到的结果为 34，即总体平均年龄为 34，34 将作为常量替换掉原来的子查询。

```sql
SELECT * FROM authors a1
WHERE (IFNULL(a1.death_year, YEAR(NOW())) - a1.birth_year) > 34;
```

运行结果为：

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

对于存在性测试和集合比较两种情况下的无关联列子查询，TiDB 会将其进行改写和等价替换以获得更好的执行性能，你可以通过阅读[子查询相关的优化](/subquery-optimization.md)章节来了解更多的实现细节。

## 关联子查询

对于关联子查询而言，由于内层的子查询引用外层查询的列，子查询需要对外层查询得到的每一行都执行一遍，也就是说假设外层查询得到一千万的结果，那么子查询也会被执行一千万次，这会导致查询需要消耗更多的时间和资源。

因此在处理过程中，TiDB 会尝试对[关联子查询去关联](/correlated-subquery-optimization.md)，以从执行计划层面上提高查询效率。

例如，假设想要查找那些大于其它相同性别作家的平均年龄的的作家，SQL 语句可以这样写：

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

TiDB 在处理该 SQL 语句是会将其改写为等价的 Join 查询：

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

作为最佳实践，在实际开发当中，建议在明确知道有更好的等价写法时，尽量避免通过关联子查询来进行查询。

## 扩展阅读

- [子查询相关的优化](/subquery-optimization.md)
- [关联子查询去关联](/correlated-subquery-optimization.md)
- [TiDB 中的子查询优化技术](https://tidb.net/blog/b997a44c)
