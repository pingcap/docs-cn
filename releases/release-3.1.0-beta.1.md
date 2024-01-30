---
title: TiDB 3.1 Beta.1 Release Notes
aliases: ['/docs/dev/releases/release-3.1.0-beta.1/','/docs/dev/releases/3.1.0-beta.1/']
summary: TiDB 3.1 Beta.1 was released on January 10, 2020. The release includes changes to TiKV, such as renaming backup files and adding incremental backup features. Tools like BR have improved backup progress information and added features for partitioned tables. TiDB Ansible now automatically disables Transparent Huge Pages and adds Grafana monitoring for BR components. Overall, the release focuses on improving backup and restore processes, monitoring, and deployment optimization.
---

# TiDB 3.1 Beta.1 Release Notes

Release date: January 10, 2020

TiDB version: 3.1.0-beta.1

TiDB Ansible version: 3.1.0-beta.1

## TiKV

+ backup
    - Change the name of the backup file from `start_key` to the hash value of `start_key` to reduce the file name's length for easy reading [#6198](https://github.com/tikv/tikv/pull/6198)
    - Disable RocksDB's `force_consistency_checks` check to avoid false positives in the consistency check [#6249](https://github.com/tikv/tikv/pull/6249)
    - Add the incremental backup feature [#6286](https://github.com/tikv/tikv/pull/6286)

+ sst_importer
    - Fix the issue that the SST file does not have MVCC properties during restoring [#6378](https://github.com/tikv/tikv/pull/6378)
    - Add the monitoring items such as `tikv_import_download_duration`, `tikv_import_download_bytes`, `tikv_import_ingest_duration`, `tikv_import_ingest_bytes`, and `tikv_import_error_counter` to observe the overheads of downloading and ingesting SST files [#6404](https://github.com/tikv/tikv/pull/6404)
+ raftstore
    - Fix the issue of Follower Read that the follower reads stale data when the leader changes, thus breaking transaction isolation [#6343](https://github.com/tikv/tikv/pull/6343)

## Tools

+ BR (Backup and Restore)
    - Fix the inaccurate backup progress information [#127](https://github.com/pingcap/br/pull/127)
    - Improve the performance of splitting Regions [#122](https://github.com/pingcap/br/pull/122)
    - Add the backup and restore feature for partitioned tables [#137](https://github.com/pingcap/br/pull/137)
    - Add the feature of automatically scheduling PD schedulers [#123](https://github.com/pingcap/br/pull/123)
    - Fix the issue that data is overwritten after non `PKIsHandle` tables are restored [#139](https://github.com/pingcap/br/pull/139)

## TiDB Ansible

- Add the feature of automatically disabling Transparent Huge Pages (THP) in the operating system during the initialization phase [#1086](https://github.com/pingcap/tidb-ansible/pull/1086)
- Add the Grafana monitoring for BR components [#1093](https://github.com/pingcap/tidb-ansible/pull/1093)
- Optimize the deployment of TiDB Lightning by automatically creating related directories [#1104](https://github.com/pingcap/tidb-ansible/pull/1104)