---
title: TiDB 2.0.11 Release Notes
category: Releases
aliases: ['/docs/releases/2.0.11/']
---

# TiDB 2.0.11 Release Notes

On January 03, 2019, TiDB 2.0.11 is released. The corresponding TiDB Ansible 2.0.11 is also released. Compared with TiDB 2.0.10, this release has great improvement in system compatibility and stability.

## TiDB

- Fix the issue that the error is not handled properly when PD is in an abnormal condition [#8764](https://github.com/pingcap/tidb/pull/8764)
- Fix the issue that the `Rename` operation on a table in TiDB is not compatible with that in MySQL [#8809](https://github.com/pingcap/tidb/pull/8809)
- Fix the issue that the error message is wrongly reported when the `ADMIN CHECK TABLE` operation is performed in the process of executing the `ADD INDEX` statement [#8750](https://github.com/pingcap/tidb/pull/8750)
- Fix the issue that the prefix index range is incorrect in some cases [#8877](https://github.com/pingcap/tidb/pull/8877)
- Fix the panic issue of the `UPDATE` statement when columns are added in some cases [#8904](https://github.com/pingcap/tidb/pull/8904)

## TiKV

- Fix two issues about Region merge
[#4003](https://github.com/tikv/tikv/pull/4003), [#4004](https://github.com/tikv/tikv/pull/4004)
