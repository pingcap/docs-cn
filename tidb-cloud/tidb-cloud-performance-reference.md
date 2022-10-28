---
title: TiDB Cloud Performance Reference
summary: Learn TiDB Cloud performance test results.
---

# TiDB Cloud Performance Reference

This document provides [TPC-C](https://www.tpc.org/tpcc/) and [Sysbench](https://github.com/akopytov/sysbench) performance test results of several TiDB cluster scales, which can be taken as a reference when you [determine the cluster size](/tidb-cloud/size-your-cluster.md).

## 2 vCPU performance

Currently, the 2 vCPU support of TiDB and TiKV is still in beta.

Test environment:

- TiDB version: v6.1.0
- Warehouses: 1,000
- Data size: 80 GiB
- Table size: 10,000,000
- Table count: 32

Test scale:

- TiDB (2 vCPU, 8 GiB) \* 2; TiKV (2 vCPU, 8 GiB) \* 3

Test results:

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC  | Average latency (ms) |
    |-------------------|---------|-------|----------------------|
    | TPCC              | 25      | 4,486 | 2.24                 |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | Average latency (ms) |
    |-------------------|---------|--------|----------------------|
    | Insert            | 25      | 2,508  | 7.92                 |
    | Point Select      | 50      | 16,858 | 1.72                 |
    | Read Write        | 50      | 360    | 4.95                 |
    | Update Index      | 25      | 1,653  | 14.05                |
    | Update Non-index  | 25      | 2,800  | 8.02                 |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC  | Average latency (ms) |
    |-------------------|---------|-------|----------------------|
    | TPCC              | 100     | 7,592 | 6.68                 |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | Average latency (ms) |
    |-------------------|---------|--------|----------------------|
    | Insert            | 100     | 6,147  | 14.77                |
    | Point Select      | 100     | 19,462 | 3.21                 |
    | Read Write        | 100     | 378    | 9.58                 |
    | Update Index      | 100     | 3,140  | 30.34                |
    | Update Non-index  | 100     | 5,805  | 15.92                |

## 4 vCPU performance

Test environment:

- TiDB version: v5.4.0
- Warehouses: 5,000
- Data size: 366 GiB
- Table size: 10,000,000
- Table count: 16

Test scale:

- TiDB (4 vCPU, 16 GiB) \* 2; TiKV (4 vCPU, 16 GiB) \* 3

Test results:

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 300     | 14,532 | 13,137 | 608                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | Insert            | 300     | 8,848  | 8,848  | 36                   |
    | Point Select      | 600     | 46,224 | 46,224 | 13                   |
    | Read Write        | 150     | 719    | 14,385 | 209                  |
    | Update Index      | 150     | 4,346  | 4,346  | 35                   |
    | Update Non-index  | 600     | 13,603 | 13,603 | 44                   |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 1,200   | 15,208 | 13,748 | 2,321                |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | Insert            | 1,500   | 11,601 | 11,601 | 129                  |
    | Point Select      | 600     | 46,224 | 46,224 | 13                   |
    | Read Write        | 150     | 719    | 14,385 | 209                  |
    | Update Index      | 1,200   | 6,526  | 6,526  | 184                  |
    | Update Non-index  | 1,500   | 14,351 | 14,351 | 105                  |

## 8 vCPU performance

Test environment:

- TiDB version: v5.4.0
- Warehouses: 5,000
- Data size: 366 GiB
- Table size: 10,000,000
- Table count: 16

Test scales:

- TiDB (8 vCPU, 16 GiB) \* 2; TiKV (8 vCPU, 32 GiB) \* 3
- TiDB (8 vCPU, 16 GiB) \* 4; TiKV (8 vCPU, 32 GiB) \* 6

Test results:

**TiDB (8 vCPU, 16 GiB) \* 2; TiKV (8 vCPU, 32 GiB) \* 3**

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 600     | 32,266 | 29,168 | 548                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | Insert            | 600     | 17,831 | 17,831 | 34                   |
    | Point Select      | 600     | 93,287 | 93,287 | 6                    |
    | Read Write        | 300     | 1,486  | 29,729 | 202                  |
    | Update Index      | 300     | 9,415  | 9,415  | 32                   |
    | Update Non-index  | 1,200   | 31,092 | 31,092 | 39                   |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 1,200   | 33,394 | 30,188 | 1,048                |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS    | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | Insert            | 2,000   | 23,633 | 23,633 | 84                   |
    | Point Select      | 600     | 93,287 | 93,287 | 6                    |
    | Read Write        | 600     | 1,523  | 30,464 | 394                  |
    | Update Index      | 2,000   | 15,146 | 15,146 | 132                  |
    | Update Non-index  | 2,000   | 34,505 | 34,505 | 58                   |

**TiDB (8 vCPU, 16 GiB) \* 4; TiKV (8 vCPU, 32 GiB) \* 6**

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 1,200   | 62,918 | 56,878 | 310                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | Insert            | 1,200   | 33,892  | 33,892  | 23                   |
    | Point Select      | 1,200   | 185,574 | 181,255 | 4                    |
    | Read Write        | 600     | 2,958   | 59,160  | 127                  |
    | Update Index      | 600     | 18,735  | 18,735  | 21                   |
    | Update Non-index  | 2,400   | 60,629  | 60,629  | 23                   |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 2,400   | 65,452 | 59,169 | 570                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | Insert            | 4,000   | 47,029  | 47,029  | 43                   |
    | Point Select      | 1,200   | 185,574 | 181,255 | 4                    |
    | Read Write        | 1,200   | 3,030   | 60,624  | 197                  |
    | Update Index      | 4,000   | 30,140  | 30,140  | 67                   |
    | Update Non-index  | 4,000   | 68,664  | 68,664  | 29                   |

## 16 vCPU performance

Test environment:

- TiDB version: v5.4.0
- Warehouses: 5,000
- Data size: 366 GiB
- Table size: 10,000,000
- Table count: 16

Test scales:

- TiDB (16 vCPU, 32 GiB) \* 2; TiKV (16 vCPU, 64 GiB) \* 3
- TiDB (16 vCPU, 32 GiB) \* 4; TiKV (16 vCPU, 64 GiB) \* 6

Test results:

**TiDB (16 vCPU, 32 GiB) \* 2; TiKV (16 vCPU, 64 GiB) \* 3**

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 1,200   | 67,941 | 61,419 | 540                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | Insert            | 1,200   | 35,096  | 35,096  | 34                   |
    | Point Select      | 1,200   | 228,600 | 228,600 | 5                    |
    | Read Write        | 600     | 3,658   | 73,150  | 164                  |
    | Update Index      | 600     | 18,886  | 18,886  | 32                   |
    | Update Non-index  | 2,000   | 63,837  | 63,837  | 31                   |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC   | QPS    | Average latency (ms) |
    |-------------------|---------|--------|--------|----------------------|
    | TPCC              | 1,200   | 67,941 | 61,419 | 540                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | Insert            | 2,000   | 43,338  | 43,338  | 46                   |
    | Point Select      | 1,200   | 228,600 | 228,600 | 5                    |
    | Read Write        | 1,200   | 3,682   | 73,631  | 326                  |
    | Update Index      | 3,000   | 29,576  | 29,576  | 101                  |
    | Update Non-index  | 3,000   | 64,624  | 64,624  | 46                   |

**TiDB (16 vCPU, 32 GiB) \* 4; TiKV (16 vCPU, 64 GiB) \* 6**

- Optimal performance with low latency

    TPC-C performance:

    | Transaction model | Threads | tpmC    | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | TPCC              | 2,400   | 133,164 | 120,380 | 305                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | Insert            | 2,400   | 69,139  | 69,139  | 22                   |
    | Point Select      | 2,400   | 448,056 | 448,056 | 4                    |
    | Read Write        | 1,200   | 7,310   | 145,568 | 97                   |
    | Update Index      | 1,200   | 36,638  | 36,638  | 20                   |
    | Update Non-index  | 4,000   | 125,129 | 125,129 | 17                   |

- Maximum TPS and QPS

    TPC-C performance:

    | Transaction model | Threads | tpmC    | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | TPCC              | 2,400   | 133,164 | 120,380 | 305                  |

    Sysbench OLTP performance:

    | Transaction model | Threads | TPS     | QPS     | Average latency (ms) |
    |-------------------|---------|---------|---------|----------------------|
    | Insert            | 4,000   | 86,242  | 86,242  | 25                   |
    | Point Select      | 2,400   | 448,056 | 448,056 | 4                    |
    | Read Write        | 2,400   | 7,326   | 146,526 | 172                  |
    | Update Index      | 6,000   | 58,856  | 58,856  | 51                   |
    | Update Non-index  | 6,000   | 128,601 | 128,601 | 24                   |
