---
title: Import Sample Data
summary: Learn how to import sample data into TiDB Cloud via UI.
---

# Import Sample Data

This document describes how to import the sample data into TiDB Cloud via the UI. The sample data used is the system data from Capital Bikeshare, released under the Capital Bikeshare Data License Agreement. Before importing the sample data, you need to have one TiDB cluster.

1. Open the **Import** page for your target cluster.

    1. Log in to the [TiDB Cloud console](https://tidbcloud.com/) and navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

        > **Tip:**
        >
        > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

    2. Click the name of your target cluster to go to its overview page, and then click **Import** in the left navigation pane.

2. Configure the source data information.

    <SimpleTab>
    <div label="AWS">

    On the **Import** page:

    - For a TiDB Dedicated cluster, click **Import Data** in the upper-right corner.
    - For a TiDB Serverless cluster, click the **import data from S3** link above the upload area.

    Fill in the following parameters:

    - **Data format**: select **SQL File**. TiDB Cloud supports importing compressed files in the following formats: `.gzip`, `.gz`, `.zstd`, `.zst` and `.snappy`. If you want to import compressed SQL files, name the files in the `${db_name}.${table_name}.${suffix}.sql.${compress}` format, in which `${suffix}` is optional and can be any integer such as '000001'. For example, if you want to import the `trips.000001.sql.gz` file to the `bikeshare.trips` table, you can rename the file as `bikeshare.trips.000001.sql.gz`. Note that you only need to compress the data files, not the database or table schema files. The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
    - **Bucket URI**: enter the sample data URI `s3://tidbcloud-sample-data/data-ingestion/`
    - **Bucket Access**: for the sample data, you can only use a Role ARN to access its bucket. For your own data, you can use either an AWS access key or a Role ARN to access your bucket.
        - **AWS Access Keys**: skip this option for the sample data.
        - **AWS Role ARN**: enter `arn:aws:iam::801626783489:role/import-sample-access`

    If the region of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

    </div>

    <div label="Google Cloud">

    If your TiDB cluster is hosted by Google Cloud, click **Import Data** in the upper-right corner, and then fill in the following parameters:

    - **Data Format**: select **SQL File**. TiDB Cloud supports importing compressed files in the following formats: `.gzip`, `.gz`, `.zstd`, `.zst` and `.snappy`. If you want to import compressed SQL files, name the files in the `${db_name}.${table_name}.${suffix}.sql.${compress}` format, in which `${suffix}` is optional and can be any integer such as '000001'. For example, if you want to import the `trips.000001.sql.gz` file to the `bikeshare.trips` table, you can rename the file as `bikeshare.trips.000001.sql.gz`. Note that you only need to compress the data files, not the database or table schema files. Note that you only need to compress the data files, not the database or table schema files. The Snappy compressed file must be in the [official Snappy format](https://github.com/google/snappy). Other variants of Snappy compression are not supported.
    - **Bucket gsutil URI**: enter the sample data URI `gs://tidbcloud-samples-us-west1/`.
    - **Bucket Access**: you can use a GCS IAM Role to access your bucket. For more information, see [Configure GCS access](/tidb-cloud/config-s3-and-gcs-access.md#configure-gcs-access).

    If the region of the bucket is different from your cluster, confirm the compliance of cross region. Click **Next**.

    </div>
    </SimpleTab>

3. You can choose to import into pre-created tables, or import schema and data from the source.

    - **Import into pre-created tables** allows you to create tables in TiDB in advance and select the tables that you want to import data into. In this case, you can choose up to 1000 tables to import. You can click **Chat2Query** in the left navigation pane to create tables. For more information about how to use Chat2Query, see [Explore Your Data with AI-Powered Chat2Query](/tidb-cloud/explore-data-with-chat2query.md).
    - **Import schema and data from S3** (This field is visible only for AWS S3) allows you to import SQL scripts for creating a table and import corresponding table data stored in S3 into TiDB.
    - **Import schema and data from GCS** (This field is visible only for GCS) allows you to import SQL scripts that create a table along with its corresponding data stored in GCS directly into TiDB.

4. Click **Start Import**.

When the data import progress shows **Completed**, you have successfully imported the sample data and the database schema to your database in TiDB Cloud.

Once the cluster finishes the data importing process, you will get the sample data in your database.

After connecting to the cluster, you can run some queries in your terminal to check the result, for example:

1. Get the trip records starting at "12th & U St NW":

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

2. Get the trip records with electric bikes:

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
