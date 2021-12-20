# CouchDB k8s Stress Tests

Proof of concepts of resilience in CouchDB EKS Cluster.

## Prerequisites

1. Have a connection with kubernetes cluster through kubectl command.
2. In case of use CouchDB, have a port forward of service in local machine.

```$ kubectl -n couchdb port-forward service/couchdb-couchdb 5984:5984```

## Scenarios 

- Scenario 1: Delete all pods
- Scenario 2: Delete some pods

### Example
```$ python main.py --scenario 1```


 helm install vpa-v0 --values charts/vpa-values.yaml cowboysysop/vertical-pod-autoscaler
