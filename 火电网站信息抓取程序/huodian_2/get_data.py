from pyquery import PyQuery as pq
from data import datas
import requests
import re
#http://huodian.bjx.com.cn/

class GetData(object):
    """docstring for get_data"""

    def __init__(self):
        super(GetData, self).__init__()
    #获取一块文本信息
    def get_block(self, block_class_name):
        p = pq(datas)
        return p('.{0}'.format(block_class_name)).html()
    #这里的key存放了文章的标题和链接
    def save_key_of_index_data(self):
        block = self.get_block('cnt2left')
        # print(block)
        d = pq(block)
        ls = []
        dic = {}
        for i in range(d('a').length):
            str = d('a').eq(i).attr('href')
            title = d('a').eq(i).attr('title')
            if str and title:
                if re.match(r'http', str):
                    dic[title + '~' + str] = ''
                    ls.append(dic)
                    dic = {}

        return ls
    #获取网页html
    def get_html(self, url):
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) '
                          'Gecko/20100101 Firefox/55.0'}
        html = requests.get(url, headers=head)
        return html
    #获取网页里面文章部分的内容
    def get_article(self, url):

        article_html = self.get_html(url)
        p = pq(article_html.content)
        return p('#{0}'.format('content')).text()
    #将文章保存到对应的的字典位置
    def save_value_of_index_data(self):
        data = self.save_key_of_index_data()
        temp_list = []
        for dic in data:
            temp_dic = {}
            article_url = list(dic.keys())[0].split('~')[1]  # 获取每篇文章的链接
            article = self.get_article(article_url)
            if article:
                temp_dic[list(dic.keys())[0]] = article
                temp_list.append(temp_dic)
        return temp_list


if __name__ == '__main__':
    te = GetData()
    te.save_value_of_index_data()
