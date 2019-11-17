from bs4 import BeautifulSoup
import requests
import json
import sys
import urllib
import codecs
import queue
import threading
import time

exitflag = False
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
        volqueue = queue.Queue()
        vols = []
        thread_pages = []
        # 开启4线程
        for i in range(4):
            t = thread_page(bookqueue, volqueue, vols, self.base)
            t.start()
            #t.join()
            thread_pages.append(t)

        # 填充queue
        for book in self.book:
            bookqueue.put(book)

        # 等待队列处理完成
        while not bookqueue.empty():
            pass
        exitflag = True

        # 退出线程
        # for thread in thread_pages:
        #     thread.join()
        #     print('end thread')
        # print(repr(vols))

        # # DUMP TO JSON     utf-8-sig
        # with codecs.open(self.bookname+'_thread.json', 'w', encoding="utf-8") as f:
        #     json.dump(vols, f, ensure_ascii=False)


# 抓取page线程
class thread_page(threading.Thread):
    def __init__(self, bookqueue, volqueue, vols, baseurl):
        threading.Thread.__init__(self)
        self.bookqueue = bookqueue
        self.vols = vols
        self.baseurl = baseurl

    def run(self):
        while not exitflag:
            try:
                book = self.bookqueue.get()
                print(book['name'])
                # # self.vols.append(book['name'])
                # # time.sleep(1)

                # # GET CONTENT FROM INTERNET
                # req = requests.get(url=self.baseurl+book['href'],
                #                    headers=reqheaders, verify=False)
                # html = req.text

                # # # GET CONTENT FROM OFFLINE FILE, testing
                # # with open('vol.html', 'rb') as f:
                # #     html = f.read()

                # # GET URL OF EACH PAGE
                # bf = BeautifulSoup(html, features="lxml")
                # pgs = bf.find(
                #     'select', class_='form-control').find_all('option')
                # pages = []

                # for pg in pgs:
                #     pages.append(pg.get('value'))

                # book.update({'pages': pages})
                # self.vols.append(book)
            except:
                pass

        # print('done')


if __name__ == '__main__':
    commic = get_commic()
    commic.get_booklist()
    commic.get_pagelist()
    # commic.get_piclist()
