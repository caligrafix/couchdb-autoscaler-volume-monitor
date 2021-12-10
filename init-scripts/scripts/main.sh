#!/bin/bash

echo 'sleeping 60 seconds'
sleep 60
./tag-zone-nodes.sh

echo 'sleeping 10 seconds'
sleep 10

echo 'finish cluster setup'
curl -s http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/_cluster_setup \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"action": "finish_cluster"}'

echo 'sleeping 10 seconds'
sleep 30
./test-placement.sh