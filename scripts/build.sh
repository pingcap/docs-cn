#!/bin/bash

set -e 

# Use current path for building and installing TiDB. 
TIDB_PATH=`pwd`
echo "building TiDB components in $TIDB_PATH"

# All the binaries are installed in the `bin` directory. 
mkdir -p $TIDB_PATH/bin

# Assume we install go in /usr/local/go
export PATH=$PATH:/usr/local/go/bin

echo "checking go is installed"
# go is required
go version 
# go version go1.6 darwin/amd64

echo "checking rust is installed"
# rust nightly is required
rustc -V
# rustc 1.12.0-nightly (7ad125c4e 2016-07-11)

# GOPATH should be set correctly.
export GOPATH=$TIDB_PATH/deps/go

# build TiDB
echo "building TiDB..."
rm -rf $GOPATH/src/github.com/pingcap/tidb
git clone --depth=1 https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
cd $GOPATH/src/github.com/pingcap/tidb

make server
cp -f ./tidb-server/tidb-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "build TiDB OK"

# build PD
echo "building PD..."
rm -rf $GOPATH/src/github.com/pingcap/pd
git clone --depth=1 https://github.com/pingcap/pd.git $GOPATH/src/github.com/pingcap/pd
cd $GOPATH/src/github.com/pingcap/pd

make build
cp -f ./bin/pd-server $TIDB_PATH/bin
cp -rf ./templates $TIDB_PATH/bin/templates
cd $TIDB_PATH
echo "build PD OK"

# build TiKV
echo "building TiKV..."
rm -rf $TIDB_PATH/deps/tikv
git clone --depth=1 https://github.com/pingcap/tikv.git $TIDB_PATH/deps/tikv
cd $TIDB_PATH/deps/tikv

ROCKSDB_SYS_STATIC=1 make release

cp -f ./target/release/tikv-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "build TiKV OK"