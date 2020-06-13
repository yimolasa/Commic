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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
browser = webdriver.Chrome(options=options)
browser.set_window_position(0, 0)
browser.set_window_size(1024, 768)
wait = WebDriverWait(browser, 10)
reqheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

base = 'http://www.manhuadb.com'
book = []
bookname = 'HunterHunter'
homepage = 'http://www.manhuadb.com/manhua/135'  # Hunter * Hunter
bookfolder = os.path.join(os.path.abspath('.'), 'output', bookname)
booklist = os.path.join(bookfolder, bookname+'.json')
downloadlog = os.path.join(bookfolder, 'dlog.txt')
errorlog = os.path.join(bookfolder, 'error.txt')


def dlog(msg, xlog):
    with open(xlog, "a", encoding="utf-8") as f:
        f.write(msg + '\n')


def get_vol():
    req = requests.get(url=homepage, headers=reqheaders, verify=False)
    html = req.text
    bf = BeautifulSoup(html, features="lxml")
    li = bf.find_all('li', class_='sort_div')
    for each in li:
        book.append({'name': each.a.get('title'),
                     'href': base + each.a.get('href')})
    # dump json {"name": VOLname, "href": URL}
    with codecs.open(booklist, 'w', encoding="utf-8") as f:
        json.dump(book, f, ensure_ascii=False)


def access_vol(lastinfo, vols):
    if lastinfo:  # continue to downlaod
        tempinfo = next(
            (sub for sub in vols if sub['name'] == lastinfo[1]), None)
        if lastinfo[0]:  # if last page of the volume
            tempvol = vols.index(tempinfo) + 1
            todownloadvols = vols[tempvol:]
            startpage = 1

        else:
            tempvol = vols.index(tempinfo)
            todownloadvols = vols[tempvol:]
            startpage = int(lastinfo[2]) + 1
    else:  # fresh start
        todownloadvols = vols
        startpage = 1
    # start to download
    for vol in todownloadvols:
        volfolder = os.path.join(bookfolder, vol['name'])
        volurl = vol['href']
        if not os.path.exists(volfolder):
            os.mkdir(volfolder)
        # print(volurl, volfolder, startpage)
        get_page(volurl, volfolder, startpage)
        startpage = 1


def get_page(volurl, volfolder, startpage):
    browser.get(volurl)
    WebDriverWait(browser, 3)

    # total page in VOL
    pages = browser.find_element_by_xpath(
        '//*[@id="page-selector"]/option[last()]').get_attribute('value')
    
    # jump to start page
    if startpage > 1:
        browser.find_element_by_xpath('//*[@id="page-selector"]/option['+str(startpage)+']').click()

    for i in range(startpage, int(pages)+1):
        # for i in range(1,5):
        pagename = os.path.join(volfolder, str(i)+'.jpg')
        wait.until(EC.presence_of_element_located((By.ID, "all")))
        #  with a try catch later & a file existing detect
        # if not os.path.exists(pagename):
        imgurl = browser.find_element_by_xpath(
            '//*[@id="all"]/div/div[2]/img').get_attribute('src')
        try:
            urllib.request.urlretrieve(imgurl, pagename) # downloading
        except:
            time.sleep(3)
            try:
                urllib.request.urlretrieve(imgurl, pagename) # one more try if failed
            except:
                msg = os.path.basename(
                    volfolder) + ',' + str(i) + ',' + pages + ',' + imgurl
                dlog(msg, errorlog)
        else:
            msg = os.path.basename(volfolder) + ',' + \
                str(i) + ',' + pages + ',' + imgurl
            dlog(msg, downloadlog)
        print(str(i))

        if i == int(pages):
            break
        nextpage = browser.find_element_by_xpath(
            '/html/body/div/div[1]/nav/div/a[3]').click()
        # with a wait
        time.sleep(2)


def lastbreak(downloadlog):
    if os.stat(downloadlog).st_size == 0: # if new log, fresh download
        return(0)
    else:
        with open(downloadlog, 'r', encoding="utf-8") as f:
            for lastline in f:
                pass
            lastinfo = lastline.split(',')
            if lastinfo[1] == lastinfo[2]: # if last page of the vol
                lastend = 1
            else:
                lastend = 0
            lastvol = lastinfo[0]
            lastpage = lastinfo[1]
            return(lastend, lastvol, lastpage)


def main():
    # prepare necessary folder and files
    if not os.path.exists(bookfolder):
        os.mkdir(bookfolder)
    if not os.path.exists(downloadlog):
        open(downloadlog, "w+")
    if not os.path.exists(errorlog):
        open(errorlog, "w+")

    # get vols's url > json
    if not os.path.exists(booklist):
        get_vol()

    # get last downlaod page
    lastinfo = lastbreak(downloadlog)

    # download in order
    with open(booklist, 'r', encoding="utf-8") as f:
        vols = json.load(f)
    access_vol(lastinfo, vols)

    browser.close()


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


# PROXY = "<HOST:PORT>"
# webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "proxyType": "MANUAL",

# }

# with webdriver.Firefox() as driver:
#     # Open URL
#     driver.get("https://selenium.dev")
