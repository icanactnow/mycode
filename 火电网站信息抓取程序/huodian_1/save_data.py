from get_data import GetData
from pyquery import PyQuery as pq
import psycopg2
data = GetData()
data_list = data.save_value_of_index_data()

#
class Save(object):
    """docstring for save"""

    def __init__(self):
        super(Save, self).__init__()

    def connect_db(self):
        conn = psycopg2.connect(database="huodian", user="postgres",
                                password="tuji2013", host="127.0.0.1", port="5432")
        print("Opened database successfully")
        return conn

    def get_title(self, dic):
        # key = list(dic.keys())[0].split('~')[0]
        return list(dic.keys())[0].split('~')[0]

    def get_href(self, dic):
        return list(dic.keys())[0].split('~')[1]

    def get_article(self, dic):
        return list(dic.values())[0]

    def save_data_to_db(self):
        data_list = GetData().save_value_of_index_data()
        conn = self.connect_db()
        cur = conn.cursor()
        i = 0
        for dic in data_list:
            title = self.get_title(dic)
            href = self.get_href(dic)
            article = self.get_article(dic)
            cur.execute(
                "INSERT INTO HUODIAN(ID,TITLE,URL,ARTICLE)VALUES(%s,%s, %s,%s)",
                (i, title, href, article))
            i += 1
        conn.commit()
        conn.close()
if __name__ == '__main__':
    save = Save()
    
    save.save_data_to_db()
