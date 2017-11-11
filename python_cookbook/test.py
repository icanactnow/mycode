from collections import deque
li = deque()
li.append(1)
li.append(2)

li.appendleft(0)
print(li)#deque([0, 1])
print(li.pop())#1
print(li)#deque([0])
print(li.popleft())#0
