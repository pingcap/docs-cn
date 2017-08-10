---
title: TiDB 运维文档
category: deployment
---

# TiDB 运维文档

* [概述](#概述)
* [日常巡检指标监控](#日常巡检指标监控)
   * [Grafana 监控指标说明](#grafana-监控指标说明)
* [告警说明](#告警说明)
   * [alert.rule 告警说明](#alertrule-告警说明)
   * [告警处理](#告警处理)
      * [TiDB_query_duration TiDB 慢查询](#tidb_query_duration--tidb-慢查询)
      * [memery_abnormal](#memery_abnormal)
      * [TiDB_TiKVclient_region_err](#tidb_tikvclient_region_err)
      * [Drainer_Disk_space_not_enough](#drainer_disk_space_not_enough)
      * [Drainer_status_timeout](#drainer_status_timeout)
* [运维相关信息与运维操作](#运维相关信息与运维操作)
   * [TiDB 集群默认目录及端口](#tidb-集群默认目录及端口)
      * [TiDB 服务默认端口](#tidb-服务默认端口)
      * [TiDB 服务默认目录](#tidb-服务默认目录)
   * [ansible 运维操作](#ansible-运维操作)
      * [滚动升级](#滚动升级)
      * [集群扩容](#集群扩容)
   * [TiDB 简单运维操作](#tidb-简单运维操作)
      * [crontab 清理日志](#crontab-清理日志)
      * [pd-ctl 使用技巧](#pd-ctl-使用技巧)
         * [查询/删除 PD 成员](#查询删除-pd-成员)
         * [查询/修改 PD 配置信息](#查询修改-pd-配置信息)
         * [查询 region store 信息](#查询-region--store-信息)
   * [常见FAQ](#常见faq)
      * [TiDB 服务相关](#tidb-服务相关)
      * [如何 kill tidb session](#如何-kill-tidb-session)
      * [查看当时运行的 ddl job](#查看当时运行的-ddl-job)
      * [备份恢复](#备份恢复)
      * [drainer 服务相关](#drainer-服务相关)
      * [TiDB LB 选用与设置](#tidb-lb-选用与设置)

## 概述

撰写此文档方便运维同学对 TiDB 的日常运维常见问题进行处理。  
对于 TiDB 日常运维分为日常巡检与告警处理。  

下面就各个部分进行详细的说明：  


## 日常巡检指标监控

TiDB 使用开源时序数据库 Prometheus 作为监控和性能指标信息存储方案，使用 Grafana 作为可视化组件进行展示。

Grafana 是一个开源的 metric 分析及可视化系统。我们使用 Grafana 来展示 TiDB 的各项性能指标 。

所以日常巡检都是围绕着 Grafana 为中心。

### Grafana 监控指标说明

> 目前 Grafana dashboard 整体分为四个dashboard，node_export，PD，TiDB，TiKV。 内容较多，主要在于全面了解整个集群各个组件	的运行情况。  
> 针对对于日常运维，我们挑选出一些重要的 metrics 指标放在 overview 页面，方便日常运维人员观察集群组件(PD,TiDB,TiKV)使用状态以及集群使用状态 。  
> 以下为 overview dashboard 说明。  

####PD运行参数

服务	|	监控对象	|	说明	|	正常范围
---	|	---	|	---	|	---
PD	|	Storage Capacity	|	TiDB 集群总可用数据库空间大小	|	
PD	|	Current Storage Size	|	TiDB 集群目前已用数据库空间大小	|	
PD	|	Store Status  -- up store	|	TiKV 正常节点数量	|	
PD	|	Store Status  -- down store	|	TiKV 异常节点数量	|	如果大于0，证明有节点不正常
PD	|	Store Status  -- offline store	|	手动执行下线操作 TiKV 节点数量	|	
PD	|	Store Status  -- Tombstone store	|	下线成功的 TiKV 节点数量	|	
PD	|	Current storage usage	|	TiKV 集群存储空间占用率	|	超过 80% 应考虑添加 TiKV 节点
PD	|	leader balance ratio	|	leader ratio 最大的节点与最小的节点的差	|	均衡状况下一般小于 5%，节点重启时会比较大
PD	|	region balance ratio	|	region ratio 最大的节点与最小的节点的差	|	均衡状况下一般小于 5%，新增/下线节点时会比较大
PD	|	number of region	|	region数量分布	|
PD	|	99% completed-cmds-duration-seconds	|	99% pd-server 请求完成时间	|	小于 5ms
PD	|	average completed-cmds-duration-seconds	|	pd-server 请求平均完成时间	|	小于 50ms

####TiDB运行参数

服务	|	监控对象	|	说明	|	正常范围
---	|	---	|	---	|	---
TiDB	|	connection count	  |	从业务服务器连接到数据库的连接数	|	和业务相关。但是如果连接数发生跳变，需要查明原因。比如突然掉为0，可以检查网络是否中断；如果突然上涨，需要检查业务。
TiDB	|	handle-requests-duration-seconds	|	请求 PD 获取 TSO 响应时间	|	小于100ms
TiDB	|	TiDB server QPS	|	集群的请求量	|	这个和业务相关
TiDB	|	statement count	|	单位时间内不同类型语句执行的数目	|	这个和业务相关
TiDB	|	Query Duration 99th percentile	|	99% 的 query 时长	|	

####TiKV运行参数

服务	|	监控对象	|	说明	|	正常范围
---	|	---	|	---	|	---
TiKV	|	99%  & 99.99%  scheduler command duration	|	99% & 99.99% 命令执行的时长	|	99% 小于 50ms；99.99% 小于100ms
TiKV	|	99%  & 99.99% storage async_request duration	|	99% & 99.99% Raft 命令执行时间	|	99% 小于 50ms；99.99% 小于100ms
TiKV	|	server report failure message	|	发送失败或者收到了错误的 message	|	如果出现了大量的 unreachadble 的消息，表明系统网络出现了问题。如果有 store not match 这样的错误，表明收到了不属于这个集群发过来的消息
TiKV	|	Vote	|	Raft vote 的频率	|	通常这个值只会在发生 split 的时候有变动，如果长时间出现了 vote 偏高的情况，证明系统出现了严重的问题，有一些节点无法工作了
TiKV	|	95% 以及 99% coprocessor request duration	|	95% 以及 99.99%  coprocessor 执行时间	|	和业务相关，但通常不会出现持续高位的值
TiKV	|	Pending task	|	累积的任务数量	|	除了 pd worker，其他任何偏高都属于异常
TiKV	|	stall	|	RocksDB Stall 时间	|	大于 0，表明 RocksDB 忙不过来，需要注意 IO 和 CPU 了
TiKV	|	channel full	|	channel 满了，表明线程太忙无法处理	|	如果大于 0，表明线程已经没法处理了
TiKV	|	95% send-message-duration-seconds	|	95% 发送消息的时间	|	小于50ms
TiKV	|	leader/region	|	每个 TiKV 的leader/region数量	|	和业务相关


-----

## 告警说明


Prometheus 提供了多个组件供用户使用。目前，我们使用 Prometheus Server，来收集和存储时间序列数据。  
Client 代码库，在程序中定制需要的 Metric 。  
Push GateWay 来接收 Client Push 上来的数据，统一供 Prometheus 主服务器抓取。  
以及 AlertManager 来实现报警机制，目前生产环境告警会发送到我们 slack 工具上。  

其结构如下图：  
 
![ Prometheus ](https://github.com/pingcap/docs-cn/blob/master/media/prometheus-in-tidb.png?raw=true)

根据 TiDB 的业务，我们在 Prometheus 定制了一些业务告警规则(`alert.rule`),并设定了一些默认阈值，上线前可以根据而业务自动定制 alert.rule 信息。  

以下是默认 alert.rule 规则说明

### alert.rule 告警说明

服务	|	ALERT 	|	说明	|	metrics
---	|	---	|	---	|	---
TiDB	|	load_schema_fail	|	检测 TiDB  loader schema tableinfo 执行状态，如果出现 failed 则告警，如果状态 failed，TiDB 进入不可用状态。(当执行完 DDL，TiDB 会有 loader schema tableinfo 操作，加载最新表信息	|	rate(TiDB_domain_load_schema_total{type='failed'}[1m]) > 0
TiDB	|	load_shema_latency	|	TiDB loader schema tablesinfo 时间超过5秒，一般情况是 TiKV 主机变慢了，可以 观察监控 TiDB--Schema Load 组下面三个面板	|	histogram_quantile(1, rate(TiDB_domain_load_schema_duration_bucket[5m])) > 5
TiDB	|	memery_abnormal	|	监控 TiDB 服务内存使用率(主要防止出现 TiDB OOM 现象，如果 TiDB 内存占用超过阈值需要排查相关 TiDB 进程 是否在执行 ddl 或者慢查询)	|	go_memstats_heap_inuse_bytes{job='TiDB'} > 1000000000
TiDB	|	TiDB_query_duration	|	99% query 请求时间，当有超过 1s 的慢查询告警	|	histogram_quantile(0.99, sum(rate(TiDB_server_handle_query_duration_seconds_bucket[1m])) by (le, instance)) > 1
TiDB	|	TiDB_TiKVclient_region_err	|	TiKV 运行出现 server is busy 次数，出现这个告警，说明目前 TiKV 节点比较繁忙了，需要检查集群状态(是否在调度 leader/region , TiKV 节点磁盘利用率, rockdb cpu 使用率,)	|	sum(rate(TiDB_TiKVclient_region_err_total{type='server_is_busy'}[1m])) > 0
TiKV	|	TiKV_raft_process_ready	|	处理 ready 的耗时	|	sum(rate(TiKV_raftstore_raft_process_nanos_total{type='ready'}[1m])) by (type, instance) / 1000000000 > 1
TiKV	|	raft_sotre_msg	|	消息发送失败的个数	|	sum(rate(TiKV_server_report_failure_msg_total{type='unreachable'}[1m])) > 10
TiKV	|	TiKV_channel_full_total	|	TiKV 出现 channel full > 0,相关 TiKV 节点太繁忙，或者 TiKV 节点不可用状态	|	sum(rate(TiKV_channel_full_total[1m])) by (type, instance) > 0
TiKV	|	coprocessor_pending_request	|	请求太多，出现排队，	|	sum(rate(TiKV_coprocessor_pending_request[1m])) by (type,instance) > 2
TiKV	|	TiKV_scheduler_context_total	|	如果这个告警数值太大，表示目前有大量写入正在进行	|	sum(TiKV_scheduler_contex_total) by (job) > 300
TiKV	|	TiKV_thread_cpu_seconds_total	|	raftstore CPU 告警	|	rate(TiKV_thread_cpu_seconds_total{name='raftstore'}[1m]) > 0.8
TiKV	|	TiKV_thread_cpu_seconds_total	|	endpoint-pool CPU 告警	|	rate(TiKV_thread_cpu_seconds_total{name='endpoint-pool'}[1m]) > 0.9
TiKV	|	TiKV_thread_cpu_seconds_total	|	sched-worker-pool CPU 告警	|	rate(TiKV_thread_cpu_seconds_total{name='sched-worker-pool'}[1m]) > 0.9
TiKV	|	TiKV_leader_drops	|	TiKV 单节点 30s leader 数量调度情况，如果连续下降10个以上会告警。	|	delta(TiKV_pd_heartbeat_tick_total{type="leader"}[30s]) < -10
PD	|	etcd_disk_fsync	|	监控 etcd wal 写入情况，判断 etcd 是否进程退出。当 etcd 无法写入时，PD 进程会退出	|	sum(rate(etcd_disk_wal_fsync_duration_seconds_count[1m])) by (instance) == 0
Syncer	|	Syncer_status	|	Syncer binlog 同步告警，当 master 与 syncer binlog 文件大与1时告警。	|	syncer_binlog_file{node='master'} - ON(instance, job) syncer_binlog_file{node='syncer'} > 1
drainer	|	Drainer_status_timeout	|	Drainer 与线上同步时间超时1800秒告警	|	(binlog_drainer_window{instance="production-users-TiDB-1",marker="upper"} - IGNORING(marker) binlog_drainer_position{instance="production-users-TiDB-1"}) / (2 ^ 18 * 10 ^ 3) > 1800
drainer	|	Drainer_Disk_space_not_enough	|	drainer 服务磁盘告警，需要指定 drainer 主机，磁盘剩余小于150G告警	|	node_filesystem_avail{instance='10.1.102.62:9100',mountpoint='/data'}/1024/1024/1024 < 150
OS	|	Disk_space_not_enough	|	磁盘剩余空间告警，磁盘剩余空间小于30%告警	|	node_filesystem_free{fstype!~"rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs",instance=~".+",mountpoint!~"^/boo.+|/usr.+",mountpoint=~".+"} / node_filesystem_size{fstype!~"rootfs|selinuxfs|autofs|rpc_pipefs|tmpfs",instance=~".+",mountpoint!~"^/boo.+|/usr.+",mountpoint=~".+"} * 100 < 30
OS	|	Disk_IO_Utilization	|	磁盘 IO 利用率告警，大于30告警	|	sort_desc(rate(node_disk_io_time_ms[1m])/10  or irate(node_disk_io_time_ms[1m]) /10 ) 


### 告警处理

#### TiDB_query_duration && TiDB 慢查询

- 查看 Grafana TiDB dashboard，查看 `Query Duration 80th percentile` & `Average Query Duration`
	- 根据监控，可以查看到是那台 TiDB 进程正在执行 sql
- 登录相关节点查看日志
	- grep TIME_QUERY TiDB.log 
	- 查到相关 sql 语句，看是否可以进行优化
	- 查看 TiKV 是否存在热点，如磁盘 read 利用率高(iostat)
- 登录TiDB ，使用 `show processlist` 可以看到执行语句
	- 使用 `kill TiDB pid` 可杀死相应进程， pid 为 `show processlist` 查到的sql id。


#### memery_abnormal

- 查看 TiDB dashboard , `.99 query` & `.95 query` 有没有曲线图突增
- 查看 TiDB dashboard , `Heap Memory Usage` 查看是那台TiDB机器占用内存过高
- 登录相关 TiDB ，查看日志是否有 慢查询/ddl操作

#### TiDB_TiKVclient_region_err 

- 检查 TiDB dashboard QPS 曲线图有没有突增


#### Drainer_Disk_space_not_enough

- drainer 磁盘空间不够，删除一部分空间即可

#### Drainer_status_timeout 

> 当出现此告警的时候，rainer dashboard `synchronization delay` 值会出现持续增长状态

- 检查 drainer 日志输出，根据日志输出判断问题
- drainer 上游组件影响说明
	- PD `用来获取 pump 组件信息`
		- 如果所有 PD 机器宕机，那么会出现整个 TiDB 集群不可用
	- pump `pump链接 TiDB，生成binlog，drainer 来 pump 拉 binlog 信息`
		- 注意 pump 数据磁盘空间是否写满
		- 查看日志是否还在生成 binlog 文件
	- TiDB `TiDB 进程正常退出，pump无法生成 binlog，不影响drainer；如果TiDB异常，pump无法生成 binlog，drainer 因数据一致性操作，拿不到 binlog 会异常`

-----

## 运维相关信息与运维操作

### TiDB 集群默认目录及端口

#### TiDB 服务默认端口

服务	|	变量&参数	|	说明
---| --- | --- 				
PD	|	pd_client_port: 2379	|	处理客户端请求监听 URL 列表
PD	|	pd_peer_port: 2380	|	处理其他 PD 节点请求监听 URL 列表。
TiKV	|	TiKV_port: 20160	|	TiKV 监听地址
PUMP	|	pump_port: 8250	|	PUMP 监听地址
TiDB	|	TiDB_port: 4000	|	TiDB 监听地址
TiDB	|	TiDB_status_port: 10080	|	TiDB 服务状态监听端口（监控数据）
Monitor	|	node_exporter_port: 9100	|	node_exporter 服务监听端口(主机监控)
Monitor	|	Prometheus_port: 9090	|	Promethus 服务监听端口
Monitor	|	pushgateway_port: 9091	|	PushGateway 服务监听端口
Monitor	|	Grafana_port: 3000	|	Grafana 服务监听端口( web port )


#### TiDB 服务默认目录

服务	|	变量&参数	|	说明
---| --- | --- 	
Local	|	downloads_dir: "{{ playbook_dir }}/downloads"	|	binary 下载目录
Local	|	resources_dir: "{{ playbook_dir }}/resources"	|	二进制文件目录
Local	|	fetch_log_dir: "{{ playbook_dir }}/fetch_logfile"	|	ansible获取主机fetch 信息存放位置
Deploy	|	deploy_dir = /home/TiDB/deploy	|	默认binary部署目录
Deploy	|	backup_dir: "{{ deploy_dir }}/backup"	|	检测到binary发生改变，备份binary目录
Supervise	|	status_dir: "{{ deploy_dir }}/status"	|	supervise 状态文件目录
TiKV	|	TiKV_log_dir: "{{ deploy_dir }}/log"	|	TiKV 日志目录
TiKV	|	TiKV_data_dir: "{{ deploy_dir }}/data"	|	TiKV 数据目录，TiKV --store 目录
PD	|	pd_log_dir: "{{ deploy_dir }}/log"	|	pd 日志目录
PD	|	pd_data_dir: "{{ deploy_dir }}/data.pd"	|	pd 数据目录，pd --data-dir 目录
PUMP	|	pump_socket: "{{ status_dir }}/pump.sock"	|	pump 与 TiDB 通信socket 通信文件
PUMP	|	pump_log_dir: "{{ deploy_dir }}/log"	|	pump 服务日志目录
PUMP	|	pump_data_dir: "{{ deploy_dir }}/data.pump"	|	pump binlog 日志存放目录，pump --data-dir 目录
TiDB	|	TiDB_log_dir: "{{ deploy_dir }}/log"	|	TiDB 服务日志目录
Monitor	|	node_exporter_log_dir: "{{ deploy_dir }}/log"	|	node exporter 服务日志目录
Monitor	|	pushgateway_log_dir: "{{ deploy_dir }}/log"	|	pushgataway 服务日志目录
Monitor	|	Prometheus_data_dir: "{{ deploy_dir }}/data.metrics"	|	Prometheus 监控数据存放目录，来自于下层node_export与TiDB pd TiKV服务信息
Monitor	|	Grafana_log_dir: "{{ deploy_dir }}/log"	|	Grafana 服务日志目录
Monitor	|	Grafana_data_dir: "{{ deploy_dir }}/data.Grafana"	|	Grafana 存放数据目录


### ansible 运维操作

|任务|Playbook|
|----|--------|
|启动集群|ansible-playbook start.yml|
|停止集群|ansible-playbook stop.yml|
|销毁集群|ansible-playbook unsafe_cleanup.yml| (若部署目录为挂载点，会报错，但不影响执行效果）|
|清除数据(测试用)|ansible-playbook cleanup_data.yml|
|滚动升级|ansible-playbook rolling_update.yml|
|滚动升级 TiKV|ansible-playbook rolling_update.yml --tags=TiKV|
|滚动升级除 pd 外模块|ansible-playbook rolling_update.yml --skip-tags=pd|


#### 滚动升级

> 滚动升级 TiDB 服务，滚动升级期间不影响业务运行(最小环境 ：`pd*3 、TiDB*2、TiKV*3`)  
> 远程连接权限问题，参考以上步骤( 已建立互信无需加 `-k` )

- 下载binary
  - 第一种：使用 playbook 下载最新 master binary，自动替换 binary 到`TiDB-ansible/resource/bin/`

                ansible-playbook local_prepare.yml

  - 第二种：使用 wget 下载 binary，手动替换 binary 到 `TiDB-ansible/resource/bin/`

                wget http://download.pingcap.org/TiDB-latest-linux-amd64.tar.gz

- 使用 ansible 滚动升级

> 滚动升级TiKV节点( 只升级单独服务 )

                ansible-playbook rolling_update.yml --tags=TiKV

> 滚动升级所有服务

                ansible-playbook rolling_update.yml



#### 集群扩容

使用 ansible 在原有集群基础上添加新节点（PD、TiDB、TiKV）

- 修改 inventory.ini，添加 pd、TiDB、TiKV 节点信息，要在原来的配置末尾添加
- 修改 inventory.ini 注释 ansible_become = true
	- 执行 ansible-playbook bootstrap.yml ，初始化新添加机器
- 修改 inventory.ini 取消 ansible_become = true 注释
	- 执行 ansible-playbook deploy.yml ，为新添加机器部署服务
- 如本次扩容中包含PD节点，需手动修改部分文件
	- 登录到新添加的 PD 节点，修改启动脚本  {deploy_dir}/scripts/run_pd.sh 
	- 删除 --initial-cluster="xxxx" 配置
	- 添加配置 join="http://192.168.1.101:2379"
		- 192.168.1.101 为已存在PD节点之一
	- 手动启动新节点的 PD 服务
		- {deploy_dir}/scripts/start_pd.sh  使用 pd-ctl 检查是否加入成功
			- ./pd-ctl -u "http://192.168.1.101:2379"  
				- member
- 滚动重启整个集群
	- ansible-playbook rolling_update.yml
- 查看监控检查新节点运行情况 (dashboard title)
	- PD dashboard
		- Leader Balance Ratio
	- TiKV dashboard
		- leader
		- region
	- TiDB dashboard
		- QPS


### TiDB 简单运维操作

#### crontab 清理日志

目前 tidb tikv pd 等服务日志自动按天进行切割，但是没有设置自动清理功能。  
运维人员可以使用 crontab 自行清理服务日志，比如使用以下命令，清理 3 天前的日志文件。

`find /data1/deploy/log/ -type f -cmin +4320 -exec rm -rf {} \;`  

`/data1/deploy/log/` 为 tidb 日志目录


#### pd-ctl 使用技巧

> 使用 ./pd-ctl -u "http://127.0.0.1:2379" 链接 PD 服务
> pd-ctl 使用命令行交互模式调整 tidb 集群状态信息
> 以下为运维操作简单示例，更多功能请看[ PD Control 使用说明](https://github.com/pingcap/docs-cn/blob/master/op-guide/pd-control.md )

##### 查询/删除 PD 成员

```
>> member                               // 显示所有成员的信息
{
  "members": [......]
}
>> member leader                        // 显示 leader 的信息
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete pd2                    // 下线 "pd2"
Success!
```

##### 查询/修改 PD 配置信息

```
>> config show                   //　显示 config 的信息， config show all 可以看到所有配置信息
{
  "max-snapshot-count": 3,
  "max-store-down-time": "1h",
  "leader-schedule-limit": 8,
  "region-schedule-limit": 4,
  "replica-schedule-limit": 8,
}
```

通过调整 leader-schedule-limit 可以控制同时进行 leader 调度的任务个数。 这个值主要影响 leader balance 的速度，值越大调度得越快，设置为 0 则关闭调度。 Leader 调度的开销较小，需要的时候可以适当调大

```
	>> config set leader-schedule-limit 4       // 最多同时进行 4 个 leader 调度
```

##### 查询 region & store 信息

> 查询 region 信息，当出现 region miss 或者 tidb 日志 backoff 时，可通过查找 region id 确定 tikv 节点信息

```
>> region                               //　显示所有 region 信息
{
  "count": 1,
  "regions": [......]
}

>> region 78524                             // 显示 region id 为 78524 的信息
{
  "id": 78524,
  "start_key": "dIAAAAAAAAD/N19ygAAAAAv/GqfRAAAAAAD6",
  "end_key": "dIAAAAAAAAD/N19ygAAAAAv/NE/1AAAAAAD6",
  "region_epoch": {
    "conf_ver": 19,
    "version": 102
  },
  "peers": [
    {
      "id": 78525,
      "store_id": 9
    },
    {
      "id": 78526,
      "store_id": 14
    },
    {
      "id": 78527,
      "store_id": 13
    }
  ],
  "Leader": {
    "id": 78525,
    "store_id": 9
  },
  "DownPeers": [],
  "PendingPeers": [],
  "WrittenBytes": 140081
}

```

> 查询 store 信息，每个 tikv 节点拥有一个 store id，通过 id 查到相关 tikv 节点状态

```
» store 1
{
  "store": {
    "id": 1,
    "address": "10.10.10.1:20172",  # tikv 节点信息 IP:port
    "state": 0,
    "labels": [   # tikv labels 信息
      {
        "key": "host",
        "value": "h36"
      }
    ],
    "state_name": "Up"  # tikv 节点状态
  },
  "status": {
    "store_id": 1,  	# tikv 节点 id
    "capacity": "1.9 TiB",  # 磁盘空间
    "available": "1.7 TiB", # 可用空间
    "leader_count": 266,	# store id 1 节点上 leader 数量
    "region_count": 792,	# store id 1 节点上 region 数量
    "sending_snap_count": 0,
    "receiving_snap_count": 0,
    "applying_snap_count": 0,
    "is_busy": false,
    "start_ts": "2017-07-26T17:21:18+08:00",
    "last_heartbeat_ts": "2017-08-06T13:32:33.867159016+08:00",
    "uptime": "260h11m15.867159016s"
  }
}
```

### 常见FAQ

#### TiDB 服务相关

- TiDB 出现只读，无法写入操作
	- TiDB 因为写入过大数据量进入保护模式，重启相关TiDB服务即可
- TiDB 重置所有连接
	- 重启TiDB后，即可重置所有连接
		- ansible-playbook stop.yml --tags=TiDB
		- ansible-playbook start.yml --tags=TiDB
- TiDB 出现 `backoffer.maxSleep 15000ms is exceeded`
	- 首先查看 tidb dashboard `KV Backoff Count` metrics信息
	- 如果出现 regionmiss,注意查看 tikv dashboard `region` / `check split` metrics 
- TiDB 日志出现 EXPENSIVE_QUERY
	- 优化器检测到 SQL 资源开销比较大
- TiDB 日志出现 TIME_QUERY
	- TiDB 对执行超过 300ms 的语句输出 slow log 
- TiDB 日志出现 TIME_INDEX_DOBLE
	- 先取一次索引，再从索引中拿倒相应的主键，再通过主键取一次数据

#### 如何 kill tidb session

- ddl语句跑起来之后除非出错，否则 kill 不了
- 其他语句可以通过 `show processlist` 查看到 session id 
	- 找到 session id 后, kill tidb connection id ;

#### 查看当时运行的 ddl job

- 在 TiDB 执行 `admin show ddl` 查看 
- 注意：ddl 除非是遇到错误 否则是不能取消的

#### 备份恢复

首先 TiDB 本身就是高可用构架，每条数据都有两个副本（加自己是三个）。所以如果不是非常需要备份的场景是完全 ok 的(比如金融类)。  

我们高度兼容 MYSQL ，所以直接使用 MYSQL 的备份工具 mydumper 导出数据。使用我们的 loader 工具恢复备份。  

TiDB 有自身的 binlog，可以做数据增量备份 同时每天可以用 mydumper 做一份全量，结合 tidb-binlog 就可以恢复到任意时间点的状态

#### drainer 服务相关

- drainer 日志出现 `desc = binlogger: file not found`
	- 找不到 pump binlog 文件
	- 检查 savepoint 与 pump 节点 binlog 文件ID 是否一致
	- 一般场景不会出现此问题，出现此问题尽快联系 pingcap 运维

#### TiDB LB 选用与设置

- TiDB LB 需要支持四层 TCP 协议
	- 如： haproxy / LVS / F5硬件设备
	- 云厂商 负载均衡服务 基于 LVS+NGINX 构建
- 配置 LB 需要注意以下事项
	- 负载均衡策略
	- 后端主机状态监测
		- 选择 TCP 协议 `TiDB listen port`
		- 根据业务配置 检测隔断时长/重试次数/重试隔断时长
		- 健康监测端口可以选择TiDB status port (10080)
	- keepalived TCP 根据业务，默认可以不开启

