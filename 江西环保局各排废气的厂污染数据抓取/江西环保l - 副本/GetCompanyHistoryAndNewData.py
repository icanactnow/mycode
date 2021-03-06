from CommonClass import ParseFlash
from pyamf import remoting
from contextlib import closing
from datetime import datetime ,timedelta
import heapq

from t3c.manager.db import DB
from CommonClass import all_data_list

class GetCompanyHistoryAndNewData(object):

   def __init__(self):
      super(GetCompanyHistoryAndNewData, self).__init__()
      self.all_data_list = all_data_list
      self.url = 'http://111.75.227.207:9180/eipp/messagebroker/amf'
      self.db = DB()



   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

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
         print(data)
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
            print(e)

   def save_data(self,all_data):
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
            self.save_detial(temp_list)

   def get_commpany_day_datas(self,date,commpany_datas):
      commpany_day_data =[]
      message = ['findAllHoursGasLastDay', '', 'PollGasWatDataService']
      disMonitName_list = commpany_datas[::2]
      print(commpany_datas+ '------'+ commpany_datas[1::2])
      disMonitName_index = 0

      for disOutId  in commpany_datas[1::2] :

         body = [0, str(disOutId), date]
         resp = ParseFlash()._amf(message, body, self.url)

         if resp.ok:
            resp_msg = remoting.decode(resp.content).bodies[0][1]
            gas_data_list = list(resp_msg.body.body)
            # print(gas_data_list)
            #判断当据是否全部为-
            flg = True
            for single in gas_data_list:
               if single['so2Zsnd'] != '-':
                  flg = False

            if flg:
               disMonitName_index += 1
               print('------')
               continue

            for gas_data_dic in gas_data_list:
               if gas_data_dic['so2Zsnd'] == '-' and gas_data_dic['nxoxZsnd'] == '-' and gas_data_dic['dustZs'] == '-':
                  continue
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
               print(disOutId[:-3])
               commpany_day_data.append(commpany_hour_data)

            disMonitName_index += 1

      return commpany_day_data

   def get_day_datas(self,date_str):
      all_data = []
      for item in all_data_list:
         commpany_datas = item[1]
         all_data.append(self.get_commpany_day_datas(date_str, commpany_datas))
      self.save_data(all_data)



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
            print(e)



   def save_all_commpany_data(self):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute('SELECT MAX(monitor_time) FROM plant_app_tcx.tb_acquisition;')
         data = res.fetchall()
      if not data[0][0]:
         db_date = datetime.strptime('2017-01-01 00:00:00','%Y-%m-%d 00:00:00')
      else:
         db_date = data[0][0]
      last_date = datetime.now() - timedelta(days = 1)
      db_date_str = datetime.strftime(db_date, '%Y-%m-%d')
      last_date_str = datetime.strftime(last_date, '%Y-%m-%d')

      while db_date_str != last_date_str:
         db_date += timedelta(days = 1)
         db_date_str = datetime.strftime(db_date, '%Y-%m-%d')
         self.get_day_datas(db_date_str)

   def save_tb_acquisition_new_data(self):
      temp = datetime.now() - timedelta(hours = 1)
      temp_up = datetime.now() - timedelta(hours = 2)
      temp_new_date_hour = str(temp)[:14]+'00:00'
      temp_up_date_hour = str(temp)[:14]+'00:00'
      new_date_hour = str(datetime.strptime(temp_new_date_hour, '%Y-%m-%d %H:%M:%S'))
      up_date_hour = str(datetime.strptime(temp_up_date_hour, '%Y-%m-%d %H:%M:%S'))

      db = DB()
      with closing(db.engine.connect()) as cn:
         res = cn.execute('SELECT province_id, monitor_point, monitor_time,'\
            'project_id, monitor_value,enterprise_id'\
            ' FROM plant_app_tcx.tb_acquisition WHERE monitor_time =' + '\'' +new_date_hour+'\''+';')
         data = res.fetchall()
         self.save_now_detial(data)
         print('保存了'+ new_date_hour + '最新数据')
         res1 = cn.execute('DELETE FROM plant_app_tcx.tb_acquisition_new_data'\
            ' WHERE monitor_time =' + '\'' +up_date_hour+'\''+';')

if __name__ == '__main__':
   t  = GetCompanyHistoryAndNewData()
   t.save_all_commpany_data()
