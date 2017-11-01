"""
['qy_corporation', 'qy_id', 'qy_address', 'province_id', 'qy_link_phone', 'qy_wrylx', 'qy_name', 'qy_industry', 'qy_auto_monitor_operation_style']
"""
insert = ['monitor_time','project_id','monitor_value','standard_limit_value','standard_limit_value','monitor_point','enterprise_id','province_id']
update = ['monitor_time','project_id','monitor_value','standard_limit_value','standard_limit_value','monitor_point','enterprise_id','province_id']
"""
(%(defect_id)s, %(defect_describe)s, ' \
                     '%(defect_creator)s, %(defect_creator_duty)s, %(defect_creator_profession)s, ' \
                     '%(defect_grade_describe)s, %(defect_profession)s, %(status_description)s, ' \
                     '%(unit_system)s, %(defect_datetime)s, %(defect_up_datetime)s, ' \
                     '%(responsible_person)s, %(responsible_company)s, %(receiver)s, %(checker)s, ' \
                     '%(check_datetime)s, %(hang_up_cause)s, %(hang_up_info)s, ' \
                     '%(complete_datetime)s, %(fix_department_opinion)s, ' \
                     '%(technique_department_opinion)s, %(eliminate_case)s, %(is_eliminate)s);
                     defect_describe=%(defect_describe)s,' \
                     ' defect_creator=%(defect_creator)s, def

monitor_time=%(monitor_time)s,project_id=%(project_id)s,monitor_value=%(monitor_value)s,standard_limit_value=%(standard_limit_value)s,standard_limit_value=%(standard_limit_value)s,monitor_point=%(monitor_point)s,enterprise_id=%(enterprise_id)s,province_id=%(province_id)s,
"""


def insert_format():
   temp_list = []
   st1 = ''
   st2 = ''
   for item in insert:
      # temp_list.append('%({0})s'.format(item)+',')
      st1 +=  '%({0})s'.format(item)+','
      st2 += item+','
   # print(tuple(temp_list))
   # print(st2)
   print(st1)

def update_format():
   temp_list = []
   st1 = ''
   st2 = ''
   for item in insert:
      # temp_list.append('%({0})s'.format(item)+',')
      st1 +=  '{0}=%({1})s'.format(item,item)+','
      st2 += item+','
   # print(tuple(temp_list))
   # print(st2)
   print(st1)

if __name__ == '__main__':
   insert_format()
   # update_format()
