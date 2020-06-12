from bs4 import BeautifulSoup
import requests
import json
import argparse
import urllib.request
# import sys
# import urllib
import codecs
# import queue
# import threading
import os
import time
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

def dlog():
    print('fuck holder')

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


def get_page(volurl, volfolder):
    browser.get(volurl)
    WebDriverWait(browser, 3)
    pages = browser.find_element_by_xpath(
        '//*[@id="page-selector"]/option[last()]').get_attribute('value')

    # for i in range(1,int(pages)+1):
    for i in range(1,3):
        pagename = os.path.join(volfolder, str(i)+'.jpg')
        imgurl = browser.find_element_by_xpath('//*[@id="all"]/div/div[2]/img').get_attribute('src')
        #  with a try catch later & a file existing detect
        urllib.request.urlretrieve(imgurl, pagename)
        print(str(i))
        time.sleep(2)
        nextpage = browser.find_element_by_xpath('/html/body/div/div[1]/nav/div/a[3]').click()
        # with a wait
        time.sleep(2)


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
        get_page(volurl, volfolder)
        


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


from selenium import webdriver

PROXY = "<HOST:PORT>"
webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
    "httpProxy": PROXY,
    "ftpProxy": PROXY,
    "sslProxy": PROXY,
    "proxyType": "MANUAL",

}

with webdriver.Firefox() as driver:
    # Open URL
    driver.get("https://selenium.dev")