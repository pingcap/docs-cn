---
title: TiDB Dashboard SQL 语句分析列表页面
summary: 查看所有 SQL 语句在集群上执行情况
aliases: ['/docs-cn/dev/dashboard/dashboard-statement-list/']
---

# TiDB Dashboard SQL 语句分析执行详情页面

该页面可以查看所有 SQL 语句在集群上执行情况，常用于分析总耗时或单次耗时执行耗时较长的 SQL 语句。

在该页面中，结构一致的 SQL 查询（即使查询参数不一致）都会被归为同一个 SQL 语句，例如 `SELECT * FROM employee WHERE id IN (1, 2, 3)` 和 `select * from EMPLOYEE where ID in (4, 5)` 都属于同一 SQL 语句 `select * from employee where id in (...)`。

## 访问列表页面

可以通过以下两种方法访问 SQL 语句分析页面：

- 登录后，左侧导航条点击**SQL 语句分析**（SQL Statements）：

  ![访问](/media/dashboard/dashboard-statement-access.png)

- 在浏览器中访问 <http://127.0.0.1:2379/dashboard/#/statement>（将 `127.0.0.1:2379` 替换为实际 PD 实例地址和端口）。

SQL 语句分析页面所展示的所有数据都来自于 TiDB Statement 系统表，参见 [Statement Summary Tables](/statement-summary-tables.md) 文档了解该系统表的详细情况。

### 修改列表过滤条件

页面顶部可修改显示的时间范围、按执行 SQL 所在数据库进行过滤，或按 SQL 类型进行过滤，如下所示。默认显示最近一个收集周期（默认最近 30 分钟）内的所有 SQL 语句执行情况。

![修改过滤条件](/media/dashboard/dashboard-statement-filter-options.png)

### 显示其他字段

页面顶部**选择列**（Columns）选项中可选择显示更多列，可将鼠标移动到列名右侧的 (i) 图标处查看列的说明：

![选择列](/media/dashboard/dashboard-statement-columns-selector.png)

### 修改列表排序依据

列表默认以**累计耗时**（Total Latency）从高到低进行排序，点击不同的列标题可以修改排序依据或切换排序顺序：

![修改列排序](/media/dashboard/dashboard-statement-change-order.png)

### 修改数据收集设置

在列表页面，点击顶部右侧的**设置**（Settings）按钮，即可对 SQL 语句分析功能进行设置：

![设置入口](/media/dashboard/dashboard-statement-setting-entry.png)

点击后设置界面如下图所示：

![设置](/media/dashboard/dashboard-statement-settings.png)

在设置中可以选择关闭或开启 SQL 语句分析功能。在开启 SQL 语句分析功能时可以修改以下选项：

  - 数据收集周期：默认 30 分钟，每次进行 SQL 语句分析的时间长度。SQL 语句分析功能每次对一段时间范围内的所有 SQL 语句进行汇总统计，如果这个时间范围过长，则统计的粒度粗，不利用定位问题；如果太短，则统计的粒度细，方便定位问题，但会导致在相同的数据保留时间内产生更多的记录，产生更多的内存占用。因此需要根据实际情况调整，在需要定位问题时适当地将值调低。
  
  - 数据保留时间：默认 1 天，统计信息保留的时间，超过这个时间的数据会被从系统表中删除。

参见 [Statement Summary Tables 参数设置](/statement-summary-tables.md#参数配置) 文档了解详细情况。

> **注意：**
>
> 由于 Statement 系统表只存放在内存中，关闭此功能后，系统表中的数据会将清空。
>
> 数据收集周期和保留时间的值会影响内存占用，因此建议根据实际情况调整，保留时间不宜设置过大。

## 下一步

阅读[查看执行详情](/dashboard/dashboard-statement-details.md)章节了解如何进一步查看 SQL 语句的详细执行情况。
