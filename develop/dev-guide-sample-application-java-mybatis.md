---
title: TiDB 和 MyBatis 的简单 CRUD 应用程序
summary: 给出一个 TiDB 和 MyBatis 的简单 CRUD 应用程序示例。
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# TiDB 和 MyBatis 的简单 CRUD 应用程序

[Mybatis](https://mybatis.org/mybatis-3/index.html) 是当前比较流行的开源 Java 应用持久层框架。

本文档将展示如何使用 TiDB 和 MyBatis 来构造一个简单的 CRUD 应用程序。

> **注意：**
>
> 推荐使用 Java 8 及以上版本进行 TiDB 的应用程序的编写。

## 拓展学习视频

- [使用 Connector/J - TiDB v6](https://learn.pingcap.com/learner/course/840002/?utm_source=docs-cn-dev-guide)
- [在 TiDB 上开发应用的最佳实践 - TiDB v6](https://learn.pingcap.com/learner/course/780002/?utm_source=docs-cn-dev-guide)

## 第 1 步：启动你的 TiDB 集群

本节将介绍 TiDB 集群的启动方法。

**使用 TiDB Serverless 集群**

详细步骤，请参考：[创建 TiDB Serverless 集群](/develop/dev-guide-build-cluster-in-cloud.md#第-1-步创建-tidb-serverless-集群)。

**使用本地集群**

详细步骤，请参考：[部署本地测试 TiDB 集群](/quick-start-with-tidb.md#部署本地测试集群)或[部署正式 TiDB 集群](/production-deployment-using-tiup.md)。

## 第 2 步：获取代码

```shell
git clone https://github.com/pingcap-inc/tidb-example-java.git
```

与 [MyBatis](https://mybatis.org/mybatis-3/index.html) 对比，JDBC 的实现方式并非最优体验。你需要自行编写错误处理逻辑，并且代码无法简单复用。这会使你的代码有些冗余。

本文将以 Maven 插件的方式使用 [MyBatis Generator](https://mybatis.org/generator/quickstart.html) 生成部分持久层代码。

进入目录 `plain-java-mybatis`：

```shell
cd plain-java-mybatis
```

目录结构如下所示：

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

其中，自动生成的文件有：

- `src/main/java/com/pingcap/model/Player.java`：Player 实体类文件
- `src/main/java/com/pingcap/model/PlayerMapper.java`：Player Mapper 的接口文件
- `src/main/resources/mapper/PlayerMapper.xml`：Player Mapper 的 XML 映射，它是 MyBatis 用于生成 Player Mapper 接口的实现类的配置

这些文件的生成策略被写在了 `mybatis-generator.xml` 配置文件内，它是 [MyBatis Generator](https://mybatis.org/generator/quickstart.html) 的配置文件，下面配置文件中添加了使用方法的说明：

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
                This attribute indicated Mybatis how to implement interface.
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

`mybatis-generator.xml` 在 `pom.xml` 中，以 `mybatis-generator-maven-plugin` 插件配置的方式被引入：

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

在 Maven 插件内引入后，可删除旧的生成文件后，通过命令 `mvn mybatis-generate` 生成新的文件。或者你也可以使用已经编写好的 `make` 命令，通过 `make gen` 来同时删除旧文件，并生成新文件。

> **注意：**
>
> `mybatis-generator.xml` 中的属性 `configuration.overwrite` 仅可控制新生成的 Java 代码文件使用覆盖方式被写入，但 XML 映射文件仍会以追加方式写入。因此，推荐在 MyBatis Generator 生成新的文件前，先删除掉旧的文件。

`Player.java` 是使用 MyBatis Generator 生成出的数据实体类文件，为数据库表在程序内的映射。`Player` 类的每个属性都对应着 `player` 表的一个字段。

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

`PlayerMapper.java` 是使用 MyBatis Generator 生成出的映射接口文件，它仅规定了接口，接口的实现类是由 MyBatis 来通过 XML 或注解自动生成的：

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

`PlayerMapper.xml` 是使用 MyBatis Generator 生成出的映射 XML 文件，MyBatis 将使用这个文件自动生成 `PlayerMapper` 接口的实现类：

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

由于 MyBatis Generator 需要逆向生成源码，因此，数据库中需先行有此表结构，可使用 `dbinit.sql` 生成表结构：

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

额外拆分接口 `PlayerMapperEx` 继承 `PlayerMapper`，并且编写与之匹配的 `PlayerMapperEx.xml`。避免直接更改 `PlayerMapper.java` 和 `PlayerMapper.xml`。这是为了规避 MyBatis Generator 的反复生成，影响到自行编写的代码。

在 `PlayerMapperEx.java` 中定义自行增加的接口：

```java
package com.pingcap.model;

import java.util.List;

public interface PlayerMapperEx extends PlayerMapper {
    Player selectByPrimaryKeyWithLock(String id);

    List<Player> selectByLimit(Integer limit);

    Integer count();
}
```

在 `PlayerMapperEx.xml` 中定义映射规则：

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

`PlayerDAO.java` 是程序用来管理数据对象的类。其中 `DAO` 是 [Data Access Object](https://en.wikipedia.org/wiki/Data_access_object) 的缩写。在其中定义了一系列数据的操作方法，用于数据的写入。

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

`MybatisExample` 是 `plain-java-mybatis` 这个示例程序的主类。其中定义了入口函数：

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

## 第 3 步：运行代码

本节将逐步介绍代码的运行方法。

### 第 3 步第 1 部分：表初始化

使用 MyBatis 时，需手动初始化数据库表。若你本地已经安装了 `mysql-client`，且使用本地集群，可直接在 `plain-java-mybatis` 目录下通过 `make prepare` 运行：

```shell
make prepare
```

或直接执行：

```shell
mysql --host 127.0.0.1 --port 4000 -u root < src/main/resources/dbinit.sql
```

若你不使用本地集群，或未安装 `mysql-client`，请直接登录你的集群，并运行 `src/main/resources/dbinit.sql` 文件内的 SQL 语句。

### 第 3 步第 2 部分：TiDB Cloud 更改参数

若你使用 TiDB Serverless 集群，更改 `mybatis-config.xml` 内关于 `dataSource.url`、`dataSource.username`、`dataSource.password` 的参数：

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

若你设定的密码为 `123456`，而且从 TiDB Serverless 集群面板中得到的连接信息为：

- Endpoint: `xxx.tidbcloud.com`
- Port: `4000`
- User: `2aEp24QWEDLqRFs.root`

那么此处应将配置文件中 `dataSource` 节点内更改为：

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

### 第 3 步第 3 部分：运行

你可以分别运行 `make prepare`, `make gen`, `make build` 和 `make run` 以运行此代码：

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

或者你也可以直接使用原生的命令：

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

再或者直接运行 `make` 命令，这是 `make prepare`, `make gen`, `make build` 和 `make run` 的组合。

## 第 4 步：预期输出

[MyBatis 预期输出](https://github.com/pingcap-inc/tidb-example-java/blob/main/Expected-Output.md#plain-java-mybatis)
