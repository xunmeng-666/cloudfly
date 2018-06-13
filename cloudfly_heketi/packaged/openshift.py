# from kubernetes import client,config
# import requests
# import urllib3
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# import yaml
#
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# api_url = 'https://shanghai.paas.ctyun.cn:8443'
# api_namespaces = '/api/v1/namespaces/'
# api_pod='/api/v1/pods'
# api_project = "/oapi/v1/projects"
# api_pv ='/api/v1/persistentvolumes'
# api_pvc = '/api/v1/persistentvolumeclaims'
# headers = {'Authorization': 'Bearer VlPBIwbMxgRSHEWYvgRIzYtIOKnZIAHEIwRIb_dflBE'}
#
# config.load_kube_config()
# #
# def get_namespaces():
#     #获取namespace 列表
#     ns_func = requests.get("%s/%s" % (api_url, api_namespaces), headers=headers, verify=False)
#     namespace_list = []
#     for ns in ns_func.json()['items']:
#         namespace_list.append(ns['metadata']['name'])
#     return namespace_list
#
# def get_project():
#     #获取项目列表
#     project_func = requests.get("%s/%s" % (api_url, api_project), headers=headers, verify=False)
#     project_list = []
#     for project in project_func.json()['items']:
#         project_list.append(project['metadata']['name'])
#     return project_list
#
# def get_pv():
#     pv_func = requests.get("%s/%s/" % (api_url,api_pv), headers=headers, verify=False)
#     pv_list =[]
#     for pv_info in pv_func.json()['items']:
#         print('pv',pv_info)
#         pv_list.append(pv_info['metadata'])
#     return pv_list
#
# def get_pvc():
#     #获取PVC
#     print('pvc')
#     pvc_func = requests.get("%s/%s/" %(api_url,api_pvc),headers=headers,verify=False)
#     pvc_list=[]
#     for pvc in pvc_func.json()['items']:
#         pvc_list.append(pvc['metadata'])
#     return pvc_list
# def get_pod():
#     #获取pod信息
#     pod_func = requests.get("%s/%s" % (api_url, api_pod), headers=headers, verify=False)
#     pod_list = []
#     for pod_info in pod_func.json()['items']:
#         pod_list.append(pod_info['metadata'])
#     return pod_list
#
# c = get_pod()
# print('a',c)


from  kubernetes import config,client
from cloudfly_heketi.packaged.env_file import OSEnv
import json

# config.load_kube_config()
# aa = client.CoreV1Api()
# print(aa.list_node())

class Openshift_info(OSEnv):
    # config.load_kube_config()

    def authentication(self):
        self.auth = self.token

    def get_namespaces(self):
        ns_func = client.CoreV1Api().list_namespace()
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
            print('lable is none',labels)
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
        print('data',data)
        return data



a = Openshift_info().get_pod()