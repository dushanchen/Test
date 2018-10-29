from django.shortcuts import render,redirect
from django.http import JsonResponse
from urllib import parse
import requests
import json

from .models import *
# Create your views here.



def weixin_login(request):
    '''获取微信用户信息'''

    if request.method == 'GET':
        code = request.GET.get('code')
        state = request.GET.get('state','/worker/')
        print(code)
        print(state)
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        params = {
            'appid':'wx3d59f92c7bf0d0f9',
            'secret':'04e6251c3b54340f68e693dafe761a0c',
            'code':code,
            'grant_type':'authorization_code'
            }

        wechat_response = requests.get(url,params=params).json()
        if 'access_token' not in wechat_response:
            return JsonResponse(result)

        access_token = wechat_response['access_token']
        open_id = wechat_response['openid']
        print(open_id)

        user = User.objects.filter(open_id=open_id)
        if user.exists():
            request.session['user_id'] = user.first().id
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
            user = User.objects.create(open_id=open_id,nickname=nickname,city=city)
            request.session['user_id'] = user.id
        
        return redirect(state)




def check_user(func):

    def view(request,*args,**kwargs):

        if 'user_id' not in request.session:
            redirect_uri = request.path
            print('sdfasdfasfasd')
            return redirect('/login?redirect_uri='+redirect_uri)

        user_id = request.session['user_id']
        request.user = User.objects.filter(id=user_id).first()
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
def worker(request):
    '''工人'''

    ctx = {}
    user = request.user
    if request.method == 'GET':
        return render(request,'worker.html',ctx)

    if request.method == 'POST':
        pass



@check_user
def employer(request):
    '''雇主,包工'''
    
    pass



