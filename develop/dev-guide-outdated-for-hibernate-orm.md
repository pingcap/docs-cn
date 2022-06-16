---
title: App Development for Hibernate ORM
summary: Learn how to develop a simple Java application using TiDB and the Hibernate ORM.
---

# App Development for Hibernate ORM

> **Note:**
>
> This document has been archived. This indicates that this document will not be updated thereafter. You can see [Developer Guide Overview](/develop/dev-guide-overview.md) for more details.

This tutorial shows you how to build a simple Java application based on TiDB and the Hibernate ORM, the best practices, and the known limitations. The sample application to build here is a simple CRM tool where you can add, query, and update customer and order information.

## Step 1. Start a TiDB cluster

Start a pseudo TiDB cluster on your local storage:

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

The above command starts a temporary and single-node cluster with mock TiKV. The cluster listens on the port `$LOCAL_PORT`. After the cluster is stopped, any changes already made to the database are not persisted.

> **Note:**
>
> To deploy a "real" TiDB cluster for production, see the following guides:
>
> + [Deploy TiDB using TiUP for On-Premises](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> + [Deploy TiDB on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> You can also [use TiDB Cloud](https://pingcap.com/products/tidbcloud/), a fully-managed Database-as-a-Service (DBaaS), which offers free trial.

## Step 2. Create a database

1. Connect to TiDB. Because TiDB is compatible with the MySQL protocol, you can connect to TiDB using any MySQL client:

    {{< copyable "" >}}

    ```bash
    mysql -u root -h 127.0.0.1 -P $LOCAL_PORT
    ```

2. In the SQL shell, create the `bank` database that your application will use:

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE bank;
    ```

3. Create a SQL user for your application:

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    Take note of the username and password. You will use them in your application code later.

4. Grant necessary permissions to the SQL user you have just created:

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON bank.* TO <username>;
    ```

## Step 3. Get and run the application code

The sample application code in this tutorial (`Example.java`) uses Hibernate to map Java methods to SQL operations. You can use the example application code on your local machine.

The code performs the following operations that roughly correspond to method calls in the `Example` class:

1. Creates the `Example$User` and `Example$Order` tables in the `hibernate_example` database as specified by the `User` and the `Order` mapping classes. For example, the `User` class corresponds to the creation of a table as follows:

    {{< copyable "" >}}

    ```sql
    CREATE TABLE `Example$User` (
    `userId` int(11) NOT NULL AUTO_INCREMENT,
    `gender` int(11) DEFAULT NULL,
    `name` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`userId`) /*T![clustered_index] CLUSTERED */
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=758190
    ```

2. Inserts demo rows into the table with the constructed `User` instances and `Order` instances.
3. Updates the `Example$Order` table by modifying the `Order` instance.
4. Removes one row from the `Example$Order` table.
5. Executes a query which joins the `Example$User` table and the `Example$Order` table and gets the name of the user whose total order price is greater than `500`.

The contents of `Example.java`:

{{< copyable "" >}}

```java
package com.pingcap;

package com.pingcap.hibernate;

import org.hibernate.Session;
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.query.Query;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import java.util.Iterator;
import java.util.List;

public class Example {

   public static enum Gender {
      MALE, FEMALE
   }

   /**
    * The User class.
    */
   @Entity
   public static class User {
      /** The ID. */
      @Id
      @GeneratedValue(strategy=GenerationType.IDENTITY)
      private int userId;

      private String name;

      private Gender gender;

      public User() {}

      public User(String name, Gender gender) {
         setName(name);
         setGender(gender);
      }

      public int getUserId() {
         return userId;
      }

      public String getName() {
         return name;
      }

      public void setName(String name) {
         this.name = name;
      }

      public Gender getGender() {
         return gender;
      }

      public void setGender(Gender gender) {
         this.gender = gender;
      }
   }

   @Entity
   public static class Order {
      /** The order ID. */
      @Id
      @GeneratedValue(strategy=GenerationType.IDENTITY)
      private int orderId;

      /** The user ID related to this order. */
      private int userId;

      /** The price. */
      private double price;

      public Order() {}

      public Order(int userId, double price) {
         setUserId(userId);
         setPrice(price);
      }

      public int getOrderId() {
         return orderId;
      }

      public int getUserId() {
         return userId;
      }

      public void setUserId(int userId) {
         this.userId = userId;
      }

      public double getPrice() {
         return price;
      }

      public void setPrice(double price) {
         this.price = price;
      }
   }


   /**
    * The main method.
    *
    * @param args the arguments
    */
   public static void main(String[] args) {
      Session session = openSession();
      try {
         User tom = new User("Tom", Gender.MALE);
         persist(session, tom);

         User jack = new User("Jack", Gender.MALE);
         persist(session, jack);

         Order order1 = new Order(tom.getUserId(), 100.0);
         Order order2 = new Order(tom.getUserId(), 200.0);
         Order order3 = new Order(jack.getUserId(), 300.0);

         persist(session, order1);
         persist(session, order2);
         persist(session, order3);

         order1.setPrice(500);
         persist(session, order1);

         session.delete(order3);

         Query query = session.createQuery("SELECT u.name FROM Example$User u JOIN Example$Order o ON u.userId = o.userId GROUP BY u.name HAVING SUM(o.price) > 500");
         List list = query.list();
         Iterator it = list.iterator();
         while (it.hasNext()) {
            System.out.println("User name:" + (String) it.next());
         }
      } finally {
         session.close();
      }
   }

   /**
    * Persists the object by wrapping an explicit transaction.
    *
    * @param obj the user
    * @throws Exception the exception
    */
   private static void persist(Session session, Object obj) {
      session.getTransaction().begin();
      session.persist(obj);
      session.getTransaction().commit();
   }

   /** The session factory. */
   private static SessionFactory sessionFactory = null;

   /**
    * Open session.
    *
    * @return the session
    */
   private static Session openSession() {
      if (sessionFactory == null) {
         final Configuration configuration = new Configuration();
         configuration.addAnnotatedClass(User.class);
         configuration.addAnnotatedClass(Order.class);

         sessionFactory = configuration.buildSessionFactory(new StandardServiceRegistryBuilder().build());
      }
      return sessionFactory.openSession();
   }
}
```

### Step 1. Get the application code

To get the `Example.java` code above, clone the `tidb-hibernate-example` repository to your machine:

{{< copyable "" >}}

```bash
git clone https://github.com/bb7133/tidb-hibernate-example
```

### Step 2. Update the connection parameters

Edit `src/main/resources/hibernate.properties` in a text editor:

1. Modify the `hibernate.connection.url` property with the port number from the `hibernate.properties` configuration file:

    {{< copyable "" >}}

    ```
    hibernate.connection.url jdbc:mysql://127.0.0.1:4000/hibernate_example
    hibernate.connection.username root
    hibernate.connection.password
    ```

    In the above example, `4000` is the port number on which the TiDB cluster is listening.

2. Set the `hibernate.connection.username` property to the username you have created in [Create a database](#step-2-create-a-database).

3. Set the `hibernate.connection.password` property to the user's password.

### Step 3. Run the application code

Compile and run the application code using `gradlew` that also downloads the dependencies.

{{< copyable "" >}}

```bash
./gradlew run
```

At the end of the output, you are expected see:

```
User name: Jack
```

To verify whether the results have been updated successfully in the database, execute the following statement in the MySQL client:

{{< copyable "" >}}

```sql
> SELECT * FROM ;
+----+-----------+
| id | balance   |
+----+-----------+
|  1 |    900.00 |
|  2 |    350.00 |
|  3 |  |
+----+-----------+
3 rows in set (0.03 sec)
```

## Best practices

This section introduces the best practices for building Java applications using TiDB and Hibernate.

### Quotes for identifiers

Most of the keywords in MySQLDialect are not registered as "reserved keywords". Therefore, if an entity is defined with a name in the MySQL reserved keywords, an error might be reported. For example, suppose that you have an entity named `Set`:

```
@Entity
public class Set {
    ...
}
```

Because `Set` is a reserved keywords in both TiDB and MySQL, an error similar to the following one is reported:

```
ERROR: You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 15 near "Set"
Exception in thread "main" javax.persistence.PersistenceException: org.hibernate.exception.SQLGrammarException: could not execute statement
```

To avoid the above error, it is recommended to set `GLOBALLY_QUOTED_IDENTIFIERS=true` in the configuration file of Hibernate ORM.

### Collations

By default, TiDB does not support case-insensitive or accent-insensitive collations. All collations TiDB are treated as aliases of the `_bin` collation, unless the [new collation framework](https://docs.pingcap.com/tidb/v5.1/character-set-and-collation#new-framework-for-collations) is enabled.

You can enable the new collation framework ONLY WHEN you initialize a cluster.

### JDBC

Most of the best practices that apply to JDBC can be applied to Hibernate. For more details, see [Best Practices for Developing Java Applications with TiDB](https://docs.pingcap.com/tidb/v5.1/java-app-best-practices).

## Known Limitation

### Limited support for foreign key

Foreign key constraints and cascades updates are not fully supported by TiDB yet. For details, see [Constraints in TiDB](https://docs.pingcap.com/tidb/v5.1/constraints#foreign-key).

Take the previous demo application as an example. Suppose that you define a one-to-many mapping for `Example$User` and `Example$Order`:

```
@Entity
public static class User {
   ...

   @OneToMany
   @JoinColumn(name = "userId")
   private Set<Order> orders;
}
```

This leads to a foreign key constraint for the definition of `Example$Order` table:

{{< copyable "" >}}

```sql
CREATE TABLE `Example$Order` (
  `orderId` int(11) NOT NULL AUTO_INCREMENT,
  `price` double NOT NULL,
  `userId` int(11) NOT NULL,
  PRIMARY KEY (`orderId`) /*T![clustered_index] CLUSTERED */,
  CONSTRAINT `FKq64l0s3am0rlue6gxsxljg056` FOREIGN KEY (`userId`) REFERENCES `Example$User` (`userId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1618271
```

The definition of `FOREIGN KEY` is supported by TiDB, but it does not take affect actually. Consider the following cases:

```sql
tidb> select * from Example$User;
+--------+--------+------+
| userId | gender | name |
+--------+--------+------+
|      1 |      0 | Tom  |
|      2 |      0 | Jack |
+--------+--------+------+
2 rows in set (0.00 sec)

tidb> select * from Example$Order;                                                                               +---------+-------+--------+
+---------+-------+--------+
| orderId | price | userId |
+---------+-------+--------+
|       1 |   500 |      1 |
|       2 |   200 |      1 |
|       3 |   300 |      2 |
+---------+-------+--------+
```

If you try to delete the `Jack` row from `Example$User` table, using either the Hibernate code (`delete(session, jack)`) or the SQL statement (`delete from Example$User where userId=2;`), you might expect the an error as follows:

```sql
ERROR 1452 (23000): Cannot add or update a child row: a foreign key constraint fails (`hibernate_example`.`Example$Order`, CONSTRAINT `FKrd372ndoovvnmduu9iwffri3a` FOREIGN KEY (`orderId`) REFERENCES `Example$User` (`userId`))
```

However, the expected error is NOT reported by TiDB, because the foreign key constraint is ignored.

To avoid this situation, you need to maintain the mapping by yourself.

The support of foreign key is on the roadmap of TiDB. You can track the GitHub issue [#18209](https://github.com/pingcap/tidb/issues/18209) for more progress.

## What's next?

Learn more about how to use the [Hibernate ORM](http://hibernate.org/orm/).

You might also be interested in [Best Practices for Developing Java Applications with TiDB](https://docs.pingcap.com/tidb/v5.1/java-app-best-practices).
