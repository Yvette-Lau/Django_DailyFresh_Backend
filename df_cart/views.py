#coding:utf-8
from django.shortcuts import render,redirect

from .models import *

from django.http import JsonResponse

from df_user.user_auth import islogin

# Create your views here.


@islogin
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts':carts,
    }
    return render(request,'df_cart/cart.html',context)


@islogin
def add(request, gid, count):
    # 用户uid购买了gid商品，数量为count
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 查询购物车中是否已经有此商品，如果有则数量增加，如果没有则新增
    carts = CartInfo.objects.filter(user_id=uid,goods_id=gid)
    if len(carts) >=1:
        cart=carts[0]
        cart.count = cart.count + count

    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    # 如果是ajax请求则返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'cart_id': cart.id, 'count': count, 'gid': gid})
    else:
        return redirect('/cart/')



@islogin
def edit(request,cart_id,count):
    count1=1
    try:
        cart=CartInfo.objects.get(pk=int(cart_id))
        count1=cart.count
        cart.count=int(count)
        cart.save()
        data={'ok':0}
    except Exception as e:
        data={'ok':count1}
    return JsonResponse(data)


@islogin
def delete(request,cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)