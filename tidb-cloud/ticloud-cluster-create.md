---
title: ticloud serverless create
summary: `ticloud serverless create` 命令的参考。
---

# ticloud serverless create

创建 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create [flags]
```

## 示例

在交互模式下创建 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create
```

在非交互模式下创建 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create --display-name <display-name> --region <region>
```

在非交互模式下创建带有支出限制的 TiDB Cloud Serverless 集群：

```shell
ticloud serverless create --display-name <display-name> --region <region> --spending-limit-monthly <spending-limit-monthly>
``` 

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志                      | 描述                                                                                                    | 是否必需 | 说明                                                |
|------------------------------|--------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| -n --display-name string     | 指定要创建的集群的名称。                                                                                | 是       | 仅在非交互模式下有效。                               |
| --spending-limit-monthly int | 指定每月最大支出限制（以美分为单位）。                                                                  | 否       | 仅在非交互模式下有效。                               |
| -p, --project-id string      | 指定要在其中创建集群的项目的 ID。默认值为 `default project`。                                          | 否       | 仅在非交互模式下有效。                               |
| -r, --region string          | 指定云区域的名称。你可以使用 "ticloud serverless region" 查看所有区域。                                | 是       | 仅在非交互模式下有效。                               |
| --disable-public-endpoint    | 禁用公共端点。                                                                                          | 否       | 仅在非交互模式下有效。                               |
| --encryption                 | 启用增强的静态加密。                                                                                    | 否       | 仅在非交互模式下有效。                               |
| -h, --help                   | 显示此命令的帮助信息。                                                                                  | 否       | 在非交互和交互模式下均有效。                         |

## 继承的参数标志

| 参数标志              | 描述                                                                                                | 是否必需 | 说明                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                   | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                   | 否       | 在非交互和交互模式下均有效。                                                                           |
| -D, --debug          | 启用调试模式。                                                                                       | 否       | 在非交互和交互模式下均有效。                                                                           |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。
