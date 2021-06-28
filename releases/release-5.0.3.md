---
title: TiDB 5.0.3 Release Notes
---

# TiDB 5.0.3 Release Notes

发版日期：2021 年 6 月 30 日

TiDB 版本：5.0.3

## 兼容性更改

## 新功能

## 提升改进

+ TiDB

  - 支持将 TopN 算子下推到 TiFlash。 [#25162](https://github.com/pingcap/tidb/pull/25162)
  - 支持将内置函数 `json_unquote()` 下推到 TiKV。 [#25720](https://github.com/pingcap/tidb/pull/25720)
  - 支持在 Dual 表上移除 Union 算子的优化。 [#25614](https://github.com/pingcap/tidb/pull/25614)
  - 支持将内置函数 `replace()` 下推到 TiFlash。 [#25565](https://github.com/pingcap/tidb/pull/25565)
  - 支持将内置函数 `unix_timestamp()`,`concat()`,`year()`,`day()`,`datediff()`,`datesub()`,`castTimeAsString()`,`concat_ws()` 下推到 TiFlash。 [#25564](https://github.com/pingcap/tidb/pull/25564)
  - 修改聚合算子的代价常数。 [#25241](https://github.com/pingcap/tidb/pull/25241)
  - 支持将 Limit 算子下推到 TiFlash。 [#25159](https://github.com/pingcap/tidb/pull/25159)
  - 支持将内置函数 `str_to_date()` 下推到 TiFlash。 [#25148](https://github.com/pingcap/tidb/pull/25148)
  - 允许 MPP outer join 根据表行数选择 build table。 [#25142](https://github.com/pingcap/tidb/pull/25142)
  - 支持将内置函数 `left()`,`right()`,`abs()` 下推到 TiFlash。 [#25133](https://github.com/pingcap/tidb/pull/25133)
  - 支持将 broadcast cartesian join 下推到 TiFlash。 [#25106](https://github.com/pingcap/tidb/pull/25106)
  - 支持将 Union All 算子下推到 TiFlash。 [#25051](https://github.com/pingcap/tidb/pull/25051)
  - 支持 MPP 查询任务按 region 均衡到不同 TiFlash 节点上。 [#24724](https://github.com/pingcap/tidb/pull/24724)
  - 支持执行 MPP 查询后将缓存中过时的 region 无效化。 [#24432](https://github.com/pingcap/tidb/pull/24432)
## Bug 修复

+ TiDB

    - 禁止在 stale read 中设置一个未来的读时间戳。[#25761](https://github.com/pingcap/tidb/pull/25761)
    - 修复 ODBC 类常数（例如 `{d '2020-01-01'}`）不能被用作表达式的问题。 [#25577](https://github.com/pingcap/tidb/pull/25577)
    - 修复 `SELECT DISTINCT` 被转化为 batch get 而导致结果不正确的问题。 [#25533](https://github.com/pingcap/tidb/pull/25533)
    - 修复无法触发将查询从 TiFlash 回退到 TiKV 的问题。 [#24600](https://github.com/pingcap/tidb/pull/24600)
    - 修复在检查 `only_full_group_by` 时的 index-out-of-range 错误。 [#24016](https://github.com/pingcap/tidb/pull/24016)
