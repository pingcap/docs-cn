---
title: Connect to TiDB with Spring Boot
summary: Learn how to connect to TiDB using Spring Boot. This tutorial gives Java sample code snippets that work with TiDB using Spring Boot.
aliases: ['/tidbcloud/dev-guide-sample-application-spring-boot','/tidb/dev/dev-guide-sample-application-spring-boot']
---

# Connect to TiDB with Spring Boot

TiDB is a MySQL-compatible database, and [Spring](https://spring.io/) is a popular open-source container framework for Java. This document uses [Spring Boot](https://spring.io/projects/spring-boot) as the way to use Spring.

In this tutorial, you can learn how to use TiDB along with [Spring Data JPA](https://spring.io/projects/spring-data-jpa) and [Hibernate](https://hibernate.org/orm/) as the JPA provider to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using Hibernate and Spring Data JPA.
- Build and run your application. Optionally, you can find [sample code snippets](#sample-code-snippets) for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- **Java Development Kit (JDK) 17** or higher. You can choose [OpenJDK](https://openjdk.org/) or [Oracle JDK](https://www.oracle.com/hk/java/technologies/downloads/) based on your business and personal requirements.
- [Maven](https://maven.apache.org/install.html) **3.8** or higher.
- [Git](https://git-scm.com/downloads).
- A TiDB cluster.

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

## Run the sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart.git
cd tidb-java-springboot-jpa-quickstart
```

### Step 2: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** matches your environment.

    > **Tip:**
    >
    > If your program is running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.

4. Click **Create password** to create a random password.

    > **Tip:**
    >
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Run the following command to copy `env.sh.example` and rename it to `env.sh`:

    ```shell
    cp env.sh.example env.sh
    ```

6. Copy and paste the corresponding connection string into the `env.sh` file. The example result is as follows:

    ```shell
    export TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. xxxxxx.root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='true'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

    TiDB Serverless requires a secure connection. Therefore, you need to set the value of `USE_SSL` to `true`.

7. Save the `env.sh` file.

</div>
<div label="TiDB Dedicated">

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the CA certificate.

    For more details about how to obtain the connection string, refer to [TiDB Dedicated standard connection](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection).

4. Run the following command to copy `env.sh.example` and rename it to `env.sh`:

    ```shell
    cp env.sh.example env.sh
    ```

5. Copy and paste the corresponding connection string into the `env.sh` file. The example result is as follows:

    ```shell
    export TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    export TIDB_PORT='4000'
    export TIDB_USER='{user}'  # e.g. root
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog.

6. Save the `env.sh` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `env.sh.example` and rename it to `env.sh`:

    ```shell
    cp env.sh.example env.sh
    ```

2. Copy and paste the corresponding connection string into the `env.sh` file. The example result is as follows:

    ```shell
    export TIDB_HOST='{host}'
    export TIDB_PORT='4000'
    export TIDB_USER='root'
    export TIDB_PASSWORD='{password}'
    export TIDB_DB_NAME='test'
    export USE_SSL='false'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters, and set `USE_SSL` to `false`. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `env.sh` file.

</div>
</SimpleTab>

### Step 3: Run the code and check the result

1. Execute the following command to run the sample code:

    ```shell
    make
    ```

2. Run the request script in another terminal session:

    ```shell
    make request
    ```

3. Check the [Expected-Output.txt](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart/blob/main/Expected-Output.txt) to see if the output matches.

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-java-springboot-jpa-quickstart](https://github.com/tidb-samples/tidb-java-springboot-jpa-quickstart) repository.

### Connect to TiDB

Edit the configuration file `application.yml`:

```yaml
spring:
  datasource:
    url: ${TIDB_JDBC_URL:jdbc:mysql://localhost:4000/test}
    username: ${TIDB_USER:root}
    password: ${TIDB_PASSWORD:}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    show-sql: true
    database-platform: org.hibernate.dialect.TiDBDialect
    hibernate:
      ddl-auto: create-drop
```

After configuration, set the environment variables `TIDB_JDBC_URL`, `TIDB_USER`, and `TIDB_PASSWORD` to the actual values of your TiDB cluster. The configuration file provides default settings for these environment variables. If you do not configure the environment variables, the default values are as follows:

- `TIDB_JDBC_URL`: `"jdbc:mysql://localhost:4000/test"`
- `TIDB_USER`: `"root"`
- `TIDB_PASSWORD`: `""`

### Data management: `@Repository`

Spring Data JPA manages data through the `@Repository` interface. To use the CRUD operations provided by `JpaRepository`, you need to extend the `JpaRepository` interface:

```java
@Repository
public interface PlayerRepository extends JpaRepository<PlayerBean, Long> {
}
```

Then, you can use `@Autowired` for automatic dependency injection in any class that requires the `PlayerRepository`. This enables you to directly use CRUD functions. The following is an example:

```java
@Autowired
private PlayerRepository playerRepository;
```

### Insert or update data

```java
playerRepository.save(player);
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md) and [Update data](/develop/dev-guide-update-data.md).

### Query data

```java
PlayerBean player = playerRepository.findById(id).orElse(null);
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Delete data

```java
playerRepository.deleteById(id);
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Next steps

- Learn more usage of Hibernate from [the documentation of Hibernate](https://hibernate.org/orm/documentation).
- Learn more usage about the third-party libraries and frameworks used in this document, refer to their official documentation:

    - [The documentation of Spring Framework](https://spring.io/projects/spring-framework)
    - [The documentation of Spring Boot](https://spring.io/projects/spring-boot)
    - [The documentation of Spring Data JPA](https://spring.io/projects/spring-data-jpa)
    - [The documentation of Hibernate](https://hibernate.org/orm/documentation)

- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.
- Learn through the course for Java developers: [Working with TiDB from Java](https://eng.edu.pingcap.com/catalog/info/id:212).

## Need help?

<CustomContent platform="tidb">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](/support.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

Ask questions on the [Discord](https://discord.gg/DQZ2dy3cuc?utm_source=doc), or [create a support ticket](https://support.pingcap.com/).

</CustomContent>
