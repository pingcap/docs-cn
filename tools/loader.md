---
title: Loader Instructions
category: advanced
---

# Loader instructions

## What is Loader?

Developed by PingCAP, Loader is a data import tool and it imports data to TiDB and MySQL.

[Source code](https://github.com/pingcap/tidb-tools/tree/master/loader)

[Download the Binary](http://download.pingcap.org/tidb-tools-latest-linux-amd64.tar.gz)

## Why did we develop Loader?

Since tools like mysqldump will take us days to migrate massive amounts of data, we used the mydumper/myloader suite of Percona to multi-thread export and import data. During the process, we found that mydumper works well. However, as myloader lacks functions of error retry and savepoint, it is inconvenient for us to use. Therefore, we developed loader, which reads the output data files of mydumper and imports data to TiDB/MySQL through mysql protocol.

## What can Loader do?

+ Multi-thread import data

+ Support mydumper data format

+ Support error retry

+ Support savepoint

+ Improve the speed of importing data through system variable

## Usage

### Parameter discription
```
  -L string: the log level setting. It can be set as debug, info, warn, error, fatal (default: "info")
  
  -P int: the port of TiDB/MySQL (default: 4000)
  
  -d string: the storage directory of data that need to import (default: "./")
  
  -h string: the host of TiDB/MySQL (default: "127.0.0.1")
  
  -checkpoint string: the file location of checkpoint. In the execution process, loader will constantly update this file. After recovering from an interruption, loader will get the process of the last run through this file. (default: "loader.checkpoint")
  
  -skip-unique-check: whether to skip the unique index check, 0 means no while 1 means yes (can improve the speed of importing data).
  Note: Only when you import data to TiDB can you open this option (default: 1)
  
  -p string: the account and password of TiDB/MySQL
  
  -pprof-addr string: the pprof address of Loader. It tunes the perfomance of Loader (default: ":10084")
  
  -q int: the number of insert statement that included in each transaction during the import process (default: 1. By default, the size of each insert statement of sql exported by mydumper is 1MB, including many rows of data.)
  
  -t int: the number of thread (default: 4)
  
  -u string: the user name of TiDB/MySQL (default: "root")
```

### Configuration file

Apart from command line parameters, you can also use configuration files. The format is shown as below:

```toml
# Loader log level
log-level = "info"

# Loader log file
log-file = ""

# Directory of the dump to import
dir = "./"

# Loader saved checkpoint
checkpoint = "loader.checkpoint"

# Loader pprof addr
pprof-addr = ":10084"

# Number of threads to use
worker = 4

# Number of queries per transcation
batch = 1

# Skip unique index check Note: If you don't import data to TiDB, please set this value to 0.
skip-unique-check = 1

# DB config
[db]
host = "127.0.0.1"
user = "root"
password = ""
port = 4000
```

### Usage

Command line parameter:

    ./bin/loader -d ./test -h 127.0.0.1 -u root -P 4000

Or use configuration file "config.toml":

    ./bin/loader -c=config.toml
    
### Note

If you use the default checkpoint file, after importing the data of a database, please delete loader.checkpoint before you begin to import the next database. When importing each database, explicitly specify the file name of checkpoint is recommended.
