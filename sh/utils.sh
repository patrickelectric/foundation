BOLD=$(tput bold)
NORMAL=$(tput sgr0)
# Generate random output file
VERBOSE_OUTPUT="/tmp/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 12 | head -n 1).txt"

# echob "message"
echob() {
    echo "${BOLD}${1}${NORMAL}"
}

# printfb "message"
printfb() {
    printf "${BOLD}${1}${NORMAL}"
}

# error "message"
error() {
    echo -e "ERROR: $*" >&2
    exit 1
}

# checktool 'command'
# checktool 'command' name "erro message"
checktool() {
    name=""
    errormsg=""
    if (( $# > 1 )); then
        name=$2
        if (( $# >= 3 )); then
            errormsg=$3
        fi
    else
        name=($1)
    fi
    printfb "$name: "
    eval "$1" >>$VERBOSE_OUTPUT 2>&1

    [ $? == 0 ] || {
        echob "✖"
        cat $VERBOSE_OUTPUT
        error "$name is not available." $errormsg
    }
    echob "✔"
}

#runstep 'command' 'success message' 'error message'
runstep() {
    name=$1
    okmessage=$2
    errormsg=$3
    printfb "$okmessage: "
    eval "$1" >>$VERBOSE_OUTPUT 2>&1
    [ $? == 0 ] || {
        echob "✖"
        cat $VERBOSE_OUTPUT
        error "$name failed." $errormsg
    }
    echob "✔"
}
