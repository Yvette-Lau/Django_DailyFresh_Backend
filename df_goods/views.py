#coding=utf-8

from django.shortcuts import render
from django.core.paginator import Paginator,Page
from .models import *
from df_cart.models import *

# Create your views here.


def index(request):

    typelist = TypeInfo.objects.all()
    t0 = typelist[0].id
    t1 = typelist[1].id
    t2 = typelist[2].id
    t3 = typelist[3].id
    t4 = typelist[4].id
    t5 = typelist[5].id
    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]
    context = {
        'title':'首页',
        'guest_cart':1,
        'type0':type0,
        'type01':type01,
        'type1': type1,
        'type11': type11,
        'type2': type2,
        'type21': type21,
        'type3': type3,
        'type31': type31,
        'type4': type4,
        'type41': type41,
        'type5': type5,
        'type51': type51,
        't0':t0,
        't1': t1,
        't2': t2,
        't3': t3,
        't4': t4,
        't5': t5,
    }
    return render(request,'df_goods/index.html',context)


def list(request,typeid, pageid, sort):

    """
        列出水果分类信息
        :param typeid: 分类编号
        :param pageid: 页编号
        :param sort: 排序方式
    """
    typeinfo = TypeInfo.objects.get(id=typeid)
    news = GoodsInfo.objects.all().order_by('-id')[:2]
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id= int(typeid)).order_by('-id')
    elif sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id= int(typeid)).order_by('-gprice')
    elif sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id= int(typeid)).order_by('-gclick')

    paginator = Paginator(goods_list,10)
    page = paginator.page(int(pageid))
    context ={
        'title': typeinfo.ttitle,
        'page': page,
        'paginator': paginator,
        'news':news,
        'typeinfo':typeinfo,
        'guess_cart':1,
        'sort':sort,
        'typeid':typeid,
        # 'cart_count':cart_count(request),
    }

    return render(request, 'df_goods/list.html',context)


#购物车商品数量
def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0

def detail(request, id):
    """
    商品详情
    """
    goodinfor = GoodsInfo.objects.get(pk= int(id))
    goodinfor.gclick += 1
    goodinfor.save()

    news = goodinfor.gtype.goodsinfo_set.order_by('-id')[:2]
    # count = request.session.get('count')

    context = {
        'gtype':goodinfor.gtype,
        'title':goodinfor.gtype.ttitle,
        'g':goodinfor,
        'news':news,
        'id':id,
        'guess_cart':1,

    }

    response = render(request, 'df_goods/detail.html',context)

    # 使用cookies记录最近浏览的商品id

    # 获取cookies
    goods_ids = request.COOKIES.get('goods_ids','')

    # 获取当前点击商品id
    goods_id = '%d'%goodinfor.id
    if goods_ids != '':   # 判断是否有浏览记录，如果有则继续判断
        goods_ids1 = goods_ids.split(',')  # 拆分为列表
        if goods_ids1.count(goods_id)>=1:  # 如果商品已经被记录，则删除
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)  # 添加到第一个

        if len(goods_ids1) >= 6:  # 如果超过6个则删除最后一个
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)  # 拼接为字符串
    else:
        goods_ids = goods_id  # 如果没有浏览记录则直接加

    response.set_cookie('goods_ids', goods_ids)  # 写入cookie 类型为商品id

    return response

from haystack.views import SearchView
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView,self).extra_context()
        context['title'] = '搜索'
        context['guess_cart'] = 1
        context['cart_count'] = cart_count(self.request)
        return context


