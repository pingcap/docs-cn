---
title: Connectors and APIs
summary: Learn about the connectors and APIs.
category: reference
---

# Connectors and APIs

Database Connectors provide connectivity to the TiDB server for client programs. APIs provide low-level access to the MySQL protocol and MySQL resources. Both Connectors and the APIs enable you to connect and execute MySQL statements from another language or environment, including ODBC, Java (JDBC), Perl, Python, PHP, Ruby and C.

TiDB is compatible with all Connectors and APIs of MySQL (5.6, 5.7), including:

- [MySQL Connector/C](https://dev.mysql.com/doc/refman/5.7/en/connector-c-info.html)
- [MySQL Connector/C++](https://dev.mysql.com/doc/refman/5.7/en/connector-cpp-info.html)
- [MySQL Connector/J](https://dev.mysql.com/doc/refman/5.7/en/connector-j-info.html)
- [MySQL Connector/Net](https://dev.mysql.com/doc/refman/5.7/en/connector-net-info.html)
- [MySQL Connector/ODBC](https://dev.mysql.com/doc/refman/5.7/en/connector-odbc-info.html)
- [MySQL Connector/Python](https://dev.mysql.com/doc/refman/5.7/en/connector-python-info.html)
- [MySQL C API](https://dev.mysql.com/doc/refman/5.7/en/c-api.html)
- [MySQL PHP API](https://dev.mysql.com/doc/refman/5.7/en/apis-php-info.html)
- [MySQL Perl API](https://dev.mysql.com/doc/refman/5.7/en/apis-perl.html)
- [MySQL Python API](https://dev.mysql.com/doc/refman/5.7/en/apis-python.html)
- [MySQL Ruby APIs](https://dev.mysql.com/doc/refman/5.7/en/apis-ruby.html)
- [MySQL Tcl API](https://dev.mysql.com/doc/refman/5.7/en/apis-tcl.html)
- [MySQL Eiffel Wrapper](https://dev.mysql.com/doc/refman/5.7/en/apis-eiffel.html)
- [Mysql Go API](https://github.com/go-sql-driver/mysql)

## Connect to TiDB using MySQL Connectors

Oracle develops the following APIs and TiDB is compatible with all of them:

- [MySQL Connector/C](https://dev.mysql.com/doc/refman/5.7/en/connector-c-info.html): a standalone replacement for the `libmysqlclient`, to be used for C applications
- [MySQL Connector/C++](https://dev.mysql.com/doc/refman/5.7/en/connector-cpp-info.html)：to enable C++ applications to connect to MySQL
- [MySQL Connector/J](https://dev.mysql.com/doc/refman/5.7/en/connector-j-info.html)：to enable Java applications to connect to MySQL using the standard JDBC API
- [MySQL Connector/Net](https://dev.mysql.com/doc/refman/5.7/en/connector-net-info.html)：to enable .Net applications to connect to MySQL; [MySQL for Visual Studio](https://dev.mysql.com/doc/visual-studio/en/) uses this; support Microsoft Visual Studio 2012, 2013, 2015 and 2017 versions
- [MySQL Connector/ODBC](https://dev.mysql.com/doc/refman/5.7/en/connector-odbc-info.html)：the standard ODBC API; support Windows, Unix, and OS X platforms
- [MySQL Connector/Python](https://dev.mysql.com/doc/refman/5.7/en/connector-python-info.html)：to enable Python applications to connect to MySQL, compliant with the [Python DB API version 2.0](http://www.python.org/dev/peps/pep-0249/)

## Connect to TiDB using MySQL C API

If you use C language programs to connect to TiDB, you can connect to `libmysqlclient` directly and use the MySQL [C API](https://dev.mysql.com/doc/refman/5.7/en/c-api.html). This is one of the major connection methods using C language, widely used by various clients and APIs, including Connector/C.

## Connect to TiDB using third-party MySQL APIs

The third-party APIs are not developed by Oracle. The following table lists the commonly used third-party APIs:

| Environment    | API                                      | Type                             | Notes                                    |
| -------------- | ---------------------------------------- | -------------------------------- | ---------------------------------------- |
| Ada            | GNU Ada MySQL Bindings                   | `libmysqlclient`                 | See [MySQL Bindings for GNU Ada](http://gnade.sourceforge.net/) |
| C              | C API                                    | `libmysqlclient`                 | See [Section 27.8, “MySQL C API”](https://dev.mysql.com/doc/refman/5.7/en/c-api.html) |
| C              | Connector/C                              | Replacement for `libmysqlclient` | See [MySQL Connector/C Developer Guide](https://dev.mysql.com/doc/connector-c/en/) |
| C++            | Connector/C++                            | `libmysqlclient`                 | See [MySQL Connector/C++ Developer Guide](https://dev.mysql.com/doc/connector-cpp/en/) |
|                | MySQL++                                  | `libmysqlclient`                 | See [MySQL++ Web site](http://tangentsoft.net/mysql++/doc/) |
|                | MySQL wrapped                            | `libmysqlclient`                 | See [MySQL wrapped](http://www.alhem.net/project/mysql/) |
| Go             | go-sql-driver                            | Native Driver                    | See [Mysql Go API](https://github.com/go-sql-driver/mysql) |
| Cocoa          | MySQL-Cocoa                              | `libmysqlclient`                 | Compatible with the Objective-C Cocoa environment. See <http://mysql-cocoa.sourceforge.net/> |
| D              | MySQL for D                              | `libmysqlclient`                 | See [MySQL for D](http://www.steinmole.de/d/) |
| Eiffel         | Eiffel MySQL                             | `libmysqlclient`                 | See [Section 27.14, “MySQL Eiffel Wrapper”](https://dev.mysql.com/doc/refman/5.7/en/apis-eiffel.html) |
| Erlang         | `erlang-mysql-driver`                    | `libmysqlclient`                 | See [`erlang-mysql-driver`](http://code.google.com/p/erlang-mysql-driver/) |
| Haskell        | Haskell MySQL Bindings                   | Native Driver                    | See [Brian O'Sullivan's pure Haskell MySQL bindings](http://www.serpentine.com/blog/software/mysql/) |
|                | `hsql-mysql`                             | `libmysqlclient`                 | See [MySQL driver for Haskell](http://hackage.haskell.org/cgi-bin/hackage-scripts/package/hsql-mysql-1.7) |
| Java/JDBC      | Connector/J                              | Native Driver                    | See [MySQL Connector/J 5.1 Developer Guide](https://dev.mysql.com/doc/connector-j/5.1/en/) |
| Kaya           | MyDB                                     | `libmysqlclient`                 | See [MyDB](http://kayalang.org/library/latest/MyDB) |
| Lua            | LuaSQL                                   | `libmysqlclient`                 | See [LuaSQL](http://keplerproject.github.io/luasql/manual.html) |
| .NET/Mono      | Connector/Net                            | Native Driver                    | See [MySQL Connector/Net Developer Guide](https://dev.mysql.com/doc/connector-net/en/) |
| Objective Caml | OBjective Caml MySQL Bindings            | `libmysqlclient`                 | See [MySQL Bindings for Objective Caml](http://raevnos.pennmush.org/code/ocaml-mysql/) |
| Octave         | Database bindings for GNU Octave         | `libmysqlclient`                 | See [Database bindings for GNU Octave](http://octave.sourceforge.net/database/index.html) |
| ODBC           | Connector/ODBC                           | `libmysqlclient`                 | See [MySQL Connector/ODBC Developer Guide](https://dev.mysql.com/doc/connector-odbc/en/) |
| Perl           | `DBI`/`DBD::mysql`                       | `libmysqlclient`                 | See [Section 27.10, “MySQL Perl API”](https://dev.mysql.com/doc/refman/5.7/en/apis-perl.html) |
|                | `Net::MySQL`                             | Native Driver                    | See [`Net::MySQL`](http://search.cpan.org/dist/Net-MySQL/MySQL.pm) at CPAN |
| PHP            | `mysql`, `ext/mysql`interface (deprecated) | `libmysqlclient`                 | See [Original MySQL API](https://dev.mysql.com/doc/apis-php/en/apis-php-mysql.html) |
|                | `mysqli`, `ext/mysqli`interface          | `libmysqlclient`                 | See [MySQL Improved Extension](https://dev.mysql.com/doc/apis-php/en/apis-php-mysqli.html) |
|                | `PDO_MYSQL`                              | `libmysqlclient`                 | See [MySQL Functions (PDO_MYSQL)](https://dev.mysql.com/doc/apis-php/en/apis-php-pdo-mysql.html) |
|                | PDO mysqlnd                              | Native Driver                    |                                          |
| Python         | Connector/Python                         | Native Driver                    | See [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/) |
| Python         | Connector/Python C Extension             | `libmysqlclient`                 | See [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/) |
|                | MySQLdb                                  | `libmysqlclient`                 | See [Section 27.11, “MySQL Python API”](https://dev.mysql.com/doc/refman/5.7/en/apis-python.html) |
| Ruby           | MySQL/Ruby                               | `libmysqlclient`                 | Uses `libmysqlclient`. See [Section 27.12.1, “The MySQL/Ruby API”](https://dev.mysql.com/doc/refman/5.7/en/apis-ruby-mysqlruby.html) |
|                | Ruby/MySQL                               | Native Driver                    | See [Section 27.12.2, “The Ruby/MySQL API”](https://dev.mysql.com/doc/refman/5.7/en/apis-ruby-rubymysql.html) |
| Scheme         | `Myscsh`                                 | `libmysqlclient`                 | See [`Myscsh`](https://github.com/aehrisch/myscsh) |
| SPL            | `sql_mysql`                              | `libmysqlclient`                 | See [`sql_mysql` for SPL](http://www.clifford.at/spl/spldoc/sql_mysql.html) |
| Tcl            | MySQLtcl                                 | `libmysqlclient`                 | See [Section 27.13, “MySQL Tcl API”](https://dev.mysql.com/doc/refman/5.7/en/apis-tcl.html) |

## Connector versions supported by TiDB

| Connector        | Connector Version            |
| ---------------- | ---------------------------- |
| Connector/C      | 6.1.0 GA                     |
| Connector/C++    | 1.0.5 GA                     |
| Connector/J      | 5.1.8                        |
| Connector/Net    | 6.9.9 GA                     |
| Connector/Net    | 6.8.8 GA                     |
| Connector/ODBC   | 5.1                          |
| Connector/ODBC   | 3.51 (Unicode not supported) |
| Connector/Python | 2.0                          |
| Connector/Python | 1.2                          |
