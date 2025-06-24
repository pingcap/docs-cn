---
title: 使用知识库
summary: 了解如何通过使用 Chat2Query 知识库 API 来改进 Chat2Query 的查询结果。
---

# 使用知识库

知识库是一组结构化数据的集合，可用于增强 Chat2Query 的 SQL 生成能力。

从 v3 版本开始，Chat2Query API 允许您通过调用 Chat2Query Data App 的知识库相关端点来添加或修改知识库。

> **注意：**
>
> 知识库相关端点默认在 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群上可用。如需在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用知识库相关端点，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。

## 开始之前

在为数据库创建知识库之前，请确保您已经具备以下条件：

- 一个 [Chat2Query Data App](/tidb-cloud/use-chat2query-api.md#create-a-chat2query-data-app)
- 一个 [Chat2Query Data App 的 API 密钥](/tidb-cloud/use-chat2query-api.md#create-an-api-key)

## 步骤 1. 为关联数据库创建知识库

> **注意：**
>
> Chat2Query 使用的知识是**按数据库维度进行组织的**。您可以将多个 Chat2Query Data App 连接到同一个数据库，但每个 Chat2Query Data App 只能使用其关联数据库的知识。

在您的 Chat2Query Data App 中，您可以通过调用 `/v3/knowledgeBases` 端点为特定数据库创建知识库。创建完成后，您将获得一个用于后续知识管理的 `knowledge_base_id`。

以下是调用此端点的通用代码示例。

> **提示：**
>
> 要获取特定端点的代码示例，请在 Data App 左侧窗格中点击端点名称，然后点击 **Show Code Example**。更多信息，请参见[获取端点的示例代码](/tidb-cloud/use-chat2query-api.md#get-the-code-example-of-an-endpoint)。

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases'\
 --header 'content-type: application/json'\
 --data-raw '{
    "cluster_id": "<数据库所属集群的 ID>",
    "database": "<目标数据库的名称>",
    "description": "<您的知识库描述>"
}'
```

示例响应如下：

```json
{
    "code":200,
    "msg":"",
    "result":
        {
            "default":true,
            "description":"",
            "knowledge_base_id":2
        }
}
```

收到响应后，请记录响应中的 `knowledge_base_id` 值，以供后续使用。

## 步骤 2. 选择知识类型

每个数据库的知识库可以包含多种类型的知识。在向知识库添加知识之前，您需要选择最适合您使用场景的知识类型。

目前，Chat2Query 知识库支持以下知识类型。每种类型都是为不同场景专门设计的，并具有独特的知识结构。

- [少样本示例](#少样本示例)
- [术语表解释](#术语表解释)
- [指令](#指令)

### 少样本示例

少样本示例是指提供给 Chat2Query 的问答学习样本，包括示例问题及其对应的答案。这些示例帮助 Chat2Query 更有效地处理新任务。

> **注意：**
>
> 请确保新添加示例的准确性，因为示例质量会影响 Chat2Query 的学习效果。不良示例（如问题和答案不匹配）可能会降低 Chat2Query 在新任务上的表现。

#### 知识结构

每个示例由一个示例问题及其对应答案组成。

例如：

```json
{
    "question": "How many records are in the 'test' table?",
    "answer": "SELECT COUNT(*) FROM `test`;"
}
```

#### 使用场景

少样本示例可以显著提高 Chat2Query 在各种场景下的表现，包括但不限于以下情况：

1. **处理罕见或复杂问题时**：如果 Chat2Query 遇到不常见或复杂的问题，添加少样本示例可以增强其理解能力并提高结果的准确性。

2. **在处理某类问题时遇到困难**：如果 Chat2Query 经常在特定问题上出错或遇到困难，添加少样本示例可以帮助改善其在这些问题上的表现。

### 术语表解释

术语表解释是指对特定术语或一组相似术语的全面解释，帮助 Chat2Query 理解这些术语的含义和用法。

> **注意：**
>
> 请确保新添加术语解释的准确性，因为解释质量会影响 Chat2Query 的学习效果。错误的解释不仅不会改善 Chat2Query 的结果，还可能导致负面影响。

#### 知识结构

每个解释包括单个术语或一组相似术语及其详细描述。

例如：

```json
{
    "term": ["OSS"],
    "description": "OSS Insight 是一个强大的工具，基于近 60 亿行 GitHub 事件数据为用户提供在线数据分析。"
}
```

#### 使用场景

术语表解释主要用于提高 Chat2Query 对用户查询的理解，特别是在以下情况下：

- **处理行业特定术语或缩写**：当您的查询包含可能不被普遍认知的行业特定术语或缩写时，使用术语表解释可以帮助 Chat2Query 理解这些术语的含义和用法。
- **处理用户查询中的歧义**：当您的查询包含令人困惑的模糊概念时，使用术语表解释可以帮助 Chat2Query 澄清这些歧义。
- **处理具有多种含义的术语**：当您的查询包含在不同上下文中具有不同含义的术语时，使用术语表解释可以帮助 Chat2Query 辨别正确的解释。

### 指令

指令是一段文本命令。它用于指导或控制 Chat2Query 的行为，特别是指导它如何根据特定要求或条件生成 SQL。

> **注意：**
>
> - 指令的长度限制为 512 个字符。
> - 请确保提供尽可能清晰和具体的指令，以确保 Chat2Query 能够有效理解和执行指令。

#### 知识结构

指令仅包含一段文本命令。

例如：

```json
{
    "instruction": "如果任务需要计算环比增长率，请在 SQL 中使用带有 OVER 子句的 LAG 函数"
}
```

#### 使用场景

指令可以在许多场景中用于指导 Chat2Query 按照您的要求输出，包括但不限于以下情况：

- **限制查询范围**：如果您希望 SQL 只考虑某些表或列，可以使用指令来指定这一点。
- **指导 SQL 结构**：如果您对 SQL 结构有特定要求，可以使用指令来指导 Chat2Query。

## 步骤 3. 向新创建的知识库添加知识

要添加新知识，您可以调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 端点。

### 添加少样本示例类型的知识

例如，如果您希望 Chat2Query 以特定结构生成计算表中行数的 SQL 语句，您可以通过调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 添加少样本示例类型的知识，如下所示：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases/<knowledge_base_id>/data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "type": "few-shot",
    "meta_data": {},
    "raw_data": {
         "question": "How many records are in the 'test' table?",
         "answer": "SELECT COUNT(*) FROM `test`;"
    }
}'
```

在上述示例代码中，`"type": "few-shot"` 表示少样本示例知识类型。

### 添加术语表解释类型的知识

例如，如果您希望 Chat2Query 使用您提供的解释来理解术语 `OSS` 的含义，您可以通过调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 添加术语表解释类型的知识，如下所示：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases/<knowledge_base_id>/data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "type": "term-sheet",
    "meta_data": {},
    "raw_data": {
        "term": ["OSS"],
        "description": "OSS Insight 是一个强大的工具，基于近 60 亿行 GitHub 事件数据为用户提供在线数据分析。"
    }
}'
```

在上述示例代码中，`"type": "term-sheet"` 表示术语表解释知识类型。

### 添加指令类型的知识

例如，如果您希望 Chat2Query 在处理有关环比增长率计算的问题时始终使用带有 `OVER` 子句的 `LAG` 函数，您可以通过调用 `/v3/knowledgeBases/{knowledge_base_id}/data` 添加指令类型的知识，如下所示：

```bash
curl --digest --user ${PUBLIC_KEY}:${PRIVATE_KEY} --request POST 'https://<region>.data.tidbcloud.com/api/v1beta/app/chat2query-<ID>/endpoint/v3/knowledgeBases/<knowledge_base_id>/data'\
 --header 'content-type: application/json'\
 --data-raw '{
    "type": "instruction",
    "meta_data": {},
    "raw_data": {
        "instruction": "如果任务需要计算环比增长率，请在 SQL 中使用带有 OVER 子句的 LAG 函数"
    }
}'
```

在上述示例代码中，`"type": "instruction"` 表示指令知识类型。
