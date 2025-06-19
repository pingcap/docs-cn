---
title: 导入示例数据到 TiDB Cloud Dedicated
summary: 了解如何通过 UI 将示例数据导入到 TiDB Cloud Dedicated。
---

# 导入示例数据到 TiDB Cloud Dedicated

本文介绍如何通过 UI 将示例数据导入到 TiDB Cloud Dedicated。使用的示例数据是 Capital Bikeshare 的系统数据，根据 Capital Bikeshare 数据许可协议发布。在导入示例数据之前，你需要有一个 TiDB 集群。

<SimpleTab>
<div label="Amazon S3">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**。

3. 在**从 Amazon S3 导入数据**页面上，配置以下源数据信息：

    - **包含架构文件**：对于示例数据，选择**是**。
    - **数据格式**：选择 **SQL**。
    - **文件夹 URI** 或**文件 URI**：输入示例数据 URI `s3://tidbcloud-sample-data/data-ingestion/`。
    - **存储桶访问**：对于示例数据，你只能使用 Role ARN 访问其存储桶。对于你自己的数据，你可以使用 AWS 访问密钥或 Role ARN 访问你的存储桶。
        - **AWS Role ARN**：输入 `arn:aws:iam::801626783489:role/import-sample-access`。
        - **AWS 访问密钥**：对于示例数据，跳过此选项。

4. 点击**连接** > **开始导入**。

</div>
<div label="Google Cloud">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**。

3. 在**从 GCS 导入数据**页面上，配置以下源数据信息：

    - **包含架构文件**：对于示例数据，选择**是**。
    - **数据格式**：选择 **SQL**。
    - **文件夹 URI** 或**文件 URI**：输入示例数据 URI `gs://tidbcloud-samples-us-west1/`。
    - **存储桶访问**：你可以使用 GCS IAM 角色访问你的存储桶。更多信息，请参见[配置 GCS 访问](/tidb-cloud/dedicated-external-storage.md#configure-gcs-access)。

    如果存储桶的区域与你的集群不同，请确认跨区域合规性。

4. 点击**连接** > **开始导入**。

</div>

<div label="Azure Blob Storage">

1. 打开目标集群的**导入**页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)并导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

        > **提示：**
        >
        > 你可以使用左上角的组合框在组织、项目和集群之间切换。

    2. 点击目标集群的名称进入其概览页面，然后在左侧导航栏中点击**数据** > **导入**。

2. 选择**从云存储导入数据**。

3. 在**从 Azure Blob Storage 导入数据**页面上，配置以下源数据信息：

    - **包含架构文件**：对于示例数据，选择**是**。
    - **数据格式**：选择 **SQL**。
    - **文件夹 URI**：输入示例数据 URI `https://tcidmsampledata.blob.core.windows.net/sql/`。
    - **SAS 令牌**：
        - 对于示例数据，使用以下 **SAS 令牌**：`sv=2015-04-05&ss=b&srt=co&sp=rl&se=2099-03-01T00%3A00%3A01.0000000Z&sig=cQHvaofmVsUJEbgyf4JFkAwTJGsFOmbQHx03GvVMrNc%3D`。
        - 对于你自己的数据，你可以使用 SAS 令牌访问你的 Azure Blob Storage。更多信息，请参见[配置 Azure Blob Storage 访问](/tidb-cloud/dedicated-external-storage.md#configure-azure-blob-storage-access)。

    如果存储账户的区域与你的集群不同，请确认跨区域合规性。

4. 点击**连接** > **开始导入**。

</div>
</SimpleTab>

当数据导入进度显示**已完成**时，你已成功将示例数据和数据库架构导入到 TiDB Cloud 中的数据库。

连接到集群后，你可以在终端中运行一些查询来检查结果，例如：

1. 获取起始站为 "12th & U St NW" 的行程记录：

    ```sql
    use bikeshare;
    ```

    ```sql
    select * from `trips` where start_station_name='12th & U St NW' limit 10;
    ```

    ```sql
    +-----------------+---------------+---------------------+---------------------+--------------------+------------------+-------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | ride_id         | rideable_type | started_at          | ended_at            | start_station_name | start_station_id | end_station_name                          | end_station_id | start_lat | start_lng  | end_lat   | end_lng    | member_casual |
    +-----------------+---------------+---------------------+---------------------+--------------------+------------------+-------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | E291FF5018      | classic_bike  | 2021-01-02 11:12:38 | 2021-01-02 11:23:47 | 12th & U St NW     |            31268 | 7th & F St NW / National Portrait Gallery |          31232 | 38.916786 |  -77.02814 |  38.89728 | -77.022194 | member        |
    | E76F3605D0      | docked_bike   | 2020-09-13 00:44:11 | 2020-09-13 00:59:38 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | casual        |
    | FFF0B75414      | docked_bike   | 2020-09-28 16:47:53 | 2020-09-28 16:57:30 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | casual        |
    | C3F2C16949      | docked_bike   | 2020-09-13 00:42:03 | 2020-09-13 00:59:43 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | casual        |
    | 1C7EC91629      | docked_bike   | 2020-09-28 16:47:49 | 2020-09-28 16:57:26 | 12th & U St NW     |            31268 | 17th St & Massachusetts Ave NW            |          31267 | 38.916786 |  -77.02814 | 38.908142 |  -77.03836 | member        |
    | A3A38BCACA      | classic_bike  | 2021-01-14 09:52:53 | 2021-01-14 10:00:51 | 12th & U St NW     |            31268 | 10th & E St NW                            |          31256 | 38.916786 |  -77.02814 | 38.895912 |  -77.02606 | member        |
    | EC4943257E      | electric_bike | 2021-01-28 10:06:52 | 2021-01-28 10:16:28 | 12th & U St NW     |            31268 | 10th & E St NW                            |          31256 | 38.916843 | -77.028206 |  38.89607 |  -77.02608 | member        |
    | D4070FBFA7      | classic_bike  | 2021-01-12 09:50:51 | 2021-01-12 09:59:41 | 12th & U St NW     |            31268 | 10th & E St NW                            |          31256 | 38.916786 |  -77.02814 | 38.895912 |  -77.02606 | member        |
    | 6EABEF3CAB      | classic_bike  | 2021-01-09 15:00:43 | 2021-01-09 15:18:30 | 12th & U St NW     |            31268 | 1st & M St NE                             |          31603 | 38.916786 |  -77.02814 | 38.905697 | -77.005486 | member        |
    | 2F5CC89018      | electric_bike | 2021-01-02 01:47:07 | 2021-01-02 01:58:29 | 12th & U St NW     |            31268 | 3rd & H St NE                             |          31616 | 38.916836 |  -77.02815 |  38.90074 |  -77.00219 | member        |
    +-----------------+---------------+---------------------+---------------------+--------------------+------------------+-------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    ```

2. 获取电动自行车的行程记录：

    ```sql
    use bikeshare;
    ```

    ```sql
    select * from `trips` where rideable_type="electric_bike" limit 10;
    ```

    ```sql
    +------------------+---------------+---------------------+---------------------+----------------------------------------+------------------+-------------------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | ride_id          | rideable_type | started_at          | ended_at            | start_station_name                     | start_station_id | end_station_name                                      | end_station_id | start_lat | start_lng  | end_lat   | end_lng    | member_casual |
    +------------------+---------------+---------------------+---------------------+----------------------------------------+------------------+-------------------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    | AF15B12839DA4367 | electric_bike | 2021-01-23 14:50:46 | 2021-01-23 14:59:55 | Columbus Circle / Union Station        |            31623 | 15th & East Capitol St NE                             |          31630 |   38.8974 |  -77.00481 | 38.890    | 76.98354   | member        |
    | 7173E217338C4752 | electric_bike | 2021-01-15 08:28:38 | 2021-01-15 08:33:49 | 37th & O St NW / Georgetown University |            31236 | 34th St & Wisconsin Ave NW                            |          31226 | 38.907825 | -77.071655 | 38.916    | -77.0683   | member        |
    | E665505ED621D1AB | electric_bike | 2021-01-05 13:25:47 | 2021-01-05 13:35:58 | N Lynn St & Fairfax Dr                 |            31917 | 34th St & Wisconsin Ave NW                            |          31226 |  38.89359 |  -77.07089 | 38.916    | 77.06829   | member        |
    | 646AFE266A6375AF | electric_bike | 2021-01-16 00:08:10 | 2021-01-16 00:35:58 | 7th St & Massachusetts Ave NE          |            31647 | 34th St & Wisconsin Ave NW                            |          31226 | 38.892235 | -76.996025 |  38.91    | 7.068245   | member        |
    | 40CDDA0378E45736 | electric_bike | 2021-01-03 11:14:50 | 2021-01-03 11:26:04 | N Lynn St & Fairfax Dr                 |            31917 | 34th St & Wisconsin Ave NW                            |          31226 | 38.893734 |  -77.07096 | 38.916    | 7.068275   | member        |
    | E0A7DDB0CE680C01 | electric_bike | 2021-01-05 18:18:17 | 2021-01-05 19:04:11 | Maine Ave & 7th St SW                  |            31609 | Smithsonian-National Mall / Jefferson Dr & 12th St SW |          31248 | 38.878727 |  -77.02304 |   38.8    | 7.028755   | casual        |
    | 71BDF35029AF0039 | electric_bike | 2021-01-07 10:23:57 | 2021-01-07 10:59:43 | 10th & K St NW                         |            31263 | East West Hwy & Blair Mill Rd                         |          32019 |  38.90279 |  -77.02633 | 38.990    | 77.02937   | member        |
    | D5EACDF488260A61 | electric_bike | 2021-01-13 20:57:23 | 2021-01-13 21:04:19 | 8th & H St NE                          |            31661 | 15th & East Capitol St NE                             |          31630 |  38.89985 | -76.994835 |  38.88    | 76.98345   | member        |
    | 211D449363FB7EE3 | electric_bike | 2021-01-15 17:22:02 | 2021-01-15 17:35:49 | 7th & K St NW                          |            31653 | 15th & East Capitol St NE                             |          31630 |  38.90216 |   -77.0211 |  38.88    | 76.98357   | casual        |
    | CE667578A7291701 | electric_bike | 2021-01-15 16:55:12 | 2021-01-15 17:38:26 | East West Hwy & 16th St                |            32056 | East West Hwy & Blair Mill Rd                         |          32019 | 38.995674 |  -77.03868 | 38.990    | 77.02953   | casual        |
    +------------------+---------------+---------------------+---------------------+----------------------------------------+------------------+-------------------------------------------------------+----------------+-----------+------------+-----------+------------+---------------+
    ```
