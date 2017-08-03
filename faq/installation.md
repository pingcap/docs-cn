---
title: 部署安装
category: faq-operations
---

# 部署安装

## 为什么修改了 TiKV/PD 的 toml 配置文件，却没有生效？

如果要使用配置文件，请设置 TiKV/PD 的 --config 参数，TiKV/PD 默认情况下不会读取配置文件。


## 我的数据盘是 xfs 且不能更改怎么办？
因为 rocksdb 在 xfs 和某些 linux kernel 中有 [bug](https://github.com/facebook/rocksdb/pull/2038)。所以不推荐使用 xfs 作为文件系统。

目前有个测试脚本，在 tikv 的部署盘运行，如果结果是 5000，可以尝试使用，但是上生产不建议。

	#!/bin/bash
	touch tidb_test
	fallocate -n -o 0 -l 9192 tidb_test
	printf 'a%.0s' {1..5000} > tidb_test
	truncate -s 5000 tidb_test
	fallocate -p -n -o 5000 -l 4192 tidb_test
	LANG=en_US.UTF-8 stat tidb_test |awk 'NR==2{print $2}'
	rm -rf tidb_test
	
## chrony 能满足时间同步的要求 ？
可以，只要能让 pd 机器时间同步就行。