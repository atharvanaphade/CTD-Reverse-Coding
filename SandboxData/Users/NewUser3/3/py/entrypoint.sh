#!/usr/bin/env bash
ulimit -s 100
timeout --signal=SIGTERM 2 python3 main.py < input
exit $?
