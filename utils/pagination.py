###自定义分页组件###


from django.utils.safestring import mark_safe

class Pagination(object):

    def __init__(self,request,queryset,page_size=10,page_param='page',plus=5):
        import copy
        query_dict=copy.deepcopy(request.GET)
        query_dict._mutable=True
        self.query_dict=query_dict
        self.page_param=page_param
        
        page=request.GET.get(page_param,'1')
        if page.isdecimal():
            page=int(page)
        else:
            page=1

        self.page=page

        total_count = queryset.count()  # 数据库总条数
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count

        if self.page>self.total_page_count:
            self.page=self.total_page_count
        self.page_size=page_size

        self.start=(self.page-1)*page_size
        self.end=self.page*page_size

        

        self.page_queryset=queryset[self.start:self.end]
        
        

        self.plus=plus

        
    
    def html(self):
        #plus=5
        #计算出显示当前页的前5页和后5页
        if self.total_page_count<=2*self.plus+1:
            #数据库中的数据比较少，都没有达到11页
            start_page=1
            end_page=self.total_page_count
        else:
            #数据库中的数据比较多，超过11页

            #当前页面小于6时，不能出现负数（小极值）
            if self.page<=self.plus:
                start_page=1
                end_page=2*self.plus+1
            else:
                #当前页>5
                #当前页面+5大于总页面
                if (self.page+self.plus)>self.total_page_count:
                    start_page=self.total_page_count-2*self.plus
                    end_page=self.total_page_count
                else:
                    start_page=self.page-self.plus
                    end_page=self.page+self.plus

        #页码
        page_str_list=[]

        #首页
        self.query_dict.setlist(self.page_param,[1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        #上一页
        if self.page>1:
            self.query_dict.setlist(self.page_param, [self.page-1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        #页面
        for i in range(start_page,end_page+1):
            if i==self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        #下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])

            prev = '<li><a href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)
        
        #尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append(
            '<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        #页码搜索框
        search_string='''
        <li>
            <form method='get' class='input-group' style='width: 200px;float: left; margin-left: 3px;'>
                <input type="text" class="form-control" placeholder="页码" name={}>
                <span class="input-group-btn">
                <button class="btn btn-default" type="submit">跳转</button>
                </span>
            </form>
        </li>
        '''.format(self.page_param)
        page_str_list.append(search_string)

        page_string=mark_safe(''.join(page_str_list))

        return page_string
        
    




