# Route Planner Application Deployment with PyInfra

This project provides multiple deployment methods for a Route Planner application with a MongoDB database using PyInfra. You can choose one of the following deployment options based on your needs:

1. [Systemd Setup](#systemd-setup)
2. [Podman with Kubernetes YAML](#podman-with-kubernetes-yaml)

## Prerequisites

Before deploying the application, ensure you have the following prerequisites:

- Python 3.6+
- PyInfra installed: `pip install pyinfra` or `pip install -r requirements.txt`

Fill neccessary info in group_data/demo.py

Add ip or dns of instance that you want to deploy in inventory/demo.py

Setup was tested against Ubuntu 20.04 cloud images

## Systemd Setup

This method deploys the Route Planner application and MongoDB as systemd services on a single machine.

```shell
pyinfra inventories/demo.py deploy_systemd.py
```


## Podman with Kubernetes YAML

This method allows you to experiment with deploying the application in a Podman pod using Kubernetes YAML files. It is intended for preparing an eventual Kubernetes setup without the actual need for a Kubernetes cluster itself.

With this approach, you can verify that Kubernetes objects (such as Deployments and Services) are valid and that your application behaves as expected when deployed in a Kubernetes-like environment. It provides an excellent way to test your configuration and ensure compatibility with Kubernetes before transitioning to a production Kubernetes cluster.

```shell
pyinfra inventories/demo.py deploy_podman.py
```



