---
title: ticloud config use
summary: `ticloud config use` 命令的参考文档。
---

# ticloud config use

将指定的配置文件设置为活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)：

```shell
ticloud config use <profile-name> [flags]
```

## 示例

将 `test` 配置文件设置为活动用户配置文件：

```shell
ticloud config use test
```

## 参数标志

| 参数标志    | 描述                     |
|------------|--------------------------|
| -h, --help | 显示此命令的帮助信息。     |

## 继承的参数标志

| 参数标志              | 描述                                                                                    | 是否必需 | 说明                                                                                      |
|----------------------|----------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------|
| --no-color          | 禁用输出中的颜色。                                                                      | 否       | 仅在非交互模式下有效。在交互模式下，禁用颜色可能对某些 UI 组件不起作用。                      |
| -P, --profile string | 指定此命令使用的活动[用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。          | 否       | 在非交互和交互模式下均可使用。                                                              |
| -D, --debug         | 启用调试模式。                                                                          | 否       | 在非交互和交互模式下均可使用。                                                              |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。同时，我们也欢迎任何形式的贡献。
