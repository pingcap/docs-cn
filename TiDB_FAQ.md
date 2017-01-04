# TiDB FAQ

## What is TiDB?

TiDB is a distributed SQL database that features in horizontal scalability, high availability and consistent distributed transactions. It also enables you to use MySQL’s SQL syntax and protocol to manage and retrieve data.

## How do TiDB and TiKV work together? What is the relationship between the two?

TiDB works as the SQL layer and TiKV works as the Key-Value layer. TiDB is mainly responsible for parsing SQL, specifying query plan, and generating executor while TiKV is to store the actual data and works as the storage engine.

TiDB provides TiKV the SQL enablement and turns TiKV into a NewSQL database. TiDB and TiKV work together to be as scalable as a NoSQL database while maintains the ACID transactions of a relational database.

## Why do you have separate layers?

Inspired by Google F1 and Spanner, TiDB and TiKV adopt a highly-layered architecture. This architecture supports pluggable storage drivers and engines, which powers you to customize your database solutions based on your own business requirements. Meanwhile, this architecture makes it easy to debug, update, tune, and maintain. You won’t have to go through the entire system just to find and fix a bug in one module.

## What does Placement Driver (PD) do?

Placement Driver (PD) works as the cluster manager of TiDB. It manages the TiKV metadata and makes decisions for data placement and load balancing. PD periodically checks replication constraints to balance load and data automatically.

## Is it easy to use TiDB?

Yes, it is. When all the required services are started, you can use TiDB as easily as a MySQL server.  You can replace MySQL with TiDB to power your applications without changing a single line of code in most cases. You can also manage TiDB using the popular MySQL management tools.

## When to use TiDB?

TiDB is at your service if your applications require any of the following:
+ Horizontal scalability
+ High availability
+ Strong consistency
+ Support for distributed ACID transactions

## When not to use TiDB?

TiDB is not a good choice if the number of the rows in your database table is less than 100GB and there is no requirement for high availability, strong consistency and cross-datacenter replication.

## How does TiDB manage user account?

TiDB follows MySQL user authentication mechanism. You can create user accounts and authorize them. 

+ You can use MySQL grammar to create user accounts. For example, you can create a user account by using the following statement:
  ```
  CREATE USER 'test'@'localhost' identified by '123';
  ```
  The user name of this account is "test"; the password is “123" and this user can login from localhost only.

  You can use the `Set Password` statement to set and change the password. For example, to set the password for the default "root" account, you can use the following statement:

  ```
  SET PASSWORD FOR 'root'@'%' = '123';
  ```

+ You can also use MySQL grammar to authorize this user. For example, you can grant the read privilege to the "test" user by using the following statement:

  ```
  GRANT SELECT ON \*.\* TO  'test'@'localhost';
  ```

Note: There are following differences between TiDB and MySQL in user account creating and authorizing:

+ You can use the "user@hostname" grammar to create accounts. In this grammar, “hostname” supports exact match like “192.168.199.1” and full match like “%”, but doesn’t support prefix match like “192.168.%”.

+ To be compatible with the existing MySQL businesses, TiDB supports user authorization but it only supports the authorization grammar and recording the authorization in the system table. TiDB checks the authorization for the DropTable statement only. It does not check the authorization for other statements.

## How does TiDB scale?

As your business grows, your database might face the following three bottlenecks:

+ Lack of storage resources which means that the disk space is not enough.

+ Lack of computing resources such as high CPU occupancy.

+ Not enough throughputs.

You can scale TiDB as your business grows.

+ If the disk space is not enough, you can increase the capacity simply by adding more TiKV nodes. When the new node is started, PD will migrate the data from other nodes to the new node automatically.

+ You can add more TiDB nodes or TiKV nodes if the computing resources are not enough. After a TiDB node is added, you can simply configure it in the Load Balancer.

+ If the throughputs are not enough, you can add both TiDB nodes and TiKV nodes.

## How is TiDB highly available?

TiDB is self-healing. All of the three components, TiDB, TiKV and PD, can tolerate failures of some of their instances. With its strong consistency guarantee, whether it’s data machine failures or even downtime of an entire data center, your data can be recovered automatically.

## How is TiDB strongly-consistent?

Strong consistency means all replicas return the same value when queried for the attribute of an object. TiDB uses the [Raft consensus algorithm](https://raft.github.io/) to ensure consistency among multiple replicas. TiDB allows a collection of machines to work as a coherent group that can survive the failures of some of its members.

## Does TiDB support distributed transactions?

Yes. The transaction model in TiDB is inspired by Google’s Percolator, a paper published in 2006. It’s mainly a two-phase commit protocol with some practical optimizations. This model relies on a timestamp allocator to assign monotone increasing timestamp for each transaction, so the conflicts can be detected.  PD works as the timestamp allocator in a TiDB cluster.

## Does TiDB have ACID semantics?

Yes. ACID semantics are guaranteed in TiDB:

+ Atomicity: Each transaction in TiDB is "all or nothing": if one part of the transaction fails, then the entire transaction fails, and the database state is left unchanged. TiDB guarantees atomicity in each and every situation, including power failures, errors, and crashes. 

+ Consistency: TiDB ensures that any transaction brings the database from one valid state to another. Any data written to the TiDB database must be valid according to all defined rules, including constraints, cascades, triggers, and any combination thereof. 

+ Isolation: TiDB provides snapshot isolation (SI), snapshot isolation with lock (SQL statement: SELECT ... FOR UPDATE), and externally consistent reads and writes in distributed transactions.   

+ Durability: TiDB allows a collection of machines to work as a coherent group that can survive the failures of some of its members. So in TiDB, once a transaction has been committed, it will remain so, even in the event of power loss, crashes, or errors. 

## How to choose the lease parameter in TiDB?

The lease parameter is set from the command line when starting a TiDB server. The value of the lease parameter impacts the Database Schema Changes (DDL) speed of the current session. In the testing environments, you can set the value to 1s for to speed up the testing cycle. But in the production environments, it is recommended to set the value to minutes (for example, 300s) to ensure the DDL safety.

## Why is the DDL statement so slow when using TiDB?

TiDB implements the online change algorithm of [Google F1](http://research.google.com/pubs/pub41376.html). Generally, DDL is not a frequent operation. In case of DDL, the top priority of TiDB is to ensure the data consistency and business continuity. A complete DDL has 2 to 5 phases depending on the statement type. Each phase takes the time of 2 leases. Assuming one lease is 1 minute, for a Drop Table statement which requires 2 phases, it takes 4 minutes (2 x 2 x 1 = 4). As what we have learned from Google F1, the DDL operation is handled by the database administrator (DBA) using special tools and it usually takes days.

## What programming language can I use to work with TiDB?

Any language that has MySQL client or driver.

## How does TiDB support SQL?

TiDB is compatible with MySQL protocol. TiDB sever speaks MySQL protocol and follows MySQL’s SQL grammar. The MySQL protocol layer and the TiDB SQL layer within the TiDB server work together to translate MySQL requests to TiDB SQL plan.

TiDB maps relational databases to Key-Value databases. It maps the relational table to Key-Value pairs and it also translate SQL statements to Key-Value operations. 

## Can I use SQL statements to work with TiDB?

Yes. TiDB follows MySQL’s SQL grammar. You can use TiDB just as using MySQL.

## Is TiDB based on MySQL?

No. TiDB supports MySQL syntax and protocol, but it is a new open source database that is developed and maintained by PingCAP, Inc.

## How does TiDB compare to traditional relational databases like Oracle and MySQL?

TiDB scores in horizontal scalability while still maintains the traditional relation database features. You can easily increase the capacity or balance the load by adding more machines.

## How does TiDB compare to NoSQL databases like Cassandra, Hbase, or MongoDB?

TiDB is as scalable as NoSQL databases but features in the usability and functionality of traditional SQL databases, such as SQL syntax and consistent distributed transactions.

## Can a MySQL application be migrated to TiDB?

Yes. Your applications can be migrated to TiDB without changing a single line of code in most cases.

## Can I use other key-value storage engines with TiDB?

Yes. TiDB supports many popular storage engines, such as goleveldb and TiKV.

## Why the modified `toml` configuration for TiKV/PD does not take effect?
You need to set the `--config` parameter in TiKV/PD to make the `toml` configuration effective. TiKV/PD does not read the configuration by default.

## Why the TiKV data directory is gone?

For TiKV, the default value of the `--store` parameter is `/tmp/tikv/store`. In some virtual machines, restarting the operating system results in removing all the data under the `/tmp` directory. It is recommended to set the TiKV data directory explicitly by setting the `--store` parameter.

## The `cluster ID mismatch` message is displayed when starting TiKV.

This is because the cluster ID stored in local TiKV is different from the cluster ID specified by PD. When a new PD cluster is deployed, PD generates random cluster IDs. TiKV gets the cluster ID from PD and stores the cluster ID locally when it is initialized. The next time when TiKV is started, it checks the local cluster ID with the cluster ID in PD. If the cluster IDs don't match, the `cluster ID mismatch` message is displayed and TiKV exits.

If you previously deploy a PD cluster, but then you remove the PD data and deploy a new PD cluster, this error occurs because TiKV uses the old data to connect to the new PD cluster.

## The `TiKV cluster is not bootstrapped` message is displayed when accessing PD.
Most of the APIs of PD are available only when the TiKV cluster is initialized. This message is displayed if PD is accessed when PD is started while TiKV is not started when a new cluster is deployed.
If this message is displayed, start the TiKV cluster. When TiKV is initialized, PD is accessible.
