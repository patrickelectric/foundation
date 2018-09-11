#!/bin/bash
PROG=$(basename $0)

error() {
    echo -e "ERROR: $*" >&2
    exit 1
}

usage() {
    echo "USAGE: $PROG 000000 or $PROG 00,00,00"
}

if [[ $# -eq 1 ]]; then
    COLOR="$1"
else
    usage && error "Incorrect number of arguments: $#"
fi

# Check if value is r,g,b (int)
RGB=$(echo $COLOR | grep -oP "\d{1,3},\d{1,3},\d{1,3}")

# If is r,g,b (int) transform it to hexadecimal value and format #RRGGBB
if [[ $RGB != "" ]]; then
    COLOR=""
    for i in $(echo $RGB | tr "," "\n"); do
        COLOR="$COLOR$(echo "obase=16; $i" | bc | awk '{printf("%02s", $1)}')"
    done
    COLOR=${COLOR// /0}
fi

echo "Search for color: #$COLOR"
curl -s --compressed https://api.color.pizza/v1/${COLOR} |  python -m json.tool