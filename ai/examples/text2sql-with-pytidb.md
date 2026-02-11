---
title: 文本转 SQL 示例
summary: 使用 AI 模型将自然语言查询转换为 SQL 语句。
---

# 文本转 SQL 示例

本演示展示了如何构建一个由 AI 驱动的 interface，将自然语言问题转换为 SQL 语句，并在 TiDB 上 execute。该示例基于 [`pytidb`](https://github.com/pingcap/pytidb)（TiDB 官方 Python SDK）、OpenAI GPT 和 Streamlit 构建，让你可以用英文直接 query 你的数据库。

## 前置条件

在开始之前，请确保你具备以下条件：

- **Python (>=3.10)**：安装 [Python](https://www.python.org/downloads/) 3.10 或以上版本。
- **TiDB Cloud Starter 集群**：你可以在 [TiDB Cloud](https://tidbcloud.com/free-trial) 上创建一个免费的 TiDB 集群。
- **OpenAI API key**：从 [OpenAI](https://platform.openai.com/api-keys) 获取 OpenAI API key。

## 运行方法

### 第 1 步. 克隆 `pytidb` 仓库

```bash
git clone https://github.com/pingcap/pytidb.git
cd pytidb/examples/text2sql/
```

### 第 2 步. 安装所需依赖包

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r reqs.txt
```

### 第 3 步. 运行 Streamlit 应用

```bash
streamlit run app.py
```

### 第 4 步. 使用应用

打开浏览器并访问 `http://localhost:8501`。

1. 在左侧边栏输入你的 OpenAI API key
2. 在左侧边栏输入 TiDB 连接字符串，例如：`mysql+pymysql://root@localhost:4000/test`

## 相关资源

- **源代码**：[在 GitHub 上查看](https://github.com/pingcap/pytidb/tree/main/examples/text2sql)