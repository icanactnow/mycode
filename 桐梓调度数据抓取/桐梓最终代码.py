# -*- coding:utf-8 -*-
import json
import requests
from random import random
from contextlib import closing
from pyquery import PyQuery as pq
from datetime import datetime, timedelta

from t3c.manager.db import DB

class TongziNetContent(object):
   def __init__(self):
      super(TongziNetContent, self).__init__()
      self.headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows '
                                    'NT 6.3; WOW64; Trident/7.0; .NET4.0E; .NET4.0C; '
                                    '.NET CLR 3.5.30729; .NET CLR 2.0.50727; .NET CLR 3.0.30729)'}
      self.url = 'http://10.52.2.238:8080/DRC/drc/ddbb/ddrb/query/ddrb_content.non'
      self.db = DB()

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def get_dlqk_json(self, pq_obj):
      datas = []

      for item in pq_obj('#sectionMain').find('td'):
         data = pq(item).text()

         if not data:
            data = '0'

         datas.append(data)

      dlqk_json = '{"text": "电量情况", "placeholder": "请输入一级分类名称", "key": %.17f, ' \
          '"children":[%s, %s, %s]}'
      sjfdl_json = '{"text": "实际发电量", "placeholder": "请输入二级分类名称", "key": %.17f, ' \
           '"values":[{"text": "实际发电量", "key": %.17f, "inputValue": "%s"}]}'
      sjfdl_list = [datas[0], datas[1], datas[6], datas[7], datas[12], datas[13], datas[24], datas[25], datas[30],
                 datas[31], datas[36], datas[37], datas[42], datas[43], datas[48], datas[49], datas[54], datas[55]]
      sjfdl_json = sjfdl_json % (random(), random(), self.partition(sjfdl_list))
      jhfdl_json = '{"text": "计划发电量", "placeholder": "请输入二级分类名称", "key": %.17f, ' \
           '"values":[{"text": "计划发电量", "key": %.17f, "inputValue": "%s"}]}'
      jhfdl_list = [datas[2], datas[3], datas[8], datas[9], datas[14], datas[15], datas[26], datas[27], datas[32],
                 datas[33], datas[38], datas[39], datas[50], datas[51], datas[56], datas[57]]
      jhfdl_json = jhfdl_json % (random(), random(), self.partition(jhfdl_list))
      fdfhl_json = '{"text": "发电负荷率", "placeholder": "请输入二级分类名称", "key": %.17f, ' \
           '"values":[{"text": "发电负荷率", "key": %.17f, "inputValue": "%s"}]}'
      fdfhl_list = [datas[4], datas[5], datas[10], datas[11], datas[16], datas[17], datas[28], datas[29],
                 datas[34], datas[35], datas[40], datas[41], datas[52], datas[53], datas[58], datas[59]]
      fdfhl_json = fdfhl_json % (random(), random(), self.partition(fdfhl_list))
      dlqk_json = dlqk_json % (random(), sjfdl_json, jhfdl_json, fdfhl_json)

      return dlqk_json

   def partition(self, _list, _size=2):
      value = []
      data = [_list[i:i + _size] for i in range(0, len(_list), _size)]

      for x in data:
         value.append(' '.join(x))

      return ','.join(value)

   def get_ssdqk_json(self, pq_obj):
      datas = []

      for item in pq_obj('#sectionSsd').find('td'):
         data = pq(item).text()

         if not data:
            data = '0'

         datas.append(data)

      base_json = '{"text": "送售电情况", "placeholder": "请输入一级分类名称", "key": %.17f, ' \
           '"values":[%s],"children":[]}'
      base_str =  ',{"key": %.17f, "text":"%s", "inputValue": "送受电量 %s, 计划电量 %s,' \
                  '完成比 %s, 最高负荷 %s, 最低负荷 %s"}'
      temp_str = ''

      for i in range(5):
         i = i*6
         data = datas[i:i+6]
         data.insert(0, random())
         temp_str += base_str % (tuple(data))

      ssdqk_json = base_json % (random(), temp_str[1:])

      return ssdqk_json

   def get_jzqk_json(self, pq_obj):
      datas = []

      for item in pq_obj('#sectionJlqk').find('td'):
         data = pq(item).text()

         if not data:
            data = '0'

         datas.append(data)

      data = [datas[i:i + 8] for i in range(0, len(datas), 8)]
      title = ["装机容量", "检修容量", "停备容量", "受限容量"]
      values = '['
      parse_data = self.parse_jzyxqk(data)

      for i in range(len(parse_data)):
         vlaue = '{"key": %.17f, "text": "%s", "inputValue": "%s"},' % (random(), title[i], parse_data[i])
         values += vlaue

      jzqk_json = '{"key": %.17f, "text": "机组运行情况", "placeholder": "请输入一级分类名称", "values": %s], "children": []}' % (random(), values[:-1])
      return jzqk_json

   def parse_jzyxqk(self, data):
      v1 = []
      v2 = []
      v3 = []
      v4 = []

      for i in data:
         v1.extend(i[0:2])
         v2.extend(i[2:4])
         v3.extend(i[4:6])
         v4.extend(i[6:8])

      return self.partition(v1), self.partition(v2), self.partition(v3), self.partition(v4)

   def get_hdyxqk_json(self, pq_obj):
      datas = []

      for item in pq_obj('#sectionHdyxqk').find('td'):
         data = pq(item).text()

         if not data:
            data = 'null'

         datas.append(data)

      base_json = '{"text": "火电运行情况", "values":[%s], "children":[]}'
      base_json1 = '{"集团":"%s", "电厂名称":"%s", "实际电量":"%s", "计划电量":"%s", "完成率":"%s", '\
      ' "运行":"%s", "备用":"%s", "检修":"%s", "进煤量":"%s", "用煤量":"%s", "应急煤":"%s", '\
      '"存煤量(含应急煤)":"%s", "原煤耗":"%s", "累计进煤量":"%s", "累计耗煤量":"%s", '\
      ' "可用天数":"%s", "装机容量":"%s"}'
      base_json2 = ',{"合计":"%s", "实际电量":"%s", "计划电量":"%s", "完成率":"%s", '\
      ' "运行":"%s", "备用":"%s", "检修":"%s", "进煤量":"%s", "用煤量":"%s", "应急煤":"%s", '\
      '"存煤量(含应急煤)":"%s", "原煤耗":"%s", "累计进煤量":"%s", "累计耗煤量":"%s", '\
      ' "可用天数":"%s", "装机容量":"%s"}'
      temp_json = ''

      for i in range(22):
         i = i*17
         temp_json += ',' + base_json1 % tuple(datas[i:i+17])

      temp_json += base_json2 % tuple(datas[-16:])
      hdyxqk_json = (base_json% temp_json[1:])

      return hdyxqk_json

   def get_ddyxjl_json(self, pq_obj):
      data = pq_obj('#sectionYxjl')('.section_content').html()
      ddyxjl_json = '{"key": %.17f, "text": "调度运行记录", "placeholder": "请输入一级分类名称", ' \
             '"values": [{"text": "运行记录", "key": %.17f, "inputValue": "%s"}] ,"children":[]}' % (random(), random(), data)

      return ddyxjl_json

   def get_one_day_datas(self, date):
      one_day_all_datas = []
      data = {}
      data['sdate'] = date
      re = requests.post(self.url, data = data, headers = self.headers)
      json_str = json.loads(re.text)

      if json_str['success'] == False:

         return 'null', 'null'

      htmls = json_str['content']
      pq_obj = pq(htmls)
      dlqk_json = self.get_dlqk_json(pq_obj)
      ssdq_json = self.get_ssdqk_json(pq_obj)
      jzqk_json = self.get_jzqk_json(pq_obj)
      hdyxqk_json = self.get_hdyxqk_json(pq_obj)
      ddyxjl_json = self.get_ddyxjl_json(pq_obj)
      temp_json = ''
      temp_json = '[%s]' % (('%s, %s, %s, %s') % (dlqk_json, ssdq_json, jzqk_json, ddyxjl_json))

      return temp_json, hdyxqk_json

   def save_detial(self, datas, hdyxqk_json):
      insert_sql = 'INSERT INTO "plant_app_core"."tb_daily_production_report" ( date,'\
      'content, create_time, creator) VALUES (%(date)s, %(content)s, %(create_time)s, %(creator)s);'
      update_sql = 'UPDATE "plant_app_core"."tb_daily_production_report" '\
      ' SET content=%(content)s, create_time = %(create_time)s, creator = %(creator)s '\
      'WHERE (date=%(date)s);'
      insert_sql2 = 'INSERT INTO "plant_app_etl"."tb_etl_ddrb" ( date,'\
         'content) VALUES (%(date)s, %(content)s);'
      update_sql2 = 'UPDATE "plant_app_etl"."tb_etl_ddrb" '\
         ' SET content=%(content)s WHERE (date=%(date)s);'

      if datas[1] != 'null':
         con = {}
         con2 = {}
         con['content'] = datas[1]
         con['date'] = datetime.strptime(datas[0], '%Y-%m-%d')
         now = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
         con['create_time'] = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
         con['creator'] = 'admin'
         con2['content'] = hdyxqk_json[1]
         con2['date'] = datetime.strptime(hdyxqk_json[0], '%Y-%m-%d')
         con2['create_time'] = datetime.now()
         con2['creator'] = 'admin'
         self.update_insert(insert_sql, update_sql, con)
         self.update_insert(insert_sql2, update_sql2, con2)

   def get_all_day_datas(self):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute('SELECT MAX(date) FROM plant_app_core.tb_daily_production_report;')
         data = res.fetchall()

      if not data[0][0]:
         last_date = datetime.strptime('2017-10-01', '%Y-%m-%d')
      else:
         last_date = data[0][0]

      last_date_str = datetime.strftime(last_date, '%Y-%m-%d')
      now_date = datetime.now()
      now_date_str = datetime.strftime(now_date, '%Y-%m-%d')
      datas = []
      hdyxqk_json = []

      while last_date_str != now_date_str:
         part1, part2 = self.get_one_day_datas(last_date_str)
         datas.append(last_date_str)
         datas.append(part1)
         hdyxqk_json.append(last_date_str)
         hdyxqk_json.append(part2)
         self.save_detial(datas, hdyxqk_json)
         datas = []
         hdyxqk_json =[]
         last_date += timedelta(days = 1)
         last_date_str = datetime.strftime(last_date, '%Y-%m-%d')

   def start(self):
      self.get_all_day_datas()

if __name__ == '__main__':
   test = TongziNetContent()
   test.start()