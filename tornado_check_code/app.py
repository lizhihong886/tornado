#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import io
import check_code
from session import Session


class BaseHandler(tornado.web.RequestHandler):
    #初始化方法，一调用就立刻执行
    def initialize(self):
        self.session=Session(self)

class IndexHandler(BaseHandler):

    def get(self, *args, **kwargs):
       if self.get_argument('u',None) in ['admin','user']:
           # self.session.set_value('is_login',True)
            self.session['is_login']=True #调用__setitem__方法
       else:
           self.write('<a href=/login>请登录</a>')
    def post(self, *args, **kwargs):
        pass

class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html',status='')

    def post(self, *args, **kwargs):
        user=self.get_argument('user',None)
        pwd=self.get_argument('pwd',None)
        code=self.get_argument('code',None)
        #验证
        check_code=self.session['check_code']
        if code.upper()==check_code.upper():#不区分大小写
            self.write('验证码正确')
        else:
            self.render('login.html',status='验证码错误')


class CheckCodeHandler(BaseHandler):

    def get(self):
        # 很多时候，数据读写不一定是文件，也可以在内存中读写,BytesIO实现了在内存中读写bytes
        mstream = io.BytesIO()#创建一个BytesIO，存在于内存中
        #创建图片，并写入验证码
        img, code = check_code.create_validate_code()
        #将图片对象写入到mstream中
        img.save(mstream, "GIF")
        #为每个用户保存其验证码

        self.session["check_code"] = code
        self.write(mstream.getvalue())#读取图片上的内容，写到页面上



settings = {
    'template_path': 'templates',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': 'aiuasdhflashjdfoiuashdfiuh',
}

application = tornado.web.Application([
    (r"/login", LoginHandler),
    (r'/index',IndexHandler),
    (r"/check_code", CheckCodeHandler),
], **settings)


if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()