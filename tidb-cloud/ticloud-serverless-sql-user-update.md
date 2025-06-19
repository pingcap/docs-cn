---
title: ticloud serverless sql-user update
summary: `ticloud serverless sql-user update` 命令的参考。
---

# ticloud serverless sql-user update

更新 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user update [flags]
```

## 示例

在交互模式下更新 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user update
```

在非交互模式下更新 TiDB Cloud Serverless SQL 用户：

```shell
ticloud serverless sql-user update -c <cluster-id> --user <user-name> --password <password> --role <role>
```

## 参数标志

在非交互模式下，你需要手动输入必需的参数标志。在交互模式下，你可以按照 CLI 提示填写它们。

| 参数标志               | 描述                                                                                                | 是否必需 | 说明                                                 |
|------------------------|-----------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | 指定集群的 ID。                                                                                      | 是       | 仅在非交互模式下有效。                               |
| --password string       | 指定 SQL 用户的新密码。                                                                              | 否       | 仅在非交互模式下有效。                               |
| --role strings          | 指定 SQL 用户的新角色。使用此标志会替换现有角色。                                                   | 否       | 仅在非交互模式下有效。                               |
| --add-role strings      | 指定要添加给 SQL 用户的角色。                                                                        | 否       | 仅在非交互模式下有效。                               |
| --delete-role strings   | 指定要从 SQL 用户中删除的角色。                                                                      | 否       | 仅在非交互模式下有效。                               |
| -u, --user string       | 指定要更新的 SQL 用户的名称。                                                                        | 否       | 仅在非交互模式下有效。                               |
| -h, --help             | 显示此命令的帮助信息。                                                                               | 否       | 在非交互和交互模式下均有效。                         |

## 继承的参数标志

| 参数标志              | 描述                                                                                                | 是否必需 | 说明                                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                                   | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                              |
| -P, --profile string | 指定此命令中使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。                   | 否       | 在非交互和交互模式下均有效。                                                                           |
| -D, --debug          | 启用调试模式。                                                                                       | 否       | 在非交互和交互模式下均有效。                                                                           |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何贡献。
