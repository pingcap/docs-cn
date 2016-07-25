# Build

## Supported platforms

The following table lists TiDB support for common architectures and operating systems. 

|Architecture|Operating System|Status|
|------------|----------------|------|
|AMD64|Linux Ubuntu (14.04+)|Stable|
|AMD64|Linux CentOS (7+)|Stable|
|AMD64|Mac OSX|Experimental|

## Prerequisites

+ Go [1.5+](https://golang.org/doc/install)
+ Rust [nightly version](https://www.rust-lang.org/downloads.html)
+ GCC 4.8+ with static library

The [check requirement script](../scripts/check_requirement.sh) can help you check prerequisites and 
install the missing automatically.

## Build TiDB project

```
# Create a root path for building and installing TiDB. 
mkdir -p /Users/tidb
export TIDB_PATH=/Users/tidb
# All the binaries are installed in the `bin` directory. 
mkdir -p $TIDB_PATH/bin

# go is required
go version
# go version go1.6 darwin/amd64

# rust nightly is required
rustc -V
# rustc 1.12.0-nightly (7ad125c4e 2016-07-11)

# GOPATH should be set correctly.
export GOPATH=$TIDB_PATH/go

# build TiDB
git clone https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
cd $GOPATH/src/github.com/pingcap/tidb

make server
cp -f ./tidb-server/tidb-server $TIDB_PATH/bin
cd $TIDB_PATH

# build PD
git clone https://github.com/pingcap/pd.git $GOPATH/src/github.com/pingcap/pd
cd $GOPATH/src/github.com/pingcap/pd

make build
cp -f ./bin/pd-server $TIDB_PATH/bin
cd $TIDB_PATH

# build TiKV
git clone https://github.com/pingcap/tikv.git $TIDB_PATH/tikv
cd $TIDB_PATH/tikv

ROCKSDB_SYS_STATIC=1 make release

cp -f ./target/release/tikv-server $TIDB_PATH/bin
cd $TIDB_PATH
```