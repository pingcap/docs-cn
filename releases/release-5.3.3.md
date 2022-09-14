---
title: TiDB 5.3.3 Release Note
---

# TiDB 5.3.3 Release Note

Release date: September 14, 2022

TiDB version: 5.3.3

## Bug fix

+ TiKV

    - Fix the issue of continuous SQL execution errors in the cluster after the PD leader is switched or PD is restarted.

        This issue is caused by a TiKV bug that TiKV does not retry sending heartbeat information to PD client after heartbeat requests fail, until TiKV reconnects to PD client. As a result, the Region information on the failed TiKV node becomes outdated, and TiDB cannot get the latest Region information, which causes SQL execution errors.

        This issue is fixed in v5.3. You can upgrade your cluster to v5.3.3.

        As a workaround, you can also restart the TiKV nodes that cannot send Region heartbeat to PD, until there is no Region heartbeat to send.

        For bug details, see [#12934](https://github.com/tikv/tikv/issues/12934).
