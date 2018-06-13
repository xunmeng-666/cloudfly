# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-25 08:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Glusterfs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Volume Name')),
                ('vid', models.CharField(max_length=128, unique=True, verbose_name='Volume ID')),
                ('status', models.CharField(max_length=64, unique=True, verbose_name='状态')),
                ('brick1', models.CharField(blank=True, max_length=128, null=True, verbose_name='Brick1')),
                ('brick2', models.CharField(blank=True, max_length=128, null=True, verbose_name='Brick2')),
                ('brick3', models.CharField(blank=True, max_length=128, null=True, verbose_name='Brick3')),
            ],
            options={
                'verbose_name': 'GlusterFS',
                'verbose_name_plural': 'GlusterFS',
            },
        ),
        migrations.CreateModel(
            name='Heketi_Auth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roles', models.CharField(default='http', max_length=8, verbose_name='协议')),
                ('admin_key', models.CharField(max_length=128, verbose_name='认证模式')),
                ('host', models.GenericIPAddressField(unique=True, verbose_name='IP地址')),
                ('port', models.IntegerField(default=8080, verbose_name='端口')),
                ('status', models.CharField(blank=True, default='未连接', max_length=16, null=True, verbose_name='连接状态')),
            ],
            options={
                'verbose_name': '设置',
                'verbose_name_plural': '设置',
            },
        ),
        migrations.CreateModel(
            name='Heketi_Cluster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cid', models.CharField(blank=True, max_length=128, null=True, verbose_name='ID')),
            ],
            options={
                'verbose_name': '集群',
                'verbose_name_plural': '集群',
            },
        ),
        migrations.CreateModel(
            name='Heketi_Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nid', models.CharField(max_length=128, verbose_name='ID')),
                ('managehost', models.GenericIPAddressField(null=True, verbose_name='Management Hostname')),
                ('storagehost', models.GenericIPAddressField(null=True, verbose_name='Storage Hostname')),
                ('state', models.CharField(max_length=8, verbose_name='state')),
                ('cluster', models.ForeignKey(max_length=128, on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.Heketi_Cluster', verbose_name='Cluster')),
            ],
            options={
                'verbose_name': '节点',
                'verbose_name_plural': '节点',
            },
        ),
        migrations.CreateModel(
            name='Heketi_Volume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vid', models.CharField(blank=True, max_length=128, null=True, unique=True, verbose_name='ID')),
                ('size', models.IntegerField(blank=True, null=True, verbose_name='Size')),
                ('mounts', models.GenericIPAddressField(blank=True, null=True, verbose_name='Mount')),
                ('backmounts', models.CharField(blank=True, max_length=128, null=True, verbose_name='Mount Options')),
                ('path', models.CharField(blank=True, max_length=128, null=True, verbose_name='Path')),
                ('device', models.CharField(blank=True, max_length=128, null=True, verbose_name='Device')),
                ('cluster', models.ForeignKey(max_length=128, on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.Heketi_Cluster', verbose_name='Clusters')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.Glusterfs')),
                ('nodes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.Heketi_Node')),
            ],
            options={
                'verbose_name': '存储',
                'verbose_name_plural': '存储',
            },
        ),
        migrations.CreateModel(
            name='NameSpaces',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='项目')),
            ],
            options={
                'verbose_name': 'NameSpaces',
                'verbose_name_plural': 'NameSpaces',
            },
        ),
        migrations.CreateModel(
            name='Pod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Pod')),
                ('volumename', models.CharField(max_length=128, unique=True, verbose_name='Volume')),
                ('status', models.CharField(max_length=64, unique=True, verbose_name='运行状态')),
                ('namespaces', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.NameSpaces')),
            ],
            options={
                'verbose_name': 'Pod',
                'verbose_name_plural': 'Pod',
            },
        ),
        migrations.CreateModel(
            name='PV',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='PV')),
                ('capacity', models.CharField(max_length=16, unique=True, verbose_name='容量')),
                ('endpoints', models.CharField(max_length=32, unique=True, verbose_name='存储服务器')),
                ('path', models.CharField(max_length=128, unique=True, verbose_name='挂载')),
                ('accessmodes', models.CharField(max_length=16, unique=True, verbose_name='访问模式')),
                ('status', models.CharField(max_length=16, unique=True, verbose_name='状态')),
                ('namespaces', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.NameSpaces')),
            ],
            options={
                'verbose_name': 'PV',
                'verbose_name_plural': 'PV',
            },
        ),
        migrations.CreateModel(
            name='PVC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='名称')),
                ('selflink', models.CharField(max_length=128, unique=True, verbose_name='路径')),
                ('storage', models.CharField(max_length=16, unique=True, verbose_name='容量')),
                ('accessmodes', models.CharField(max_length=16, unique=True, verbose_name='访问模式')),
                ('namespace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.NameSpaces')),
                ('pv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.PV')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.Glusterfs')),
            ],
            options={
                'verbose_name': 'PVC',
                'verbose_name_plural': 'PVC',
            },
        ),
        migrations.AddField(
            model_name='pod',
            name='pvc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cloudfly_heketi.PVC'),
        ),
    ]