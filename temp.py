import requests
import json
import sys
import urllib
from bs4 import BeautifulSoup
import os,time, threading


# def test(p):
#     print(p,'start')
#     time.sleep(5)
#     print(p,'end')
# thmax=3
# list =[]
# for i in range(50):
#     list.append(str(i))

# for item in list:
    
#     while threading.activeCount() > thmax:
#         print(threading.activeCount(),'threads')
#         #time.sleep(1)

#     t=threading.Thread(target=test,args=item)   
#     t.start()
#     t.join()

# print('end')
x='5'
#urllib.request.urlretrieve('http://www.manhuadb.com/static/57/510/186_djsfqcne.jpg', 'x3.jpg')
with open(os.path.join(os.path.abspath('.'), 'new folder',x+'.jpg'), 'wb') as f:
    f.write(requests.get('http://wx4.sinaimg.cn/large/68f976d7gy1g50xt7kyb2j20n00v6q81.jpg').content)

