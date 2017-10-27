import re
from pyquery import PyQuery as pq
import requests
index_list = ['http://119.60.9.17:9001/xxgk/qyhjxxgk.html',
'http://218.95.153.246:9002/xxgk/qyhjxxgk.html',
'http://222.75.161.242:9003/xxgk/qyhjxxgk.html',
'http://222.75.161.242:9004/xxgk/qyhjxxgk.html',
'http://222.75.161.242:9005/xxgk/qyhjxxgk.html']
# for item in index_list:
#    print(item)
class ning_xia_limt(object):
   """docstring for ning_xia_limt"""
   def __init__(self):
      super(ning_xia_limt, self).__init__()
      self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
   def get_all_companny_link(self):
      for link in index_list:
         link_html =  requests.get(link)#,headers = self.headers
         print(link_html.text)
         # parse_link = pq(url = link)
         # print(parse_link.html())
if __name__ == '__main__':
   test = ning_xia_limt()
   test.get_all_companny_link()