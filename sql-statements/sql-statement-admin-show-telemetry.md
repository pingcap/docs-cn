---
title：ADMIN SHOW TELEMETRY
summary：TiDB 数据库中 ADMIN SHOW TELEMETRY 的使用概况。
---

# ADMIN SHOW TELEMETRY

`ADMIN SHOW TELEMETRY` 语句用于查看通过[遥测](/telemetry.md)功能收集到并分享给 PingCAP 的使用信息。

## 语法图

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 'SHOW' ( 'DDL' ( 'JOBS' Int64Num? WhereClauseOptional | 'JOB' 'QUERIES' NumList )? | TableName 'NEXT_ROW_ID' | 'SLOW' AdminShowSlow | 'TELEMETRY' ) | 'CHECK' ( 'TABLE' TableNameList | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? ) | 'RECOVER' 'INDEX' TableName Identifier | 'CLEANUP' ( 'INDEX' TableName Identifier | 'TABLE' 'LOCK' TableNameList ) | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList | 'RELOAD' ( 'EXPR_PUSHDOWN_BLACKLIST' | 'OPT_RULE_BLACKLIST' | 'BINDINGS' ) | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList | 'REPAIR' 'TABLE' TableName CreateTableStmt | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS' )

```

## 示例

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY\G
```

```sql
*************************** 1. row ***************************
 TRACKING_ID: a1ba1d97-b940-4d5b-a9d5-ddb0f2ac29e7
 LAST_STATUS: {
  "check_at": "2021-08-11T08:23:38+02:00",
  "is_error": false,
  "error_msg": "",
  "is_request_sent": true
}
DATA_PREVIEW: {
  "hardware": [
    {
      "instanceType": "tidb",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "4000",
      "cpu": {
        "cache": "8192",
        "cpuFrequency": "2301.00MHz",
        "cpuLogicalCores": "8",
        "cpuPhysicalCores": "4"
      },
      "memory": {
        "capacity": "16410021888"
      },
      "disk": {
        "ebbca862689fa9fef7c55c3112e375c4ce575fe4": {
          "deviceName": "ebbca862689fa9fef7c55c3112e375c4ce575fe4",
          "free": "624438726656",
          "freePercent": "0.61",
          "fstype": "btrfs",
          "opts": "bind,rw,relatime",
          "path": "fb365c1216b59e1cfc86950425867007a60f4435",
          "total": "1022488477696",
          "used": "397115568128",
          "usedPercent": "0.39"
        },
        "nvme0n1p1": {
          "deviceName": "nvme0n1p1",
          "free": "582250496",
          "freePercent": "0.93",
          "fstype": "vfat",
          "opts": "rw,relatime",
          "path": "0fc8c8d71702d81a02e216fb6ef19f4dda4973df",
          "total": "627900416",
          "used": "45649920",
          "usedPercent": "0.07"
        },
        "nvme0n1p2": {
          "deviceName": "nvme0n1p2",
          "free": "701976576",
          "freePercent": "0.74",
          "fstype": "ext4",
          "opts": "rw,relatime",
          "path": "/boot",
          "total": "1023303680",
          "used": "250863616",
          "usedPercent": "0.26"
        }
      }
    },
    {
      "instanceType": "pd",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "2379",
      "cpu": {
        "cache": "8192",
        "cpuFrequency": "2301.00MHz",
        "cpuLogicalCores": "8",
        "cpuPhysicalCores": "4"
      },
      "memory": {
        "capacity": "16410021888"
      },
      "disk": {
        "ebbca862689fa9fef7c55c3112e375c4ce575fe4": {
          "deviceName": "ebbca862689fa9fef7c55c3112e375c4ce575fe4",
          "free": "624438726656",
          "freePercent": "0.61",
          "fstype": "btrfs",
          "opts": "bind,rw,relatime",
          "path": "fb365c1216b59e1cfc86950425867007a60f4435",
          "total": "1022488477696",
          "used": "397115568128",
          "usedPercent": "0.39"
        },
        "nvme0n1p1": {
          "deviceName": "nvme0n1p1",
          "free": "582250496",
          "freePercent": "0.93",
          "fstype": "vfat",
          "opts": "rw,relatime",
          "path": "0fc8c8d71702d81a02e216fb6ef19f4dda4973df",
          "total": "627900416",
          "used": "45649920",
          "usedPercent": "0.07"
        },
        "nvme0n1p2": {
          "deviceName": "nvme0n1p2",
          "free": "701976576",
          "freePercent": "0.74",
          "fstype": "ext4",
          "opts": "rw,relatime",
          "path": "/boot",
          "total": "1023303680",
          "used": "250863616",
          "usedPercent": "0.26"
        }
      }
    },
    {
      "instanceType": "tikv",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "20160",
      "cpu": {
        "cpuFrequency": "3730MHz",
        "cpuLogicalCores": "8",
        "cpuPhysicalCores": "4",
        "cpuVendorId": "GenuineIntel",
        "l1CacheLineSize": "64",
        "l1CacheSize": "32768",
        "l2CacheLineSize": "64",
        "l2CacheSize": "262144",
        "l3CacheLineSize": "64",
        "l3CacheSize": "8388608"
      },
      "memory": {
        "capacity": "16803861504"
      },
      "disk": {
        "36e7dfacbb83843f83075d78aeb4cf850a4882a1": {
          "deviceName": "36e7dfacbb83843f83075d78aeb4cf850a4882a1",
          "free": "624438726656",
          "freePercent": "0.61",
          "fstype": "btrfs",
          "path": "fb365c1216b59e1cfc86950425867007a60f4435",
          "total": "1022488477696",
          "used": "398049751040",
          "usedPercent": "0.39"
        },
        "nvme0n1p1": {
          "deviceName": "nvme0n1p1",
          "free": "582250496",
          "freePercent": "0.93",
          "fstype": "vfat",
          "path": "0fc8c8d71702d81a02e216fb6ef19f4dda4973df",
          "total": "627900416",
          "used": "45649920",
          "usedPercent": "0.07"
        },
        "nvme0n1p2": {
          "deviceName": "nvme0n1p2",
          "free": "701976576",
          "freePercent": "0.69",
          "fstype": "ext4",
          "path": "/boot",
          "total": "1023303680",
          "used": "321327104",
          "usedPercent": "0.31"
        }
      }
    },
    {
      "instanceType": "tiflash",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "3930",
      "cpu": {
        "cpuFrequency": "3400MHz",
        "cpuLogicalCores": "8",
        "cpuPhysicalCores": "4",
        "l1CacheLineSize": "64",
        "l1CacheSize": "32768",
        "l2CacheLineSize": "64",
        "l2CacheSize": "262144",
        "l3CacheLineSize": "64",
        "l3CacheSize": "8388608"
      },
      "memory": {
        "capacity": "16410021888"
      },
      "disk": {
        "36e7dfacbb83843f83075d78aeb4cf850a4882a1": {
          "deviceName": "36e7dfacbb83843f83075d78aeb4cf850a4882a1",
          "free": "624438726656",
          "freePercent": "0.61",
          "fstype": "btrfs",
          "path": "fb365c1216b59e1cfc86950425867007a60f4435",
          "total": "1022488477696",
          "used": "398049751040",
          "usedPercent": "0.39"
        }
      }
    }
  ],
  "instances": [
    {
      "instanceType": "tidb",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "4000",
      "statusHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "statusPort": "10080",
      "version": "5.1.1",
      "gitHash": "797bddd25310ed42f0791c8eccb78be8cce2f502",
      "startTime": "2021-08-11T08:23:38+02:00",
      "upTime": "22.210217487s"
    },
    {
      "instanceType": "pd",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "2379",
      "statusHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "statusPort": "2379",
      "version": "5.1.1",
      "gitHash": "7cba1912b317a533e18b16ea2ba9a14ed2891129",
      "startTime": "2021-08-11T08:23:32+02:00",
      "upTime": "28.210220368s"
    },
    {
      "instanceType": "tikv",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "20160",
      "statusHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "statusPort": "20180",
      "version": "5.1.1",
      "gitHash": "4705d7c6e9c42d129d3309e05911ec6b08a25a38",
      "startTime": "2021-08-11T08:23:33+02:00",
      "upTime": "27.210221447s"
    },
    {
      "instanceType": "tiflash",
      "listenHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "listenPort": "3930",
      "statusHostHash": "4b84b15bff6ee5796152495a230e45e3d7e947d9",
      "statusPort": "20292",
      "version": "v5.1.1",
      "gitHash": "c8fabfb50fe28db17cc5118133a69be255c40efd",
      "startTime": "2021-08-11T08:23:40+02:00",
      "upTime": "20.210222452s"
    }
  ],
  "hostExtra": {
    "cpuFlags": [
      "fpu",
      "vme",
      "de",
      "pse",
      "tsc",
      "msr",
      "pae",
      "mce",
      "cx8",
      "apic",
      "sep",
      "mtrr",
      "pge",
      "mca",
      "cmov",
      "pat",
      "pse36",
      "clflush",
      "dts",
      "acpi",
      "mmx",
      "fxsr",
      "sse",
      "sse2",
      "ss",
      "ht",
      "tm",
      "pbe",
      "syscall",
      "nx",
      "pdpe1gb",
      "rdtscp",
      "lm",
      "constant_tsc",
      "art",
      "arch_perfmon",
      "pebs",
      "bts",
      "rep_good",
      "nopl",
      "xtopology",
      "nonstop_tsc",
      "cpuid",
      "aperfmperf",
      "pni",
      "pclmulqdq",
      "dtes64",
      "monitor",
      "ds_cpl",
      "vmx",
      "est",
      "tm2",
      "ssse3",
      "sdbg",
      "fma",
      "cx16",
      "xtpr",
      "pdcm",
      "pcid",
      "sse4_1",
      "sse4_2",
      "x2apic",
      "movbe",
      "popcnt",
      "tsc_deadline_timer",
      "aes",
      "xsave",
      "avx",
      "f16c",
      "rdrand",
      "lahf_lm",
      "abm",
      "3dnowprefetch",
      "cpuid_fault",
      "epb",
      "invpcid_single",
      "ssbd",
      "ibrs",
      "ibpb",
      "stibp",
      "ibrs_enhanced",
      "tpr_shadow",
      "vnmi",
      "flexpriority",
      "ept",
      "vpid",
      "ept_ad",
      "fsgsbase",
      "tsc_adjust",
      "sgx",
      "bmi1",
      "avx2",
      "smep",
      "bmi2",
      "erms",
      "invpcid",
      "mpx",
      "rdseed",
      "adx",
      "smap",
      "clflushopt",
      "intel_pt",
      "xsaveopt",
      "xsavec",
      "xgetbv1",
      "xsaves",
      "dtherm",
      "ida",
      "arat",
      "pln",
      "pts",
      "hwp",
      "hwp_notify",
      "hwp_act_window",
      "hwp_epp",
      "md_clear",
      "flush_l1d",
      "arch_capabilities"
    ],
    "cpuModelName": "Intel(R) Core(TM) i7-10510U CPU @ 1.80GHz",
    "os": "linux",
    "platform": "fedora",
    "platformFamily": "fedora",
    "platformVersion": "34",
    "kernelVersion": "5.13.5-200.fc34.x86_64",
    "kernelArch": "x86_64",
    "virtualizationSystem": "kvm",
    "virtualizationRole": "host"
  },
  "reportTimestamp": 1628663040,
  "trackingId": "a1ba1d97-b940-4d5b-a9d5-ddb0f2ac29e7",
  "featureUsage": {
    "txn": {
      "asyncCommitUsed": true,
      "onePCUsed": true,
      "txnCommitCounter": {
        "twoPC": 9,
        "asyncCommit": 0,
        "onePC": 0
      }
    },
    "clusterIndex": {},
    "temporaryTable": false,
    "cte": {
      "nonRecursiveCTEUsed": 0,
      "recursiveUsed": 0,
      "nonCTEUsed": 13
    }
  },
  "windowedStats": [],
  "slowQueryStats": {
    "slowQueryBucket": {}
  }
}
1 row in set (0.0259 sec)
```

## MySQL 兼容性

`ADMIN` 语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [遥测](/telemetry.md)
* [系统变量 `tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入)
