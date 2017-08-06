
class PagingInfo:
    '''
    current:当前页
    all_count:所有的信息数
    page_item:每页显示的信息数
    start:当前页显示信息的开始位置
    end:当前页显示信息的结束位置
    all_page_count:总共的页数
    '''
    def __init__(self,current_page,all_count,page_item=5):
        self.current_page=current_page
        self.all_count=all_count
        self.page_item=page_item
    @property #@property属性装饰器，将一个类方法转变成一个类属性，在调用这个方法的时候不用加括号
    def start(self):
        start = (self.current_page - 1) * self.page_item
        return start
    @property
    def end(self):
        end = self.current_page * self.page_item
        return end
    @property
    def all_page_count(self):
        temp = divmod(self.all_count, self.page_item)
        if temp[1] == 0:
            all_page_count = temp[0]
        else:
            all_page_count = temp[0] + 1
        return all_page_count

    def paging(self,page_count,base_url):
        '''
        :param page_count:分页数
        :base_url:路径
        :return:分页标签列表
        '''
        begin=1
        end=12
        index_page=int(self.current_page)
        print(index_page)
        page_count=int(page_count)
        print(page_count)
        print(123)
        if index_page<6:
            begin=0
            end=11if page_count>11 else page_count

        elif index_page+5>page_count:
            begin=index_page-6
            end=page_count
        else:
            begin=index_page-6
            end=index_page+5

        html_item = []
        if index_page == 1:
            firstpage = "<a href=''%s%d' class='selected'>首页</a>" %(base_url,1)
        else:
            firstpage = "<a href=''%s%d'>首页</a>" %(base_url,1)
        html_item.append(firstpage)
        for i in range(begin,end):
            if index_page == i + 1:
                a_html = "<a href='%s%d' class='selected'>%d</a>" % (base_url,i + 1, i + 1)
            else:
                a_html = "<a href='%s%d'>%d</a>" % (base_url,i + 1, i + 1)
            html_item.append(a_html)

        if index_page == 1:
            previous_html = "<a href='%s%d'>上一页</a>" % (base_url,1)
        else:
            previous_html = "<a href='%s%d'>上一页</a>" % (base_url,index_page - 1)
        if index_page == page_count:
            next_html = "<a href='%s%d'>下一页</a>" % (base_url,page_count)
        else:
            next_html = "<a href='%s%d'>下一页</a>" % (base_url,index_page + 1)

        if index_page == page_count:
            lastpage = "<a href='%s%d' class='selected'>尾页</a>"  % (base_url,page_count)
        else:
            lastpage = "<a href='%s%d'>尾页</a>" % (base_url,page_count)

        #页面跳转
        jump="""<input type='text'/ placeholder="总%s页"><a onclick="Jump(%s,%s,this)" style="cursor:pointer">跳转</a>"""%(page_count,page_count,base_url,)
        script="""
        <script>
        function Jump(page_count,base_url,ths){
            var val=ths.previousElementSibling.value;
            if(val.trim().length>0){
                val=parseInt(val)
                if(val>0 && val<page_count+1){
                location.href=base_url+val
                }
            }
        }
        </script>
        """
        html_item.insert(1,previous_html)
        html_item.append(next_html)
        html_item.append(lastpage)
        html_item.append(jump)
        html_item.append(script)

        # 拼接成字符串的形式
        Html_item = (''.join(html_item))
        return Html_item
