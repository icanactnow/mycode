from pyquery import PyQuery as pq
import requests
import time
from NameId import name_id
import json
class GetLimt(object):
   """docstring for GetLimt"""

   def __init__(self):
      super(GetLimt, self).__init__()
      # self.indexs_url = 'http://113.140.66.227:8064/province_publicity/tbasCorp/getCorpTree?wrtype=YQ&year=2017&code=610000&&timestamp='
      self.indexs_url = 'http://113.140.66.227:8064/province_publicity/EleView/queryCheckList?corpId={0}&wrtype=YQ&timestamp={1}'
      self.str =''
   def datetime_timestamp(self,dt0, type='ms'):
   
      if isinstance(dt0, str):
         ts = time.mktime(time.strptime(dt0, '%Y-%m-%d %H:%M:%S'))
      else:
         ts = time.mktime(dt0)

      delta = time.timezone  # mktime默认时间是本地时间，需用 ts+delta 调整时区
      if type.lower() == 'ms':
         ts0 = int(ts) * 1000 - delta * 1000
      elif type.lower() == 's':
         ts0 = int(ts) - delta
      
      return ts0

   def get_commpany_corpId(self):
      now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      # print(now_time)
      time_chuo = self.datetime_timestamp(now_time)
      url = self.indexs_url+str(time_chuo)
      # print(url)
      prop_data = pq(url=url)
      # print(type(prop_data))
      print(prop_data.html())
      # print(prop_data(''))
   #返回所有信息
   def get_all_datas(self):
      now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
      # print(now_time)
      time_chuo = self.datetime_timestamp(now_time)
      namelist = name_id().result()
      # print(namelist)
      limt_list = []
      for li in namelist:
         com_id = li[1]
         url = 'http://113.140.66.227:8064/province_publicity/EleView/queryCheckList?corpId={0}&wrtype=YQ&timestamp={1}'.format(com_id,time_chuo)
         limt_data = pq(url)
         #将json解析为python对象。
         lj = json.loads(limt_data.html())
         limt_list.append(lj)
         
         #循环遍历获取想要的限值
         
      return limt_list
         # so = limt_list[0][0]
   def get_so2_limt(self):
      all_datas = self.get_all_datas()
      so2_limt_list=[]
      for li in all_datas:
         for dic in li:#遍历每一个字典
            if 'monitoritem' and 'itemlimit' in dic:
               if dic['monitoritem'] == '二氧化硫':
                  so2_limt_list.append(dic['itemlimit'])
                  break
         else:
            so2_limt_list.append('null')
      return so2_limt_list


   def get_nox_limt(self):
      all_datas = self.get_all_datas()
      nox_limt_list=[]
      for li in all_datas:
         for dic in li:#遍历每一个字典
            if 'monitoritem' and 'itemlimit' in dic:
               if dic['monitoritem'] == '氮氧化物':
                  
                  nox_limt_list.append(dic['itemlimit'])
                  break
         else:
            nox_limt_list.append('null')
      return nox_limt_list
   def get_yan_limt(self):
      all_datas = self.get_all_datas()
      yan_limt_list=[]
      for li in all_datas:
         for dic in li:#遍历每一个字典
            if 'monitoritem' and 'itemlimit' in dic:
               if dic['monitoritem'] == '氮氧化物':
                  
                  yan_limt_list.append(dic['itemlimit'])
                  break
         else:
            yan_limt_list.append('null')
      return yan_limt_list
      #standard
   def get_standard_limt(self):
      all_datas = self.get_all_datas()
      standard_limt_list=[]
      for li in all_datas:
         for dic in li:#遍历每一个字典
            if 'monitoritem' and 'itemlimit' in dic:
               standard_limt_list.append(dic['standard'])
               break
         else:
            standard_limt_list.append('null')
      return standard_limt_list
if __name__ == '__main__':
   # t = GetLimt().get_commpany_corpId()
   t=GetLimt()
   # t.get_all_datas()
   for num in t.get_standard_limt():
      print(num)
   # print(t.get_so2_limt())
