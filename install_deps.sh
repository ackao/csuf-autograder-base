#!/bin/bash

apt-get update
apt-get install -y gcc
apt-get install -y cmake libgtest-dev libgmock-dev
apt-get install -y clang clang-tidy clang-format
apt-get install -y python3 python3-pip
pip3 install pyyaml
mkdir /usr/tmp && cd /usr/tmp && cmake /usr/src/googletest && make install && rm -rf /usr/tmp