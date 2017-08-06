#!/usr/bin/env python
# -*- coding:utf-8 -*-
import fields


class BaseForm:
    # 定义一个form验证的基类
    def __init__(self):
        self._value_dict = {} #存放数据
        self._error_dict = {} #存放错误信息
        self._valid_status = True #验证状态

    def valid(self, handler):
        #证用户表单请求的数据
        for field_name, field_obj in self.__dict__.items():
            # if field_name.startswith('_'):#过滤私有字段
            #     continue
            if type(field_obj) == fields.CheckBoxField:  #checkbox处理

                post_value = handler.get_arguments(field_name, None)
            elif type(field_obj) == fields.FileField: #文件处理
                post_value = []
                file_list = handler.request.files.get(field_name, [])
                for file_item in file_list:
                    post_value.append(file_item['filename'])
            else:
                post_value = handler.get_argument(field_name, None)

            field_obj.match(field_name, post_value) #正则匹配
            if field_obj.is_valid: #如果验证成功

                self._value_dict[field_name] = field_obj.value
            else:
                self._error_dict[field_name] = field_obj.error  #错误信息
                self._valid_status = False

        return self._valid_status   #返回验证状态

obj=BaseForm()
obj.valid(obj)
