from django.shortcuts import render
from elasticsearch import Elasticsearch
from public.settings import ES_URL
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from pprint import pprint

from .models import *
import json

_index = Elasticsearch(ES_URL)


@csrf_exempt
def insert(request):
    ctx = {}

    body = json.loads(request.body.decode('utf-8'))
    print(body)
    
    if body:
        result = Tender.objects.get_or_create(id=body['id'],
            province=body['province'],
            title=body['title'],
            content=body['content'],
            source_url=body['source_url'],
            publish_time=body['publish_time'])

        if result[1]:
            
            _index.index(index='tender',doc_type='tender',body=body,id=body['id'])

        return JsonResponse({'code':'success'})
    return JsonResponse({'code':'failed'})


def page_aop(func):
    def view(request, *args, **kwargs):
        
        pagesize = int(request.POST.get('pagesize','30'))
        page = int(request.POST.get('page','1'))
        
        result = func(request, *args, **kwargs)

        if isinstance(result, tuple):
            print(result)
            res = result[0]
            res['pagesize'] = pagesize
            res['page'] = page
            print(res)
            paginator = Paginator(res['objects'], pagesize) 
            try:
                res['objects'] = paginator.page(page)
            except EmptyPage:
                res['objects'] = paginator.page(paginator.num_pages) 
            return render(request, result[1], res)

        elif isinstance(result, JsonResponse):
            return result

    view.__name__ = func.__name__

    return view


def index(request):

    ctx = {}
    return render(request,'search.html',ctx)


@csrf_exempt
@page_aop
def query(request):
    ctx = {}
    
    tender = Tender.objects.all()

    if request.method == 'POST':
        ctx['province'] = province = request.POST.get('province','')
        ctx['key'] = key = request.POST.get('key','')
        ctx['publish_time'] = publish_time = request.POST.get('publish_time','')

        if province:
            tender = tender.filter(province=province)
        if key:
            tender = tender.filter(Q(title__contains=key) | Q(content__contains=key))
        if publish_time:
            tender = tender.filter(publish_time__gte=publish_time).order_by('publish_time')
        else:
            tender = tender.order_by('-publish_time')



    ctx['objects'] = tender


    # query = {
    #         "query": {
    #             # "bool": {
    #             #     "must": [
                        
    #             #     ]
    #             # }
    #         },
    #         "from":0,
    #         "size":100,
    #         "_source":["title","province","publish_time","id"],
    #         "highlight":{
    #             "fields":{
    #                 "title":{}
    #             }
    #         }
    # }
    # if key:
    #     query['query']['multi_match'] = {'fields':['title','content'], 'query':key, 'fuzziness':'AUTO'}
    # if not province:
    #     query['query']['bool']['must'].append({"match": {"province": province}})
    # if publish_time:
    #     query['query']['bool']['must'].append({"match": {"publish_time": publish_time}})
    # # if not key and not province and not area and not publish_time and not c_type:
    # #     query = {
    # #         "query":{
    # #             'match_all': {

    # #             }
    # #         }
            
    # #     }
    # print(query)
    # search_result = _index.search(index='tender', body=query)['hits']['hits']
    # ctx['result'] = [_['_source'] for _ in search_result]
    # print(ctx['result'])
    return  (ctx,'search.html')


def get(request,object_id):

    ctx = {}
    # ctx['object'] = obj = _index.get(index='tender',doc_type='tender',id=object_id)['_source']
    ctx['object'] = obj = Tender.objects.get(id=object_id)

    print(obj)
    return render(request,'object.html',ctx)