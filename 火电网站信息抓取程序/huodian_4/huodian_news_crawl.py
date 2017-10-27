# -*- coding: utf-8 -*-

from contextlib import closing
from pyquery import PyQuery as pq
import datetime
import hashlib
import re
import requests

from t3c.manager.db import DB


class HuoDianNewsCrawl():
   def __init__(self):
      self.db = DB()
      self.now = datetime.datetime.now()
      self.session = requests.Session()
      self.url = 'http://huodian.bjx.com.cn/'

   def get_html(self, url):
      head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) '\
              'Gecko/20100101 Firefox/56.0'}

      html = requests.get(url, headers=head)

      return html

   def get_block(self, block_class_name):
      block_data = pq(self.get_html(self.url).content)

      return block_data('.{0}'.format(block_class_name)).html()

   def get_date(self, url):
      date_html = self.get_html(url)
      date_data = pq(date_html.content)

      return date_data('.{0}'.format('list_copy')).find('b').eq(0).text()

   def get_source(self, url):
      source_html = self.get_html(url)
      source_data = pq(source_html.content)

      return source_data('.{0}'.format('list_copy')).find('b').eq(1).text()

   def save_key_of_index_data(self):
      block = self.get_block('cnt2left')
      block_data = pq(block)
      result = []
      temp_dic = {}

      for i in range(block_data('li').length):
         str = block_data('li').eq(i).find('a').attr('href')
         title = block_data('li').eq(i).find('a').attr('title')
         date = self.get_date(str)
         source = self.get_source(str)

         if str and title:
            if re.match(r'http', str):
               temp_dic[title + '~' + str + '~' + date + '~' + source] = ''
               result.append(temp_dic)
               temp_dic = {}

      return result

   def get_article(self, url):
      article_html = self.get_html(url)
      article_data = pq(article_html.content)

      return article_data('#{0}'.format('content')).text()

   def save_value_of_index_data(self):
      data = self.save_key_of_index_data()
      temp_list = []

      for dic in data:
         temp_dic = {}
         article_url = list(dic.keys())[0].split('~')[1]
         article = self.get_article(article_url)

         if article:
            temp_dic[list(dic.keys())[0]] = article
            temp_list.append(temp_dic)

      return temp_list

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def qxd_list(self):
      insert_sql = 'INSERT INTO "plant_app_etl"."tb_etl_huodian_news" '\
                     '(datetime,title,href,source,content,content_sha1)' \
                     'VALUES (%(datetime)s, %(title)s,%(href)s,%(source)s,'\
                     ' %(content)s, %(content_sha1)s);'
      update_sql = 'UPDATE "plant_app_etl"."tb_etl_huodian_news" SET ' \
                     ' href=%(href)s, content=%(content)s , source=%(source)s,'\
                     ' content_sha1=%(content_sha1)s' \
                     ' WHERE (title=%(title)s AND datetime=%(datetime)s);'
      data_list = self.save_value_of_index_data()

      for data_dic in data_list:
         con = {}
         con['content'] = list(data_dic.values())[0]
         con['title'] = list(data_dic.keys())[0].split('~')[0]
         con['href'] = list(data_dic.keys())[0].split('~')[1]
         con['source'] = list(data_dic.keys())[0].split('~')[2]
         con['datetime'] = list(data_dic.keys())[0].split('~')[3]
         con['content_sha1'] = hashlib.sha1(con['content'].encode('utf-8')).hexdigest().upper()

         self.update_insert(insert_sql, update_sql, con)

if __name__ == '__main__':
   hd = HuoDianNewsCrawl()
   hd.qxd_list()