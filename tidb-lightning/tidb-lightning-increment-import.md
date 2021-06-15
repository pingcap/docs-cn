---
title: TiDB Lightning 增量导入
---

# TiDB Lightning 增量导入

增量导入是指向已经有数据的表中导入数据，TiDB Lightning 的各个后端对增量导入特性的支持如下所示：

| 后端 | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| 支持的 TiDB Lightning 集群版本 | >= v5.1.0 | >= v5.1.0 | 全部 |
| 支持 TiDB 集群版本 | >= v4.0.0 | 全部 | 全部 |
| 导入时是否满足 ACID | 否 | 否 | 是 |
| 是否支持数据校验 | 是 | 是 | 否 |
| 额外组件 | 无 | `tikv-importer` | 无 |
| 是否支持导入重复数据 | 否 | 否 | 是 |

TiDB Lightning 会自动调整 ID 分配器的基准值以确保为设置 AUTO_INCREMENT 等类型的字段分配的值不会重复。同时，在开始导入之前，如果 TiDB Lightning 发现目标表中包含数据，则会首先执行一次 Checksum，确保最终 Checksum 结果的正确性。

TiDB Lightning 总是会检测目标表中是否包含数据，如果包含，则会自动切换至增量导入模式，因此无须执行任何额外操作即可使用此功能。

## 重复数据处理

重复数据是指导入数据的不同行的主键或唯一键的值相同。Local 和 Importer 后端目前不支持对包含重复数据(包含导入的数据文件之间以及导入数据和表内以后数据之间的冲突)，TiDB 后端支持导入包含冲突的数据。

在使用 TiDB Lightning 的 TiDB 后端时，可以通过设置 `tikv-importer.on-duplicate` 配置项指定冲突数据的处理方式。

`tikv-importer.on-duplicate` 各个取值的含义说明：

| on-duplicate | 含义 |
|:---|:---|
| replace (默认值) | 使用新插入的数据替换已存在的数据 |
| ignore | 忽略新插入的数据，保留已存在的数据 |
| error | 返回错误并终止导入 |

## 使用说明

TiDB Lightning 默认支持增量导入，无需增加额外的配置。具体部署和运行流程请参考 [部署执行](/tidb-lightning/deploy-tidb-lightning.md).
