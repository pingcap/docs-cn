# Build For Development

## Overview

If you want to develop the TiDB project, you can follow this guide.

Before you begin, check the [supported platforms](../dev-guide/requirements.md#supported-platforms) and [prerequisites](../dev-guide/requirements.md#prerequisites) first.

## Build TiKV

+ Get TiKV source code from GitHub

    ```bash
    git clone https://github.com/pingcap/tikv.git 
    cd tikv
    ```

+ Run all unit tests:

    ```bash
    make test
    ```

+ Build in release mode:

    ```bash
    make release
    ```

## Build TiDB

+ Make sure the GOPATH environment is set correctly.

+ Get the TiDB source code.

    ```bash
    git clone https://github.com/pingcap/tidb.git $GOPATH/src/github.com/pingcap/tidb
    ```
    
+ Enter `$GOPATH/src/github.com/pingcap/tidb` to build and install the binary in the `bin` directory.

    ```bash
    make
    ```
+ Run unit test.
    
    ```bash
    make test
    ```

## Build PD

+ Get the PD source code.

    ```bash
    git clone https://github.com/pingcap/pd.git $GOPATH/src/github.com/pingcap/pd
    ```
    
+ Enter `$GOPATH/src/github.com/pingcap/pd` to build and install the binary in the `bin` directory.

    ```bash
    make
    ```
+ Run unit test.
    
    ```bash
    make test
    ```
