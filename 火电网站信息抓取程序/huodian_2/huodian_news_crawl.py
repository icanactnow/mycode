# -*- coding: utf-8 -*-
import requests
import datetime
from contextlib import closing
from t3c.manager.db import DB
from get_data import GetData

class HuoDianNewsCrawl():
    def __init__(self):
        self.db = DB()
        self.now = datetime.datetime.now()
        self.session = requests.Session()
        self.url = 'http://huodian.bjx.com.cn/'

    def update_insert(self, insert, update, contents):
        with closing(self.db.engine.connect()) as cn:
            # res = cn.execute(update, contents)

            # if not res.rowcount:
            cn.execute(insert, contents)

    def qxd_list(self):
        insert_sql = 'INSERT INTO "plant_app_etl"."huodian_news" (id,title,href,content)'\
                     'VALUES (%(id)s, %(title)s,%(href)s, %(content)s);'

        update_sql = 'UPDATE "plant_app_etl"."huodian_news" SET title=%(title)s,' \
                     ' href=%(href)s, content=%(content)s,' \
                     ' id=%(id)s;'

        data_list = GetData().save_value_of_index_data()
        i = 0
        for data_dic in data_list:
            con = {}
            con['id'] = i
            con['title'] = list(data_dic.keys())[0].split('~')[0]
            con['href'] = list(data_dic.keys())[0].split('~')[1]
            con['content'] = list(data_dic.values())[0]
            self.update_insert(insert_sql, update_sql, con)
            i += 1
                

if __name__ == '__main__':
    hd = HuoDianNewsCrawl()
    hd.qxd_list()
