'''
获取排放废气的公司的详细信息
'''
import pyamf
from pyamf.flex import messaging
import uuid
import requests
import datetime
from pyamf import remoting
from pyamf.flex import messaging
from pyquery import PyQuery as pq
from contextlib import closing

from t3c.manager.db import DB
from CommonClass import GetGasCommpanyData , ParseFlash

class GetGasCompanyDetial(object):

   def __init__(self):
      super(GetGasCompanyDetial, self).__init__()
      self.url = 'http://111.75.227.207:9180/eipp/messagebroker/amf'
      self.session = requests.Session()
      self.db = DB()


# 获取单个公司的详细信息，返回dict
   def get_company_detial(self, company_id):
      message = ['getEnterpriseReportDetail', '', 'EnterpriseBasService']
      body = ['2017']
      body.insert(0, company_id)
      resp = ParseFlash()._amf(message, body, self.url)
      if resp.ok:
         resp_msg = remoting.decode(resp.content).bodies[0][1]
         # 获取自己想要的值，保存为字典，并返回。
         content = list(resp_msg.body.body)
         return content[0]

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def save_detial(self, datas):
      insert_sql = 'INSERT INTO "plant_app_tcx"."tb_enterprise" (qy_corporation,qy_id,qy_address,'\
      'province_id,qy_link_phone,qy_wrylx,qy_name,qy_industry,qy_auto_monitor_operation_style)'\
          'VALUES (%(qy_corporation)s,%(qy_id)s,%(qy_address)s,%(province_id)s,%(qy_link_phone)s,'\
          '%(qy_wrylx)s,%(qy_name)s,%(qy_industry)s,%(qy_auto_monitor_operation_style)s);'
      update_sql = 'UPDATE "plant_app_tcx"."tb_enterprise" SET qy_corporation=%(qy_corporation)s,'\
      'qy_address=%(qy_address)s,qy_link_phone=%(qy_link_phone)s,qy_wrylx=%(qy_wrylx)s,qy_name=%(qy_name)s,'\
      'qy_industry=%(qy_industry)s,qy_auto_monitor_operation_style=%(qy_auto_monitor_operation_style)s '\
      'WHERE (  qy_id=%(qy_id)s AND  province_id=%(province_id)s);'

      for data in datas:
         # print(data)
         try:
            con = {}
            con['qy_name'] = data['enterPriseName']
            con['qy_corporation'] = data['legalPerson']
            con['qy_link_phone'] = data['officePhone']
            con['qy_address'] = data['address']
            con['qy_industry'] = data['industryTypeName']
            con['qy_wrylx'] = data['monitorTypeName']
            con['province_id'] = int(36000000)
            con['qy_id'] = str(int(data['enterPriseId']))
            con['qy_auto_monitor_operation_style'] = '自动监测和手工监测'
            self.update_insert(insert_sql, update_sql, con)
         except Exception as e:
            print(e)

   def save_all_company_detial(self):
      company_id_list = GetGasCommpanyData().all_gas_company_name_company_id()
      company_detial_lists = []
      for item in company_id_list:
         company_detial_lists.append(self.get_company_detial(item[1]))
      # 保存到数据库
      self.save_detial(company_detial_lists)
if __name__ == '__main__':
   g = GetGasCompanyDetial().save_all_company_detial()
