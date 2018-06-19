from django.db import models

# Create your models here.


class Heketi_Cluster(models.Model):
    cid=models.CharField(verbose_name='ID',max_length=128,blank=True,null=True)


    class Meta:
        verbose_name = "集群"
        verbose_name_plural = "集群"
class Heketi_Node(models.Model):
    nid=models.CharField(verbose_name='ID',max_length=128)
    cluster = models.ForeignKey(Heketi_Cluster,max_length=128,verbose_name='Cluster')
    hostnames = models.CharField(verbose_name='HostName',max_length=128,null=True)
    state = models.CharField(verbose_name='state',max_length=8)

    class Meta:
        verbose_name = "节点"
        verbose_name_plural = "节点"
class Heketi_Volume(models.Model):
    vid = models.CharField(verbose_name='ID',max_length=128,blank=True,null=True,unique=True)
    cluster = models.ForeignKey(Heketi_Cluster,max_length=128,verbose_name="Clusters",)
    nodes = models.ForeignKey(Heketi_Node,max_length=128,verbose_name='Nodes')
    name = models.CharField(verbose_name='Name',max_length=128,blank=True,null=True,unique=True)
    size = models.IntegerField(verbose_name='Size',blank=True,null=True)
    mounts = models.GenericIPAddressField(verbose_name='Mount',blank=True,null=True)
    path = models.CharField(verbose_name='Path',max_length=128,blank=True,null=True)
    device = models.CharField(verbose_name='Device',max_length=128,blank=True,null=True)
    class Meta:
        verbose_name = "存储"
        verbose_name_plural = "存储"

class Heketi_Auth(models.Model):
    # roles_method_choices = (0, 'HTTP'),
    # roles = models.SmallIntegerField("连接方式", choices=roles_method_choices,default='HTTP', unique=True)
    roles = models.CharField("协议",max_length=8,default='http')
    admin_key = models.CharField(verbose_name='认证模式',max_length=128,default='My Secret')
    host = models.GenericIPAddressField(verbose_name='IP地址',unique=True)
    port = models.IntegerField(verbose_name='端口',default=8080)
    # status_method_choices = ((0,'未连接'),
    #                          (1,'已连接'),
    #                          )
    # status = models.IntegerField(verbose_name='连接状态',choices=status_method_choices,default='未连接',unique=True)
    status = models.CharField(verbose_name='连接状态',max_length=16,default='未连接',blank=True,null=True)

    class Meta:
        verbose_name = '设置'
        verbose_name_plural = '设置'