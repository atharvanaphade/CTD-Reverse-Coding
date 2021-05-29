#!/usr/bin/env bash
javac main.java
ret=$?
if [ $ret -ne 0 ]
then
  exit 2
fi
ulimit -s 100
timeout --signal=SIGTERM 1 java main < input
exit $?
