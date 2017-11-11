# -*- coding:utf-8 -*-
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

class ParseFlash(object):
   """docstring for ParseFlash"""
   def __init__(self):
      super(ParseFlash, self).__init__()
      self.session = requests.Session()

   def amf(self, message, body, url):
      msg = messaging.RemotingMessage(operation=message[0],
                                      source=message[1],
                                      clientId=str(uuid.uuid4()).lower(),
                                      timestamp=0,
                                      timeToLive=0,
                                      destination=message[2],
                                      messageId=str(uuid.uuid4()).upper()
                                      )
      msg.body = body
      msg.headers['DSEndpoint'] = 'null'
      msg.headers['DSId'] = str(uuid.uuid1()).upper()
      req = remoting.Request(target='', body=[msg])
      ev = remoting.Envelope(pyamf.AMF3)
      ev['/0'] = req
      bin_msg = remoting.encode(ev)
      resp = self.session.post(url, data=bin_msg.getvalue(),
                               headers={'Content-Type': 'application/x-amf'})

      return resp


class GetGasCommpanyData(object):
   """
    获取所有排放废气的公司的名称以及prisedId
   """
   def __init__(self):
      super(GetGasCommpanyData, self).__init__()
      self.url = 'http://111.75.227.207:9180/eipp/messagebroker/amf'

   def all_gas_company_name_company_id(self):
      message = ['getEnterprisesByType', '', 'EnterpriseBasService']
      body = ['2', '1', '2017']
      resp = ParseFlash().amf(message, body, self.url)

      if resp.ok:
         resp_msg = remoting.decode(resp.content).bodies[0][1]
         gas_company_data_list = list(resp_msg.body.body)
         all_gas_company_name_companyId = []

         for dic in gas_company_data_list:
            gas_company_name_companyId = []
            gas_company_name_companyId.append(dic['name'])
            gas_company_name_companyId.append(str(int(dic['enterpriseId'])))
            all_gas_company_name_companyId.append(gas_company_name_companyId)

         return all_gas_company_name_companyId

   def get_all_commpany_id_disOutId(self):
      commpany_name_id_list = self.all_gas_company_name_company_id()
      message = ['findAutoMonitorByEnterpriseId',
                 '', 'DischargeMonitorService']
      commpany_name_id_disOutId_list = commpany_name_id_list
      get_all_commpany_id_disOutId = []

      for commpany_name_id in commpany_name_id_list:
         body = [commpany_name_id[1]]
         resp = ParseFlash().amf(message, body, self.url)

         if resp.ok:
            resp_msg = remoting.decode(resp.content).bodies[0][1]
            gas_company_data_list = list(resp_msg.body.body)

            for dic in gas_company_data_list:
               gas_company_name_companyId = []
               commpany_name_id.append((dic['disMonitName']))
               commpany_name_id.append(str(int(dic['disOutId'])))

            get_all_commpany_id_disOutId.append(commpany_name_id)

      return get_all_commpany_id_disOutId

if __name__ == '__main__':
   pass