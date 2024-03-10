#!/bin/bash

DATAFILE="./data/happiness.txt"
APPMAIN="./app/main.py"

rm -f "$DATAFILE.backup"
if [ -f "$DATAFILE" ]; then
    mv "$DATAFILE" "$DATAFILE.backup"
fi
$(which python3 || which pypy3 || which python || which pypy) "$APPMAIN" > "$DATAFILE"
