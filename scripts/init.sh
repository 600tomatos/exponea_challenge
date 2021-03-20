#!/bin/bash

ROOT_ABS_PATH="$(cd "$(dirname $(dirname "${BASH_SOURCE[0]}"))" >/dev/null && pwd)"

source $ROOT_ABS_PATH/scripts/common.sh

# Try to find python3.7 on local system
PYTHON_EXECUTOR=''

_python_ex=$(python3.7 --version)
_python3_ex=$(python3 --version)

if [[ $_python_ex == *"3.7"* ]]; then
  PYTHON_EXECUTOR=$(which python3.7)
elif [[  $_python3_ex == *"3.7"* ]]; then
 PYTHON_EXECUTOR=$(which python3)
fi

colored $GREEN "python executable have been found by path ${PYTHON_EXECUTOR} \n"


if [[ -d "${ROOT_ABS_PATH}/venv" ]]
then
    colored $GREEN "seems you've already installed all dependencies for your local env."
else
    colored $BLUE "Init new virtual env...\n"
    $PYTHON_EXECUTOR -m venv venv
    colored $BLUE "Virtual env activation...\n"
    source  $ROOT_ABS_PATH/venv/bin/activate
    colored $BLUE "Dependencies installation...\n"
    pip install -r $ROOT_ABS_PATH/src/requirements.txt
fi