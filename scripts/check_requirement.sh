#!/bin/bash

set -e

echo "Checking requirements..."

SUDO=
if which sudo &>/dev/null; then 
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

function install_go {
    echo "Intall go ..."
    case "$OSTYPE" in 
        linux*) 
            curl -L https://storage.googleapis.com/golang/go1.10.2.linux-amd64.tar.gz -o golang.tar.gz
            ${SUDO} tar -C /usr/local -xzf golang.tar.gz
            rm golang.tar.gz
        ;;

        darwin*)
            curl -L https://storage.googleapis.com/golang/go1.10.2.darwin-amd64.tar.gz -o golang.tar.gz
            ${SUDO} tar -C /usr/local -xzf golang.tar.gz
            rm golang.tar.gz
        ;;

        *)
            echo "unsupported $OSTYPE"
            exit 1
        ;;
    esac
}

function install_gpp {
    echo "Install g++ ..."
    case "$OSTYPE" in 
        linux*) 
            dist=$(get_linux_platform)
            case $dist in
                Ubuntu)
                    ${SUDO} apt-get install -y g++
                ;;
                CentOS)
                    ${SUDO} yum install -y gcc-c++ libstdc++-static
                ;;
                *)
                    echo "unsupported platform $dist, you may install g++ manually"
                    exit 1
                ;;
            esac
        ;;

        darwin*)
            # refer to https://github.com/facebook/rocksdb/blob/master/INSTALL.md
            xcode-select --install
            brew update
            brew tap homebrew/versions
            brew install gcc48 --use-llvm
        ;;

        *)
            echo "unsupported $OSTYPE"
            exit 1
        ;;
    esac
}

# Check rust
if which rustc &>/dev/null; then
    if ! rustc --version | grep nightly &>/dev/null; then
        printf "Please run following command to upgrade Rust to nightly: \n\
\t rustup install nightly\n\
\t rustup default nightly\n"
        exit 1
    fi
else
    echo "Install Rust ..."
    ${SUDO} curl https://sh.rustup.rs -sSf | sh
    ${SUDO} rustup install nightly
    ${SUDO} rustup default nightly
fi

# Check go
if which go &>/dev/null; then
    # requires go >= 1.8
    GO_VER_1=`go version | awk 'match($0, /([0-9])+(\.[0-9]+)+/) { ver = substr($0, RSTART, RLENGTH); split(ver, n, "."); print n[1];}'`
    GO_VER_2=`go version | awk 'match($0, /([0-9])+(\.[0-9]+)+/) { ver = substr($0, RSTART, RLENGTH); split(ver, n, "."); print n[2];}'`
    if [[ (($GO_VER_1 -eq 1 && $GO_VER_2 -lt 10)) || (($GO_VER_1 -lt 1)) ]]; then
        echo "Please upgrade Go to 1.10 or later."
        exit 1
    fi
else
    install_go
fi

# Check g++
if which g++ &>/dev/null; then
    #  Check g++ version, RocksDB requires g++ 4.8 or later.
    G_VER_1=`g++ -dumpversion | awk '{split($0, n, "."); print n[1];}'`
    G_VER_2=`g++ -dumpversion | awk '{split($0, n, "."); print n[2];}'`
    if [[ (($G_VER_1 -eq 4 && $G_VER_2 -lt 8)) || (($G_VER_1 -lt 4)) ]]; then
        echo "Please upgrade g++ to 4.8 or later."
        exit 1
    fi
else
    install_gpp
fi

echo OK
