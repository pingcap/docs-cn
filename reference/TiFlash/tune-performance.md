# TiFlash 性能调优
本文介绍了使 TiFlash 性能达到最优的几种方式，主要包括规划机器资源、调整 TiDB 参数、配置 TiKV Region 个数和大小等。

## 资源规划
对于希望节省机器资源，并且完全没有隔离要求的场景，可以使用 TiKV 和 TiFlash 联合部署。请为 TiKV 与 TiFlash 分别留够资源，并且不要共享磁盘。

## TiDB 相关参数调优
对于 AP / TiFlash 专属的 TiDB 节点请调大读取并发数 tidb_distsql_scan_concurrency 到 80：  
```
set @@tidb_distsql_scan_concurrency = 80
```
开启聚合推过 JOIN 优化：
```
set @@tidb_opt_agg_push_down = 1
```
## Region 大小的影响
Region 个数和大小会对 TiFlash 性能有一定的影响，过多的小 Region 将会对 TiFlash 性能带来多达数倍的降速。在以分析查询为主的使用场景，推荐使用 192M 大小的 Region Size，并且开启 Region Merge 以保证自动合并运行时产生的小 Region。
集群用 ansible 部署
在  roles/tikv/vars/default.yml 文件中添加如下配置并重启集群完成 Region Size 修改。
```
coprocessor:
region-max-size: "288MiB"
region-split-size: "192MiB"
region-max-keys:  2880000
region-split-keys:  1920000
```
在  roles/pd/vars/default.yml 文件中添加如下配置可以开启 Region Merge。
也可以直接通过 pd-ctl 的 config set <config-name> 命令设置。
 ```
schedule: 
max-merge-region-size: 20 # 合并 20M 以下的 region
max-merge-region-keys: 200000 # 合并 20000 keys 以下的 region
split-merge-interval: "1h"
merge-schedule-limit: 8 # 控制 merge 速度，设为 0 将关闭 region merge
 ```
非 ansible 部署
在  tikv.toml 文件中添加如下配置并重启集群完成 Region Size 修改。
```
[coprocessor]
region-max-size = "288MiB"
region-split-size = "192MiB"
region-max-keys = 2880000
region-split-keys = 1920000
```
在 pd.toml 文件中添加如下配置可以开启 Region Merge。也可以直接通过 pd-ctl 的 config set <config-name> 命令设置。
```
[schedule]
max-merge-region-size = 20
max-merge-region-keys = 200000
split-merge-interval = "1h"
merge-schedule-limit = 8
```
