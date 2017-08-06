import tornado.ioloop,tornado.web
from session import RedisSession

#既然Index与MangeHandler每次均要调用Session方法，我们何不创建一个基类统一调用，Index与Manage继承基类不就ok了
class BaseHandler(tornado.web.RequestHandler):
    #初始化方法，一调用就立刻执行
    def initialize(self):
        self.session=RedisSession(self)

class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):

       if self.get_argument('u',None) in ['admin','user']:
           # self.session.set_value('is_login',True)
            self.session['is_login']=True #调用__setitem__方法
       else:
           self.write("<a href='/manager'>请登录</a>")
       self.session['is_login']=True
    def post(self, *args, **kwargs):
        pass

class ManageHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # val=self.session.get_value('is_login')
        val=self.session['is_login']#调用__getitem方法
        print(val)
        if val:
            self.write('成功')
        else:
            self.write("失败")
    def post(self, *args, **kwargs):
        pass

application=tornado.web.Application([
    (r'/index',IndexHandler),
    (r'/manager',ManageHandler),
])

if __name__=='__main__':
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()