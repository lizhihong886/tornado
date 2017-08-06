#!/usr/bin/env/ python
# -*-coding:utf-8 -*-
#自定义session 模块化
container={}
class Session:
    """封装了__getitem__和__setitem__魔法方法"""
    def __init__(self,handler):
        self.handler=handler
        self.random_str=None

    #定义一个生成随机字符串的私有方法，只能内部访问
    def __generate_random_str(self):
        import hashlib
        import time
        obj=hashlib.md5()
        obj.update(bytes(str(time.time()),encoding='utf-8'))
        random_str=obj.hexdigest()
        return random_str

#把随机字符串内生成一个字典对象并写入数据并把随机字符串通过cookie写到客户端
    # def set_value(self,key,value):
    def __setitem__(self, key, value): #魔法方法 使得调用时像字典一样简单赋值
        """
         __setitem__(self, key, value) 定义当一个条目被赋值时的行为,使用 self[key] = value 。这也是可变容器和不可变容器协议中都要有的一部分
        """
        # 判断
        #在container中加入随机字符串
        #定义专属于自己的数据
        #往客户机中写入随机字符串

        #判断，请求用户是否已有随机字符串
        if not self.random_str: #如果container中有
            random_str=self.handler.get_cookie('k1',None)
        #如果没有则生成
            if not random_str:
                random_str = self.__generate_random_str()
                container[random_str] = {}
            else:
                #客户机有随机字符串
                if random_str in container.keys():
                    # 再次确认一下服务器端是否存在，防止服务端重启后，数据被清空
                    pass
                else:
                    random_str=self.__generate_random_str()
                    container[random_str] = {}
        container[random_str][key]=value
        self.handler.set_cookie('k1',random_str)

#获取客户端的随机字符串并取值
    # def get_value(self,key):
    def __getitem__(self, item):#魔法方法 使得调用时像字典一样简单取值
        """
         __getitem__(self, key) 定义当一个条目被访问时，使用符号 self[key] 。这也是不可变容器和可变容器都要有的协议的一部分。如果键的类型错误和 KeyError 或者没有合适的值。那么应该抛出适当的 TypeError 异常
       
        """
        #获取客户端的随机字符串
        #从container中获取我的数据
        #专属信息【key】
        random_str=self.handler.get_cookie("k1")
        if not random_str:
            return None
        #客户机有随机字符串话,获取该字符串在服务器中对应的数据
        user_info_dict=container.get(random_str,None)
        if not user_info_dict:
            #如果服务器中没有的话，cookie有可能是伪造的
            return None
        #获取值
        value=user_info_dict.get(item,None)
        return value


