---
title: 将本地文件导入到 TiDB Cloud Serverless
summary: 了解如何将本地文件导入到 TiDB Cloud Serverless。
---

# 将本地文件导入到 TiDB Cloud Serverless

你可以直接将本地文件导入到 TiDB Cloud Serverless。只需点击几下即可完成任务配置，然后你的本地 CSV 数据将快速导入到你的 TiDB 集群。使用此方法，你无需提供云存储和凭证。整个导入过程快速流畅。

目前，此方法支持在一个任务中将一个 CSV 文件导入到一个空的现有表或新表中。

## 限制

- 目前，TiDB Cloud 仅支持在一个任务中导入大小在 250 MiB 以内的 CSV 格式本地文件。
- 导入本地文件仅支持 TiDB Cloud Serverless 集群，不支持 TiDB Cloud Dedicated 集群。
- 你不能同时运行多个导入任务。

## 导入本地文件

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 在**导入**页面，你可以直接将本地文件拖放到上传区域，或点击**上传本地文件**选择并上传目标本地文件。注意，一个任务只能上传一个小于 250 MiB 的 CSV 文件。如果你的本地文件大于 250 MiB，请参见[如何导入大于 250 MiB 的本地文件？](#如何导入大于-250-mib-的本地文件)。

3. 在**目标**部分，选择目标数据库和目标表，或直接输入名称创建新的数据库或新表。名称只能包含 Unicode BMP（基本多语言平面）中的字符，不包括空字符 `\u0000` 和空白字符，长度最多为 64 个字符。点击**定义表**，将显示**表定义**部分。

4. 检查表。

    你可以看到可配置的表列列表。每行显示 TiDB Cloud 推断的表列名、推断的表列类型以及 CSV 文件中的预览数据。

    - 如果你将数据导入到 TiDB Cloud 中的现有表，列列表是从表定义中提取的，预览数据通过列名映射到相应的列。

    - 如果你要创建新表，列列表是从 CSV 文件中提取的，列类型由 TiDB Cloud 推断。例如，如果预览数据都是整数，推断的列类型将是整数。

5. 配置列名和数据类型。

    如果 CSV 文件中的第一行记录了列名，请确保选中**使用第一行作为列名**，该选项默认是选中的。

    如果 CSV 文件没有列名行，请不要选中**使用第一行作为列名**。在这种情况下：

    - 如果目标表已存在，CSV 文件中的列将按顺序导入到目标表中。多余的列将被截断，缺少的列将填充默认值。

    - 如果你需要 TiDB Cloud 创建目标表，请为每列输入名称。列名必须满足以下要求：

        * 名称必须由 Unicode BMP 中的字符组成，不包括空字符 `\u0000` 和空白字符。
        * 名称长度必须小于 65 个字符。

        如果需要，你也可以更改数据类型。

    > **注意：**
    >
    > 当你将 CSV 文件导入到 TiDB Cloud 中的现有表，且目标表的列数多于源文件时，多余的列的处理方式取决于具体情况：
    > - 如果多余的列不是主键或唯一键，不会报错。相反，这些多余的列将填充其[默认值](/data-type-default-values.md)。
    > - 如果多余的列是主键或唯一键，且没有 `auto_increment` 或 `auto_random` 属性，将会报错。在这种情况下，建议你选择以下策略之一：
    >   - 提供包含这些主键或唯一键列的源文件。
    >   - 修改目标表的主键和唯一键列以匹配源文件中的现有列。
    >   - 将主键或唯一键列的属性设置为 `auto_increment` 或 `auto_random`。

6. 对于新的目标表，你可以设置主键。你可以选择一列作为主键，或选择多列创建复合主键。复合主键将按照你选择列名的顺序形成。

    > **注意：**
    >
    > 表的主键是聚簇索引，创建后不能删除。

7. 如果需要，编辑 CSV 配置。

   你还可以点击**编辑 CSV 配置**来配置反斜杠转义、分隔符和定界符，以实现更精细的控制。有关 CSV 配置的更多信息，请参见 [CSV 导入数据配置](/tidb-cloud/csv-config-for-import-data.md)。

8. 点击**开始导入**。

    你可以在**导入任务详情**页面查看导入进度。如果有警告或失败的任务，你可以查看详情并解决它们。

9. 导入任务完成后，你可以点击**使用 SQL 编辑器探索数据**来查询导入的数据。有关如何使用 SQL 编辑器的更多信息，请参见[使用 AI 辅助的 SQL 编辑器探索数据](/tidb-cloud/explore-data-with-chat2query.md)。

10. 在**导入**页面，你可以在**操作**列中点击 **...** > **查看**来检查导入任务详情。

## 常见问题

### 我可以只使用 TiDB Cloud 的导入功能导入指定的列吗？

不可以。目前，使用导入功能时，你只能将 CSV 文件的所有列导入到现有表中。

要只导入指定的列，你可以使用 MySQL 客户端连接你的 TiDB 集群，然后使用 [`LOAD DATA`](https://docs.pingcap.com/tidb/stable/sql-statement-load-data) 指定要导入的列。例如：

```sql
CREATE TABLE `import_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `address` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
LOAD DATA LOCAL INFILE 'load.txt' INTO TABLE import_test FIELDS TERMINATED BY ',' (name, address);
```

如果你使用 `mysql` 并遇到 `ERROR 2068 (HY000): LOAD DATA LOCAL INFILE file request rejected due to restrictions on access.`，你可以在连接字符串中添加 `--local-infile=true`。

### 为什么导入数据到 TiDB Cloud 后无法查询带有保留关键字的列？

如果列名是 TiDB 中的保留[关键字](/keywords.md)，当你查询该列时，需要添加反引号 `` ` `` 来包围列名。例如，如果列名是 `order`，你需要使用 `` `order` `` 来查询该列。

### 如何导入大于 250 MiB 的本地文件？

如果文件大于 250 MiB，你可以使用 [TiDB Cloud CLI](/tidb-cloud/get-started-with-cli.md) 来导入文件。更多信息，请参见 [`ticloud serverless import start`](/tidb-cloud/ticloud-import-start.md)。

或者，你可以使用 `split [-l ${line_count}]` 工具将其分割成多个较小的文件（仅适用于 Linux 或 macOS）。例如，运行 `split -l 100000 tidb-01.csv small_files` 将名为 `tidb-01.csv` 的文件按行长度 `100000` 分割，分割后的文件命名为 `small_files${suffix}`。然后，你可以将这些较小的文件逐个导入到 TiDB Cloud。

参考以下脚本：

```bash
#!/bin/bash
n=$1
file_path=$2
file_extension="${file_path##*.}"
file_name="${file_path%.*}"
total_lines=$(wc -l < $file_path)
lines_per_file=$(( (total_lines + n - 1) / n ))
split -d -a 1 -l $lines_per_file $file_path $file_name.
for (( i=0; i<$n; i++ ))
do
    mv $file_name.$i $file_name.$i.$file_extension
done
```

你可以输入 `n` 和文件名，然后运行脚本。脚本将文件平均分成 `n` 份，同时保持原始文件扩展名。例如：

```bash
> sh ./split.sh 3 mytest.customer.csv
> ls -h | grep mytest
mytest.customer.0.csv
mytest.customer.1.csv
mytest.customer.2.csv
mytest.customer.csv
```
