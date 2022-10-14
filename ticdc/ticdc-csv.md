---
title: TiCDC CSV Protocol
summary: 了解 TiCDC CSV Protocol 的概念和使用方法。
---

# TiCDC CSV Protocol

## 使用 CSV
[//]: 举例说明如何使用 csv

## 数据格式定义

Col1: The operation-type indicator: `I`, `D`, `U`; `I` means INSERT, `U` means UPDATE, `D` means DELETE.
Col2: Table name, the name of the source table.
Col3: Schema name, the name of the source schema.
Col4: Commit TS, the commit-ts of the source txn. The existence of this column can be configured.
Col5-n: one or more columns that represent the data to be changed.


## 数据类型映射
[//]: 描述 Data type mapping

## DDL 事件
[//]: 描述 schema.json 文件以及各种数据类型细节