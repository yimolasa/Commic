import json
# import sys
# import urllib
# from bs4 import BeautifulSoup
import os #,time, threading


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
# x='5'
#urllib.request.urlretrieve('http://www.manhuadb.com/static/57/510/186_djsfqcne.jpg', 'x3.jpg')


# volsname = os.path.join(os.path.abspath('..'),'local test','bac'+'homepage.html')
# print(volsname)
# with open(os.path.join(os.path.abspath('..'),'local test','homepage.html'), 'rb') as f:
#             html = f.read()
#             print(html)

def lastbreak(downloadlog):
    if os.stat(downloadlog).st_size == 0:
        return(0)
    else:    
        with open(downloadlog, 'r', encoding="utf-8") as f:
            for lastline in f:
                pass
            lastinfo = lastline.split(',')
            if lastinfo[1] == lastinfo[2]:
                lastend = 1
            else:
                lastend = 0    
            lastvol = lastinfo[0]
            lastpage = lastinfo[1]
            return(lastend,lastvol,lastpage)
    

# open('x.txt',"w+")
lastinfo = lastbreak('x.txt')        
print(repr(lastinfo))

# with open('h.json', 'r', encoding="utf-8") as f:
#     vols = json.load(f)
# if lastinfo[0]:
#     tempinfo = next((sub for sub in vols if sub['name'] == lastinfo[1]), None) 
#     tempvol = vols.index(tempinfo) + 1
#     print(str(tempvol),vols[tempvol])
# else:
#     tempinfo = next((sub for sub in vols if sub['name'] == lastinfo[1]), None) 
#     tempvol = vols.index(tempinfo)
#     print(str(tempvol),vols[tempvol])    