# -*- coding:utf-8-*-
import os
from cloudfly_heketi.conf import conf
from cloudfly_heketi.packaged.logger import logger
from kubernetes import config

class OSEnv(object):
    def heketi_url(self):
        logger('获取Heketi RUL')
        heketi_url = os.environ.get('HEKETI_URL')
        if not heketi_url or heketi_url == '':
            logger('环境变量中未找到Heketi URL')
            logger('设置Heketi URL为默认地址: %s' %conf.HEKETI_SERVER)
            heketi_url=conf.HEKETI_SERVER
        return heketi_url

    def heketi_user(self):
        logger('获取Heketi USER')
        user = os.environ.get('HEKETI_USER')
        if not user:
            logger('环境变量中未找到Heketi USER')
            logger('设置Heketi USER: %s' % conf.HEKETI_USER)
            user = conf.HEKETI_USER
        return user

    def heketi_user_key(self):
        logger('获取Heketi KEY')
        user_key = os.environ.get('HEKETI_KEY')
        if not user_key:
            logger('环境变量中未找到Heketi KEY')
            logger('设置Heketi KEY: %s' % conf.HEKETI_ADMIN_KEY)
            user_key = conf.HEKETI_ADMIN_KEY
        return user_key

    def openshift_address(self):
        self.master_address = os.environ.get('OPENSHIFT_MASTER_ADDRESS')
        return self.master_address

    def openshfit_token(self):
        self.token = os.environ.get('OPENSHIFT_TOKEN')

        return self.token

