# i = 0
# while True:
#    i += 1
#    if i==4:
#       print('goodby'+str(i))
#       break
# for i in range(100):
#    print('s')
#    for y in range(100):
#       print('============')
#       break
# li = [1]
# print(li[-1])
# from datetime import datetime
# # cday = datetime.strptime('2015-6-1 18', '%Y-%m-%d %H:%M:%S')
# cday = datetime.strptime('2015-6-1 18', '%Y-%m-%d %H')
# # print(cday)
# li = [1,2,3,4]
# # l = []
# # print(dir(li))
# # print(li.pop(2))
# # print(li)
# # print(li.insert(1,0))
# # print(dir(li))
# l = li.copy()
# # l = li
# l.append(222,333)
# print(l)
# print(li)
# from datetime import datetime
# data =['1#脱硫塔烟气排口', '2016-06-20 16时', '5.47', '601010008']
# print(type(datetime.strptime(data[1][:-1], '%Y-%m-%d %H')))
# print(datetime.strptime(data[1][:-1], '%Y-%m-%d %H'))
dic = {'a':1 , 'b':'-'}
# print(dir(dic))
# print(dic.values())
# print(dir(dic.values()))
for key in dic:
   dic[key] = 'NULL' if dic[key] == '-' else dic[key]
print(dic)