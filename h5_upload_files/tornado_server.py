#!/usr/bin/env/ python
# -*-coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import os
import datetime


class MainHandler(tornado.web.RequestHandler):
    def get(self):

        self.render('demo.html')

    def post(self, *args, **kwargs):
        today=datetime.datetime.today()
        file_metas = self.request.files.get('image_file',[])#通过input的name作为键取值
        for meta in file_metas:
            file_name = meta['filename']
            dir_name="image_upload"+'/%d/%d'%(today.year,today.month)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            with open(os.path.join(dir_name,file_name),'wb') as up:
                up.write(meta['body'])

settings = {
    'template_path': '',
    'static_path':'static',
}

application = tornado.web.Application([
    (r"/upload", MainHandler),
], **settings)


if __name__ == "__main__":
    application.listen(8282)
    tornado.ioloop.IOLoop.instance().start()

