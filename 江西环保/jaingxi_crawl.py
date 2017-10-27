# -*- coding: utf-8 -*-

import pyamf
import uuid
import requests
import datetime
from pyamf import remoting
from pyamf.flex import messaging
from pyquery import PyQuery as pq
from contextlib import closing

from t3c.manager.db import DB


class XiangYangCrawl():

   def __init__(self):
      self.db = DB()
      self.now = datetime.datetime.now()
      self.session = requests.Session()
      # self.url = 'http://111.75.227.207:9180/eipp/flexoutput/index.html'
      self.url = 'http://111.75.227.207:9180/eipp/messagebroker/amf'

   def _amf(self, message, body, url):
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
      resp = self.session.post(url, data=bin_msg.getvalue(), headers={'Content-Type':
                                                                        'application/x-amf'})

      return resp

   def update_insert(self, insert, update, contents):
      with closing(self.db.engine.connect()) as cn:
         res = cn.execute(update, contents)

         if not res.rowcount:
            cn.execute(insert, contents)

   def login(self):
      message = ['getEnterpriseReportDetail', '', 'EnterpriseBasService']
      body = ['601220001', '2017']
      resp = self._amf(message, body, self.url)

      return resp.ok

   def qxd_list(self, start_time, end_time):
      insert_sql = 'INSERT INTO "plant_app_core"."tb_defect" (defect_id, defect_describe, ' \
                     'defect_creator, defect_creator_duty, defect_creator_profession, ' \
                     'defect_grade_describe, defect_profession, status_description, unit_system, ' \
                     'defect_datetime, defect_up_datetime, responsible_person, responsible_company,' \
                     ' receiver, checker, check_datetime, hang_up_cause, hang_up_info, ' \
                     'complete_datetime, fix_department_opinion, technique_department_opinion, ' \
                     'eliminate_case, is_eliminate) VALUES (%(defect_id)s, %(defect_describe)s, ' \
                     '%(defect_creator)s, %(defect_creator_duty)s, %(defect_creator_profession)s, ' \
                     '%(defect_grade_describe)s, %(defect_profession)s, %(status_description)s, ' \
                     '%(unit_system)s, %(defect_datetime)s, %(defect_up_datetime)s, ' \
                     '%(responsible_person)s, %(responsible_company)s, %(receiver)s, %(checker)s, ' \
                     '%(check_datetime)s, %(hang_up_cause)s, %(hang_up_info)s, ' \
                     '%(complete_datetime)s, %(fix_department_opinion)s, ' \
                     '%(technique_department_opinion)s, %(eliminate_case)s, %(is_eliminate)s);'
      update_sql = 'UPDATE "plant_app_core"."tb_defect" SET defect_describe=%(defect_describe)s,' \
                     ' defect_creator=%(defect_creator)s, defect_creator_duty=%(defect_creator_duty)s,' \
                     ' defect_creator_profession=%(defect_creator_profession)s, ' \
                     'defect_grade_describe=%(defect_grade_describe)s, ' \
                     'defect_profession=%(defect_profession)s, status_description=%(status_description)s,' \
                     ' unit_system=%(unit_system)s, defect_datetime=%(defect_datetime)s, ' \
                     'defect_up_datetime=%(defect_up_datetime)s, responsible_person=%(responsible_person)s,' \
                     ' responsible_company=%(responsible_company)s, receiver=%(receiver)s, ' \
                     'checker=%(checker)s, check_datetime=%(check_datetime)s, ' \
                     'hang_up_cause=%(hang_up_cause)s, hang_up_info=%(hang_up_info)s, ' \
                     'complete_datetime=%(complete_datetime)s, ' \
                     'fix_department_opinion=%(fix_department_opinion)s, ' \
                     'technique_department_opinion=%(technique_department_opinion)s, ' \
                     'eliminate_case=%(eliminate_case)s, is_eliminate=%(is_eliminate)s WHERE ' \
                     '(defect_id=%(defect_id)s);'
      message = ['GetQxpList', 'PJGL', 'fluorine']
      body = ['1', start_time, end_time, '-1', '1,2,3,4', '-1', '0', '-1',
                '-1', '-1', '-1', '-1', '', '0']
      resp = self._amf(message, body, self.url)

      if resp.ok:
         content = self.parse_to_list(resp)

         for data in content:
            try:
               con = {}
               con['defect_id'] = int(data['QXPBH'][2:])
               con['defect_describe'] = data['QXMS']
               con['defect_creator'] = data['FXR']
               con['defect_creator_duty'] = None
               con['defect_creator_profession'] = data['ZYMC']
               con['defect_grade_describe'] = data['JBMC']
               con['defect_profession'] = data['JZMC']
               con['status_description'] = data['QXZT']
               con['unit_system'] = data['SBMC']
               con['defect_datetime'] = data['DJRQ']
               con['defect_up_datetime'] = data['SLSJ']
               con['responsible_person'] = data['SLR']
               con['responsible_company'] = None
               con['receiver'] = None
               con['checker'] = data['YSRQZ']
               con['check_datetime'] = data['YSSJ']
               con['hang_up_cause'] = data['WCLYY']
               con['hang_up_info'] = None
               con['fix_department_opinion'] = data['JXCLYJ']
               con['technique_department_opinion'] = data['SJCLYJ']
               con['eliminate_case'] = data['XQQK']
               con['complete_datetime'] = data['XQSJ']
               con['is_eliminate'] = data['ISJX']
               self.update_insert(insert_sql, update_sql, con)
            except Exception as e:
               print(e)

   # def parse_to_list(self, resp):
   def parse_to_list(self):
      message = ['getEnterpriseReportDetail', '', 'EnterpriseBasService']
      body = ['601220001', '2017']
      resp = self._amf(message, body, self.url)
      if resp.ok:
         resp_msg = remoting.decode(resp.content).bodies[0][1]
         print(resp_msg)
         print('body.body--------------------')
         print(list(resp_msg.body.body))
         print('--------------------')
         print(dir(resp_msg))
         # content = list(resp_ msg.body.body)
         # print(connect)
      # return content

   def start(self, start_time=None, end_time=None):
      if self.login():

         if start_time is None:
            start_time = self.now.date().strftime('%Y-%m-%d')

            if end_time is None:
               end_time = self.now.strftime('%Y-%m-%d %X')
            self.qxd_list(start_time, end_time)


if __name__ == '__main__':
   # start_time = '2015-01-01 00:00:00'
   # end_time = '2017-09-26 17:25:17'
   # xy = XiangYangCrawl()
   # xy.start(start_time)
   xy = XiangYangCrawl()
   xy.parse_to_list()