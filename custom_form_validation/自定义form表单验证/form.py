#!/usr/bin/env/ python
# -*-coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from hashlib import sha1
import os,time
import re

class MainForm(object):
    def __init__(self):
        self.host='(.*)'
        self.ip="^(25[0-5]|2[0-4]\d|[0-1]?/d?/d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$"
        self.port="(\d+)"
        self.phone="~1[3][4][5][8][0-9]\d{8}$"

    def check_valid(self,request):
        form_dict=self.__dict__  #获取对象中的所有成员
        for key,regular in form_dict.items():
            post_value=request.get_argument(key)
            ret=re.match(regular,post_value) #正则匹配
            print(key,ret,post_value)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self, *args, **kwargs):
        obj=MainForm()
        result=obj.check_valid(self)
        self.write("Ok")

settings={
    'static_path':'static',
    'static_url_prefix':'/static/',
    'cookie_secret':'aiuasdhflashjdfoiuashdfiuh',
    'login_url':'/login'
}

application=tornado.web.Application([
    (r'/index',MainHandler),

],**settings)

if __name__=='__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()