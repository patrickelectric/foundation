#!/usr/bin/env bash
# Get an human friendly list of names of the check that are failing
keys=( $(pylint $(git ls-files '*.py') | rg '.*py:\d+:\d+: (.*):.*' -r '$1' | sort | uniq) )
msgs=( $(pylint --list-msgs | rg ":(.*) \(([A-Z]\d+)\).*" -r '$1,$2' | sort) )

for msg in "${msgs[@]}"; do
    for key in "${keys[@]}"; do
        if [[ $msg == *"$key" ]]; then
            echo "${msg::-5}"
        fi
    done
done
