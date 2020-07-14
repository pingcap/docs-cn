---
title: TiDB Binlog Troubleshooting
summary: Learn the troubleshooting process of TiDB Binlog.
aliases: ['/docs/dev/tidb-binlog/troubleshoot-tidb-binlog/','/docs/dev/reference/tidb-binlog/troubleshoot/binlog/','/docs/dev/how-to/troubleshoot/tidb-binlog/']
---

# TiDB Binlog Troubleshooting

This document describes how to troubleshoot TiDB Binlog to find the problem.

If you encounter errors while running TiDB Binlog, take the following steps to troubleshoot:

1. Check whether each monitoring metric is normal or not. Refer to [TiDB Binlog Monitoring](/tidb-binlog/monitor-tidb-binlog-cluster.md) for details.

2. Use the [binlogctl tool](/tidb-binlog/binlog-control.md) to check whether the state of each Pump or Drainer node is normal or not.

3. Check whether `ERROR` or `WARN` exists in the Pump log or Drainer log.

After finding out the problem by the above steps, refer to [FAQ](/tidb-binlog/tidb-binlog-faq.md) and [TiDB Binlog Error Handling](/tidb-binlog/handle-tidb-binlog-errors.md) for the solution. If you fail to find the solution or the solution provided does not help, submit an [issue](https://github.com/pingcap/tidb-binlog/issues) for help.
