import re
import requests
from datetime import datetime
from pyquery import PyQuery as pq
from t3c.manager.db import DB
from contextlib import closing

class get3dHis(object):
   """docstring for get3dHis"""
   def __init__(self):
      super(get3dHis, self).__init__()
      self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
      self.db = DB()

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def save_detial(self, data):
      insert_sql = 'INSERT INTO "sun_tick_datas"."threed_datas" ( date,'\
      'no , num ) VALUES (%(date)s, %(no)s, %(num)s);'

      update_sql = 'UPDATE "sun_tick_datas"."threed_datas" '\
      ' SET num =%(num)s WHERE (date=%(date)s AND no= %(no)s);'

      con = {}
      con['date'] = datetime.strptime(data[0], '%Y-%m-%d')
      con['no'] = int(data[1])
      con['num'] = data[2]

      self.update_insert(insert_sql, update_sql, con)

   def max_no(self):
      max_no_sql = 'SELECT MAX(no) FROM sun_tick_datas.threed_datas'

      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(max_no_sql)
         max_no = res.fetchall()[0][0]
      if not max_no:
         print(2004001)
         return 2004001
      print(max_no)
      return max_no

   def save(self, datas):
      max_no = self.max_no()

      for data in datas:
         if int(data[1]) < max_no:
            return True
         self.save_detial(data)
      return False

   def get_html(self,page):
      url = 'http://kaijiang.zhcw.com/zhcw/inc/3d/3d_wqhg.jsp?pageNum='+str(page)
      html = requests.post(url,headers=self.headers)
      return html.text

   def parse_html(self,html):#f返回页面中的数据list
      data_obj = pq(html)
      # date = data_obj('body')('tbody')
      datas_list = []
      for tr in data_obj('body').find('tr')[2:-1]:
         # print(pq(tr).html())
         data = []
         date = pq(tr).find('td').eq(0).html()
         no =  pq(tr).find('td').eq(1).html()
         num = ''
         for em in pq(tr).find('td').eq(2).find('em'):
            num += pq(em).text()
         data.append(date)
         data.append(no)
         data.append(num)
         datas_list.append(data)
      # print(datas_list)
      return datas_list

   def get_3d_datas_save(self):
      for i in range(1,237):
         datas = []
         html = self.get_html(i)
         datas = self.parse_html(html)
         if self.save(datas):
            break

if __name__ == '__main__':
   t = get3dHis()
   t.get_3d_datas_save()