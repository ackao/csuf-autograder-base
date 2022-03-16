#!/bin/bash

mv /bin/uname /bin/uname.orig
printf '#!/bin/bash\n\nif [[ "$1" == "-r" ]] ;then\n echo '4.9.250'\n exit\nelse\n uname.orig "$@"\nfi' > /bin/uname
chmod 755 /bin/uname

apt-get update
apt-get install -y gcc
apt-get install -y cmake libgtest-dev
apt-get install -y clang clang-tidy clang-format
apt-get install -y python3 python3-pip
pip3 install pyyaml
mkdir /usr/tmp && cd /usr/tmp && cmake /usr/src/googletest && make install && rm -rf /usr/tmp
