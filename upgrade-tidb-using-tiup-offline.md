---
title: Upgrade TiDB Using TiUP Offline Mirror
summary: Learn how to upgrade TiDB using the TiUP offline mirror.
aliases: ['/docs/dev/upgrade-tidb-using-tiup-offline/']
---

# Upgrade TiDB Using TiUP Offline Mirror

This document describes how to upgrade TiDB using TiUP offline mirror. The upgrade steps are as follows.

## Update TiUP offline mirror

1. To update the local TiUP offline mirror, refer to Step 1 and Step 2 in [Deploy a TiDB Cluster Offline Using TiUP](/production-offline-deployment-using-tiup.md) to download and deploy the new version of the TiUP offline mirror.

    After you execute `local_install.sh`, TiUP completes the overwrite and upgrade.

2. The offline mirror is successfully updated. After the overwrite, if an error is reported when TiUP is running, it might be that `manifest` is not updated. To fix this, you can execute `rm -rf ~/.tiup/manifests` before using TiUP.

## Upgrade TiDB cluster

After the local mirror is updated, refer to [Upgrade TiDB Using TiUP](/upgrade-tidb-using-tiup.md) to upgrade the TiDB cluster.

> **Note:**
>
> By default, TiUP and TiDB (starting from v4.0.2) share usage details with PingCAP to help understand how to improve the product. For details about what is shared and how to disable the sharing, see [Telemetry](/telemetry.md).
