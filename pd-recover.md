---
title: PD Recover User Guide
summary: Use PD Recover to recover a PD cluster which cannot start or provide services normally.
aliases: ['/docs/dev/pd-recover/','/docs/dev/reference/tools/pd-recover/']
---

# PD Recover User Guide

PD Recover is a disaster recovery tool of PD, used to recover the PD cluster which cannot start or provide services normally. PD Recover is downloaded with TiDB Ansible in the `resource/bin/pd-recover` path.

## Quick Start

This section describes how to use PD Recover to recover a PD cluster.

### Get cluster ID

The cluster ID can be obtained from the log of PD, TiKV or TiDB. To get the cluster ID, you can either use the `ansible ad-hoc` command in the Control Machine, or view the log directly on the server.

#### Get `[info] cluster ID` from PD log (recommended)

To get the `[info] cluster id` from the PD log, run the following command:

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini pd_servers -m shell -a 'cat {{deploy_dir}}/log/pd.log | grep "init cluster id" | head -10'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/14 10:35:38.880 +00:00] [INFO] [server.go:212] ["init cluster id"] [cluster-id=6747551640615446306]
……
```

#### Get `[info] cluster ID` from TiDB log

To get the `[info] cluster ID` from the TiDB log, run the following command:

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tidb_servers -m shell -a 'cat {{deploy_dir}}/log/tidb*.log | grep "init cluster id" | head -10'
```

```
10.0.1.15 | CHANGED | rc=0 >>
2019/10/14 19:23:04.688 client.go:161: [info] [pd] init cluster id 6747551640615446306
……
```

#### Get `[info] PD cluster` from TiKV log

To get the `[info] PD cluster` from the TiKV log, run the following command:

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tikv_servers -m shell -a 'cat {{deploy_dir}}/log/tikv* | grep "PD cluster" | head -10'
```

```
10.0.1.15 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.278 +00:00] [INFO] [tikv-server.rs:464] ["connect to PD cluster 6747551640615446306"]
……
```

### Get `Alloc ID` (TiKV StoreID)

The `alloc-id` value you specify must be larger than the currently largest `Alloc ID` value. To get `Alloc ID`, you can either use the `ansible ad-hoc` command in the Control Machine, or view the log directly on the server.

#### Get `[info] allocates id` from PD log

To get the `[info] allocates id` from the PD log, run the following command:

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini pd_servers -m shell -a 'cat {{deploy_dir}}/log/pd* | grep "allocates" | head -10'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.824 +00:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=3000]
[2019/10/15 08:55:01.275 +00:00] [INFO] [id.go:91] ["idAllocator allocates a new id"] [alloc-id=4000]
……
```

#### Get `[info] alloc store id` from TiKV log

To get the `[info] alloc store id` from the TiKV log, run the following command:

{{< copyable "shell-regular" >}}

```
ansible -i inventory.ini tikv_servers -m shell -a 'cat {{deploy_dir}}/log/tikv* | grep "alloc store" | head -10'
```

```
10.0.1.13 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.516 +00:00] [INFO] [node.rs:229] ["alloc store id 4 "]
10.0.1.14 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.734 +00:00] [INFO] [node.rs:229] ["alloc store id 5 "]
10.0.1.15 | CHANGED | rc=0 >>
[2019/10/14 07:06:35.418 +00:00] [INFO] [node.rs:229] ["alloc store id 1 "]
10.0.1.21 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.826 +00:00] [INFO] [node.rs:229] ["alloc store id 2001 "]
10.0.1.20 | CHANGED | rc=0 >>
[2019/10/15 03:15:05.987 +00:00] [INFO] [node.rs:229] ["alloc store id 2002 "]
```

### Deploy a new PD cluster

To deploy a new PD cluster, run the following command:

{{< copyable "shell-regular" >}}

```
ansible-playbook bootsrap.yml --tags=pd &&
ansible-playbook deploy.yml --tags=pd &&
ansible-playbook start.yml --tags=pd
```

To delete the old cluster, delete the `data.pd` directory and restart the PD service.

### Use pd-recover

{{< copyable "shell-regular" >}}

```
./pd-recover -endpoints http://10.0.1.13:2379 -cluster-id 6747551640615446306 -alloc-id 10000
```

### Restart PD cluster

{{< copyable "shell-regular" >}}

```
ansible-playbook rolling_update.yml --tags=pd
```

### Restart TiDB or TiKV

{{< copyable "shell-regular" >}}

```
ansible-playbook rolling_update.yml --tags=tidb,tikv
```

## FAQ

### Multiple cluster IDs are found when getting the cluster ID

When a PD cluster is created, a new cluster ID is generated. You can determine the cluster ID of the old cluster by viewing the log.

### The error `dial tcp 10.0.1.13:2379: connect: connection refused` is returned when executing `pd-recover`

The PD service is required when you execute `pd-recover`. Deploy and start the PD cluster before you use PD Recover.
