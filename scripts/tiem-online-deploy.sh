#!/bin/bash

# Prerequisite:
# 1. Install TiUP as root
    # Example command:
    # curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
# 2. Prepare an EM deployment topology yaml to /opt/config.yaml
# 3. Put current script in /root/ path of EM machine and run it as root privilege, and leave the rest to the script.
    # Example command:
    # sh online_install.sh http://172.16.5.148:8080/tiup-repo/ /opt/config.yaml

if [ $# -ne 2 ]
then
    echo "usage: $0 <online-repo-path> <em-deployment-topology-path>"
    exit
fi

EM_REPO_MIRROR_PATH=$1
EM_DEPLOYMENT_TOPO=$2

echo "##### assign privileges for deployment topology file to all users started #####"
chmod 777 $EM_DEPLOYMENT_TOPO
echo "##### assign privileges for deployment topology file to all users finished #####"

echo "##### add user tidb started #####"
useradd tidb
echo "##### add user tidb finished #####"

echo "##### install TiUP to /usr/local/bin/ started #####"
install -Dm755 ~/.tiup/bin/tiup /usr/local/bin/
echo "##### install TiUP to /usr/local/bin/ finished #####"

su - tidb << EOF

echo "##### mkdir & set mirror for EM installer started #####"
mkdir -p /home/tidb/.em/bin
TIUP_HOME=/home/tidb/.em tiup mirror set $EM_REPO_MIRROR_PATH
echo "##### mkdir & set mirror for EM installer finished #####"

echo "##### mkdir & set mirror for TiDB installer started #####"
mkdir -p /home/tidb/.tiup/bin
TIUP_HOME=/home/tidb/.tiup tiup mirror set https://tiup-mirrors.pingcap.com
echo "##### mkdir & set mirror for TiDB installer finished #####"


EOF

echo "##### mkdir & set mirror for TiDB installer finished #####"


EOF

echo "##### generate identity key started, simply press enter or respond yes if needed #####"
su - tidb -c "ssh-keygen -t rsa"
su - tidb -c "cp /home/tidb/.ssh/id_rsa /home/tidb/.ssh/tiup_rsa"

echo "##### generate identity key finished #####"

echo "##### deploy EM started, you may need to provide password for central machine and respond yes if needed #####"
su - tidb -c "TIUP_HOME=/home/tidb/.em tiup em deploy em-test $VERSION $EM_DEPLOYMENT_TOPO -u root -p"
su - tidb -c "TIUP_HOME=/home/tidb/.em tiup em start em-test"
echo "##### deploy EM finished #####"
