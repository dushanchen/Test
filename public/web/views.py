from django.shortcuts import render
from elasticsearch import Elasticsearch
from wonder.settings import ES_URL
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from pprint import pprint

from .models import *
# Create your views here.
import json

_index = Elasticsearch(ES_URL)

@csrf_exempt
def insert(request):
    ctx = {}

    body = json.loads(request.body)
    print(body)
    
    if body:
        result = Tender.objects.get_or_create(id=body['id'],
            province=body['province'],
            title=body['title'],
            content=body['content'],
            source_url=body['source_url'],
            publish_time=body['publish_time'])

        if result[1]:
            data = {
                '_index':'tender',
                '_type':'doc',
                '_id':body['id'],
                '_source':body
            }
            _index.index(index='tender',doc_type='doc',body=body,id=body['id'])

            return JsonResponse({'code':'success'})
    return JsonResponse({'code':'failed'})


def index(request):

    ctx = {}
    return render(request,'search.html',ctx)


def query(request):
    ctx = {}
    ctx['province'] = province = request.POST.get('province','')
    ctx['key'] = key = request.POST.get('key','')
    ctx['publish_time'] = publish_time = request.POST.get('publish_time','')

    query = {
            "query": {
                "bool": {
                    "must": [
                        
                    ]
                }
            },
            "from":0,
            "size":100,
            "_source":["title","province","publish_time","id"],
            "highlight":{
                "fields":{
                    "title":{}
                }
            }
    }
    if key:
        query['query']['bool']['should'] = [{"term": {"title": key}},{"term": {"content": key}}]
    if province:
        query['query']['bool']['must'].append({"match": {"province": '北京'}})
    if publish_time:
        query['query']['bool']['must'].append({"match": {"publish_time": publish_time}})
    # if not key and not province and not area and not publish_time and not c_type:
    #     query = {
    #         "query":{
    #             'match_all': {

    #             }
    #         }
            
    #     }
    print(query)
    search_result = _index.search(index='tender', body=query)['hits']['hits']
    ctx['result'] = [_['_source'] for _ in search_result]
    print(ctx['result'])
    return render(request,'search.html',ctx)


def get(request,object_id):

    ctx = {}
    ctx['object'] = obj = _index.get(index='tender',doc_type='doc',id=object_id)['_source']

    print(obj)
    return render(request,'object.html',ctx)