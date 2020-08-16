# minikube_test_framework
This repo has methods to retrieve and manipulate kubernetes objects in a single node minikube cluster.
We can use this module in a existing test framework (say PyTest which contains test_scripts) as a utility module.
Also, contains kuberenetes definition files which I have created for creating the kubernetest objects in my node.

k8s_api_module.py - File contains the methods that interact with kubernetes cluster

k8s_config.ini - Configuration info required by the k8s_api_module.py

KUBECONFIG - Place your kubeconfig file in the dummy file location.

k8s_definition_files - This folder contains sample kubernetes definition YAML files.
