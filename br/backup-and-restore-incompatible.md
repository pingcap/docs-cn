---
title: Backup & Restore 兼容性问题
summary: BR 兼容性问题梳理。
aliases: ['/docs-cn/dev/br/backup-and-restore-incompatible/']
---

# BR 兼容性问题整理

BR 和 集群 兼容性可以划分成两个方面，一方面是在某些 feature 在开启或关闭情况下，会导致 KV 格式发生变化，因此可能带来不兼容的问题，另一方面是 BR 某些版本和集群接口不兼容，现整理如下:

不兼容 feature | 相关 issue | 解决方式
|  ----  | ----  | ----- |
Cluster Index  | [#565](https://github.com/pingcap/br/issues/565)       | 确保备份时 cluster_index 和恢复时一致，否则会导致数据不一致的问题，如 default not found, 数据索引不一致。
New collation  | [#352](https://github.com/pingcap/br/issues/352)       | 确保备份时集群 new_collation 和恢复时一致，否则会导致数据索引不一致，checksum 不通过。
恢复集群开启 CDC 同步 | [#364](https://github.com/pingcap/br/issues/364#issuecomment-646813965) | BR ingest 的 SST 文件, TiKV 还没实现下推到 CDC，因此使用 BR 恢复时候需要关闭 CDC。

在上述 feature 确保兼容的**前提**下，BR 和 TiKV/TiDB/PD 还可能因为版本内部协议不一致/接口不一致出现不兼容的问题，因此 BR 内置了版本检查。
## 版本检查：
BR 内置版本检查会在执行前，对集群版本和自身版本进行对比检查，如果大版本对不上（比如 BR 4.x 用在 TiDB 5.x 上), 那么会提示退出。但是可以通过设置 `--check-requirements=false` 强行跳过版本检查。 
需要注意的是，跳过检查可能会遇到版本不兼容的问题，现整理如下：

| 备份 \ 恢复| BR nightly / TiDB nightly| BR 5.0 / TiDB 5.0| BR 4.0 / TiDB 4.0 |
|  ----  | ----  | ------| ----- |
**BR nightly / TiDB nightly**|✅| ✅ | ✅ |
**BR 5.0 / TiDB 5.0** | ✅ | ✅ | ✅ |
**BR 4.0 / TiDB 4.0** | ✅ | ✅ | ✅(TiKV>=4.0.0-rc.1(BR [#233](https://github.com/pingcap/br/pull/233) and TiKV not include [#7241](https://github.com/tikv/tikv/pull/7241)), BR will panic TiKV) |
**BR nightly or 5.0 / TiDB 4.0** | ❌(TiDB < 4.0.9 after [#609](https://github.com/pingcap/br/issues/609)) | ❌(TiDB < 4.0.9 after [#609](https://github.com/pingcap/br/issues/609)) | ❌(TiDB < 4.0.9 after [#609](https://github.com/pingcap/br/issues/609)) |




