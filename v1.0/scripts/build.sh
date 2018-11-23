#!/bin/bash

set -e 

# Use current path for building and installing TiDB. 
TIDB_PATH=`pwd`
echo "building TiDB components in $TIDB_PATH"

# All the binaries are installed in the `bin` directory. 
mkdir -p $TIDB_PATH/bin

# Assume we install go in /usr/local/go
export PATH=$PATH:/usr/local/go/bin

echo "checking if go is installed"
# Go is required
go version 
# The output might be like: go version go1.6 darwin/amd64

echo "checking if rust is installed"
# Rust nightly is required
rustc -V
# The output might be like: rustc 1.12.0-nightly (7ad125c4e 2016-07-11)

# Set the GOPATH correctly.
export GOPATH=$TIDB_PATH/deps/go

# Build TiDB
echo "building TiDB..."
rm -rf $GOPATH/src/github.com/pingcap/tidb
git clone --depth=1 https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
cd $GOPATH/src/github.com/pingcap/tidb

make
cp -f ./bin/tidb-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "TiDB is built"

# Build PD
echo "building PD..."
rm -rf $GOPATH/src/github.com/pingcap/pd
git clone --depth=1 https://github.com/pingcap/pd.git $GOPATH/src/github.com/pingcap/pd
cd $GOPATH/src/github.com/pingcap/pd

make
cp -f ./bin/pd-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "PD is built"

# Build TiKV
echo "building TiKV..."
rm -rf $TIDB_PATH/deps/tikv
git clone --depth=1 https://github.com/pingcap/tikv.git $TIDB_PATH/deps/tikv
cd $TIDB_PATH/deps/tikv

make release

cp -f ./bin/tikv-server $TIDB_PATH/bin
cd $TIDB_PATH
echo "TiKV is built"
