#!/bin/bash

APPMAIN="./app/main.py"
PY=$(which python3 || which pypy3 || which python || which pypy) 

DISPLAY=:0 "$PY" "$APPMAIN" $(uname)
