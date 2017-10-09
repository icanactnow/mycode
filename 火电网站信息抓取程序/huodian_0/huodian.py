import requests
import re
from pyquery import PyQuery as pq
from index_data import datas
import psycopg2

class get_huodian_news(object):
    """docstring for GetHtmlget_html"""

    def __init__(self):
        super(get_huodian_news, self).__init__()

    def get_html(self):
        head = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        html = requests.get('http://huodian.bjx.com.cn/', headers=head)
        with open('huodian.html', 'w', encoding=html.encoding) as f:
            f.write(html.text)

    def connect_db(self):
        conn = psycopg2.connect(database="huodian", user="postgres",password="tuji2013", host="127.0.0.1", port="5432")
        print("Opened database successfully")
        return conn
        
    def save_data_to_db(self):
        d = pq(datas)
        conn = self.connect_db()
        cur = conn.cursor()
        for i in range(d('a').length):
            str = d('a').eq(i).attr('href')
            title = d('a').eq(i).attr('title')
            if str and title:
                if re.match(r'http', str):
                    cur.execute("INSERT INTO HUODIAN(ID , TITLE,URL)VALUES(%s, %s,%s)", (i, title, str))
        conn.commit()
        conn.close()
if __name__ == '__main__':
    save_data = get_huodian_news()
    save_data.save_data_to_db()
