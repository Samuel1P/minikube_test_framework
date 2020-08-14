from kubernetes import client, config as k8_config, watch
from pdb import set_trace as debug
import configparser
import os
import requests
from ast import literal_eval
from urllib.parse import urljoin
from kubernetes.client.rest import ApiException


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'k8s_config.ini')
KUBECONFIG_PATH = os.path.join(ROOT_DIR, 'KUBECONFIG')
config = configparser.ConfigParser(os.environ)
config.read(CONFIG_PATH)
node_ip = config.get('node', 'node_ip')
base_url = config.get('node', 'base_url')
def_header = config.get('constants', 'default_header')
def_header = literal_eval(def_header)
k8_config.load_kube_config(config_file=KUBECONFIG_PATH)
v = client.CoreApi()
v1 = client.CoreV1Api()
v1_apps = client.AppsV1Api()

class kubernetes_library:
    """
    Kuberntes library contains methods that will connect to a kubernetes cluster and performs fetching or manipulation of kubernetes objects running in the cluster.
    """
    def get_pods_details_in_default_namespace(self):
        """
        This method fetches all the pod name, pod ip and pod status in the default namespace.
        currently I am printing the output, In a real environment we can return this information.
        :return: None
        """
        pod_list = v1.list_namespaced_pod("default")
        for pod in pod_list.items:
            print(f" Pod Name : {pod.metadata.name}, "
                  f"Pod Status : {pod.status.phase}, "
                  f"Pod IP : {pod.status.pod_ip}")

    def get_pods_details_in_user_defined_namespace(self, ns):
        """
        This method fetches all the pod name, pod ip and pod status in the user defined namespace.
        currently I am printing the output, In a real environment we can return this information.
        :param ns:
        :return: None
        """
        pod_list = v1.list_namespaced_pod(ns)
        for pod in pod_list.items:
            print(f" Pod Name : {pod.metadata.name}, "
                  f"Pod Status : {pod.status.phase}, "
                  f"Pod IP : {pod.status.pod_ip}")

    def get_kubernetes_version_info(self):
        """
        fetching the kubernetes version installed on the host
        :return: None
        """
        response = requests.get(urljoin(base_url, 'version'), headers=def_header)
        debug()
        if response.status_code == 200:
            print (f" Kubernetes version installed is {response.text}")
        else:
            print ("Kubernetes Version Not available")

    def get_api_versions_available(self):
        """
        This method lists all the supported API's and their version in the kubernetes cluster
        :return: None
        """
        print("Supported APIs (* is preferred version):")
        print (v.get_api_versions().versions)
        for api in client.ApisApi().get_api_versions().groups:
            print (f"{api.versions[0].group_version} - {api.versions[0].version}")


    def watch_pods_in_default_ns(self):
        """
        This method watches the event type, pod name and pod status of the default namespace and print when there is a change.

        :return: None
        """
        stream = watch.Watch().stream(v1.list_namespaced_pod, "default")
        for event in stream:
            print (event['type'], event['object'].metadata.name, event['object'].status.phase)

    def get_deployments_in_a_ns(self, ns=''):
        """
        This method fetches the deployment info of the namespace provided, if namespace is empty, deployments in default namespace is provided.
        currently I am printing the output, In a real environment we can return this information.
        :param ns:
        :return: None
        """
        deployments = v1_apps.list_namespaced_deployment(ns)
        for i, j in enumerate(deployments.items):
            print (f"deployments info: {deployments.items[i].metadata.name}")



class_obj = kubernetes_library()
# class_obj.get_pods_details_in_default_namespace()
# class_obj.get_deployments_in_a_ns()
# class_obj.get_api_versions_available()
