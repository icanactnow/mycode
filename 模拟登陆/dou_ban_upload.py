import requests
import re

def test():
   url = 'https://accounts.douban.com/login?alias=&redir=https%3A%2F%2Fwww.douban.com%2F&source=index_nav&error=1001'


   cooks_str='bid=XGThSXTRxPc; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1509887103%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRLQ54N_d0T4ghR5XmmT0e_6GSt-wiQQsy_AUlOwE0Ky%26wd%3D%26eqid%3D9ccde3e40007c7790000000359ff0c76%22%5D; _pk_id.100001.8cb4=975f656887398220.1507027153.7.1509890225.1509883725.; __utma=30149280.1653219163.1507027155.1509883420.1509887103.7; __utmz=30149280.1509887103.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ll="118372"; ps=y; ue="694209060@qq.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16143; _pk_ses.100001.8cb4=*; __utmb=30149280.34.10.1509887103; ap=1; __utmc=30149280; dbcl2="161439123:t37//qqOGOE"; ck=jzkr; __utmt=1'
   Cookie     bid=XGThSXTRxPc; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1509887103%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRLQ54N_d0T4ghR5XmmT0e_6GSt-wiQQsy_AUlOwE0Ky%26wd%3D%26eqid%3D9ccde3e40007c7790000000359ff0c76%22%5D; _pk_id.100001.8cb4=975f656887398220.1507027153.7.1509890254.1509883725.; __utma=30149280.1653219163.1507027155.1509883420.1509887103.7; __utmz=30149280.1509887103.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ll="118372"; ps=y; ue="694209060@qq.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16143; ap=1; __utmc=30149280; dbcl2="161439123:t37//qqOGOE"; ck=jzkr
   s = re.sub('=|;',' ',cooks_str)
   s = re.sub(r'\s+',' ',s)
   cook_list = s.split(' ')
   # print(cook_list[::2])
   print(len(cook_list))
   keys = cook_list[::2]
   dic = {}
   dic = dic.fromkeys(keys)
   for value in cook_list[1::2]:
      print(value)
      for key in dic:
         dic[key] = value
         continue
   print(dic)

test()