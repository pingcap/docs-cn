# TiFlash 集群运维
## TiFlash 版本查看
假设 TiFlash 的二进制文件名为 `tiflash`，则通过 `./tiflash version` 方式可以获取 TiFlash 版本。但是 tiflash 的运行依赖于动态库 `libtiflash_proxy.so`，因此需要将包含动态库 `libtiflash_proxy.so` 的目录路径添加到环境变量 `LD_LIBRARY_PATH` 后，上述命令才能正常执行。例如，当 `tiflash` 和 `libtiflash_proxy.so` 在同一个目录下时，切换到该目录后，可以通过该命令查看 TiFlash 版本：`LD_LIBRARY_PATH=./ ./tiflash version`
在 TiFlash 的 log 中也可以查看版本。

## TiFlash 下线方法
注意：下线与缩容不同，下线 TiFlash 并不会在 Ansible 中删除这个节点，而仅仅是安全地关闭这个进程。

下线 TiFlash 节点的步骤如下：

如果该 tiflash 集群剩余节点数大于等于所有数据表的最大副本数，直接进行第 4 步；
在 tidb 客户端中针对所有副本数大于集群剩余 tiflash 节点数的表执行：
```
alter table <db-name>.<table-name> set tiflash replica 0；
```
等待相关表的 tiflash 副本被删除（按照文档中“查看表同步进度”一节操作，查不到相关表的同步信息时即为副本被删除）；
在 pd-ctl 中输入 store 命令，查看 tiflash  对应的 store id；（关于pd-ctl 的使用参考官网手册）
在 pd-ctl 中输入 store delete <store_id>，其中 <store_id> 为上一步查到的 tiflash 对应的 store id;
等待 tiflash 对应的 store 消失或者 state_name 变成 Tomestone 再关闭 tiflash 进程；

注意：
如果在集群中所有的 tiflash 节点停止运行之前，没有取消所有同步到 tiflash 的表，则需要手动在 pd 中清除同步规则（发送 DELETE 请求 `http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/<rule_id>`，rule_id 是需要清除的 rule 的 id），否则无法成功完成 tiflash 节点的下线。
## TiFlash 故障处理
本节介绍了一些 TiFlash 常见问题、原因及解决办法。
### TiFlash 副本始终处于不可用状态

该问题一般由于配置错误或者环境问题导致 TiFlash 处于异常状态，可以先通过以下步骤定位问题组件；
检查 PD 是否按照安装部署一节开启 Placement Rules 功能；
```
echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
```
应该看到 `"enable-placement-rules": "true"`
检查 TiFlash 进程是否正常；
通过 pd-ctl 查看 TiFlash proxy 状态是否正常；
```
echo "store" | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
```
store.labels 中含有 `{"key": "engine", "value": "tiflash"}` 信息的为 TiFlash proxy
查看 pd buddy 是否正常打印 log (log 路径的对应配置项 [flash.flash_cluster]log 设置的值，默认为 TiFlash 配置文件配置的 tmp 目录下）；
检查 PD 配置的 max-replicas 是否小于等于集群 TiKV 节点数，若 max-replicas 超过 TiKV 节点数，则 PD 不会向 TiFlash 同步数据；
```
echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
```
确认 "max-replicas" 参数值
检查 TiFlash 节点对应 store 所在机器剩余的磁盘空间是否充足，默认情况下当磁盘剩余空间小于该 store 的 capacity 的 20%（通过 low-space-ratio 参数控制） 时，PD 不会向 TiFlash 调度数据。
### TiFlash 查询时间不稳定，同时 error log 中打印出大量的 Lock Exception

该问题是由于集群中存在大量写入，导致 TiFlash 查询时遇到锁并发生查询重试，可以通过在 TiDB 中将查询时间戳设置为 1 秒前（例如：`set @@tidb_snapshot=412881237115666555;`），来减小 TiFlash 查询碰到锁的可能性，从而减轻查询时间不稳定的程度。
### 部分查询返回 Region Unavailable 的错误
如果在 TiFlash 上的负载压力过大，会导致 TiFlash 数据同步落后，部分查询可能会返回 `Region Unavailable` 的错误，在这种情况下可以通过增加 TiFlash 节点数分担负载压力。
### 数据文件损坏
可依照如下步骤进行处理：

参照 “TiFlash 下线方法” 一节下线对应的 TiFlash 节点；
清除该 TiFlash 节点的相关数据；
重新在集群中部署 TiFlash 节点。
## TiFlash 重要 Log 介绍
```
[ 23 ] <Information> KVStore: Start to persist [region 47, applied: term 6 index 10]，在 TiFlash 中看到类似 log 代表数据开始同步；（log 开头方括号内的数字代表线程号，下同）
[ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handling DAG request，该 log 代表 TiFlash 开始处理一个 Coprocessor 请求；
[ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handle DAG request done，该 log 代表 TiFlash 完成 Coprocessor 请求的处理；
```
找到一个 Coprocessor 请求的开始或者结束，可以通过 log 前面打印的线程号找到该 Coprocessor 请求的其他相关 log；
## TiFlash 系统表
information_schema.tiflash_replica

| 列名          | 含义                |
|---------------|---------------------|
| TABLE_SCHEMA  | 数据库名            |
| TABLE_NAME    | 表名                |
| TABLE_ID      | 表 ID               |
| REPLICA_COUNT | TiFlash 副本数      |
| AVAILABLE     | 是否可用（0/1）     |
| PROGRESS      | 同步进度 [0.0 ~1.0] |

