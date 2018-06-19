# -*- coding:utf-8-*-

import os

#定义配置文件路径
BASH = os.path.dirname(os.path.dirname(__file__))
#LOG目录
LOGS = "%s/logs/cloudfly.log" %BASH

HEKETI_ADMIN_KEY = ""
HEKETI_USER = ''
HEKETI_SERVER = ""
