---
title: Stress Test TiDB Using TiUP Bench Component
summary: Learns how to stress test TiDB with TPC-C and TPC-H workloads using TiUP.
aliases: ['/docs/dev/tiup/tiup-bench/','/docs/dev/reference/tools/tiup/bench/']
---

# Stress Test TiDB Using TiUP Bench Component

When you test the performance of a database, it is often required to stress test the database. To facilitate this, TiUP has integrated the bench component, which provides two workloads for stress testing: TPC-C and TPC-H. The commands and flags are as follows:

{{< copyable "shell-root" >}}

```bash
tiup bench
```

```
Starting component `bench`: /home/tidb/.tiup/components/bench/v1.5.0/bench
Benchmark database with different workloads

Usage:
  tiup bench [command]

Available Commands:
  help        Help about any command
  tpcc
  tpch

Flags:
      --count int           Total execution count, 0 means infinite
  -D, --db string           Database name (default "test")
  -d, --driver string       Database driver: mysql
      --dropdata            Cleanup data before prepare
  -h, --help                help for /Users/joshua/.tiup/components/bench/v0.0.1/bench
  -H, --host string         Database host (default "127.0.0.1")
      --ignore-error        Ignore error when running workload
      --interval duration   Output interval time (default 10s)
      --isolation int       Isolation Level 0: Default, 1: ReadUncommitted,
                            2: ReadCommitted, 3: WriteCommitted, 4: RepeatableRead,
                            5: Snapshot, 6: Serializable, 7: Linerizable
      --max-procs int       runtime.GOMAXPROCS
  -p, --password string     Database password
  -P, --port int            Database port (default 4000)
      --pprof string        Address of pprof endpoint
      --silence             Don't print error when running workload
      --summary             Print summary TPM only, or also print current TPM when running workload
  -T, --threads int         Thread concurrency (default 16)
      --time duration       Total execution time (default 2562047h47m16.854775807s)
  -U, --user string         Database user (default "root")
```

The following sections describe how to run TPC-C and TPC-H tests using TiUP.

## Run TPC-C test using TiUP

The TiUP bench component supports the following commands and flags to run the TPC-C test:

```bash
Available Commands:
  check       Check data consistency for the workload
  cleanup     Cleanup data for the workload
  prepare     Prepare data for the workload
  run         Run workload

Flags:
      --check-all        Run all consistency checks
  -h, --help             help for tpcc
      --output string    Output directory for generating csv file when preparing data
      --parts int        Number to partition warehouses (default 1)
      --tables string    Specified tables for generating file, separated by ','. Valid only if output is set. If this flag is not set, generate all tables by default.
      --warehouses int   Number of warehouses (default 10)
```

### Test procedures

1. Create 4 warehouses using 4 partitions via hash:

    ```shell
    tiup bench tpcc --warehouses 4 --parts 4 prepare
    ```

2. Run the TPC-C test:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 run
    ```

3. Clean up data:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 cleanup
    ```

4. Check the consistency:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 check
    ```

5. Generate the CSV file:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data
    ```

6. Generate the CSV file for the specified table:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data --tables history,orders
    ```

7. Enable pprof:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpcc --warehouses 4 prepare --output data --pprof :10111
    ```

## Run TPC-H test using TiUP

The TiUP bench component supports the following commands and parameters to run the TPC-H test:

```bash
Available Commands:
  cleanup     Cleanup data for the workload
  prepare     Prepare data for the workload
  run         Run workload

Flags:
      --check            Check output data, only when the scale factor equals 1
  -h, --help             help for tpch
      --queries string   All queries (default "q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15,q16,q17,q18,q19,q20,q21,q22")
      --sf int           scale factor
```

### Test procedures

1. Prepare data:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

2. Run the TPC-H test by executing one of the following commands:

    - If you check the result, run this command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup bench tpch --sf=1 --check=true run
        ```

    - If you do not check the result, run this command:

        {{< copyable "shell-regular" >}}

        ```shell
        tiup bench tpch --sf=1 run
        ```

3. Clean up data:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch cleanup
    ```
