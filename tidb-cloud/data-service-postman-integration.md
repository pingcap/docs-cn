---
title: 在 Postman 中运行数据应用
summary: 了解如何在 Postman 中运行数据应用。
---

# 在 Postman 中运行数据应用

[Postman](https://www.postman.com/) 是一个 API 平台，它简化了 API 生命周期并增强了协作，以实现更快更好的 API 开发。

在 TiDB Cloud [数据服务](https://tidbcloud.com/project/data-service)中，你可以轻松地将数据应用导入到 Postman，并利用 Postman 的丰富工具来增强你的 API 开发体验。

本文档描述如何将数据应用导入到 Postman 以及如何在 Postman 中运行数据应用。

## 开始之前

在将数据应用导入到 Postman 之前，请确保你具有以下条件：

- 一个 [Postman](https://www.postman.com/) 账户
- 一个 [Postman 桌面应用](https://www.postman.com/downloads)（可选）。或者，你可以使用 Postman 网页版而无需下载应用。
- 一个至少具有一个定义完善的[端点](/tidb-cloud/data-service-manage-endpoint.md)的[数据应用](/tidb-cloud/data-service-manage-data-app.md)。只有满足以下要求的端点才能导入到 Postman：

    - 已选择目标集群。
    - 已配置端点路径和请求方法。
    - 已编写 SQL 语句。

- 数据应用的 [API 密钥](/tidb-cloud/data-service-api-key.md#创建-api-密钥)。

## 步骤 1. 将数据应用导入到 Postman

要将数据应用导入到 Postman，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，导航到项目的[**数据服务**](https://tidbcloud.com/project/data-service)页面。
2. 在左侧窗格中，点击目标数据应用的名称以查看其详细信息。
3. 在页面右上角，点击**在 Postman 中运行**。此时会显示一个包含导入说明的对话框。

    > **注意：**
    >
    > - 如果数据应用缺少定义完善的端点（已配置目标集群、路径、请求方法和 SQL 语句），则该数据应用的**在 Postman 中运行**按钮将保持禁用状态。
    > - Chat2Query 数据应用不提供**在 Postman 中运行**功能。

4. 按照对话框中提供的步骤导入数据应用：

    1. 根据你的偏好，选择**在 Postman 网页版中运行**或**在 Postman 桌面版中运行**以打开你的 Postman 工作区，然后选择目标工作区。

        - 如果你尚未登录 Postman，请按照屏幕上的说明先登录 Postman。
        - 如果你点击了**在 Postman 桌面版中运行**，请按照屏幕上的说明启动 Postman 桌面应用。

    2. 在 Postman 中的目标工作区页面上，点击左侧导航菜单中的**导入**。
    3. 从 TiDB Cloud 对话框中复制数据应用 URL，然后将 URL 粘贴到 Postman 中进行导入。

5. 粘贴 URL 后，Postman 会自动将数据应用作为新的[集合](https://learning.postman.com/docs/collections/collections-overview)导入。集合的名称格式为 `TiDB Data Service - <你的应用名称>`。

    在集合中，已部署的端点被分组在 **Deployed** 文件夹下，未部署的端点被分组在 **Draft** 文件夹下。

## 步骤 2. 在 Postman 中配置数据应用的 API 密钥

在 Postman 中运行导入的数据应用之前，你需要在 Postman 中配置数据应用的 API 密钥，步骤如下：

1. 在 Postman 的左侧导航菜单中，点击 `TiDB Data Service - <你的应用名称>` 以在右侧打开一个标签页。
2. 在 `TiDB Data Service - <你的应用名称>` 标签页下，点击 **Variables** 标签。
3. 在变量表中，在 **Current value** 列中输入数据应用的公钥和私钥。
4. 在 `TiDB Data Service - <你的应用名称>` 标签页的右上角，点击**保存**。

## 步骤 3. 在 Postman 中运行数据应用

要在 Postman 中运行数据应用，请执行以下步骤：

1. 在 Postman 的左侧导航窗格中，展开 **Deployed** 或 **Draft** 文件夹，然后点击你的端点名称以在右侧打开一个标签页。
2. 在 `<你的端点名称>` 标签页下，你可以按以下方式调用端点：

    - 对于没有参数的端点，你可以直接点击**发送**来调用它。
    - 对于有参数的端点，你需要先填写参数值，然后点击**发送**。

        - 对于 `GET` 或 `DELETE` 请求，在 **Query Params** 表中填写参数值。
        - 对于 `POST` 或 `PUT` 请求，点击 **Body** 标签，然后将参数值作为 JSON 对象填写。如果在 TiDB Cloud 数据服务中为端点启用了**批量操作**，则将参数值作为 JSON 对象数组填写到 `items` 字段中。

3. 在下方窗格中查看响应。

4. 如果你想使用不同的参数值再次调用端点，可以相应地编辑参数值，然后再次点击**发送**。

要了解更多关于 Postman 的使用方法，请参见 [Postman 文档](https://learning.postman.com/docs)。

## 处理数据应用中的新变更

将数据应用导入到 Postman 后，TiDB Cloud 数据服务不会自动将数据应用的新变更同步到 Postman。

如果你想让任何新变更在 Postman 中反映出来，你必须再次[按照导入流程](#步骤-1-将数据应用导入到-postman)操作。由于集合名称在 Postman 工作区中是唯一的，你可以使用最新的数据应用替换之前导入的应用，或者将最新的数据应用作为新集合导入。

此外，重新导入数据应用后，你还需要在 Postman 中再次[为新导入的应用配置 API 密钥](#步骤-2-在-postman-中配置数据应用的-api-密钥)。
