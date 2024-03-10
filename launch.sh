#!/bin/bash

DATAFILE="./data/happiness.txt"
APPMAIN="./app/main.py"
PY=$(which python3 || which pypy3 || which python || which pypy) 

rm -f "$DATAFILE.backup"
if [ -f "$DATAFILE" ]; then
    mv "$DATAFILE" "$DATAFILE.backup"
fi
DISPLAY=:0 "$PY" "$APPMAIN" >> "$DATAFILE"
