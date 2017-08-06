#!/usr/bin/env python
# -*- coding:utf-8 -*-
import config
from hashlib import sha1
import os
import time
import json

#生成随机字符串
create_session_id = lambda: sha1(bytes('%s%s' % (os.urandom(16), time.time()), encoding='utf-8')).hexdigest()


class SessionFactory:

    @staticmethod
    def get_session_obj(handler):
        obj = None

        if config.SESSION_TYPE == "cache":
            obj = CacheSession(handler)
        elif config.SESSION_TYPE == "memcached":
            obj = MemcachedSession(handler)
        elif config.SESSION_TYPE == "py_redis":
            obj = RedisSession(handler)
        return obj


class CacheSession:
    session_container = {}
    session_id = "__sessionId__"

    def __init__(self, handler):
        self.handler = handler
        client_random_str = handler.get_cookie(CacheSession.session_id, None)
        if client_random_str and client_random_str in CacheSession.session_container:
            self.random_str = client_random_str
        else:
            self.random_str = create_session_id()
            CacheSession.session_container[self.random_str] = {}

        expires_time = time.time() + config.SESSION_EXPIRES
        handler.set_cookie(CacheSession.session_id, self.random_str, expires=expires_time)

    def __getitem__(self, key):
        ret = CacheSession.session_container[self.random_str].get(key, None)
        return ret

    def __setitem__(self, key, value):
        CacheSession.session_container[self.random_str][key] = value

    def __delitem__(self, key):
        if key in CacheSession.session_container[self.random_str]:
            del CacheSession.session_container[self.random_str][key]

import redis

pool = redis.ConnectionPool(host='192.168.49.130', port=6379)
r = redis.Redis(connection_pool=pool)
class RedisSession:
    session_id = "__sessionId__"

    def __init__(self, handler):
        self.handler = handler
        #从客户端获取随机字符串
        client_random_str = handler.get_cookie(RedisSession.session_id, None)
        # 判断客户机是否有随机字符串，还有服务器端是否也存在，防止服务端重启后，数据被清空
        if client_random_str and r.exists(client_random_str) :
            self.random_str = client_random_str
        else:
            self.random_str = create_session_id()#生成随机字符串
            r.hset('self.random_str',None,None)#创建Session

        #来一次访问更新一下时间
        r.expire('self.random_str', config.SESSION_EXPIRES)
        expires_time = time.time() + config.SESSION_EXPIRES
        handler.set_cookie(RedisSession.session_id, self.random_str, expires=expires_time)

    def __getitem__(self ,key):
        ret_str=r.hget(self.random_str,key)
        #判断是否为空
        if ret_str:
            #不为空则检测索取所取的值是否能loads
            try:
                ret=json.loads(ret_str)
            except:
                ret=ret_str
            return ret

    def __setitem__(self, key, value):
        if type(value)==dict:
            r.hset(self.random_str,key,json.dumps(value))#因为value是会以字符串的形式写进redis里的，故先把其dumps成字符串，方便后面的取值操作通过loads还原其类型
        else:
            r.hset(self.random_str, key,value)

    def __delitem__(self, key):
        r.hdel(self.random_str,key)


import memcache
mc=memcache.Client(['192.168.49.130:12000'],debug=True) #连接
mc.set('session_container',json.dumps({}))#由于Memcached存储的是字符串类型，因此我们需把dict给json.dumps
class MemcachedSession:
    session_id = "__sessionId__"

    def __init__(self, handler):
        self.handler = handler
        #从客户端获取随机字符串
        client_random_str = handler.get_cookie(MemcachedSession.session_id, None)

        s_c = json.loads(mc.get('session_container'))
        # 判断客户机是否有随机字符串，还有服务器端是否也存在，防止服务端重启后，数据被清空
        if client_random_str and client_random_str in s_c:
            self.random_str = client_random_str
        else:
            self.random_str = create_session_id()
            s_c[self.random_str] = {}
            mc.set('session_container', json.dumps(s_c), config.SESSION_EXPIRES)

        #来一次访问更新一下时间
        mc.set('session_container',json.dumps(s_c),config.SESSION_EXPIRES)
        expires_time = time.time() + config.SESSION_EXPIRES
        handler.set_cookie(MemcachedSession.session_id, self.random_str, expires=expires_time)

    def __getitem__(self ,key):
        s_c = json.loads(mc.get('session_container'))
        ret = s_c[self.random_str].get(key, None)
        return ret

    def __setitem__(self, key, value):
        s_c = json.loads(mc.get('session_container'))
        s_c[self.random_str][key] =value
        mc.set('session_container',json.dumps(s_c),config.SESSION_EXPIRES)

    def __delitem__(self, key):
        s_c = json.loads(mc.get('session_container'))
        if key in s_c[self.random_str]:
            del s_c[self.random_str][key]
            mc.set('session_container', json.dumps(s_c), config.SESSION_EXPIRES)

