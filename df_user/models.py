#coding=utf-8
from django.db import models

# Create your models here.


class UserInfo(models.Model):
    uname = models. CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    reciver = models.CharField(max_length=20,default='')
    raddress = models.CharField(max_length=100,default='')
    zipCode = models.CharField(max_length=6,default='')
    rphone = models.CharField(max_length=11,default='')


