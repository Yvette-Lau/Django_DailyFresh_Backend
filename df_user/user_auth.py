#coding:utf-8

from django.http import HttpResponseRedirect

def islogin(func):
    '''用户登录认证装饰器'''

    def login_func(request, *args, **kwargs):
        if request.session.has_key('user_id'):
            return func(request, *args, **kwargs)
        else:
            response = HttpResponseRedirect('/user/login/')
            # 登录时会设置一个键为uname的COOKIE，所以在进入某些页面前用此装饰器判断用户是否登录，如果已经登录，则返回该页面的view层方法，正常跳转。如果用户未登录则记录下用户浏览的完整URL，在登录成功后跳转到用户刚才浏览的URL
            response.set_cookie('uri',request.get_full_path)

        return response

    return login_func


