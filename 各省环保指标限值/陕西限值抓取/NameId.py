from dataList import list_str
#返回list
import re
class name_id(object):
    """docstring for name_id"""
    def __init__(self):
        super(name_id).__init__()
        # self.result()
        
    def result(self):
        name_id_list =[]
        for dic in list_str:
            if 'corpId' in dic:
                if int(dic['corpId']) >510800000057:
                    temp_list = []
                    temp_list.append(dic['name'])
                    temp_list.append(dic['corpId'])
                    name_id_list.append(temp_list)
        return name_id_list
if __name__ == '__main__':
    r = name_id()
    for li in r.result():
        print(li[0])
