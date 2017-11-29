---
title: PD Control User Guide
category: tools
---

# PD Control User Guide

As a command line tool of PD, PD Control obtains the state information of the cluster and tunes the cluster.

## Source code compiling

1. [*Go*](https://golang.org/) Version 1.7 or later
2. In the PD root directory, use `make` command to compile and generate bin/pd-ctl

**Note:** Generally, you don't need to compile source code as the PD Control tool already exists in the released Binary or Docker. However, dev users can refer to the above instruction for compiling source code.

## Usage

single-command mode:

    ./pd-ctl store -d -u http://127.0.0.1:2379

interactive mode:

    ./pd-ctl -u http://127.0.0.1:2379

use environment variables:

```bash
export PD_ADDR=http://127.0.0.1:2379
./pd-ctl
```

## command line flags

### \-\-pd,-u

+ PD address
+ Default address: http://127.0.0.1:2379
+ Enviroment variable: PD_ADDR

### \-\-detach,-d

+ Use single command line mode (not entering readline)
+ Default value: false

## command (command)

### store [delete] \<store_id\>

Display the store information or delete a specified store.

Usage:

```bash
>> store            // Display the information of all stores
{
  "count": 3,
  "stores": [...]
}
>> store 1          // Get the store with a store id 1
  ......
>> store delete 1   // Make the store with a store id 1 offline
  ......
```

### region \<region_id\>

Display the region information.

Usage:

```bash
>> region                               //　Display the information of all regions
{
  "count": 1,
  "regions": [......]
}

>> region 2                             // Display the information of region id 2
{
  "region": {
      "id": 2,
      ......
  }
  "leader": {
      ......
  }
}
```

### region key [--format=raw|pb|proto|protobuf] \<key\>

Query the region that a specific key resides in. It supports the raw and protobuf format.

Raw format usage (default):

```bash
>> region key abc
{
  "region": {
    "id": 2,
    ......
  }
}
```

Protobuf format usage:

```bash
>> region key --format=pb t\200\000\000\000\000\000\000\377\035_r\200\000\000\000\000\377\017U\320\000\000\000\000\000\372
{
  "region": {
    "id": 2,
    ......
  }
}
```

### member [leader | delete]

Display the PD member informaiton or delete a specified member.

Usage:

```bash
>> member                               // Display the information of all members
{
  "members": [......]
}
>> member leader show                   // Display the information of leader
{
  "name": "pd",
  "addr": "http://192.168.199.229:2379",
  "id": 9724873857558226554
}
>> member delete name pd2               // Make "pd2" offline
Success!
>> member delete id 1319539429105371180 // Use id to shut down the node
```

### config [show | set \<option\> \<value\>]

Display or modify the configuration information.

Usage:

```bash
>> config show                             //　Dispaly the information of config
{
  "max-snapshot-count": 3,
  "max-store-down-time": "1h",
  "leader-schedule-limit": 8,
  "region-schedule-limit": 4,
  "replica-schedule-limit": 8,
}
```

By modifying `leader-schedule-limit`, you can control the number of simultaneously implementing leader schedule.
This value mainly impacts the speed of *leader balance*: the bigger the value is, the faster the schedule goes. If the value is set to 0, the schedule will be closed.
The overhead of the Leader schedule is smaller and it can set to be bigger when necessary.

```bash
>> config set leader-schedule-limit 4       // Up to 4 leader schedules can be implemented simutaneously
```

By modifying `region-schedule-limit`, you can control the number of simultaneously implementing region schedule.
This value mainly impacts the speed of *region balance*: the bigger the value is, the faster the schedule goes. If the value is set to 0, the schedule will be closed.
The overhead of the Region schedule is relatively big and it should not set to be too big.

```bash
>> config set region-schedule-limit 2       // Up to 2 region schedules can be implemented simutaneously
```

By modifying `replica-schedule-limit`, you can control the number of simultaneously implementing replica schedule.
This value mainly impacts the schedule speed when a node breaks down or becomes offline: the bigger the value is, the faster the schedule goes. If the value is set to 0, the schedule will be closed.
The overhead of the Replica schedule is relatively big and it should not set to be too big.

```bash
>> config set replica-schedule-limit 4      // Up to 4 replica schedules can be implemented simutaneously
```

### operator [show | add | remove]

Display and control schedule operations.

Usage:

```bash
>> operator show                            // Display all operators
>> operator show admin                      // Display all admin operators
>> operator show leader                     // Display all leader operators
>> operator show region                     // Display all region operators
>> operator add transfer-leader 1 2         // Schedule the leader of region 1 to store 2
>> operator add transfer-region 1 2 3 4     // Schedule region 1 to store 2,3,4
>> operator add transfer-peer 1 2 3         // Schedule the replica of region 1 on store 2 to store 3
>> operator remove 1                        // Delete the schedule operation of region 1
```

### scheduler [show | add | remove]

Display and control schedule strategies.

Usage:

```bash
>> scheduler show                             // Display all schedulers
>> scheduler add grant-leader-scheduler 1     // Schedule the leader of all regions on store 1 to store 1
>> scheduler add evict-leader-scheduler 1     // Schedule the leader of all regions on store 1 out of store 1
>> scheduler add shuffle-leader-scheduler     // Randomly exchange leaders on store
>> scheduler add shuffle-region-scheduler     // Randomly schedule regions on different stores
>> scheduler remove grant-leader-scheduler-1  // Delete the corresponding scheduler
```

### hot [read | write | store]

Display the hot spot in the cluster.

Usage:

```bash
>> hot read                                   // Display hot spot for the read operation
>> hot write                                  // Display hot spot for the write operation
>> hot store                                  // Display hot spot for all the read and write operations
```