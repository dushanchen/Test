from django.shortcuts import render,redirect
from elasticsearch import Elasticsearch
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt

from .models import *
from public.settings import ES_URL


import json
import requests
import datetime
from urllib import parse

# Create your views here.



def weixin_login(request):
    '''获取微信用户信息'''

    if request.method == 'GET':
        code = request.GET.get('code')
        state = request.GET.get('state','/worker/')
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid':'wx3d59f92c7bf0d0f9',
            'secret':'04e6251c3b54340f68e693dafe761a0c',
            'code':code,
            'grant_type':'authorization_code'
            }

        wechat_response = requests.get(url,params=params).json()
        if 'access_token' not in wechat_response:
            return JsonResponse(wechat_response)
        print(wechat_response)
        access_token = wechat_response['access_token']
        open_id = wechat_response['openid']
        print(open_id)

        user = User.objects.filter(open_id=open_id)
        if user.exists():
            request.session['user_id'] = user.first().id
            request.session['open_id'] = user.first().open_id
        else:
            user_info_params = {
                'access_token':access_token,
                'openid':open_id,
                'lang':'zh_CN'
            }

            user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
            user_info = requests.get(user_info_url,params=user_info_params).content

            user_info = json.loads(user_info.decode('utf-8'))
            print('user_info')
            print(user_info)
            if 'nickname' not in user_info:
                return JsonResponse(user_info)
            nickname = user_info['nickname']
            city = user_info['city']
            headimgurl = user_info['headimgurl']

            user = User.objects.create(open_id=open_id, nickname=nickname, city=city, avatar_url=headimgurl)
            request.session['user_id'] = user.id
            request.session['open_id'] = open_id
            print('request.session = open_id')
            print(open_id)
        return redirect(state)




def check_user(func):

    def view(request,*args,**kwargs):

        if 'user_id' not in request.session:
            redirect_uri = request.path
            
            return redirect('/login?redirect_uri='+redirect_uri)

        user_id = request.session['user_id']
        user = User.objects.filter(id=user_id).first()
        user.last_login_time = datetime.datetime.now()

        return func(request,*args,**kwargs)

    return view



def login(request):
    '''获取code'''

    redirect_uri = request.GET.get('redirect_uri','/worker/')

    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?'
    params = {
        'appid':'wx3d59f92c7bf0d0f9',
        'response_type':'code',
        'redirect_uri':'http://127.0.0.1:8000/weixin/login/',
        'scope':'snsapi_userinfo',
        'state':redirect_uri
    }
    print(params)
    return redirect(url + parse.urlencode(params))


@check_user
def mine(request):
    ctx = {'self': True}

    openid = request.session['open_id']
    ctx['user'] = user = User.objects.filter(open_id=openid, status=0).first()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        ctx['type'] = type_ = request.POST.get('type', '')
        if action == 'show_phone':
            show_phone = request.POST.get('show_phone', 0)
            user.show_phone = show_phone
            user.save()
            return JsonResponse({'result':'success'})

        if action == 'type':
            ctx['type'] = type_ = request.POST.get('type', '')
            print(type_)
            if user.exists():
                ctx['user'] = user = user.first()
                if type_ == 'Employer':
                    user.type = 0
                else:
                    user.type = 1
                user.save()
            return render(request, 'mine.html', ctx)
    print(user)
    
    if user.type is None:
        return render(request, 'type.html', ctx)

    return render(request, 'mine.html', ctx)


@check_user
def detail(request, user_id):
    ctx = {'self': False}

    ctx['user'] = user = User.objects.filter(id=user_id, status=0).first()

    return render(request, 'mine.html', ctx)

@check_user
def edit(request):
    ctx = {}
    id = request.session['user_id']

    user = User.objects.filter(id=id)
    ctx['user'] = user = user.first()
    ctx['skills'] = skills = Skill.objects.all()

    print(user)
    if request.method == 'POST':
        
        skills = request.POST.getlist('skill', [])
        if user:
            _save_attr_(user, request)

            user.skill.clear()

            for _ in skills:

                user.skill.add(Skill.objects.filter(id=int(_)).first())

            return redirect(mine)
    return render(request, 'edit.html', ctx)


@check_user
def worker(request):
    '''工人'''

    ctx = {}
    user = request.user

    workers = User.objects.filter(type=1).order_by('-create_time')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'search':
            name = request.POST.get('name', '')
            skill_id = request.POST.get('skill_id', '')
            if skill_id:
                workers = Skill.objects.get(id=skill_id).user_set.all().filter(type=1)
            if name:
                workers = workers.filter(name__contains=name)

    ctx['workers'] = workers

    return render(request,'worker.html',ctx)


@check_user
def employer(request):
    '''雇主,包工'''
    
    ctx = {}
    user = request.user

    employers = User.objects.filter(type=0).order_by('-create_time')

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'search':
            name = request.POST.get('name', '')
            skill_id = request.POST.get('skill_id', '')
            if skill_id:
                employers = Skill.objects.get(id=skill_id).user_set.all().filter(type=0).order_by('-create_time')
            if name:
                employers = employers.filter(name__contains=name)

    ctx['employers'] = employers

    return render(request,'employer.html',ctx)


@csrf_exempt
@check_user
def tender(request):
    _index = Elasticsearch(ES_URL)

    ctx = {}
    
    ctx['page'] = page = int(request.POST.get('page','1'))

    query = {
            "query": {
                "bool": {
                    "must":[
                    ]
                }
            },
            "from": page * 20 -20,
            "size": 20,
            "_source":["title","province","publish_time","id",'source_url'],
            "sort":{
                "publish_time":"desc"
            }
    }
    
    
    if request.method == 'POST':
        ctx['province'] = province = request.POST.get('province','上海')
        ctx['key'] = key = request.POST.get('key','')
        ctx['publish_time'] = publish_time = request.POST.get('publish_time','')
        print(key)
        if key:
            query['query']['bool']['must'].append({'match_phrase': {'title':{'query':key}}})
        if province:
            query['query']['bool']['must'].append({"match": {"province": province}})
        if publish_time:
            query['query']['bool']['must'].append({"match": {"publish_time": publish_time}})
    
    print(query)
    search_result = _index.search(index='tender', body=query)['hits']['hits']
    print(search_result)
    ctx['result'] = [_['_source'] for _ in search_result]

    action = request.POST.get('action','')
        
    if action == 'page':    
        return render(request,'tender_append.html',ctx)

    return render(request,'tender.html',ctx)


def tender_detail(request, tender_id):
    _index = Elasticsearch(ES_URL)

    ctx = {}
    ctx['object'] = obj = _index.get(index='tender',doc_type='tender',id=tender_id)['_source']

    print(obj)
    return render(request,'tender_detail.html',ctx)


def _save_attr_(obj,request):
    fields = obj._meta.fields

    for field in fields:
        field_name = field.name
        value = request.POST.get(field_name, '')
        if value:
            obj.__setattr__(field_name, value)
        else:
            value = request.FILES.get(field_name, '')
            if value:
                obj.__setattr__(field_name, value)
    obj.save()

