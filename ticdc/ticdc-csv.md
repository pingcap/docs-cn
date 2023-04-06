---
title: TiCDC CSV Protocol
summary: 了解 TiCDC CSV Protocol 的概念和使用方法。
---

# TiCDC CSV Protocol

当使用云存储服务作为下游 sink 时，你可以使用 CSV 格式将 DML 事件发送到下游云存储服务。

> **警告：**
>
> 在 enable-old-value = true 时，CSV 格式无法输出更新事件的旧值。
>
> 具体原因请参考 [TiCDC 在开启 Old Value 功能后更新事件格式有何变化？](/ticdc/ticdc-faq.md#%E5%AF%B9%E4%BA%8E%E9%9D%9E%E6%9C%89%E6%95%88%E7%B4%A2%E5%BC%95%E5%88%97%E7%9A%84%E6%9B%B4%E6%96%B0%E4%BA%8B%E4%BB%B6%E5%92%8C%E6%9C%89%E6%95%88%E7%B4%A2%E5%BC%95%E5%88%97%E7%9A%84%E6%9B%B4%E6%96%B0%E4%BA%8B%E4%BB%B6%E8%A2%AB%E8%BE%93%E5%87%BA%E4%B8%BA%E6%9B%B4%E6%96%B0%E4%BA%8B%E4%BB%B6%E7%9A%84%E6%83%85%E5%86%B5cloud-storage-sink-%E7%9A%84-csv-%E6%A0%BC%E5%BC%8F%E6%97%A0%E6%B3%95%E6%AD%A3%E7%A1%AE%E7%9A%84%E8%BE%93%E5%87%BA%E6%97%A7%E5%80%BC)。

## 使用 CSV

使用 CSV 时的配置样例如下所示：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="csv-test" --sink-uri="s3://bucket/prefix" --config changefeed.toml
```

`changefeed.toml` 文件内容如下：

```toml
[sink]
protocol = "csv"
terminator = "\n"

[sink.csv]
delimiter = ','
quote = '"'
null = '\N'
include-commit-ts = true
```

## 数据保存的事务性约束

- 单个 CSV 文件中后一行数据的 commit-ts 大于等于前一行数据的 commit-ts。
- 单表的同一事务不会存储在不同的 CSV 文件中。
- 相同事务涉及的不同表会存储在不同的 CSV 文件中。

## 数据存储路径结构

关于数据存储路径结构的更多信息，请参考[同步数据到存储服务](/ticdc/ticdc-sink-to-cloud-storage.md#存储路径组织结构)。

## 数据格式定义

CSV 文件中，单行的每一列定义如下：

- 第一列：DML 操作指示符，取值包括 `I`、`U` 和 `D`。`I` 表示 `INSERT`，`U` 表示 `UPDATE`，`D` 表示 `DELETE`。
- 第二列：表名。
- 第三列：库名。
- 第四列：`commit ts`，即原始事务的 commit ts。该列为可选配置。
- 第五列至最后一列：变更数据的列，可为一列或多列。

假设某张表 `hr.employee` 的定义如下：

```sql
CREATE TABLE `employee` (
  `Id` int NOT NULL,
  `LastName` varchar(20) DEFAULT NULL,
  `FirstName` varchar(30) DEFAULT NULL,
  `HireDate` date DEFAULT NULL,
  `OfficeLocation` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

该表上的 DML 事件以 CSV 格式存储后如下所示：

```
"I","employee","hr",433305438660591626,101,"Smith","Bob","2014-06-04","New York"
"U","employee","hr",433305438660591627,101,"Smith","Bob","2015-10-08","Los Angeles"
"D","employee","hr",433305438660591629,101,"Smith","Bob","2017-03-13","Dallas"
"I","employee","hr",433305438660591630,102,"Alex","Alice","2017-03-14","Shanghai"
"U","employee","hr",433305438660591630,102,"Alex","Alice","2018-06-15","Beijing"
```

## 数据类型映射

| MySQL 类型                                                          | CSV 类型  | 示例                             | 描述                            |
|-------------------------------------------------------------------|---------|--------------------------------|-------------------------------|
| `BOOLEAN`/`TINYINT`/`SMALLINT`/`INT`/`MEDIUMINT`/`BIGINT`         | Integer | `123`                          | -                             |
| `FLOAT`/`DOUBLE`                                                  | Float   | `153.123`                      | -                             |
| `NULL`                                                            | Null    | `\N`                           | -                             |
| `TIMESTAMP`/`DATETIME`                                            | String  | `"1973-12-30 15:30:00.123456"` | 格式：`yyyy-MM-dd HH:mm:ss.%06d` |
| `DATE`                                                            | String  | `"2000-01-01"`                 | 格式：`yyyy-MM-dd`               |
| `TIME`                                                            | String  | `"23:59:59"`                   | 格式：`HH:mm:ss`                 |
| `YEAR`                                                            | Integer | `1970`                         | -                             |
| `VARCHAR`/`JSON`/`TINYTEXT`/`MEDIUMTEXT`/`LONGTEXT`/`TEXT`/`CHAR` | String  | `"test"`                       | 以 UTF-8 编码输出                  |
| `VARBINARY`/`TINYBLOB`/`MEDIUMBLOB`/`LONGBLOB`/`BLOB`/`BINARY`    | String  | `"6Zi/5pav"`                   | 以 Base64 编码输出                 |
| `BIT`                                                             | Integer | `81`                           | -                             |
| `DECIMAL`                                                         | String  | `"129012.1230000"`             | -                             |
| `ENUM`                                                            | String  | `"a"`                          | -                             |
| `SET`                                                             | String  | `"a,b"`                        | -                             |
