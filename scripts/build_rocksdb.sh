#!/bin/bash

set -e

# Use current path for building and installing RocksDB. 
TIDB_PATH=`pwd`
DEPS_PATH=${TIDB_PATH}/deps
echo "building RocksDB in $DEPS_PATH"

mkdir -p ${DEPS_PATH}
cd $DEPS_PATH

ROCKSDB_VER=v5.1.2

SUDO=
if which sudo; then 
    SUDO=sudo
fi

function get_linux_platform {
    if [ -f /etc/redhat-release ]; then 
        # For CentOS or redhat, we treat all as CentOS.
        echo "CentOS"
    elif [ -f /etc/lsb-release ]; then
        DIST=`cat /etc/lsb-release | grep '^DISTRIB_ID' | awk -F=  '{ print $2 }'`
        echo "$DIST"
    else
        echo "Unknown"
    fi 
}

function install_in_ubuntu {
    echo "building RocksDB in Ubuntu..."
    if [ ! -d rocksdb-${ROCKSDB_VER} ]; then
        ${SUDO} apt-get update 
        ${SUDO} apt-get install -y --no-install-recommends zlib1g-dev libbz2-dev libsnappy-dev libgflags-dev liblz4-dev 
        curl -L https://github.com/facebook/rocksdb/archive/${ROCKSDB_VER}.tar.gz -o rocksdb.tar.gz 
        tar xf rocksdb.tar.gz 
    fi
    
    cd rocksdb-${ROCKSDB_VER} 
    make shared_lib 
    ${SUDO} make install-shared 
    # guarantee tikv can find rocksdb.
    ${SUDO} ldconfig
}

function install_in_centos {
    echo "building RocksDB in CentOS..."
    if [ ! -d rocksdb-${ROCKSDB_VER} ]; then
        ${SUDO} yum install -y epel-release
        ${SUDO} yum install -y snappy-devel zlib-devel bzip2-devel lz4-devel
        curl -L https://github.com/facebook/rocksdb/archive/${ROCKSDB_VER}.tar.gz -o rocksdb.tar.gz 
        tar xf rocksdb.tar.gz 
    fi
    
    cd rocksdb-${ROCKSDB_VER} 
    make shared_lib 
    ${SUDO} make install-shared 
    # guarantee tikv can find rocksdb.
    ${SUDO} ldconfig
}

function install_in_macosx {
    echo "building RocksDB in Mac OS X..."
    if [ ! -d rocksdb-${ROCKSDB_VER} ]; then
        brew=$(which brew 2>/dev/null) || true
        if [ -n "$brew" ]; then
            brew update
            brew install lz4 || true
            brew install snappy || true
        else
            # note: macports do allow you to do port install rocksdb
            port=$(which port 2>/dev/null) || true
            if [ -n "$port" ]; then
                $SUDO port selfupdate
                $SUDO port install lz4 || true
                $SUDO port install snappy || true
            fi
        fi
        curl -L https://github.com/facebook/rocksdb/archive/${ROCKSDB_VER}.tar.gz -o rocksdb.tar.gz 
        tar xf rocksdb.tar.gz 
    fi
    
    cd rocksdb-${ROCKSDB_VER} 
    make shared_lib 
    ${SUDO} make install-shared
}

case "$OSTYPE" in 
    linux*) 
        dist=$(get_linux_platform)
        case $dist in
            Ubuntu)
                install_in_ubuntu
            ;;
            CentOS)
                install_in_centos
            ;;
            *)
                echo "unsupported platform $dist, you may install RocksDB manually"
                exit 0
            ;;
        esac
    ;;
    darwin*) 
        install_in_macosx
    ;;
    *) 
        echo "unsupported $OSTYPE"
        exit 1
    ;;
esac

cd ${TIDB_PATH}
echo "building RocksDB OK"
