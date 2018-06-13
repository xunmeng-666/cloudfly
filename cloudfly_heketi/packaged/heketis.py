# -*- coding:utf-8-*-
import unittest
import json
import os
import logging
from requests.exceptions import ConnectionError
import heketi
from heketi import HeketiClient
from gluster import cli
from cloudfly_heketi.admin_base import site
from cloudfly_heketi.packaged.logger import logger
from cloudfly_heketi.conf import conf
from cloudfly_heketi.packaged.env_file import OSEnv




# c = HeketiClient(conf.HEKETI_SERVER, 'admin', conf.HEKETI_ADMIN_KEY)

cluster_req = {}
class Test_Heketi(unittest.TestCase,OSEnv):

    def init_func(self):
        self.c = HeketiClient(self.heketi_server,self.heketi_user,self.heketi_user_key)

    def create_cluster(self):
        try:
            cluster_req['file'] = True
            cluster = self.c.cluster_create()
            cluster_func = cluster
            return cluster_func
        except ConnectionError as e:
            logger('%s' % e, logging.ERROR)
            return False

    def list_cluster(self):
        list = self.c.cluster_list()
        print('list',list)
        return json.dumps(list)

    def change_cluster(self,cid):
        cluster_setflags_req = {}
        cluster_setflags_req['block'] = False
        cluster_setflags_req['file'] = True
        ok = self.c.cluster_setflags(cid, cluster_setflags_req)
        self.assertTrue(ok)

    def del_cluster(self,cid):
        delete_cluster =c.cluster_delete(cid)
        return delete_cluster

    def info_cluster(self,cid):
        info=self.c.cluster_info(cid)
        logger('cluster_id:%s info %s' %(cid,info))
        return info

    def info_node(self,n_id):
        info = self.c.node_info(n_id)
        print('info',info)
        return info

    def add_node(self,c_id):
        node_req=c_id
        add_node = self.c.node_add(node_req)
        return add_node

    def list_node(self,c_id):
        list_ele = {}
        list_func = self.info_cluster(c_id)
        if list_func.get('nodes') != None:
            for list_n in list_func.get('nodes'):
                list_ele.update({'Cluster':list_func.get('id'),'Id':list_n})
            return list_ele

    def list_volume(self):
        list = self.c.volume_list()
        return list

    def info_volume(self,v_id):
        info = self.c.volume_info(v_id)
        print('volume',info)
        return info


class Get_Heketi(Test_Heketi):
    def get_cluster(self):
        cluster_list = self.list_cluster()
        return cluster_list

    def get_node(self,cid):
        node_list = json.dumps(self.list_node(cid))
        return node_list



