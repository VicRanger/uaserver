from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import User
import re
import random
from django.utils import timezone
# Create your views here.


def is_valid_phone(phone):
    if len(phone) != 11:
        return False
    pat = r'^1[3458]\d{9}$'
    res = re.match(pat, phone)
    return False if res == None else True


def is_valid_username(username):
    if len(username) < 3 or len(username) > 11:
        return False
    pat = r'^[a-z][a-z0-9_]+$'
    res = re.match(pat, username)
    return False if res == None else True


def is_valid_password(password):
    if len(password) < 6 or len(password) > 16:
        return False
    pat = r'^[a-zA-Z0-9?~!@#$%^&*_]+$'
    res = re.match(pat, password)
    return False if res == None else True


def find_user_by_username(query):
    if 'username' in query:
        user = User.objects.filter(username=query['username'])
        return user
    return None

@csrf_exempt
def check_phone(req):
    if(req.method == "POST"):
        query = req.POST.dict()
        ret = {}
        ret['query'] = query
        if not('phone' in query):
            ret['msg'] = "未提供手机号码，无法完成用户验证"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not(is_valid_phone(query['phone'])):
            ret['msg'] = "非法的手机号码，无法完成用户验证"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        users_query = User.objects.filter(phone=query['phone'])
        user = None
        if users_query.count()>0:
            user = users_query[0]
            if user.is_phone_verified:
                ret['msg'] = "手机号码已激活"
                ret['status'] = -1
                return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret['msg'] = "没有找到该手机号的预留信息，确认手机已收到验证码后再次发送请求"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not('idcode' in query):
            ret['msg'] = "手机号码已找到，但未提供验证码"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if query['idcode'] == user.idcode:
            user.is_phone_verified = False
            user.save()
            ret['msg'] = "手机号码验证成功"
            ret['status'] = 1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        else:
            ret['msg'] = "手机号码已找到，但验证码错误"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
    if(req.method == "GET"):
        query = req.GET.dict()
        ret = {}
        ret['msg'] = "用GET方法无法完成check_phone请求，请改用POST方法"
        return HttpResponse(json.dumps(ret, ensure_ascii=False))

'''
used to register the phone number
and send message to verify the phone number
(one phone number refers to one person)

http_params:
    phone: phone number

http_rets:
    msg: information
    status: -1(fail) 1(success)
'''
@csrf_exempt
def send_phone(req):
    if(req.method == "POST"):
        query = req.POST.dict()
        ret = {}
        ret['query'] = query
        if not('phone' in query):
            ret['msg'] = "未提供手机号码，无法完成用户创建"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not(is_valid_phone(query['phone'])):
            ret['msg'] = "非法的手机号码，无法完成用户创建"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        users_query = User.objects.filter(phone=query['phone'])
        user = None
        if users_query.count()>1:
            ret['msg'] = "手机号存在重复情况，有问题请联系管理员"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if users_query.count()==1:
            user = users_query[0]
            if user.is_phone_verified:
                ret['msg'] = "手机号码已激活"
                ret['status'] = -1
                return HttpResponse(json.dumps(ret, ensure_ascii=False))
            ret['msg'] = "手机号码已存在，但未激活"
        else:
            user = User()
            user.phone = query['phone']
            user.save()
            ret['msg'] = "手机号码已创建，但未激活"
        idcode = "%04d" % (random.randint(0,9999))
        ret['idcode'] = idcode
        user.idcode = idcode
        user.idcode_time = timezone.now
        user.save()
        ret['status'] = 1
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
    if(req.method == "GET"):
        query = req.GET.dict()
        ret = {}
        ret['msg'] = "用GET方法无法完成send_phone请求，请改用POST方法"
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


'''
use when phone has been verified
then user loads in his password

http_params:
    phone: phone number
    password: user password 

http_rets:
    msg: info
    status: -1(failure) 1(success)
'''
@csrf_exempt
def signup(req):
    if(req.method == "POST"):
        query = req.POST.dict()
        ret = {}
        if not('phone' in query):
            ret['msg'] = '未提供手机号，无法完成注册'
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not(is_valid_phone(query['phone'])):
            ret['msg'] = "手机号码不符合要求"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        user_query = User.objects.filter(phone=query['phone'])
        if user_query.count() > 0:
            user = user_query[0]
        else:
            ret['msg'] = "该手机号码未进行验证"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if user.is_activated:
            ret['msg'] = "该手机号码对应的用户已注册完毕"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not(user.is_phone_verified):
            ret['msg'] = "该手机号码已在数据库，但还未通过验证"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not('password' in query):
            ret['msg'] = "该手机号码已验证，但缺少密码信息"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        if not(is_valid_password(query['password'])):
            ret['msg'] = "密码不符合要求"
            ret['status'] = -1
            return HttpResponse(json.dumps(ret, ensure_ascii=False))
        # user.username = query['username']
        user.password = make_password(query['password'])
        user.raw_password = query['password']
        user.is_activated = True
        user.save()
        ret['msg'] = '手机号码已验证，密码录入成功'
        ret['status'] = 1
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
    if(req.method == "GET"):
        ret = {}
        ret['msg'] = '用GET方法无法完成signup请求，请改用POST方法'
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


@csrf_exempt
def login(req):
    if(req.method == "POST"):
        query = req.POST.dict()
        ret = {}
        user = None
        if 'phone' in query:
            user = User.objects.filter(username=query['phone'])
        if user!=None and user.count() == 1:
            if check_password(query['password'], user[0].password):
                ret["status"] = 1
                ret["msg"] = '登录成功'
            else:
                ret["status"] = 0
                ret["msg"] = '密码错误'
        else:
            ret["status"] = -1
            ret["msg"] = '用户不存在'
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
        ret['msg'] = "无效请求"
        return HttpResponse(json.dumps(ret, ensure_ascii=False))


def users_to_list(users):
    ret = []
    for user in users:
        item = {}
        item['username'] = user.username
        item['phone'] = user.phone
        ret.append(item)
    return ret


@csrf_exempt
def user(req):
    if(req.method == "GET"):
        query = req.GET.dict()
        print(query)
        ret = {}
        user = find_user_by_username(query)
        ret['data'] = users_to_list(user)
        ret['query'] = query
        ret['msg'] = "查询成功"
        return HttpResponse(json.dumps(ret, ensure_ascii=False))
