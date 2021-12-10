echo 'create database mydb'
curl -X PUT http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/mydb

echo 'inserting data...'
curl -X PUT http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/mydb/joan -d '{"loves":"cats"}'

curl -X PUT http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/mydb/robert -d '{"loves":"dogs"}'

echo 'view shards distribution'
curl -s http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/mydb | jq .

curl -s http://QIvMWnriiEmNMrih:mWclZkABuWRvTmGu@couchdb-svc-couchdb.couchdb.svc.cluster.local:5984/mydb/_shards | jq .