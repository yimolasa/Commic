from bs4 import BeautifulSoup
import requests
import json
import sys
#from __future__ import unicode_literals
import codecs


# https://www.manhuadb.com/ccbaike/1449/13847/011_ngftrucq.jpg
# https://www.manhuadb.com/manhua/135/1449_13847_p2.html

class get_commic(object):
    def __init__(self):
        self.bookname = 'HunterHunter'
        self.base = 'http://www.manhuadb.com'
        self.homepage = 'http://www.manhuadb.com/manhua/135'  # Hunter * Hunter
        self.book = []
        self.booklist = []
        self.pagelist = {}  # {'xx':['x','x','x','x','x']}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

    def get_booklist(self):
        print("book")
        # GET CONTENT FROM INTERNET
        # req = requests.get(url=self.homepage,
        #                    headers=self.headers, verify=False)
        # html = req.text

        # GET CONTENT FROM OFFLINE FILE
        with open('homepage.html', 'rb') as f:
            html = f.read()
        # print(html)

        # GET NAME AND URL OF EACH VOLUME
        bf = BeautifulSoup(html, features="lxml")
        li = bf.find_all('li', class_='sort_div')
        # print(repr(li))
        # print(type(li))
        for each in li:
            # print(repr(each.a.get('title')))
            # self.booklist.append(each.a.get('title'))
            # self.pagelist.update({each.a.get('href'): ''})
            self.book.append([{'name': each.a.get('title')},
                              {'href': each.a.get('href')}])
        # print(repr(self.book[3]))
        # print(repr(self.pagelist))

    def get_pagelist(self):
        print("page")
        for each in self.book:
            # GET CONTENT FROM INTERNET
            req = requests.get(url=self.base+each[1]['href'],
                               headers=self.headers, verify=False)
            html = req.text

            # # GET CONTENT FROM OFFLINE FILE
            # with open('vol.html', 'rb') as f:
            #     html = f.read()

            # GET URL OF EACH PAGE
            bf = BeautifulSoup(html, features="lxml")
            pgs = bf.find('select', class_='form-control').find_all('option')
            pages = []
            for pg in pgs:
                # print(pg.get('value'))
                pages.append(pg.get('value'))
            each.append({'pages':pages})   

        # DUMP TO JSON
        with codecs.open(self.bookname+'.json', 'w', encoding="utf-8") as f:
            json.dump(self.book, f, ensure_ascii=False)     

    def download(self, target, filename):
        print("Download")


if __name__ == '__main__':
    commic = get_commic()
    commic.get_booklist()
    commic.get_pagelist()
