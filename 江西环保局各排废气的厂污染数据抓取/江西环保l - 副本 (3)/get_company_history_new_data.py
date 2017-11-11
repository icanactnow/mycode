from common_class import ParseFlash
from pyamf import remoting
from contextlib import closing
from datetime import datetime, timedelta

from t3c.manager.db import DB

class GetCompanyHistoryAndNewData(object):

   def __init__(self):
      super(GetCompanyHistoryAndNewData, self).__init__()
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
      index = 0

      for disOutId  in commpany_datas[1::2] :
         body = [0, str(disOutId), date]
         resp = ParseFlash().amf(message, body, self.url)

         if resp.ok:
            resp_msg = remoting.decode(resp.content).bodies[0][1]
            gas_data_list = list(resp_msg.body.body)

            flg = True
            for single in gas_data_list:
               if single['so2Zsnd'] != '-':
                  flg = False

            if flg:
               index += 1
               continue

            for gas_data_dic in gas_data_list:
               if gas_data_dic['so2Zsnd'] == '-' and gas_data_dic['nxoxZsnd'] == '-' and gas_data_dic['dustZs'] == '-':
                  continue
               for key in gas_data_dic:
                  gas_data_dic[key] = '0.00' if gas_data_dic[key] == '-' else gas_data_dic[key]

               commpany_hour_data = []
               commpany_hour_data.append(disMonitName_list[index])
               commpany_hour_data.append(gas_data_dic['strNewDate'])
               commpany_hour_data.append(gas_data_dic['so2Zsnd'])
               commpany_hour_data.append(gas_data_dic['nxoxZsnd'])
               commpany_hour_data.append(gas_data_dic['dustZs'])
               commpany_hour_data.append(disOutId[:-3])
               commpany_day_data.append(commpany_hour_data)

            index += 1

      return commpany_day_data

   def get_day_datas(self,date_str):
      all_data = []

      with closing(self.db.engine.connect()) as cn:
         res = cn.execute('SELECT qy_id FROM plant_app_tcx.tb_enterprise;')
         commpany_id_list = res.fetchall()

      for commpany_id in commpany_id_list:
         all_data.append(self.get_commpany_day_datas(date_str, commpany_id[0]))

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
         con = {}
         con['monitor_value'] = data[4]
         con['province_id'] = 36000000
         con['enterprise_id'] = data[5]
         con['monitor_point'] = data[1]
         con['project_id'] = data[3]
         con['monitor_time'] = data[2]

         self.update_insert(insert_sql, update_sql, con)

   def save_all_commpany_data(self):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute('SELECT MAX(monitor_time) FROM plant_app_tcx.tb_acquisition;')
         data = res.fetchall()

      db_date = data[0][0]
      last_date = datetime.now() - timedelta(days = 1)
      db_date_str = datetime.strftime(db_date, '%Y-%m-%d')
      last_date_str = datetime.strftime(last_date, '%Y-%m-%d')

      while db_date_str != last_date_str:
         db_date += timedelta(days = 1)
         db_date_str = datetime.strftime(db_date, '%Y-%m-%d')
         self.get_day_datas(db_date_str)

   def save_new_datas(self):
      temp = datetime.now() - timedelta(hours = 1)
      temp_up = datetime.now() - timedelta(hours = 2)
      new_date_hour = temp.strftime('%Y-%m-%d %H:00:00')
      up_date_hour = temp_up.strftime('%Y-%m-%d %H:00:00')

      with closing(self.db.engine.connect()) as cn:
         res = cn.execute('SELECT province_id, monitor_point, monitor_time,'\
            'project_id, monitor_value,enterprise_id'\
            ' FROM plant_app_tcx.tb_acquisition WHERE monitor_time =' + '\'' +new_date_hour+'\''+';')
         data = res.fetchall()

         self.save_now_detial(data)

         res1 = cn.execute('DELETE FROM plant_app_tcx.tb_acquisition_new_data'\
            ' WHERE monitor_time =' + '\'' +up_date_hour+'\''+';')

if __name__ == '__main__':
   t = GetCompanyHistoryAndNewData()
   t.save_all_commpany_data()
   t.save_new_datas()
