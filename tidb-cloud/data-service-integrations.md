---
title: 将 Data App 与第三方工具集成
summary: 了解如何在 TiDB Cloud 控制台中将 TiDB Cloud Data App 与第三方工具（如 GPTs 和 Dify）集成。
---

# 将 Data App 与第三方工具集成

将第三方工具与你的 Data App 集成可以通过第三方工具提供的高级自然语言处理和人工智能（AI）功能来增强你的应用程序。这种集成使你的应用程序能够执行更复杂的任务并提供智能解决方案。

本文档介绍如何在 TiDB Cloud 控制台中将 Data App 与第三方工具（如 GPTs 和 Dify）集成。

## 将 Data App 与 GPTs 集成

你可以将 Data App 与 [GPTs](https://openai.com/blog/introducing-gpts) 集成，为你的应用程序增加智能功能。

要将 Data App 与 GPTs 集成，请执行以下步骤：

1. 导航到项目的 [**Data Service**](https://tidbcloud.com/project/data-service) 页面。
2. 在左侧窗格中，找到目标 Data App，点击目标 Data App 的名称，然后点击**集成**标签。
3. 在**与 GPTs 集成**区域，点击**获取配置**。

    ![获取配置](/media/tidb-cloud/data-service/GPTs1.png)

4. 在显示的对话框中，你可以看到以下字段：

    a. **API 规范 URL**：复制 Data App 的 OpenAPI 规范的 URL。更多信息，请参见[使用 OpenAPI 规范](/tidb-cloud/data-service-manage-data-app.md#use-the-openapi-specification)。

    b. **API 密钥**：输入 Data App 的 API 密钥。如果你还没有 API 密钥，点击**创建 API 密钥**来创建一个。更多信息，请参见[创建 API 密钥](/tidb-cloud/data-service-api-key.md#create-an-api-key)。

    c. **API 密钥编码**：复制与你提供的 API 密钥等效的 base64 编码字符串。

    ![GPTs 对话框](/media/tidb-cloud/data-service/GPTs2.png)

5. 在你的 GPT 配置中使用复制的 API 规范 URL 和编码后的 API 密钥。

## 将 Data App 与 Dify 集成

你可以将 Data App 与 [Dify](https://docs.dify.ai/guides/tools) 集成，为你的应用程序增加智能功能，如向量距离计算、高级相似度搜索和向量分析。

要将 Data App 与 Dify 集成，请按照与 [GPTs 集成](#将-data-app-与-gpts-集成)相同的步骤操作。唯一的区别是在**集成**标签页上，你需要在**与 Dify 集成**区域点击**获取配置**。
