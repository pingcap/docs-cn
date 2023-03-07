---
title: Logical Import Mode Introduction
summary: Learn about the logical import mode in TiDB Lightning.
---

# Logical Import Mode Introduction

The logical import mode is one of the two import modes supported by TiDB Lightning. In the logical import mode, TiDB Lightning first encodes data into SQL statements and then runs the SQL statements to import data.

If your TiDB cluster already contains data and provides service for external applications, it is recommended to import data in the logical import mode. The behavior of the logical import mode is the same as executing normal SQL statements, and thus it guarantees ACID compliance.

The backend for the logical import mode is `tidb`.

## Environment requirements

**Operating system**:

It is recommended to use fresh CentOS 7 instances. You can deploy a virtual machine either on your local host or in the cloud. Because TiDB Lightning consumes as much CPU resources as needed by default, it is recommended that you deploy it on a dedicated server. If this is not possible, you can deploy it on a single server together with other TiDB components (for example, tikv-server) and then configure `region-concurrency` to limit the CPU usage from TiDB Lightning. Usually, you can configure the size to 75% of the logical CPU.

**Memory and CPU**:

It is recommended that you allocate CPU more than 4 cores and memory greater than 8 GiB to get better performance. It is verified that TiDB Lightning does not have significant memory usage (no more than 5 GiB) in the logical import mode. However, if you increase the value of `region-concurrency`, TiDB Lightning might consume more memory.

**Network**: A 1 Gbps or 10 Gbps Ethernet card is recommended.

## Limitations

When you use multiple TiDB Lightning to import data to the same target, do not mix the backends. That is, do not use the physical import mode and the logical import mode to import data to a single TiDB cluster at the same time.
