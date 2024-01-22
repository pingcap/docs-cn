---
title: 客户端连接参数
summary: 介绍客户端连接参数。
---

# 客户端连接参数

<!--TODO: 针对 TiDB 适配的 [MySQL 5.7 Client Options](https://dev.mysql.com/doc/refman/8.0/en/mysql-command-options.html) 需逐个检验命令行参数是否符合预期。-->

|            参数名称            |                                       描述                                        | 是否符合预期 | 验证版本 |
| :----------------------------: | :-------------------------------------------------------------------------------: | :----------: | :------: |
|         --auto-rehash          |                            Enable automatic rehashing                             |
|     --auto-vertical-output     |                   Enable automatic vertical result set display                    |
|            --batch             |                              Do not use history file                              |
|        --binary-as-hex         |                   Display binary values in hexadecimal notation                   |
|         --binary-mode          |      Disable \r\n - to - \n translation and treatment of \0 as end-of-query       |
|         --bind-address         |            Use specified network interface to connect to MySQL Server             |
|      --character-sets-dir      |                   Directory where character sets are installed                    |
|         --column-names         |                           Write column names in results                           |
|       --column-type-info       |                            Display result set metadata                            |
|           --comments           |       Whether to retain or strip comments in statements sent to the server        |
|           --compress           |              Compress all information sent between client and server              |
|   --connect-expired-password   |      Indicate to server that client can handle expired-password sandbox mode      |
|       --connect-timeout        |                    Number of seconds before connection timeout                    |
|           --database           |                                The database to use                                |
|            --debug             |   Write debugging log; supported only if MySQL was built with debugging support   |
|         --debug-check          |                  Print debugging information when program exits                   |
|          --debug-info          |    Print debugging information, memory, and CPU statistics when program exits     |
|         --default-auth         |                           Authentication plugin to use                            |
|    --default-character-set     |                           Specify default character set                           |
|     --defaults-extra-file      |             Read named option file in addition to usual option files              |
|        --defaults-file         |                            Read only named option file                            |
|    --defaults-group-suffix     |                             Option group suffix value                             |
|          --delimiter           |                            Set the statement delimiter                            |
|   --enable-cleartext-plugin    |                      Enable cleartext authentication plugin                       |
|           --execute            |                          Execute the statement and quit                           |
|            --force             |                       Continue even if an SQL error occurs                        |
|    --get-server-public-key     |                        Request RSA public key from server                         |
|             --help             |                           Display help message and exit                           |
|          --histignore          |            Patterns specifying which statements to ignore for logging             |
|             --host             |                       Host on which MySQL server is located                       |
|             --html             |                                Produce HTML output                                |
|        --ignore-spaces         |                        Ignore spaces after function names                         |
|         --init-command         |                     SQL statement to execute after connecting                     |
|         --line-numbers         |                           Write line numbers for errors                           |
|         --local-infile         |               Enable or disable for LOCAL capability for LOAD DATA                |
|          --login-path          |                     Read login path options from .mylogin.cnf                     |
|      --max-allowed-packet      |              Maximum packet length to send to or receive from server              |
|        --max-join-size         |         The automatic limit for rows in a join when using --safe-updates          |
|        --named-commands        |                            Enable named mysql commands                            |
|      --net-buffer-length       |                  Buffer size for TCP/IP and socket communication                  |
|        --no-auto-rehash        |                            Disable automatic rehashing                            |
|           --no-beep            |                           Do not beep when errors occur                           |
|         --no-defaults          |                               Read no option files                                |
|         --one-database         | Ignore statements except those for the default database named on the command line |
|            --pager             |                   Use the given command for paging query output                   |
|           --password           |                     Password to use when connecting to server                     |
|             --pipe             |                 Connect to server using named pipe (Windows only)                 |
|          --plugin-dir          |                       Directory where plugins are installed                       |
|             --port             |                         TCP/IP port number for connection                         |
|        --print-defaults        |                               Print default options                               |
|            --prompt            |                      Set the prompt to the specified format                       |
|           --protocol           |                             Transport protocol to use                             |
|            --quick             |                          Do not cache each query result                           |
|             --raw              |                   Write column values without escape conversion                   |
|          --reconnect           |      If the connection to the server is lost, automatically try to reconnect      |
| --safe-updates, --i-am-a-dummy |          Allow only UPDATE and DELETE statements that specify key values          |
|         --secure-auth          |              Do not send passwords to server in old (pre-4.1) format              |
|         --select-limit         |        The automatic limit for SELECT statements when using --safe-updates        |
|    --server-public-key-path    |                    Path name to file containing RSA public key                    |
|   --shared-memory-base-name    |          Shared-memory name for shared-memory connections (Windows only)          |
|        --show-warnings         |                Show warnings after each statement if there are any                |
|        --sigint-ignore         |         Ignore SIGINT signals (typically the result of typing Control+C)          |
|            --silent            |                                    Silent mode                                    |
|       --skip-auto-rehash       |                            Disable automatic rehashing                            |
|      --skip-column-names       |                       Do not write column names in results                        |
|      --skip-line-numbers       |                           Skip line numbers for errors                            |
|     --skip-named-commands      |                           Disable named mysql commands                            |
|          --skip-pager          |                                  Disable paging                                   |
|        --skip-reconnect        |                               Disable reconnecting                                |
|            --socket            |                   Unix socket file or Windows named pipe to use                   |
|             --ssl              |                           Enable connection encryption                            |
|            --ssl-ca            |          File that contains list of trusted SSL Certificate Authorities           |
|          --ssl-capath          |    Directory that contains trusted SSL Certificate Authority certificate files    |
|           --ssl-cert           |                       File that contains X.509 certificate                        |
|          --ssl-cipher          |                   Permissible ciphers for connection encryption                   |
|           --ssl-crl            |                  File that contains certificate revocation lists                  |
|         --ssl-crlpath          |             Directory that contains certificate revocation-list files             |
|           --ssl-key            |                           File that contains X.509 key                            |
|           --ssl-mode           |                  Desired security state of connection to server                   |
|    --ssl-verify-server-cert    |         Verify host name against server certificate Common Name identity          |
|            --syslog            |                       Log interactive statements to syslog                        |
|            --table             |                         Display output in tabular format                          |
|             --tee              |                       Append a copy of output to named file                       |
|         --tls-version          |                Permissible TLS protocols for encrypted connections                |
|          --unbuffered          |                         Flush the buffer after each query                         |
|             --user             |                 MySQL user name to use when connecting to server                  |
|           --verbose            |                                   Verbose mode                                    |
|           --version            |                       Display version information and exit                        |
|           --vertical           |          Print query output rows vertically (one line per column value)           |
|             --wait             |    If the connection cannot be established, wait and retry instead of aborting    |
|             --xml              |                                Produce XML output                                 |
