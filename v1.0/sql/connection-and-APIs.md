# 连接器和 API

数据库连接器为客户端提供了连接数据库服务端的方式，APIs 提供了使用 MySQL 协议和资源的底层接口。无论是连接器还是 API，都可以用来在不同的语言和环境内连接服务器并执行 sql 语句，包括 odbc、java(jdbc)、Perl、Python、PHP、Ruby 和 C。

TiDB 兼容 MySQL(5.6、5.7) 的所有连接器和 API，包括：

+ [MySQL Connector/C](https://dev.mysql.com/doc/refman/5.7/en/connector-c-info.html)
+ [MySQL Connector/C++](https://dev.mysql.com/doc/refman/5.7/en/connector-cpp-info.html)
+ [MySQL Connector/J](https://dev.mysql.com/doc/refman/5.7/en/connector-j-info.html)
+ [MySQL Connector/Net](https://dev.mysql.com/doc/refman/5.7/en/connector-net-info.html)
+ [MySQL Connector/ODBC](https://dev.mysql.com/doc/refman/5.7/en/connector-odbc-info.html)
+ [MySQL Connector/Python](https://dev.mysql.com/doc/refman/5.7/en/connector-python-info.html)
+ [MySQL C API](https://dev.mysql.com/doc/refman/5.7/en/c-api.html)
+ [MySQL PHP API](https://dev.mysql.com/doc/refman/5.7/en/apis-php-info.html)
+ [MySQL Perl API](https://dev.mysql.com/doc/refman/5.7/en/apis-perl.html)
+ [MySQL Python API](https://dev.mysql.com/doc/refman/5.7/en/apis-python.html)
+ [MySQL Ruby APIs](https://dev.mysql.com/doc/refman/5.7/en/apis-ruby.html)
+ [MySQL Tcl API](https://dev.mysql.com/doc/refman/5.7/en/apis-tcl.html)
+ [MySQL Eiffel Wrapper](https://dev.mysql.com/doc/refman/5.7/en/apis-eiffel.html)
+ [Mysql Go API](https://github.com/go-sql-driver/mysql)

## 使用 MySQL 连接器连接 TiDB

Oracle 官方提供了以下 API , TiDB 可以兼容所有这些 API。

+ [MySQL Connector/C](https://dev.mysql.com/doc/refman/5.7/en/connector-c-info.html)：C 语言的客户端库，是 libmysqlclient 的替代品
+ [MySQL Connector/C++](https://dev.mysql.com/doc/refman/5.7/en/connector-cpp-info.html)：C++ 语言的客户端库
+ [MySQL Connector/J](https://dev.mysql.com/doc/refman/5.7/en/connector-j-info.html)：Java 语言的客户端库，基于标准 JDBC 接口
+ [MySQL Connector/Net](https://dev.mysql.com/doc/refman/5.7/en/connector-net-info.html)：.Net 语言的客户端库，[MySQL for Visual Studio](https://dev.mysql.com/doc/visual-studio/en/)使用这个库，支持 Microsoft Visual Studio 2012，2013，2015和2017版本
+ [MySQL Connector/ODBC](https://dev.mysql.com/doc/refman/5.7/en/connector-odbc-info.html)：标准的 ODBC 接口，支持 Windows，Unix 和 OS X
+ [MySQL Connector/Python](https://dev.mysql.com/doc/refman/5.7/en/connector-python-info.html)：Python 语言的客户端包，和 [Python DB API version 2.0](http://www.python.org/dev/peps/pep-0249/) 一致

## 使用 MySQL C API 连接 TiDB

如果使用 C 语言程序直接连接 TiDB，可以直接链接 libmysqlclient 库，使用 MySQL 的 [C API](https://dev.mysql.com/doc/refman/5.7/en/c-api.html)，这是最主要的一种 C 语言连接方式，被各种客户端和 API 广泛使用，包括 Connector/C。

## 使用 MySQL 第三方 API 连接 TiDB

第三方 API 非 Oracle 官方提供，下表列出了常用的第三方 API：

| Environment    | API                                      | Type                             | Notes                                    |
| -------------- | ---------------------------------------- | -------------------------------- | ---------------------------------------- |
| Ada            | GNU Ada MySQL Bindings                   | `libmysqlclient`                 | See [MySQL Bindings for GNU Ada](http://gnade.sourceforge.net/) |
| C              | C API                                    | `libmysqlclient`                 | See [Section 27.8, “MySQL C API”](https://dev.mysql.com/doc/refman/5.7/en/c-api.html). |
| C              | Connector/C                              | Replacement for `libmysqlclient` | See [MySQL Connector/C Developer Guide](https://dev.mysql.com/doc/connector-c/en/). |
| C++            | Connector/C++                            | `libmysqlclient`                 | See [MySQL Connector/C++ Developer Guide](https://dev.mysql.com/doc/connector-cpp/en/). |
|                | MySQL++                                  | `libmysqlclient`                 | See [MySQL++ Web site](http://tangentsoft.net/mysql++/doc/). |
|                | MySQL wrapped                            | `libmysqlclient`                 | See [MySQL wrapped](http://www.alhem.net/project/mysql/). |
| Go             | go-sql-driver                            | Native Driver                    | See [Mysql Go API](https://github.com/go-sql-driver/mysql) |
| Cocoa          | MySQL-Cocoa                              | `libmysqlclient`                 | Compatible with the Objective-C Cocoa environment. See<http://mysql-cocoa.sourceforge.net/> |
| D              | MySQL for D                              | `libmysqlclient`                 | See [MySQL for D](http://www.steinmole.de/d/). |
| Eiffel         | Eiffel MySQL                             | `libmysqlclient`                 | See [Section 27.14, “MySQL Eiffel Wrapper”](https://dev.mysql.com/doc/refman/5.7/en/apis-eiffel.html). |
| Erlang         | `erlang-mysql-driver`                    | `libmysqlclient`                 | See [`erlang-mysql-driver`.](http://code.google.com/p/erlang-mysql-driver/) |
| Haskell        | Haskell MySQL Bindings                   | Native Driver                    | See [Brian O'Sullivan's pure Haskell MySQL bindings](http://www.serpentine.com/blog/software/mysql/). |
|                | `hsql-mysql`                             | `libmysqlclient`                 | See [MySQL driver for Haskell](http://hackage.haskell.org/cgi-bin/hackage-scripts/package/hsql-mysql-1.7). |
| Java/JDBC      | Connector/J                              | Native Driver                    | See [MySQL Connector/J 5.1 Developer Guide](https://dev.mysql.com/doc/connector-j/5.1/en/). |
| Kaya           | MyDB                                     | `libmysqlclient`                 | See [MyDB](http://kayalang.org/library/latest/MyDB). |
| Lua            | LuaSQL                                   | `libmysqlclient`                 | See [LuaSQL](http://keplerproject.github.io/luasql/doc/us/). |
| .NET/Mono      | Connector/Net                            | Native Driver                    | See [MySQL Connector/Net Developer Guide](https://dev.mysql.com/doc/connector-net/en/). |
| Objective Caml | OBjective Caml MySQL Bindings            | `libmysqlclient`                 | See [MySQL Bindings for Objective Caml](http://raevnos.pennmush.org/code/ocaml-mysql/). |
| Octave         | Database bindings for GNU Octave         | `libmysqlclient`                 | See [Database bindings for GNU Octave](http://octave.sourceforge.net/database/index.html). |
| ODBC           | Connector/ODBC                           | `libmysqlclient`                 | See [MySQL Connector/ODBC Developer Guide](https://dev.mysql.com/doc/connector-odbc/en/). |
| Perl           | `DBI`/`DBD::mysql`                       | `libmysqlclient`                 | See [Section 27.10, “MySQL Perl API”](https://dev.mysql.com/doc/refman/5.7/en/apis-perl.html). |
|                | `Net::MySQL`                             | Native Driver                    | See [`Net::MySQL`](http://search.cpan.org/dist/Net-MySQL/MySQL.pm) at CPAN |
| PHP            | `mysql`, `ext/mysql`interface (deprecated) | `libmysqlclient`                 | See [Original MySQL API](https://dev.mysql.com/doc/apis-php/en/apis-php-mysql.html). |
|                | `mysqli`, `ext/mysqli`interface          | `libmysqlclient`                 | See [MySQL Improved Extension](https://dev.mysql.com/doc/apis-php/en/apis-php-mysqli.html). |
|                | `PDO_MYSQL`                              | `libmysqlclient`                 | See [MySQL Functions (PDO_MYSQL)](https://dev.mysql.com/doc/apis-php/en/apis-php-pdo-mysql.html). |
|                | PDO mysqlnd                              | Native Driver                    |                                          |
| Python         | Connector/Python                         | Native Driver                    | See [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/). |
| Python         | Connector/Python C Extension             | `libmysqlclient`                 | See [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/). |
|                | MySQLdb                                  | `libmysqlclient`                 | See [Section 27.11, “MySQL Python API”](https://dev.mysql.com/doc/refman/5.7/en/apis-python.html). |
| Ruby           | MySQL/Ruby                               | `libmysqlclient`                 | Uses `libmysqlclient`. See [Section 27.12.1, “The MySQL/Ruby API”](https://dev.mysql.com/doc/refman/5.7/en/apis-ruby-mysqlruby.html). |
|                | Ruby/MySQL                               | Native Driver                    | See [Section 27.12.2, “The Ruby/MySQL API”](https://dev.mysql.com/doc/refman/5.7/en/apis-ruby-rubymysql.html). |
| Scheme         | `Myscsh`                                 | `libmysqlclient`                 | See [`Myscsh`](https://github.com/aehrisch/myscsh). |
| SPL            | `sql_mysql`                              | `libmysqlclient`                 | See [`sql_mysql` for SPL](http://www.clifford.at/spl/spldoc/sql_mysql.html). |
| Tcl            | MySQLtcl                                 | `libmysqlclient`                 | See [Section 27.13, “MySQL Tcl API”](https://dev.mysql.com/doc/refman/5.7/en/apis-tcl.html). |

## TiDB 支持的连接器版本

| Connector        | Connector version            |
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
