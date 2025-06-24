---
title: 系统变量
summary: 使用系统变量来优化性能或改变运行行为。
---

# 系统变量

TiDB 系统变量的行为与 MySQL 类似，设置应用于 `SESSION` 或 `GLOBAL` 范围：

- 在 `SESSION` 范围内的更改只会影响当前会话。
- 在 `GLOBAL` 范围内的更改会立即生效。如果此变量也是 `SESSION` 范围的，则所有会话（包括您的会话）将继续使用其当前的会话值。
- 使用 [`SET` 语句](/sql-statements/sql-statement-set-variable.md) 进行更改：

```sql
# 这两个相同的语句更改会话变量
SET tidb_distsql_scan_concurrency = 10;
SET SESSION tidb_distsql_scan_concurrency = 10;

# 这两个相同的语句更改全局变量
SET @@global.tidb_distsql_scan_concurrency = 10;
SET GLOBAL tidb_distsql_scan_concurrency = 10;
```

> **注意：**
>
> 几个 `GLOBAL` 变量会持久化到 TiDB 集群。本文档中的某些变量具有“持久化到集群”设置，可以配置为“是”或“否”。
>
> - 对于“持久化到集群：是”的变量，当全局变量更改时，会向所有 TiDB 服务器发送通知以刷新其系统变量缓存。当您添加其他 TiDB 服务器或重新启动现有 TiDB 服务器时，将自动使用持久化的配置值。
> - 对于“持久化到集群：否”的变量，更改仅适用于您连接到的本地 TiDB 实例。要保留任何设置的值，您需要在 `tidb.toml` 配置文件中指定这些变量。
>
> 此外，TiDB 将几个 MySQL 变量显示为可读和可设置。这是兼容性所必需的，因为应用程序和连接器通常会读取 MySQL 变量。例如，JDBC 连接器会读取和设置查询缓存设置，尽管不依赖于该行为。

> **注意：**
>
> 较大的值并不总是能带来更好的性能。同样重要的是要考虑执行语句的并发连接数，因为大多数设置都适用于每个连接。
>
> 在确定安全值时，请考虑变量的单位：
>
> * 对于线程，安全值通常最多为 CPU 核心数。
> * 对于字节，安全值通常小于系统内存量。
> * 对于时间，请注意单位可能是秒或毫秒。
>
> 使用相同单位的变量可能会争用同一组资源。

从 v7.4.0 开始，您可以使用 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) 在语句执行期间临时修改某些 `SESSION` 变量的值。语句执行完毕后，当前会话中系统变量的值会自动更改回原始值。此 hint 可用于修改一些与优化器和执行器相关的系统变量。本文档中的变量具有“适用于 hint SET_VAR”设置，可以配置为“是”或“否”。

- 对于“适用于 hint SET_VAR：是”的变量，您可以使用 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint 在语句执行期间修改当前会话中系统变量的值。
- 对于“适用于 hint SET_VAR：否”的变量，您不能使用 [`SET_VAR`](/optimizer-hints.md#set_varvar_namevar_value) hint 在语句执行期间修改当前会话中系统变量的值。

有关 `SET_VAR` hint 的更多信息，请参阅 [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)。

## 变量参考

### allow_auto_random_explicit_insert <span class="version-mark">v4.0.3 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔
- 默认值：`OFF`
- 确定是否允许在 `INSERT` 语句中显式指定具有 `AUTO_RANDOM` 属性的列的值。

### authentication_ldap_sasl_auth_method_name <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`SCRAM-SHA-1`
- 可能的值：`SCRAM-SHA-1`、`SCRAM-SHA-256` 和 `GSSAPI`。
- 对于 LDAP SASL 身份验证，此变量指定身份验证方法名称。

### authentication_ldap_sasl_bind_base_dn <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：字符串
- 默认值：""
- 对于 LDAP SASL 身份验证，此变量限制搜索树内的搜索范围。如果创建用户时没有 `AS ...` 子句，TiDB 将根据用户名自动在 LDAP 服务器中搜索 `dn`。

### authentication_ldap_sasl_bind_root_dn <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：字符串
- 默认值：""
- 对于 LDAP SASL 身份验证，此变量指定用于登录到 LDAP 服务器以搜索用户的 `dn`。

### authentication_ldap_sasl_bind_root_pwd <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：字符串
- 默认值：""
- 对于 LDAP SASL 身份验证，此变量指定用于登录到 LDAP 服务器以搜索用户的密码。

### authentication_ldap_sasl_ca_path <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：字符串
- 默认值：""
- 对于 LDAP SASL 身份验证，此变量指定 StartTLS 连接的证书颁发机构文件的绝对路径。

### authentication_ldap_sasl_init_pool_size <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`10`
- 范围：`[1, 32767]`
- 对于 LDAP SASL 身份验证，此变量指定 LDAP 服务器连接池中的初始连接数。

### authentication_ldap_sasl_max_pool_size <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`1000`
- 范围：`[1, 32767]`
- 对于 LDAP SASL 身份验证，此变量指定 LDAP 服务器连接池中的最大连接数。

### authentication_ldap_sasl_server_host <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：字符串
- 默认值：""
- 对于 LDAP SASL 身份验证，此变量指定 LDAP 服务器主机名或 IP 地址。

### authentication_ldap_sasl_server_port <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`389`
- 范围：`[1, 65535]`
- 对于 LDAP SASL 身份验证，此变量指定 LDAP 服务器的 TCP/IP 端口号。

### authentication_ldap_sasl_tls <span class="version-mark">v7.1.0 新增</span>

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔
- 默认值：`OFF`
- 对于 LDAP SASL 身份验证，此变量控制插件与 LDAP 服务器的连接是否受 StartTLS 保护。

### authentication_ldap_simple_auth_method_name <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 枚举
- 默认值: `SIMPLE`
- 可选值: `SIMPLE`。
- 对于 LDAP 简单认证，此变量指定认证方法名称。唯一支持的值是 `SIMPLE`。

### authentication_ldap_simple_bind_base_dn <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 字符串
- 默认值: ""
- 对于 LDAP 简单认证，此变量限制搜索树内的搜索范围。如果用户创建时没有使用 `AS ...` 子句，TiDB 将根据用户名自动在 LDAP 服务器中搜索 `dn`。

### authentication_ldap_simple_bind_root_dn <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 字符串
- 默认值: ""
- 对于 LDAP 简单认证，此变量指定用于登录 LDAP 服务器以搜索用户的 `dn`。

### authentication_ldap_simple_bind_root_pwd <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 字符串
- 默认值: ""
- 对于 LDAP 简单认证，此变量指定用于登录 LDAP 服务器以搜索用户的密码。

### authentication_ldap_simple_ca_path <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 字符串
- 默认值: ""
- 对于 LDAP 简单认证，此变量指定 StartTLS 连接的证书颁发机构文件的绝对路径。

### authentication_ldap_simple_init_pool_size <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 整数
- 默认值: `10`
- 范围: `[1, 32767]`
- 对于 LDAP 简单认证，此变量指定到 LDAP 服务器的连接池中的初始连接数。

### authentication_ldap_simple_max_pool_size <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 整数
- 默认值: `1000`
- 范围: `[1, 32767]`
- 对于 LDAP 简单认证，此变量指定到 LDAP 服务器的连接池中的最大连接数。

### authentication_ldap_simple_server_host <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 字符串
- 默认值: ""
- 对于 LDAP 简单认证，此变量指定 LDAP 服务器主机名或 IP 地址。

### authentication_ldap_simple_server_port <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 整数
- 默认值: `389`
- 范围: `[1, 65535]`
- 对于 LDAP 简单认证，此变量指定 LDAP 服务器的 TCP/IP 端口号。

### authentication_ldap_simple_tls <span class="version-mark">v7.1.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 布尔值
- 默认值: `OFF`
- 对于 LDAP 简单认证，此变量控制插件到 LDAP 服务器的连接是否受 StartTLS 保护。

### auto_increment_increment

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 整数
- 默认值: `1`
- 范围: `[1, 65535]`
- 控制分配给列的 `AUTO_INCREMENT` 值的步长，以及 `AUTO_RANDOM` ID 的分配规则。通常与 [`auto_increment_offset`](#auto_increment_offset) 结合使用。

### auto_increment_offset

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 整数
- 默认值: `1`
- 范围: `[1, 65535]`
- 控制分配给列的 `AUTO_INCREMENT` 值的初始偏移量，以及 `AUTO_RANDOM` ID 的分配规则。此设置通常与 [`auto_increment_increment`](#auto_increment_increment) 结合使用。例如：

```sql
mysql> CREATE TABLE t1 (a int not null primary key auto_increment);
Query OK, 0 rows affected (0.10 sec)

mysql> set auto_increment_offset=1;
Query OK, 0 rows affected (0.00 sec)

mysql> set auto_increment_increment=3;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (),(),(),();
Query OK, 4 rows affected (0.04 sec)
Records: 4  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+
| a  |
+----+
|  1 |
|  4 |
|  7 |
| 10 |
+----+
4 rows in set (0.00 sec)
```

### autocommit

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 布尔值
- 默认值: `ON`
- 控制语句在没有显式事务时是否应自动提交。有关更多信息，请参见 [事务概述](/transaction-overview.md#autocommit)。

### block_encryption_mode

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: 枚举
- 默认值: `aes-128-ecb`
- 值选项: `aes-128-ecb`, `aes-192-ecb`, `aes-256-ecb`, `aes-128-cbc`, `aes-192-cbc`, `aes-256-cbc`, `aes-128-ofb`, `aes-192-ofb`, `aes-256-ofb`, `aes-128-cfb`, `aes-192-cfb`, `aes-256-cfb`
- 此变量设置内置函数 [`AES_ENCRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_encrypt) 和 [`AES_DECRYPT()`](/functions-and-operators/encryption-and-compression-functions.md#aes_decrypt) 的加密模式。

### character_set_client

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 默认值: `utf8mb4`
- 从客户端发送的数据的字符集。有关在 TiDB 中使用字符集和排序规则的详细信息，请参见 [字符集和排序规则](/character-set-and-collation.md)。建议使用 [`SET NAMES`](/sql-statements/sql-statement-set-names.md) 在需要时更改字符集。

### character_set_connection

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 默认值: `utf8mb4`
- 没有指定字符集的字符串文字的字符集。

### character_set_database

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 默认值: `utf8mb4`
- 此变量指示正在使用的默认数据库的字符集。**不建议设置此变量**。当选择新的默认数据库时，服务器会更改变量值。

### character_set_results

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 默认值: `utf8mb4`
- 将数据发送到客户端时使用的字符集。

### character_set_server

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 默认值: `utf8mb4`
- 服务器的默认字符集。

### collation_connection

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`utf8mb4_bin`
- 此变量指示当前连接中使用的排序规则。它与 MySQL 变量 `collation_connection` 一致。

### collation_database

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`utf8mb4_bin`
- 此变量指示正在使用的数据库的默认排序规则。**不建议设置此变量**。当选择一个新的数据库时，TiDB 会更改此变量的值。

### collation_server

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`utf8mb4_bin`
- 创建数据库时使用的默认排序规则。

### cte_max_recursion_depth

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：整数
- 默认值：`1000`
- 范围：`[0, 4294967295]`
- 控制公共表表达式中的最大递归深度。

### datadir

> **注意：**
>
> 此变量在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 上不受支持。

<CustomContent platform="tidb">

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：取决于组件和部署方法。
    - `/tmp/tidb`：当你为 [`--store`](/command-line-flags-for-tidb-configuration.md#--store) 设置 `"unistore"` 时，或者如果你不设置 `--store`。
    - `${pd-ip}:${pd-port}`：当你使用 TiKV 时，这是 TiUP 和 Kubernetes 部署的 TiDB Operator 的默认存储引擎。
- 此变量指示数据存储的位置。此位置可以是本地路径 `/tmp/tidb`，或者如果数据存储在 TiKV 上，则指向 PD 服务器。`${pd-ip}:${pd-port}` 格式的值表示 TiDB 启动时连接到的 PD 服务器。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：取决于组件和部署方法。
    - `/tmp/tidb`：当你为 [`--store`](https://docs.pingcap.com/tidb/stable/command-line-flags-for-tidb-configuration#--store) 设置 `"unistore"` 时，或者如果你不设置 `--store`。
    - `${pd-ip}:${pd-port}`：当你使用 TiKV 时，这是 TiUP 和 Kubernetes 部署的 TiDB Operator 的默认存储引擎。
- 此变量指示数据存储的位置。此位置可以是本地路径 `/tmp/tidb`，或者如果数据存储在 TiKV 上，则指向 PD 服务器。`${pd-ip}:${pd-port}` 格式的值表示 TiDB 启动时连接到的 PD 服务器。

</CustomContent>

### ddl_slow_threshold

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于你当前连接的 TiDB 实例。
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`300`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 记录执行时间超过阈值的 DDL 操作。

### default_authentication_plugin

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`mysql_native_password`
- 可能的值：`mysql_native_password`、`caching_sha2_password`、`tidb_sm3_password`、`tidb_auth_token`、`authentication_ldap_sasl` 和 `authentication_ldap_simple`。
- 此变量设置服务器在建立服务器-客户端连接时声明的身份验证方法。
- 要使用 `tidb_sm3_password` 方法进行身份验证，你可以使用 [TiDB-JDBC](https://github.com/pingcap/mysql-connector-j/tree/release/8.0-sm3) 连接到 TiDB。

<CustomContent platform="tidb">

有关此变量的更多可能值，请参阅 [身份验证插件状态](/security-compatibility-with-mysql.md#authentication-plugin-status)。

</CustomContent>

### default_collation_for_utf8mb4 <span class="version-mark">v7.4.0 新增</span>

- 作用域：GLOBAL | SESSION
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：字符串
- 默认值：`utf8mb4_bin`
- 可选值：`utf8mb4_bin`、`utf8mb4_general_ci`、`utf8mb4_0900_ai_ci`
- 此变量用于设置 `utf8mb4` 字符集的默认[排序规则](/character-set-and-collation.md)。它会影响以下语句的行为：
    - [`SHOW COLLATION`](/sql-statements/sql-statement-show-collation.md) 和 [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) 语句中显示的默认排序规则。
    - 如果 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 和 [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) 语句包含针对表或列的 `CHARACTER SET utf8mb4` 子句，但未指定排序规则，则使用此变量指定的排序规则。这不会影响不使用 `CHARACTER SET` 子句时的行为。
    - 如果 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) 和 [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md) 语句包含 `CHARACTER SET utf8mb4` 子句，但未指定排序规则，则使用此变量指定的排序规则。这不会影响不使用 `CHARACTER SET` 子句时的行为。
    - 如果未使用 `COLLATE` 子句，则任何 `_utf8mb4'string'` 格式的文字字符串都使用此变量指定的排序规则。

### default_password_lifetime <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`0`
- 范围：`[0, 65535]`
- 设置自动密码过期的全局策略。默认值 `0` 表示密码永不过期。如果此系统变量设置为正整数 `N`，则表示密码有效期为 `N` 天，你必须在 `N` 天内更改密码。

### default_week_format

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`0`
- 范围：`[0, 7]`
- 设置 `WEEK()` 函数使用的星期格式。

### disconnect_on_expired_password <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`ON`
- 此变量是只读的。它指示当密码过期时，TiDB 是否断开客户端连接。如果变量设置为 `ON`，则当密码过期时，客户端连接将断开。如果变量设置为 `OFF`，则客户端连接将限制为“沙盒模式”，并且用户只能执行密码重置操作。

<CustomContent platform="tidb">

- 如果你需要更改过期密码的客户端连接的行为，请修改配置文件中的 [`security.disconnect-on-expired-password`](/tidb-configuration-file.md#disconnect-on-expired-password-new-in-v650) 配置项。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 如果你需要更改过期密码的客户端连接的默认行为，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

### div_precision_increment <span class="version-mark">v8.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`4`
- 取值范围：`[0, 30]`
- 该变量指定使用 `/` 运算符执行除法运算时，结果的小数位数增加的位数。该变量与 MySQL 相同。

### error_count

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 一个只读变量，指示生成消息的最后一个语句产生的错误数。

### foreign_key_checks

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：v6.6.0 之前，默认值为 `OFF`。从 v6.6.0 开始，默认值为 `ON`。
- 该变量控制是否启用外键约束检查。

### group_concat_max_len

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1024`
- 取值范围：`[4, 18446744073709551615]`
- `GROUP_CONCAT()` 函数中项目的最大缓冲区大小。

### have_openssl

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`DISABLED`
- 用于 MySQL 兼容性的只读变量。当服务器启用 TLS 时，服务器将其设置为 `YES`。

### have_ssl

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`DISABLED`
- 用于 MySQL 兼容性的只读变量。当服务器启用 TLS 时，服务器将其设置为 `YES`。

### hostname

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：（系统主机名）
- TiDB 服务器的主机名，作为只读变量。

### identity <span class="version-mark">v5.3.0 新增</span>

该变量是 [`last_insert_id`](#last_insert_id) 的别名。

### init_connect

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- `init_connect` 功能允许在首次连接到 TiDB 服务器时自动执行 SQL 语句。如果您具有 `CONNECTION_ADMIN` 或 `SUPER` 权限，则不会执行此 `init_connect` 语句。如果 `init_connect` 语句导致错误，您的用户连接将被终止。

### innodb_lock_wait_timeout

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`50`
- 取值范围：`[1, 3600]`
- 单位：秒
- 悲观事务的锁等待超时时间（默认）。

### interactive_timeout

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`28800`
- 取值范围：`[1, 31536000]`
- 单位：秒
- 此变量表示交互式用户会话的空闲超时时间。交互式用户会话是指通过使用 `CLIENT_INTERACTIVE` 选项调用 [`mysql_real_connect()`](https://dev.mysql.com/doc/c-api/5.7/en/mysql-real-connect.html) API 建立的会话（例如，MySQL Shell 和 MySQL Client）。此变量与 MySQL 完全兼容。

### last_insert_id

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 取值范围：`[0, 18446744073709551615]`
- 此变量返回由 insert 语句生成的最后一个 `AUTO_INCREMENT` 或 `AUTO_RANDOM` 值。
- `last_insert_id` 的值与函数 `LAST_INSERT_ID()` 返回的值相同。

### last_plan_from_binding <span class="version-mark">v4.0 新增</span>

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于显示先前语句中使用的执行计划是否受到 [计划绑定](/sql-plan-management.md) 的影响。

### last_plan_from_cache <span class="version-mark">v4.0 新增</span>

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于显示先前 `execute` 语句中使用的执行计划是否直接从计划缓存中获取。

### last_sql_use_alloc <span class="version-mark">v6.4.0 新增</span>

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`OFF`
- 此变量是只读的。它用于显示先前的语句是否使用了缓存的 chunk 对象（chunk 分配）。

### license

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`Apache License 2.0`
- 此变量指示 TiDB 服务器安装的许可证。

### log_bin

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量指示是否使用 [TiDB Binlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)。

### max_allowed_packet <span class="version-mark">v6.1.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`67108864`
- 取值范围：`[1024, 1073741824]`
- 该值应为 1024 的整数倍。如果该值不能被 1024 整除，则会提示警告，并且该值将被向下舍入。例如，当该值设置为 1025 时，TiDB 中的实际值为 1024。
- 服务器和客户端在一次数据包传输中允许的最大数据包大小。
- 在 `SESSION` 作用域中，此变量是只读的。
- 此变量与 MySQL 兼容。

### password_history <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 取值范围：`[0, 4294967295]`
- 此变量用于建立密码重用策略，允许 TiDB 根据密码更改的次数限制密码重用。默认值 `0` 表示禁用基于密码更改次数的密码重用策略。当此变量设置为正整数 `N` 时，不允许重用最近 `N` 个密码。

### mpp_exchange_compression_mode <span class="version-mark">v6.6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：`UNSPECIFIED`
- 取值选项：`NONE`，`FAST`，`HIGH_COMPRESSION`，`UNSPECIFIED`
- 此变量用于指定 MPP Exchange 算子的数据压缩模式。当 TiDB 选择版本号为 `1` 的 MPP 执行计划时，此变量生效。变量值的含义如下：
    - `UNSPECIFIED`：表示未指定。TiDB 将自动选择压缩模式。目前，TiDB 自动选择 `FAST` 模式。
    - `NONE`：不使用数据压缩。
    - `FAST`：快速模式。整体性能良好，压缩率低于 `HIGH_COMPRESSION`。
- `HIGH_COMPRESSION`: 高压缩比模式。

### mpp_version <span class="version-mark">v6.6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：`UNSPECIFIED`
- 可选值：`UNSPECIFIED`，`0`，`1`，`2`
- 此变量用于指定 MPP 执行计划的不同版本。指定版本后，TiDB 会选择指定版本的 MPP 执行计划。变量值的含义如下：
    - `UNSPECIFIED`: 表示未指定。TiDB 自动选择最新版本 `2`。
    - `0`: 兼容所有 TiDB 集群版本。MPP 版本大于 `0` 的功能在此模式下不生效。
    - `1`: v6.6.0 新增，用于启用 TiFlash 上带压缩的数据交换。有关详细信息，请参阅 [MPP 版本和交换数据压缩](/explain-mpp.md#mpp-version-and-exchange-data-compression)。
    - `2`: v7.3.0 新增，用于在 MPP 任务在 TiFlash 上遇到错误时提供更准确的错误消息。

### password_reuse_interval <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 4294967295]`
- 此变量用于建立密码重用策略，允许 TiDB 基于经过的时间限制密码重用。默认值 `0` 表示禁用基于经过时间的密码重用策略。当此变量设置为正整数 `N` 时，不允许重用过去 `N` 天内使用的任何密码。

### max_connections

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 100000]`
- 单个 TiDB 实例允许的最大并发连接数。此变量可用于资源控制。
- 默认值 `0` 表示没有限制。当此变量的值大于 `0`，并且连接数达到该值时，TiDB 服务器将拒绝来自客户端的新连接。

### max_execution_time

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 语句的最大执行时间。默认值为无限制（零）。

> **注意：**
>
> 在 v6.4.0 之前，`max_execution_time` 系统变量对所有类型的语句生效。从 v6.4.0 开始，此变量仅控制只读语句的最大执行时间。超时值的精度约为 100 毫秒。这意味着语句可能不会在你指定的精确毫秒数内终止。

<CustomContent platform="tidb">

对于带有 [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint 的 SQL 语句，此语句的最大执行时间受 hint 限制，而不是受此变量限制。该 hint 也可以与 SQL 绑定一起使用，如 [SQL FAQ](/faq/sql-faq.md#how-to-prevent-the-execution-of-a-particular-sql-statement) 中所述。

</CustomContent>

<CustomContent platform="tidb-cloud">

对于带有 [`MAX_EXECUTION_TIME`](/optimizer-hints.md#max_execution_timen) hint 的 SQL 语句，此语句的最大执行时间受 hint 限制，而不是受此变量限制。该 hint 也可以与 SQL 绑定一起使用，如 [SQL FAQ](https://docs.pingcap.com/tidb/stable/sql-faq) 中所述。

</CustomContent>

### max_prepared_stmt_count

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[-1, 1048576]`
- 指定当前 TiDB 实例中 [`PREPARE`](/sql-statements/sql-statement-prepare.md) 语句的最大数量。
- 值 `-1` 表示当前 TiDB 实例中 `PREPARE` 语句的最大数量没有限制。
- 如果将变量设置为超过上限 `1048576` 的值，则使用 `1048576` 代替：

```sql
mysql> SET GLOBAL max_prepared_stmt_count = 1048577;
Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;
+---------+------+--------------------------------------------------------------+
| Level   | Code | Message                                                      |
+---------+------+--------------------------------------------------------------+
| Warning | 1292 | Truncated incorrect max_prepared_stmt_count value: '1048577' |
+---------+------+--------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GLOBAL VARIABLES LIKE 'max_prepared_stmt_count';
+-------------------------+---------+
| Variable_name           | Value   |
+-------------------------+---------+
| max_prepared_stmt_count | 1048576 |
+-------------------------+---------+
1 row in set (0.00 sec)
```

### pd_enable_follower_handle_region <span class="version-mark">v7.6.0 新增</span>

> **警告：**
>
> [Active PD Follower](https://docs.pingcap.com/tidb/dev/tune-region-performance#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service) 功能是实验性的。不建议在生产环境中使用。此功能可能会更改或删除，恕不另行通知。如果发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否启用 Active PD Follower 功能（目前仅适用于 Region 信息请求）。当值为 `OFF` 时，TiDB 仅从 PD leader 获取 Region 信息。当值为 `ON` 时，TiDB 将 Region 信息请求均匀地分配给所有 PD 服务器，PD follower 也可以处理 Region 请求，从而降低 PD leader 的 CPU 压力。
- 启用 Active PD Follower 的场景：
    * 在具有大量 Region 的集群中，由于处理心跳和调度任务的开销增加，PD leader 遇到高 CPU 压力。
    * 在具有许多 TiDB 实例的 TiDB 集群中，由于 Region 信息请求的高并发，PD leader 遇到高 CPU 压力。

### plugin_dir

> **注意：**
>
> [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 不支持此变量。

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 指示要加载插件的目录，由命令行标志指定。

### plugin_load

> **注意：**
>
> [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 不支持此变量。

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 指示 TiDB 启动时要加载的插件。这些插件由命令行标志指定，并用逗号分隔。

### port

- 作用域：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`4000`
- 范围：`[0, 65535]`
- `tidb-server` 在使用 MySQL 协议时监听的端口。

### rand_seed1

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 此变量用于为 `RAND()` SQL 函数中使用的随机值生成器设定种子。
- 此变量的行为与 MySQL 兼容。

### rand_seed2

- 范围：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 此变量用于为 `RAND()` SQL 函数中使用的随机值生成器设定种子。
- 此变量的行为与 MySQL 兼容。

### require_secure_transport <span class="version-mark">v6.1.0 新增</span>

> **注意：**
>
> 目前，[TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 不支持此变量。请**勿**为 TiDB Cloud Dedicated 集群启用此变量。否则，可能会导致 SQL 客户端连接失败。此限制是一项临时控制措施，将在未来的版本中解决。

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：对于 TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `OFF`，对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `ON`

<CustomContent platform="tidb">

- 此变量确保所有与 TiDB 的连接要么在本地套接字上，要么使用 TLS。有关更多详细信息，请参阅[启用 TiDB 客户端和服务器之间的 TLS](/enable-tls-between-clients-and-servers.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量确保所有与 TiDB 的连接要么在本地套接字上，要么使用 TLS。

</CustomContent>

- 将此变量设置为 `ON` 需要你从启用了 TLS 的会话连接到 TiDB。这有助于防止在 TLS 配置不正确时出现锁定情况。
- 此设置以前是一个 `tidb.toml` 选项 (`security.require-secure-transport`)，但从 TiDB v6.1.0 开始更改为系统变量。
- 从 v6.5.6、v7.1.2、v7.5.1 和 v8.0.0 开始，当启用安全增强模式 (SEM) 时，禁止将此变量设置为 `ON`，以避免用户潜在的连接问题。

### skip_name_resolve <span class="version-mark">v5.2.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 范围：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`
- 此变量控制 `tidb-server` 实例是否在连接握手过程中解析主机名。
- 当 DNS 不可靠时，你可以启用此选项以提高网络性能。

> **注意：**
>
> 当 `skip_name_resolve=ON` 时，身份中包含主机名的用户将无法再登录到服务器。例如：
>
> ```sql
> CREATE USER 'appuser'@'apphost' IDENTIFIED BY 'app-password';
> ```
>
> 在此示例中，建议将 `apphost` 替换为 IP 地址或通配符 (`%`)。

### socket

- 范围：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- `tidb-server` 在使用 MySQL 协议时监听的本地 unix 套接字文件。

### sql_log_bin

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`ON`
- 指示是否将更改写入 [TiDB Binlog](https://docs.pingcap.com/tidb/stable/tidb-binlog-overview)。

> **注意：**
>
> 不建议将 `sql_log_bin` 设置为全局变量，因为未来版本的 TiDB 可能只允许将其设置为会话变量。

### sql_mode

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：`ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION`
- 此变量控制许多 MySQL 兼容性行为。有关更多信息，请参阅 [SQL Mode](/sql-mode.md)。

### sql_require_primary_key <span class="version-mark">v6.3.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`
- 此变量控制是否强制要求表具有主键。启用此变量后，尝试创建或更改没有主键的表将产生错误。
- 此功能基于 MySQL 8.0 中类似命名的 [`sql_require_primary_key`](https://dev.mysql.com/doc/refman/8.0/en/server-system-variables.html#sysvar_sql_require_primary_key)。
- 强烈建议在使用 TiCDC 时启用此变量。这是因为将更改复制到 MySQL sink 需要表具有主键。

<CustomContent platform="tidb">

- 如果你启用此变量并使用 TiDB Data Migration (DM) 迁移数据，建议你将 `sql_require_ primary_key` 添加到 [DM 任务配置文件](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) 的 `session` 部分，并将其设置为 `OFF`。否则，将导致 DM 无法创建任务。

</CustomContent>

### sql_select_limit <span class="version-mark">v4.0.2 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`18446744073709551615`
- 范围：`[0, 18446744073709551615]`
- 单位：行
- `SELECT` 语句返回的最大行数。

### ssl_ca

<CustomContent platform="tidb">

- 范围：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 证书颁发机构文件的位置（如果有）。此变量的值由 TiDB 配置文件项 [`ssl-ca`](/tidb-configuration-file.md#ssl-ca) 定义。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 范围：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 证书颁发机构文件的位置（如果有）。此变量的值由 TiDB 配置文件项 [`ssl-ca`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-ca) 定义。

</CustomContent>

### ssl_cert

<CustomContent platform="tidb">

- 范围：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 用于 SSL/TLS 连接的证书文件的位置（如果有文件）。此变量的值由 TiDB 配置文件项 [`ssl-cert`](/tidb-configuration-file.md#ssl-cert) 定义。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 范围：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 用于 SSL/TLS 连接的证书文件的位置（如果有文件）。此变量的值由 TiDB 配置文件项 [`ssl-cert`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-cert) 定义。

</CustomContent>

### ssl_key

<CustomContent platform="tidb">

- 范围：NONE
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 用于 SSL/TLS 连接的私钥文件（如果存在）的位置。此变量的值由 TiDB 配置文件项 [`ssl-key`](/tidb-configuration-file.md#ssl-cert) 定义。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 范围：无
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 用于 SSL/TLS 连接的私钥文件（如果存在）的位置。此变量的值由 TiDB 配置文件项 [`ssl-key`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#ssl-key) 定义。

</CustomContent>

### system_time_zone

- 范围：无
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：（系统相关）
- 此变量显示 TiDB 首次启动时的系统时区。另请参阅 [`time_zone`](#time_zone)。

### tidb_adaptive_closest_read_threshold <span class="version-mark">v6.3.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`4096`
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 此变量用于控制当 [`tidb_replica_read`](#tidb_replica_read-new-in-v40) 设置为 `closest-adaptive` 时，TiDB 服务器倾向于将读取请求发送到与 TiDB 服务器位于同一可用区中的副本的阈值。如果估计结果高于或等于此阈值，TiDB 倾向于将读取请求发送到同一可用区中的副本。否则，TiDB 将读取请求发送到 leader 副本。

### tidb_allow_tiflash_cop <span class="version-mark">v7.3.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`
- 当 TiDB 将计算任务下推到 TiFlash 时，有三种方法（或协议）可供选择：Cop、BatchCop 和 MPP。与 Cop 和 BatchCop 相比，MPP 协议更成熟，并提供更好的任务和资源管理。因此，建议使用 MPP 协议。
    - `0` 或 `OFF`：优化器仅生成使用 TiFlash MPP 协议的计划。
    - `1` 或 `ON`：优化器根据成本估算确定是使用 Cop、BatchCop 还是 MPP 协议来生成执行计划。

### tidb_allow_batch_cop <span class="version-mark">v4.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：整数
- 默认值：`1`
- 范围：`[0, 2]`
- 此变量用于控制 TiDB 如何将 coprocessor 请求发送到 TiFlash。它具有以下值：

    * `0`：从不批量发送请求
    * `1`：聚合和连接请求批量发送
    * `2`：所有 coprocessor 请求批量发送

### tidb_allow_fallback_to_tikv <span class="version-mark">v5.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：""
- 此变量用于指定可能回退到 TiKV 的存储引擎列表。如果 SQL 语句的执行由于列表中指定的存储引擎发生故障而失败，TiDB 会使用 TiKV 重试执行此 SQL 语句。此变量可以设置为 "" 或 "tiflash"。当此变量设置为 "tiflash" 时，如果 TiFlash 返回超时错误（错误代码：ErrTiFlashServerTimeout），TiDB 会使用 TiKV 重试执行此 SQL 语句。

### tidb_allow_function_for_expression_index <span class="version-mark">v5.2.0 新增</span>

- 范围：无
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`json_array, json_array_append, json_array_insert, json_contains, json_contains_path, json_depth, json_extract, json_insert, json_keys, json_length, json_merge_patch, json_merge_preserve, json_object, json_pretty, json_quote, json_remove, json_replace, json_search, json_set, json_storage_size, json_type, json_unquote, json_valid, lower, md5, reverse, tidb_shard, upper, vitess_hash`
- 此只读变量用于显示允许用于创建[表达式索引](/sql-statements/sql-statement-create-index.md#expression-index)的函数。

### tidb_allow_mpp <span class="version-mark">v5.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔值
- 默认值：`ON`
- 控制是否使用 TiFlash 的 MPP 模式来执行查询。值选项如下：
    - `0` 或 `OFF`，表示不使用 MPP 模式。对于 v7.3.0 或更高版本，如果将此变量的值设置为 `0` 或 `OFF`，还需要启用 [`tidb_allow_tiflash_cop`](/system-variables.md#tidb_allow_tiflash_cop-new-in-v730) 变量。否则，查询可能会返回错误。
    - `1` 或 `ON`，表示优化器根据成本估算（默认）确定是否使用 MPP 模式。

MPP 是 TiFlash 引擎提供的分布式计算框架，允许节点之间的数据交换，并提供高性能、高吞吐量的 SQL 算法。有关 MPP 模式选择的详细信息，请参阅[控制是否选择 MPP 模式](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)。

### tidb_allow_remove_auto_inc <span class="version-mark">v2.1.18 和 v3.0.4 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

- 范围：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`
- 此变量用于设置是否允许通过执行 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 语句删除列的 `AUTO_INCREMENT` 属性。默认情况下不允许。

### tidb_analyze_distsql_scan_concurrency <span class="version-mark">v7.6.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`4`
- 范围：`[1, 4294967295]`
- 此变量用于设置执行 `ANALYZE` 操作时 `scan` 操作的并发度。

### tidb_analyze_partition_concurrency

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`2`。对于 v7.4.0 及更早版本，默认值为 `1`。
- 此变量指定 TiDB 分析分区表时，读取和写入分区表的统计信息的并发度。

### tidb_analyze_version <span class="version-mark">v5.1.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`2`
- 范围：`[1, 2]`
- 控制 TiDB 如何收集统计信息。
    - 对于 TiDB Self-Managed，从 v5.3.0 开始，此变量的默认值从 `1` 更改为 `2`。
    - 对于 TiDB Cloud，从 v6.5.0 开始，此变量的默认值从 `1` 更改为 `2`。
    - 如果您的集群是从早期版本升级的，则升级后 `tidb_analyze_version` 的默认值不会更改。
- 有关此变量的详细介绍，请参见[统计信息介绍](/statistics.md)。

### tidb_analyze_skip_column_types <span class="version-mark">v7.2.0 新增</span>

- 范围：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值："json,blob,mediumblob,longblob"
- 可能的值: "json,blob,mediumblob,longblob,text,mediumtext,longtext"
- 此变量控制在执行 `ANALYZE` 命令收集统计信息时，哪些类型的列将被跳过统计信息收集。该变量仅适用于 `tidb_analyze_version = 2`。即使你使用 `ANALYZE TABLE t COLUMNS c1, ... , cn` 指定了一个列，如果该列的类型在 `tidb_analyze_skip_column_types` 中，也不会收集该列的统计信息。

```
mysql> SHOW CREATE TABLE t;
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                             |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) DEFAULT NULL,
  `b` varchar(10) DEFAULT NULL,
  `c` json DEFAULT NULL,
  `d` blob DEFAULT NULL,
  `e` longblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT @@tidb_analyze_skip_column_types;
+----------------------------------+
| @@tidb_analyze_skip_column_types |
+----------------------------------+
| json,blob,mediumblob,longblob    |
+----------------------------------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t;
Query OK, 0 rows affected, 1 warning (0.05 sec)

mysql> SELECT job_info FROM mysql.analyze_jobs ORDER BY end_time DESC LIMIT 1;
+---------------------------------------------------------------------+
| job_info                                                            |
+---------------------------------------------------------------------+
| analyze table columns a, b with 256 buckets, 500 topn, 1 samplerate |
+---------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> ANALYZE TABLE t COLUMNS a, c;
Query OK, 0 rows affected, 1 warning (0.04 sec)

mysql> SELECT job_info FROM mysql.analyze_jobs ORDER BY end_time DESC LIMIT 1;
+------------------------------------------------------------------+
| job_info                                                         |
+------------------------------------------------------------------+
| analyze table columns a with 256 buckets, 500 topn, 1 samplerate |
+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

### tidb_auto_analyze_end_time

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Time
- 默认值: `23:59 +0000`
- 此变量用于限制允许自动更新统计信息的时间窗口。例如，要仅允许在 UTC 时间的凌晨 1 点到凌晨 3 点之间自动更新统计信息，请设置 `tidb_auto_analyze_start_time='01:00 +0000'` 和 `tidb_auto_analyze_end_time='03:00 +0000'`。

### tidb_auto_analyze_partition_batch_size <span class="version-mark">v6.4.0 新增</span>

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 默认值: `128`。在 v7.6.0 之前，默认值为 `1`。
- 范围: `[1, 1024]`
- 此变量指定 TiDB 在分析分区表时（意味着自动收集分区表的统计信息）[自动分析](/statistics.md#automatic-update)的分区数量。
- 如果此变量的值小于分区数，TiDB 会分批自动分析分区表的所有分区。如果此变量的值大于或等于分区数，TiDB 会同时分析分区表的所有分区。
- 如果分区表的分区数远大于此变量值，并且自动分析花费的时间很长，则可以增加此变量的值以减少时间消耗。

### tidb_auto_analyze_ratio

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Float
- 默认值: `0.5`
- 范围: `(0, 1]`。 v8.0.0 及更早版本的范围是 `[0, 18446744073709551615]`。
- 此变量用于设置 TiDB 在后台线程中自动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 以更新表统计信息的阈值。例如，值为 0.5 表示当表中超过 50% 的行被修改时，将触发自动分析。可以通过指定 `tidb_auto_analyze_start_time` 和 `tidb_auto_analyze_end_time` 将自动分析限制为仅在一天中的某些小时执行。

> **注意:**
>
> 此功能需要将系统变量 `tidb_enable_auto_analyze` 设置为 `ON`。

### tidb_auto_analyze_start_time

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Time
- 默认值: `00:00 +0000`
- 此变量用于限制允许自动更新统计信息的时间窗口。例如，要仅允许在 UTC 时间的凌晨 1 点到凌晨 3 点之间自动更新统计信息，请设置 `tidb_auto_analyze_start_time='01:00 +0000'` 和 `tidb_auto_analyze_end_time='03:00 +0000'`。

### tidb_auto_build_stats_concurrency <span class="version-mark">v6.5.0 新增</span>

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `1`
- 范围: `[1, 256]`
- 此变量用于设置执行自动更新统计信息的并发度。

### tidb_backoff_lock_fast

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `10`
- 范围: `[1, 2147483647]`
- 此变量用于设置读取请求遇到锁时的 `backoff` 时间。

### tidb_backoff_weight

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `2`
- 范围: `[0, 2147483647]`
- 此变量用于增加 TiDB `backoff` 的最大时间权重，即遇到内部网络或其他组件（TiKV、PD）故障时，发送重试请求的最大重试时间。此变量可用于调整最大重试时间，最小值为 1。

    例如，TiDB 从 PD 获取 TSO 的基本超时时间为 15 秒。当 `tidb_backoff_weight = 2` 时，获取 TSO 的最大超时时间为：*基本时间 \* 2 = 30 秒*。

    在网络环境较差的情况下，适当增加此变量的值可以有效缓解因超时而导致的应用端错误报告。如果应用端希望更快地收到错误信息，请尽量减小此变量的值。

### tidb_batch_commit

> **警告:**
>
> **不**建议启用此变量。

- 作用域: SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `OFF`
- 该变量用于控制是否启用已弃用的批量提交功能。启用此变量后，事务可能会被拆分为多个事务，通过对一些语句进行分组并以非原子方式提交，不建议这样做。

### tidb_batch_delete

> **警告：**
>
> 此变量与已弃用的批量 DML 功能相关联，可能会导致数据损坏。因此，不建议为批量 DML 启用此变量。请改用[非事务性 DML](/non-transactional-dml.md)。

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 该变量用于控制是否启用批量删除功能，该功能是已弃用的批量 DML 功能的一部分。启用此变量后，`DELETE` 语句可能会被拆分为多个事务并以非原子方式提交。要使其工作，还需要启用 `tidb_enable_batch_dml` 并为 `tidb_dml_batch_size` 设置一个正值，不建议这样做。

### tidb_batch_insert

> **警告：**
>
> 此变量与已弃用的批量 DML 功能相关联，可能会导致数据损坏。因此，不建议为批量 DML 启用此变量。请改用[非事务性 DML](/non-transactional-dml.md)。

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 该变量用于控制是否启用批量插入功能，该功能是已弃用的批量 DML 功能的一部分。启用此变量后，`INSERT` 语句可能会被拆分为多个事务并以非原子方式提交。要使其工作，还需要启用 `tidb_enable_batch_dml` 并为 `tidb_dml_batch_size` 设置一个正值，不建议这样做。

### tidb_batch_pending_tiflash_count <span class="version-mark">v6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`4000`
- 范围：`[0, 4294967295]`
- 指定使用 `ALTER DATABASE SET TIFLASH REPLICA` 添加 TiFlash 副本时允许的最大不可用表数量。如果不可用表的数量超过此限制，则操作将被停止，或者为剩余表设置 TiFlash 副本的速度将非常慢。

### tidb_broadcast_join_threshold_count <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`10240`
- 范围：`[0, 9223372036854775807]`
- 单位：行
- 如果 join 操作的对象属于子查询，优化器无法估计子查询结果集的大小。在这种情况下，大小由结果集中的行数决定。如果子查询中估计的行数小于此变量的值，则使用 Broadcast Hash Join 算法。否则，使用 Shuffled Hash Join 算法。
- 在启用 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) 后，此变量将不起作用。

### tidb_broadcast_join_threshold_size <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`104857600` (100 MiB)
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 如果表大小小于该变量的值，则使用 Broadcast Hash Join 算法。否则，使用 Shuffled Hash Join 算法。
- 在启用 [`tidb_prefer_broadcast_join_by_exchange_data_size`](/system-variables.md#tidb_prefer_broadcast_join_by_exchange_data_size-new-in-v710) 后，此变量将不起作用。

### tidb_build_stats_concurrency

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`2`。对于 v7.4.0 及更早版本，默认值为 `4`。
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置执行 `ANALYZE` 语句的并发性。
- 当变量设置为较大的值时，会影响其他查询的执行性能。

### tidb_build_sampling_stats_concurrency <span class="version-mark">v7.5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 单位：线程
- 默认值：`2`
- 范围：`[1, 256]`
- 此变量用于设置 `ANALYZE` 过程中的采样并发性。
- 当变量设置为较大的值时，会影响其他查询的执行性能。

### tidb_capture_plan_baselines <span class="version-mark">v4.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于控制是否启用[基线捕获](/sql-plan-management.md#baseline-capturing)功能。此功能依赖于语句摘要，因此在使用基线捕获之前需要启用语句摘要。
- 启用此功能后，会定期遍历语句摘要中的历史 SQL 语句，并自动为至少出现两次的 SQL 语句创建绑定。

### tidb_cdc_write_source <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION
- 是否持久化到集群：否
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 15]`
- 当此变量设置为 0 以外的值时，在此会话中写入的数据被认为是 TiCDC 写入的。此变量只能由 TiCDC 修改。在任何情况下都不要手动修改此变量。

### tidb_check_mb4_value_in_utf8

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于强制 `utf8` 字符集仅存储来自 [基本多文种平面 (BMP)](https://en.wikipedia.org/wiki/Plane_(Unicode)#Basic_Multilingual_Plane) 的值。要存储 BMP 之外的字符，建议使用 `utf8mb4` 字符集。
- 当您从早期版本的 TiDB 升级集群时，可能需要禁用此选项，因为早期版本的 TiDB 中 `utf8` 检查更为宽松。有关详细信息，请参见[升级后常见问题解答](https://docs.pingcap.com/tidb/stable/upgrade-faq)。

### tidb_checksum_table_concurrency

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`4`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置执行 [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) 语句的扫描索引并发性。
- 当变量设置为较大的值时，会影响其他查询的执行性能。

### tidb_committer_concurrency <span class="version-mark">v6.1.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`128`
- 范围：`[1, 10000]`
- 用于处理单事务提交阶段中执行提交相关请求的 Goroutine 数量。
- 如果要提交的事务太大，则提交事务时流控队列的等待时间可能过长。在这种情况下，您可以增加此配置值以加快提交速度。
- 此设置以前是一个 `tidb.toml` 选项 (`performance.committer-concurrency`)，但从 TiDB v6.1.0 开始更改为系统变量。

### tidb_config

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 此变量是只读的。它用于获取当前 TiDB 服务器的配置信息。

### tidb_constraint_check_in_place

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量仅适用于乐观事务。对于悲观事务，请改用 [`tidb_constraint_check_in_place_pessimistic`](#tidb_constraint_check_in_place_pessimistic-new-in-v630)。
- 当此变量设置为 `OFF` 时，对唯一索引中重复值的检查将延迟到事务提交时。这有助于提高性能，但对于某些应用程序来说可能是一种意想不到的行为。有关详细信息，请参见 [约束](/constraints.md#optimistic-transactions)。

    - 当设置 `tidb_constraint_check_in_place` 为 `OFF` 并使用乐观事务时：

        ```sql
        tidb> create table t (i int key);
        tidb> insert into t values (1);
        tidb> begin optimistic;
        tidb> insert into t values (1);
        Query OK, 1 row affected
        tidb> commit; -- 仅在事务提交时检查。
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    - 当设置 `tidb_constraint_check_in_place` 为 `ON` 并使用乐观事务时：

        ```sql
        tidb> set @@tidb_constraint_check_in_place=ON;
        tidb> begin optimistic;
        tidb> insert into t values (1);
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_constraint_check_in_place_pessimistic <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean

<CustomContent platform="tidb">

- 默认值：默认情况下，[`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) 配置项为 `true`，因此此变量的默认值为 `ON`。当 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640) 设置为 `false` 时，此变量的默认值为 `OFF`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 默认值：`ON`

</CustomContent>

- 此变量仅适用于悲观事务。对于乐观事务，请改用 [`tidb_constraint_check_in_place`](#tidb_constraint_check_in_place)。
- 当此变量设置为 `OFF` 时，TiDB 会延迟唯一索引的唯一约束检查（延迟到下次执行需要锁定索引的语句时，或延迟到提交事务时）。这有助于提高性能，但对于某些应用程序来说可能是一种意想不到的行为。有关详细信息，请参见 [约束](/constraints.md#pessimistic-transactions)。
- 禁用此变量可能会导致 TiDB 在悲观事务中返回 `LazyUniquenessCheckFailure` 错误。发生此错误时，TiDB 会回滚当前事务。
- 禁用此变量后，您无法在悲观事务中使用 [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md)。
- 禁用此变量后，提交悲观事务可能会返回 `Write conflict` 或 `Duplicate entry` 错误。发生此类错误时，TiDB 会回滚当前事务。

    - 当设置 `tidb_constraint_check_in_place_pessimistic` 为 `OFF` 并使用悲观事务时：

        {{< copyable "sql" >}}

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=OFF;
        create table t (i int key);
        insert into t values (1);
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        Query OK, 1 row affected
        ```

        ```sql
        tidb> commit; -- 仅在事务提交时检查。
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

    - 当设置 `tidb_constraint_check_in_place_pessimistic` 为 `ON` 并使用悲观事务时：

        ```sql
        set @@tidb_constraint_check_in_place_pessimistic=ON;
        begin pessimistic;
        insert into t values (1);
        ```

        ```
        ERROR 1062 : Duplicate entry '1' for key 't.PRIMARY'
        ```

### tidb_cost_model_version <span class="version-mark">v6.2.0 新增</span>

> **注意：**
>
> - 从 TiDB v6.5.0 开始，新创建的集群默认使用 Cost Model Version 2。如果您从早于 v6.5.0 的 TiDB 版本升级到 v6.5.0 或更高版本，则 `tidb_cost_model_version` 值不会更改。
> - 切换成本模型版本可能会导致查询计划发生变化。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`2`
- 可选值：
    - `1`：启用 Cost Model Version 1，这是 TiDB v6.4.0 及更早版本中默认使用的。
    - `2`：启用 [Cost Model Version 2](/cost-model.md#cost-model-version-2)，该版本在 TiDB v6.5.0 中正式发布，并且在内部测试中比版本 1 更准确。
- 成本模型的版本会影响优化器的计划决策。有关更多详细信息，请参见 [成本模型](/cost-model.md)。

### tidb_current_ts

- 作用域：SESSION
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 此变量是只读的。它用于获取当前事务的时间戳。

### tidb_ddl_disk_quota <span class="version-mark">v6.3.0 新增</span>

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，此变量是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`107374182400` (100 GiB)
- 范围：`[107374182400, 1125899906842624]` ([100 GiB, 1 PiB])
- 单位：字节
- 仅当启用 [`tidb_ddl_enable_fast_reorg`](#tidb_ddl_enable_fast_reorg-new-in-v630) 时，此变量才生效。它设置创建索引时回填期间本地存储的使用限制。

### tidb_ddl_enable_fast_reorg <span class="version-mark">v6.3.0 新增</span>

> **注意：**
>
> - 如果您使用的是 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 集群，要使用此变量提高索引创建速度，请确保您的 TiDB 集群托管在 AWS 上，并且您的 TiDB 节点大小至少为 8 vCPU。
> - 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群，此变量是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用 `ADD INDEX` 和 `CREATE INDEX` 的加速功能，以提高创建索引时回填数据的速度。将此变量值设置为 `ON` 可以提高大数据量表上创建索引的性能。
- 从 v7.1.0 版本开始，索引加速操作支持检查点。即使 TiDB owner 节点由于故障而重启或更改，TiDB 仍然可以从定期自动更新的检查点恢复进度。
- 要验证已完成的 `ADD INDEX` 操作是否已加速，您可以执行 [`ADMIN SHOW DDL JOBS`](/sql-statements/sql-statement-admin-show-ddl.md#admin-show-ddl-jobs) 语句，查看 `JOB_TYPE` 列中是否显示 `ingest`。

<CustomContent platform="tidb">

> **注意：**
>
> * 索引加速需要一个可写的且具有足够可用空间的 [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)。如果 `temp-dir` 不可用，TiDB 将回退到非加速索引构建。建议将 `temp-dir` 放在 SSD 磁盘上。
>
> * 在将 TiDB 升级到 v6.5.0 或更高版本之前，建议您检查 TiDB 的 [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630) 路径是否已正确挂载到 SSD 磁盘。确保运行 TiDB 的操作系统用户具有此目录的读写权限。否则，DDL 操作可能会遇到不可预测的问题。此路径是 TiDB 配置项，在 TiDB 重启后生效。因此，在升级前设置此配置项可以避免再次重启。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> 目前，此功能与[在单个 `ALTER TABLE` 语句中更改多个列或索引](/sql-statements/sql-statement-alter-table.md)不完全兼容。在使用索引加速添加唯一索引时，需要避免在同一语句中更改其他列或索引。

</CustomContent>

### tidb_enable_dist_task <span class="version-mark">v7.1.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否支持 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 此变量用于控制是否启用 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md)。启用该框架后，DDL 和导入等 DXF 任务将由集群中的多个 TiDB 节点分布式执行和完成。
- 从 TiDB v7.1.0 开始，DXF 支持分布式执行分区表的 [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 语句。
- 从 TiDB v7.2.0 开始，DXF 支持分布式执行导入作业的 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句。
- 从 TiDB v8.1.0 开始，默认启用此变量。如果要将启用了 DXF 的集群升级到 v8.1.0 或更高版本，请在升级前禁用 DXF（通过将 `tidb_enable_dist_task` 设置为 `OFF`），以避免升级期间的 `ADD INDEX` 操作导致数据索引不一致。升级后，您可以手动启用 DXF。
- 此变量已从 `tidb_ddl_distribute_reorg` 重命名。

### tidb_cloud_storage_uri <span class="version-mark">v7.4.0 新增</span>

> **注意：**
>
> 目前，[全局排序](/tidb-global-sort.md)过程会消耗 TiDB 节点的大量计算和内存资源。在用户业务应用程序正在运行的情况下在线添加索引等场景中，建议向集群添加新的 TiDB 节点，为这些节点配置 [`tidb_service_scope`](/system-variables.md#tidb_service_scope-new-in-v740) 变量，并连接到这些节点以创建任务。这样，分布式框架会将任务调度到这些节点，从而将工作负载与其他 TiDB 节点隔离，以减少执行 `ADD INDEX` 和 `IMPORT INTO` 等后端任务对用户业务应用程序的影响。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否支持 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`""`
- 此变量用于指定 Amazon S3 云存储 URI 以启用[全局排序](/tidb-global-sort.md)。启用 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 后，您可以通过配置 URI 并将其指向具有访问存储所需权限的适当云存储路径来使用全局排序功能。有关更多详细信息，请参阅 [Amazon S3 URI 格式](/external-storage-uri.md#amazon-s3-uri-format)。
- 以下语句可以使用全局排序功能。
    - [`ADD INDEX`](/sql-statements/sql-statement-add-index.md) 语句。
    - 导入作业的 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句。

### tidb_ddl_error_count_limit

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否支持 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`512`
- 范围：`[0, 9223372036854775807]`
- 此变量用于设置 DDL 操作失败时的重试次数。当重试次数超过参数值时，错误的 DDL 操作将被取消。

### tidb_ddl_flashback_concurrency <span class="version-mark">v6.3.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否支持 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`64`
- 范围：`[1, 256]`
- 此变量控制 [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) 的并发性。

### tidb_ddl_reorg_batch_size

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否支持 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`256`
- 范围：`[32, 10240]`
- 单位：行
- 此变量用于设置 DDL 操作的 `re-organize` 阶段的批量大小。例如，当 TiDB 执行 `ADD INDEX` 操作时，索引数据需要由 `tidb_ddl_reorg_worker_cnt` （数量）个并发 worker 回填。每个 worker 批量回填索引数据。
    - 如果 `tidb_ddl_enable_fast_reorg` 设置为 `OFF`，则 `ADD INDEX` 作为事务执行。如果在 `ADD INDEX` 执行期间目标列中存在许多更新操作（例如 `UPDATE` 和 `REPLACE`），则较大的批量大小表示事务冲突的可能性更大。在这种情况下，建议您将批量大小设置为较小的值。最小值是 32。
    - 如果不存在事务冲突，或者如果 `tidb_ddl_enable_fast_reorg` 设置为 `ON`，则可以将批量大小设置为较大的值。这使得数据回填更快，但也增加了 TiKV 的写入压力。对于合适的批量大小，您还需要参考 `tidb_ddl_reorg_worker_cnt` 的值。有关参考，请参阅 [在线工作负载和 `ADD INDEX` 操作的交互测试](https://docs.pingcap.com/tidb/dev/online-workloads-and-add-index-operations)。

### tidb_ddl_reorg_priority

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION
- 是否支持 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`PRIORITY_LOW`
- 值选项：`PRIORITY_LOW`，`PRIORITY_NORMAL`，`PRIORITY_HIGH`
- 此变量用于设置在 `re-organize` 阶段执行 `ADD INDEX` 操作的优先级。
- 您可以将此变量的值设置为 `PRIORITY_LOW`、`PRIORITY_NORMAL` 或 `PRIORITY_HIGH`。

### tidb_ddl_reorg_worker_cnt

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`4`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置 `re-organize` 阶段 DDL 操作的并发度。

### `tidb_enable_fast_create_table` <span class="version-mark">v8.0.0 新增</span>

> **警告：**
>
> 此变量目前是一项实验性功能，不建议在生产环境中使用。此功能可能会更改或删除，恕不另行通知。如果您发现错误，请在 GitHub 上提出 [issue](https://github.com/pingcap/tidb/issues) 进行反馈。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于控制是否启用 [TiDB 加速建表](/accelerated-table-creation.md)。
- 从 v8.0.0 开始，TiDB 支持使用 `tidb_enable_fast_create_table` 通过 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句加速建表。
- 此变量是从 v7.6.0 中引入的变量 [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_ddl_version-new-in-v760) 重命名的。从 v8.0.0 开始，`tidb_ddl_version` 不再生效。

### tidb_default_string_match_selectivity <span class="version-mark">v6.2.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 默认值：`0.8`
- 范围：`[0, 1]`
- 此变量用于设置在估计行数时，过滤器条件中 `like`、`rlike` 和 `regexp` 函数的默认选择性。此变量还控制是否启用 TopN 来帮助估计这些函数。
- TiDB 尝试使用统计信息来估计过滤器条件中的 `like`。但是，当 `like` 匹配复杂的字符串，或者使用 `rlike` 或 `regexp` 时，TiDB 通常无法完全使用统计信息，而是将默认值 `0.8` 设置为选择性比率，从而导致不准确的估计。
- 此变量用于更改上述行为。如果将该变量设置为 `0` 以外的值，则选择性比率是指定的变量值，而不是 `0.8`。
- 如果将该变量设置为 `0`，TiDB 会尝试使用统计信息中的 TopN 进行评估，以提高准确性，并在估计上述三个函数时考虑统计信息中的 NULL 数量。前提是在 [`tidb_analyze_version`](#tidb_analyze_version-new-in-v510) 设置为 `2` 时收集统计信息。这种评估可能会稍微影响性能。
- 如果将该变量设置为 `0.8` 以外的值，TiDB 会相应地调整对 `not like`、`not rlike` 和 `not regexp` 的估计。

### tidb_disable_txn_auto_retry

> **警告：**
>
> 从 v8.0.0 开始，此变量已弃用，TiDB 不再支持乐观事务的自动重试。作为替代方案，当遇到乐观事务冲突时，您可以在应用程序中捕获错误并重试事务，或者改用 [悲观事务模式](/pessimistic-transaction.md)。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于设置是否禁用显式乐观事务的自动重试。默认值 `ON` 表示事务不会在 TiDB 中自动重试，并且 `COMMIT` 语句可能会返回需要在应用程序层处理的错误。

    将值设置为 `OFF` 表示 TiDB 将自动重试事务，从而减少 `COMMIT` 语句中的错误。更改此设置时要小心，因为它可能会导致更新丢失。

    此变量不影响自动提交的隐式事务和 TiDB 中内部执行的事务。这些事务的最大重试次数由 `tidb_retry_limit` 的值决定。

    有关更多详细信息，请参见 [重试限制](/optimistic-transaction.md#limits-of-retry)。

    <CustomContent platform="tidb">

    此变量仅适用于乐观事务，不适用于悲观事务。悲观事务的重试次数由 [`max_retry_count`](/tidb-configuration-file.md#max-retry-count) 控制。

    </CustomContent>

    <CustomContent platform="tidb-cloud">

    此变量仅适用于乐观事务，不适用于悲观事务。悲观事务的重试次数为 256。

    </CustomContent>

### tidb_distsql_scan_concurrency

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`15`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置 `scan` 操作的并发度。
- 在 OLAP 场景中使用较大的值，在 OLTP 场景中使用较小的值。
- 对于 OLAP 场景，最大值不应超过所有 TiKV 节点的 CPU 核心数。
- 如果表有很多分区，您可以适当减小变量值（由要扫描的数据大小和扫描频率决定），以避免 TiKV 内存不足 (OOM)。
- 对于只有 `LIMIT` 子句的简单查询，如果 `LIMIT` 值小于 100000，则下推到 TiKV 的扫描操作会将此变量的值视为 `1`，以提高执行效率。
- 对于 `SELECT MAX/MIN(col) FROM ...` 查询，如果 `col` 列具有以 `MAX(col)` 或 `MIN(col)` 函数所需的相同顺序排序的索引，TiDB 会将查询重写为 `SELECT col FROM ... LIMIT 1` 进行处理，并且此变量的值也将被处理为 `1`。例如，对于 `SELECT MIN(col) FROM ...`，如果 `col` 列具有升序索引，TiDB 可以通过将查询重写为 `SELECT col FROM ... LIMIT 1` 并直接读取索引的第一行来快速获得 `MIN(col)` 值。

### tidb_dml_batch_size

> **警告：**
>
> 此变量与已弃用的 batch-dml 功能相关联，该功能可能会导致数据损坏。因此，不建议为 batch-dml 启用此变量。而是使用 [非事务性 DML](/non-transactional-dml.md)。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：行
- 当此值大于 `0` 时，TiDB 会将 `INSERT` 等语句批量提交到较小的事务中。这减少了内存使用量，并有助于确保批量修改不会达到 `txn-total-size-limit`。
- 只有值 `0` 提供 ACID 兼容性。将此值设置为任何其他值将破坏 TiDB 的原子性和隔离性保证。
- 要使此变量生效，您还需要启用 `tidb_enable_batch_dml` 和 `tidb_batch_insert` 和 `tidb_batch_delete` 中的至少一个。

> **注意：**
>
> 从 v7.0.0 开始，`tidb_dml_batch_size` 不再对 [`LOAD DATA` 语句](/sql-statements/sql-statement-load-data.md) 生效。

### tidb_dml_type <span class="version-mark">v8.0.0 新增</span>

> **警告：**
>
> 批量 DML 执行模式 (`tidb_dml_type = "bulk"`) 是一项实验性功能。不建议在生产环境中使用。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以报告 [issue](https://github.com/pingcap/tidb/issues)。在当前版本中，当 TiDB 使用批量 DML 模式执行大型事务时，可能会影响 TiCDC、TiFlash 和 TiKV 的 resolved-ts 模块的内存使用和执行效率，并可能导致 OOM 问题。此外，BR 可能会被阻塞，并且在遇到锁时无法处理。因此，不建议在启用这些组件或功能时使用此模式。

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：String
- 默认值：`"standard"`
- 可选值：`"standard"`, `"bulk"`
- 此变量控制 DML 语句的执行模式。
    - `"standard"` 表示标准 DML 执行模式，其中 TiDB 事务在提交之前缓存在内存中。此模式适用于具有潜在冲突的高并发事务场景，是默认推荐的执行模式。
    - `"bulk"` 表示批量 DML 执行模式，适用于写入大量数据导致 TiDB 内存使用过多的场景。
        - 在 TiDB 事务执行期间，数据不会完全缓存在 TiDB 内存中，而是持续写入 TiKV 以减少内存使用并平滑写入压力。
        - 只有 `INSERT`、`UPDATE`、`REPLACE` 和 `DELETE` 语句受 `"bulk"` 模式影响。由于 `"bulk"` 模式下的流水线式执行，当更新导致冲突时，使用 `INSERT IGNORE ... ON DUPLICATE UPDATE ...` 可能会导致 `Duplicate entry` 错误。 相比之下，在 `"standard"` 模式下，由于设置了 `IGNORE` 关键字，此错误将被忽略，不会返回给用户。
        - `"bulk"` 模式仅适用于**写入大量数据且没有冲突**的场景。此模式对于处理写入冲突效率不高，因为写入-写入冲突可能导致大型事务失败并回滚。
        - `"bulk"` 模式仅对启用自动提交的语句生效，并且需要将 [`pessimistic-auto-commit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#pessimistic-auto-commit-new-in-v600) 配置项设置为 `false`。
        - 使用 `"bulk"` 模式执行语句时，请确保在执行过程中 [metadata lock](/metadata-lock.md) 保持启用状态。
        - `"bulk"` 模式不能用于 [临时表](/temporary-tables.md) 和 [缓存表](/cached-tables.md)。
        - 当外键约束检查启用 (`foreign_key_checks = ON`) 时，`"bulk"` 模式不能用于包含外键的表和被外键引用的表。
        - 在环境不支持或与 `"bulk"` 模式不兼容的情况下，TiDB 会回退到 `"standard"` 模式并返回警告消息。要验证是否使用了 `"bulk"` 模式，可以使用 [`tidb_last_txn_info`](#tidb_last_txn_info-new-in-v409) 检查 `pipelined` 字段。`true` 值表示使用了 `"bulk"` 模式。
        - 在 `"bulk"` 模式下执行大型事务时，事务持续时间可能会很长。对于此模式下的事务，事务锁的最大 TTL 是 [`max-txn-ttl`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#max-txn-ttl) 和 24 小时之间的较大值。此外，如果事务执行时间超过了 [`tidb_gc_max_wait_time`](#tidb_gc_max_wait_time-new-in-v610) 设置的值，GC 可能会强制回滚事务，导致事务失败。
        - 当 TiDB 在 `"bulk"` 模式下执行事务时，事务大小不受 TiDB 配置项 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 的限制。
        - 此模式由 Pipelined DML 功能实现。有关详细设计和 GitHub issue，请参阅 [Pipelined DML](https://github.com/pingcap/tidb/blob/release-8.1/docs/design/2024-01-09-pipelined-DML.md) 和 [#50215](https://github.com/pingcap/tidb/issues/50215)。

### tidb_enable_1pc <span class="version-mark">New in v5.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于指定是否为仅影响一个 Region 的事务启用单阶段提交功能。与常用的两阶段提交相比，单阶段提交可以大大减少事务提交的延迟并提高吞吐量。

> **注意：**
>
> - 默认值 `ON` 仅适用于新集群。如果您的集群是从早期版本的 TiDB 升级而来，则将使用值 `OFF`。
> - 如果您已启用 TiDB Binlog，则启用此变量无法提高性能。为了提高性能，建议使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 代替。
> - 启用此参数仅意味着单阶段提交成为事务提交的可选模式。实际上，最合适的事务提交模式由 TiDB 决定。

### tidb_enable_analyze_snapshot <span class="version-mark">New in v6.2.0</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制执行 `ANALYZE` 时是读取历史数据还是最新数据。如果此变量设置为 `ON`，则 `ANALYZE` 读取 `ANALYZE` 时可用的历史数据。如果此变量设置为 `OFF`，则 `ANALYZE` 读取最新数据。
- 在 v5.2 之前，`ANALYZE` 读取最新数据。从 v5.2 到 v6.1，`ANALYZE` 读取 `ANALYZE` 时可用的历史数据。

> **警告：**
>
> 如果 `ANALYZE` 读取 `ANALYZE` 时可用的历史数据，则 `AUTO ANALYZE` 的长时间运行可能会导致 `GC life time is shorter than transaction duration` 错误，因为历史数据已被垃圾回收。

### tidb_enable_async_commit <span class="version-mark">New in v5.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用异步提交功能，以便在两阶段事务提交的第二阶段在后台异步执行。启用此功能可以减少事务提交的延迟。

> **注意：**
>
> - 默认值 `ON` 仅适用于新集群。如果您的集群是从早期版本的 TiDB 升级而来，则将使用值 `OFF`。
> - 如果您已启用 TiDB Binlog，则启用此变量无法提高性能。为了提高性能，建议使用 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 代替。
> - 启用此参数仅意味着异步提交成为事务提交的可选模式。实际上，最合适的事务提交模式由 TiDB 决定。

### tidb_enable_auto_analyze <span class="version-mark">New in v6.1.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 范围：全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 决定 TiDB 是否自动更新表统计信息作为后台操作。
- 此设置以前是 `tidb.toml` 选项 (`performance.run-auto-analyze`)，但从 TiDB v6.1.0 开始更改为系统变量。

### tidb_enable_auto_analyze_priority_queue <span class="version-mark">v8.0.0 新增</span>

- 范围：全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 此变量用于控制是否启用优先级队列来调度自动收集统计信息的任务。启用此变量后，TiDB 会优先收集对收集更有价值的表的统计信息，例如新创建的索引和具有分区更改的分区表。此外，TiDB 会优先处理健康评分较低的表，将其放在队列的前面。

### tidb_enable_auto_increment_in_generated

- 范围：会话 | 全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`OFF`
- 此变量用于确定在创建生成列或表达式索引时是否包含 `AUTO_INCREMENT` 列。

### tidb_enable_batch_dml

> **警告：**
>
> 此变量与已弃用的 batch-dml 功能相关联，可能会导致数据损坏。因此，不建议为 batch-dml 启用此变量。请改用[非事务性 DML](/non-transactional-dml.md)。

- 范围：全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`OFF`
- 此变量控制是否启用已弃用的 batch-dml 功能。启用后，某些语句可能会拆分为多个事务，这是非原子的，应谨慎使用。使用 batch-dml 时，必须确保您操作的数据上没有并发操作。要使其工作，您还必须为 `tidb_batch_dml_size` 指定一个正值，并启用 `tidb_batch_insert` 和 `tidb_batch_delete` 中的至少一个。

### tidb_enable_cascades_planner

> **警告：**
>
> 目前，cascades planner 是一项实验性功能。不建议在生产环境中使用它。

- 范围：会话 | 全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔型
- 默认值：`OFF`
- 此变量用于控制是否启用 cascades planner。

### tidb_enable_check_constraint <span class="version-mark">v7.2.0 新增</span>

- 范围：全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`OFF`
- 此变量用于控制是否启用 [`CHECK` 约束](/constraints.md#check)功能。

### tidb_enable_chunk_rpc <span class="version-mark">v4.0 新增</span>

- 范围：会话
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 此变量用于控制是否在 Coprocessor 中启用 `Chunk` 数据编码格式。

### tidb_enable_clustered_index <span class="version-mark">v5.0 新增</span>

- 范围：会话 | 全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`ON`
- 可选值：`OFF`、`ON`、`INT_ONLY`
- 此变量用于控制是否默认将主键创建为[聚簇索引](/clustered-indexes.md)。“默认”是指语句未显式指定关键字 `CLUSTERED`/`NONCLUSTERED`。支持的值为 `OFF`、`ON` 和 `INT_ONLY`：
    - `OFF` 表示默认将主键创建为非聚簇索引。
    - `ON` 表示默认将主键创建为聚簇索引。
    - `INT_ONLY` 表示该行为由配置项 `alter-primary-key` 控制。如果 `alter-primary-key` 设置为 `true`，则默认将所有主键创建为非聚簇索引。如果设置为 `false`，则仅将由整数列组成的主键创建为聚簇索引。

### tidb_enable_ddl <span class="version-mark">v6.3.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 范围：全局
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 可选值：`OFF`、`ON`
- 此变量控制相应的 TiDB 实例是否可以成为 DDL 所有者。如果当前 TiDB 集群中只有一个 TiDB 实例，则无法阻止其成为 DDL 所有者，这意味着您无法将其设置为 `OFF`。

### tidb_enable_collect_execution_info

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 范围：全局
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 此变量控制是否在慢查询日志中记录每个算子的执行信息，以及是否记录[索引的使用统计信息](/information-schema/information-schema-tidb-index-usage.md)。

### tidb_enable_column_tracking <span class="version-mark">v5.4.0 新增</span>

> **警告：**
>
> 目前，收集 `PREDICATE COLUMNS` 的统计信息是一项实验性功能。不建议在生产环境中使用它。

- 范围：全局
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`OFF`
- 此变量控制是否启用 TiDB 收集 `PREDICATE COLUMNS`。启用收集后，如果禁用它，则会清除先前收集的 `PREDICATE COLUMNS` 的信息。有关详细信息，请参见[收集某些列的统计信息](/statistics.md#collect-statistics-on-some-columns)。

### tidb_enable_enhanced_security

- 范围：无
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型

<CustomContent platform="tidb">

- 默认值：`OFF`
- 此变量指示您连接的 TiDB 服务器是否启用了安全增强模式 (SEM)。要更改其值，您需要修改 TiDB 服务器配置文件中 `enable-sem` 的值并重新启动 TiDB 服务器。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 默认值：`ON`
- 此变量是只读的。对于 TiDB Cloud，默认启用安全增强模式 (SEM)。

</CustomContent>

- SEM 的灵感来自 [Security-Enhanced Linux](https://en.wikipedia.org/wiki/Security-Enhanced_Linux) 等系统的设计。它减少了具有 MySQL `SUPER` 权限的用户的能力，而是需要授予 `RESTRICTED` 细粒度权限作为替代。这些细粒度权限包括：
    - `RESTRICTED_TABLES_ADMIN`：能够将数据写入 `mysql` schema 中的系统表，并查看 `information_schema` 表上的敏感列。
    - `RESTRICTED_STATUS_ADMIN`：能够查看命令 `SHOW STATUS` 中的敏感变量。
    - `RESTRICTED_VARIABLES_ADMIN`：能够查看和设置 `SHOW [GLOBAL] VARIABLES` 和 `SET` 中的敏感变量。
- `RESTRICTED_USER_ADMIN`: 阻止其他用户更改或删除用户帐户的能力。

### tidb_enable_exchange_partition

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用 [`exchange partitions with tables`](/partitioned-table.md#partition-management) 功能。默认值为 `ON`，即默认启用 `exchange partitions with tables`。
- 此变量自 v6.3.0 起已弃用。它的值将固定为默认值 `ON`，即默认启用 `exchange partitions with tables`。

### tidb_enable_extended_stats

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量指示 TiDB 是否可以收集扩展统计信息来指导优化器。有关更多信息，请参见[扩展统计信息简介](/extended-statistics.md)。

### tidb_enable_external_ts_read <span class="version-mark">v6.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 如果此变量设置为 `ON`，TiDB 会使用 [`tidb_external_ts`](#tidb_external_ts-new-in-v640) 指定的时间戳读取数据。

### tidb_external_ts <span class="version-mark">v6.4.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 如果 [`tidb_enable_external_ts_read`](#tidb_enable_external_ts_read-new-in-v640) 设置为 `ON`，TiDB 会使用此变量指定的时间戳读取数据。

### tidb_enable_fast_analyze

> **警告：**
>
> 从 v7.5.0 开始，此变量已弃用。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于设置是否启用统计信息 `Fast Analyze` 功能。
- 如果启用了统计信息 `Fast Analyze` 功能，TiDB 会随机抽样大约 10,000 行数据作为统计信息。当数据分布不均匀或数据量较小时，统计信息的准确性较低。这可能会导致非最佳执行计划，例如，选择错误的索引。如果常规 `Analyze` 语句的执行时间可以接受，建议禁用 `Fast Analyze` 功能。

### tidb_enable_fast_table_check <span class="version-mark">v7.2.0 新增</span>

> **注意：**
>
> 此变量不适用于[多值索引](/sql-statements/sql-statement-create-index.md#multi-valued-indexes)和前缀索引。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制是否使用基于校验和的方法来快速检查表中数据和索引的完整性。默认值 `ON` 表示默认启用此功能。
- 启用此变量后，TiDB 可以更快地执行 [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) 语句。

### tidb_enable_foreign_key <span class="version-mark">v6.3.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：v6.6.0 之前，默认值为 `OFF`。从 v6.6.0 开始，默认值为 `ON`。
- 此变量控制是否启用 `FOREIGN KEY` 功能。

### tidb_enable_gc_aware_memory_track

> **警告：**
>
> 此变量是 TiDB 中用于调试的内部变量。它可能会在未来的版本中被删除。**请勿**设置此变量。

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否启用 GC-Aware 内存跟踪。

### tidb_enable_global_index <span class="version-mark">v7.6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 可选值：`OFF`，`ON`
- 此变量控制是否支持为分区表创建 `Global indexes`。`Global index` 目前处于开发阶段。**不建议修改此系统变量的值**。

### tidb_enable_non_prepared_plan_cache

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否启用 [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) 功能。
- 启用此功能可能会产生额外的内存和 CPU 开销，并且可能不适用于所有情况。请根据您的实际情况确定是否启用此功能。

### tidb_enable_non_prepared_plan_cache_for_dml <span class="version-mark">v7.1.0 新增</span>

> **警告：**
>
> 用于 DML 语句的非预备执行计划缓存是一项实验性功能。不建议在生产环境中使用它。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`。
- 此变量控制是否为 DML 语句启用 [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) 功能。

### tidb_enable_gogc_tuner <span class="version-mark">v6.4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用 GOGC Tuner。

### tidb_enable_historical_stats

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用历史统计信息。默认值从 `OFF` 更改为 `ON`，这意味着默认启用历史统计信息。

### tidb_enable_historical_stats_for_capture

> **警告：**
>
> 此变量控制的功能在当前 TiDB 版本中尚未完全实现。请勿更改默认值。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制 `PLAN REPLAYER CAPTURE` 捕获的信息是否默认包含历史统计信息。默认值 `OFF` 表示默认不包含历史统计信息。

### tidb_enable_index_merge <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> - 将 TiDB 集群从低于 v4.0.0 的版本升级到 v5.4.0 或更高版本后，默认情况下禁用此变量，以防止由于执行计划的更改而导致性能下降。
>
> - 将 TiDB 集群从 v4.0.0 或更高版本升级到 v5.4.0 或更高版本后，此变量保持升级前的设置。
>
> - 自 v5.4.0 起，对于新部署的 TiDB 集群，默认启用此变量。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制是否启用索引合并功能。

### tidb_enable_index_merge_join

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 指定是否启用 `IndexMergeJoin` 算子。
- 此变量仅用于 TiDB 的内部操作。**不建议**调整它。否则，可能会影响数据的正确性。

### tidb_enable_legacy_instance_scope <span class="version-mark">v6.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量允许使用 `SET SESSION` 以及 `SET GLOBAL` 语法来设置 `INSTANCE` 作用域的变量。
- 默认启用此选项是为了与早期版本的 TiDB 兼容。

### tidb_enable_list_partition <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于设置是否启用 `LIST (COLUMNS) TABLE PARTITION` 功能。

### tidb_enable_local_txn

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于尚未发布的功能。**请勿更改变量值**。

### tidb_enable_metadata_lock <span class="version-mark">v6.3.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于设置是否启用 [Metadata lock](/metadata-lock.md) 功能。请注意，在设置此变量时，需要确保集群中没有正在运行的 DDL 语句。否则，数据可能不正确或不一致。

### tidb_enable_mutation_checker <span class="version-mark">v6.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制是否启用 TiDB mutation checker，该工具用于检查 DML 语句执行期间数据和索引之间的一致性。如果 checker 为某个语句返回错误，TiDB 会回滚该语句的执行。启用此变量会导致 CPU 使用率略有增加。有关更多信息，请参见 [解决数据和索引不一致问题](/troubleshoot-data-inconsistency-errors.md)。
- 对于 v6.0.0 或更高版本的新集群，默认值为 `ON`。对于从早于 v6.0.0 的版本升级的现有集群，默认值为 `OFF`。

### tidb_enable_new_cost_interface <span class="version-mark">v6.2.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- TiDB v6.2.0 重构了之前成本模型的实现。此变量控制是否启用重构后的成本模型实现。
- 默认启用此变量，因为重构后的成本模型使用与之前相同的成本公式，这不会改变计划决策。
- 如果您的集群是从 v6.1 升级到 v6.2，则此变量保持 `OFF`，建议手动启用它。如果您的集群是从早于 v6.1 的版本升级的，则默认情况下此变量设置为 `ON`。

### tidb_enable_new_only_full_group_by_check <span class="version-mark">v6.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制 TiDB 执行 `ONLY_FULL_GROUP_BY` 检查时的行为。有关 `ONLY_FULL_GROUP_BY` 的详细信息，请参阅 [MySQL 文档](https://dev.mysql.com/doc/refman/8.0/en/sql-mode.html#sqlmode_only_full_group_by)。在 v6.1.0 中，TiDB 更严格和正确地处理此检查。
- 为了避免版本升级可能导致的兼容性问题，此变量在 v6.1.0 中的默认值为 `OFF`。

### tidb_enable_noop_functions <span class="version-mark">v4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`OFF`
- 可能的值：`OFF`、`ON`、`WARN`
- 默认情况下，当您尝试使用尚未实现的功能的语法时，TiDB 会返回错误。当变量值设置为 `ON` 时，TiDB 会静默地忽略此类不可用功能的情况，如果您无法更改 SQL 代码，这将很有帮助。
- 启用 `noop` 函数控制以下行为：
    * `LOCK IN SHARE MODE` 语法
    * `SQL_CALC_FOUND_ROWS` 语法
    * `START TRANSACTION READ ONLY` 和 `SET TRANSACTION READ ONLY` 语法
    * `tx_read_only`、`transaction_read_only`、`offline_mode`、`super_read_only`、`read_only` 和 `sql_auto_is_null` 系统变量
    * `GROUP BY <expr> ASC|DESC` 语法

> **警告：**
>
> 只有默认值 `OFF` 才能被认为是安全的。设置 `tidb_enable_noop_functions=1` 可能会导致应用程序中出现意外行为，因为它允许 TiDB 忽略某些语法而不提供错误。例如，允许使用语法 `START TRANSACTION READ ONLY`，但事务仍处于读写模式。

### tidb_enable_noop_variables <span class="version-mark">v6.2.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 如果您将变量值设置为 `OFF`，TiDB 的行为如下：
    * 当您使用 `SET` 设置 `noop` 变量时，TiDB 返回 `“setting *variable_name* has no effect in TiDB”` 警告。
    * `SHOW [SESSION | GLOBAL] VARIABLES` 的结果不包括 `noop` 变量。
    * 当您使用 `SELECT` 读取 `noop` 变量时，TiDB 返回 `“variable *variable_name* has no effect in TiDB”` 警告。
- 要检查 TiDB 实例是否已设置和读取 `noop` 变量，可以使用 `SELECT * FROM INFORMATION_SCHEMA.CLIENT_ERRORS_SUMMARY_GLOBAL;` 语句。

### tidb_enable_null_aware_anti_join <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：在 v7.0.0 之前，默认值为 `OFF`。从 v7.0.0 开始，默认值为 `ON`。
- 类型：Boolean
- 此变量控制当由特殊集合运算符 `NOT IN` 和 `!= ALL` 引导的子查询生成 ANTI JOIN 时，TiDB 是否应用 Null Aware Hash Join。
- 当您从早期版本升级到 v7.0.0 或更高版本的集群时，该功能会自动启用，这意味着此变量设置为 `ON`。

### tidb_enable_outer_join_reorder <span class="version-mark">v6.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 从 v6.1.0 版本开始，TiDB 的 [Join Reorder](/join-reorder.md) 算法支持 Outer Join。此变量控制 TiDB 是否启用 Join Reorder 对 Outer Join 的支持。
- 如果您的集群是从早期版本的 TiDB 升级而来，请注意以下事项：

    - 如果升级前的 TiDB 版本早于 v6.1.0，则升级后此变量的默认值为 `ON`。
    - 如果升级前的 TiDB 版本为 v6.1.0 或更高版本，则升级后此变量的默认值与升级前的值保持一致。

### `tidb_enable_inl_join_inner_multi_pattern` <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制当内表上有 `Selection` 或 `Projection` 算子时，是否支持 Index Join。默认值 `OFF` 表示在这种情况下不支持 Index Join。

### tidb_enable_ordered_result_mode

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 指定是否自动对最终输出结果进行排序。
- 例如，启用此变量后，TiDB 将 `SELECT a, MAX(b) FROM t GROUP BY a` 处理为 `SELECT a, MAX(b) FROM t GROUP BY a ORDER BY a, MAX(b)`。

### tidb_enable_paging <span class="version-mark">v5.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否使用分页的方法发送 Coprocessor 请求。对于 [v5.4.0, v6.2.0) 中的 TiDB 版本，此变量仅对 `IndexLookup` 算子生效；对于 v6.2.0 及更高版本，此变量全局生效。从 v6.4.0 开始，此变量的默认值从 `OFF` 更改为 `ON`。
- 用户场景：

    - 在所有 OLTP 场景中，建议使用分页方法。
    - 对于使用 `IndexLookup` 和 `Limit` 的读取查询，并且 `Limit` 无法下推到 `IndexScan`，读取查询可能存在高延迟，并且 TiKV `Unified read pool CPU` 的使用率很高。在这种情况下，由于 `Limit` 算子只需要少量数据，如果将 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540) 设置为 `ON`，TiDB 处理的数据量会减少，从而降低查询延迟和资源消耗。
    - 在使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 进行数据导出和全表扫描等场景中，启用分页可以有效降低 TiDB 进程的内存消耗。

> **注意：**
>
> 在使用 TiKV 作为存储引擎而不是 TiFlash 的 OLAP 场景中，启用分页在某些情况下可能会导致性能下降。如果发生性能下降，请考虑使用此变量禁用分页，或者使用 [`tidb_min_paging_size`](/system-variables.md#tidb_min_paging_size-new-in-v620) 和 [`tidb_max_paging_size`](/system-variables.md#tidb_max_paging_size-new-in-v630) 变量来调整分页大小的行数范围。

### tidb_enable_parallel_apply <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否为 `Apply` 算子启用并发。并发数由 `tidb_executor_concurrency` 变量控制。`Apply` 算子处理相关子查询，默认情况下没有并发，因此执行速度很慢。将此变量值设置为 `1` 可以增加并发并加快执行速度。目前，默认情况下禁用 `Apply` 的并发。

### tidb_enable_parallel_hashagg_spill <span class="version-mark">v8.0.0 新增</span>

> **警告：**
>
> 目前，此变量控制的功能是实验性的。不建议在生产环境中使用。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：v8.1.0 为 `ON`；v8.1.1 及之后的 8.1 patch 版本为 `OFF`
- 此变量控制 TiDB 是否支持并行 HashAgg 算法的磁盘溢出。当它为 `ON` 时，可以为并行 HashAgg 算法触发磁盘溢出。此变量将在未来版本中此功能普遍可用后被弃用。

### tidb_enable_pipelined_window_function

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量指定是否对 [窗口函数](/functions-and-operators/window-functions.md) 使用流水线执行算法。

### tidb_enable_plan_cache_for_param_limit <span class="version-mark">v6.6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制 Prepared Plan Cache 是否缓存以变量作为 `LIMIT` 参数 (`LIMIT ?`) 的执行计划。默认值为 `ON`，表示 Prepared Plan Cache 支持缓存此类执行计划。请注意，Prepared Plan Cache 不支持缓存变量大于 10000 的执行计划。

### tidb_enable_plan_cache_for_subquery <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制 Prepared Plan Cache 是否缓存包含子查询的查询。

### tidb_enable_plan_replayer_capture

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用 `PLAN REPLAYER CAPTURE` 功能。默认值 `ON` 表示启用 `PLAN REPLAYER CAPTURE` 功能。

</CustomContent>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否启用 [`PLAN REPLAYER CAPTURE` 功能](/sql-plan-replayer.md#use-plan-replayer-capture-to-capture-target-plans)。默认值 `ON` 表示启用 `PLAN REPLAYER CAPTURE` 功能。

</CustomContent>

### tidb_enable_plan_replayer_continuous_capture <span class="version-mark">v7.0.0 新增</span>

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否启用 `PLAN REPLAYER CONTINUOUS CAPTURE` 功能。默认值 `OFF` 表示禁用该功能。

</CustomContent>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否启用 [`PLAN REPLAYER CONTINUOUS CAPTURE` 功能](/sql-plan-replayer.md#use-plan-replayer-continuous-capture)。默认值 `OFF` 表示禁用该功能。

</CustomContent>

### tidb_enable_prepared_plan_cache <span class="version-mark">v6.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔型
- 默认值：`ON`
- 决定是否启用 [Prepared Plan Cache](/sql-prepared-plan-cache.md)。启用后，`Prepare` 和 `Execute` 的执行计划会被缓存，以便后续执行跳过优化执行计划的步骤，从而提高性能。
- 此设置之前是 `tidb.toml` 中的一个选项 (`prepared-plan-cache.enabled`)，但从 TiDB v6.1.0 开始更改为系统变量。

### tidb_enable_prepared_plan_cache_memory_monitor <span class="version-mark">v6.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 此变量控制是否统计 Prepared Plan Cache 中缓存的执行计划所消耗的内存。有关详细信息，请参阅 [Prepared Plan Cache 的内存管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)。

### tidb_enable_pseudo_for_outdated_stats <span class="version-mark">v5.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔型
- 默认值：`OFF`
- 此变量控制优化器在表统计信息过期时使用该统计信息的行为。

<CustomContent platform="tidb">

- 优化器通过以下方式确定表的统计信息是否过期：自上次对表执行 `ANALYZE` 以获取统计信息以来，如果 80% 的表行被修改（修改的行数除以总行数），则优化器确定此表的统计信息已过期。您可以使用 [`pseudo-estimate-ratio`](/tidb-configuration-file.md#pseudo-estimate-ratio) 配置更改此比率。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 优化器通过以下方式确定表的统计信息是否过期：自上次对表执行 `ANALYZE` 以获取统计信息以来，如果 80% 的表行被修改（修改的行数除以总行数），则优化器确定此表的统计信息已过期。

</CustomContent>

- 默认情况下（变量值为 `OFF`），当表的统计信息过期时，优化器仍会继续使用该表的统计信息。如果将变量值设置为 `ON`，则优化器会确定该表的统计信息不再可靠，除非总行数。然后，优化器使用伪统计信息。
- 如果表上的数据经常被修改而没有及时对该表执行 `ANALYZE`，为了保持执行计划的稳定，建议将变量值设置为 `OFF`。

### tidb_enable_rate_limit_action

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`OFF`
- 此变量控制是否为读取数据的算子启用动态内存控制功能。默认情况下，此算子启用 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 允许的最大线程数来读取数据。当单个 SQL 语句的内存使用量每次超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，读取数据的算子会停止一个线程。

<CustomContent platform="tidb">

- 当读取数据的算子只剩下一个线程，并且单个 SQL 语句的内存使用量持续超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，此 SQL 语句会触发其他内存控制行为，例如 [将数据溢出到磁盘](/system-variables.md#tidb_enable_tmp_storage_on_oom)。
- 当 SQL 语句仅读取数据时，此变量可以有效地控制内存使用量。如果需要计算操作（例如连接或聚合操作），则内存使用量可能不受 `tidb_mem_quota_query` 的控制，这会增加 OOM 的风险。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 当读取数据的算子只剩下一个线程，并且单个 SQL 语句的内存使用量继续超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 时，此 SQL 语句会触发其他内存控制行为，例如将数据溢出到磁盘。

</CustomContent>

### tidb_enable_resource_control <span class="version-mark">v6.6.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 类型：布尔型
- 此变量是 [资源控制功能](/tidb-resource-control.md) 的开关。当此变量设置为 `ON` 时，TiDB 集群可以基于资源组隔离应用程序资源。

### tidb_enable_reuse_chunk <span class="version-mark">v6.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 可选值：`OFF`，`ON`
- 此变量控制 TiDB 是否启用 chunk 对象缓存。如果值为 `ON`，TiDB 倾向于使用缓存的 chunk 对象，只有当请求的对象不在缓存中时才从系统请求。如果值为 `OFF`，TiDB 直接从系统请求 chunk 对象。

### tidb_enable_slow_log

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 此变量用于控制是否启用慢查询日志功能。

### tidb_enable_tmp_storage_on_oom

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 可选值：`OFF`，`ON`
- 控制当单个 SQL 语句超过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 指定的内存配额时，是否为某些算子启用临时存储。
- 在 v6.3.0 之前，您可以使用 TiDB 配置项 `oom-use-tmp-storage` 启用或禁用此功能。将集群升级到 v6.3.0 或更高版本后，TiDB 集群将使用 `oom-use-tmp-storage` 的值自动初始化此变量。之后，更改 `oom-use-tmp-storage` 的值将**不再**生效。

### tidb_enable_stmt_summary <span class="version-mark">v3.0.4 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 此变量用于控制是否启用语句摘要功能。如果启用，SQL 执行信息（如时间消耗）将被记录到 `information_schema.STATEMENTS_SUMMARY` 系统表中，以识别和排除 SQL 性能问题。

### tidb_enable_strict_double_type_check <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔型
- 默认值：`ON`
- 此变量用于控制是否可以使用 `DOUBLE` 类型的无效定义创建表。此设置旨在提供从早期 TiDB 版本升级的途径，因为早期版本在验证类型方面不太严格。
- 默认值 `ON` 与 MySQL 兼容。

例如，类型 `DOUBLE(10)` 现在被认为是无效的，因为浮点类型的精度无法保证。将 `tidb_enable_strict_double_type_check` 更改为 `OFF` 后，表将被创建：

```sql
mysql> CREATE TABLE t1 (id int, c double(10));
ERROR 1149 (42000): You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use

mysql> SET tidb_enable_strict_double_type_check = 'OFF';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE TABLE t1 (id int, c double(10));
Query OK, 0 rows affected (0.09 sec)
```

> **注意：**
>
> 此设置仅适用于 `DOUBLE` 类型，因为 MySQL 允许 `FLOAT` 类型的精度。从 MySQL 8.0.17 开始，此行为已被弃用，不建议为 `FLOAT` 或 `DOUBLE` 类型指定精度。

### tidb_enable_table_partition

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`ON`
- 可选值：`OFF`，`ON`，`AUTO`
- 此变量用于设置是否启用 `TABLE PARTITION` 功能：
    - `ON` 表示启用 Range 分区、Hash 分区和单列 Range 列分区。
    - `AUTO` 的功能与 `ON` 相同。
    - `OFF` 表示禁用 `TABLE PARTITION` 功能。在这种情况下，可以执行创建分区表的语法，但创建的表不是分区表。

### tidb_enable_telemetry <span class="version-mark">v4.0.2 新增，v8.1.0 弃用</span>

> **警告：**
>
> 从 v8.1.0 开始，TiDB 中的遥测功能已移除，此变量不再起作用。保留此变量仅是为了与早期版本兼容。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`

<CustomContent platform="tidb">

- 在 v8.1.0 之前，此变量控制是否启用 TiDB 中的遥测收集。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

### tidb_enable_tiflash_read_for_write_stmt <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`ON`
- 此变量控制包含 `INSERT`、`DELETE` 和 `UPDATE` 的 SQL 语句中的读取操作是否可以下推到 TiFlash。例如：

    - `INSERT INTO SELECT` 语句中的 `SELECT` 查询（典型使用场景：[TiFlash 查询结果物化](/tiflash/tiflash-results-materialization.md)）
    - `UPDATE` 和 `DELETE` 语句中的 `WHERE` 条件过滤
- 从 v7.1.0 开始，此变量已被弃用。当 [`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50) 时，优化器会根据 [SQL 模式](/sql-mode.md) 和 TiFlash 副本的成本估算智能地决定是否将查询下推到 TiFlash。请注意，仅当当前会话的 [SQL 模式](/sql-mode.md) 不是严格模式时，TiDB 才允许将包含 `INSERT`、`DELETE` 和 `UPDATE` 的 SQL 语句（例如 `INSERT INTO SELECT`）中的读取操作下推到 TiFlash，这意味着 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`。

### tidb_enable_top_sql <span class="version-mark">v5.4.0 新增</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`

<CustomContent platform="tidb">

- 此变量用于控制是否启用 [Top SQL](/dashboard/top-sql.md) 功能。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于控制是否启用 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 功能。

</CustomContent>

### tidb_enable_tso_follower_proxy <span class="version-mark">v5.3.0 新增</span>

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，此变量是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`
- 此变量控制是否启用 TSO Follower Proxy 功能。当值为 `OFF` 时，TiDB 仅从 PD leader 获取 TSO。当值为 `ON` 时，TiDB 将 TSO 请求均匀地分配给所有 PD 服务器，PD follower 也可以处理 TSO 请求，从而降低 PD leader 的 CPU 压力。
- 启用 TSO Follower Proxy 的场景：
    * 由于 TSO 请求压力过大，PD leader 的 CPU 达到瓶颈，导致 TSO RPC 请求的延迟较高。
    * TiDB 集群有许多 TiDB 实例，并且增加 [`tidb_tso_client_batch_max_wait_time`](#tidb_tso_client_batch_max_wait_time-new-in-v530) 的值无法缓解 TSO RPC 请求的高延迟问题。

> **注意：**
>
> 假设 TSO RPC 延迟增加的原因不是 PD leader 的 CPU 使用率瓶颈（例如网络问题）。在这种情况下，启用 TSO Follower Proxy 可能会增加 TiDB 中的执行延迟并影响集群的 QPS 性能。

### tidb_enable_unsafe_substitute <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`
- 此变量控制是否以不安全的方式将表达式替换为生成列。默认值为 `OFF`，表示默认禁用不安全替换。有关更多详细信息，请参见 [生成列](/generated-columns.md)。

### tidb_enable_vectorized_expression <span class="version-mark">v4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔值
- 默认值：`ON`
- 此变量用于控制是否启用向量化执行。

### tidb_enable_window_function

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`ON`
- 此变量用于控制是否启用对 [窗口函数](/functions-and-operators/window-functions.md) 的支持。请注意，窗口函数可能会使用保留关键字。这可能会导致原本可以正常执行的 SQL 语句在 TiDB 升级后无法解析。在这种情况下，您可以将 `tidb_enable_window_function` 设置为 `OFF`。

### `tidb_enable_row_level_checksum` <span class="version-mark">v7.1.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔值
- 默认值：`OFF`

<CustomContent platform="tidb">

- 此变量用于控制是否启用 [TiCDC 单行数据的数据完整性验证](/ticdc/ticdc-integrity-check.md) 功能。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于控制是否启用 [TiCDC 单行数据的数据完整性验证](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check) 功能。

</CustomContent>

- 您可以使用 [`TIDB_ROW_CHECKSUM()`](/functions-and-operators/tidb-functions.md#tidb_row_checksum) 函数来获取行的校验和值。

### tidb_enforce_mpp <span class="version-mark">v5.1 新增</span>

- 作用域：SESSION
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`

<CustomContent platform="tidb">

- 要更改此默认值，请修改 [`performance.enforce-mpp`](/tidb-configuration-file.md#enforce-mpp) 配置值。

</CustomContent>

- 控制是否忽略优化器的成本估算，并强制使用 TiFlash 的 MPP 模式执行查询。取值选项如下：
    - `0` 或 `OFF`，表示不强制使用 MPP 模式（默认）。
    - `1` 或 `ON`，表示忽略成本估算，强制使用 MPP 模式。请注意，此设置仅在 `tidb_allow_mpp=true` 时生效。

MPP 是 TiFlash 引擎提供的分布式计算框架，支持节点间的数据交换，并提供高性能、高吞吐量的 SQL 算法。有关 MPP 模式选择的详细信息，请参考 [控制是否选择 MPP 模式](/tiflash/use-tiflash-mpp-mode.md#control-whether-to-select-the-mpp-mode)。

### tidb_evolve_plan_baselines <span class="version-mark">v4.0 新增</span>

> **警告：**
>
> 此变量控制的功能为实验性功能。不建议在生产环境中使用。如果发现 Bug，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于控制是否启用基线演进功能。有关详细介绍或用法，请参见 [基线演进](/sql-plan-management.md#baseline-evolution)。
- 为了减少基线演进对集群的影响，请使用以下配置：
    - 设置 `tidb_evolve_plan_task_max_time` 以限制每个执行计划的最大执行时间。默认值为 600 秒。
    - 设置 `tidb_evolve_plan_task_start_time` 和 `tidb_evolve_plan_task_end_time` 以限制时间窗口。默认值分别为 `00:00 +0000` 和 `23:59 +0000`。

### tidb_evolve_plan_task_end_time <span class="version-mark">v4.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Time
- 默认值：`23:59 +0000`
- 此变量用于设置一天中基线演进的结束时间。

### tidb_evolve_plan_task_max_time <span class="version-mark">v4.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`600`
- 范围：`[-1, 9223372036854775807]`
- 单位：秒
- 此变量用于限制基线演进功能中每个执行计划的最大执行时间。

### tidb_evolve_plan_task_start_time <span class="version-mark">v4.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Time
- 默认值：`00:00 +0000`
- 此变量用于设置一天中基线演进的开始时间。

### tidb_executor_concurrency <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`5`
- 范围：`[1, 256]`
- 单位：线程

此变量用于设置以下 SQL 算子的并发度（设置为一个值）：

- `index lookup`
- `index lookup join`
- `hash join`
- `hash aggregation`（`partial` 和 `final` 阶段）
- `window`
- `projection`

`tidb_executor_concurrency` 将以下现有系统变量作为一个整体进行合并，以便于管理：

+ `tidb_index_lookup_concurrency`
+ `tidb_index_lookup_join_concurrency`
+ `tidb_hash_join_concurrency`
+ `tidb_hashagg_partial_concurrency`
+ `tidb_hashagg_final_concurrency`
+ `tidb_projection_concurrency`
+ `tidb_window_concurrency`

自 v5.0 起，您仍然可以单独修改上面列出的系统变量（会返回弃用警告），并且您的修改只会影响相应的单个算子。之后，如果您使用 `tidb_executor_concurrency` 修改算子并发度，则单独修改的算子将不受影响。如果您想使用 `tidb_executor_concurrency` 修改所有算子的并发度，可以将上面列出的所有变量的值设置为 `-1`。

对于从早期版本升级到 v5.0 的系统，如果您没有修改上面列出的任何变量的值（这意味着 `tidb_hash_join_concurrency` 的值为 `5`，其余变量的值为 `4`），则先前由这些变量管理的算子并发度将自动由 `tidb_executor_concurrency` 管理。如果您修改了这些变量中的任何一个，则相应算子的并发度仍将由修改后的变量控制。

### tidb_expensive_query_time_threshold

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`60`
- 范围：`[10, 2147483647]`
- 单位：秒
- 此变量用于设置确定是否打印昂贵查询日志的阈值。昂贵查询日志和慢查询日志的区别在于：
    - 慢查询日志在语句执行后打印。
    - 昂贵查询日志打印正在执行的语句，其执行时间超过阈值，以及它们的相关信息。

### tidb_expensive_txn_time_threshold <span class="version-mark">v7.2.0 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`600`
- 范围：`[60, 2147483647]`
- 单位：秒
- 此变量控制记录昂贵事务的阈值，默认为 600 秒。当事务的持续时间超过阈值，且事务既未提交也未回滚时，该事务被认为是昂贵事务，并将被记录。

### tidb_force_priority

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`NO_PRIORITY`
- 可选值：`NO_PRIORITY`、`LOW_PRIORITY`、`HIGH_PRIORITY`、`DELAYED`
- 此变量用于更改在 TiDB 服务器上执行的语句的默认优先级。一个用例是确保执行 OLAP 查询的特定用户获得的优先级低于执行 OLTP 查询的用户。
- 默认值 `NO_PRIORITY` 表示不强制更改语句的优先级。

> **注意：**
>
> 从 v6.6.0 版本开始，TiDB 支持 [资源控制](/tidb-resource-control.md)。你可以使用此功能在不同的资源组中以不同的优先级执行 SQL 语句。通过为这些资源组配置适当的配额和优先级，你可以更好地控制具有不同优先级的 SQL 语句的调度。启用资源控制后，语句优先级将不再生效。建议你使用 [资源控制](/tidb-resource-control.md) 来管理不同 SQL 语句的资源使用情况。

### tidb_gc_concurrency <span class="version-mark">v5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 指定 GC 的 [Resolve Locks](/garbage-collection-overview.md#resolve-locks) 步骤中的线程数。值为 `-1` 表示 TiDB 将自动决定要使用的垃圾回收线程数。

### tidb_gc_enable <span class="version-mark">v5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 启用 TiKV 的垃圾回收。禁用垃圾回收会降低系统性能，因为旧版本的行将不再被清除。

### tidb_gc_life_time <span class="version-mark">v5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Duration
- 默认值：`10m0s`
- 范围：对于 TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[10m0s, 8760h0m0s]`，对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `[10m0s, 168h0m0s]`
- 每次 GC 保留数据的时间限制，格式为 Go Duration。发生 GC 时，当前时间减去此值即为安全点。

> **注意：**
>
> - 在频繁更新的场景中，`tidb_gc_life_time` 的较大值（几天甚至几个月）可能会导致潜在问题，例如：
>     - 更大的存储使用量
>     - 大量的历史数据可能会在一定程度上影响性能，特别是对于范围查询，例如 `select count(*) from t`
> - 如果有任何事务的运行时间超过 `tidb_gc_life_time`，在 GC 期间，将保留自 `start_ts` 以来的数据，以使该事务继续执行。例如，如果 `tidb_gc_life_time` 配置为 10 分钟，在所有正在执行的事务中，最早开始的事务已经运行了 15 分钟，GC 将保留最近 15 分钟的数据。

### tidb_gc_max_wait_time <span class="version-mark">v6.1.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`86400`
- 范围：`[600, 31536000]`
- 单位：秒
- 此变量用于设置活动事务阻塞 GC 安全点的最大时间。在每次 GC 时，默认情况下，安全点不会超过正在进行的事务的开始时间。如果活动事务的运行时长不超过此变量值，则 GC 安全点将被阻塞，直到运行时长超过此值。

### tidb_gc_run_interval <span class="version-mark">v5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Duration
- 默认值：`10m0s`
- 范围：`[10m0s, 8760h0m0s]`
- 指定 GC 间隔，格式为 Go Duration，例如 `"1h30m"` 和 `"15m"`

### tidb_gc_scan_lock_mode <span class="version-mark">v5.0 新增</span>

> **警告：**
>
> 目前，Green GC 是一项实验性功能。不建议在生产环境中使用它。

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`LEGACY`
- 可选值：`PHYSICAL`，`LEGACY`
    - `LEGACY`：使用旧的扫描方式，即禁用 Green GC。
    - `PHYSICAL`：使用物理扫描方法，即启用 Green GC。

<CustomContent platform="tidb">

- 此变量指定 GC 的 Resolve Locks 步骤中扫描锁的方式。当变量值设置为 `LEGACY` 时，TiDB 按 Region 扫描锁。当使用值 `PHYSICAL` 时，它使每个 TiKV 节点能够绕过 Raft 层并直接扫描数据，这可以有效地缓解启用 [Hibernate Region](/tikv-configuration-file.md#hibernate-regions) 功能时 GC 唤醒所有 Region 的影响，从而提高 Resolve Locks 步骤的执行速度。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量指定 GC 的 Resolve Locks 步骤中扫描锁的方式。当变量值设置为 `LEGACY` 时，TiDB 按 Region 扫描锁。当使用值 `PHYSICAL` 时，它使每个 TiKV 节点能够绕过 Raft 层并直接扫描数据，这可以有效地缓解 GC 唤醒所有 Region 的影响，从而提高 Resolve Locks 步骤的执行速度。

</CustomContent>

### tidb_general_log

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于你当前连接的 TiDB 实例。
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`

<CustomContent platform="tidb-cloud">

- 此变量用于设置是否在日志中记录所有 SQL 语句。默认情况下，此功能已禁用。如果需要在定位问题时跟踪所有 SQL 语句，请启用此功能。

</CustomContent>

<CustomContent platform="tidb">

- 此变量用于设置是否将所有 SQL 语句记录在 [日志](/tidb-configuration-file.md#logfile) 中。默认情况下，此功能已禁用。如果维护人员需要在定位问题时跟踪所有 SQL 语句，他们可以启用此功能。

- 如果指定了 [`log.general-log-file`](/tidb-configuration-file.md#general-log-file-new-in-v800) 配置项，则通用日志将单独写入指定的文件。

- [`log.format`](/tidb-configuration-file.md#format) 配置项使你能够配置日志消息格式，无论通用日志是位于单独的文件中还是与其他日志组合在一起。

- [`tidb_redact_log`](#tidb_redact_log) 变量使你能够编辑通用日志中记录的 SQL 语句。

- 只有成功执行的语句才会记录在通用日志中。失败的语句不会记录在通用日志中，而是记录在 TiDB 日志中，并显示 `command dispatched failed` 消息。

- 要查看此功能在日志中的所有记录，您需要将 TiDB 配置项 [`log.level`](/tidb-configuration-file.md#level) 设置为 `"info"` 或 `"debug"`，然后查询 `"GENERAL_LOG"` 字符串。记录以下信息：
    - `time`: 事件发生的时间。
    - `conn`: 当前会话的 ID。
    - `user`: 当前会话用户。
    - `schemaVersion`: 当前 schema 版本。
    - `txnStartTS`: 当前事务开始的时间戳。
    - `forUpdateTS`: 在悲观事务模式下，`forUpdateTS` 是当前 SQL 语句的时间戳。当悲观事务中发生写冲突时，TiDB 会重试当前正在执行的 SQL 语句并更新此时间戳。您可以通过 [`max-retry-count`](/tidb-configuration-file.md#max-retry-count) 配置重试次数。在乐观事务模型中，`forUpdateTS` 等同于 `txnStartTS`。
    - `isReadConsistency`: 指示当前事务隔离级别是否为读已提交 (RC)。
    - `current_db`: 当前数据库的名称。
    - `txn_mode`: 事务模式。可选值为 `OPTIMISTIC` 和 `PESSIMISTIC`。
    - `sql`: 与当前查询对应的 SQL 语句。

</CustomContent>

### tidb_non_prepared_plan_cache_size

> **警告：**
>
> 从 v7.1.0 开始，此变量已被弃用。请改用 [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710) 进行设置。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`100`
- 范围：`[1, 100000]`
- 此变量控制 [Non-prepared plan cache](/sql-non-prepared-plan-cache.md) 可以缓存的最大执行计划数量。

### tidb_generate_binary_plan <span class="version-mark">New in v6.2.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否在慢日志和语句摘要中生成二进制编码的执行计划。
- 当此变量设置为 `ON` 时，您可以在 TiDB Dashboard 中查看可视化执行计划。请注意，TiDB Dashboard 仅提供在此变量启用后生成的执行计划的可视化显示。
- 您可以执行 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan) 语句来从二进制计划中解析特定计划。

### tidb_gogc_tuner_max_value <span class="version-mark">New in v7.5.0</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`500`
- 范围：`[10, 2147483647]`
- 该变量用于控制 GOGC Tuner 可以调整的 GOGC 最大值。

### tidb_gogc_tuner_min_value <span class="version-mark">New in v7.5.0</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`100`
- 范围：`[10, 2147483647]`
- 该变量用于控制 GOGC Tuner 可以调整的 GOGC 最小值。

### tidb_gogc_tuner_threshold <span class="version-mark">New in v6.4.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`0.6`
- 范围：`[0, 0.9)`
- 此变量指定调整 GOGC 的最大内存阈值。当内存超过此阈值时，GOGC Tuner 停止工作。

### tidb_guarantee_linearizability <span class="version-mark">New in v5.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制异步提交的 commit TS 的计算方式。默认情况下（值为 `ON`），两阶段提交从 PD 服务器请求一个新的 TS，并使用该 TS 来计算最终的 commit TS。在这种情况下，保证所有并发事务的线性一致性。
- 如果将此变量设置为 `OFF`，则会跳过从 PD 服务器获取 TS 的过程，但代价是仅保证因果一致性，而不保证线性一致性。有关更多详细信息，请参见博客文章 [Async Commit, the Accelerator for Transaction Commit in TiDB 5.0](https://www.pingcap.com/blog/async-commit-the-accelerator-for-transaction-commit-in-tidb-5-0/)。
- 对于仅需要因果一致性的场景，您可以将此变量设置为 `OFF` 以提高性能。

### tidb_hash_exchange_with_new_collation

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制是否在启用新排序规则的集群中生成 MPP 哈希分区交换算子。`true` 表示生成该算子，`false` 表示不生成。
- 此变量用于 TiDB 的内部操作。**不建议**设置此变量。

### tidb_hash_join_concurrency

> **警告：**
>
> 自 v5.0 起，此变量已被弃用。请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置 `hash join` 算法的并发度。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tidb_hashagg_final_concurrency

> **警告：**
>
> 自 v5.0 起，此变量已被弃用。请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置在 `final` 阶段执行并发 `hash aggregation` 算法的并发度。
- 当聚合函数的参数不是 distinct 时，`HashAgg` 会在两个阶段并发运行，分别是 `partial` 阶段和 `final` 阶段。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tidb_hashagg_partial_concurrency

> **警告：**
>
> 自 v5.0 起，此变量已被弃用。请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置在 `partial` 阶段执行并发 `hash aggregation` 算法的并发度。
- 当聚合函数的参数不是 distinct 时，`HashAgg` 会在两个阶段并发运行，分别是 `partial` 阶段和 `final` 阶段。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tidb_historical_stats_duration <span class="version-mark">New in v6.6.0</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Duration
- 默认值: `168h`，表示 7 天
- 此变量控制历史统计信息在存储中保留的时长。

### tidb_idle_transaction_timeout <span class="version-mark">v7.6.0 新增</span>

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `0`
- 范围: `[0, 31536000]`
- 单位: 秒
- 此变量控制用户会话中事务的空闲超时时间。当用户会话处于事务状态并且空闲时间超过此变量的值时，TiDB 将终止该会话。空闲用户会话意味着没有活动的请求，并且会话正在等待新的请求。
- 默认值 `0` 表示无限制。

### tidb_ignore_prepared_cache_close_stmt <span class="version-mark">v6.0.0 新增</span>

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `OFF`
- 此变量用于设置是否忽略关闭预处理语句缓存的命令。
- 当此变量设置为 `ON` 时，将忽略 Binary 协议的 `COM_STMT_CLOSE` 命令和文本协议的 [`DEALLOCATE PREPARE`](/sql-statements/sql-statement-deallocate.md) 语句。有关详细信息，请参见 [忽略 `COM_STMT_CLOSE` 命令和 `DEALLOCATE PREPARE` 语句](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)。

### tidb_ignore_inlist_plan_digest <span class="version-mark">v7.6.0 新增</span>

- 作用域: GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `OFF`
- 此变量控制 TiDB 在生成 Plan Digests 时是否忽略不同查询中 `IN` 列表中的元素差异。

    - 当为默认值 `OFF` 时，TiDB 在生成 Plan Digests 时不会忽略 `IN` 列表中的元素差异（包括元素数量的差异）。 `IN` 列表中的元素差异会导致不同的 Plan Digests。
    - 当设置为 `ON` 时，TiDB 会忽略 `IN` 列表中的元素差异（包括元素数量的差异），并使用 `...` 替换 Plan Digests 中 `IN` 列表中的元素。 在这种情况下，TiDB 会为相同类型的 `IN` 查询生成相同的 Plan Digests。

### tidb_index_join_batch_size

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Integer
- 默认值: `25000`
- 范围: `[1, 2147483647]`
- 单位: 行
- 此变量用于设置 `index lookup join` 操作的批处理大小。
- 在 OLAP 场景中使用较大的值，在 OLTP 场景中使用较小的值。

### tidb_index_join_double_read_penalty_cost_rate <span class="version-mark">v6.6.0 新增</span>

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Float
- 默认值: `0`
- 范围: `[0, 18446744073709551615]`
- 此变量确定是否对索引连接的选择应用惩罚成本，从而降低优化器选择索引连接的可能性，并增加选择替代连接方法（如哈希连接和 tiflash 连接）的可能性。
- 当选择索引连接时，会触发许多表查找请求，这会消耗过多的资源。 您可以使用此变量来降低优化器选择索引连接的可能性。
- 此变量仅在 [`tidb_cost_model_version`](/system-variables.md#tidb_cost_model_version-new-in-v620) 变量设置为 `2` 时生效。

### tidb_index_lookup_concurrency

> **警告：**
>
> 从 v5.0 开始，此变量已弃用。 请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `-1`
- 范围: `[1, 256]`
- 单位: 线程
- 此变量用于设置 `index lookup` 操作的并发性。
- 在 OLAP 场景中使用较大的值，在 OLTP 场景中使用较小的值。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tidb_index_lookup_join_concurrency

> **警告：**
>
> 从 v5.0 开始，此变量已弃用。 请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `-1`
- 范围: `[1, 256]`
- 单位: 线程
- 此变量用于设置 `index lookup join` 算法的并发性。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tidb_index_merge_intersection_concurrency <span class="version-mark">v6.5.0 新增</span>

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 默认值: `-1`
- 范围: `[1, 256]`
- 此变量设置索引合并执行的交集操作的最大并发数。 仅当 TiDB 在动态修剪模式下访问分区表时才有效。 实际并发数是 `tidb_index_merge_intersection_concurrency` 和分区表的分区数的较小值。
- 默认值 `-1` 表示使用 `tidb_executor_concurrency` 的值。

### tidb_index_lookup_size

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Integer
- 默认值: `20000`
- 范围: `[1, 2147483647]`
- 单位: 行
- 此变量用于设置 `index lookup` 操作的批处理大小。
- 在 OLAP 场景中使用较大的值，在 OLTP 场景中使用较小的值。

### tidb_index_serial_scan_concurrency

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Integer
- 默认值: `1`
- 范围: `[1, 256]`
- 单位: 线程
- 此变量用于设置 `serial scan` 操作的并发性。
- 在 OLAP 场景中使用较大的值，在 OLTP 场景中使用较小的值。

### tidb_init_chunk_size

- 作用域: SESSION | GLOBAL
- 是否持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `32`
- 范围: `[1, 32]`
- 单位: 行
- 此变量用于设置执行过程中初始 chunk 的行数。 一个 chunk 的行数直接影响单个查询所需的内存量。 您可以通过考虑查询中所有列的总宽度和 chunk 的行数来粗略估计单个 chunk 所需的内存。 将其与执行器的并发性结合起来，您可以粗略估计单个查询所需的总内存。 建议单个 chunk 的总内存不超过 16 MiB。

### tidb_isolation_read_engines <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域: SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 默认值: `tikv,tiflash,tidb`
- 此变量用于设置 TiDB 在读取数据时可以使用的存储引擎列表。

### tidb_last_ddl_info <span class="version-mark">v6.0.0 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 类型：String
- 这是一个只读变量。它在 TiDB 内部用于获取当前会话中最后一次 DDL 操作的信息。
    - "query": 最后一次 DDL 查询字符串。
    - "seq_num": 每个 DDL 操作的序列号。它用于标识 DDL 操作的顺序。

### tidb_last_query_info <span class="version-mark">v4.0.14 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 这是一个只读变量。它在 TiDB 内部用于查询最后一条 DML 语句的事务信息。该信息包括：
    - `txn_scope`: 事务的作用域，可以是 `global` 或 `local`。
    - `start_ts`: 事务的开始时间戳。
    - `for_update_ts`: 先前执行的 DML 语句的 `for_update_ts`。这是一个 TiDB 内部术语，用于测试。通常，您可以忽略此信息。
    - `error`: 错误信息（如果有）。
    - `ru_consumption`: 执行语句消耗的 [RU](/tidb-resource-control.md#what-is-request-unit-ru)。

### tidb_last_txn_info <span class="version-mark">v4.0.9 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：String
- 此变量用于获取当前会话中最后一次事务的信息。这是一个只读变量。事务信息包括：
    - 事务作用域。
    - 开始和提交 TS。
    - 事务提交模式，可能是两阶段提交、一阶段提交或异步提交。
    - 从异步提交或一阶段提交回退到两阶段提交的事务信息。
    - 遇到的错误。

### tidb_last_plan_replayer_token <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：String
- 此变量是只读的，用于获取当前会话中最后一次 `PLAN REPLAYER DUMP` 执行的结果。

### tidb_load_based_replica_read_threshold <span class="version-mark">v7.0.0 新增</span>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`"1s"`
- 范围：`[0s, 1h]`
- 类型：String
- 此变量用于设置触发基于负载的副本读取的阈值。当 leader 节点的估计队列时间超过阈值时，TiDB 优先从 follower 节点读取数据。格式为时间长度，例如 `"100ms"` 或 `"1s"`。有关更多详细信息，请参阅[解决热点问题](/troubleshoot-hot-spot-issues.md#scatter-read-hotspots)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`"1s"`
- 范围：`[0s, 1h]`
- 类型：String
- 此变量用于设置触发基于负载的副本读取的阈值。当 leader 节点的估计队列时间超过阈值时，TiDB 优先从 follower 节点读取数据。格式为时间长度，例如 `"100ms"` 或 `"1s"`。有关更多详细信息，请参阅[解决热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#scatter-read-hotspots)。

</CustomContent>

### `tidb_load_binding_timeout` <span class="version-mark">v8.0.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`200`
- 范围：`(0, 2147483647]`
- 单位：毫秒
- 此变量用于控制加载绑定的超时时间。如果加载绑定的执行时间超过此值，则加载将停止。

### `tidb_lock_unchanged_keys` <span class="version-mark">v7.1.1 和 v7.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制是否锁定以下场景中的特定键。当值设置为 `ON` 时，这些键将被锁定。当值设置为 `OFF` 时，这些键将不会被锁定。
    - `INSERT IGNORE` 和 `REPLACE` 语句中的重复键。在 v6.1.6 之前，这些键未被锁定。此问题已在 [#42121](https://github.com/pingcap/tidb/issues/42121) 中修复。
    - `UPDATE` 语句中键的值未更改时的唯一键。在 v6.5.2 之前，这些键未被锁定。此问题已在 [#36438](https://github.com/pingcap/tidb/issues/36438) 中修复。
- 为了保持事务的一致性和合理性，不建议更改此值。如果升级 TiDB 由于这两个修复导致严重的性能问题，并且可以接受没有锁定的行为（请参阅上述问题），则可以将此变量设置为 `OFF`。

### tidb_log_file_max_days <span class="version-mark">v5.3.0 新增</span>

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，此变量是只读的。

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 2147483647]`

<CustomContent platform="tidb">

- 此变量用于设置当前 TiDB 实例上日志保留的最大天数。其值默认为配置文件中 [`max-days`](/tidb-configuration-file.md#max-days) 配置的值。更改变量值仅影响当前 TiDB 实例。TiDB 重启后，变量值将被重置，配置值不受影响。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于设置当前 TiDB 实例上日志保留的最大天数。

</CustomContent>

### tidb_low_resolution_tso

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于设置是否启用低精度 TSO 功能。启用此功能后，TiDB 使用缓存的时间戳读取数据。默认情况下，缓存的时间戳每 2 秒更新一次。从 v8.0.0 开始，您可以通过 [`tidb_low_resolution_tso_update_interval`](#tidb_low_resolution_tso_update_interval-new-in-v800) 配置更新间隔。
- 主要适用场景是在读取旧数据可以接受的情况下，减少小型只读事务获取 TSO 的开销。

### `tidb_low_resolution_tso_update_interval` <span class="version-mark">v8.0.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`2000`
- 范围：`[10, 60000]`
- 单位：毫秒
- 此变量用于设置低精度 TSO 功能中使用的缓存时间戳的更新间隔，以毫秒为单位。
- 仅当启用 [`tidb_low_resolution_tso`](#tidb_low_resolution_tso) 时，此变量才可用。

### tidb_max_auto_analyze_time <span class="version-mark">v6.1.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`43200`
- 范围：`[0, 2147483647]`
- 单位：秒
- 此变量用于指定自动 `ANALYZE` 任务的最大执行时间。当自动 `ANALYZE` 任务的执行时间超过指定时间时，该任务将被终止。当此变量的值为 `0` 时，自动 `ANALYZE` 任务的最大执行时间没有限制。

### tidb_max_bytes_before_tiflash_external_group_by <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否支持 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`-1`
- 取值范围：`[-1, 9223372036854775807]`
- 此变量用于指定 TiFlash 中带有 `GROUP BY` 的 Hash Aggregation 算子的最大内存使用量，以字节为单位。当内存使用量超过指定值时，TiFlash 会触发 Hash Aggregation 算子溢写到磁盘。当此变量的值为 `-1` 时，TiDB 不会将此变量传递给 TiFlash。只有当此变量的值大于等于 `0` 时，TiDB 才会将此变量传递给 TiFlash。当此变量的值为 `0` 时，表示内存使用量不受限制，即 TiFlash Hash Aggregation 算子不会触发溢写。详情请参考 [TiFlash 溢写到磁盘](/tiflash/tiflash-spill-disk.md)。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，聚合通常在多个 TiFlash 节点上分布式执行。此变量控制单个 TiFlash 节点上聚合算子的最大内存使用量。
> - 当此变量设置为 `-1` 时，TiFlash 会根据其自身配置项 [`max_bytes_before_external_group_by`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) 的值来确定聚合算子的最大内存使用量。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，聚合通常在多个 TiFlash 节点上分布式执行。此变量控制单个 TiFlash 节点上聚合算子的最大内存使用量。
> - 当此变量设置为 `-1` 时，TiFlash 会根据其自身配置项 `max_bytes_before_external_group_by` 的值来确定聚合算子的最大内存使用量。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_join <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否支持 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`-1`
- 取值范围：`[-1, 9223372036854775807]`
- 此变量用于指定 TiFlash 中带有 `JOIN` 的 Hash Join 算子的最大内存使用量，以字节为单位。当内存使用量超过指定值时，TiFlash 会触发 Hash Join 算子溢写到磁盘。当此变量的值为 `-1` 时，TiDB 不会将此变量传递给 TiFlash。只有当此变量的值大于等于 `0` 时，TiDB 才会将此变量传递给 TiFlash。当此变量的值为 `0` 时，表示内存使用量不受限制，即 TiFlash Hash Join 算子不会触发溢写。详情请参考 [TiFlash 溢写到磁盘](/tiflash/tiflash-spill-disk.md)。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，Join 通常在多个 TiFlash 节点上分布式执行。此变量控制单个 TiFlash 节点上 Join 算子的最大内存使用量。
> - 当此变量设置为 `-1` 时，TiFlash 会根据其自身配置项 [`max_bytes_before_external_join`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) 的值来确定 Join 算子的最大内存使用量。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，Join 通常在多个 TiFlash 节点上分布式执行。此变量控制单个 TiFlash 节点上 Join 算子的最大内存使用量。
> - 当此变量设置为 `-1` 时，TiFlash 会根据其自身配置项 `max_bytes_before_external_join` 的值来确定 Join 算子的最大内存使用量。

</CustomContent>

### tidb_max_bytes_before_tiflash_external_sort <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否支持 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`-1`
- 取值范围：`[-1, 9223372036854775807]`
- 此变量用于指定 TiFlash 中 TopN 和 Sort 算子的最大内存使用量，以字节为单位。当内存使用量超过指定值时，TiFlash 会触发 TopN 和 Sort 算子溢写到磁盘。当此变量的值为 `-1` 时，TiDB 不会将此变量传递给 TiFlash。只有当此变量的值大于等于 `0` 时，TiDB 才会将此变量传递给 TiFlash。当此变量的值为 `0` 时，表示内存使用量不受限制，即 TiFlash TopN 和 Sort 算子不会触发溢写。详情请参考 [TiFlash 溢写到磁盘](/tiflash/tiflash-spill-disk.md)。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，TopN 和 Sort 通常在多个 TiFlash 节点上分布式执行。此变量控制单个 TiFlash 节点上 TopN 和 Sort 算子的最大内存使用量。
> - 当此变量设置为 `-1` 时，TiFlash 会根据其自身配置项 [`max_bytes_before_external_sort`](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters) 的值来确定 TopN 和 Sort 算子的最大内存使用量。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> - 如果 TiDB 集群有多个 TiFlash 节点，TopN 和 Sort 通常在多个 TiFlash 节点上分布式执行。此变量控制单个 TiFlash 节点上 TopN 和 Sort 算子的最大内存使用量。
> - 当此变量设置为 `-1` 时，TiFlash 会根据其自身配置项 `max_bytes_before_external_sort` 的值来确定 TopN 和 Sort 算子的最大内存使用量。

</CustomContent>

### tidb_max_chunk_size

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否支持 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1024`
- 取值范围：`[32, 2147483647]`
- 单位：行
- 此变量用于设置执行过程中一个 Chunk 的最大行数。设置过大的值可能会导致缓存局部性问题。建议此变量的值不大于 65536。一个 Chunk 的行数直接影响单个查询所需的内存量。您可以粗略地估计单个 Chunk 所需的内存，方法是考虑查询中所有列的总宽度和 Chunk 的行数。结合执行器的并发性，您可以粗略估计单个查询所需的总内存。建议单个 Chunk 的总内存不超过 16 MiB。当查询涉及大量数据且单个 Chunk 不足以处理所有数据时，TiDB 会多次处理，每次处理迭代都会使 Chunk 大小加倍，从 [`tidb_init_chunk_size`](#tidb_init_chunk_size) 开始，直到 Chunk 大小达到 `tidb_max_chunk_size` 的值。

### tidb_max_delta_schema_count <span class="version-mark">v2.1.18 和 v3.0.5 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否支持 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1024`
- 取值范围：`[100, 16384]`
- 该变量用于设置允许缓存的最大 schema 版本数（为相应版本修改的表 ID）。取值范围为 100 ~ 16384。

### tidb_max_paging_size <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`50000`
- 范围：`[1, 9223372036854775807]`
- 单位：行
- 该变量用于设置 Coprocessor 分页请求过程中的最大行数。将其设置为太小的值会增加 TiDB 和 TiKV 之间的 RPC 计数，而将其设置为太大的值在某些情况下会导致过多的内存使用，例如加载数据和全表扫描。此变量的默认值在 OLTP 场景中比在 OLAP 场景中带来更好的性能。如果应用程序仅使用 TiKV 作为存储引擎，请考虑在执行 OLAP 工作负载查询时增加此变量的值，这可能会带来更好的性能。

### tidb_max_tiflash_threads <span class="version-mark">v6.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[-1, 256]`
- 单位：线程
- 该变量用于设置 TiFlash 执行请求的最大并发数。默认值为 `-1`，表示此系统变量无效，最大并发数取决于 TiFlash 配置 `profiles.default.max_threads` 的设置。当值为 `0` 时，TiFlash 会自动配置最大线程数。

### tidb_mem_oom_action <span class="version-mark">v6.1.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`CANCEL`
- 可选值：`CANCEL`，`LOG`

<CustomContent platform="tidb">

- 指定当单个 SQL 语句超过 `tidb_mem_quota_query` 指定的内存配额且无法溢出到磁盘时，TiDB 执行的操作。有关详细信息，请参阅 [TiDB 内存控制](/configure-memory-usage.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 指定当单个 SQL 语句超过 [`tidb_mem_quota_query`](#tidb_mem_quota_query) 指定的内存配额且无法溢出到磁盘时，TiDB 执行的操作。

</CustomContent>

- 默认值为 `CANCEL`，但在 TiDB v4.0.2 及更早版本中，默认值为 `LOG`。
- 此设置以前是一个 `tidb.toml` 选项 (`oom-action`)，但从 TiDB v6.1.0 开始更改为系统变量。

### tidb_mem_quota_analyze <span class="version-mark">v6.1.0 新增</span>

> **警告：**
>
> 目前，`ANALYZE` 内存配额是一项实验性功能，并且在生产环境中内存统计信息可能不准确。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[-1, 9223372036854775807]`
- 单位：字节
- 此变量控制 TiDB 更新统计信息的最大内存使用量。当您手动执行 [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) 以及 TiDB 在后台自动分析任务时，会发生这种内存使用。当总内存使用量超过此阈值时，用户执行的 `ANALYZE` 将退出，并报告一条错误消息，提醒您尝试降低采样率或稍后重试。如果 TiDB 后台的自动任务因超过内存阈值而退出，并且使用的采样率高于默认值，则 TiDB 将使用默认采样率重试更新。当此变量值为负数或零时，TiDB 不限制手动和自动更新任务的内存使用量。

> **注意：**
>
> 仅当在 TiDB 启动配置文件中启用了 `run-auto-analyze` 时，才会在 TiDB 集群中触发 `auto_analyze`。

### tidb_mem_quota_apply_cache <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`33554432` (32 MiB)
- 范围：`[0, 9223372036854775807]`
- 单位：字节
- 该变量用于设置 `Apply` 算子中本地缓存的内存使用阈值。
- `Apply` 算子中的本地缓存用于加速 `Apply` 算子的计算。您可以将变量设置为 `0` 以禁用 `Apply` 缓存功能。

### tidb_mem_quota_binding_cache <span class="version-mark">v6.0.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`67108864`
- 范围：`[0, 2147483647]`
- 单位：字节
- 该变量用于设置缓存 bindings 所用内存的阈值。
- 如果系统创建或捕获过多的 bindings，导致过度使用内存空间，TiDB 会在日志中返回警告。在这种情况下，缓存无法容纳所有可用的 bindings 或确定要存储哪些 bindings。因此，某些查询可能会错过它们的 bindings。要解决此问题，您可以增加此变量的值，这将增加用于缓存 bindings 的内存。修改此参数后，您需要运行 `admin reload bindings` 以重新加载 bindings 并验证修改。

### tidb_mem_quota_query

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1073741824` (1 GiB)
- 范围：`[-1, 9223372036854775807]`
- 单位：字节

<CustomContent platform="tidb">

- 对于低于 TiDB v6.1.0 的版本，这是一个会话范围变量，并使用 `tidb.toml` 中的 `mem-quota-query` 值作为初始值。从 v6.1.0 开始，`tidb_mem_quota_query` 是一个 `SESSION | GLOBAL` 范围变量。
- 对于低于 TiDB v6.5.0 的版本，此变量用于设置 **查询** 的内存配额阈值。如果查询在执行期间的内存配额超过阈值，TiDB 将执行由 [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610) 定义的操作。
- 对于 TiDB v6.5.0 及更高版本，此变量用于设置 **会话** 的内存配额阈值。如果会话在执行期间的内存配额超过阈值，TiDB 将执行由 [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610) 定义的操作。请注意，从 TiDB v6.5.0 开始，会话的内存使用量包含会话中事务消耗的内存。有关 TiDB v6.5.0 及更高版本中事务内存使用量的控制行为，请参阅 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit)。
- 当您将变量值设置为 `0` 或 `-1` 时，内存阈值为正无穷大。当您设置的值小于 128 时，该值将默认为 `128`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 对于低于 TiDB v6.1.0 的版本，这是一个会话范围变量。从 v6.1.0 开始，`tidb_mem_quota_query` 是一个 `SESSION | GLOBAL` 范围变量。
- 对于低于 TiDB v6.5.0 的版本，此变量用于设置 **查询** 的内存配额阈值。如果查询在执行期间的内存配额超过阈值，TiDB 将执行由 [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610) 定义的操作。
- 对于 TiDB v6.5.0 及更高版本，此变量用于设置**会话**的内存配额阈值。如果会话在执行期间的内存配额超过阈值，TiDB 将执行由 [`tidb_mem_oom_action`](#tidb_mem_oom_action-new-in-v610) 定义的操作。请注意，从 TiDB v6.5.0 开始，会话的内存使用量包含会话中事务消耗的内存。
- 当您将变量值设置为 `0` 或 `-1` 时，内存阈值为正无穷大。当您设置的值小于 128 时，该值将默认为 `128`。

</CustomContent>

### tidb_memory_debug_mode_alarm_ratio

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Float
- 默认值：`0`
- 此变量表示 TiDB 内存调试模式下允许的内存统计误差值。
- 此变量用于 TiDB 的内部测试。**不建议**设置此变量。

### tidb_memory_debug_mode_min_heap_inuse

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 此变量用于 TiDB 的内部测试。**不建议**设置此变量。启用此变量会影响 TiDB 的性能。
- 配置此参数后，TiDB 将进入内存调试模式，以分析内存跟踪的准确性。TiDB 将在后续 SQL 语句的执行过程中频繁触发 GC，并比较实际内存使用量和内存统计信息。如果当前内存使用量大于 `tidb_memory_debug_mode_min_heap_inuse` 且内存统计误差超过 `tidb_memory_debug_mode_alarm_ratio`，TiDB 会将相关的内存信息输出到日志和文件。

### tidb_memory_usage_alarm_ratio

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Float
- 默认值：`0.7`
- 范围：`[0.0, 1.0]`

<CustomContent platform="tidb">

- 此变量设置触发 tidb-server 内存告警的内存使用率。默认情况下，当 TiDB 内存使用量超过其总内存的 70% 并且满足任何 [告警条件](/configure-memory-usage.md#trigger-the-alarm-of-excessive-memory-usage) 时，TiDB 会打印告警日志。
- 当此变量配置为 `0` 或 `1` 时，表示禁用内存阈值告警功能。
- 当此变量配置为大于 `0` 且小于 `1` 的值时，表示启用内存阈值告警功能。

    - 如果系统变量 [`tidb_server_memory_limit`](#tidb_server_memory_limit-new-in-v640) 的值为 `0`，则内存告警阈值为 `tidb_memory-usage-alarm-ratio * 系统内存大小`。
    - 如果系统变量 `tidb_server_memory_limit` 的值设置为大于 0，则内存告警阈值为 `tidb_memory-usage-alarm-ratio * tidb_server_memory_limit`。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量设置触发 [tidb-server 内存告警](https://docs.pingcap.com/zh/tidb/stable/configure-memory-usage#trigger-the-alarm-of-excessive-memory-usage) 的内存使用率。
- 当此变量配置为 `0` 或 `1` 时，表示禁用内存阈值告警功能。
- 当此变量配置为大于 `0` 且小于 `1` 的值时，表示启用内存阈值告警功能。

</CustomContent>

### tidb_memory_usage_alarm_keep_record_num <span class="version-mark">New in v6.4.0</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`5`
- 范围：`[1, 10000]`
- 当 tidb-server 内存使用量超过内存告警阈值并触发告警时，TiDB 默认仅保留最近 5 次告警期间生成的状态文件。您可以使用此变量调整此数量。

### tidb_merge_join_concurrency

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 范围：`[1, 256]`
- 默认值：`1`
- 此变量设置查询执行时 `MergeJoin` 算子的并发度。
- **不建议**设置此变量。修改此变量的值可能会导致数据正确性问题。

### tidb_merge_partition_stats_concurrency

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`1`
- 此变量指定 TiDB 分析分区表时，合并分区表统计信息的并发度。

### tidb_enable_async_merge_global_stats <span class="version-mark">New in v7.5.0</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`。当您将 TiDB 从低于 v7.5.0 的版本升级到 v7.5.0 或更高版本时，默认值为 `OFF`。
- 此变量用于 TiDB 异步合并全局统计信息，以避免 OOM 问题。

### tidb_metric_query_range_duration <span class="version-mark">New in v4.0</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`60`
- 范围：`[10, 216000]`
- 单位：秒
- 此变量用于设置查询 `METRICS_SCHEMA` 时生成的 Prometheus 语句的范围持续时间。

### tidb_metric_query_step <span class="version-mark">New in v4.0</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`60`
- 范围：`[10, 216000]`
- 单位：秒
- 此变量用于设置查询 `METRICS_SCHEMA` 时生成的 Prometheus 语句的步长。

### tidb_min_paging_size <span class="version-mark">New in v6.2.0</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`128`
- 范围：`[1, 9223372036854775807]`
- 单位：行
- 此变量用于设置 coprocessor 分页请求过程中的最小行数。将其设置为太小的值会增加 TiDB 和 TiKV 之间的 RPC 请求计数，而将其设置为太大的值可能会导致使用 IndexLookup with Limit 执行查询时性能下降。此变量的默认值在 OLTP 场景中比在 OLAP 场景中带来更好的性能。如果应用程序仅使用 TiKV 作为存储引擎，请考虑在执行 OLAP 工作负载查询时增加此变量的值，这可能会为您带来更好的性能。

![分页大小对 TPCH 的影响](/media/paging-size-impact-on-tpch.png)

如图所示，当启用 [`tidb_enable_paging`](#tidb_enable_paging-new-in-v540) 时，TPCH 的性能会受到 `tidb_min_paging_size` 和 [`tidb_max_paging_size`](#tidb_max_paging_size-new-in-v630) 设置的影响。纵轴是执行时间，越小越好。

### tidb_mpp_store_fail_ttl

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Duration
- 默认值：`60s`
- 新启动的 TiFlash 节点不提供服务。为了防止查询失败，TiDB 限制 tidb-server 向新启动的 TiFlash 节点发送查询。此变量指示新启动的 TiFlash 节点不发送请求的时间范围。

### tidb_multi_statement_mode <span class="version-mark">v4.0.11 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`OFF`
- 可选值：`OFF`，`ON`，`WARN`
- 此变量控制是否允许在同一个 `COM_QUERY` 调用中执行多个查询。
- 为了减少 SQL 注入攻击的影响，TiDB 默认情况下会阻止在同一个 `COM_QUERY` 调用中执行多个查询。此变量旨在用作从早期 TiDB 版本升级路径的一部分。以下行为适用：

| 客户端设置            | `tidb_multi_statement_mode` 值 | 允许多个语句吗？ |
| ------------------------- | --------------------------------- | ------------------------------ |
| Multiple Statements = ON  | OFF                               | 是                            |
| Multiple Statements = ON  | ON                                | 是                            |
| Multiple Statements = ON  | WARN                              | 是                            |
| Multiple Statements = OFF | OFF                               | 否                             |
| Multiple Statements = OFF | ON                                | 是                            |
| Multiple Statements = OFF | WARN                              | 是 (+ 返回警告)        |

> **注意：**
>
> 只有默认值 `OFF` 才能被认为是安全的。如果您的应用程序是专门为早期版本的 TiDB 设计的，则可能需要设置 `tidb_multi_statement_mode=ON`。如果您的应用程序需要多语句支持，建议使用客户端库提供的设置，而不是 `tidb_multi_statement_mode` 选项。例如：
>
> * [go-sql-driver](https://github.com/go-sql-driver/mysql#multistatements) (`multiStatements`)
> * [Connector/J](https://dev.mysql.com/doc/connector-j/en/connector-j-reference-configuration-properties.html) (`allowMultiQueries`)
> * PHP [mysqli](https://www.php.net/manual/en/mysqli.quickstart.multiple-statement.php) (`mysqli_multi_query`)

### tidb_nontransactional_ignore_error <span class="version-mark">v6.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔
- 默认值：`OFF`
- 此变量指定在非事务 DML 语句中发生错误时是否立即返回错误。
- 当该值设置为 `OFF` 时，非事务 DML 语句在第一个错误处立即停止并返回错误。所有后续批次都将被取消。
- 当该值设置为 `ON` 并且批处理中发生错误时，后续批处理将继续执行，直到所有批处理都执行完毕。执行过程中发生的所有错误将一起在结果中返回。

### tidb_opt_agg_push_down

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔
- 默认值：`OFF`
- 此变量用于设置优化器是否执行将聚合函数下推到 Join、Projection 和 UnionAll 之前位置的优化操作。
- 当查询中的聚合操作速度较慢时，可以将变量值设置为 ON。

### tidb_opt_broadcast_cartesian_join

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：整数
- 默认值：`1`
- 范围：`[0, 2]`
- 指示是否允许 Broadcast Cartesian Join。
- `0` 表示不允许 Broadcast Cartesian Join。`1` 表示基于 [`tidb_broadcast_join_threshold_count`](#tidb_broadcast_join_threshold_count-new-in-v50) 允许。`2` 表示始终允许，即使表大小超过阈值。
- 此变量在 TiDB 内部使用，**不**建议修改其值。

### tidb_opt_concurrency_factor

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`3.0`
- 表示在 TiDB 中启动 Golang goroutine 的 CPU 成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### tidb_opt_copcpu_factor

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`3.0`
- 表示 TiKV Coprocessor 处理一行数据的 CPU 成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### tidb_opt_correlation_exp_factor

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：整数
- 默认值：`1`
- 范围：`[0, 2147483647]`
- 当基于列顺序相关性估计行数的方法不可用时，将使用启发式估计方法。此变量用于控制启发式方法的行为。
    - 当值为 0 时，不使用启发式方法。
    - 当值大于 0 时：
        - 值越大，表示启发式方法中可能使用索引扫描。
        - 值越小，表示启发式方法中可能使用表扫描。

### tidb_opt_correlation_threshold

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：浮点数
- 默认值：`0.9`
- 范围：`[0, 1]`
- 此变量用于设置阈值，该阈值确定是否启用使用列顺序相关性估计行数。如果当前列与 `handle` 列之间的顺序相关性超过阈值，则启用此方法。

### tidb_opt_cpu_factor

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：浮点数
- 范围：`[0, 2147483647]`
- 默认值：`3.0`
- 表示 TiDB 处理一行数据的 CPU 成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### `tidb_opt_derive_topn` <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：布尔
- 默认值：`OFF`
- 控制是否启用 [从窗口函数推导 TopN 或 Limit](/derive-topn-from-window.md) 的优化规则。

### tidb_opt_desc_factor

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`3.0`
- 表示 TiKV 以降序扫描磁盘中一行数据的成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### tidb_opt_disk_factor

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：浮点数
- 范围：`[0, 18446744073709551615]`
- 默认值：`1.5`
- 表示 TiDB 从临时磁盘读取或写入一个字节的数据的 I/O 成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### tidb_opt_distinct_agg_push_down

- 作用域：SESSION
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于设置优化器是否执行将带有 `distinct` 的聚合函数（例如 `select count(distinct a) from t`）下推到 Coprocessor 的优化操作。
- 当带有 `distinct` 操作的聚合函数在查询中速度较慢时，您可以将变量值设置为 `1`。

在以下示例中，在启用 `tidb_opt_distinct_agg_push_down` 之前，TiDB 需要从 TiKV 读取所有数据并在 TiDB 端执行 `distinct`。 启用 `tidb_opt_distinct_agg_push_down` 后，`distinct a` 被下推到 Coprocessor，并且将 `group by` 列 `test.t.a` 添加到 `HashAgg_5`。

```sql
mysql> desc select count(distinct a) from test.t;
+-------------------------+----------+-----------+---------------+------------------------------------------+
| id                      | estRows  | task      | access object | operator info                            |
+-------------------------+----------+-----------+---------------+------------------------------------------+
| StreamAgg_6             | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#4 |
| └─TableReader_10        | 10000.00 | root      |               | data:TableFullScan_9                     |
|   └─TableFullScan_9     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+-------------------------+----------+-----------+---------------+------------------------------------------+
3 rows in set (0.01 sec)

mysql> set session tidb_opt_distinct_agg_push_down = 1;
Query OK, 0 rows affected (0.00 sec)

mysql> desc select count(distinct a) from test.t;
+---------------------------+----------+-----------+---------------+------------------------------------------+
| id                        | estRows  | task      | access object | operator info                            |
+---------------------------+----------+-----------+---------------+------------------------------------------+
| HashAgg_8                 | 1.00     | root      |               | funcs:count(distinct test.t.a)->Column#3 |
| └─TableReader_9           | 1.00     | root      |               | data:HashAgg_5                           |
|   └─HashAgg_5             | 1.00     | cop[tikv] |               | group by:test.t.a,                       |
|     └─TableFullScan_7     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo           |
+---------------------------+----------+-----------+---------------+------------------------------------------+
4 rows in set (0.00 sec)
```

### tidb_opt_enable_correlation_adjustment

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制优化器是否基于列顺序相关性来估计行数

### tidb_opt_enable_hash_join <span class="version-mark">v6.5.6、v7.1.2 和 v7.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制优化器是否为表选择哈希连接。 默认值为 `ON`。 如果设置为 `OFF`，则优化器在生成执行计划时会避免选择哈希连接，除非没有其他连接算法可用。
- 如果同时配置了系统变量 `tidb_opt_enable_hash_join` 和 `HASH_JOIN` hint，则 `HASH_JOIN` hint 优先。 即使 `tidb_opt_enable_hash_join` 设置为 `OFF`，当您在查询中指定 `HASH_JOIN` hint 时，TiDB 优化器仍然会强制执行哈希连接计划。

### tidb_opt_enable_non_eval_scalar_subquery <span class="version-mark">v7.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于控制 `EXPLAIN` 语句是否禁用在优化阶段可以展开的常量子查询的执行。 当此变量设置为 `OFF` 时，`EXPLAIN` 语句会在优化阶段提前展开子查询。 当此变量设置为 `ON` 时，`EXPLAIN` 语句不会在优化阶段展开子查询。 有关更多信息，请参见 [禁用子查询扩展](/explain-walkthrough.md#disable-the-early-execution-of-subqueries)。

### tidb_opt_enable_late_materialization <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制是否启用 [TiFlash 延迟物化](/tiflash/tiflash-late-materialization.md) 功能。 请注意，TiFlash 延迟物化在 [快速扫描模式](/tiflash/use-fastscan.md) 下不起作用。
- 当此变量设置为 `OFF` 以禁用 TiFlash 延迟物化功能时，为了处理带有过滤条件（`WHERE` 子句）的 `SELECT` 语句，TiFlash 会在过滤之前扫描所需列的所有数据。 当此变量设置为 `ON` 以启用 TiFlash 延迟物化功能时，TiFlash 可以首先扫描与下推到 TableScan 算子的过滤条件相关的列数据，过滤出满足条件的行，然后扫描这些行的其他列的数据以进行进一步计算，从而减少数据处理的 IO 扫描和计算。

### tidb_opt_enable_mpp_shared_cte_execution <span class="version-mark">v7.2.0 新增</span>

> **警告：**
>
> 此变量控制的功能是实验性的。 不建议在生产环境中使用它。 此功能可能会更改或删除，恕不另行通知。 如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制非递归 [公共表表达式 (CTE)](/sql-statements/sql-statement-with.md) 是否可以在 TiFlash MPP 上执行。 默认情况下，当禁用此变量时，CTE 在 TiDB 上执行，与启用此功能相比，性能差距很大。

### tidb_opt_enable_fuzzy_binding <span class="version-mark">v7.6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量控制是否启用 [跨数据库绑定](/sql-plan-management.md#cross-database-binding) 功能。

### tidb_opt_fix_control <span class="version-mark">v6.5.3 和 v7.1.0 新增</span>

<CustomContent platform="tidb">

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：String
- 默认值：`""`
- 此变量用于控制优化器的一些内部行为。
- 优化器的行为可能因用户场景或 SQL 语句而异。 此变量提供了对优化器更细粒度的控制，并有助于防止升级后由于优化器中的行为更改而导致的性能下降。
- 有关更详细的介绍，请参见 [优化器修复控制](/optimizer-fix-controls.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 字符串
- 默认值: `""`
- 此变量用于控制优化器的一些内部行为。
- 优化器的行为可能因用户场景或 SQL 语句而异。此变量提供了对优化器更细粒度的控制，并有助于防止升级后由于优化器行为更改而导致的性能下降。
- 有关更详细的介绍，请参阅 [优化器修复控制](/optimizer-fix-controls.md)。

</CustomContent>

### tidb_opt_force_inline_cte <span class="version-mark">v6.3.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 布尔值
- 默认值: `OFF`
- 此变量用于控制是否内联整个会话中的公共表表达式 (CTE)。默认值为 `OFF`，表示默认情况下不强制内联 CTE。但是，您仍然可以通过指定 `MERGE()` hint 来内联 CTE。如果变量设置为 `ON`，则此会话中的所有 CTE（递归 CTE 除外）都将被强制内联。

### tidb_opt_advanced_join_hint <span class="version-mark">v7.0.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 布尔值
- 默认值: `ON`
- 此变量用于控制 Join Method hint（例如 [`HASH_JOIN()` hint](/optimizer-hints.md#hash_joint1_name--tl_name-) 和 [`MERGE_JOIN()` hint](/optimizer-hints.md#merge_joint1_name--tl_name-)）是否影响 Join Reorder 优化过程，包括 [`LEADING()` hint](/optimizer-hints.md#leadingt1_name--tl_name-) 的使用。默认值为 `ON`，表示不影响。如果设置为 `OFF`，则在同时使用 Join Method hint 和 `LEADING()` hint 的某些场景中可能会发生冲突。

> **注意：**
>
> v7.0.0 之前的版本的行为与将此变量设置为 `OFF` 的行为一致。为了确保向前兼容性，当您从早期版本升级到 v7.0.0 或更高版本的集群时，此变量设置为 `OFF`。为了获得更灵活的 hint 行为，强烈建议在没有性能下降的情况下将此变量切换为 `ON`。

### tidb_opt_insubq_to_join_and_agg

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 布尔值
- 默认值: `ON`
- 此变量用于设置是否启用将子查询转换为 join 和聚合的优化规则。
- 例如，在启用此优化规则后，子查询将按如下方式转换：

    ```sql
    select * from t where t.a in (select aa from t1);
    ```

    子查询转换为 join 如下：

    ```sql
    select t.* from t, (select aa from t1 group by aa) tmp_t where t.a = tmp_t.aa;
    ```

    如果 `t1` 在 `aa` 列中被限制为 `unique` 和 `not null`。您可以使用以下语句，无需聚合。

    ```sql
    select t.* from t, t1 where t.a=t1.aa;
    ```

### tidb_opt_join_reorder_threshold

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 整数
- 默认值: `0`
- 范围: `[0, 2147483647]`
- 此变量用于控制 TiDB Join Reorder 算法的选择。当参与 Join Reorder 的节点数大于此阈值时，TiDB 选择贪婪算法，当小于此阈值时，TiDB 选择动态规划算法。
- 目前，对于 OLTP 查询，建议保持默认值。对于 OLAP 查询，建议将变量值设置为 10~15，以便在 OLAP 场景中获得更好的连接顺序。

### tidb_opt_limit_push_down_threshold

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 整数
- 默认值: `100`
- 范围: `[0, 2147483647]`
- 此变量用于设置确定是否将 Limit 或 TopN 算子下推到 TiKV 的阈值。
- 如果 Limit 或 TopN 算子的值小于或等于此阈值，则这些算子将被强制下推到 TiKV。此变量解决了 Limit 或 TopN 算子由于错误估计而无法部分下推到 TiKV 的问题。

### tidb_opt_memory_factor

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 浮点数
- 范围: `[0, 2147483647]`
- 默认值: `0.001`
- 表示 TiDB 存储一行数据的内存成本。此变量在 [成本模型](/cost-model.md) 中内部使用，**不**建议修改其值。

### tidb_opt_mpp_outer_join_fixed_build_side <span class="version-mark">v5.1.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 布尔值
- 默认值: `OFF`
- 当变量值为 `ON` 时，左连接算子始终使用内表作为构建端，右连接算子始终使用外表作为构建端。如果将值设置为 `OFF`，则外连接算子可以使用表的任意一侧作为构建端。

### tidb_opt_network_factor

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 浮点数
- 范围: `[0, 2147483647]`
- 默认值: `1.0`
- 表示通过网络传输 1 字节数据的网络成本。此变量在 [成本模型](/cost-model.md) 中内部使用，**不**建议修改其值。

### tidb_opt_objective <span class="version-mark">v7.4.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 枚举
- 默认值: `moderate`
- 可选值: `moderate`, `determinate`
- 此变量控制优化器的目标。`moderate` 保持 TiDB v7.4.0 之前版本的默认行为，其中优化器尝试使用更多信息来生成更好的执行计划。`determinate` 模式倾向于更保守，并使执行计划更稳定。
- 实时统计信息是基于 DML 语句自动更新的总行数和修改的行数。当此变量设置为 `moderate`（默认值）时，TiDB 基于实时统计信息生成执行计划。当此变量设置为 `determinate` 时，TiDB 不使用实时统计信息来生成执行计划，这将使执行计划更稳定。
- 对于长期稳定的 OLTP 工作负载，或者如果用户对现有的执行计划有信心，建议使用 `determinate` 模式以减少意外执行计划更改的可能性。此外，您可以使用 [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) 来防止统计信息被修改并进一步稳定执行计划。

### tidb_opt_ordering_index_selectivity_ratio <span class="version-mark">v8.0.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: 浮点数
- 默认值: `-1`
- 范围: `[-1, 1]`
- 此变量控制索引的估计行数，该索引匹配 SQL 语句 `ORDER BY`，当 SQL 语句中存在 `ORDER BY` 和 `LIMIT` 子句，但不包含某些过滤条件时。
- 这解决了与系统变量 [tidb_opt_ordering_index_selectivity_threshold](#tidb_opt_ordering_index_selectivity_threshold-new-in-v700) 相同的查询模式。
- 它的实现方式不同，它应用了合格行将被找到的可能范围的比率或百分比。
- 值为 `-1`（默认）或小于 `0` 会禁用此比率。任何介于 `0` 和 `1` 之间的值都适用 0% 到 100% 的比率（例如，`0.5` 对应于 `50%`）。
- 在以下示例中，表 `t` 总共有 1,000,000 行。使用相同的查询，但使用 `tidb_opt_ordering_index_selectivity_ratio` 的不同值。示例中的查询包含一个 `WHERE` 子句谓词，该谓词限定了很小百分比的行（1,000,000 行中的 9,000 行）。有一个索引支持 `ORDER BY a`（索引 `ia`），但 `b` 上的过滤器不包含在此索引中。根据实际的数据分布，当扫描非过滤索引时，匹配 `WHERE` 子句和 `LIMIT 1` 的行可能会作为访问的第一行找到，或者最坏的情况是，在几乎所有行都已处理之后找到。
- 每个示例都使用索引提示来演示对 estRows 的影响。最终的计划选择取决于其他计划的可用性和成本。
- 第一个示例使用默认值 `-1`，它使用现有的估计公式。默认情况下，在找到合格行之前，会扫描一小部分行进行估计。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = -1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | id                                | estRows | task      | access object         | operator info                   |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00    | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00    | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 109.20  | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 109.20  | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    ```

- 第二个示例使用 `0`，它假设在找到合格行之前将扫描 0% 的行。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 0;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | id                                | estRows | task      | access object         | operator info                   |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00    | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00    | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 1.00    | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 1.00    | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+---------+-----------+-----------------------+---------------------------------+
    ```

- 第三个示例使用 `0.1`，它假设在找到合格行之前将扫描 10% 的行。此条件具有很高的选择性，只有 1% 的行满足条件。因此，在最坏的情况下，可能需要扫描 99% 的行才能找到符合条件的 1%。99% 的 10% 大约是 9.9%，这反映在 estRows 中。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 0.1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    | id                                | estRows  | task      | access object         | operator info                   |
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00     | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00     | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00     | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 99085.21 | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00     | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 99085.21 | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+----------+-----------+-----------------------+---------------------------------+
    ```

- 第四个示例使用 `1.0`，它假设在找到合格行之前将扫描 100% 的行。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE b <= 9000 ORDER BY a LIMIT 1;
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    | id                                | estRows   | task      | access object         | operator info                   |
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    | Limit_12                          | 1.00      | root      |                       | offset:0, count:1               |
    | └─Projection_22                   | 1.00      | root      |                       | test.t.a, test.t.b, test.t.c    |
    |   └─IndexLookUp_21                | 1.00      | root      |                       |                                 |
    |     ├─IndexFullScan_18(Build)     | 990843.14 | cop[tikv] | table:t, index:ia(a)  | keep order:true                 |
    |     └─Selection_20(Probe)         | 1.00      | cop[tikv] |                       | le(test.t.b, 9000)              |
    |       └─TableRowIDScan_19         | 990843.14 | cop[tikv] | table:t               | keep order:false                |
    +-----------------------------------+-----------+-----------+-----------------------+---------------------------------+
    ```

- 第五个例子也使用了 `1.0`，但增加了一个关于 `a` 的谓词，在最坏的情况下限制了扫描范围。这是因为 `WHERE a <= 9000` 匹配了索引，大约有 9,000 行符合条件。鉴于 `b` 上的过滤谓词不在索引中，在找到匹配 `b <= 9000` 的行之前，所有大约 9,000 行都被认为是扫描过的。

    ```sql
    > SET SESSION tidb_opt_ordering_index_selectivity_ratio = 1;

    > EXPLAIN SELECT * FROM t USE INDEX (ia) WHERE a <= 9000 AND b <= 9000 ORDER BY a LIMIT 1;
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | id                                 | estRows | task      | access object         | operator info                      |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    | Limit_12                           | 1.00    | root      |                       | offset:0, count:1                  |
    | └─Projection_22                    | 1.00    | root      |                       | test.t.a, test.t.b, test.t.c       |
    |   └─IndexLookUp_21                 | 1.00    | root      |                       |                                    |
    |     ├─IndexRangeScan_18(Build)     | 9074.99 | cop[tikv] | table:t, index:ia(a)  | range:[-inf,9000], keep order:true |
    |     └─Selection_20(Probe)          | 1.00    | cop[tikv] |                       | le(test.t.b, 9000)                 |
    |       └─TableRowIDScan_19          | 9074.99 | cop[tikv] | table:t               | keep order:false                   |
    +------------------------------------+---------+-----------+-----------------------+------------------------------------+
    ```

### tidb_opt_ordering_index_selectivity_threshold <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 默认值：`0`
- 范围：`[0, 1]`
- 该变量用于控制优化器在 SQL 语句中存在 `ORDER BY` 和 `LIMIT` 子句以及过滤条件时，如何选择索引。
- 对于此类查询，优化器会考虑选择相应的索引来满足 `ORDER BY` 和 `LIMIT` 子句（即使此索引不满足任何过滤条件）。但是，由于数据分布的复杂性，优化器在这种情况下可能会选择次优索引。
- 此变量表示一个阈值。当存在可以满足过滤条件的索引并且其选择性估计低于此阈值时，优化器将避免选择用于满足 `ORDER BY` 和 `LIMIT` 的索引。相反，它会优先选择满足过滤条件的索引。
- 例如，当变量设置为 `0` 时，优化器保持其默认行为；当它设置为 `1` 时，优化器始终优先选择满足过滤条件的索引，并避免选择同时满足 `ORDER BY` 和 `LIMIT` 子句的索引。
- 在以下示例中，表 `t` 总共有 1,000,000 行。当使用列 `b` 上的索引时，其估计行数约为 8,748，因此其选择性估计值约为 0.0087。默认情况下，优化器选择列 `a` 上的索引。但是，将此变量设置为 0.01 后，由于列 `b` 上的索引的选择性 (0.0087) 小于 0.01，因此优化器选择列 `b` 上的索引。

```sql
> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+-----------------------------------+---------+-----------+----------------------+--------------------+
| id                                | estRows | task      | access object        | operator info      |
+-----------------------------------+---------+-----------+----------------------+--------------------+
| Limit_12                          | 1.00    | root      |                      | offset:0, count:1  |
| └─Projection_25                   | 1.00    | root      |                      | test.t.a, test.t.b |
|   └─IndexLookUp_24                | 1.00    | root      |                      |                    |
|     ├─IndexFullScan_21(Build)     | 114.30  | cop[tikv] | table:t, index:ia(a) | keep order:true    |
|     └─Selection_23(Probe)         | 1.00    | cop[tikv] |                      | le(test.t.b, 9000) |
|       └─TableRowIDScan_22         | 114.30  | cop[tikv] | table:t              | keep order:false   |
+-----------------------------------+---------+-----------+----------------------+--------------------+

> SET SESSION tidb_opt_ordering_index_selectivity_threshold = 0.01;

> EXPLAIN SELECT * FROM t WHERE b <= 9000 ORDER BY a LIMIT 1;
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| id                               | estRows | task      | access object        | operator info                       |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
| TopN_9                           | 1.00    | root      |                      | test.t.a, offset:0, count:1         |
| └─IndexLookUp_20                 | 1.00    | root      |                      |                                     |
|   ├─IndexRangeScan_17(Build)     | 8748.62 | cop[tikv] | table:t, index:ib(b) | range:[-inf,9000], keep order:false |
|   └─TopN_19(Probe)               | 1.00    | cop[tikv] |                      | test.t.a, offset:0, count:1         |
|     └─TableRowIDScan_18          | 8748.62 | cop[tikv] | table:t              | keep order:false                    |
+----------------------------------+---------+-----------+----------------------+-------------------------------------+
```

### tidb_opt_prefer_range_scan <span class="version-mark">v5.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 将此变量的值设置为 `ON` 后，优化器始终优先选择范围扫描而不是全表扫描。
- 在以下示例中，在启用 `tidb_opt_prefer_range_scan` 之前，TiDB 优化器执行全表扫描。启用 `tidb_opt_prefer_range_scan` 后，优化器选择索引范围扫描。

```sql
explain select * from t where age=5;
+-------------------------+------------+-----------+---------------+-------------------+
| id                      | estRows    | task      | access object | operator info     |
+-------------------------+------------+-----------+---------------+-------------------+
| TableReader_7           | 1048576.00 | root      |               | data:Selection_6  |
| └─Selection_6           | 1048576.00 | cop[tikv] |               | eq(test.t.age, 5) |
|   └─TableFullScan_5     | 1048576.00 | cop[tikv] | table:t       | keep order:false  |
+-------------------------+------------+-----------+---------------+-------------------+
3 rows in set (0.00 sec)

set session tidb_opt_prefer_range_scan = 1;

explain select * from t where age=5;
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| id                            | estRows    | task      | access object               | operator info                 |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
| IndexLookUp_7                 | 1048576.00 | root      |                             |                               |
| ├─IndexRangeScan_5(Build)     | 1048576.00 | cop[tikv] | table:t, index:idx_age(age) | range:[5,5], keep order:false |
| └─TableRowIDScan_6(Probe)     | 1048576.00 | cop[tikv] | table:t                     | keep order:false              |
+-------------------------------+------------+-----------+-----------------------------+-------------------------------+
3 rows in set (0.00 sec)
```

### tidb_opt_prefix_index_single_scan <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `ON`
- 此变量控制 TiDB 优化器是否将一些过滤条件推送到前缀索引，以避免不必要的表查找并提高查询性能。
- 当此变量值设置为 `ON` 时，一些过滤条件会被推送到前缀索引。假设 `col` 列是表中的索引前缀列。查询中的 `col is null` 或 `col is not null` 条件被视为索引上的过滤条件，而不是表查找的过滤条件，从而避免了不必要的表查找。

<details>
<summary><code>tidb_opt_prefix_index_single_scan</code> 的使用示例</summary>

创建一个带有前缀索引的表：

```sql
CREATE TABLE t (a INT, b VARCHAR(10), c INT, INDEX idx_a_b(a, b(5)));
```

禁用 `tidb_opt_prefix_index_single_scan`：

```sql
SET tidb_opt_prefix_index_single_scan = 'OFF';
```

对于以下查询，执行计划使用前缀索引 `idx_a_b`，但需要表查找（出现 `IndexLookUp` 算子）。

```sql
EXPLAIN FORMAT='brief' SELECT COUNT(1) FROM t WHERE a = 1 AND b IS NOT NULL;
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| id                            | estRows | task      | access object                | operator info                                         |
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| HashAgg                       | 1.00    | root      |                              | funcs:count(Column#8)->Column#5                       |
| └─IndexLookUp                 | 1.00    | root      |                              |                                                       |
|   ├─IndexRangeScan(Build)     | 99.90   | cop[tikv] | table:t, index:idx_a_b(a, b) | range:[1 -inf,1 +inf], keep order:false, stats:pseudo |
|   └─HashAgg(Probe)            | 1.00    | cop[tikv] |                              | funcs:count(1)->Column#8                              |
|     └─Selection               | 99.90   | cop[tikv] |                              | not(isnull(test.t.b))                                 |
|       └─TableRowIDScan        | 99.90   | cop[tikv] | table:t                      | keep order:false, stats:pseudo                        |
+-------------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
6 rows in set (0.00 sec)
```

启用 `tidb_opt_prefix_index_single_scan`：

```sql
SET tidb_opt_prefix_index_single_scan = 'ON';
```

启用此变量后，对于以下查询，执行计划使用前缀索引 `idx_a_b`，但不需要表查找。

```sql
EXPLAIN FORMAT='brief' SELECT COUNT(1) FROM t WHERE a = 1 AND b IS NOT NULL;
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| id                       | estRows | task      | access object                | operator info                                         |
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
| StreamAgg                | 1.00    | root      |                              | funcs:count(Column#7)->Column#5                       |
| └─IndexReader            | 1.00    | root      |                              | index:StreamAgg                                       |
|   └─StreamAgg            | 1.00    | cop[tikv] |                              | funcs:count(1)->Column#7                              |
|     └─IndexRangeScan     | 99.90   | cop[tikv] | table:t, index:idx_a_b(a, b) | range:[1 -inf,1 +inf], keep order:false, stats:pseudo |
+--------------------------+---------+-----------+------------------------------+-------------------------------------------------------+
4 rows in set (0.00 sec)
```

</details>

### tidb_opt_projection_push_down <span class="version-mark">New in v6.1.0</span>

- Scope: SESSION
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Type: Boolean
- Default value: `OFF`
- 指定是否允许优化器将 `Projection` 下推到 TiKV 或 TiFlash coprocessor。

### tidb_opt_range_max_size <span class="version-mark">New in v6.4.0</span>

- Scope: SESSION | GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): Yes
- Default value: `67108864` (64 MiB)
- Scope: `[0, 9223372036854775807]`
- Unit: Bytes
- 此变量用于设置优化器构建扫描范围时使用的内存上限。当变量值为 `0` 时，构建扫描范围没有内存限制。如果构建精确扫描范围消耗的内存超过限制，优化器将使用更宽松的扫描范围（例如 `[[NULL,+inf]]`）。如果执行计划没有使用精确扫描范围，您可以增加此变量的值，以使优化器构建精确扫描范围。

此变量的使用示例如下：

<details>
<summary><code>tidb_opt_range_max_size</code> 使用示例</summary>

查看此变量的默认值。从结果可以看出，优化器最多使用 64 MiB 的内存来构建扫描范围。

```sql
SELECT @@tidb_opt_range_max_size;
```

```sql
+----------------------------+
| @@tidb_opt_range_max_size |
+----------------------------+
| 67108864                   |
+----------------------------+
1 row in set (0.01 sec)
```

```sql
EXPLAIN SELECT * FROM t use index (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

在 64 MiB 内存上限内，优化器构建以下精确扫描范围 `[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60]`，如下面的执行计划结果所示。

```sql
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id                            | estRows | task      | access object            | operator info                                                                                                                                                               |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| IndexLookUp_7                 | 0.90    | root      |                          |                                                                                                                                                                             |
| ├─IndexRangeScan_5(Build)     | 0.90    | cop[tikv] | table:t, index:idx(a, b) | range:[10 40,10 40], [10 50,10 50], [10 60,10 60], [20 40,20 40], [20 50,20 50], [20 60,20 60], [30 40,30 40], [30 50,30 50], [30 60,30 60], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.90    | cop[tikv] | table:t                  | keep order:false, stats:pseudo                                                                                                                                              |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

现在设置优化器构建扫描范围的内存使用上限为 1500 字节。

```sql
SET @@tidb_opt_range_max_size = 1500;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

在 1500 字节的内存限制下，优化器构建了更宽松的扫描范围 `[10,10], [20,20], [30,30]`，并使用警告通知用户构建精确扫描范围所需的内存使用量超过了 `tidb_opt_range_max_size` 的限制。

```sql
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
| id                            | estRows | task      | access object            | operator info                                                   |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
| IndexLookUp_8                 | 0.09    | root      |                          |                                                                 |
| ├─Selection_7(Build)          | 0.09    | cop[tikv] |                          | in(test.t.b, 40, 50, 60)                                        |
| │ └─IndexRangeScan_5          | 30.00   | cop[tikv] | table:t, index:idx(a, b) | range:[10,10], [20,20], [30,30], keep order:false, stats:pseudo |
| └─TableRowIDScan_6(Probe)     | 0.09    | cop[tikv] | table:t                  | keep order:false, stats:pseudo                                  |
+-------------------------------+---------+-----------+--------------------------+-----------------------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)
```

```sql
SHOW WARNINGS;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                     |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Memory capacity of 1500 bytes for 'tidb_opt_range_max_size' exceeded when building ranges. Less accurate ranges such as full range are chosen |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

然后设置内存使用上限为 100 字节：

```sql
set @@tidb_opt_range_max_size = 100;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

```sql
EXPLAIN SELECT * FROM t USE INDEX (idx) WHERE a IN (10,20,30) AND b IN (40,50,60);
```

在 100 字节的内存限制下，优化器选择 `IndexFullScan`，并使用警告通知用户构建精确扫描范围所需的内存超过了 `tidb_opt_range_max_size` 的限制。

```sql
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
| id                            | estRows  | task      | access object            | operator info                                      |
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
| IndexLookUp_8                 | 8000.00  | root      |                          |                                                    |
| ├─Selection_7(Build)          | 8000.00  | cop[tikv] |                          | in(test.t.a, 10, 20, 30), in(test.t.b, 40, 50, 60) |
| │ └─IndexFullScan_5           | 10000.00 | cop[tikv] | table:t, index:idx(a, b) | keep order:false, stats:pseudo                     |
| └─TableRowIDScan_6(Probe)     | 8000.00  | cop[tikv] | table:t                  | keep order:false, stats:pseudo                     |
+-------------------------------+----------+-----------+--------------------------+----------------------------------------------------+
4 rows in set, 1 warning (0.00 sec)
```

```sql
SHOW WARNINGS;
```

```sql
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                                                     |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
| Warning | 1105 | Memory capacity of 100 bytes for 'tidb_opt_range_max_size' exceeded when building ranges. Less accurate ranges such as full range are chosen |
+---------+------+---------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

</details>

### tidb_opt_scan_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 范围：`[0, 2147483647]`
- 默认值：`1.5`
- 表示 TiKV 从磁盘按升序扫描一行数据的成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### tidb_opt_seek_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Float
- 范围：`[0, 2147483647]`
- 默认值：`20`
- 表示 TiDB 从 TiKV 请求数据的启动成本。此变量在 [成本模型](/cost-model.md) 内部使用，**不**建议修改其值。

### tidb_opt_skew_distinct_agg <span class="version-mark">v6.2.0 新增</span>

> **注意：**
>
> 启用此变量进行查询性能优化**仅对 TiFlash 有效**。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`OFF`
- 此变量设置优化器是否将带有 `DISTINCT` 的聚合函数重写为两级聚合函数，例如将 `SELECT b, COUNT(DISTINCT a) FROM t GROUP BY b` 重写为 `SELECT b, COUNT(a) FROM (SELECT b, a FROM t GROUP BY b, a) t GROUP BY b`。当聚合列存在严重倾斜且 `DISTINCT` 列具有许多不同的值时，此重写可以避免查询执行中的数据倾斜并提高查询性能。

### tidb_opt_three_stage_distinct_agg <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Boolean
- 默认值：`ON`
- 此变量指定是否将 `COUNT(DISTINCT)` 聚合重写为 MPP 模式下的三阶段聚合。
- 此变量目前适用于仅包含一个 `COUNT(DISTINCT)` 的聚合。

### tidb_opt_tiflash_concurrency_factor

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型: Float
- 范围: `[0, 2147483647]`
- 默认值: `24.0`
- 表示 TiFlash 计算的并发数。此变量在内部用于成本模型，不建议修改其值。

### tidb_opt_use_invisible_indexes <span class="version-mark">v8.0.0 新增</span>

- 作用域: SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Boolean
- 默认值: `OFF`
- 此变量控制优化器是否可以在当前会话中选择[不可见索引](/sql-statements/sql-statement-create-index.md#invisible-index)进行查询优化。不可见索引由 DML 语句维护，但不会被查询优化器使用。这在您希望在永久删除索引之前进行双重检查的情况下非常有用。当变量设置为 `ON` 时，优化器可以在会话中选择不可见索引进行查询优化。

### tidb_opt_write_row_id

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域: SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Boolean
- 默认值: `OFF`
- 此变量用于控制是否允许 `INSERT`、`REPLACE` 和 `UPDATE` 语句操作 `_tidb_rowid` 列。此变量只能在使用 TiDB 工具导入数据时使用。

### tidb_optimizer_selectivity_level

- 作用域: SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Integer
- 默认值: `0`
- 范围: `[0, 2147483647]`
- 此变量控制优化器估计逻辑的迭代。更改此变量的值后，优化器的估计逻辑将发生很大变化。目前，`0` 是唯一有效的值。不建议将其设置为其他值。

### tidb_partition_prune_mode <span class="version-mark">v5.1 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 类型: Enumeration
- 默认值: `dynamic`
- 可选值: `static`, `dynamic`, `static-only`, `dynamic-only`
- 指定分区表使用 `dynamic` 还是 `static` 模式。请注意，只有在收集了完整的表级统计信息或 GlobalStats 后，动态分区才有效。在收集 GlobalStats 之前，TiDB 将使用 `static` 模式。有关 GlobalStats 的详细信息，请参阅[在动态剪枝模式下收集分区表的统计信息](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)。有关动态剪枝模式的详细信息，请参阅[分区表的动态剪枝模式](/partitioned-table.md#dynamic-pruning-mode)。

### tidb_persist_analyze_options <span class="version-mark">v5.4.0 新增</span>

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `ON`
- 此变量控制是否启用 [ANALYZE 配置持久化](/statistics.md#persist-analyze-configurations)功能。

### tidb_pessimistic_txn_fair_locking <span class="version-mark">v7.0.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `ON`
- 确定是否对悲观事务使用增强的悲观锁唤醒模型。此模型严格控制悲观锁定单点冲突场景中悲观事务的唤醒顺序，以避免不必要的唤醒。它大大降低了现有唤醒机制的随机性带来的不确定性。如果在您的业务场景中遇到频繁的单点悲观锁定冲突（例如，频繁更新同一行数据），从而导致频繁的语句重试、高尾部延迟，甚至偶尔出现 `pessimistic lock retry limit reached` 错误，您可以尝试启用此变量来解决问题。
- 对于从低于 v7.0.0 的版本升级到 v7.0.0 或更高版本的 TiDB 集群，默认情况下禁用此变量。

> **注意：**
>
> - 根据具体的业务场景，启用此选项可能会导致频繁锁冲突的事务吞吐量降低（平均延迟增加）。
> - 此选项仅对需要锁定单个键的语句生效。如果一个语句需要同时锁定多行，则此选项对这些语句无效。
> - 此功能在 v6.6.0 中由 [`tidb_pessimistic_txn_aggressive_locking`](https://docs.pingcap.com/tidb/v6.6/system-variables#tidb_pessimistic_txn_aggressive_locking-new-in-v660) 变量引入，默认情况下禁用。

### tidb_placement_mode <span class="version-mark">v6.0.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Enumeration
- 默认值: `STRICT`
- 可选值: `STRICT`, `IGNORE`
- 此变量控制 DDL 语句是否忽略 [SQL 中指定的放置规则](/placement-rules-in-sql.md)。当变量值为 `IGNORE` 时，所有放置规则选项都将被忽略。
- 它旨在供逻辑转储/恢复工具使用，以确保即使分配了无效的放置规则，也可以始终创建表。这类似于 mysqldump 如何在每个转储文件的开头写入 `SET FOREIGN_KEY_CHECKS=0;`。

### `tidb_plan_cache_invalidation_on_fresh_stats` <span class="version-mark">v7.1.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `ON`
- 此变量控制是否在更新相关表的统计信息时自动使计划缓存失效。
- 启用此变量后，计划缓存可以更充分地利用统计信息来生成执行计划。例如：
    - 如果在统计信息可用之前生成执行计划，则计划缓存在统计信息可用后重新生成执行计划。
    - 如果表的数据分布发生变化，导致先前最佳的执行计划变为非最佳，则计划缓存在重新收集统计信息后重新生成执行计划。
- 对于从低于 v7.1.0 的版本升级到 v7.1.0 或更高版本的 TiDB 集群，默认情况下禁用此变量。

### `tidb_plan_cache_max_plan_size` <span class="version-mark">v7.1.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 是
- 默认值: `2097152` (即 2 MiB)
- 范围: `[0, 9223372036854775807]`，以字节为单位。也支持带有单位 "KiB|MiB|GiB|TiB" 的内存格式。`0` 表示没有限制。
- 此变量控制可以缓存在预处理或非预处理计划缓存中的计划的最大大小。如果计划的大小超过此值，则该计划将不会被缓存。有关更多详细信息，请参阅[预处理计划缓存的内存管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)和[非预处理计划缓存](/sql-plan-management.md#usage)。

### tidb_pprof_sql_cpu <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域: GLOBAL
- 持久化到集群: 否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `0`
- 范围: `[0, 1]`
- 此变量用于控制是否在 profile 输出中标记相应的 SQL 语句，以识别和排除性能问题。

### tidb_prefer_broadcast_join_by_exchange_data_size <span class="version-mark">v7.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：`OFF`
- 此变量控制 TiDB 在选择 [MPP Hash Join 算法](/tiflash/use-tiflash-mpp-mode.md#algorithm-support-for-the-mpp-mode) 时，是否使用网络传输开销最小的算法。如果启用此变量，TiDB 将分别使用 `Broadcast Hash Join` 和 `Shuffled Hash Join` 估算网络中要交换的数据大小，然后选择较小的一个。
- 启用此变量后，[`tidb_broadcast_join_threshold_count`](/system-variables.md#tidb_broadcast_join_threshold_count-new-in-v50) 和 [`tidb_broadcast_join_threshold_size`](/system-variables.md#tidb_broadcast_join_threshold_size-new-in-v50) 将不会生效。

### tidb_prepared_plan_cache_memory_guard_ratio <span class="version-mark">v6.1.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Float
- 默认值：`0.1`
- 范围：`[0, 1]`
- 预处理计划缓存触发内存保护机制的阈值。有关详细信息，请参阅 [预处理计划缓存的内存管理](/sql-prepared-plan-cache.md)。
- 此设置以前是一个 `tidb.toml` 选项 (`prepared-plan-cache.memory-guard-ratio`)，但从 TiDB v6.1.0 开始更改为系统变量。

### tidb_prepared_plan_cache_size <span class="version-mark">v6.1.0 新增</span>

> **警告：**
>
> 从 v7.1.0 开始，此变量已弃用。请改用 [`tidb_session_plan_cache_size`](#tidb_session_plan_cache_size-new-in-v710) 进行设置。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`100`
- 范围：`[1, 100000]`
- 会话中可以缓存的最大计划数。有关详细信息，请参阅 [预处理计划缓存的内存管理](/sql-prepared-plan-cache.md)。
- 此设置以前是一个 `tidb.toml` 选项 (`prepared-plan-cache.capacity`)，但从 TiDB v6.1.0 开始更改为系统变量。

### tidb_projection_concurrency

> **警告：**
>
> 从 v5.0 开始，此变量已弃用。请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`[-1, 256]`
- 单位：线程
- 此变量用于设置 `Projection` 算子的并发度。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tidb_query_log_max_len

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`4096` (4 KiB)
- 范围：`[0, 1073741824]`
- 单位：字节
- SQL 语句输出的最大长度。当语句的输出长度大于 `tidb_query_log_max_len` 值时，该语句将被截断输出。
- 此设置以前也可用作 `tidb.toml` 选项 (`log.query-log-max-len`)，但从 TiDB v6.1.0 开始仅作为系统变量。

### tidb_rc_read_check_ts <span class="version-mark">v6.0.0 新增</span>

> **警告：**
>
> - 此功能与 [`replica-read`](#tidb_replica_read-new-in-v40) 不兼容。请勿同时启用 `tidb_rc_read_check_ts` 和 `replica-read`。
> - 如果您的客户端使用游标，则不建议启用 `tidb_rc_read_check_ts`，以防客户端已使用前一批返回的数据，并且该语句最终失败。
> - 从 v7.0.0 开始，此变量对于使用预处理语句协议的游标提取读取模式不再有效。

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于优化时间戳获取，适用于读已提交隔离级别且读写冲突很少的场景。启用此变量可以避免获取全局时间戳的延迟和成本，并可以优化事务级别的读取延迟。
- 如果读写冲突严重，启用此功能将增加获取全局时间戳的成本和延迟，并可能导致性能下降。有关详细信息，请参阅 [读已提交隔离级别](/transaction-isolation-levels.md#read-committed-isolation-level)。

### tidb_rc_write_check_ts <span class="version-mark">v6.3.0 新增</span>

> **警告：**
>
> 此功能目前与 [`replica-read`](#tidb_replica_read-new-in-v40) 不兼容。启用此变量后，客户端发送的所有请求都不能使用 `replica-read`。因此，请勿同时启用 `tidb_rc_write_check_ts` 和 `replica-read`。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于优化时间戳的获取，适用于悲观事务的 `READ-COMMITTED` 隔离级别中点写冲突较少的场景。启用此变量可以避免在执行点写语句期间获取全局时间戳所带来的延迟和开销。目前，此变量适用于三种类型的点写语句：`UPDATE`、`DELETE` 和 `SELECT ...... FOR UPDATE`。点写语句是指使用主键或唯一键作为过滤条件，并且最终执行算子包含 `POINT-GET` 的写语句。
- 如果点写冲突严重，启用此变量将增加额外的开销和延迟，从而导致性能下降。有关详细信息，请参阅 [读已提交隔离级别](/transaction-isolation-levels.md#read-committed-isolation-level)。

### tidb_read_consistency <span class="version-mark">v5.4.0 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是（请注意，如果存在[非事务性 DML 语句](/non-transactional-dml.md)，则使用 hint 修改此变量的值可能不会生效。）
- 类型：String
- 默认值：`strict`
- 此变量用于控制自动提交读取语句的读取一致性。
- 如果变量值设置为 `weak`，则读取语句遇到的锁将被直接跳过，并且读取执行可能会更快，这是弱一致性读取模式。但是，事务语义（例如原子性）和分布式一致性（例如线性一致性）无法得到保证。
- 对于自动提交读取需要快速返回且可以接受弱一致性读取结果的用户场景，可以使用弱一致性读取模式。

### tidb_read_staleness <span class="version-mark">v5.4.0 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[-2147483648, 0]`
- 此变量用于设置 TiDB 在当前会话中可以读取的历史数据的时间范围。设置该值后，TiDB 会从该变量允许的范围内选择一个尽可能新的时间戳，并且所有后续的读取操作都将针对该时间戳执行。例如，如果此变量的值设置为 `-5`，在 TiKV 具有相应历史版本数据的前提下，TiDB 将在 5 秒的时间范围内选择一个尽可能新的时间戳。

### tidb_record_plan_in_slow_log

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量用于控制是否将慢查询的执行计划包含在慢日志中。

### tidb_redact_log

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`OFF`
- 可选值：`OFF`，`ON`，`MARKER`
- 此变量控制是否隐藏记录到 TiDB 日志和慢日志中的 SQL 语句中的用户信息。
- 默认值为 `OFF`，表示不对用户信息进行任何处理。
- 当您将变量设置为 `ON` 时，用户信息将被隐藏。例如，如果执行的 SQL 语句是 `INSERT INTO t VALUES (1,2)`，则该语句在日志中记录为 `INSERT INTO t VALUES (?,?)`。
- 当您将变量设置为 `MARKER` 时，用户信息将用 `‹ ›` 包裹。例如，如果执行的 SQL 语句是 `INSERT INTO t VALUES (1,2)`，则该语句在日志中记录为 `INSERT INTO t VALUES (‹1›,‹2›)`。如果输入包含 `‹`，则转义为 `‹‹`，`›` 转义为 `››`。基于标记的日志，您可以决定在显示日志时是否对标记的信息进行脱敏。

### tidb_regard_null_as_point <span class="version-mark">v5.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制优化器是否可以使用包含 null 等价的查询条件作为索引访问的前缀条件。
- 默认情况下启用此变量。启用后，优化器可以减少要访问的索引数据量，从而加快查询执行速度。例如，如果查询涉及多列索引 `index(a, b)` 并且查询条件包含 `a<=>null and b=1`，则优化器可以使用查询条件中的 `a<=>null` 和 `b=1` 进行索引访问。如果禁用该变量，由于 `a<=>null and b=1` 包含 null 等价条件，优化器将不使用 `b=1` 进行索引访问。

### tidb_remove_orderby_in_subquery <span class="version-mark">v6.1.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：v7.2.0 之前的默认值为 `OFF`。 从 v7.2.0 开始，默认值为 `ON`。
- 指定是否删除子查询中的 `ORDER BY` 子句。
- 在 ISO/IEC SQL 标准中，`ORDER BY` 主要用于对顶级查询的结果进行排序。 对于子查询，该标准不要求结果按 `ORDER BY` 排序。
- 要对子查询结果进行排序，通常可以在外部查询中处理它，例如使用窗口函数或在外部查询中再次使用 `ORDER BY`。 这样做可以确保最终结果集的顺序。

### tidb_replica_read <span class="version-mark">v4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Enumeration
- 默认值：`leader`
- 可选值：`leader`、`follower`、`leader-and-follower`、`prefer-leader`、`closest-replicas`、`closest-adaptive` 和 `learner`。 `learner` 值在 v6.6.0 中引入。
- 此变量用于控制 TiDB 从哪里读取数据。
- 有关用法和实现的更多详细信息，请参见 [Follower read](/follower-read.md)。

### tidb_restricted_read_only <span class="version-mark">v5.2.0 新增</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- `tidb_restricted_read_only` 和 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 的行为类似。 在大多数情况下，您应该只使用 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)。
- 具有 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限的用户可以修改此变量。 但是，如果启用了 [安全增强模式](#tidb_enable_enhanced_security)，则需要额外的 `RESTRICTED_VARIABLES_ADMIN` 权限才能读取或修改此变量。
- `tidb_restricted_read_only` 在以下情况下会影响 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)：
    - 将 `tidb_restricted_read_only` 设置为 `ON` 会将 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 更新为 `ON`。
    - 将 `tidb_restricted_read_only` 设置为 `OFF` 不会更改 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)。
    - 如果 `tidb_restricted_read_only` 为 `ON`，则无法将 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 设置为 `OFF`。
- 对于 TiDB 的 DBaaS 提供商，如果 TiDB 集群是另一个数据库的下游数据库，为了使 TiDB 集群只读，您可能需要启用 [安全增强模式](#tidb_enable_enhanced_security) 来使用 `tidb_restricted_read_only`，这可以防止您的客户使用 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531) 使集群可写。 为此，您需要启用 [安全增强模式](#tidb_enable_enhanced_security)，使用具有 `SYSTEM_VARIABLES_ADMIN` 和 `RESTRICTED_VARIABLES_ADMIN` 权限的管理员用户来控制 `tidb_restricted_read_only`，并让您的数据库用户使用具有 `SUPER` 权限的 root 用户来仅控制 [`tidb_super_read_only`](#tidb_super_read_only-new-in-v531)。
- 此变量控制整个集群的只读状态。 当变量为 `ON` 时，整个集群中的所有 TiDB 服务器都处于只读模式。 在这种情况下，TiDB 仅执行不修改数据的语句，例如 `SELECT`、`USE` 和 `SHOW`。 对于其他语句（例如 `INSERT` 和 `UPDATE`），TiDB 会拒绝在只读模式下执行这些语句。
- 使用此变量启用只读模式只能确保整个集群最终进入只读状态。 如果您已更改 TiDB 集群中此变量的值，但该更改尚未传播到其他 TiDB 服务器，则未更新的 TiDB 服务器仍然**不**处于只读模式。
- TiDB 在执行 SQL 语句之前检查只读标志。 从 v6.2.0 开始，在提交 SQL 语句之前也会检查该标志。 这有助于防止长时间运行的 [自动提交](/transaction-overview.md#autocommit) 语句在服务器置于只读模式后可能修改数据的情况。
- 启用此变量后，TiDB 按以下方式处理未提交的事务：
    - 对于未提交的只读事务，您可以正常提交事务。
    - 对于未提交的非只读事务，将拒绝在这些事务中执行写操作的 SQL 语句。
    - 对于具有修改数据的未提交的只读事务，将拒绝提交这些事务。
- 启用只读模式后，所有用户（包括具有 `SUPER` 权限的用户）都无法执行可能写入数据的 SQL 语句，除非用户被明确授予 `RESTRICTED_REPLICA_WRITER_ADMIN` 权限。

### tidb_request_source_type <span class="version-mark">v7.4.0 新增</span>

- 作用域：SESSION
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：String
- 默认值：`""`
- 可选值：`"ddl"`, `"stats"`, `"br"`, `"lightning"`, `"background"`
- 此变量用于显式指定当前会话的任务类型，该类型由 [资源控制](/tidb-resource-control.md) 识别和控制。例如：`SET @@tidb_request_source_type = "background"`。

### tidb_retry_limit

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`10`
- 范围：`[-1, 9223372036854775807]`
- 此变量用于设置乐观事务的最大重试次数。当事务遇到可重试错误（例如事务冲突、事务提交非常慢或表结构更改）时，将根据此变量重新执行该事务。请注意，将 `tidb_retry_limit` 设置为 `0` 会禁用自动重试。此变量仅适用于乐观事务，不适用于悲观事务。

### tidb_row_format_version

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`2`
- 范围：`[1, 2]`
- 控制表中新保存数据的格式版本。在 TiDB v4.0 中，默认使用 [新的存储行格式](https://github.com/pingcap/tidb/blob/release-8.1/docs/design/2018-07-19-row-format.md) 版本 `2` 来保存新数据。
- 如果您从低于 v4.0.0 的 TiDB 版本升级到 v4.0.0 或更高版本，则格式版本不会更改，TiDB 将继续使用版本 `1` 的旧格式将数据写入表，这意味着**只有新创建的集群默认使用新的数据格式**。
- 请注意，修改此变量不会影响已保存的旧数据，而是仅将相应的版本格式应用于修改此变量后新写入的数据。

### tidb_runtime_filter_mode <span class="version-mark">v7.2.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Enumeration
- 默认值：`OFF`
- 可选值：`OFF`, `LOCAL`
- 控制 Runtime Filter 的模式，即 **Filter Sender operator** 和 **Filter Receiver operator** 之间的关系。有两种模式：`OFF` 和 `LOCAL`。`OFF` 表示禁用 Runtime Filter。`LOCAL` 表示在本地模式下启用 Runtime Filter。有关更多信息，请参见 [Runtime Filter 模式](/runtime-filter.md#runtime-filter-mode)。

### tidb_runtime_filter_type <span class="version-mark">v7.2.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Enumeration
- 默认值：`IN`
- 可选值：`IN`
- 控制生成的 Filter operator 使用的谓词类型。目前，仅支持一种类型：`IN`。有关更多信息，请参见 [Runtime Filter 类型](/runtime-filter.md#runtime-filter-type)。

### tidb_scatter_region

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 默认情况下，在 TiDB 中创建新表时，会拆分 Region。启用此变量后，新拆分的 Region 会在执行 `CREATE TABLE` 语句期间立即分散。这适用于在批量创建表后需要批量写入数据的场景，因为新拆分的 Region 可以预先分散在 TiKV 中，而不必等待 PD 调度。为了确保批量写入数据的持续稳定性，只有在 Region 成功分散后，`CREATE TABLE` 语句才会返回成功。这使得语句的执行时间比禁用此变量时长数倍。
- 请注意，如果在创建表时已设置 `SHARD_ROW_ID_BITS` 和 `PRE_SPLIT_REGIONS`，则在创建表后会均匀拆分指定数量的 Region。

### tidb_schema_cache_size <span class="version-mark">v8.0.0 新增</span>

> **警告：**
>
> 此变量控制的功能在当前 TiDB 版本中尚未生效。请勿更改默认值。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 此变量控制 TiDB 中 schema 缓存的大小。单位是字节。默认值为 `0`，表示未启用缓存限制功能。启用此功能后，TiDB 使用您设置的值作为最大可用内存限制，并使用最近最少使用 (LRU) 算法来缓存所需的表，从而有效减少 schema 信息占用的内存。

### tidb_schema_version_cache_limit <span class="version-mark">v7.4.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`16`
- 范围：`[2, 255]`
- 此变量限制了 TiDB 实例中可以缓存的历史 schema 版本的数量。默认值为 `16`，表示 TiDB 默认缓存 16 个历史 schema 版本。
- 通常，您不需要修改此变量。当使用 [Stale Read](/stale-read.md) 功能并且频繁执行 DDL 操作时，会导致 schema 版本非常频繁地更改。因此，当 Stale Read 尝试从快照中获取 schema 信息时，由于 schema 缓存未命中，可能需要花费大量时间来重建信息。在这种情况下，您可以增加 `tidb_schema_version_cache_limit` 的值（例如，`32`）以避免 schema 缓存未命中的问题。
- 修改此变量会导致 TiDB 的内存使用量略有增加。监控 TiDB 的内存使用情况以避免 OOM 问题。

### tidb_server_memory_limit <span class="version-mark">v6.4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`80%`
- 范围：
    - 您可以设置百分比格式的值，这意味着内存使用量相对于总内存的百分比。取值范围为 `[1%, 99%]`。
    - 您也可以设置内存大小的值。取值范围为 `0` 和 `[536870912, 9223372036854775807]`（以字节为单位）。支持带有单位 "KiB|MiB|GiB|TiB" 的内存格式。`0` 表示没有内存限制。
    - 如果此变量设置为小于 512 MiB 但不为 `0` 的内存大小，则 TiDB 使用 512 MiB 作为实际大小。
- 此变量指定 TiDB 实例的内存限制。当 TiDB 的内存使用量达到限制时，TiDB 会取消当前运行的内存使用量最高的 SQL 语句。成功取消 SQL 语句后，TiDB 会尝试调用 Golang GC 以立即回收内存，从而尽快缓解内存压力。
- 只有内存使用量超过 [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640) 限制的 SQL 语句才会被优先选择取消。
- 目前，TiDB 每次只会取消一个 SQL 语句。在 TiDB 完全取消一个 SQL 语句并回收资源后，如果内存使用量仍然大于此变量设置的限制，TiDB 才会开始下一个取消操作。

### tidb_server_memory_limit_gc_trigger <span class="version-mark">New in v6.4.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`70%`
- 范围：`[50%, 99%]`
- TiDB 尝试触发 GC 的阈值。当 TiDB 的内存使用量达到 `tidb_server_memory_limit` \* `tidb_server_memory_limit_gc_trigger` 的值时，TiDB 将主动触发 Golang GC 操作。一分钟内只会触发一次 GC 操作。

### tidb_server_memory_limit_sess_min_size <span class="version-mark">New in v6.4.0</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`134217728` (即 128 MiB)
- 范围：`[128, 9223372036854775807]`，单位为字节。也支持带有单位 "KiB|MiB|GiB|TiB" 的内存格式。
- 启用内存限制后，TiDB 将终止当前实例上内存使用量最高的 SQL 语句。此变量指定要终止的 SQL 语句的最小内存使用量。如果超过限制的 TiDB 实例的内存使用量是由太多内存使用量低的会话引起的，您可以适当降低此变量的值，以允许取消更多会话。

### tidb_service_scope <span class="version-mark">New in v7.4.0</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：String
- 默认值：""
- 可选值：长度不超过 64 个字符的字符串。有效字符包括数字 `0-9`、字母 `a-zA-Z`、下划线 `_` 和连字符 `-`。
- 此变量是一个实例级别的系统变量。您可以使用它来控制 [TiDB 分布式执行框架 (DXF)](/tidb-distributed-execution-framework.md) 下每个 TiDB 节点的 Service Scope。DXF 根据此变量的值确定可以将哪些 TiDB 节点调度来执行分布式任务。有关具体规则，请参见[任务调度](/tidb-distributed-execution-framework.md#task-scheduling)。

### tidb_session_alias <span class="version-mark">New in v7.4.0</span>

- 作用域：SESSION
- 是否持久化到集群：否
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：""
- 您可以使用此变量自定义与当前会话相关的日志中 `session_alias` 列的值，这有助于在问题排查中识别会话。此设置会影响语句执行涉及的多个节点（包括 TiKV）的日志。此变量的最大长度限制为 64 个字符，任何超过长度的字符都将被自动截断。值末尾的空格也会被自动删除。

### tidb_session_plan_cache_size <span class="version-mark">New in v7.1.0</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`100`
- 范围：`[1, 100000]`
- 此变量控制可以缓存的最大计划数。[Prepared plan cache](/sql-prepared-plan-cache.md) 和 [non-prepared plan cache](/sql-non-prepared-plan-cache.md) 共享同一个缓存。
- 当您从早期版本升级到 v7.1.0 或更高版本时，此变量的值与 [`tidb_prepared_plan_cache_size`](#tidb_prepared_plan_cache_size-new-in-v610) 保持相同。

### tidb_shard_allocate_step <span class="version-mark">New in v5.0</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`9223372036854775807`
- 范围：`[1, 9223372036854775807]`
- 此变量控制为 [`AUTO_RANDOM`](/auto-random.md) 或 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md) 属性分配的连续 ID 的最大数量。通常，`AUTO_RANDOM` ID 或 `SHARD_ROW_ID_BITS` 注释的行 ID 在一个事务中是递增且连续的。您可以使用此变量来解决大型事务场景中的热点问题。

### tidb_simplified_metrics

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 启用此变量后，TiDB 不会收集或记录 Grafana 面板中未使用的指标。

### tidb_skip_ascii_check <span class="version-mark">New in v5.0</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于设置是否跳过 ASCII 验证。
- 验证 ASCII 字符会影响性能。当您确定输入字符是有效的 ASCII 字符时，可以将变量值设置为 `ON`。

### tidb_skip_isolation_level_check

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 启用此开关后，如果将 TiDB 不支持的隔离级别分配给 `tx_isolation`，则不会报告错误。这有助于提高与设置（但不依赖于）不同隔离级别的应用程序的兼容性。

```sql
tidb> set tx_isolation='serializable';
ERROR 8048 (HY000): The isolation level 'serializable' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
tidb> set tidb_skip_isolation_level_check=1;
Query OK, 0 rows affected (0.00 sec)

tidb> set tx_isolation='serializable';
Query OK, 0 rows affected, 1 warning (0.00 sec)
```

### tidb_skip_missing_partition_stats <span class="version-mark">New in v7.3.0</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 在[动态分区裁剪模式](/partitioned-table.md#dynamic-pruning-mode)下访问分区表时，TiDB 会聚合每个分区的统计信息以生成 GlobalStats。此变量控制在缺少分区统计信息时 GlobalStats 的生成。

    - 如果此变量为 `ON`，TiDB 在生成 GlobalStats 时会跳过缺少的分区统计信息，因此 GlobalStats 的生成不受影响。
    - 如果此变量为 `OFF`，TiDB 在检测到任何缺少的分区统计信息时会停止生成 GlobalStats。

### tidb_skip_utf8_check

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于设置是否跳过 UTF-8 验证。
- 验证 UTF-8 字符会影响性能。当您确定输入字符是有效的 UTF-8 字符时，可以将此变量值设置为 `ON`。

> **注意：**
>
> 如果跳过字符检查，TiDB 可能无法检测到应用程序写入的非法 UTF-8 字符，导致执行 `ANALYZE` 时出现解码错误，并引入其他未知的编码问题。如果您的应用程序无法保证写入字符串的有效性，则不建议跳过字符检查。

### tidb_slow_log_threshold

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：GLOBAL
- 是否持久化到集群：否，仅适用于您当前连接的 TiDB 实例。
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`300`
- 范围：`[-1, 9223372036854775807]`
- 单位：毫秒
- 此变量输出慢日志消耗时间的阈值，默认设置为 300 毫秒。当查询消耗的时间大于此值时，此查询被认为是慢查询，其日志将输出到慢查询日志。请注意，当 [`log.level`](https://docs.pingcap.com/zh/tidb/v8.1/tidb-configuration-file#level) 的输出级别为 `"debug"` 时，所有查询都会记录在慢查询日志中，而与此变量的设置无关。

### tidb_slow_query_file

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 查询 `INFORMATION_SCHEMA.SLOW_QUERY` 时，只会解析配置文件中 `slow-query-file` 设置的慢查询日志名称。默认的慢查询日志名称是 "tidb-slow.log"。要解析其他日志，请将 `tidb_slow_query_file` 会话变量设置为特定的文件路径，然后查询 `INFORMATION_SCHEMA.SLOW_QUERY` 以基于设置的文件路径解析慢查询日志。

<CustomContent platform="tidb">

有关详细信息，请参阅[识别慢查询](/identify-slow-queries.md)。

</CustomContent>

### tidb_slow_txn_log_threshold <span class="version-mark">v7.0.0 新增</span>

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Unsigned integer
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 单位：毫秒
- 此变量设置慢事务日志记录的阈值。当事务的执行时间超过此阈值时，TiDB 会记录有关该事务的详细信息。当该值设置为 `0` 时，此功能将被禁用。

### tidb_snapshot

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 此变量用于设置会话读取数据的时间点。例如，当您将变量设置为 "2017-11-11 20:20:20" 或像 "400036290571534337" 这样的 TSO 编号时，当前会话会读取该时刻的数据。

### tidb_source_id <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1`
- 范围：`[1, 15]`

<CustomContent platform="tidb">

- 此变量用于在[双向复制](/ticdc/ticdc-bidirectional-replication.md)集群中配置不同的集群 ID。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于在[双向复制](https://docs.pingcap.com/zh/tidb/stable/ticdc-bidirectional-replication)集群中配置不同的集群 ID。

</CustomContent>

### tidb_stats_cache_mem_quota <span class="version-mark">v6.1.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 单位：Byte
- 默认值：`0`，表示内存配额自动设置为 TiDB 实例总内存大小的一半。
- 范围：`[0, 1099511627776]`
- 此变量设置 TiDB 统计信息缓存的内存配额。

### tidb_stats_load_pseudo_timeout <span class="version-mark">v5.4.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制当 SQL 优化等待同步加载完整列统计信息的时间达到超时时，TiDB 的行为。默认值 `ON` 表示 SQL 优化在超时后恢复使用伪统计信息。如果此变量设置为 `OFF`，则 SQL 执行在超时后失败。

### tidb_stats_load_sync_wait <span class="version-mark">v5.4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/zh/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`100`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 此变量控制是否启用同步加载统计信息功能。值 `0` 表示该功能已禁用。要启用该功能，您可以将此变量设置为 SQL 优化最多可以等待同步加载完整列统计信息的超时时间（以毫秒为单位）。有关详细信息，请参阅[加载统计信息](/statistics.md#load-statistics)。

### tidb_stmt_summary_enable_persistent <span class="version-mark">v6.6.0 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> 语句摘要持久化是一项实验性功能。不建议在生产环境中使用它。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：GLOBAL
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量是只读的。它控制是否启用[语句摘要持久化](/statement-summary-tables.md#persist-statements-summary)。

<CustomContent platform="tidb">

- 此变量的值与配置项 [`tidb_stmt_summary_enable_persistent`](/tidb-configuration-file.md#tidb_stmt_summary_enable_persistent-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_filename <span class="version-mark">v6.6.0 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> 语句摘要持久化是一项实验性功能。不建议在生产环境中使用它。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：GLOBAL
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：String
- 默认值：`"tidb-statements.log"`
- 此变量是只读的。它指定在启用[语句摘要持久化](/statement-summary-tables.md#persist-statements-summary)时，持久数据写入的文件。

<CustomContent platform="tidb">

- 此变量的值与配置项 [`tidb_stmt_summary_filename`](/tidb-configuration-file.md#tidb_stmt_summary_filename-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_file_max_backups <span class="version-mark">v6.6.0 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**

> 语句摘要持久化是一项实验性功能。不建议在生产环境中使用。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：GLOBAL
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 此变量为只读。它指定启用[语句摘要持久化](/statement-summary-tables.md#persist-statements-summary)时可以持久化的最大数据文件数。

<CustomContent platform="tidb">

- 此变量的值与配置项 [`tidb_stmt_summary_file_max_backups`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_backups-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_file_max_days <span class="version-mark">v6.6.0 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> 语句摘要持久化是一项实验性功能。不建议在生产环境中使用。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：GLOBAL
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`3`
- 单位：天
- 此变量为只读。它指定启用[语句摘要持久化](/statement-summary-tables.md#persist-statements-summary)时，持久数据文件保留的最长天数。

<CustomContent platform="tidb">

- 此变量的值与配置项 [`tidb_stmt_summary_file_max_days`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_days-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_file_max_size <span class="version-mark">v6.6.0 新增</span>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

</CustomContent>

> **警告：**
>
> 语句摘要持久化是一项实验性功能。不建议在生产环境中使用。此功能可能会更改或删除，恕不另行通知。如果您发现错误，可以在 GitHub 上报告 [issue](https://github.com/pingcap/tidb/issues)。

- 作用域：GLOBAL
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`64`
- 单位：MiB
- 此变量为只读。它指定启用[语句摘要持久化](/statement-summary-tables.md#persist-statements-summary)时，持久数据文件的最大大小。

<CustomContent platform="tidb">

- 此变量的值与配置项 [`tidb_stmt_summary_file_max_size`](/tidb-configuration-file.md#tidb_stmt_summary_file_max_size-new-in-v660) 的值相同。

</CustomContent>

### tidb_stmt_summary_history_size <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`24`
- 范围：`[0, 255]`
- 此变量用于设置[语句摘要表](/statement-summary-tables.md)的历史容量。

### tidb_stmt_summary_internal_query <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`OFF`
- 此变量用于控制是否在[语句摘要表](/statement-summary-tables.md)中包含 TiDB 的 SQL 信息。

### tidb_stmt_summary_max_sql_length <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`4096`
- 范围：`[0, 2147483647]`
- 单位：字节

<CustomContent platform="tidb">

- 此变量用于控制[语句摘要表](/statement-summary-tables.md)和 [TiDB Dashboard](/dashboard/dashboard-intro.md) 中 SQL 字符串的长度。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于控制[语句摘要表](/statement-summary-tables.md) 中 SQL 字符串的长度。

</CustomContent>

### tidb_stmt_summary_max_stmt_count <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`3000`
- 范围：`[1, 32767]`
- 此变量用于限制 [`statements_summary`](/statement-summary-tables.md#statements_summary) 和 [`statements_summary_history`](/statement-summary-tables.md#statements_summary_history) 表可以在内存中总共存储的 SQL 摘要的数量。

<CustomContent platform="tidb">

> **注意：**
>
> 当启用 [`tidb_stmt_summary_enable_persistent`](/statement-summary-tables.md#persist-statements-summary) 时，`tidb_stmt_summary_max_stmt_count` 仅限制 [`statements_summary`](/statement-summary-tables.md#statements_summary) 表可以在内存中存储的 SQL 摘要的数量。

</CustomContent>

### tidb_stmt_summary_refresh_interval <span class="version-mark">v4.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1800`
- 范围：`[1, 2147483647]`
- 单位：秒
- 此变量用于设置[语句摘要表](/statement-summary-tables.md)的刷新时间。

### tidb_store_batch_size

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`4`
- 范围：`[0, 25000]`
- 此变量用于控制 `IndexLookUp` 算子的 Coprocessor Tasks 的批量大小。 `0` 表示禁用批量处理。当任务数量相对较大且出现慢查询时，您可以增加此变量以优化查询。

### tidb_store_limit <span class="version-mark">v3.0.4 和 v4.0 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 此变量用于限制 TiDB 可以同时发送到 TiKV 的最大请求数。 0 表示没有限制。

### tidb_streamagg_concurrency

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1`
- 此变量设置查询执行时 `StreamAgg` 算子的并发度。
- **不建议**设置此变量。修改变量值可能会导致数据正确性问题。

### tidb_super_read_only <span class="version-mark">v5.3.1 新增</span>

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `OFF`
- `tidb_super_read_only` 旨在作为 MySQL 变量 `super_read_only` 的替代品来实现。但是，由于 TiDB 是一个分布式数据库，`tidb_super_read_only` 不会在执行后立即使数据库变为只读，而是最终变为只读。
- 具有 `SUPER` 或 `SYSTEM_VARIABLES_ADMIN` 权限的用户可以修改此变量。
- 此变量控制整个集群的只读状态。当变量为 `ON` 时，整个集群中的所有 TiDB 服务器都处于只读模式。在这种情况下，TiDB 仅执行不修改数据的语句，例如 `SELECT`、`USE` 和 `SHOW`。对于其他语句，例如 `INSERT` 和 `UPDATE`，TiDB 会拒绝在只读模式下执行这些语句。
- 使用此变量启用只读模式只能确保整个集群最终进入只读状态。如果您已在 TiDB 集群中更改了此变量的值，但该更改尚未传播到其他 TiDB 服务器，则未更新的 TiDB 服务器仍然**不是**处于只读模式。
- TiDB 在执行 SQL 语句之前检查只读标志。从 v6.2.0 开始，在提交 SQL 语句之前也会检查该标志。这有助于防止长时间运行的 [auto commit](/transaction-overview.md#autocommit) 语句在服务器进入只读模式后修改数据的情况。
- 启用此变量后，TiDB 通过以下方式处理未提交的事务：
    - 对于未提交的只读事务，您可以正常提交事务。
    - 对于未提交的非只读事务，将拒绝在这些事务中执行写操作的 SQL 语句。
    - 对于具有修改数据的未提交只读事务，将拒绝提交这些事务。
- 启用只读模式后，所有用户（包括具有 `SUPER` 权限的用户）都无法执行可能写入数据的 SQL 语句，除非该用户被明确授予 `RESTRICTED_REPLICA_WRITER_ADMIN` 权限。
- 当 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) 系统变量设置为 `ON` 时，`tidb_super_read_only` 在某些情况下会受到 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) 的影响。有关详细影响，请参阅 [`tidb_restricted_read_only`](#tidb_restricted_read_only-new-in-v520) 的描述。

### tidb_sysdate_is_now <span class="version-mark">v6.0.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `OFF`
- 此变量用于控制 `SYSDATE` 函数是否可以被 `NOW` 函数替换。此配置项与 MySQL 选项 [`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now) 具有相同的效果。

### tidb_sysproc_scan_concurrency <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `1`
- 范围: `[1, 4294967295]`。v7.5.0 及更早版本的最大值为 `256`。
- 此变量用于设置 TiDB 执行内部 SQL 语句（例如自动更新统计信息）时执行的扫描操作的并发性。

### tidb_table_cache_lease <span class="version-mark">v6.0.0 新增</span>

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `3`
- 范围: `[1, 10]`
- 单位: 秒
- 此变量用于控制 [缓存表](/cached-tables.md) 的租约时间，默认值为 `3`。此变量的值会影响对缓存表的修改。对缓存表进行修改后，最长的等待时间可能是 `tidb_table_cache_lease` 秒。如果表是只读的或可以接受较高的写入延迟，则可以增加此变量的值，以增加缓存表的有效时间并减少租约续订的频率。

### tidb_tmp_table_max_size <span class="version-mark">v5.3.0 新增</span>

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `67108864`
- 范围: `[1048576, 137438953472]`
- 单位: 字节
- 此变量用于设置单个[临时表](/temporary-tables.md)的最大大小。任何大小大于此变量值的临时表都会导致错误。

### tidb_top_sql_max_meta_count <span class="version-mark">v6.0.0 新增</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `5000`
- 范围: `[1, 10000]`

<CustomContent platform="tidb">

- 此变量用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟收集的 SQL 语句类型的最大数量。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于控制 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 每分钟收集的 SQL 语句类型的最大数量。

</CustomContent>

### tidb_top_sql_max_time_series_count <span class="version-mark">v6.0.0 新增</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

> **注意：**
>
> 目前，TiDB Dashboard 中的 Top SQL 页面仅显示对负载贡献最大的前 5 种 SQL 查询类型，这与 `tidb_top_sql_max_time_series_count` 的配置无关。

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Integer
- 默认值: `100`
- 范围: `[1, 5000]`

<CustomContent platform="tidb">

- 此变量用于控制 [Top SQL](/dashboard/top-sql.md) 每分钟可以记录的对负载贡献最大的 SQL 语句的数量（即前 N 个）。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于控制 [Top SQL](https://docs.pingcap.com/tidb/stable/top-sql) 每分钟可以记录的对负载贡献最大的 SQL 语句的数量（即前 N 个）。

</CustomContent>

### tidb_track_aggregate_memory_usage

- 作用域: SESSION | GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Boolean
- 默认值: `ON`
- 此变量控制 TiDB 是否跟踪聚合函数的内存使用情况。

> **警告：**
>
> 如果禁用此变量，TiDB 可能无法准确跟踪内存使用情况，并且无法控制相应 SQL 语句的内存使用情况。

### tidb_tso_client_batch_max_wait_time <span class="version-mark">v5.3.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域: GLOBAL
- 持久化到集群: 是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): 否
- 类型: Float
- 默认值: `0`
- 范围: `[0, 10]`
- 单位: 毫秒
- 此变量用于设置 TiDB 从 PD 请求 TSO 时，批量操作的最大等待时间。默认值为 `0`，表示没有额外的等待时间。
- 每次从 PD 获取 TSO 请求时，TiDB 使用的 PD Client 会尽可能多地收集同时收到的 TSO 请求。然后，PD Client 将收集到的请求批量合并为一个 RPC 请求，并将其发送到 PD。这有助于减轻 PD 的压力。
- 将此变量设置为大于 `0` 的值后，TiDB 会在每次批量合并结束前等待此值的最大持续时间。这是为了收集更多的 TSO 请求并提高批量操作的效果。
- 增加此变量值的场景：
    * 由于 TSO 请求的压力过大，PD leader 的 CPU 达到瓶颈，导致 TSO RPC 请求的延迟较高。
    * 集群中的 TiDB 实例不多，但每个 TiDB 实例都处于高并发状态。
- 建议将此变量设置为尽可能小的值。

> **注意：**
>
> 假设 TSO RPC 延迟增加的原因不是 PD leader 的 CPU 使用率瓶颈（例如网络问题）。在这种情况下，增加 `tidb_tso_client_batch_max_wait_time` 的值可能会增加 TiDB 中的执行延迟，并影响集群的 QPS 性能。

### tidb_ttl_delete_rate_limit <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`0`
- 范围：`[0, 9223372036854775807]`
- 此变量用于限制每个 TiDB 节点上 TTL 作业中 `DELETE` 语句的速率。该值表示 TTL 作业中单个节点每秒允许的最大 `DELETE` 语句数。当此变量设置为 `0` 时，不应用任何限制。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_delete_batch_size <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`100`
- 范围：`[1, 10240]`
- 此变量用于设置 TTL 作业中单个 `DELETE` 事务中可以删除的最大行数。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_delete_worker_count <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`4`
- 范围：`[1, 256]`
- 此变量用于设置每个 TiDB 节点上 TTL 作业的最大并发数。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_job_enable <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 类型：Boolean
- 此变量用于控制是否启用 TTL 作业。如果设置为 `OFF`，则所有具有 TTL 属性的表都会自动停止清理过期数据。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_scan_batch_size <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`500`
- 范围：`[1, 10240]`
- 此变量用于设置 TTL 作业中用于扫描过期数据的每个 `SELECT` 语句的 `LIMIT` 值。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_scan_worker_count <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`4`
- 范围：`[1, 256]`
- 此变量用于设置每个 TiDB 节点上 TTL 扫描作业的最大并发数。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_job_schedule_window_start_time <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Time
- 持久化到集群：是
- 默认值：`00:00 +0000`
- 此变量用于控制后台 TTL 作业的调度窗口的开始时间。修改此变量的值时，请注意，较小的窗口可能会导致过期数据清理失败。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_job_schedule_window_end_time <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Time
- 持久化到集群：是
- 默认值：`23:59 +0000`
- 此变量用于控制后台 TTL 作业的调度窗口的结束时间。修改此变量的值时，请注意，较小的窗口可能会导致过期数据清理失败。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_ttl_running_tasks <span class="version-mark">v7.0.0 新增</span>

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`-1`
- 范围：`-1` 和 `[1, 256]`
- 指定整个集群中正在运行的 TTL 任务的最大数量。 `-1` 表示 TTL 任务的数量等于 TiKV 节点的数量。有关更多信息，请参阅 [Time to Live](/time-to-live.md)。

### tidb_txn_assertion_level <span class="version-mark">v6.0.0 新增</span>

- 作用域：SESSION | GLOBAL
- 持久化到集群：是
- 适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`FAST`
- 可能的值：`OFF`、`FAST`、`STRICT`
- 此变量用于控制断言级别。断言是数据和索引之间的一致性检查，用于检查正在写入的键在事务提交过程中是否存在。有关更多信息，请参阅 [解决数据和索引不一致问题](/troubleshoot-data-inconsistency-errors.md)。

    - `OFF`：禁用此检查。
    - `FAST`：启用大多数检查项，几乎不影响性能。
    - `STRICT`：启用所有检查项，当系统工作负载较高时，对悲观事务性能有轻微影响。

- 对于 v6.0.0 或更高版本的新集群，默认值为 `FAST`。对于从低于 v6.0.0 的版本升级的现有集群，默认值为 `OFF`。

### tidb_txn_commit_batch_size <span class="version-mark">v6.2.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`16384`
- 范围：`[1, 1073741824]`
- 单位：字节

<CustomContent platform="tidb">

- 此变量用于控制 TiDB 发送到 TiKV 的事务提交请求的批量大小。如果应用程序工作负载中的大多数事务都有大量的写入操作，则将此变量调整为更大的值可以提高批量处理的性能。但是，如果此变量设置得太大并超过 TiKV 的 [`raft-entry-max-size`](/tikv-configuration-file.md#raft-entry-max-size) 限制，则提交可能会失败。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于控制 TiDB 发送到 TiKV 的事务提交请求的批量大小。如果应用程序工作负载中的大多数事务都有大量的写入操作，则将此变量调整为更大的值可以提高批量处理的性能。但是，如果此变量设置得太大并超过 TiKV 的单个日志的最大大小限制（默认为 8 MiB），则提交可能会失败。

</CustomContent>

### tidb_txn_entry_size_limit <span class="version-mark">v7.6.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`0`
- 范围：`[0, 125829120]`
- 单位：字节

<CustomContent platform="tidb">

- 此变量用于动态修改 TiDB 配置项 [`performance.txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v4010-and-v500)。它限制 TiDB 中单行数据的大小，与配置项等效。此变量的默认值为 `0`，表示 TiDB 默认使用配置项 `txn-entry-size-limit` 的值。当此变量设置为非零值时，`txn-entry-size-limit` 也会设置为相同的值。

</CustomContent>

<CustomContent platform="tidb-cloud">

- 此变量用于动态修改 TiDB 配置项 [`performance.txn-entry-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-entry-size-limit-new-in-v4010-and-v500)。它限制 TiDB 中单行数据的大小，与配置项等效。此变量的默认值为 `0`，表示 TiDB 默认使用配置项 `txn-entry-size-limit` 的值。当此变量设置为非零值时，`txn-entry-size-limit` 也会设置为相同的值。

</CustomContent>

> **注意：**
>
> 使用 SESSION 作用域修改此变量只会影响当前用户会话，而不会影响 TiDB 内部会话。如果 TiDB 内部事务的条目大小超过配置项的限制，则可能会导致事务失败。因此，要动态增加限制，建议使用 GLOBAL 作用域修改变量。

### tidb_txn_mode

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，此变量为只读。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`pessimistic`
- 可选值：`pessimistic`，`optimistic`
- 此变量用于设置事务模式。TiDB 3.0 支持悲观事务。自 TiDB 3.0.8 起，默认启用[悲观事务模式](/pessimistic-transaction.md)。
- 如果您将 TiDB 从 v3.0.7 或更早版本升级到 v3.0.8 或更高版本，则默认事务模式不会更改。**只有新创建的集群默认使用悲观事务模式**。
- 如果此变量设置为 "optimistic" 或 ""，则 TiDB 使用[乐观事务模式](/optimistic-transaction.md)。

### tidb_use_plan_baselines <span class="version-mark">v4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔
- 默认值：`ON`
- 此变量用于控制是否启用执行计划绑定功能。默认情况下启用，可以通过分配 `OFF` 值来禁用。有关执行计划绑定的使用，请参见[执行计划绑定](/sql-plan-management.md#create-a-binding)。

### tidb_wait_split_region_finish

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，此变量为只读。

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：布尔
- 默认值：`ON`
- 通常，分散 Region 需要很长时间，这取决于 PD 调度和 TiKV 负载。此变量用于设置在执行 `SPLIT REGION` 语句时，是否在所有 Region 完全分散后将结果返回给客户端：
    - `ON` 要求 `SPLIT REGIONS` 语句等待直到所有 Region 都被分散。
    - `OFF` 允许 `SPLIT REGIONS` 语句在完成分散所有 Region 之前返回。
- 请注意，在分散 Region 时，正在分散的 Region 的写入和读取性能可能会受到影响。在批量写入或数据导入场景中，建议在 Region 分散完成后导入数据。

### tidb_wait_split_region_timeout

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，此变量为只读。

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`300`
- 范围：`[1, 2147483647]`
- 单位：秒
- 此变量用于设置执行 `SPLIT REGION` 语句的超时时间。如果语句在指定的时间值内未完全执行，则返回超时错误。

### tidb_window_concurrency <span class="version-mark">v4.0 新增</span>

> **警告：**
>
> 自 v5.0 起，此变量已弃用。请改用 [`tidb_executor_concurrency`](#tidb_executor_concurrency-new-in-v50) 进行设置。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：整数
- 默认值：`-1`
- 范围：`[1, 256]`
- 单位：线程
- 此变量用于设置窗口算子的并发度。
- 值为 `-1` 表示将使用 `tidb_executor_concurrency` 的值。

### tiflash_fastscan <span class="version-mark">v6.3.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：`OFF`
- 类型：布尔
- 如果启用 [FastScan](/tiflash/use-fastscan.md)（设置为 `ON`），TiFlash 提供更高效的查询性能，但不保证查询结果的准确性或数据一致性。

### tiflash_fine_grained_shuffle_batch_size <span class="version-mark">v6.2.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 默认值：`8192`
- 范围：`[1, 18446744073709551615]`
- 启用 Fine Grained Shuffle 后，下推到 TiFlash 的窗口函数可以并行执行。此变量控制发送方发送的数据的批量大小。
- 性能影响：根据您的业务需求设置合理的大小。不正确的设置会影响性能。如果该值设置得太小，例如 `1`，会导致每个 Block 进行一次网络传输。如果该值设置得太大，例如表的总行数，会导致接收端花费大部分时间等待数据，流水线计算无法工作。要设置合适的值，您可以观察 TiFlash 接收器接收到的行数分布。如果大多数线程只接收到少量行，例如几百行，您可以增加此值以减少网络开销。

### tiflash_fine_grained_shuffle_stream_count <span class="version-mark">v6.2.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：是
- 类型：Integer
- 默认值：`0`
- 范围：`[-1, 1024]`
- 当窗口函数下推到 TiFlash 执行时，可以使用此变量来控制窗口函数执行的并发级别。可能的值如下：

    * -1：禁用 Fine Grained Shuffle 功能。下推到 TiFlash 的窗口函数在单线程中执行。
    * 0：启用 Fine Grained Shuffle 功能。如果 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) 设置为有效值（大于 0），则 `tiflash_fine_grained_shuffle_stream_count` 设置为 [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610) 的值。否则，它会根据 TiFlash 计算节点的 CPU 资源自动估算。TiFlash 上窗口函数的实际并发级别为：min(`tiflash_fine_grained_shuffle_stream_count`，TiFlash 节点上的物理线程数)。
    * 大于 0 的整数：启用 Fine Grained Shuffle 功能。下推到 TiFlash 的窗口函数在多个线程中执行。并发级别为：min(`tiflash_fine_grained_shuffle_stream_count`，TiFlash 节点上的物理线程数)。
- 理论上，窗口函数的性能会随着此值的增加而线性增长。但是，如果该值超过实际的物理线程数，反而会导致性能下降。

### tiflash_mem_quota_query_per_node <span class="version-mark">v7.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[-1, 9223372036854775807]`
- 此变量限制了 TiFlash 节点上查询的最大内存使用量。当查询的内存使用量超过此限制时，TiFlash 会返回错误并终止查询。将此变量设置为 `-1` 或 `0` 表示没有限制。当此变量设置为大于 `0` 的值，并且 [`tiflash_query_spill_ratio`](/system-variables.md#tiflash_query_spill_ratio-new-in-v740) 设置为有效值时，TiFlash 会启用 [查询级别的溢写](/tiflash/tiflash-spill-disk.md#query-level-spilling)。

### tiflash_query_spill_ratio <span class="version-mark">v7.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Float
- 默认值：`0.7`
- 范围：`[0, 0.85]`
- 此变量控制 TiFlash [查询级别溢写](/tiflash/tiflash-spill-disk.md#query-level-spilling) 的阈值。`0` 表示禁用自动查询级别溢写。当此变量大于 `0` 且查询的内存使用量超过 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) * `tiflash_query_spill_ratio` 时，TiFlash 会触发查询级别的溢写，根据需要溢写查询中支持的算子的数据。

> **注意：**
>
> - 此变量仅在 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) 大于 `0` 时生效。换句话说，如果 [tiflash_mem_quota_query_per_node](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) 为 `0` 或 `-1`，即使 `tiflash_query_spill_ratio` 大于 `0`，也不会启用查询级别的溢写。
> - 启用 TiFlash 查询级别溢写后，各个 TiFlash 算子的溢写阈值会自动失效。换句话说，如果 [`tiflash_mem_quota_query_per_node`](/system-variables.md#tiflash_mem_quota_query_per_node-new-in-v740) 和 `tiflash_query_spill_ratio` 都大于 0，则三个变量 [tidb_max_bytes_before_tiflash_external_sort](/system-variables.md#tidb_max_bytes_before_tiflash_external_sort-new-in-v700)、[tidb_max_bytes_before_tiflash_external_group_by](/system-variables.md#tidb_max_bytes_before_tiflash_external_group_by-new-in-v700) 和 [tidb_max_bytes_before_tiflash_external_join](/system-variables.md#tidb_max_bytes_before_tiflash_external_join-new-in-v700) 会自动失效，相当于将它们设置为 `0`。

### tiflash_replica_read <span class="version-mark">v7.3.0 新增</span>

> **注意：**
>
> 此 TiDB 变量不适用于 TiDB Cloud。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`all_replicas`
- 可选值：`all_replicas`、`closest_adaptive` 或 `closest_replicas`
- 此变量用于设置查询需要 TiFlash 引擎时选择 TiFlash 副本的策略。
    - `all_replicas` 表示使用所有可用的 TiFlash 副本进行分析计算。
    - `closest_adaptive` 表示优先使用与发起查询的 TiDB 节点位于同一区域的 TiFlash 副本。如果此区域中的副本不包含所有必需的数据，则查询将涉及来自其他区域的 TiFlash 副本及其相应的 TiFlash 节点。
    - `closest_replicas` 表示仅使用与发起查询的 TiDB 节点位于同一区域的 TiFlash 副本。如果此区域中的副本不包含所有必需的数据，则查询将返回错误。

<CustomContent platform="tidb">

> **注意：**
>
> - 如果 TiDB 节点未配置 [区域属性](/schedule-replicas-by-topology-labels.md#optional-configure-labels-for-tidb) 且 `tiflash_replica_read` 未设置为 `all_replicas`，则 TiFlash 将忽略副本选择策略。相反，它将使用所有 TiFlash 副本进行查询并返回 `The variable tiflash_replica_read is ignored.` 警告。
> - 如果 TiFlash 节点未配置 [区域属性](/schedule-replicas-by-topology-labels.md#configure-labels-for-tikv-and-tiflash)，则它们被视为不属于任何区域的节点。

</CustomContent>

### tikv_client_read_timeout <span class="version-mark">v7.4.0 新增</span>

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 Hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 单位：毫秒
- 您可以使用 `tikv_client_read_timeout` 设置 TiDB 在查询中发送 TiKV RPC 读取请求的超时时间。当 TiDB 集群处于网络不稳定或 TiKV I/O 延迟抖动严重的环境中，并且您的应用程序对 SQL 查询的延迟敏感时，您可以设置 `tikv_client_read_timeout` 以减少 TiKV RPC 读取请求的超时时间。在这种情况下，当 TiKV 节点出现 I/O 延迟抖动时，TiDB 可以快速超时并将 RPC 请求重新发送到下一个 TiKV Region Peer 所在的 TiKV 节点。如果所有 TiKV Region Peer 的请求都超时，TiDB 将使用默认超时时间（通常为 40 秒）重试。
- 你也可以在查询中使用优化器提示 `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=N) */` 来设置 TiDB 向 TiKV 发送 RPC 读取请求的超时时间。如果同时设置了优化器提示和此系统变量，则优化器提示的优先级更高。
- 默认值 `0` 表示使用默认超时时间（通常为 40 秒）。

> **注意：**
>
> - 通常，一个常规查询只需要几毫秒，但偶尔当 TiKV 节点处于不稳定的网络或出现 I/O 抖动时，查询可能需要超过 1 秒甚至 10 秒。在这种情况下，你可以使用优化器提示 `/*+ SET_VAR(TIKV_CLIENT_READ_TIMEOUT=100) */` 为特定查询设置 TiKV RPC 读取请求超时时间为 100 毫秒。这样，即使 TiKV 节点的响应速度很慢，TiDB 也可以快速超时，然后将 RPC 请求重新发送到下一个 TiKV Region Peer 所在的 TiKV 节点。由于两个 TiKV 节点同时出现 I/O 抖动的概率很低，因此查询通常可以在几毫秒到 110 毫秒内完成。
> - 不要为 `tikv_client_read_timeout` 设置太小的值（例如，1 毫秒）。否则，当 TiDB 集群的工作负载很高时，请求可能很容易超时，随后的重试会进一步增加 TiDB 集群的负载。
> - 如果需要为不同类型的查询设置不同的超时值，建议使用优化器提示。

### time_zone

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`SYSTEM`
- 此变量返回当前时区。值可以指定为偏移量，例如 '-8:00'，或者指定为命名时区，例如 'America/Los_Angeles'。
- 值 `SYSTEM` 表示时区应与系统主机相同，可通过 [`system_time_zone`](#system_time_zone) 变量获得。

### timestamp

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Float
- 默认值：`0`
- 范围：`[0, 2147483647]`
- 此变量的非空值表示用作 `CURRENT_TIMESTAMP()`、`NOW()` 和其他函数的时间戳的 UNIX epoch。此变量可能用于数据恢复或复制。

### transaction_isolation

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：枚举
- 默认值：`REPEATABLE-READ`
- 可选值：`READ-UNCOMMITTED`、`READ-COMMITTED`、`REPEATABLE-READ`、`SERIALIZABLE`
- 此变量设置事务隔离级别。TiDB 声明 `REPEATABLE-READ` 是为了与 MySQL 兼容，但实际的隔离级别是快照隔离。有关更多详细信息，请参阅[事务隔离级别](/transaction-isolation-levels.md)。

### tx_isolation

此变量是 `transaction_isolation` 的别名。

### tx_isolation_one_shot

> **注意：**
>
> 此变量在 TiDB 内部使用。不建议你使用它。

在内部，TiDB 解析器将 `SET TRANSACTION ISOLATION LEVEL [READ COMMITTED| REPEATABLE READ | ...]` 语句转换为 `SET @@SESSION.TX_ISOLATION_ONE_SHOT = [READ COMMITTED| REPEATABLE READ | ...]`。

### tx_read_ts

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：""
- 在 Stale Read 场景中，此会话变量用于帮助记录 Stable Read 时间戳值。
- 此变量用于 TiDB 的内部操作。**不建议**设置此变量。

### txn_scope

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`global`
- 可选值：`global` 和 `local`
- 此变量用于设置当前会话事务是全局事务还是本地事务。
- 此变量用于 TiDB 的内部操作。**不建议**设置此变量。

### validate_password.check_user_name <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`ON`
- 类型：Boolean
- 此变量是密码复杂度检查中的一个检查项。它检查密码是否与用户名匹配。此变量仅在启用 [`validate_password.enable`](#validate_passwordenable-new-in-v650) 时生效。
- 当此变量生效并设置为 `ON` 时，如果你设置密码，TiDB 会将密码与用户名（不包括主机名）进行比较。如果密码与用户名匹配，则密码将被拒绝。
- 此变量独立于 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650)，不受密码复杂度检查级别的限制。

### validate_password.dictionary <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`""`
- 类型：String
- 此变量是密码复杂度检查中的一个检查项。它检查密码是否与字典匹配。此变量仅在启用 [`validate_password.enable`](#validate_passwordenable-new-in-v650) 且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设置为 `2` (STRONG) 时生效。
- 此变量是一个不超过 1024 个字符的字符串。它包含一个密码中不能存在的单词列表。每个单词用分号 (`;`) 分隔。
- 默认情况下，此变量设置为空字符串，这意味着不执行字典检查。要执行字典检查，你需要将要匹配的单词包含在字符串中。如果配置了此变量，当你设置密码时，TiDB 会将密码的每个子字符串（长度为 4 到 100 个字符）与字典中的单词进行比较。如果密码的任何子字符串与字典中的单词匹配，则密码将被拒绝。比较不区分大小写。

### validate_password.enable <span class="version-mark">v6.5.0 新增</span>

> **注意：**
>
> 此变量始终为 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 启用。

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`OFF`
- 类型：Boolean
- 此变量控制是否执行密码复杂度检查。如果此变量设置为 `ON`，则在设置密码时，TiDB 会执行密码复杂度检查。

### validate_password.length <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`8`
- 范围：对于 TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `[8, 2147483647]`
- 此变量是密码复杂度检查中的一个检查项。它检查密码长度是否足够。默认情况下，最小密码长度为 `8`。此变量仅在启用 [`validate_password.enable`](#validate_passwordenable-new-in-v650) 时生效。
- 此变量的值不得小于表达式：`validate_password.number_count + validate_password.special_char_count + (2 * validate_password.mixed_case_count)`。
- 如果你修改了 `validate_password.number_count`、`validate_password.special_char_count` 或 `validate_password.mixed_case_count` 的值，使得表达式的值大于 `validate_password.length`，那么 `validate_password.length` 的值会自动更改以匹配表达式的值。

### validate_password.mixed_case_count <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `[1, 2147483647]`
- 此变量是密码复杂度检查中的一个检查项。它检查密码是否包含足够的大写和小写字母。此变量仅在启用 [`validate_password.enable`](#validate_passwordenable-new-in-v650) 且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设置为 `1` (MEDIUM) 或更大时生效。
- 密码中的大写字母数量和小写字母数量都不能少于 `validate_password.mixed_case_count` 的值。例如，当该变量设置为 `1` 时，密码必须至少包含一个大写字母和一个小写字母。

### validate_password.number_count <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `[1, 2147483647]`
- 此变量是密码复杂度检查中的一个检查项。它检查密码是否包含足够的数字。此变量仅在启用 [`validate_password.enable`](#password_reuse_interval-new-in-v650) 且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设置为 `1` (MEDIUM) 或更大时生效。

### validate_password.policy <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Enumeration
- 默认值：`1`
- 可选值：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `0`、`1` 和 `2`；[TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `1` 和 `2`
- 此变量控制密码复杂度检查的策略。此变量仅在启用 [`validate_password.enable`](#password_reuse_interval-new-in-v650) 时生效。此变量的值决定了除了 `validate_password.check_user_name` 之外，其他 `validate-password` 变量是否在密码复杂度检查中生效。
- 此变量的值可以是 `0`、`1` 或 `2`（分别对应于 LOW、MEDIUM 或 STRONG）。不同的策略级别有不同的检查：
    - 0 或 LOW：密码长度。
    - 1 或 MEDIUM：密码长度、大写和小写字母、数字和特殊字符。
    - 2 或 STRONG：密码长度、大写和小写字母、数字、特殊字符和字典匹配。

### validate_password.special_char_count <span class="version-mark">v6.5.0 新增</span>

- 作用域：GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`1`
- 范围：TiDB Self-Managed 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 为 `[0, 2147483647]`，[TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 为 `[1, 2147483647]`
- 此变量是密码复杂度检查中的一个检查项。它检查密码是否包含足够的特殊字符。此变量仅在启用 [`validate_password.enable`](#password_reuse_interval-new-in-v650) 且 [`validate_password.policy`](#validate_passwordpolicy-new-in-v650) 设置为 `1` (MEDIUM) 或更大时生效。

### version

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`8.0.11-TiDB-`(tidb 版本)
- 此变量返回 MySQL 版本，后跟 TiDB 版本。例如 '8.0.11-TiDB-v8.1.2'。

### version_comment

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：(string)
- 此变量返回有关 TiDB 版本的其他详细信息。例如，'TiDB Server (Apache License 2.0) Community Edition, MySQL 8.0 compatible'。

### version_compile_machine

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：(string)
- 此变量返回 TiDB 运行所在的 CPU 架构的名称。

### version_compile_os

- 作用域：NONE
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：(string)
- 此变量返回 TiDB 运行所在的 OS 的名称。

### wait_timeout

> **注意：**
>
> 此变量对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 是只读的。

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Integer
- 默认值：`28800`
- 范围：`[0, 31536000]`
- 单位：秒
- 此变量控制用户会话的空闲超时。零值表示无限制。

### warning_count

- 作用域：SESSION
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 默认值：`0`
- 此只读变量指示先前执行的语句中发生的警告数量。

### windowing_use_high_precision

- 作用域：SESSION | GLOBAL
- 是否持久化到集群：是
- 是否适用于 hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value)：否
- 类型：Boolean
- 默认值：`ON`
- 此变量控制在计算 [窗口函数](/functions-and-operators/window-functions.md) 时是否使用高精度模式。
