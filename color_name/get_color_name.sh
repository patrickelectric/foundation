#!/bin/bash
PROG=$(basename $0)

error() {
    echo -e "ERROR: $*" >&2
    exit 1
}

usage() {
    echo "USAGE: $PROG 000000"
}

if [[ $# -eq 1 ]]; then
    COLOR="$1"
else
    usage && error "Incorrect number of arguments: $#"
fi

curl -s --compressed https://api.color.pizza/v1/${COLOR} |  python -m json.tool