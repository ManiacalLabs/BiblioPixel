#!/bin/bash

# Test to see that `bp` rereads its files on a SIGHUP
# Must be run from the root

PROJECT=/tmp/bp-project.yml

cp projects/51-red.yml $PROJECT
bp -sv "$PROJECT" &
echo "showing red"
sleep 1
echo "red steady"
sleep 10

cp projects/52-green.yml $PROJECT
killall -SIGHUP %1
echo "showing green?"

sleep 1000
