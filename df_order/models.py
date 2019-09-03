#conding:utf-8
from django.db import models

# Create your models here.


class OrderInfo(models.Model):
    """订单信息"""
    oid = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey('df_user.UserInfo')
    odate = models.DateTimeField(auto_now=True)
    oIspay = models.IntegerField(default=0)
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddress = models.CharField(max_length=150,default='')
    zhifu = models.IntegerField(default=0)


class OrderDetailInfo(models.Model):
    """订单详细信息"""
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    count = models.IntegerField()
    subtotal = models.DecimalField(max_digits=6,decimal_places=2)