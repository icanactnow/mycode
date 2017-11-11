from common_class import ParseFlash
from pyamf import remoting
from contextlib import closing
from datetime import datetime, timedelta

from t3c.manager.db import DB
from common_class import GetGasCommpanyData

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

      monitor_type_list = ['二氧化硫折算值', '氮氧化物折算值', '烟尘折算值']

      for data in datas:
         monitor_value_index = 2
         for monitor_type in monitor_type_list:
            con = {}
            con['monitor_point'] = data[0]
            con['project_id'] = monitor_type
            con['monitor_value'] = data[monitor_value_index]
            con['enterprise_id'] = data[5]
            con['province_id'] = 36000000
            con['monitor_time'] = datetime.strptime(data[1][:-1], '%Y-%m-%d %H')
            monitor_value_index += 1
            self.update_insert(insert_sql, update_sql, con)

   def save_now_detial(self, datas):
      insert_sql = 'INSERT INTO "plant_app_tcx"."tb_acquisition_new_data" (monitor_time,'\
      'project_id,monitor_value,monitor_point,enterprise_id,province_id)'\
      'VALUES (%(monitor_time)s,%(project_id)s,%(monitor_value)s,%(monitor_point)s,'\
      '%(enterprise_id)s,%(province_id)s);'

      update_sql = 'UPDATE "plant_app_tcx"."tb_acquisition_new_data" SET monitor_value='\
      '%(monitor_value)s, monitor_time=%(monitor_time)s '\
      'WHERE (province_id=%(province_id)s AND enterprise_id=%(enterprise_id)s '\
      'AND  monitor_point=%(monitor_point)s  AND  project_id=%(project_id)s ) ;'

      monitor_type_list = ['二氧化硫折算值', '氮氧化物折算值', '烟尘折算值']
      for data in datas:

         con = {}
         con['monitor_point'] = data[1]
         con['monitor_time'] = data[2].strftime('%Y-%m-%d %H:00:00')
         # datetime.strptime(data[2], '%Y-%m-%d %H:00:00')
         con['project_id'] = data[3]
         con['monitor_value'] = data[4]
         con['enterprise_id'] = data[5]
         con['province_id'] = 36000000


         self.update_insert(insert_sql, update_sql, con)

   def get_commpany_day_datas(self,date,commpany_datas):
      commpany_day_data =[]
      message = ['findAllHoursGasLastDay', '', 'PollGasWatDataService']
      disMonitName_list = commpany_datas[2::2]
      print(date)
      print(commpany_datas)
      # print(commpany_datas+ '------'+ commpany_datas[2::2])
      disMonitName_index = 0

      for disOutId  in commpany_datas[3::2] :

         body = [0, str(disOutId), date]
         resp = ParseFlash().amf(message, body, self.url)

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
               commpany_day_data.append(commpany_hour_data)

            disMonitName_index += 1
      self.save_detial(commpany_day_data)

   def get_commpany_last_date(self,commpany_id):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute('SELECT MAX(monitor_time) FROM '\
         ' plant_app_tcx.tb_acquisition_new_data '\
         ' WHERE enterprise_id ='+ '\''+ commpany_id +'\''+ ' AND province_id = 36000000;')
         date = res.fetchall()[0][0]
         if not date:
            date = datetime.strptime('2017-01-01 00:00:00','%Y-%m-%d 00:00:00')
            # print(date)
      return date

   def get_commpany_new_datas(self,commpany_id):
      with closing(self.db.engine.connect()) as cn:
         res1 = cn.execute('SELECT MAX(monitor_time) FROM '\
         ' plant_app_tcx.tb_acquisition '\
         ' WHERE enterprise_id ='+ '\''+ commpany_id +'\''+ ' AND province_id = 36000000;')

         data1 = res1.fetchall()

         res2 = cn.execute('SELECT province_id, monitor_point, monitor_time,'\
            'project_id, monitor_value,enterprise_id'\
            ' FROM plant_app_tcx.tb_acquisition WHERE monitor_time =' + '\'' +data1[0][0].strftime('%Y-%m-%d %H:00:00')+ '\'' + ' AND enterprise_id =' + '\'' + commpany_id + '\''+ ' ;')

         data2 = res2.fetchall()


         res3 = cn.execute('DELETE FROM plant_app_tcx.tb_acquisition_new_data'\
            ' WHERE enterprise_id =' + '\'' +commpany_id+'\''+';')

         self.save_now_detial(data2)
      # print(data2)

   def get_commpany_datas(self, commpany_datas):
      last_date = self.get_commpany_last_date(commpany_datas[1])
      now_date = datetime.now() + timedelta(days = 1)
      last_date_str = datetime.strftime(last_date, '%Y-%m-%d')
      now_date_str = datetime.strftime(now_date, '%Y-%m-%d')
      print('last_date = ' + last_date_str)
      while last_date_str != now_date_str:
         # 获取公司每一天的数值并保存
         self.get_commpany_day_datas(last_date_str,commpany_datas)
         self.get_commpany_new_datas(commpany_datas[1])
         last_date += timedelta(days = 1)
         last_date_str = datetime.strftime(last_date, '%Y-%m-%d')

   # 获取并保存所有公司信息
   def get_all_commpany_datas(self):
      # with closing(self.db.engine.connect()) as cn:
      #    res = cn.execute('SELECT qy_id FROM plant_app_tcx.tb_enterprise;')
      #    commpany_id_list = res.fetchall()

      all_commpany_info_datas = GetGasCommpanyData().get_all_commpany_id_disOutId()
      # print(all_commpany_info_datas)
      for commpany_datas in all_commpany_info_datas:
         #通过id获取保存该公司所需要的数据
         self.get_commpany_datas(commpany_datas)



if __name__ == '__main__':
   t = GetCompanyHistoryAndNewData()
   # t.save_all_commpany_data()
   # t.save_new_datas()
   # t.get_commpany_last_date('601010008')
   t.get_all_commpany_datas()
   # t.get_commpany_new_datas('601010008')
