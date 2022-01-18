# CouchDB k8s Cluster Volume Monitor

This repo monitor couchdb volumes associated to nodes of couchdb cluster and scale this volumes based on parametrized threshold. 

Table of Contents
- [CouchDB k8s Cluster Volume Monitor](#couchdb-k8s-cluster-volume-monitor)
  - [Repository Structure](#repository-structure)
  - [Volumes Monitor Script](#volumes-monitor-script)

## Repository Structure
    .
    ├── src                   # Principal Code
    │   ├── couch             # Couchdb Functions
    │   ├── k8s               # Kubernetes Functions
    │   ├── envs.py           # Environment Variables 
    │   ├── scripts.py        # Monitor Volumes Script
    ├── Dockerfile            # To build this image
    ├── main.py               # Main file 


## Volumes Monitor Script 

Monitoring Script to observe the capacity of CouchDB Volumes, and increase their size in case that % of use is over defined threshold (parametrized). 




