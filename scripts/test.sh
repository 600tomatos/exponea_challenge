#!/bin/bash

ROOT_ABS_PATH="$(cd "$(dirname $(dirname "${BASH_SOURCE[0]}"))" >/dev/null && pwd)"

source $ROOT_ABS_PATH/scripts/common.sh

if [ -z "$(sudo lsof -i -P -n | grep LISTEN | grep :5000)" ]; then
  read -d '' info <<EOF
  I just checked if the application is running on port 5000 and found out that the port is free.
   The tests require running a local server to communicate with it.
   Make sure to start the local server by running 'make run' before running the test.
EOF
  colored $RED "\n\n$info\n\n"
  sleep 2
fi

$(which bash) -c "python -m pytest -v"
