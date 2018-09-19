from  kubernetes import config,client
from cloudfly_heketi.packaged.env_file import OSEnv
from cloudfly_heketi.packaged.logger import logger
import json

class Openshift_info(OSEnv):

    try:
        config.load_kube_config()
    except FileNotFoundError:
        pass

    def get_namespaces(self):
        logger('已连接到服务器，正在获取项目列表')
        ns_func = client.CoreV1Api().list_namespace()
        logger('项目列表获取成功，返回项目列表')
        return ns_func

    def get_pod(self):
        pod_func = client.CoreV1Api().list_pod_for_all_namespaces()
        return pod_func

    def get_namespace_pod(self,namespaces):
        pod_info = client.CoreV1Api().list_namespaced_pod(namespace=namespaces)
        return pod_info

    def get_amespaced_persistent_volume_claim(self,namespaces):
        volume_info = client.CoreV1Api().list_namespaced_persistent_volume_claim(namespace=namespaces)
        return volume_info

    def get_persistent_volume(self):
        volume_info = client.CoreV1Api().list_persistent_volume()
        return volume_info

    def get_pvc_info(self,name,namespace):
        pvc_info = client.CoreV1Api().read_namespaced_persistent_volume_claim(name,namespace)
        return pvc_info

    def get_pod_count(self,namespace):
        pod_info = self.get_namespace_pod(namespace)
        count = 0
        for info in pod_info.items:
            if info.metadata.namespace == namespace and info.metadata.name != None:
                count += 1
        return {namespace:count}


    def pvc_func(self,pvc_info):
        # labels = []
        if not pvc_info.metadata.labels:
            labels=("none")
        else:
            labels=("application=%s" %pvc_info.metadata.labels.get('application'))
        data = {'Name': pvc_info.metadata.name, 'Namespace': pvc_info.metadata.namespace,
                'StorageClass': pvc_info.metadata.annotations.get('volume.beta.kubernetes.io/storage-class'),
                'Status': pvc_info.status.phase, 'Volume': pvc_info.spec.volume_name,
                'Labels': "%s" %labels,
                "Annotations": ["%s=%s" % (k, v) for k, v in pvc_info.metadata.annotations.items()],
                "Finalizers": pvc_info.metadata.finalizers,
                'Capacity': pvc_info.status.capacity.get('storage'),
                'access_modes': pvc_info.status.access_modes[0]}
        return data

