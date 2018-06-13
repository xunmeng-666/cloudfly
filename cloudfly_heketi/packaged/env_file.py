# -*- coding:utf-8-*-
import os
from kubernetes import config

class OSEnv(object):
    def heketi_system_env(self):
        self.heketi_server = os.environ.get('HEKETI_SERVER')
        self.heketi_user = os.environ.get('HEKETI_USER')
        self.heketi_user_key = os.environ.get('HEKETI_KEY')
        if not self.heketi_server:self.heketi_server='localhost'
        if not self.heketi_user:self.heketi_user='admin'
        if not self.heketi_user_key:self.heketi_user_key='My Secret'

    def openshift_system_env(self):
        self.master = os.environ.get('OPENSHIFT_MASTER_ADDRESS')
        self.token = os.environ.get('OPENSHIFT_TOKEN')
        if not self.master:self.master='localhost'
        if not self.token:config.load_kube_config()
