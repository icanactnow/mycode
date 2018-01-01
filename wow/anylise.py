# 数据分析
import pandas as pd
from pandas import DataFrame
from contextlib import closing
from t3c.manager.db import DB

import matplotlib.pyplot as plt
import seaborn as sns
# from pandas import

class anylist(object):
   """docstring for anylist"""
   def __init__(self):
      super(anylist, self).__init__()
      self.db  = DB()

   def get_origin_datas(self):
      sql = 'SELECT * FROM  sun_tick_datas.threed_datas ORDER BY date '
      with closing(self.db.engine.connect()) as cn:
         tmp_datas = cn.execute(sql)
         datas = tmp_datas.fetchall()
      return list(datas)

   def date_no_sum(self):
      datas = self.get_origin_datas()
      for item in datas:
         a, b, c = item[2]
         sum = int(a) + int(b) + int(c)
         sum_li = list(item)
         sum_li[2] = sum
         datas[datas.index(item)] = sum_li

      df = pd.DataFrame(datas, columns = ['date', 'no' , 'sum'])
      return df

   def sum_qu_xian(self):
      df = self.date_no_sum()
      sns.set_style("whitegrid")
      plt.plot(df['sum'][-100:])

      plt.show()
      # print(df)
   def sum_mi_du(self):
      df = self.date_no_sum()
      fig, axes = plt.subplots(1,2)
      sns.distplot(df['sum'], ax = axes[0], kde = True, rug = True)        # kde 密度曲线  rug 边际毛毯
      sns.kdeplot(df['sum'], ax = axes[1], shade=True)                     # shade  阴影
      plt.show()

if __name__ == '__main__':
   t = anylist()
   # t.get_origin_datas()
   # t.date_no_sum()
   # t.sum_qu_xian()
   t.sum_mi_du()