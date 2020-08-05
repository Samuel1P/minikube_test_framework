from kubernetes import client, config as k8_config, watch
from pdb import set_trace as debug
kube_config = "C:\Program Files\Kubernetes_Files\k8s_repo\k8s_python\KUBECONFIG"
k8_config.load_kube_config(config_file=kube_config)
v1 = client.CoreV1Api()
v1_apps = client.AppsV1Api()


def get_pods_details_in_default_namespace():
    """
    This method fetches all the pod name, pod ip and pod status in the default namespace.
    :return: None
    """
    pod_list = v1.list_namespaced_pod("default")
    for pod in pod_list.items:
        print(f" Pod Name : {pod.metadata.name}, "
              f"Pod Status : {pod.status.phase}, "
              f"Pod IP : {pod.status.pod_ip}")

def get_pods_details_in_dynamic_namespace(ns):

    pod_list = v1.list_namespaced_pod(ns)
    for pod in pod_list.items:
        print(f" Pod Name : {pod.metadata.name}, "
              f"Pod Status : {pod.status.phase}, "
              f"Pod IP : {pod.status.pod_ip}")

def watch_pods_in_default_ns():
    """
    This method watches the event type, pod name and pod status of the default namespace and print when there is a change.
    :return: None
    """
    stream = watch.Watch().stream(v1.list_namespaced_pod, "default")
    for event in stream:
        print (event['type'], event['object'].metadata.name, event['object'].status.phase)

def get_deployments_in_a_ns(ns=''):
    deployments = v1_apps.list_namespaced_deployment(ns)
    for i, j in enumerate(deployments.items):
        print (f"deployments in all ns: {deployments.items[i].metadata.name}")


if __name__ == "__main__":
    #get_pods_details_in_default_namespace()
    #get_pods_details_in_dynamic_namespace("kube-system")
    #watch_pods_in_default_ns()
    #get_deployments_in_a_ns("")
    pass