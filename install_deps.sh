#!/bin/bash

apt-get update
apt-get install -y gcc
apt-get install -y cmake
apt-get install -y clang clang-tidy clang-format libx11-dev
apt-get install -y python3 python3-pip
pip3 install pyyaml
cd /tmp/ && git clone https://github.com/google/googletest && cd googletest && mkdir build && cd build && cmake .. -DCMAKE_CXX_STANDARD=17 && make && make install && rm -rf /tmp/googletest
