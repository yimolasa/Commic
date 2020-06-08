from bs4 import BeautifulSoup
import requests
import json
import argparse
# import sys
# import urllib
import codecs
# import queue
# import threading
import os
# import re

reqheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

base = 'http://www.manhuadb.com'
homepage = 'http://www.manhuadb.com/manhua/135'  # Hunter * Hunter
book = []
bookname = 'HunterHunter'
bookfolder = os.path.join(os.path.abspath('.'), 'output', bookname)
booklist = os.path.join(bookfolder, bookname+'.json')


def get_vol():
    if not os.path.exists(bookfolder):
        os.mkdir(bookfolder)

    req = requests.get(url=homepage, headers=reqheaders, verify=False)
    html = req.text
    bf = BeautifulSoup(html, features="lxml")
    li = bf.find_all('li', class_='sort_div')
    for each in li:
        book.append({'name': each.a.get('title'), 'href': each.a.get('href')})

    with codecs.open(booklist, 'w', encoding="utf-8") as f:
        json.dump(book, f, ensure_ascii=False)


def get_page():
    with open(booklist, 'r', encoding="utf-8") as f:
        vols = json.load(f)
    # print(repr(vols))
    for vol in vols:
        volfolder = os.path.join(bookfolder, vol['name'])
        vollist = os.path.join(volfolder, vol['name']+'.json')
        volurl = base + vol['href']
        if not os.path.exists(volfolder):
            os.mkdir(volfolder)
        if not os.path.exists(vollist):
            print(volurl)
            req = requests.get(url=volurl, headers=reqheaders, verify=False)
            html = req.text
            bf =BeautifulSoup(html, features="lxml")
            pgs = bf.find('select', class_='form-control').find_all('option')
            pages = []
            for pg in pgs:
                pages.append(pg.get('value'))
            with codecs.open(vollist, 'w', encoding="utf-8") as f:
                json.dump(pages, f, ensure_ascii=False)    


def main():
    if not os.path.exists(booklist):
        get_vol()
    get_page()


if __name__ == '__main__':
    main()


# def parse_args():
#     parser = argparse.ArgumentParser()
#     # TODO: pass username and password via stdin pipe.
#     parser.add_argument('-m', '--mode', choices=[_DISCOVER_MODE, _UPDATE_MODE],
#                         required=True, help="""Discover mode search for new companies.
#                         Update mode update company detailed information if any.""")
#     parser.add_argument('-u', '--username', required=True, help='Tianyancha username')
#     parser.add_argument('-p', '--password', required=True, help='Tianyancha password')
#     return parser.parse_args()


# def main():
#     args = parse_args()
#     driver = login(args.username, args.password)
#     if args.mode == _DISCOVER_MODE:
#         run_discover_mode(driver)
#     elif args.mode == _UPDATE_MODE:
#         run_update_mode(driver)
#     else:
#         raise ValueError(f'Invalid mode {args.mode}')
