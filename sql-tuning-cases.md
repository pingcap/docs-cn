---
title: SQL 优化案例
summary: 了解 TiDB 中常见的 SQL 优化方法
---

# 复合索引策略

1. 以下分页查询的执行时间为 12.2 秒，从数据库获取 10 行，执行效率低下。
2. 如果阅读执行计划：
   1. 阅读执行计划，通过indexLoopKUp 算子访问数据，IndexFullScan_20 算子对主键索引 ENCODEDKEY 进行索引全扫描，确保扫描数据有序 `keep order:true`, 因为需要对整个索引全部进行扫描，返回了 662258 行，花费了12.2秒
   2. 接着通过└─TableRowIDScan_21 和 └─Selection_22 进行回表和 `accountstate` 字段上的过滤, └─Selection_22 算子返回 11999 行。通过主键索引扫描之后还需要回表，说明该表不是 clustered index。如果使用 clustered index，则可避免回表操作。
   3. 后续通过 └─Projection_24 算子之后数据下降为 4096 行，└─Projection_24 之后下降为 2048 行，
   4. 通过 limits 算子，下降为 10 行


{{< copyable "sql" >}}
```sql
SELECT
  `encodedkey`
FROM
  `savingsaccount`
WHERE
  `accountstate` IN ('ACTIVE', 'APPROVED')
ORDER BY
  `encodedkey`
LIMIT
    10;
```

{{< copyable "sql" >}}

```sql
	id                         	task     	estRows	operator info                                                                         	actRows	execution info                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              	memory   	disk
	Projection_7               	root     	10     	bankingbaseline.savingsaccount.encodedkey                                             	10     	time:12.2s, loops:2, Concurrency:OFF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        	804 Bytes	N/A
	└─Limit_13                 	root     	10     	offset:1230, count:10                                                                 	10     	time:12.2s, loops:2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         	N/A      	N/A
	  └─Projection_24          	root     	1240   	bankingbaseline.savingsaccount.encodedkey, bankingbaseline.savingsaccount.accountstate	2048   	time:12.2s, loops:2, Concurrency:5                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          	191.7 KB 	N/A
	    └─IndexLookUp_23       	root     	1240   	                                                                                      	4096   	time:12.2s, loops:4, index_task: {total_time: 12.2s, fetch_handle: 12.2s, build: 11ms, wait: 67.5µs}, table_task: {total_time: 68.4ms, num: 8, concurrency: 5}                                                                                                                                                                                                                                                                                                                                                             	18.7 MB  	N/A
	      ├─IndexFullScan_20   	cop[tikv]	1251.65	table:savingsaccount, index:PRIMARY(ENCODEDKEY), keep order:true                      	662258 	time:12.2s, loops:112, cop_task: {num: 1, max: 12.2s, proc_keys: 662258, tot_proc: 12.2s, tot_wait: 16ms, rpc_num: 1, rpc_time: 12.2s, copr_cache_hit_ratio: 0.00}, tikv_task:{time:492ms, loops:651}, scan_detail: {total_process_keys: 662258, total_process_keys_size: 86755798, total_keys: 668559, rocksdb: {delete_skipped_count: 0, key_skipped_count: 667658, block: {cache_hit_count: 1276, read_count: 0, read_byte: 0 Bytes}}}                                                                                   	N/A      	N/A
	      └─Selection_22       	cop[tikv]	1240   	in(bankingbaseline.savingsaccount.accountstate, "ACTIVE", "APPROVED")                 	11999  	time:50.7ms, loops:22, cop_task: {num: 8, max: 13.4ms, min: 2.37ms, avg: 6.03ms, p95: 13.4ms, max_proc_keys: 4096, p95_proc_keys: 4096, tot_proc: 40ms, rpc_num: 8, rpc_time: 48.1ms, copr_cache_hit_ratio: 0.00}, tikv_task:{proc max:12ms, min:0s, p80:8ms, p95:12ms, iters:40, tasks:8}, scan_detail: {total_process_keys: 11999, total_process_keys_size: 12418965, total_keys: 18307, rocksdb: {delete_skipped_count: 16, key_skipped_count: 35685, block: {cache_hit_count: 1776, read_count: 0, read_byte: 0 Bytes}}}	N/A      	N/A
	        └─TableRowIDScan_21	cop[tikv]	1251.65	table:savingsaccount, keep order:false                                                	11999  	tikv_task:{proc max:12ms, min:0s, p80:8ms, p95:12ms, iters:40, tasks:8}                                                                                                                                                                                                                                                                                                                                                                                                                                                     	N/A      	N/A
```

3. 优化思路
   1. 现有表结构只存在 ENCODEDKEY 字段，针对该 SQL，可以新建覆盖索引 (accountstate, ENCODEDKEY), 前导列为 accountstate 可以避免访问无效数据，第二列 ENCODEDKEY 可以避免排序操作，只需要分别扫描 accountstate 为 `ACTIVE` 和 `APPROVED` 两种状态的前 10 条记录。
{{< copyable "sql" >}}
```sql
alter table bankingbaseline.savingsaccount add index (accountstate, ENCODEDKEY);
   ```

4. 优化效果
   
{{< copyable "sql" >}}
```sql
alter table bankingbaseline.savingsaccount add index (accountstate, ENCODEDKEY);
   ```

# 复合索引策略


