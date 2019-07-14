from bs4 import BeautifulSoup
import requests
import json
import sys
import urllib
import codecs
import queue
import threading
import os
import re
exitflag = False
volexitflag = False
reqheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}


# https://www.manhuadb.com/ccbaike/1449/13847/011_ngftrucq.jpg
# https://www.manhuadb.com/manhua/135/1449_13847_p2.html


class get_commic(object):
    def __init__(self):
        self.bookname = 'HunterHunter'
        self.base = 'http://www.manhuadb.com'
        self.homepage = 'http://www.manhuadb.com/manhua/135'  # Hunter * Hunter
        self.book = []

    # 获取每卷的title和url
    def get_booklist(self):
        print("book")
        # # GET CONTENT FROM INTERNET
        # req = requests.get(url=self.homepage,
        #                    headers=reqheaders, verify=False)
        # html = req.text

        # GET CONTENT FROM OFFLINE FILE, testing
        with open('homepage.html', 'rb') as f:
            html = f.read()

        # GET NAME AND URL OF EACH VOLUME
        bf = BeautifulSoup(html, features="lxml")
        li = bf.find_all('li', class_='sort_div')

        for each in li:

            self.book.append({'name': each.a.get('title'),
                              'href': each.a.get('href')})

    # 获取每卷中的每页url，并存入json
    def get_pagelist(self):
        global exitflag
        bookqueue = queue.Queue()
        vols = []
        thread_pages = []
        # 开启4线程
        for i in range(4):
            t = thread_page(bookqueue, vols, self.base)
            t.start()
            thread_pages.append(t)

        # 填充queue
        for book in self.book:
            bookqueue.put(book)

        # 等待队列处理完成
        while not bookqueue.empty():
            pass
        exitflag = True

        # 退出线程
        for thread in thread_pages:
            thread.join()
            print('end thread')
        # print(repr(vols))

        # DUMP TO JSON     utf-8
        with codecs.open(self.bookname+'_thread.json', 'w', encoding="utf-8") as f:
            json.dump(vols, f, ensure_ascii=False)

    def get_piclist(self):
        with open(self.bookname+'_thread.json', 'rb') as f:
            vols = json.load(f)
        global volexitflag
        picqueue = queue.Queue()
        thread_pics = []
        pics = []
        # 开启10线程
        for i in range(10):
            t = thread_pic(picqueue, self.base, pics)
            t.start()
            thread_pics.append(t)

        # 填充queue
        for vol in vols:
            for pic in vol['pages']:
                picqueue.put([vol['name'], pic])

        # 等待队列处理完成
        while not picqueue.empty():
            pass
        volexitflag = True

        # 退出线程
        for thread in thread_pics:
            thread.join()

        # DUMP TO JSON     utf-8
        with codecs.open(self.bookname+'_pic_thread.json', 'w', encoding="utf-8") as f:
            json.dump(pics, f, ensure_ascii=False)

        print('done')


# 抓取page线程
class thread_page(threading.Thread):
    def __init__(self, bookqueue, vols, baseurl):
        threading.Thread.__init__(self)
        self.bookqueue = bookqueue
        self.vols = vols
        self.baseurl = baseurl

    def run(self):
        while not exitflag:
            try:
                book = self.bookqueue.get()
                print(book['name'])
                # self.vols.append(book['name'])
                # time.sleep(1)

                # GET CONTENT FROM INTERNET
                req = requests.get(url=self.baseurl+book['href'],
                                   headers=reqheaders, verify=False)
                html = req.text

                # # GET CONTENT FROM OFFLINE FILE, testing
                # with open('vol.html', 'rb') as f:
                #     html = f.read()

                # GET URL OF EACH PAGE
                bf = BeautifulSoup(html, features="lxml")
                pgs = bf.find(
                    'select', class_='form-control').find_all('option')
                pages = []

                for pg in pgs:
                    pages.append(pg.get('value'))

                book.update({'pages': pages})
                self.vols.append(book)
            except:
                pass

        # print('done')


class thread_pic(threading.Thread):
    def __init__(self, picqueue, baseurl, pics):
        threading.Thread.__init__(self)
        self.picqueue = picqueue
        self.baseurl = baseurl
        self.pics = pics

    def run(self):
        while not volexitflag:
            try:
                pic = self.picqueue.get()
                # print(pic[0], pic[1])
                # 每卷一个目录
                if not os.path.exists(os.path.join(os.path.abspath('.'), pic[0])):
                    os.mkdir(os.path.join(os.path.abspath('.'), pic[0]))

                # 获取页码
                pagex = re.match(r'.*p(\d*).*', pic[1])
                if len(pagex.group(1)) == 0:
                    x = '1'
                else:
                    x = pagex.group(1)
                # print(x)

                # 获取pic URL
                html = requests.get(
                    url=self.baseurl + pic[1], headers=reqheaders, verify=False).text
                picurl = BeautifulSoup(html, features="lxml").find(
                    'img', class_='img-fluid').get('src')
                print(x, picurl)

                self.pics.append([pic[0], x, self.baseurl + picurl])

                # # DOWNLOAD, test
                # with open(os.path.join(os.path.abspath('.'), pic[0], x + '.json'), 'w', encoding="utf-8") as f:
                #     f.write(pic[0]+x + self.baseurl + picurl)

            except:
                pass


if __name__ == '__main__':
    commic = get_commic()
    # commic.get_booklist()
    # commic.get_pagelist()
    commic.get_piclist()
