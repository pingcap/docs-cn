---
title: CALIBRATE RESOURCE
summary: TiDB 数据库中 CALIBRATE RESOURCE 的使用概况。
---

# `CALIBRATE RESOURCE`

`CALIBRATE RESOURCE` 语句用于预估并输出当前集群的 [`Request Unit (RU)`](/tidb-resource-control.md#什么是-request-unit-ru) 的容量。

## 语法图

```ebnf+diagram
CalibrateResourceStmt ::= 'CALIBRATE' 'RESOURCE'
``` 

## 权限

执行此命令依赖如下配置和权限：

- [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 需要处于开启状态
- 需要拥有 `SUPER` 或者 `RESOURCE_GROUP_ADMIN` 权限
- 需要拥有 `METRICS_SCHEMA` 库下所有表的 `SELECT` 权限

## 示例

```sql
CALIBRATE RESOURCE;
+-------+
| QUOTA |
+-------+
| 68569 |
+-------+
1 row in set (0.03 sec)
```

> **注意：**
>
> 集群 RU 的容量会随集群的拓扑结构和各个组件软硬件配置的变化而变化，每个集群实际能消耗的 RU 还与实际的负载相关。此预估值仅供参考，可能会与实际的最大值存在偏差。
