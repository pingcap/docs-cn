# Build

## Supported platforms

The following table lists TiDB support for common architectures and operating systems. 

|Architecture|Operating System|Status|
|------------|----------------|------|
|amd64|Linux Ubuntu (14.04+)|Stable|
|amd64|Linux CentOS (7+)|Stable|
|amd64|Mac OSX|Experimental|

## Prerequisites

+ Go [1.5+](https://golang.org/doc/install)
+ Rust [nightly version](https://www.rust-lang.org/downloads.html)
+ GCC 4.8+ with static library

### Install GO

#### Linux

```bash
curl -L https://storage.googleapis.com/golang/go1.6.3.linux-amd64.tar.gz -o golang.tar.gz
tar -C /usr/local -xzf golang.tar.gz
```

#### Mac OS X

```bash
curl -L https://storage.googleapis.com/golang/go1.6.3.darwin-amd64.tar.gz -o golang.tar.gz
tar -C /usr/local -xzf golang.tar.gz
```

### Install Rust

```bash
curl -sSf https://static.rust-lang.org/rustup.sh | sh -s -- --channel=nightly
```

### Install GCC

#### Linux Ubuntu

```bash
apt-get update
apt-get install -y gcc g++
```

#### Linux CentOS

```bash
yum install -y gcc-c++ glibc-static libstdc++-static
```

#### Mac OS X

```bash
xcode-select --install
brew update
brew tap homebrew/versions
brew install gcc48 --use-llvm
```

## Build TiDB project

```
# Create a root path for building and installing TiDB. 
mkdir -p /Users/tidb
export TIDB_PATH=/Users/tidb
# All the binaries are installed in the `bin` directory. 
mkdir -p $TIDB_PATH/bin
```

### Build TiDB

```bash
# go is required
go version
# go version go1.6 darwin/amd64

# GOPATH should be set correctly.
export GOPATH=$TIDB_PATH/go

git clone https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
cd $GOPATH/src/github.com/pingcap/tidb

make server
cp -f ./tidb-server/tidb-server $TIDB_PATH/bin
cd $TIDB_PATH
```

### Build PD

```bash
export GOPATH=$TIDB_PATH/go

git clone https://github.com/pingcap/pd.git $GOPATH/src/github.com/pingcap/pd
cd $GOPATH/src/github.com/pingcap/pd

make build
cp -f ./bin/pd-server $TIDB_PATH/bin
cd $TIDB_PATH
```

### Build TiKV

```bash
# rust nightly is required
rustc -V
# rustc 1.12.0-nightly (7ad125c4e 2016-07-11)

git clone https://github.com/pingcap/tikv.git $TIDB_PATH/tikv
cd $TIDB_PATH/tikv

ROCKSDB_SYS_STATIC=1 make release
cp -f ./target/release/tikv-server $TIDB_PATH/bin
cd $TIDB_PATH
```

## Build Portable TiDB project

You can copy the binary executions to other machines and run them directly, but `tikv-server` may fail to start, you may meet following conditions:

+ Missing `stdc++` library. You can install g++ in your machine or link static c++ library directly when building TiKV, for example:

    ```bash
    ROCKSDB_SYS_STATIC=1 ROCKSDB_OTHER_STATIC=stdc++ ROCKSDB_OTHER_STATIC_PATH=/usr/lib/gcc/x86_64-linux-gnu/4.8/ make release 
    ```
    
    If you want to link static c++ directly, you must explicitly set c++ library path.

+ Panic because of different platform. Building RocksDB is optimized for native platform you're compiling by default, but if you want to use this in another different platform, you must explicitly set portable, for example:

    ```bash
    ROCKSDB_SYS_STATIC=1 ROCKSDB_SYS_PORTABLE=1 make release
    ```
    
If you want to run `tikv-server` in different platforms and don't want to install g++, you can do

```bash
ROCKSDB_SYS_STATIC=1 ROCKSDB_OTHER_STATIC=stdc++ ROCKSDB_OTHER_STATIC_PATH=/usr/lib/gcc/x86_64-linux-gnu/4.8/ make release 
```


