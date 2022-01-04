# CouchDB k8s Cluster 

This repo contains three main topics, can be used in conjunction with (fsalazar helm repo) to setup a cluster of couchdb with automated placement tagging and volume monitor and autoscaling with Helm. For more information visit the repo and follow instructions to deploy. 

Table of Contents
- [CouchDB k8s Cluster](#couchdb-k8s-cluster)
	- [Repository Structure](#repository-structure)
	- [Stress Tests](#stress-tests)
	- [Placement Tagging Script](#placement-tagging-script)
	- [Volumes Monitor Script](#volumes-monitor-script)

## Repository Structure
    .
    ├── src                   # Principal Code
    │   ├── couch             # Couchdb Functions
    │   ├── k8s               # Kubernetes Functions
    │   ├── envs.py           # Kubernetes Functions
    │   ├── scenarios.py      # Stress Tests scenarios
    │   ├── scripts.py        # Initialization Script and Monitor Volumes Script
    ├── Dockerfile            # To build this image
    ├── main.py               # Main file 


## Stress Tests 
Stress Tests Scenarios to demostrate Resilience in Couchdb Cluster.
| # | Scenario         | Objective                                                |
|---|------------------|----------------------------------------------------------|
| 0 | Populate CouchDB | Stress Couchdb populating fake data                      |
| 1 | Delete All Pods  | Resilience of Couchdb after deleting all pods of cluster |
| 2 | Delete Some Pods | Writing couchdb data while some pods are down            |
| 3 | Resize PVC       | Resize PVC of specific pods                              |


## Placement Tagging Script

Initialization Script for tagging couchdb cluster nodes with placement attribute in order to achieve HA across AZ (Availability Zones).

To achieve [placement a database on specific nodes](https://docs.couchdb.org/en/stable/cluster/databases.html#placing-a-database-on-specific-nodes) and configure cluster for HA. 


## Volumes Monitor Script 

Monitoring Script to observe the capacity of CouchDB Volumes, and increase their size in case that % of use is over defined threshold (parametrized). 




