# -*- coding:utf-8-*-

import os

#定义配置文件路径
BASH = os.path.dirname(os.path.dirname(__file__))
#LOG目录
LOGS = "%s/logs/cloudfly.log" %BASH

HEKETI_ADMIN_KEY = "My Secret"
HEKETI_SERVER = "http://36.111.0.89:32858"
# HEKETI_SERVER = "http://127.0.0.1:32858"
GLUSTERFS_SERVER ="10.211.55.13"