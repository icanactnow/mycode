# -*- coding:utf-8 -*-
from pyquery import PyQuery as pq
from datetime import datetime , timedelta
import requests
from contextlib import closing
import json

from t3c.manager.db import DB

class TongZi(object):
   """docstring for TongZi"""
   def __init__(self):
      super(TongZi, self).__init__()
      self.headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)'}
      self.pam = {'_r':'0.5384878307082654'}
      self.url = 'http://10.52.2.238:8080/DRC/drc/ddbb/ddrb/query/ddrb_content.non'
      # self.db = DB
      self.db = DB()

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def get_date_list(self):
      last_date = datetime.strptime('2017-10-01 18:19:59', '%Y-%m-%d %H:%M:%S')
      limt_date_str = str(datetime.now()- timedelta(days= 1))[:10]
      # print(limt_date_str)
      date_list= []
      temp_date = last_date
      while True:
         if str(temp_date)[:10] == limt_date_str:
            date_list.append(str(temp_date)[:10])
            break
         date_list.append(str(temp_date)[:10])
         temp_date += timedelta(days = 1)
      return date_list

   def list_to_jsondic(self,li):
      st = '{"%s":"%s"'
      for i in range(len(li[::2])-1):
         st += ',"%s":"%s"'
      st += '}'
      return st % tuple(li)

   def list_to_children(self,li):
      lb = []
      st = '{"name": "%s" ,"data":"%s","children":null}'
      for i in range(len(li[::2])-1):
         st += ',{"name": "%s" ,"data":"%s","children":null}'
      st = st % tuple(li)
      return st

   def get_1_json(self,lis,date):
      if date == '2017-10-09':
         lis.insert(6,0)
         lis.insert(18,0)
      if date == '2017-10-10':
         lis.insert(28,0)
         lis.insert(34,0)
      j1 = '{"name": "电量情况","data":{"单位":"MWh"},"children":[%s]}'
      j12 = '{"name": "全网发电量","data":"%s","children":[%s]}'
      j13 = '{"name": "计划发电量","data":"%s","children":[%s]}'
      j14 = '{"name": "全网发电量负荷率","data":"%s","children":[%s]}'
      j15 = '{"name": "全省供电量","data":"%s","children":[%s]}'
      j12 = j12 % (lis[8],self.list_to_children(lis[7:-14][::3]))
      j13 = j13 % (lis[10],self.list_to_children(lis[9:-14][::3]))
      j14 = j14 % (lis[12],self.list_to_children(lis[11:-12][::3]))
      j15 = j15 % (lis[-13],self.list_to_children(lis[-14:]))
      st = '%s,%s,%s,%s' % (j12,j13,j14,j15)
      j1 = j1 % st
      return j1

   def get_3_json(self,li):
      j1 = '{"name": "送售电情况","data":{"单位":"MWh、MW"},"children":[%s]}'
      j12 = '{"name": "黔电送粤","data":[%s],"children":null}'
      j13 = '{"name": "送重庆","data":[%s],"children":null}'
      j14 = '{"name": "送湖南","data":[%s],"children":null}'
      j15 = '{"name": "麻丹县送广西","data":[%s],"children":null}'
      j16 = '{"name": "合计","data":[%s],"children":null}'
      st =  '{"送受电量":"%s", "计划电量":"%s", "完成比":"%s", "最高负荷":"%s", "最低负荷":"%s"}'
      j12 = j12 % ( st % tuple(li.eq(1).text().split(' ')[1:]))
      j13 = j13 % ( st % tuple(li.eq(2).text().split(' ')[1:]))
      j14 = j14 % ( st % (0,0,0,0,0))
      j15 = j15 % ( st % tuple(li.eq(4).text().split(' ')[1:]))
      j16 = j16 % ( st % tuple(li.eq(5).text().split(' ')[1:]))
      return j1 % ('%s,%s,%s,%s,%s' % (j12,j13,j14,j15,j16))
      st = '{"name": "负荷情况","data":{"单位":"MWh、MW"},"children":[%s]}'
      di = self.list_to_jsondic(li[1:])
      return st % di

   def get_8_json(self,li):
      st = '{"name": "机组情况","data":{"单位":"MW"},"children":[%s]}'
      if len(li) == 24:
         li.insert(19,0)
      di = self.list_to_jsondic(li[1:])
      return st % di

   def get_one_day_datas(self,date):
      one_day_all_datas = []
      dates = {}
      dates['sdate'] = date
      r = requests.post(self.url, data = dates, headers = self.headers, params = self.pam)
      json_str = json.loads(r.text)
      if json_str['success'] == False:
         return 'null'
      htmls = json_str['content']
      p = pq(htmls)
      d1 = p('#sectionMain').text().split(' ')
      s1 = self.get_1_json(d1,date)
      d3 = p('#sectionSsd').find('tr')
      s3 = self.get_3_json(d3)
      d8 = p('#sectionJlqk').text().split(' ')
      s8 = self.get_8_json(d8)
      s9 = '[%s]' % ('%s,%s,%s' % (s1,s3,s8))
      return s9

   def save_detial(self, datas):
      insert_sql = 'INSERT INTO "plant_app_tcx"."tb_gui_data" (date_str,'\
      'json_data) VALUES (%(date_str)s,%(json_data)s);'

      update_sql = 'UPDATE "plant_app_tcx"."tb_gui_data" SET json_data=%(json_data)s'\
      'WHERE (date_str=%(date_str)s);'

      try:
         con = {}
         print(datas[0])
         con['json_data'] = datas[1]
         con['date_str'] = datetime.strptime(datas[0], '%Y-%m-%d')
         self.update_insert(insert_sql, update_sql, con)
      except Exception as e:
         print(e)

   def get_all_day_datas(self):
      date_list = self.get_date_list()
      datas = []
      for date_str in date_list:
         datas.append(date_str)
         datas.append(self.get_one_day_datas(date_str))
         self.save_detial(datas)
         datas = []

if __name__ == '__main__':
   t = TongZi()
   t.get_all_day_datas()
