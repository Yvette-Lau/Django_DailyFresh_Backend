#coding=utf-8
from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from .models import *
from hashlib import sha1
from django.http import JsonResponse
from .user_auth import *
from df_goods.models import *
from df_order.models import *



# Create your views here.
# Test account:
# yiting 87654321 yiting163@.com
# yvette 12345678 yvette163@.com



def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):

    #判断用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    #判断两次密码
    if upwd != ucpwd:
        return redirect('/user/register/')

    #密码加密
    s1 = sha1()
    s1.update(upwd.encode('utf-8'))
    sha1_pwd= s1.hexdigest()


    #创建对象
    user = UserInfo()
    user.uname=uname
    user.upwd=sha1_pwd
    user.uemail = uemail
    user.save()

    #注册成功,转到登录页面
    return redirect('/user/login/')


def register_exit(request):
    "判断用户是否存在"
    user_name = request.GET.get('uname')
    print(user_name)
    count = UserInfo.objects.filter(uname=user_name).count()
    return JsonResponse ({'count':count})


def login(request):
    "登录"
    uname = request.COOKIES.get('uname','')
    # ??????
    context = {'error_name':0, 'error_pwd':0, 'title':'登录','uname':uname}
    # ????
    return render(request,'df_user/login.html',context)




# /user/login_handle
def login_handle(request):
    """登录处理"""
    post = request.POST
    uname = post.get('username')
    pwd = post.get('pwd')
    remember = post.get('remember',0)
    try:
        users = UserInfo.objects.get(uname=uname)
        upwd = users.upwd
    except Exception as result:
        # 用户名错误
        context = {'error_name': 1, 'error_pwd': 0, 'title': '用户登录', 'uname': uname, 'upwd': pwd}
        return render(request, 'df_user/login.html', context)
    else:
        s1 = sha1()
        s1.update(pwd.encode('utf-8'))
        upwd2 = s1.hexdigest()
        if upwd2 == upwd:
            response = redirect('/user/info/')
            if remember != 0:
                response.set_cookie('uname', uname, max_age=7*24*3600)
            else:
                response.set_cookie('uname', '', max_age=-1)  # 清空cookie，立马失效
            request.session['user_id'] = users.id
            request.session['user_name'] = uname
            return response
        else:
            # 密码错误
            context = {'error_pwd':1, 'title':'-登录', 'error_name':0, 'uname':uname, 'upwd':pwd}
            return render(request, 'df_user/login.html', context)


@islogin
def user_center_info(request):
    "用户中心"

    user_info = UserInfo.objects.get(id=request.session['user_id'])
    user_email = user_info.uemail
    goods_list = []
    goods_ids = request.COOKIES.get('goods_ids','')
    if goods_ids != '':
        goods_ids = goods_ids.split(',')
        for goods_id in goods_ids:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {
        'user_email':user_email,
        'user_name':request.session['user_name'],
        'title':'用户中心',
        'rphone': user_info.rphone,
        'page_name': 1,
        'goods_list': goods_list,
    }
    return render(request, 'df_user/user_center_info.html', context)

@islogin
def user_center_order(request,pindex):

    """全部订单"""
    order_list = OrderInfo.objects.filter(user_id = request.session['user_id']).order_by('-oid')
    paginator = Paginator(order_list, 4)
    if pindex == '':
        pindex = '1'
    orderlist = paginator.page(int(pindex))
    context = {
        'title': '用户中心',
        'page_name': 1,
        'paginator':paginator,
        'orderlist':orderlist,
    }
    return render(request, 'df_user/user_center_order.html', context)


@islogin
def user_center_site(request):
    "用户中心收货地址"
    users = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        users.reciver = post.get('reciver')
        users.raddress = post.get('uaddress')
        users.zipCode = post.get('upostcode')
        users.rphone = post.get('uphone')
        users.save()
    return render(request, 'df_user/user_center_site.html',{'users':users, 'title': '用户中心'})

@islogin
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')