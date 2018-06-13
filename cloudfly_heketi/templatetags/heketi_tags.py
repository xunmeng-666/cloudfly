from django.template import Library
from django.utils.safestring import mark_safe
from django.utils import timezone
from cloudfly_heketi.packaged.openshift import Openshift_info
#标签文件


register = Library()

@register.simple_tag
def get_abs_value(loop_num , curent_page_number):
    return abs(loop_num - curent_page_number)

@register.simple_tag
def build_table_row(row,admin_class,model_name):

    obj = admin_class.model._meta.model_name
    row_ele = "<tr>"
    row_ele += "<th class='text-center'><input type='checkbox'  class='row-obj' name ='_selected_obj'  value='{obj_id}'></th>".format(obj_id=row.id)
    for index,column_name in enumerate(admin_class.list_display):
        field_obj = row._meta.get_field(column_name)

        if field_obj.choices:
            column_display_func = getattr(row,"get_%s_display"% column_name)
            column_val = column_display_func()
        else:
            column_val = getattr(row,column_name)
        if index == 0:
            if obj == 'heketi_cluster':
                td_ele = "<th><a href='/cluster_info/{obj_id}/{model_name}/' id='info_cluster'>{column_val}</a></th>".format(obj_id=row.cid,column_val=column_val,model_name=admin_class.model._meta.model_name)
            elif obj == 'heketi_node':
                td_ele = "<th ><a href='/node_info/{obj_id}/{model_name}/'>{column_val}</a></th>".format(obj_id=row.nid,model_name=admin_class.model._meta.model_name,column_val=column_val)
            elif obj == 'heketi_volume':
                td_ele = "<th ><a href='/volume_info/{obj_id}/{model_name}/'>{column_val}</a></th>".format(obj_id=row.vid,model_name=admin_class.model._meta.model_name,column_val=column_val)
            elif obj == 'heketi_auth':
                td_ele = "<th>{column_val}</a></th>".format(column_val=column_val)

        else:

            if index == 1:

                if obj == 'heketi_auth':
                    td_ele = "<th>{column_val}</th>".format(column_val=column_val)
                elif obj == 'heketi_volume':
                    td_ele = "<th>{column_val}</th>".format(column_val=column_val)
                else:
                    td_ele = "<th>{column_val}</th>".format(column_val=column_val.cid)
            elif index == 2:
                if obj == 'heketi_volume':
                    td_ele = "<th ><a href='/cluster_info/{obj_id}/{model_name}/'>{column_val}</a></th>".format(obj_id=row.id, model_name=admin_class.model._meta.model_name, column_val=column_val)
                else:
                    # td_ele = "<th id='state'>{column_val}</th>".format(column_val=column_val)
                    td_ele = "<th id='{column_id}'>{column_val}</th>".format(column_id=column_val,column_val=column_val)
            else:
                td_ele = "<th id='{column_id}'>{column_val}</th>".format(column_id=column_name,column_val=column_val)
        row_ele += td_ele

    return mark_safe(row_ele)

@register.simple_tag
def build_table_func(row,model_name):

    table_th = "<th class='text-center' data-editable='false'>"
    if model_name =='heketi_cluster':
        table_a = "<a onclick='del_cluster(this)' type='button' class='btn btn-xs btn-danger'>删除</a>"
    elif model_name == 'heketi_node':
        table_a = "<a href='/cluster_info/{obj_id}/{model_name}/' class='icon icon-hand-up'></a>".format(obj_id=row.nid,model_name=model_name)
    elif model_name == 'heketi_volume':
        table_a = "<a href='/cluster_info/{obj_id}/{model_name}/' class='icon icon-hand-up'></a>".format(obj_id=row.vid,model_name=model_name)
    elif model_name == 'heketi_auth':
        table_a = "<a href='/edit_heketi/{obj_id}/{model_name}/'class='btn btn-success btn-sm btn-mini'>编辑</a>".format(obj_id=row.id,model_name=model_name)
        table_a += ' '
        # table_a += "<a id='conn_heketi'  class='btn btn-primary btn-mini'>连接</a>".format(obj_id=row.id,model_name=model_name)
        table_a += "<a id='conn_heketi_{id}'   class='btn btn-primary btn-mini conn_haketi'>连接</a>".format(id=row.id,model_name=model_name)
        table_a += ' '
        table_a += "<a id='del_heketi' class='btn btn-danger btn-sm btn-mini del_heketi'>删除</a>".format(obj_id=row.id,model_name=model_name)
    table_th+= table_a
    return mark_safe(table_th)


@register.simple_tag
def build_meta_name(admin_class):
    print('amdin_cluster',admin_class)
    try:
        meta_name = admin_class.model._meta.verbose_name
        if meta_name == '集群':
            row_ele = "<h3 id='cluster'>Heketi Cluster 列表</h3>"
        elif meta_name == '节点':
            row_ele = "<h3 id='nodes'>Heketi Nodes 列表</h3>"
        elif meta_name == "存储":
            row_ele = "<h3 id='volume'>Heketi Volume 列表</h3>"
        elif meta_name == "设置":
            row_ele = "<h3 id='auth'>Heketi 服务器列表</h3>"
        else:
            row_ele = ""
        return mark_safe(row_ele)
    except AttributeError :
        pass

@register.simple_tag
def build_cluster_info(cluster_info,model_name):
    print('model_name',model_name)
    print('cluster_info',cluster_info)
    ele_th = ""
    for node_k ,node_v in cluster_info.items():

        if node_k == 'id':
            ele_th += "<h4 class='text-capitalize'>{node_k}</h4>".format(node_k=node_k)
            ele_th += "<th><a href='/cluster_info/{n_id}/{model_name}/'>{node_v}</a></th>".format(n_id=node_v,
                                                                                                 node_v=node_v,
                                                                                            model_name=model_name)
            ele_th += "<hr>"
        elif node_k == 'cluster':
            ele_th += "<h4 class='text-capitalize'>{node_k}</h4>".format(node_k=node_k)
            ele_th += "<th><a href='/cluster_info/{c_id}/heketi_cluster/ '>{node_v}</a></th>".format(c_id=node_v,
                                                                                        node_v=node_v,
                                                                                        )
            ele_th += "<hr>"
        elif node_k == 'nodes':
            model_name = 'heketi_node'
            if type(node_v) is list:
                ele_th += "<h4 class='text-capitalize'>{node_k}</h4>".format(node_k=node_k)
                for node_id in node_v:
                    ele_th += "<p><a href='/node_info/{n_id}/{model_name}'>{node_v}</a></p>".format(n_id=node_id,
                                                                                                    node_v=node_id,
                                                                                                    model_name=model_name)
                ele_th += "<hr>"
            else:
                ele_th += "<h4 class='text-capitalize'>{node_k}</h4>".format(node_k=node_k)
                ele_th += "<th><a href='/node_info/{n_id}/{model_name}/'>{node_v}</a></th>".format(n_id=node_id,
                                                                                                   node_v=node_id,
                                                                                                   model_name=model_name)
                ele_th += "<hr>"
        elif node_k == 'volumes':
            model_name = 'heketi_volume'
            ele_th += "<h4 class='text-capitalize'>{node_k}</h4>".format(node_k=node_k)
            for volume_id in node_v:
                ele_th += "<p><a href='/volume_info/{n_id}/{model_name}/'>{node_v}</a></p>".format(n_id=volume_id,
                                                                                                      node_v=volume_id,
                                                                                                      model_name=model_name)
            ele_th += "<hr>"
        else:
            ele_th += "<h4 class='text-capitalize'>{node_k}</h4>".format(node_k = node_k)
            ele_th += "<th>{node_v}</th>".format(node_v = node_v)
            ele_th += "<hr>"

    return mark_safe(ele_th)


@register.simple_tag
def get_selected_m2m_objects(form_obj,field_name):
    if form_obj.instance.id:
        field_obj = getattr(form_obj.instance, field_name)
        return field_obj.all()
    else:
        return []

@register.simple_tag
def get_m2m_objects(admin_class,field_name,selected_objs):
    """
    1.根据field_name从admin_class.model反射出字段对象
    2.拿到关联表的所有数据
    3.返回数据
    :param admin_class:
    :param field_name:
    :return:
    """

    field_obj = getattr(admin_class.model,'%s'%field_name)
    all_objects = field_obj.rel.to.objects.all()
    return set(all_objects) - set(selected_objs)

@register.simple_tag
def build_pod_info(pod_func,volume_name,pv_path):

    ele = ""
    ele_tr = "<tr>"
    if not volume_name:
        count =0
        for index,pod in enumerate(pod_func.items):
            ele_td = "<td id='pvc_name' style='cursor:pointer;' data-toggle='modal' data-target='#myModal'>None</td>"
            ele_td += "<td>None</td>"
            ele_td += "<td>None</td>"
            ele_td += "<td>None</td>"
            ele_td += "<td>None</td>"
            ele_td += "<td>%s</td>" % pod.metadata.namespace
            ele_td += "<td>%s</td>" % timezone.datetime.strftime(pod.metadata.creation_timestamp, "%Y-%m-%d %H:%M:%S")
            for vol in pv_path.items:
                # if volume_name[index].get('pv').strip() == vol.metadata.name:
                if index == count:
                    heketi_id = vol.metadata.annotations.get('gluster.kubernetes.io/heketi-volume-id')
                    ele_td += "<td><a href='/volume_info/{heketi}/heketi_volume/'>{vol}</a></td>".format(heketi=heketi_id,vol=vol.spec.glusterfs.path)
                    count += 1
            ele_tr += ele_td
            ele_tr += '</tr>'

    else:
        for index,pod in enumerate(pod_func.items):
            print('pod',pod)
            try:
                ele_td = "<td id='pvc_name' style='cursor:pointer;' data-toggle='modal' data-target='#myModal'>%s</td>" %volume_name[index].get('pvc')
                ele_td += "<td>%s</td>" %volume_name[index].get('pv')
            except KeyError:
                ele_td = "<td>None</td>"
                ele_td += "<td>None</td>"
            if volume_name[index].get('status') == 'Bound':
                ele_td += "<td style='color: #00B700'>%s</td>" %volume_name[index].get('status')
            else:
                ele_td += "<td style='color: #FF0000'> %s </td>" %volume_name[index].get('status')
            ele_td += "<td>%s</td>" %volume_name[index].get('storage').get('storage')
            ele_td += "<td>%s</td>" %volume_name[index].get('access_modes')[0]
            ele_td += "<td>%s</td>" %pod.metadata.namespace
            ele_td += "<td>%s</td>" %timezone.datetime.strftime(pod.metadata.creation_timestamp,"%Y-%m-%d %H:%M:%S")
            for vol in pv_path.items:
                if volume_name[index].get('pv').strip() == vol.metadata.name:
                    heketi_id = vol.metadata.annotations.get('gluster.kubernetes.io/heketi-volume-id')
                    ele_td += "<td><a href='/volume_info/{heketi}/heketi_volume/'>{vol}</a></td>".format(heketi=heketi_id,vol=vol.spec.glusterfs.path)
            ele_tr += ele_td
            ele_tr += '</tr>'
    ele += ele_tr
    return mark_safe(ele)

@register.simple_tag
def build_pvc_info(pvc_info):
    print('pvc',pvc_info)
    if not pvc_info:
        return mark_safe("")
    else:
        ele_founc = "<dl class='dl-horizontal'>"+"<dt>Name</dt>" + "<dd>"+pvc_info.metadata.name+"</dd>"+"</dl>"
        ele_founc += "<dl class='dl-horizontal'>"+"<dt>Namespace</dt>" + "<dd>"+pvc_info.metadata.namespace+"</dd>"+"</dl>"
        ele_founc += "<dl class='dl-horizontal'>"+"<dt>StorageClass</dt>" + "<dd>"+pvc_info.metadata.annotations.get('volume.beta.kubernetes.io/storage-class')+"</dd>"+"</dl>"
        return mark_safe(ele_founc)

@register.simple_tag
def build_pod_count(namespace):
    ele = ""
    ele_tr = "<tr>"
    for pod_info in namespace.items:
        ns_name = pod_info.metadata.name
        pod_count = Openshift_info().get_pod_count(ns_name)
        ele_td = "<td style='text-decoration: none;text-align: center'><a href='/project_info/{project}/'>{project_name}</td>".format(project=ns_name,
                                                                                                                                      project_name=ns_name)
        ele_td += "<td style='text-decoration: none;text-align: center'>%s</td>"%pod_count[ns_name]
        ele_tr += ele_td
        ele_tr += "</tr>"
    ele += ele_tr
    return mark_safe(ele)