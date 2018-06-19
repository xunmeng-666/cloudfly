# -*- coding:utf-8-*-
import unittest
import json
import os
import logging
from requests.exceptions import ConnectionError
from heketi import HeketiClient
from cloudfly_heketi.admin_base import site
from cloudfly_heketi.packaged.logger import logger
from cloudfly_heketi.conf import conf
from cloudfly_heketi.packaged.env_file import OSEnv




c = HeketiClient(conf.HEKETI_SERVER, 'admin', conf.HEKETI_ADMIN_KEY)
cluster_req = {}
# c = HeketiClient(env_file.heketi_server,env_file.heketi_user,env_file.heketi_user_key)
#
class Test_Heketi(unittest.TestCase,OSEnv):

    # host = OSEnv().heketi_url()
    # user = OSEnv().heketi_user()
    # key = OSEnv().heketi_user_key()
    # logger('设置Heketi连接方式')
    # c = HeketiClient(host,user,key)
    # cluster_req = {}

    def create_cluster(self):
        try:
            cluster_req['file'] = True
            cluster = c.cluster_create()
            cluster_func = cluster
            return cluster_func
        except ConnectionError as e:
            logger('%s' % e, logging.ERROR)
            return False

    def list_cluster(self):
        logger('已连接到cluster接口，获取数据中')
        logger('打印连接程序c: ' ,type(c.cluster_list()))
        list = c.cluster_list()
        print('list',type(list))
        return list

    def change_cluster(self,cid):
        cluster_setflags_req = {}
        cluster_setflags_req['block'] = False
        cluster_setflags_req['file'] = True
        ok = c.cluster_setflags(cid, cluster_setflags_req)
        self.assertTrue(ok)

    def del_cluster(self,cid):
        delete_cluster =c.cluster_delete(cid)
        return delete_cluster

    def info_cluster(self,cid):

        info=c.cluster_info(cid)
        logger('cluster_id:%s info %s' %(cid,info))
        return info

    def info_node(self,n_id):
        info = c.node_info(n_id)
        return info

    def add_node(self,c_id):
        node_req=c_id
        add_node = c.node_add(node_req)
        return add_node

    def list_node(self,c_id):
        list_ele = {}
        list_func = self.info_cluster(c_id)
        if list_func.get('nodes') != None:
            for list_n in list_func.get('nodes'):
                list_ele.update({'Cluster':list_func.get('id'),'Id':list_n})
            return list_ele

    def list_volume(self):
        list = c.volume_list()
        return list

    def info_volume(self,v_id):
        info = c.volume_info(v_id)
        print('volume',info)
        return info


class Get_Heketi(Test_Heketi):
    def get_cluster(self):
        cluster_list = self.list_cluster()
        return cluster_list

    def get_node(self,cid):
        node_list = json.dumps(self.list_node(cid))
        return node_list


class Save_Data(Test_Heketi):
    def save_func(self):
        for app_name in site.registered_admins:
            admin_class = site.registered_admins[app_name]
            return admin_class


    def save_cluster(self):
        admin_class = self.save_func().get('heketi_cluster')
        logger('获取cluster列表')
        cluster_id = self.list_cluster()
        logger('Cluster ID获取成功')
        logger('准备保存ClusterID')
        for cid in cluster_id.get('clusters'):
            logger('检查ClusterID是否存在')
            check_id = self.check_cluster_id(cid)
            logger('ClusterID检查完毕')
            if check_id:
                logger('ClusterID不存在，开始执行保存')
                admin_class.model.objects.create(cid=cid)
                logger('ClusterID已保存')
        return True

    def check_cluster_id(self,cid):
        admin_class = self.save_func().get('heketi_cluster')
        model_class = admin_class.model.objects.all()
        if not model_class:
            logger('数据库是空的，不需要检查')
            return True
        cluster_id = []
        for c_id in model_class.values('cid'):
            logger('获取数据库中已有ClusterID')
            cluster_id.append(c_id.get('cid'))

        logger('匹配已有ClusterID')
        if cid in cluster_id:
            logger('ClusterID存在数据库中，不保存数据')
            return False
        else:
            return True