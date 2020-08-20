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
        try:
            pod_list = v1.list_namespaced_pod("default")
            for pod in pod_list.items:
                print(f" Pod Name : {pod.metadata.name}, "
                      f"Pod Status : {pod.status.phase}, "
                      f"Pod IP : {pod.status.pod_ip}")
        except ApiException as e:
            print (f"API Error : {e}")
        except Exception as e:
            print (f"Error: {e}")

    def get_pods_details_in_user_defined_namespace(self, ns):
        """
        This method fetches all the pod name, pod ip and pod status in the user defined namespace.
        currently I am printing the output, In a real environment we can return this information.
        :param ns:
        :return: None
        """
        try:
            pod_list = v1.list_namespaced_pod(ns)
            for pod in pod_list.items:
                print(f" Pod Name : {pod.metadata.name}, "
                      f"Pod Status : {pod.status.phase}, "
                      f"Pod IP : {pod.status.pod_ip}")
        except ApiException as e:
            print (f"API Error : {e}")
        except Exception as e:
            print (f"Error: {e}")
    def get_kubernetes_version_info(self):
        """
        fetching the kubernetes version installed on the host
        :return: None
        """
        try:
            res = requests.get(urljoin(base_url, 'version'), headers=def_header)
            debug()
            if res.status_code == 200:
                print (f" Kubernetes version installed is {res.text}")
            else:
                print ("Kubernetes Version Not available")
        except ApiException as e:
            print (f"Error : {e}")
        except Exception as e:
            print (f"Error: {e}")

    def get_api_versions_available(self):
        """
        This method lists all the supported API's and their version in the kubernetes cluster
        :return: None
        """
        try:
            print("Supported APIs:")
            print (v.get_api_versions().versions)
            for api in client.ApisApi().get_api_versions().groups:
                print (f"{api.versions[0].group_version} - {api.versions[0].version}")
        except ApiException as e:
            print (f"API Error : {e}")
        except Exception as e:
            print (f"Error: {e}")

    def watch_pods_in_default_ns(self):
        """
        This method watches the event type, pod name and pod status of the default namespace and print when there is a change.

        :return: None
        """
        try:
            stream = watch.Watch().stream(v1.list_namespaced_pod, "default")
            for event in stream:
                print (event['type'], event['object'].metadata.name, event['object'].status.phase)
        except ApiException as e:
            print (f"API Error : {e}")
        except Exception as e:
            print (f"Error: {e}")

    def get_deployments_in_a_ns(self, ns=''):
        """
        This method fetches the deployment info of the namespace provided, if namespace is empty, deployments in default namespace is provided.
        currently I am printing the output, In a real environment we can return this information.
        :param ns:
        :return: None
        """
        try:
            deployments = v1_apps.list_namespaced_deployment(ns)
            for i, j in enumerate(deployments.items):
                print (f"deployments info: {deployments.items[i].metadata.name}")
        except ApiException as e:
            print (f"API Error : {e}")
        except Exception as e:
            print (f"Error: {e}")

    def get_available_namespace(self):
        """
        this method gets all namespaces available in the cluster
        :param
        :return:
        """
        try:
            api_res = v1.list_namespace()
            namespace_names = [i.metadata.name for i in api_res.items]
            print(namespace_names)
        except ApiException as e:
            print (f"API Error : {e}")
        except Exception as e:
            print (f"Error: {e}")

    def get_if_namespace_is_present(self, ns):
        """
        this method checks if a namespace available in the cluster
        :param ns
        :return:
        """
        try:
            api_res = v1.list_namespace()
            namespace_names = [i.metadata.name for i in api_res.items]
            if ns in namespace_names:
                print (f"{ns} namespace is present")
            else:
                print (f"{ns} namespace is not present")
        except ApiException as e:
            print(f"API Error : {e}")
        except Exception as e:
            print(f"Error: {e}")

k8s_obj = kubernetes_library()
# k8s_obj.get_pods_details_in_default_namespace()
# k8s_obj.get_deployments_in_a_ns()
# k8s_obj.get_api_versions_available()
k8s_obj.get_available_namespace()
k8s_obj.get_if_namespace_is_present('default')