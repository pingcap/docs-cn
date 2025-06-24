---
title: ticloud serverless shell
summary: `ticloud serverless shell` 命令的参考。
aliases: ['/tidbcloud/ticloud-connect']
---

# ticloud serverless shell

连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell [flags]
```

## 示例

在交互模式下连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell
```

在非交互模式下使用默认用户连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell -c <cluster-id>
```

在非交互模式下使用默认用户和密码连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell -c <cluster-id> --password <password>
```

在非交互模式下使用指定用户和密码连接到 TiDB Cloud Serverless 集群：

```shell
ticloud serverless shell -c <cluster-id> -u <user-name> --password <password>
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志               | 描述                                | 是否必需 | 说明                                                 |
|------------------------|-------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                     | 是       | 仅在非交互模式下有效。                               |
| -h, --help             | 显示此命令的帮助信息。              | 否       | 在非交互和交互模式下均有效。                         |
| --password             | 指定用户的密码。                    | 否       | 仅在非交互模式下有效。                               |
| -u, --user string      | 指定登录用户。                      | 否       | 仅在非交互模式下有效。                               |

## 继承的参数标志

| 参数标志              | 描述                                                                                                | 是否必需 | 说明                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                   | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                   | 否       | 在非交互和交互模式下均有效。                                                                           |
| -D, --debug          | 启用调试模式。                                                                                       | 否       | 在非交互和交互模式下均有效。                                                                           |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。
