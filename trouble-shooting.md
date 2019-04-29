---
title: TiDB Cluster Troubleshooting Guide
summary: Learn how to diagnose and resolve issues when you use TiDB.
category: advanced
---

# TiDB Cluster Troubleshooting Guide

You can use this guide to help you diagnose and solve basic problems while using TiDB. If your problem is not resolved, please collect the following information and [create an issue](https://github.com/pingcap/tidb/issues/new/choose):

- The exact error message and the operations while the error occurs
- The state of all the components
- The `error`/`fatal`/`panic` information in the log of the component that reports the error
- The configuration and deployment topology
- The TiDB component related issue in `dmesg`

For other information, see [Frequently Asked Questions (FAQ)](FAQ.md).

## Cannot connect to the database

1. Make sure all the services are started, including `tidb-server`, `pd-server`, and `tikv-server`.
2. Use the `ps` command to check if all the processes are running.

    - If a certain process is not running, see the following corresponding sections to diagnose and solve the issue.
    + If all the processes are running, check the `tidb-server` log to see if the following messages are displayed:
        - InformationSchema is out of date: This message is displayed if the `tikv-server` cannot be connected. Check the state and log of `pd-server` and `tikv-server`.
        - panic: This message is displayed if there is an issue with the program. Please provide the detailed panic log and [create an issue](https://github.com/pingcap/tidb/issues/new/choose).
        
3. If the data is cleared and the services are re-deployed, make sure that:

    - All the data in `tikv-server` and `pd-server` are cleared.
    The specific data is stored in `tikv-server` and the metadata is stored in `pd-server`. If only one of the two servers is cleared, the data will be inconsistent.
    - After the data in `pd-server` and `tikv-server` are cleared and the `pd-server` and `tikv-server` are restarted, the `tidb-server` must be restarted too.
    The cluster ID is randomly allocated when the `pd-server` is initialized. So when the cluster is re-deployed, the cluster ID changes and you need to restart the `tidb-server` to get the new cluster ID.

## Cannot start `tidb-server`

See the following for the situations when the `tidb-server` cannot be started:

- Error in the startup parameters.
    See the [TiDB configuration and options](op-guide/configuration.md#tidb).
- The port is occupied.
    Use the `lsof -i:port` command to show all the networking related to a given port and make sure the port to start the `tidb-server` is not occupied.
+ Cannot connect to `pd-server`.

    - Check if the network between TiDB and PD is running smoothly, including whether the network can be pinged or if there is any issue with the Firewall configuration.
    - If there is no issue with the network, check the state and log of the `pd-server` process.

## Cannot start `tikv-server`

See the following for the situations when the `tikv-server` cannot be started:

- Error in the startup parameters: See the [TiKV configuration and options](op-guide/configuration.md#tikv).
- The port is occupied: Use the `lsof -i:port` command to show all the networking related to a given port and make sure the port to start the `tikv-server` is not occupied.
+ Cannot connect to `pd-server`.
    - Check if the network between TiDB and PD is running smoothly, including whether the network can be pinged or if there is any issue with the Firewall configuration.
    - If there is no issue with the network, check the state and log of the `pd-server` process.
- The file is occupied.
    Do not open two TiKV files on one database file directory.

## Cannot start `pd-server`

See the following for the situations when the `pd-server` cannot be started:

- Error in the startup parameters.
    See the [PD configuration and options](op-guide/configuration.md##placement-driver-pd).
- The port is occupied.
    Use the `lsof -i:port` command to show all the networking related to a given port and make sure the port to start the `pd-server` is not occupied.

## The TiDB/TiKV/PD process aborts unexpectedly

- Is the process started on the foreground? The process might exit because the client aborts.

- Is `nohup+&` run in the command line? This might cause the process to abort because it receives the hup signal. It is recommended to write and run the startup command in a script.

## TiDB panic

Please provide the panic log and [create an issue](https://github.com/pingcap/tidb/issues/new/choose).

## The connection is rejected

Make sure the network parameters of the operating system are correct, including but not limited to:

- The port in the connection string is consistent with the `tidb-server` starting port.
- The firewall is configured correctly.

## Open too many files

Before starting the process, make sure the result of `ulimit -n` is large enough. It is recommended to set the value to `unlimited` or larger than `1000000`.

## Database access times out and the system load is too high

First, check the [SLOW-QUERY](sql/slow-query.md) log and see if it is because of some inappropriate SQL statement.
If you failed to solve the problem, provide the following information:

+ The deployment topology
    - How many `tidb-server`/`pd-server`/`tikv-server` instances are deployed?
    - How are these instances distributed in the machines?
+ The hardware configuration of the machines where these instances are deployed:
    - The number of CPU cores
    - The size of the memory
    - The type of the disk (SSD or Hard Drive Disk)
    - Are they physical machines or virtual machines?
- Are there other services besides the TiDB cluster?
- Are the `pd-server`s and `tikv-server`s deployed separately?
- What is the current operation?
- Check the CPU thread name using the `top -H` command.
- Are there any exceptions in the network or IO monitoring data recently?
