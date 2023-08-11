---
title: Build a Simple CRUD App with TiDB and MyBatis
summary: Learn how to build a simple CRUD application with TiDB and MyBatis.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a Simple CRUD App with TiDB and MyBatis

[MyBatis](https://mybatis.org/mybatis-3/index.html) is a popular open-source Java class persistence framework.

This document describes how to use TiDB and MyBatis to build a simple CRUD application.

> **Note:**
>
> It is recommended to use Java 8 or a later Java version.

## Step 1. Launch your TiDB cluster

<CustomContent platform="tidb">

The following introduces how to start a TiDB cluster.

**Use a TiDB Serverless cluster**

For detailed steps, see [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

**Use a local cluster**

For detailed steps, see [Deploy a local test cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md).

</CustomContent>

<CustomContent platform="tidb-cloud">

See [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster).

</CustomContent>

## Step 2. Get the code

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

Compared with [MyBatis](https://mybatis.org/mybatis-3/index.html), the JDBC implementation might be not a best practice, because you need to write error handling logic manually and cannot reuse code easily, which makes your code slightly redundant.

The following uses [MyBatis Generator](https://mybatis.org/generator/quickstart.html) as a Maven plugin to generate the persistence layer code.

Change to the `plain-java-mybatis` directory:

```shell
cd plain-java-mybatis
```

The structure of this directory is as follows:

```
.
├── Makefile
├── pom.xml
└── src
    └── main
        ├── java
        │   └── com
        │       └── pingcap
        │           ├── MybatisExample.java
        │           ├── dao
        │           │   └── PlayerDAO.java
        │           └── model
        │               ├── Player.java
        │               ├── PlayerMapper.java
        │               └── PlayerMapperEx.java
        └── resources
            ├── dbinit.sql
            ├── log4j.properties
            ├── mapper
            │   ├── PlayerMapper.xml
            │   └── PlayerMapperEx.xml
            ├── mybatis-config.xml
            └── mybatis-generator.xml
```

The automatically generated files are:

- `src/main/java/com/pingcap/model/Player.java`: The `Player` entity class.
- `src/main/java/com/pingcap/model/PlayerMapper.java`: The interface of `PlayerMapper`.
- `src/main/resources/mapper/PlayerMapper.xml`: The XML mapping of `Player`. MyBatis uses this configuration to automatically generate the implementation class of the `PlayerMapper` interface.

The strategy for generating these files is written in `mybatis-generator.xml`, which is the configuration file for [MyBatis Generator](https://mybatis.org/generator/quickstart.html). There are comments in the following configuration file to describe how to use it.

```xml
<!DOCTYPE generatorConfiguration PUBLIC
 "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
 "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">

<generatorConfiguration>
    <!--
        <context/> entire document: https://mybatis.org/generator/configreference/context.html

        context.id: A unique identifier you like
        context.targetRuntime: Used to specify the runtime target for generated code.
            It has MyBatis3DynamicSql / MyBatis3Kotlin / MyBatis3 / MyBatis3Simple 4 selection to choice.
    -->
    <context id="simple" targetRuntime="MyBatis3">
        <!--
            <commentGenerator/> entire document: https://mybatis.org/generator/configreference/commentGenerator.html

            commentGenerator:
                - property(suppressDate): remove timestamp in comments
                - property(suppressAllComments): remove all comments
        -->
        <commentGenerator>
            <property name="suppressDate" value="true"/>
            <property name="suppressAllComments" value="true" />
        </commentGenerator>

        <!--
            <jdbcConnection/> entire document: https://mybatis.org/generator/configreference/jdbcConnection.html

            jdbcConnection.driverClass: The fully qualified class name for the JDBC driver used to access the database.
                Used mysql-connector-java:5.1.49, should specify JDBC is com.mysql.jdbc.Driver
            jdbcConnection.connectionURL: The JDBC connection URL used to access the database.
        -->
        <jdbcConnection driverClass="com.mysql.jdbc.Driver"
            connectionURL="jdbc:mysql://localhost:4000/test?user=root" />

        <!--
            <javaModelGenerator/> entire document: https://mybatis.org/generator/configreference/javaModelGenerator.html
            Model code file will be generated at ${targetProject}/${targetPackage}

            javaModelGenerator:
                - property(constructorBased): If it's true, generator will create constructor function in model
        -->
        <javaModelGenerator targetPackage="com.pingcap.model" targetProject="src/main/java">
            <property name="constructorBased" value="true"/>
        </javaModelGenerator>

        <!--
            <sqlMapGenerator/> entire document: https://mybatis.org/generator/configreference/sqlMapGenerator.html
            XML SQL mapper file will be generated at ${targetProject}/${targetPackage}
        -->
        <sqlMapGenerator targetPackage="." targetProject="src/main/resources/mapper"/>

        <!--
            <javaClientGenerator/> entire document: https://mybatis.org/generator/configreference/javaClientGenerator.html
            Java code mapper interface file will be generated at ${targetProject}/${targetPackage}

            javaClientGenerator.type (context.targetRuntime is MyBatis3):
                This attribute indicated MyBatis how to implement interface.
                It has ANNOTATEDMAPPER / MIXEDMAPPER / XMLMAPPER 3 selection to choice.
        -->
        <javaClientGenerator type="XMLMAPPER" targetPackage="com.pingcap.model" targetProject="src/main/java"/>

        <!--
            <table/> entire document: https://mybatis.org/generator/configreference/table.html

            table.tableName: The name of the database table.
            table.domainObjectName: The base name from which generated object names will be generated. If not specified, MBG will generate a name automatically based on the tableName.
            table.enableCountByExample: Signifies whether a count by example statement should be generated.
            table.enableUpdateByExample: Signifies whether an update by example statement should be generated.
            table.enableDeleteByExample: Signifies whether a delete by example statement should be generated.
            table.enableSelectByExample: Signifies whether a select by example statement should be generated.
            table.selectByExampleQueryId: This value will be added to the select list of the select by example statement in this form: "'<value>' as QUERYID".
        -->
        <table tableName="player" domainObjectName="Player"
               enableCountByExample="false" enableUpdateByExample="false"
               enableDeleteByExample="false" enableSelectByExample="false"
               selectByExampleQueryId="false"/>
    </context>
</generatorConfiguration>
```

`mybatis-generator.xml` is included in `pom.xml` as the configuration of `mybatis-generator-maven-plugin`.

```xml
<plugin>
    <groupId>org.mybatis.generator</groupId>
    <artifactId>mybatis-generator-maven-plugin</artifactId>
    <version>1.4.1</version>
    <configuration>
        <configurationFile>src/main/resources/mybatis-generator.xml</configurationFile>
        <verbose>true</verbose>
        <overwrite>true</overwrite>
    </configuration>

    <dependencies>
        <!-- https://mvnrepository.com/artifact/mysql/mysql-connector-java -->
        <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>5.1.49</version>
        </dependency>
    </dependencies>
</plugin>
```

Once included in the Maven plugin, you can delete the old generated files and make new ones using `mvn mybatis-generate`. Or you can use `make gen` to delete the old file and generate a new one at the same time.

> **Note:**
>
> The property `configuration.overwrite` in `mybatis-generator.xml` only ensures that the generated Java code files are overwritten. But the XML mapping files are still written as appended. Therefore, it is recommended to delete the old file before Mybaits Generator generating a new one.

`Player.java` is a data entity class file generated using MyBatis Generator, which is a mapping of database tables in the application. Each property of the `Player` class corresponds to a field in the `player` table.

```java
package com.pingcap.model;

public class Player {
    private String id;

    private Integer coins;

    private Integer goods;

    public Player(String id, Integer coins, Integer goods) {
        this.id = id;
        this.coins = coins;
        this.goods = goods;
    }

    public Player() {
        super();
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Integer getCoins() {
        return coins;
    }

    public void setCoins(Integer coins) {
        this.coins = coins;
    }

    public Integer getGoods() {
        return goods;
    }

    public void setGoods(Integer goods) {
        this.goods = goods;
    }
}
```

`PlayerMapper.java` is a mapping interface file generated using MyBatis Generator. This file only defines the interface, and the implementation classes of interface are automatically generated using XML or annotations.

```java
package com.pingcap.model;

import com.pingcap.model.Player;

public interface PlayerMapper {
    int deleteByPrimaryKey(String id);

    int insert(Player row);

    int insertSelective(Player row);

    Player selectByPrimaryKey(String id);

    int updateByPrimaryKeySelective(Player row);

    int updateByPrimaryKey(Player row);
}
```

`PlayerMapper.xml` is a mapping XML file generated using MyBatis Generator. MyBatis uses this to automatically generate the implementation class of the `PlayerMapper` interface.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapper">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>
  <select id="selectByPrimaryKey" parameterType="java.lang.String" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from player
    where id = #{id,jdbcType=VARCHAR}
  </select>
  <delete id="deleteByPrimaryKey" parameterType="java.lang.String">
    delete from player
    where id = #{id,jdbcType=VARCHAR}
  </delete>
  <insert id="insert" parameterType="com.pingcap.model.Player">
    insert into player (id, coins, goods
      )
    values (#{id,jdbcType=VARCHAR}, #{coins,jdbcType=INTEGER}, #{goods,jdbcType=INTEGER}
      )
  </insert>
  <insert id="insertSelective" parameterType="com.pingcap.model.Player">
    insert into player
    <trim prefix="(" suffix=")" suffixOverrides=",">
      <if test="id != null">
        id,
      </if>
      <if test="coins != null">
        coins,
      </if>
      <if test="goods != null">
        goods,
      </if>
    </trim>
    <trim prefix="values (" suffix=")" suffixOverrides=",">
      <if test="id != null">
        #{id,jdbcType=VARCHAR},
      </if>
      <if test="coins != null">
        #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        #{goods,jdbcType=INTEGER},
      </if>
    </trim>
  </insert>
  <update id="updateByPrimaryKeySelective" parameterType="com.pingcap.model.Player">
    update player
    <set>
      <if test="coins != null">
        coins = #{coins,jdbcType=INTEGER},
      </if>
      <if test="goods != null">
        goods = #{goods,jdbcType=INTEGER},
      </if>
    </set>
    where id = #{id,jdbcType=VARCHAR}
  </update>
  <update id="updateByPrimaryKey" parameterType="com.pingcap.model.Player">
    update player
    set coins = #{coins,jdbcType=INTEGER},
      goods = #{goods,jdbcType=INTEGER}
    where id = #{id,jdbcType=VARCHAR}
  </update>
</mapper>
```

Since MyBatis Generator needs to generate the source code from the table definition, the table needs to be created first. To create the table, you can use `dbinit.sql`.

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
    PRIMARY KEY (`id`)
);
```

Split the interface `PlayerMapperEx` additionally to extend from `PlayerMapper` and write a matching `PlayerMapperEx.xml` file. Avoid changing `PlayerMapper.java` and `PlayerMapper.xml` directly. This is to avoid overwrite by MyBatis Generator.

Define the added interface in `PlayerMapperEx.java`:

```java
package com.pingcap.model;

import java.util.List;

public interface PlayerMapperEx extends PlayerMapper {
    Player selectByPrimaryKeyWithLock(String id);

    List<Player> selectByLimit(Integer limit);

    Integer count();
}
```

Define the mapping rules in `PlayerMapperEx.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<mapper namespace="com.pingcap.model.PlayerMapperEx">
  <resultMap id="BaseResultMap" type="com.pingcap.model.Player">
    <constructor>
      <idArg column="id" javaType="java.lang.String" jdbcType="VARCHAR" />
      <arg column="coins" javaType="java.lang.Integer" jdbcType="INTEGER" />
      <arg column="goods" javaType="java.lang.Integer" jdbcType="INTEGER" />
    </constructor>
  </resultMap>
  <sql id="Base_Column_List">
    id, coins, goods
  </sql>

  <select id="selectByPrimaryKeyWithLock" parameterType="java.lang.String" resultMap="BaseResultMap">
    select 
    <include refid="Base_Column_List" />
    from player
    where `id` = #{id,jdbcType=VARCHAR}
    for update
  </select>

  <select id="selectByLimit" parameterType="java.lang.Integer" resultMap="BaseResultMap">
    select
    <include refid="Base_Column_List" />
    from player
    limit #{id,jdbcType=INTEGER}
  </select>

  <select id="count" resultType="java.lang.Integer">
    select count(*) from player
  </select>

</mapper>
```

`PlayerDAO.java` is a class used to manage data, in which `DAO` means [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object). The class defines a set of data manipulation methods for writing data. In it, MyBatis encapsulates a large number of operations such as object mapping and CRUD of basic objects, which greatly simplifies the code.

```java
package com.pingcap.dao;

import com.pingcap.model.Player;
import com.pingcap.model.PlayerMapperEx;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;

import java.util.List;
import java.util.function.Function;

public class PlayerDAO {
    public static class NotEnoughException extends RuntimeException {
        public NotEnoughException(String message) {
            super(message);
        }
    }

    // Run SQL code in a way that automatically handles the
    // transaction retry logic, so we don't have to duplicate it in
    // various places.
    public Object runTransaction(SqlSessionFactory sessionFactory, Function<PlayerMapperEx, Object> fn) {
        Object resultObject = null;
        SqlSession session = null;

        try {
            // open a session with autoCommit is false
            session = sessionFactory.openSession(false);

            // get player mapper
            PlayerMapperEx playerMapperEx = session.getMapper(PlayerMapperEx.class);

            resultObject = fn.apply(playerMapperEx);
            session.commit();
            System.out.println("APP: COMMIT;");
        } catch (Exception e) {
            if (e instanceof NotEnoughException) {
                System.out.printf("APP: ROLLBACK BY LOGIC; \n%s\n", e.getMessage());
            } else {
                System.out.printf("APP: ROLLBACK BY ERROR; \n%s\n", e.getMessage());
            }

            if (session != null) {
                session.rollback();
            }
        } finally {
            if (session != null) {
                session.close();
            }
        }

        return resultObject;
    }

    public Function<PlayerMapperEx, Object> createPlayers(List<Player> players) {
        return playerMapperEx -> {
            Integer addedPlayerAmount = 0;
            for (Player player: players) {
                playerMapperEx.insert(player);
                addedPlayerAmount ++;
            }
            System.out.printf("APP: createPlayers() --> %d\n", addedPlayerAmount);
            return addedPlayerAmount;
        };
    }

    public Function<PlayerMapperEx, Object> buyGoods(String sellId, String buyId, Integer amount, Integer price) {
        return playerMapperEx -> {
            Player sellPlayer = playerMapperEx.selectByPrimaryKeyWithLock(sellId);
            Player buyPlayer = playerMapperEx.selectByPrimaryKeyWithLock(buyId);

            if (buyPlayer == null || sellPlayer == null) {
                throw new NotEnoughException("sell or buy player not exist");
            }

            if (buyPlayer.getCoins() < price || sellPlayer.getGoods() < amount) {
                throw new NotEnoughException("coins or goods not enough, rollback");
            }

            int affectRows = 0;
            buyPlayer.setGoods(buyPlayer.getGoods() + amount);
            buyPlayer.setCoins(buyPlayer.getCoins() - price);
            affectRows += playerMapperEx.updateByPrimaryKey(buyPlayer);

            sellPlayer.setGoods(sellPlayer.getGoods() - amount);
            sellPlayer.setCoins(sellPlayer.getCoins() + price);
            affectRows += playerMapperEx.updateByPrimaryKey(sellPlayer);

            System.out.printf("APP: buyGoods --> sell: %s, buy: %s, amount: %d, price: %d\n", sellId, buyId, amount, price);
            return affectRows;
        };
    }

    public Function<PlayerMapperEx, Object> getPlayerByID(String id) {
        return playerMapperEx -> playerMapperEx.selectByPrimaryKey(id);
    }

    public Function<PlayerMapperEx, Object> printPlayers(Integer limit) {
        return playerMapperEx -> {
            List<Player> players = playerMapperEx.selectByLimit(limit);

            for (Player player: players) {
                System.out.println("\n[printPlayers]:\n" + player);
            }
            return 0;
        };
    }

    public Function<PlayerMapperEx, Object> countPlayers() {
        return PlayerMapperEx::count;
    }
}
```

`MybatisExample` is the main class of the `plain-java-mybatis` sample application. It defines the entry functions:

```java
package com.pingcap;

import com.pingcap.dao.PlayerDAO;
import com.pingcap.model.Player;
import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;

public class MybatisExample {
    public static void main( String[] args ) throws IOException {
        // 1. Create a SqlSessionFactory based on our mybatis-config.xml configuration
        // file, which defines how to connect to the database.
        InputStream inputStream = Resources.getResourceAsStream("mybatis-config.xml");
        SqlSessionFactory sessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

        // 2. And then, create DAO to manager your data
        PlayerDAO playerDAO = new PlayerDAO();

        // 3. Run some simple examples.

        // Create a player who has 1 coin and 1 goods.
        playerDAO.runTransaction(sessionFactory, playerDAO.createPlayers(
                Collections.singletonList(new Player("test", 1, 1))));

        // Get a player.
        Player testPlayer = (Player)playerDAO.runTransaction(sessionFactory, playerDAO.getPlayerByID("test"));
        System.out.printf("PlayerDAO.getPlayer:\n    => id: %s\n    => coins: %s\n    => goods: %s\n",
                testPlayer.getId(), testPlayer.getCoins(), testPlayer.getGoods());

        // Count players amount.
        Integer count = (Integer)playerDAO.runTransaction(sessionFactory, playerDAO.countPlayers());
        System.out.printf("PlayerDAO.countPlayers:\n    => %d total players\n", count);

        // Print 3 players.
        playerDAO.runTransaction(sessionFactory, playerDAO.printPlayers(3));

        // 4. Getting further.

        // Player 1: id is "1", has only 100 coins.
        // Player 2: id is "2", has 114514 coins, and 20 goods.
        Player player1 = new Player("1", 100, 0);
        Player player2 = new Player("2", 114514, 20);

        // Create two players "by hand", using the INSERT statement on the backend.
        int addedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.createPlayers(Arrays.asList(player1, player2)));
        System.out.printf("PlayerDAO.createPlayers:\n    => %d total inserted players\n", addedCount);

        // Player 1 wants to buy 10 goods from player 2.
        // It will cost 500 coins, but player 1 cannot afford it.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will fail");
        Integer updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 10, 500));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);

        // So player 1 has to reduce the incoming quantity to two.
        System.out.println("\nPlayerDAO.buyGoods:\n    => this trade will success");
        updatedCount = (Integer)playerDAO.runTransaction(sessionFactory,
                playerDAO.buyGoods(player2.getId(), player1.getId(), 2, 100));
        System.out.printf("PlayerDAO.buyGoods:\n    => %d total update players\n", updatedCount);
    }
}
```

## Step 3. Run the code

The following content introduces how to run the code step by step.

### Step 3.1 Table initialization

When using MyBatis, you need to initialize the database tables manually. If you are using a local cluster, and MySQL client has been installed locally, you can run it directly in the `plain-java-mybatis` directory:

```shell
make prepare
```

Or you can execute the following command:

```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
```

If you are using a non-local cluster or MySQL client has not been installed, connect to your cluster and run the statement in the `src/main/resources/dbinit.sql` file.

### Step 3.2 Modify parameters for TiDB Cloud

If you are using a TiDB Serverless cluster, modify the `dataSource.url`, `dataSource.username`, `dataSource.password` in `mybatis-config.xml`.

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

<configuration>
    <settings>
        <setting name="cacheEnabled" value="true"/>
        <setting name="lazyLoadingEnabled" value="false"/>
        <setting name="aggressiveLazyLoading" value="true"/>
        <setting name="logImpl" value="LOG4J"/>
    </settings>

    <typeAliases>
        <package name="com.pingcap.dao"/>
    </typeAliases>

    <environments default="development">
        <environment id="development">
            <!-- JDBC transaction manager -->
            <transactionManager type="JDBC"/>
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:4000/test"/>
                <property name="username" value="root"/>
                <property name="password" value=""/>
            </dataSource>
        </environment>
    </environments>

    <mappers>
        <mapper resource="mapper/PlayerMapper.xml"/>
        <mapper resource="mapper/PlayerMapperEx.xml"/>
    </mappers>

</configuration>
```

Suppose that the password you set is `123456`, and the connection parameters you get from the cluster details page are the following:

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

In this case, you can modify the parameters in `dataSource` node as follows:

```xml
<?xml version="1.0" encoding="UTF-8" ?>

<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">

        ...
            <!-- Database pool -->
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://xxx.tidbcloud.com:4000/test?sslMode=VERIFY_IDENTITY&amp;enabledTLSProtocols=TLSv1.2,TLSv1.3"/>
                <property name="username" value="2aEp24QWEDLqRFs.root"/>
                <property name="password" value="123456"/>
            </dataSource>
        ...

</configuration>
```

### Step 3.3 Run

To run the code, you can run `make prepare`, `make gen`, `make build` and `make run` respectively:

```shell
make prepare
# this command executes :
# - `mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql`
# - `mysql --host 127.0.0.1 --port 4000 -u root -e "TRUNCATE test.player"`

make gen
# this command executes :
# - `rm -f src/main/java/com/pingcap/model/Player.java`
# - `rm -f src/main/java/com/pingcap/model/PlayerMapper.java`
# - `rm -f src/main/resources/mapper/PlayerMapper.xml`
# - `mvn mybatis-generator:generate`

make build # this command executes `mvn clean package`
make run # this command executes `java -jar target/plain-java-mybatis-0.0.1-jar-with-dependencies.jar`
```

Or you can use the native commands:

```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
mysql --host 127.0.0.1 --port 4000 -u root -e "TRUNCATE test.player"
rm -f src/main/java/com/pingcap/model/Player.java
rm -f src/main/java/com/pingcap/model/PlayerMapper.java
rm -f src/main/resources/mapper/PlayerMapper.xml
mvn mybatis-generator:generate
mvn clean package
java -jar target/plain-java-mybatis-0.0.1-jar-with-dependencies.jar
```

Or run the `make` command directly, which is a combination of `make prepare`, `make gen`, `make build` and `make run`.

## Step 4. Expected output

[MyBatis Expected Output](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-mybatis)