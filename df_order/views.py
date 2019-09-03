from django.shortcuts import render, redirect
from .models import *
from df_user.user_auth import islogin
from df_user.models import UserInfo
from df_cart.models import CartInfo
from datetime import datetime
from django.db import transaction


# Create your views here.

@islogin
def order(request):
    user = UserInfo.objects.get(id = request.session['user_id'])
    cart_ids = request.GET.getlist("cart_id")
    cart_ids_list = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids_list)
    context = {
        'title':'提交订单',
        'page_numeber':1,
        'carts':carts,
        'cart_ids':','.join(cart_ids),
        'user':user,
    }
    return render(request, 'df_order/place_order.html',context)


'''
事务：一旦操作失败则全部回退
1、创建订单对象
2、判断商品的库存
3、创建详单对象
4、修改商品库存
5、删除购物车
'''



@transaction.atomic
@islogin
def order_handle(request):
    tran_id = transaction.savepoint()    #创建还原点
    cart_ids = request.POST.get('cart_ids')
    try:
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' %(now.strftime('%Y%m%d%H%M%S'), uid)
        order.odate = now
        order.oaddress = request.POST.get('address')
        order.ototal = 0
        order.save()

        #创建详细对象
        cart_ids = [int(item) for item in cart_ids.split(',')]
        total = 0
        for id1 in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order
            #查询购物信息
            cart =CartInfo.objects.get(id=id1)
            #库存
            goods = cart.goods
            if goods.ginventory >= cart.count:
                goods.ginventory = cart.goods.ginventory - cart.count
                goods.save()
                # 完善详单信息
                detail.goods_id = goods.id  #做聚合查询

                detail.price = goods.gprice
                detail.count = cart.count
                detail.subtotal = goods.gprice * cart.count
                detail.save()

                total = total + goods.gprice * cart.count

                cart.delete()

            else: # 如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')

        # 满88元包邮，否则10元邮费
        if total > 88:
            order.ototal = total

        else:
            order.ototal = total + 10
        order.save()
        transaction.savepoint_commit(tran_id)  # 提交事务

    except Exception as e:
        print('================%s' %e)
        transaction.savepoint_rollback(tran_id)  # 失败回滚

        # 保存总价
    return redirect('/user/order/')


@islogin
def pay(request,oid):
    order_detail = OrderDetailInfo.objects.get(oid=oid)
    order = OrderInfo.objects.get(oid=oid)
    order_detail.order.oIspay = True
    order.zhifu = 1
    order_detail.order.save()
    order.save()
    context = {
        'order_detail':order_detail,
        'order' : order
    }
    return render(request, 'df_order/pay.html', context)
