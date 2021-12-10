#!/bin/bash

# NODES=24
# TOTAL_NODES="$(($NODES-1))"


# # Pods zone 0 (us-west-2a)
# pods_zone_0=(1 4 7 10 13 16 19 22)
# # Pods zone 1 (us-west-2b)
# pods_zone_1=(2 5 8 11 14 17 20 23)
# # Pods zone 2 (us-west-2c)
# pods_zone_2=(0 3 6 9 12 15 18 21)

NODES=3
TOTAL_NODES="$(($NODES-1))"


# Pods zone 0 (us-west-2a)
pods_zone_0=(1)
# Pods zone 1 (us-west-2b)
pods_zone_1=(2)
# Pods zone 2 (us-west-2c)
pods_zone_2=(0)

zones=("us-west-2a" "us-west-2b" "us-west-2c")

echo 'before tagging nodes:'
for l in $(seq 0 $TOTAL_NODES); do
    curl -X GET http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/_node/_local/_nodes/couchdb@couchdb-couchdb-"${l}".couchdb-couchdb.couchdb.svc.cluster.local
done;

echo 'tag nodes us-west-2a:'
for i in ${pods_zone_0[@]}; do
    curl -X PUT http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/_node/_local/_nodes/couchdb@couchdb-couchdb-"${i}".couchdb-couchdb.couchdb.svc.cluster.local   -d '{  
            "_id": "couchdb@couchdb-couchdb-${i}.couchdb-couchdb.couchdb.svc.cluster.local",
            "_rev": "1-967a00dff5e02add41819138abb3284d",
            "zone": "us-west-2a"
            }'
done

echo 'tag nodes us-west-2b:'
for j in ${pods_zone_1[@]}; do
    curl -X PUT http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/_node/_local/_nodes/couchdb@couchdb-couchdb-"${j}".couchdb-couchdb.couchdb.svc.cluster.local   -d '{  
            "_id": "couchdb@couchdb-couchdb-${j}.couchdb-couchdb.couchdb.svc.cluster.local",
            "_rev": "1-967a00dff5e02add41819138abb3284d",
            "zone": "us-west-2b"
            }'
done

echo 'tag nodes us-west-2c:'
for k in ${pods_zone_2[@]}; do
    curl -X PUT http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/_node/_local/_nodes/couchdb@couchdb-couchdb-"${k}".couchdb-couchdb.couchdb.svc.cluster.local   -d '{  
            "_id": "couchdb@couchdb-couchdb-${k}.couchdb-couchdb.couchdb.svc.cluster.local",
            "_rev": "1-967a00dff5e02add41819138abb3284d",
            "zone": "us-west-2c"
            }'
done

# Get information of nodes
echo 'after tagging nodes:'
for l in $(seq 0 $TOTAL_NODES); do
    curl -X GET http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/_node/_local/_nodes/couchdb@couchdb-couchdb-"${l}".couchdb-couchdb.couchdb.svc.cluster.local
done;




