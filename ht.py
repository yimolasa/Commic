from bs4 import BeautifulSoup
import requests
import json
import sys
import urllib
import codecs


# https://www.manhuadb.com/ccbaike/1449/13847/011_ngftrucq.jpg
# https://www.manhuadb.com/manhua/135/1449_13847_p2.html

class get_commic(object):
    def __init__(self):
        self.bookname = 'HunterHunter'
        self.base = 'http://www.manhuadb.com'
        self.homepage = 'http://www.manhuadb.com/manhua/135'  # Hunter * Hunter
        self.book = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

    def get_booklist(self):
        print("book")
        # GET CONTENT FROM INTERNET
        req = requests.get(url=self.homepage,
                           headers=self.headers, verify=False)
        html = req.text

        # # GET CONTENT FROM OFFLINE FILE
        # with open('homepage.html', 'rb') as f:
        #     html = f.read()

        # GET NAME AND URL OF EACH VOLUME
        bf = BeautifulSoup(html, features="lxml")
        li = bf.find_all('li', class_='sort_div')

        for each in li:

            self.book.append({'name': each.a.get('title'),
                              'href': each.a.get('href')})

    def get_pagelist(self):

        for each in self.book:
            print(each['name'])
            # GET CONTENT FROM INTERNET
            req = requests.get(url=self.base+each['href'],
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
                pages.append(pg.get('value'))

            each.update({'pages': pages})

        # DUMP TO JSON     utf-8-sig
        with codecs.open(self.bookname+'.json', 'w', encoding="utf-8") as f:
            json.dump(self.book, f, ensure_ascii=False)

    def get_piclist(self):
        with open(self.bookname+'.json', 'rb') as f:
            vols = json.load(f)
        for vol in vols:
            i = 1
            pics = []
            for pic in vol['pages']:
                tempurl = self.base+pic
                html = requests.get(
                    url=tempurl, headers=self.headers, verify=False).text
                picurl = BeautifulSoup(html, features="lxml").find(
                    'img', class_='img-fluid').get('src')

                pics.append([{'page': i}, {'url': self.base+picurl}])
                i += 1

            # DUMP TO JSON
            with codecs.open(vol['name']+'.json', 'w', encoding="utf-8") as f:
                json.dump(pics, f, ensure_ascii=False)

    def download(self, target, filename):
        print("Download")
        urllib.request.urlretrieve(image_url, full_file_name)


if __name__ == '__main__':
    commic = get_commic()
    # commic.get_booklist()
    # commic.get_pagelist()
    # commic.get_piclist()
