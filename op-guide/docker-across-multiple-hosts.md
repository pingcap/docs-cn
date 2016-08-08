# 在多主机上使用 docker 运行一个 TiDB 集群

本篇将展示如何在多台主机上使用 Docker 部署一个 TiDB 集群

## 环境准备
假设我们有三台机器:

|Name|Host IP|
|----|-------|
|**host1**|192.168.1.100|
|**host2**|192.168.1.101|
|**host3**|192.168.1.102|

每台机器已经安装最新版本 Docker, 并且拉取了最新的 TiDB/TiKV/PD 的镜像。

```bash
docker pull pingcap/tidb:latest
docker pull pingcap/tikv:latest
docker pull pingcap/pd:latest
```

## 1. 在每台主机上启动一个 `busybox` 作为数据存储容器

```bash
export host1=192.168.1.100
export host2=192.168.1.101
export host3=192.168.1.102

docker run -d --name ti-storage \
  -v /tidata \
  busybox
```

## 2. 每台机器上启动 PD

**host1:**
```bash
docker run -d --name pd1 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd1" \
  --data-dir="/tidata/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host1}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host1}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
```

**host2:**
```bash
docker run -d --name pd2 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd2" \
  --data-dir="/tidata/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host2}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host2}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
```

**host3:**
```bash
docker run -d --name pd3 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd3" \
  --data-dir="/tidata/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://${host3}:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://${host3}:2380" \
  --initial-cluster="pd1=http://${host1}:2380,pd2=http://${host2}:2380,pd3=http://${host3}:2380" \
```

## 3. 每台机器上启动 TiKV

**host1:**
```bash
docker run -d --name tikv1 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host1}:20160" \
  --store="/tidata/tikv1" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

**host2:**
```bash
docker run -d --name tikv2 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host2}:20160" \
  --store="/tidata/tikv2" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

**host3:**
```bash
docker run -d --name tikv3 \
  -p 20160:20160
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="${host3}:20160" \
  --store="/tidata/tikv3" \
  --dsn=raftkv \
  --pd="${host1}:2379,${host2}:2379,${host3}:2379" \
  --cluster-id=1
```

## 4. 在 **host1** 上启动 TiDB

```bash
docker run -d --name tidb \
  -p 4000:4000 \
  -p 10080:10080 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb \
  --store=tikv \
  --path="${host1}:2379,${host2}:2379,${host3}:2379?cluster=1" \
  -L warn
```

## 5. 在 **host1** 上使用 MySQL 客户端连接 TiDB 进行测试

```bash
mysql -h ${host1} -P 4000 -u root -D test
```
