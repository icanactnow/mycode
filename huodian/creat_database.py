import psycopg2


class CreatTb(object):

    def __init__(self):
        super(CreatTb, self).__init__()

    def connect_db(self):
        conn = psycopg2.connect(database="huodian", user="postgres",
                                password="tuji2013", host="127.0.0.1", port="5432")
        print("Opened database successfully")
        return conn

    def creat_table(self):
        conn = self.connect_db()
        cur = conn.cursor()

        cur.execute('''CREATE TABLE HUODIAN
          (ID INT PRIMARY KEY      NOT NULL,
          TITLE           TEXT     NOT NULL ,
          URL           CHAR(500)  NOT NULL,
          ARTICLE         TEXT     NOT NULL) ;''')  # 在数据库中创建一张表
        conn.commit()
        conn.close()
if __name__ == '__main__':
    tb = CreatTb()
    tb.creat_table()
