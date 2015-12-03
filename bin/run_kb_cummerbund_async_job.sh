#!/bin/bash
script_dir=$(dirname "$(readlink -f "$0")")
export PYTHONPATH=$script_dir/../lib:$PATH:$PYTHONPATH
python $script_dir/../lib/kb_cummerbund/kb_cummerbundServer.py $1 $2 $3
