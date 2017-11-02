#-*-coding:utf-8-*-
# -*- coding:utf-8 -*-
from pyquery import PyQuery as pq
from datetime import datetime , timedelta
import requests
from contextlib import closing
import json

from t3c.manager.db import DB
# from jsons import json_str
# r = requests.post(url,data = date, headers = headers, params = pam)

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

   #从数据库有查需要获取的日期列表，默认起始日期为2017-10-01，返回日期列表。
   def get_date_list(self):

      # with closing(db.engine.connect()) as cn:
      #    res = cn.execute('SELECT  date_str FROM '\
      #       'plant_app_tcx.tb_acquisition WHERE province_id = 36000000;')
      #    data = res.fetchall()

      # if data:
      #    last_date = heapq.nlargest(1,data)[0][0] - timedelta(days = 1)
      # else:
      last_date = datetime.strptime('2017-10-01 18:19:59', '%Y-%m-%d %H:%M:%S')
      limt_date_str = str(datetime.now()- timedelta(days= 1))[:10]
      # print(limt_date_str)
      date_list= []
      temp_date = last_date
      while True:
         if str(temp_date)[:10] == limt_date_str:
            date_list.append(str(temp_date)[:10])
            # print(date_list)
            break
         date_list.append(str(temp_date)[:10])
         temp_date += timedelta(days = 1)
      return date_list
   # def get_2_json(self):
   #    li = ['三、送受电情况（单位：MWh、MW）', '类型', '送受电量', '计划电量', '完成比（%）', '最高负荷', '最低负荷', '黔电送粤', '61574', '75850', '81.18', '3902', '1023', '送重庆', '0', '0', '0', '0', '0', '送湖南', '0', '0', '麻丹线送广西', '0', '0', '0', '0', '0', '合计', '61574', '75850', '81.18', '--', '--']
   #    # li = li[7:]
   #    st = ''
   #    j1 = '{"name": "送售电情况","data":{"单位":"MWh、MW"},"children":"%s"}'
   #    # jd = '{"name": "%s","data":"%s","children":null}'
   #    jc = '{"name": "%s","data":null,"children":"%s"}'
   #    jdd = '{"送受电量":"%s", "计划电量":"%s", "完成比（%）":"%s", "最高负荷":"%s", "最低负荷":"%s"}'
   #    print(li)
   def list_to_jsondic(self,li):
      st = '{"%s":"%s"'
      for i in range(len(li[::2])-1):
         st += ',"%s":"%s"'
      st += '}'
      return st % tuple(li)
      # print(st % tuple(li))
   def list_to_children(self,li):
      lb = []
      st = '{"name": "%s" ,"data":"%s","children":null}'
      for i in range(len(li[::2])-1):
         st += ',{"name": "%s" ,"data":"%s","children":null}'
      # st += ']'
      st = st % tuple(li)
      return st
      # print(st)
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
      # print(lis[7:-14])
      # for item in lis[7:-14][::3]:
      #    print(item)
      j12 = j12 % (lis[8],self.list_to_children(lis[7:-14][::3]))
      # j12 = j12 % self.list_to_children(lis[7:-14][::3])
      j13 = j13 % (lis[10],self.list_to_children(lis[9:-14][::3]))
      # j13 = j13 % self.list_to_children(lis[9:-14][::3])
      j14 = j14 % (lis[12],self.list_to_children(lis[11:-12][::3]))
      j15 = j15 % (lis[-13],self.list_to_children(lis[-14:]))
      st = '%s,%s,%s,%s' % (j12,j13,j14,j15)
      # print(j15)
      j1 = j1 % st
      # print(j1)
      return j1
   def get_2_json(self,li):
      j1 = '{"name": "新能源","data":{"单位":"MWh、MW"},"children":[%s]}'
      j12 = '{"name": "风电","data":[%s],"children":null}'
      j13 = '{"name": "光伏","data":[%s],"children":null}'
      j14 = '{"name": "其它","data":[%s],"children":null}'
      j15 = '{"name": "合计","data":[%s],"children":null}'
      st =  '{"装机容量":"%s", "发电量":"%s", "最大出力":"%s", "最小出力":"%s", "受限电力":"%s"}'
      j12 = j12 % (st % tuple(li[8:13]))
      j13 = j13 % (st % tuple(li[14:19]))
      j14 = j14 % (st % tuple(li[20:25]))
      j15 = j15 % (st % tuple(li[-5:]))
      # print(j1 % ('%s,%s,%s,%s' % (j12,j13,j14,j15)))
      return j1 % ('%s,%s,%s,%s' % (j12,j13,j14,j15))
      # pass
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
      # print(j1 % ('%s,%s,%s,%s,%s' % (j12,j13,j14,j15,j16)))
      return j1 % ('%s,%s,%s,%s,%s' % (j12,j13,j14,j15,j16))
      # print(li.eq(1).text())
      # pass
   def get_4_json(self,li):
      st = '{"name": "负荷情况","data":{"单位":"MWh、MW"},"children":[%s]}'
      di = self.list_to_jsondic(li[1:])
      # print(st % di)
      return st % di
   def get_5_json(self,li):
      j1 = '{"name": "用电情况","data":{"单位":"MWh、MW"},"children":[%s]}'
      j12 = '{"name": "贵阳供电局","data":[%s],"children":null}'
      j13 = '{"name": "六盘水供电局","data":[%s],"children":null}'
      j14 = '{"name": "遵义供电局","data":[%s],"children":null}'
      j15 = '{"name": "安顺供电局","data":[%s],"children":null}'
      j16 = '{"name": "铜仁供电局","data":[%s],"children":null}'
      j17 = '{"name": "毕节供电局","data":[%s],"children":null}'
      j18 = '{"name": "凯里供电局","data":[%s],"children":null}'
      j19 = '{"name": "都匀供电局","data":[%s],"children":null}'
      j110 = '{"name": "贵安供电局","data":[%s],"children":null}'
      j111= '{"name": "供黔江","data":[%s],"children":null}'
      j112 = '{"name": "供涪陵","data":[%s],"children":null}'
      j113 = '{"name": "供怀化","data":[%s],"children":null}'
      j114 = '{"name": "供南丹","data":[%s],"children":null}'
      j115 = '{"name": "合计","data":[%s],"children":null}'
      st =  '{"供电量":"%s", "最高负荷":"%s", "最低负荷":"%s", "负荷率":"%s", "供电量环比":"%s"}'
      # print(tuple(li[8:13]))
      j12 = j12 % (st % tuple(li[8:13]))
      j13 = j13 % (st % tuple(li[14:19]))
      j14 = j14 % (st % tuple(li[20:25]))
      j15 = j15 % (st % tuple(li[26:31]))
      j16 = j16 % (st % tuple(li[32:37]))
      j17 = j17 % (st % tuple(li[38:43]))
      j18 = j18 % (st % tuple(li[44:49]))
      j19 = j19 % (st % tuple(li[50:55]))
      j110 = j110 % (st % tuple(li[56:61]))
      j111 = j111 % (st % tuple(li[62:67]))
      j112 = j112 % (st % tuple(li[68:73]))
      j113 = j113 % (st % tuple(li[74:79]))
      j114 = j114 % (st % tuple(li[80:85]))
      l = li[-3:]
      l.insert(1,0)
      l.insert(1,0)
      # print(l)
      j115 = j115 % (st % tuple(l))

      # print(j1 % ('%s,%s,%s,%s' % (j12,j13,j14,j15)))
      return j1 % ('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (j12,j13,j14,j15,j16,j17,j18,j19,j110,j111,j112,j113,j114,j115))
   # 获取一天的数据，返回列表。
   def get_8_json(self,li):
      st = '{"name": "机组情况","data":{"单位":"MW"},"children":[%s]}'
      if len(li) == 24:
         li.insert(19,0)
      di = self.list_to_jsondic(li[1:])
      # print(st % di)
      return st % di
   def get_one_day_datas(self,date):
      one_day_all_datas = []
      dates = {}
      dates['sdate'] = date
      #{'sdate':'2017-10-14'}
      r = requests.post(self.url, data = dates, headers = self.headers, params = self.pam)
      json_str = json.loads(r.text)
      # print(json_str['success'])
      # print(json_str)
      if json_str['success'] == False:
         # print('--')
         return 'null'
      htmls = json_str['content']
      p = pq(htmls)
      # 电量情况/送受电情况/机组情况/火电运行情况/调度运行记录
      d1 = p('#sectionMain').text().split(' ')
      s1 = self.get_1_json(d1,date)
      d2 = p('#sectionXny').text().split(' ')
      s2 = self.get_2_json(d2)

      d3 = p('#sectionSsd').find('tr')
      s3 = self.get_3_json(d3)

      d4 = p('#sectionFhqk').text().split(' ')
      s4 = self.get_4_json(d4)

      d5 = p('#sectionYdqk').text().split(' ')
      s5 = self.get_5_json(d5)

      d8 = p('#sectionJlqk').text().split(' ')
      s8 = self.get_8_json(d8)

      s9 = '[%s]' % ('%s,%s,%s,%s,%s,%s' % (s1,s2,s3,s4,s5,s8))
      # print(s9)
      return s9
   # 获取所有要获取日期的数据，返回列表。
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
      # print(date_list)
      datas = []
      for date_str in date_list:
         # print(date_str)
         datas.append(date_str)
         datas.append(self.get_one_day_datas(date_str))
         self.save_detial(datas)
         datas = []
         # print(self.get_one_day_datas(date_str))
         # print(date_str)
      # print(len(all_datas))
   # 保存数据
   # def save_datas(self):
   #    pass

if __name__ == '__main__':
   t = TongZi()
   # print(t.get_date_list())
   # t.get_one_day_datas()
   # t.get_2_json()
   t.get_all_day_datas()
   # t.get_2_json()
   # s=t.list_to_jsondic([1,2,3,4,5,6])
   # t.list_to_children([1,2,3,4,5,6])