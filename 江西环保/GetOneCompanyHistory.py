from CommonClass import ParseFlash
from pyamf import remoting
from contextlib import closing
from datetime import datetime ,timedelta
import heapq

from t3c.manager.db import DB
from CommonClass import all_data_list
#获取一家工厂的历史数据
#['江西晨鸣纸业有限责任公司(废水,废气,危险废物)', '601010008', '废水总排放口', '601010008001', '1#脱硫塔烟气排口', '601010008002', '2#脱硫塔烟气排口', '601010008004']
class GetOneCompanyDataHistory(object):
   """docstring for GetOneCompanyDataHistory"""
   def __init__(self):
      super(GetOneCompanyDataHistory, self).__init__()
      self.all_data_list = all_data_list
      # self.company_id = '601010008001'
      self.url = 'http://111.75.227.207:9180/eipp/messagebroker/amf'
      self.db = DB()
   def get_one_commpany_one_day_history(self,date,commpany_datas):

      commpany_day_data =[]
      message = ['findAllHoursGasLastDay', '', 'PollGasWatDataService']
      disMonitName_list = commpany_datas[::2]
      disMonitName_index = 0
      # print(self.data_list)
      for disOutId  in commpany_datas[1::2] :
         # print(disOutId)
         body = [0, str(disOutId), date]
         resp = ParseFlash()._amf(message, body, self.url)
         if resp.ok:
            resp_msg = remoting.decode(resp.content).bodies[0][1]
         # list(resp_msg.body.body)
            # print(list(resp_msg.body.body))
            gas_data_list = list(resp_msg.body.body)
            # print(len(gas_data_list))
            #判断当天数据是否全部为-
            flg = True
            for single in gas_data_list:
               if single['so2Zsnd'] != '-':
                  flg = False
            if flg:
               disMonitName_index += 1
               continue
            for gas_data_dic in gas_data_list:
               # if :
               #    break
               # print(gas_data_dic)
               if gas_data_dic['so2Zsnd'] == '-' and gas_data_dic['nxoxZsnd'] == '-' and gas_data_dic['dustZs'] == '-':
                  # disMonitName_index += 1
                  continue
               # print(gas_data_dic)
               #获取该厂该条件下的所有想要参数disMonitName strNewDate 3 commpany_id
               for key in gas_data_dic:
                  gas_data_dic[key] = '0.00' if gas_data_dic[key] == '-' else gas_data_dic[key]
               commpany_hour_data = []
               commpany_hour_data.append(disMonitName_list[disMonitName_index])
               commpany_hour_data.append(gas_data_dic['strNewDate'])
               commpany_hour_data.append(gas_data_dic['so2Zsnd'])
               commpany_hour_data.append(gas_data_dic['nxoxZsnd'])
               commpany_hour_data.append(gas_data_dic['dustZs'])
               commpany_hour_data.append(disOutId[:-3])
               commpany_day_data.append(commpany_hour_data)
            disMonitName_index += 1
      # print(commpany_day_data)
      # print('get_one_commpany_one_day_history')
      return commpany_day_data

      #查询表中最新日期，返回当前日期与数据库日期之间的日期集合，即为要新爬取的任务
   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)
   def get_date_list(self):
      # print('get_date_list')
      #从数据库读取存储到的最新日期
      db = DB()
      with closing(db.engine.connect()) as cn:
         res = cn.execute('SELECT  monitor_time FROM '\
            'plant_app_tcx.tb_acquisition WHERE province_id = 36000000;')
         data = res.fetchall()
         # print(data)
      #如果数据库中没有存放记录就将从2017年开始。
      if data:
         # print(dir(data))
         last_date = heapq.nlargest(1,data)[0][0] - timedelta(days = 1)
      else:
         last_date = datetime.strptime('2016-12-31 18:19:59', '%Y-%m-%d %H:%M:%S')
         # print('b')
      #计算并返回要抓取的时间段，以字符串，列表形式返回。
      last_date_str = str(last_date)[:10]
      now_date_str = str(datetime.now())[:10]
      temp_date = last_date
      # print(temp_date)
      date_list = []
      # print(last_date)
      temp_date_str = str(last_date)[:10]
      # print('需要抓取72家工厂从 %s 至 %s 共 %d 天的数据' %(last_date_str,now_date_str,len(date_list)))
      while True:
         if temp_date_str == now_date_str:
            # print(date_list)
            # date_list.append(temp_date_str)
            # return(date_list)
            break
         temp_date += timedelta(days = 1)
         # print(temp_date)
         temp_date_str = str(temp_date)[:10]
         date_list.append(temp_date_str)
      return(date_list)
         # print(temp_date_str)
# 获取一个公司数据库中没有的所有数据
   def get_one_day_all_commpany_data(self,date):
      all_data = []
      for data in self.all_data_list:
         # print(date)
         all_data.append(self.get_one_commpany_one_day_history(date,data))
         self.save_data(all_data)
         try:
            print('获取了   %s厂    %10s       %s的数据'%(all_data[-1][-1][-1],all_data[-1][-1][0],all_data[-1][-1][1][:10]))
         except:
            # print('该厂无数据')
            pass
      # print(all_data)
      return all_data
   def save_detial(self, datas):
      insert_sql = 'INSERT INTO "plant_app_tcx"."tb_acquisition" (monitor_time,'\
      'project_id,monitor_value,monitor_point,enterprise_id,province_id)'\
      'VALUES (%(monitor_time)s,%(project_id)s,%(monitor_value)s,%(monitor_point)s,'\
      '%(enterprise_id)s,%(province_id)s);'


      update_sql = 'UPDATE "plant_app_tcx"."tb_acquisition" SET monitor_value='\
      '%(monitor_value)s'\
      'WHERE (province_id=%(province_id)s AND enterprise_id=%(enterprise_id)s '\
      'AND  monitor_point=%(monitor_point)s  AND  project_id=%(project_id)s AND'\
      '  monitor_time=%(monitor_time)s);'

      for data in datas:
         # print(data)
         try:
            con = {}
            con['monitor_value'] = data[3]
            con['province_id'] = 36000000
            con['enterprise_id'] = data[4]
            con['monitor_point'] = data[0]
            con['project_id'] = data[2]
            con['monitor_time'] = datetime.strptime(data[1][:-1], '%Y-%m-%d %H')
            self.update_insert(insert_sql, update_sql, con)
         except Exception as e:
            print(e+'---')
   def save_now_detial(self, datas):
      insert_sql = 'INSERT INTO "plant_app_tcx"."tb_acquisition_new_data" (monitor_time,'\
      'project_id,monitor_value,monitor_point,enterprise_id,province_id)'\
      'VALUES (%(monitor_time)s,%(project_id)s,%(monitor_value)s,%(monitor_point)s,'\
      '%(enterprise_id)s,%(province_id)s);'


      update_sql = 'UPDATE "plant_app_tcx"."tb_acquisition_new_data" SET monitor_value='\
      '%(monitor_value)s'\
      'WHERE (province_id=%(province_id)s AND enterprise_id=%(enterprise_id)s '\
      'AND  monitor_point=%(monitor_point)s  AND  project_id=%(project_id)s AND'\
      '  monitor_time=%(monitor_time)s);'

      for data in datas:
         # print(data)
         try:
            con = {}
            con['monitor_value'] = data[4]
            con['province_id'] = 36000000
            con['enterprise_id'] = data[5]
            con['monitor_point'] = data[1]
            con['project_id'] = data[3]
            con['monitor_time'] = data[2]
            self.update_insert(insert_sql, update_sql, con)
         except Exception as e:
            print(e+'---')
   def save_data(self,all_data):
      # print('sav_one_commpany_data')
      # all_data = self.get_one_day_all_commpany_data(date)
      # data = [['1#脱硫塔烟气排口', '2016-06-20 16时', '5.47', '601010008']]
      # all_data=[['1#脱硫塔烟气排口', '2016-06-20 16时', '5.47', '0.04', '14.33', '601010008']]
      for datas in all_data:
         for data in datas:
            temp_list = []
            data1 = data.copy()
            data1.pop(3)
            data1.pop(3)
            data1.insert(2,'二氧化硫折算值')
            data2 = data.copy()
            data2.pop(2)
            data2.pop(3)
            data2.insert(2,'氮氧化物折算值')
            data3 = data.copy()
            data3.pop(2)
            data3.pop(2)
            data3.insert(2,'烟尘折算值')
            temp_list.append(data1)
            temp_list.append(data2)
            temp_list.append(data3)
            # print(temp_list)
            self.save_detial(temp_list)
   def save_all_commpany_data(self):
      date_list = self.get_date_list()
      print(date_list)
      for date in date_list:
         self.get_one_day_all_commpany_data(date)
      # for commpany_datas in all_data_list:
      #    print(commpany_datas)
      #    self.sav_one_commpany_data(commpany_datas)
   def save_tb_acquisition_new_data(self):
      temp = datetime.now() - timedelta(hours = 1)
      temp_up = datetime.now() - timedelta(hours = 2)
      temp_new_date_hour = str(temp)[:14]+'00:00'
      temp_up_date_hour = str(temp)[:14]+'00:00'
      new_date_hour = str(datetime.strptime(temp_new_date_hour, '%Y-%m-%d %H:%M:%S'))
      up_date_hour = str(datetime.strptime(temp_up_date_hour, '%Y-%m-%d %H:%M:%S'))
      # new_date_hour = '2017-01-13 09:00:00'
      # up_date_hour = '2017-01-13 09:00:00'
      print(new_date_hour)
      db = DB()
      with closing(db.engine.connect()) as cn:
         res = cn.execute('SELECT province_id, monitor_point, monitor_time,'\
            'project_id, monitor_value,enterprise_id'\
            ' FROM plant_app_tcx.tb_acquisition WHERE monitor_time =' + '\'' +new_date_hour+'\''+';')
         data = res.fetchall()
         self.save_now_detial(data)
         # print(data)
         res1 = cn.execute('DELETE FROM plant_app_tcx.tb_acquisition_new_data'\
            ' WHERE monitor_time =' + '\'' +up_date_hour+'\''+';')

if __name__ == '__main__':
   t  = GetOneCompanyDataHistory()
   # t.sav_one_commpany_data()
   # t.save_detial(data)
   t.save_all_commpany_data()
   t.save_tb_acquisition_new_data()