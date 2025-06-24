---
title: ticloud serverless authorized-network update
summary: `ticloud serverless authorized-network update` 命令的参考。
---

# ticloud serverless authorized-network update

更新授权网络：

```shell
ticloud serverless authorized-network update [flags]
```

## 示例

在交互模式下更新授权网络：

```shell
ticloud serverless authorized-network update
```

在非交互模式下更新授权网络：

```shell
ticloud serverless authorized-network update -c <cluster-id> --start-ip-address <start-ip-address> --end-ip-address <end-ip-address> --new-start-ip-address <new-start-ip-address> --new-end-ip-address <new-end-ip-address>
```

## 标志

在非交互模式下，你需要手动输入必需的标志。在交互模式下，你只需按照 CLI 提示填写即可。

| 标志                    | 描述                              | 是否必需 | 注意                                                 |
|-------------------------|------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。         | 是      | 仅在非交互模式下有效。                  |
| --start-ip-address string          | 指定授权网络的起始 IP 地址。             | 是       | 仅在非交互模式下有效。                  |
| --end-ip-address string          | 指定授权网络的结束 IP 地址。             | 是       | 仅在非交互模式下有效。   |
| --new-display-name string       | 指定授权网络的新名称。            | 否       | 仅在非交互模式下有效。                  |
| --new-start-ip-address string          | 指定授权网络的新起始 IP 地址。             | 否       | 仅在非交互模式下有效。                  |
| --new-end-ip-address string          | 指定授权网络的新结束 IP 地址。             | 否       | 仅在非交互模式下有效。   |
| -h, --help              | 显示此命令的帮助信息。 | 否       | 在非交互和交互模式下都有效。 |

## 继承的标志

| 标志                 | 描述                                                                                          | 是否必需 | 注意                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。 |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。 | 否       | 在非交互和交互模式下都有效。                                                             |
| -D, --debug          | 启用调试模式。                                                                                  | 否       | 在非交互和交互模式下都有效。                                                             |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建[议题](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。
