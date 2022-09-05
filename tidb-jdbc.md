---
title: TiDB-JDBC
summary: 本文介绍 TiDB-JDBC 介绍及使用说明
---

# TiDB-JDBC

本文介绍 TiDB-JDBC 介绍及使用说明

## repo 地址

https://github.com/pingcap/mysql-connector-j

## TiDB-JDBC 介绍

1. 基于官方 8.0.29 版本编译。
2. 修复 prepare 模式下多参数、多字段 EOF bug。
     一次数据库驱动升级引发的血案20220124 
     关于北京银行的问题分析
3. 新增 TiCDC snapshot 自动维护。
4. 新增 SM3 认证插件

## 配置

### pom 配置

```
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
```

### sm3 pom 配置

```
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcprov-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
<dependency>
    <groupId>org.bouncycastle</groupId>
    <artifactId>bcpkix-jdk15on</artifactId>
    <version>1.67</version>
</dependency>
```

# tidb-loadbalance 

## repo 地址

https://github.com/pingcap/tidb-loadbalance

## tidb-loadbalance 介绍

tidb-loadbalance 是 fork  https://github.com/tidb-incubator/TiBigData/tree/master/jdbc 
后独立维护的 JDBC Wrapper 。 

在此的基础上修复了
1. 定时扫描 TiDB-Server 由之前的默认第一台改为随机选用一台 TiDB Server 查询。
2. 在与 dbcp2 连接池整合的时候密码错误不退出 bug。
3. 新增权重策略。

tidb-loadbalance 需要配合 mysql-connector-j 一起使用。

## 方案优势

1. tidb-loadbalance 会自动维护 TiDB Server 的节点信息，根据节点信息使用 tidb-loadbalance 策略分发 JDBC Connection 。
2. tidb-loadbalance 实现了轮询、随机、权重负载均衡策略。
3. tidb-loadbalance 在客户端分发 Connection 。 客户 APP 和 TiDB Server 是使用 JDBC 直连的方式。性能比使用负载均衡组件后的高。

## 配置

### pom 配置

```
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>mysql-connector-java</artifactId>
  <version>8.0.29-tidb-1.0.0</version>
</dependency>
<dependency>
  <groupId>io.github.lastincisor</groupId>
  <artifactId>tidb-loadbalance</artifactId>
  <version>0.0.5</version>
</dependency>
```

### 连接池配置

springboot Configuration 

| 连接池组件 |配置路径| 备注 |
| :-- | :-- | :-- |
|hikari| com.zaxxer.hikari.HikariDataSource | 默认连接池 |
|dbcp2 | org.apache.commons.dbcp2.BasicDataSource |  |
|c3p0 | com.mchange.v2.c3p0.ComboPooledDataSource | 配置属性有变化 |
|tomcat pool| org.apache.tomcat.jdbc.pool.DataSource | |
|druid | com.alibaba.druid.pool.DruidDataSource |  |


hikari Configuration
```
spring.datasource.type=com.zaxxer.hikari.HikariDataSource
spring.datasource.url=jdbc:tidb://[hosts][/database][?properties]
spring.datasource.driverClassName=com.tidb.jdbc.Driver
spring.datasource.username=user
spring.datasource.password=pwd
spring.datasource.hikari.....
```
dbcp2 Configuration
```
<dependency>
    <groupId>org.apache.commons</groupId>
    <artifactId>commons-dbcp2</artifactId>
    <version>{version}</version>
</dependency>
```
```
spring.datasource.type=org.apache.commons.dbcp2.BasicDataSource
spring.datasource.url=jdbc:tidb://[hosts][/database][?properties]
spring.datasource.driverClassName=com.tidb.jdbc.Driver
spring.datasource.username=user
spring.datasource.password=pwd
spring.datasource.dbcp2.....
```
c3p0 Configuration
```
<dependency>
    <groupId>com.mchange</groupId>
    <artifactId>c3p0</artifactId>
    <version>{version}</version>
</dependency>
```
```
spring.datasource.type=com.mchange.v2.c3p0.ComboPooledDataSource
spring.datasource.jdbcUrl=jdbc:tidb://[hosts][/database][?properties]
spring.datasource.driverClass=com.tidb.jdbc.Driver
spring.datasource.user=user
spring.datasource.password=pwd
```
tomcat pool Configuration
```
<dependency>
    <groupId>org.apache.tomcat</groupId>
    <artifactId>tomcat-jdbc</artifactId>
    <version>{version}</version>
</dependency>
```
```
spring.datasource.type=org.apache.tomcat.jdbc.pool.DataSource
spring.datasource.url=jdbc:tidb://[hosts][/database][?properties]
spring.datasource.driverClassName=com.tidb.jdbc.Driver
spring.datasource.username=user
spring.datasource.password=pwd
spring.datasource.tomcat .....
```
druid Configuration
```
<dependency>
    <groupId>com.alibaba</groupId>
    <artifactId>druid-spring-boot-starter</artifactId>
    <version>{version}</version>
</dependency>
```
```
spring.datasource.type=com.alibaba.druid.pool.DruidDataSource
spring.datasource.url=jdbc:tidb://[hosts][/database][?properties]
spring.datasource.driverClassName=com.tidb.jdbc.Driver
spring.datasource.username=user
spring.datasource.password=pwd
spring.datasource.druid .....
```

### URL配置参数说明

#### tidb.jdbc.url-mapper =  [roundrobin |  weight |  random]

1. 轮询策略 tidb.jdbc.url-mapper = roundrobin
  只需要配置 一个 TiDB Server 即可
  ```
  jdbc:tidb://{ip}:{port}/db?tidb.jdbc.url-mapper=roundrobin
  ```
  该策略为默认策略，可以不用配置 tidb.jdbc.url-mapper=roundrobin 

2. 权重策略 tidb.jdbc.url-mapper = weight 
  权重策略，在此模式下  JDBC URL 需要指定 {ip} {port} {weight}
  详细配置 如下
  ```
  jdbc:tidb://{ip1}:{port1}:{weight1},{ip2}:{port2}:{weight2},{ip3}:{port3}:{weight3}/db?tidb.jdbc.url-mapper=weight
  ```

3. 随机策略 tidb.jdbc.url-mapper = random 
  只需要配置 一个 TiDB Server 即可
  ```
  jdbc:tidb://{ip}:{port}/db?tidb.jdbc.url-mapper=random
  ```

#### tidb.jdbc.min-discovery-interval

最小扫描间隔，默认 1000 毫秒。并发连接请求只会触发一次，发现相同则重用。

#### tidb.jdbc.max-discovery-interval

最大扫描间隔，当没有连接时触发扫描，driver 每 tidb.jdbc.max-discovery-interval 毫秒触发一次扫描。默认 1 分钟














