from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from cloudfly_heketi.admin_base import site
from cloudfly_heketi.packaged.heketis import Test_Heketi
from cloudfly_heketi.packaged.heketis import Save_Data
from cloudfly_heketi.packaged.logger import logger
from cloudfly_heketi.packaged.openshift import Openshift_info
# from cloudfly_heketi.packaged.openshift import MyEncoder
import json

# Create your views here.

def index(request):

    return render(request,'index.html',locals())

def admin_func():
    '''定义admin func函数，调用数据库使用'''
    for app_name in site.registered_admins:
        admin_class = site.registered_admins[app_name]
        return admin_class

def get_filter_objs(request,admin_class):
    """
    Add paging identifier，
    Extended sort identifier，
    Return filter and queryset
    """
    filter_condtions = {}
    for k,v in request.GET.items():
        if k in ['_page','_q','_o']:
            continue
        if v:
            filter_condtions[k] = v

    queryset = admin_class.model.objects.filter(**filter_condtions)
    return queryset,filter_condtions

def get_orderby_objs(request,querysets):
    """
    sorting
    1.Get value of _o
    2.Call the value of order_by for _o
    3.Deal with positive and negative numbers，To determine the order of the next sort
    4.return

    :param request:
    :param querysets:
    :return:
    """
    orderby_key = request.GET.get('_o')
    last_orderby_key = orderby_key or ''
    if orderby_key:
        order_column = orderby_key.strip('-')
        order_results = querysets.order_by(orderby_key)
        if orderby_key.startswith('-'):
            new_order_key = orderby_key.strip('-')
        else:
            new_order_key = "-%s"% orderby_key
        return order_results,new_order_key,order_column,last_orderby_key
    else:
        return querysets,None,None,last_orderby_key

def get_search_objs(request,querysets,admin_class):
    """
    1.Get value of _q
    2.Join Q selete condition
    3.Run the filter selete of Q condition
    4. Ruturn the selete
    :param request:
    :param querysets:
    :param admin_class:
    :return to the result
    """
    q_val = request.GET.get('_q')
    if q_val:
        q_obj = Q()
        q_obj.connector = "OR"
        for search_field in admin_class.search_fields:
            q_obj.children.append( ("%s__contains" %search_field,q_val) )
        search_results = querysets.filter(q_obj)
    else:
        search_results = querysets
    return search_results,q_val

def cluster(request):
    admin_class = admin_func().get('heketi_cluster')
    model_name = admin_class.model._meta.model_name
    if request.method == 'GET':
        logger("获取Cluster列表")
        Save_Data().save_cluster()
        model_name = admin_class.model._meta.model_name
        logger("Cluster列表获取成功".encode('utf-8'))
        querysets, filter_conditions = get_filter_objs(request, admin_class)
        querysets, q_val = get_search_objs(request, querysets, admin_class)
        querysets, new_order_key, order_column, last_orderby_key = get_orderby_objs(request, querysets)
        paginator = Paginator(querysets, admin_class.list_per_page)  # Show 25 contacts per page
        page = request.GET.get('_page')
        try:
            querysets = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            querysets = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            querysets = paginator.page(paginator.num_pages)
        return render(request, 'nodes/clusters/cluster_list.html', locals())
    elif request.method == 'POST':
        add_clust = Test_Heketi().create_cluster()
        return HttpResponse(json.dumps(add_clust))


def info_cluster(request,cid,model_name):

    if model_name == 'heketi_cluster':
        cluster_info = Test_Heketi().info_cluster(cid)
    elif model_name == 'heketi_node':
        cluster_info = Test_Heketi().info_node(cid)
    elif model_name == 'heketi_volume':
        cluster_info = Test_Heketi().info_volume(cid)
    return render(request,'nodes/clusters/cluster_info.html',locals())


def info_node(request,nid,model_name):
    logger('获取node 信息:%s' %nid  )
    node_info = Test_Heketi().info_node(nid.strip())
    return render(request,'nodes/clusters/cluster_info.html',locals())

@csrf_exempt
def openshift_project(request):
    if request.method == 'GET':
        logger('获取Openshift服务器中的项目')
        namespace = Openshift_info().get_namespaces()

        return render(request, 'nodes/clusters/projects.html', locals())
    elif request.method == 'POST':
        ns_name = None
        for name in request.GET.get('name').split(','):
            ns_name = name.strip()
        pod_func = Openshift_info().get_pod_count(ns_name)
        return HttpResponse(json.dumps(pod_func))

@csrf_exempt
def openshift_pod(request,namespaces=None,*args,**kwargs):
    if request.method=='GET':
        if args:
            namespaces = "".join(namespaces+"-"+args[0])

        pod_func = Openshift_info().get_namespace_pod(namespaces)
        pv_info = Openshift_info().get_amespaced_persistent_volume_claim(namespaces)
        pv_path = Openshift_info().get_persistent_volume()
        volume_name = {}
        for index,pvc in enumerate(pv_info.items):
            volume_name.update({index:{'pvc':pvc.metadata.name,'pv':pvc.spec.volume_name,
                                       'storage':pvc.status.capacity,'access_modes':pvc.status.access_modes,
                                       'status':pvc.status.phase}})
        return render(request, 'nodes/clusters/pvc_info.html', locals())

    elif request.method =='POST':
        namespaces = request.GET.get('pvc').split('/')[0]
        name = request.GET.get('pvc').split('/')[1]
        pvc_info = Openshift_info().get_pvc_info(name=name, namespace=namespaces)
        data = Openshift_info().pvc_func(pvc_info)
        return HttpResponse(json.dumps(data))

def openshift_volume(request,volume_name):
    volume_founc = Openshift_info


def settings(request):

    return render(request,'settings/settings.html',locals())