---
title: TiDB 6.5.5 Release Notes
summary: Learn about the improvements and bug fixes in TiDB 6.5.5.
---

# TiDB 6.5.5 Release Notes

Release date: September 21, 2023

TiDB version: 6.5.5

Quick access: [Quick start](https://docs.pingcap.com/tidb/v6.5/quick-start-with-tidb) | [Production deployment](https://docs.pingcap.com/tidb/v6.5/production-deployment-using-tiup) | [Installation packages](https://www.pingcap.com/download/?version=v6.5.5#version-list)

## Improvements

+ TiDB

    - Add new optimizer hints, including [`NO_MERGE_JOIN()`](/optimizer-hints.md#no_merge_joint1_name--tl_name-), [`NO_INDEX_JOIN()`](/optimizer-hints.md#no_index_joint1_name--tl_name-), [`NO_INDEX_MERGE_JOIN()`](/optimizer-hints.md#no_index_merge_joint1_name--tl_name-), [`NO_HASH_JOIN()`](/optimizer-hints.md#no_hash_joint1_name--tl_name-), and [`NO_INDEX_HASH_JOIN()`](/optimizer-hints.md#no_index_hash_joint1_name--tl_name-) [#45520](https://github.com/pingcap/tidb/issues/45520) @[qw4990](https://github.com/qw4990)
    - Add request source information related to the coprocessor [#46514](https://github.com/pingcap/tidb/issues/46514) @[you06](https://github.com/you06)

+ TiKV

    - Add the backoff mechanism for the PD client in the process of connection retries, which gradually increases retry intervals during error retries to reduce PD pressure [#15428](https://github.com/tikv/tikv/issues/15428) @[nolouch](https://github.com/nolouch)
    - Add monitoring metrics for snapshots [#15401](https://github.com/tikv/tikv/issues/15401) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - Improve stability of PITR checkpoint lag during leader transfers [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)
    - Add logs and monitoring metrics related to `safe-ts` [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - Provide more logs and monitoring metrics for `resolved-ts` [#15082](https://github.com/tikv/tikv/issues/15082) @[ekexium](https://github.com/ekexium)
    - Optimize the compaction mechanism: when a Region is split, if there is no key to split, a compaction is triggered to eliminate excessive MVCC versions [#15282](https://github.com/tikv/tikv/issues/15282) @[SpadeA-Tang](https://github.com/SpadeA-Tang)

+ Tools

    + Backup & Restore (BR)

        - Reduce the CPU overhead of log backup `resolve lock` [#40759](https://github.com/pingcap/tidb/issues/40759) @[3pointer](https://github.com/3pointer)

## Bug fixes

+ TiDB

    - Fix the issue that Stale Read might select an unavailable replica [#46198](https://github.com/pingcap/tidb/issues/46198) @[zyguan](https://github.com/zyguan)
    - Fix the issue that additional overhead is incurred due to the incompatibility between Stale Read and Schema Cache [#43481](https://github.com/pingcap/tidb/issues/43481) @[crazycs520](https://github.com/crazycs520)

+ TiKV

    - Fix the issue that the peers of the corresponding Region mistakenly hibernate when a TiKV node fails [#14547](https://github.com/tikv/tikv/issues/14547) @[hicqu](https://github.com/hicqu)
    - Fix the issue that TiKV fails to start when Titan is enabled and the `Blob file deleted twice` error occurs [#15454](https://github.com/tikv/tikv/issues/15454) @[Connor1996](https://github.com/Connor1996)
    - Fix the issue that Online Unsafe Recovery cannot handle merge abort [#15580](https://github.com/tikv/tikv/issues/15580) @[v01dstar](https://github.com/v01dstar)
    - Fix the issue that network interruption between PD and TiKV might cause PITR to get stuck [#15279](https://github.com/tikv/tikv/issues/15279) @[YuJuncen](https://github.com/YuJuncen)

+ PD

    - Fix the issue that the scheduler takes a long time to start up [#6920](https://github.com/tikv/pd/issues/6920) @[HuSharp](https://github.com/HuSharp)
    - Fix the issue that the logic for handling Leaders and Peers in Scatter Region is inconsistent [#6962](https://github.com/tikv/pd/issues/6962) @[bufferflies](https://github.com/bufferflies)
    - Fix the issue that the `empty-region-count` monitoring metric is abnormal when the cluster is restarted or the PD Leader is switched [#7008](https://github.com/tikv/pd/issues/7008) @[CabinfeverB](https://github.com/CabinfeverB)
    
+ Tools

    + Backup & Restore (BR)

        - Fix the issue that restoring implicit primary keys by PITR might lead to conflicts [#46520](https://github.com/pingcap/tidb/issues/46520) @[3pointer](https://github.com/3pointer)
        - Fix the issue that an error occurs when PITR recovers the meta-kv [#46578](https://github.com/pingcap/tidb/issues/46578) @[Leavrth](https://github.com/Leavrth)
        - Fix an error in BR integration test cases [#45561](https://github.com/pingcap/tidb/issues/46561) @[purelind](https://github.com/purelind)
        - Alleviate the issue that the latency of the PITR log backup progress increases when Region leadership migration occurs [#13638](https://github.com/tikv/tikv/issues/13638) @[YuJuncen](https://github.com/YuJuncen)

    + TiCDC

        - Fix the issue of high TiCDC replication latency caused by network isolation of PD nodes [#9565](https://github.com/pingcap/tiflow/issues/9565) @[asddongmen](https://github.com/asddongmen)
        - Fix the issue that TiCDC incorrectly changes the `UPDATE` operation to `INSERT` when using the CSV format [#9658](https://github.com/pingcap/tiflow/issues/9658) @[3AceShowHand](https://github.com/3AceShowHand)
        - Fix the issue that user passwords are recorded in some logs [#9690](https://github.com/pingcap/tiflow/issues/9690) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that using the SASL authentication might cause TiCDC to panic [#9669](https://github.com/pingcap/tiflow/issues/9669) @[sdojjy](https://github.com/sdojjy)
        - Fix the issue that TiCDC replication tasks might fail in some corner cases [#9685](https://github.com/pingcap/tiflow/issues/9685) [#9697](https://github.com/pingcap/tiflow/issues/9697) [#9695](https://github.com/pingcap/tiflow/issues/9695) [#9736](https://github.com/pingcap/tiflow/issues/9736) @[hicqu](https://github.com/hicqu) @[CharlesCheung96](https://github.com/CharlesCheung96)
        - Fix the issue that TiCDC cannot recover quickly from TiKV node failures when there are a lot of Regions upstream [#9741](https://github.com/pingcap/tiflow/issues/9741) @[sdojjy](https://github.com/sdojjy)
    
    + TiDB Lightning

        - Fix the issue that TiDB Lightning fails to start when TiCDC is deployed on the target server [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning fails to start when PD topology is changed [#46688](https://github.com/pingcap/tidb/issues/46688) @[lance6716](https://github.com/lance6716)
        - Fix the issue that TiDB Lightning cannot continue importing data after PD switching Leaders [#46540](https://github.com/pingcap/tidb/issues/46540) @[lance6716](https://github.com/lance6716)
        - Fix the issue that precheck cannot accurately detect the presence of a running TiCDC in the target cluster [#41040](https://github.com/pingcap/tidb/issues/41040) @[lance6716](https://github.com/lance6716)
