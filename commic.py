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
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)
browser.set_window_position(0, 0)
browser.set_window_size(1024, 768)

reqheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

base = 'http://www.manhuadb.com'
homepage = 'http://www.manhuadb.com/manhua/135'  # Hunter * Hunter
book = []
bookname = 'HunterHunter'
bookfolder = os.path.join(os.path.abspath('.'), 'output', bookname)
booklist = os.path.join(bookfolder, bookname+'.json')


def get_vol():
    req = requests.get(url=homepage, headers=reqheaders, verify=False)
    html = req.text
    bf = BeautifulSoup(html, features="lxml")
    li = bf.find_all('li', class_='sort_div')
    for each in li:
        book.append({'name': each.a.get('title'),
                     'href': base + each.a.get('href')})

    with codecs.open(booklist, 'w', encoding="utf-8") as f:
        json.dump(book, f, ensure_ascii=False)


def get_page(volurl):
    browser.get(volurl)
    WebDriverWait(browser, 3)
    img = browser.find_element_by_xpath('//*[@id="all"]/div/div[2]/img')
    print(img.get_attribute('src'))
    # import urllib.request
# urllib.request.urlretrieve(src, "filename.png")
    # images = browser.find_elements_by_tag_name('img')
# for image in images:
#     print(image.get_attribute('src'))
    #<img class="img-fluid show-pic" src="https://i2.manhuadb.com/static/57/502/11_fevybtvq.jpg">
    print(volurl)
    # req = requests.get(url=volurl, headers=reqheaders, verify=False)
    # html = req.text
    # bf = BeautifulSoup(html, features="lxml")
    # print(bf.text)
    # pgs = bf.find('select', class_='form-control vg-page-selector').find_all('option')
    # pgnumber = pgs[-1].get('value')
    # print(pgnumber)


def main():
    if not os.path.exists(bookfolder):
        os.mkdir(bookfolder)
    if not os.path.exists(booklist):
        get_vol()

    with open(booklist, 'r', encoding="utf-8") as f:
        vols = json.load(f)
    for vol in vols:
        volfolder = os.path.join(bookfolder, vol['name'])
        volurl = vol['href']
        if not os.path.exists(volfolder):
            os.mkdir(volfolder)
        get_page(volurl)


if __name__ == '__main__':
    main()

    # if headless:
    #     option = webdriver.ChromeOptions()
    #     option.add_argument('headless')
    #     driver = webdriver.Chrome(chrome_options=option)
    # else:
    #     driver = webdriver.Chrome()

    # # 强制声明浏览器长宽为1024*768以适配所有屏幕
    # driver.set_window_position(0, 0)
    # driver.set_window_size(1024, 768)
    # driver_safe_get(driver, _LOGIN_URL)
    # time.sleep(1)

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
