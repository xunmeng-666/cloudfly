# -*- coding:utf-8-*-

import os

#定义配置文件路径
BASH = os.path.dirname(os.path.dirname(__file__))
#LOG目录
LOGS = "%s/logs/cloudfly.log" %BASH

HEKETI_ADMIN_KEY = "My Secret"
HEKETI_USER = 'admin'
HEKETI_SERVER = "http://36.111.0.89:32858"
OPENSHIFT_MASTER_ADDRESS="https://36.111.0.89:8443"