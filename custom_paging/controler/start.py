#!/usr/bin/env/ python
# -*-coding:utf-8 -*-
import tornado.web,tornado.ioloop
from plugin import page_helper
import os

LIST_INFO=[
    {'username':'li','email':'2419636244@qq.com'}
]
class MainHandler(tornado.web.RequestHandler):
    def get(self,page):
        current_page=page
        base_url="/index/"
        pag_obj=page_helper.PagingInfo(current_page,100,10)
        all_page_count=pag_obj.all_page_count
        print(all_page_count)
        pag=pag_obj.paging(all_page_count,base_url)
        print(pag)
        self.render('home/login.html',list_info=LIST_INFO,pag=pag)

    def post(self,*args,**kwargs):
        user=self.get_argument('username')#get_argument通过表单里的name取值
        email=self.get_argument('email')
        temp={'username':user,'email':email}
        LIST_INFO.append(temp)
        print(LIST_INFO)
        self.redirect('/index/1')

BASE_DIR=os.path.dirname(os.path.dirname(__file__))
settings={
    'template_path':os.path.join(BASE_DIR,'views'),
    'static_path':os.path.join(BASE_DIR,'static')
}


application=tornado.web.Application([
    (r'/index/(?P<page>\d*)',MainHandler),
],**settings)

if __name__ == '__main__':
    application.listen('9898')
    tornado.ioloop.IOLoop.instance().start()