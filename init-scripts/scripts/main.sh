#!/bin/bash

echo 'sleeping 60 seconds'
sleep 60
./tag-zone-nodes.sh

echo 'sleeping 30 seconds'
sleep 30
./test-placement.sh