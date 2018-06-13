from django.contrib import admin
from django import forms
from cloudfly_heketi import models
from cloudfly_heketi.admin_base import site,BaseAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField




class HeketiClusterInfo(BaseAdmin):
    list_display = ["cid"]
    list_filter = ['ID']

class HeketiNodeInfo(BaseAdmin):
    list_display = ["nid",'cluster','hostnames','state']
    list_filter = ["ID",'集群','主机','状态']

class HeketiVolumeInfo(BaseAdmin):
    list_display = ["vid",'name','size','mounts','path']
    list_filter = ["ID",'存储名称','大小','挂载主机','挂载路径']

class HeketiAuthInfo(BaseAdmin):
    list_display = ['roles','admin_key','host','port','status']
    list_filter = ['连接方式','认证模式','主机地址','端口','连接状态']


site.register(models.Heketi_Cluster,HeketiClusterInfo)
site.register(models.Heketi_Node,HeketiNodeInfo)
site.register(models.Heketi_Volume,HeketiVolumeInfo)
site.register(models.Heketi_Auth,HeketiAuthInfo)