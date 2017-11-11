# -*- coding:utf-8 -*-
from pyquery import PyQuery as pq
from datetime import datetime, timedelta
import requests
from contextlib import closing
import json

from t3c.manager.db import DB

class TongZi(object):
   def __init__(self):
      super(TongZi, self).__init__()
      self.headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; .NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)'}
      self.pam = {'_r':'0.5384878307082654'}
      self.url = 'http://10.52.2.238:8080/DRC/drc/ddbb/ddrb/query/ddrb_content.non'
      self.db = DB()

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def list_to_jsondic(self, li):
      st = '{"%s":"%s"'

      for i in range(len(li[::2])-1):
         st += ',"%s":"%s"'

      st += '}'

      return st % tuple(li)

   def list_to_children(self, li):
      lb = []
      st = '{"name": "%s" ,"data":"%s","children":null}'

      for i in range(len(li[::2])-1):
         st += ',{"name": "%s", "data":"%s", "children":null}'

      st = st % tuple(li)

      return st

   def list_to_data(self, li):
      lb = []
      st = '"%s":"%s"'

      for i in range(len(li[::2])-1):
         st += ',"%s":"%s"'

      st = st % tuple(li)

      return st

   def get_1_json(self, p):
      lis = []

      for item in p('#sectionMain').find('td'):
         data = pq(item).text()
         if not data:
            data = '0'
         lis.append(data)

      j = '{"name": "电量情况","data":{"单位":"MWh"},"children":[%s]}'
      j1 = '{"name": "全网发电量","data":{%s},"children":"null"}'
      j1_list = [lis[0],lis[1],lis[6],lis[7],lis[12],lis[13],lis[24],lis[25],lis[30],lis[31],lis[36],lis[37],lis[42],lis[43],lis[48],lis[49],lis[54],lis[55],]
      j1 = j1 % (self.list_to_data(j1_list))
      j2 = '{"name": "计划发电量","data":{%s},"children":"null"}'
      j2_list = [lis[2],lis[3],lis[8],lis[9],lis[14],lis[15],lis[26],lis[27],lis[32],lis[33],lis[38],lis[39],lis[50],lis[51],lis[56],lis[57]]
      j2 = j2 % (self.list_to_data(j2_list))
      j3 = '{"name": "全网发电量负荷率","data":{%s},"children":"null"}'
      j3_list = [lis[4],lis[5],lis[10],lis[11],lis[16],lis[17],lis[28],lis[29],lis[34],lis[35],lis[40],lis[41],lis[52],lis[53],lis[58],lis[59]]
      j3 = j3 % (self.list_to_data(j3_list))
      st = '%s,%s,%s' % (j1,j2,j3)
      j = j % st

      return j

   def get_3_json(self, p):
      li = []

      for item in p('#sectionSsd').find('td'):
         data = pq(item).text()

         if not data:
            data = '0'

         li.append(data)

      j1 = '{"name": "送售电情况","data":[%s],"children":"null"}'
      base_str =  ',{"类型":"%s","送受电量":"%s", "计划电量":"%s", "完成比":"%s", "最高负荷":"%s", "最低负荷":"%s"}'
      st = ''

      for i in range(5):
         i = i*6
         st += base_str % tuple(li[i:i+6])

      json = j1 % st[1:]

      return json

   def get_8_json(self, p):
      li = []

      for item in p('#sectionJlqk').find('td'):
         data = pq(item).text()

         if not data:
            data = '0'

         li.append(data)

      st = '{"name": "机组情况","data":{%s},"children":null}' % self.list_to_data(li)

      return st

   def get_10_json(self, p):
      li = []

      for item in p('#sectionHdyxqk').find('td'):
         data = pq(item).text()

         if not data:
            data = 'null'

         li.append(data)

      j = '{"name": "火电运行情况","data":[%s],"children":null}'
      base_str = '{"集团":"%s", "电厂名称":"%s", "实际电量":"%s", "计划电量":"%s", "完成率":"%s", '\
      ' "运行":"%s", "备用":"%s", "检修":"%s", "进煤量":"%s", "用煤量":"%s", "应急煤":"%s", '\
      '"存煤量(含应急煤)":"%s", "原煤耗":"%s", "累计进煤量":"%s", "累计耗煤量":"%s", '\
      ' "可用天数":"%s", "装机容量":"%s"}'
      base_str1 = ',{"合计":"%s", "实际电量":"%s", "计划电量":"%s", "完成率":"%s", '\
      ' "运行":"%s", "备用":"%s", "检修":"%s", "进煤量":"%s", "用煤量":"%s", "应急煤":"%s", '\
      '"存煤量(含应急煤)":"%s", "原煤耗":"%s", "累计进煤量":"%s", "累计耗煤量":"%s", '\
      ' "可用天数":"%s", "装机容量":"%s"}'
      st = ''

      for i in range(22):
         i = i*17
         st += ',' + base_str % tuple(li[i:i+17])

      st += base_str1 % tuple(li[-16:])
      json = (j% st[1:])

      return json

   def get_11_json(self, p):
      li = []
      data = p('#sectionYxjl')('.section_content').text()
      json = '{"name":"调度运行记录","data":"%s" ,"children":"null"}' % data

      return json

   def get_one_day_datas(self, date):
      one_day_all_datas = []
      dates = {}
      dates['sdate'] = date
      r = requests.post(self.url, data = dates, headers = self.headers, params = self.pam)
      json_str = json.loads(r.text)

      if json_str['success'] == False:

         return 'null','null'

      htmls = json_str['content']
      p = pq(htmls)
      s1 = self.get_1_json(p)
      s3 = self.get_3_json(p)
      s8 = self.get_8_json(p)
      s10 = self.get_10_json(p)
      s11 = self.get_11_json(p)
      js = ''
      js = '[%s]' % (('%s,%s,%s,%s') % (s1,s3,s8,s11))

      return js, s10

   def save_detial(self, datas, s10):
      insert_sql = 'INSERT INTO "plant_app_core"."tb_daily_production_report" ( date,'\
      'content , create_time , creator ) VALUES (%(date)s,%(content)s ,%(create_time)s ,%(creator)s);'

      update_sql = 'UPDATE "plant_app_core"."tb_daily_production_report" '\
      ' SET content=%(content)s , create_time = %(create_time)s , creator = %(creator)s '\
      'WHERE (date=%(date)s);'

      insert_sql2 = 'INSERT INTO "plant_app_core"."tb_huo_dian_qing_kuang" ( date,'\
      'content , create_time , creator ) VALUES (%(date)s , %(content)s ,%(create_time)s ,%(creator)s);'

      update_sql2 = 'UPDATE "plant_app_core"."tb_huo_dian_qing_kuang" '\
      ' SET content=%(content)s , create_time = %(create_time)s , creator = %(creator)s '\
      'WHERE (date=%(date)s);'

      if datas[1] != 'null':
         con = {}
         con2 = {}
         con['content'] = datas[1]
         con['date'] = datetime.strptime(datas[0], '%Y-%m-%d')
         # con['create_time'] = datetime.now().strptime('%Y-%m-%d %H:%M:%S')
         now = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')
         con['create_time'] = datetime.strptime(now,'%Y-%m-%d %H:%M:%S')
         con['creator'] = '10086'

         con2['content'] = s10[1]
         con2['date'] = datetime.strptime(s10[0], '%Y-%m-%d')
         con2['create_time'] = datetime.now()
         con2['creator'] = '10086'
         self.update_insert(insert_sql, update_sql, con)
         self.update_insert(insert_sql2, update_sql2, con2)

   def get_all_day_datas(self):
      last_date = datetime.strptime('2017-10-01', '%Y-%m-%d')
      last_date_str = datetime.strftime(last_date, '%Y-%m-%d')
      now_date = datetime.now()
      now_date_str = datetime.strftime(now_date, '%Y-%m-%d')
      datas = []
      s10 = []

      while last_date_str != now_date_str:
         s1, s2 = self.get_one_day_datas(last_date_str)
         datas.append(last_date_str)
         datas.append(s1)
         s10.append(last_date_str)
         s10.append(s2)
         self.save_detial(datas, s10)
         datas = []
         s10 =[]
         last_date += timedelta(days = 1)
         last_date_str = datetime.strftime(last_date, '%Y-%m-%d')

if __name__ == '__main__':
   t = TongZi()
   t.get_all_day_datas()
