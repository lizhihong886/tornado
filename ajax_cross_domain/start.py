#!/usr/bin/env/ python
# -*-coding:utf-8 -*-

import tornado.web
import tornado.ioloop

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        callback=self.get_argument('callback')
        self.write('%s([123,456,789])'%callable)
    def post(self, *args, **kwargs):
        pass

settings={'template_path':'views',
          'static_path':'static'}

application=tornado.web.Application([
    (r'/index',IndexHandler)
],**settings)

if __name__=="__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

