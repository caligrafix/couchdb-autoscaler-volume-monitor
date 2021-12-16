kubectl delete pod cluster-init
docker build -t gitlab-registry.caligrafix.cl:443/ecaligrafix/couchdb-k8s-stress-tests:init-cluster . --no-cache
docker push gitlab-registry.caligrafix.cl:443/ecaligrafix/couchdb-k8s-stress-tests:init-cluster
kubectl create -f k8s-files/manifest/init-script.yaml
watch kubectl get pods