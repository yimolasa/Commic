import requests
import json
import argparse
import urllib.request
import codecs
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

reqheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'}

catalog = 'catalog.json'
base = 'http://www.manhuadb.com'
book = []
bookname = 'JoJo3'
homepage = 'https://www.manhuadb.com/manhua/119'  # Hunter * Hunter
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


def access_vol():
    # get last downlaod page
    lastinfo = lastbreak(downloadlog)
    # get vols
    with open(booklist, 'r', encoding="utf-8") as f:
        vols = json.load(f)

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
    # start to browser
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1024, 768)
    wait = WebDriverWait(browser, 10)
    # download vol by vol
    for vol in todownloadvols:
        volfolder = os.path.join(bookfolder, vol['name'])
        volurl = vol['href']
        if not os.path.exists(volfolder):
            os.mkdir(volfolder)
        # print(volurl, volfolder, startpage)
        get_page(browser, wait, volurl, volfolder, startpage)
        startpage = 1
    # close browser
    browser.close()


def get_page(browser, wait, volurl, volfolder, startpage):
    browser.get(volurl)
    WebDriverWait(browser, 3)

    # total page in VOL
    pages = browser.find_element_by_xpath(
        '//*[@id="page-selector"]/option[last()]').get_attribute('value')

    # jump to start page
    if startpage > 1:
        browser.find_element_by_xpath(
            '//*[@id="page-selector"]/option['+str(startpage)+']').click()

    for i in range(startpage, int(pages)+1):
        # for i in range(1,5): #  test
        try:
            pagename = os.path.join(volfolder, str(i)+'.jpg')
            wait.until(EC.presence_of_element_located((By.ID, "all")))
        except TimeoutError:
            time.sleep(10)
            browser.refresh()
            pagename = os.path.join(volfolder, str(i)+'.jpg')
            wait.until(EC.presence_of_element_located((By.ID, "all")))

        # if not os.path.exists(pagename):
        imgurl = browser.find_element_by_xpath(
            '//*[@id="all"]/div/div[2]/img').get_attribute('src')
        try:
            # urllib.request.urlretrieve(imgurl, pagename)  # downloading
            with open(pagename, 'wb') as f:
                f.write(requests.get(imgurl).content)
        except:
            time.sleep(3)
            try:
                # one more try if failed
                # urllib.request.urlretrieve(imgurl, pagename)
                with open(pagename, 'wb') as f:
                    f.write(requests.get(imgurl).content)
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
    if os.stat(downloadlog).st_size == 0:  # if new log, fresh download
        return(0)
    else:
        with open(downloadlog, 'r', encoding="utf-8") as f:
            for lastline in f:
                pass
            lastinfo = lastline.split(',')
            if lastinfo[1] == lastinfo[2]:  # if last page of the vol
                lastend = 1
            else:
                lastend = 0
            lastvol = lastinfo[0]
            lastpage = lastinfo[1]
            return(lastend, lastvol, lastpage)


def rdepages():  # download again for the failed pages from error log
    if os.stat(downloadlog).st_size > 0:  # if new log, fresh download
        with open(errorlog, 'r+', encoding='utf-8') as f:
            templog = []
            for x in f:
                x = x.rstrip()
                tinfo = x.split(',')
                tempfname = os.path.join(bookfolder, tinfo[0], tinfo[1]+'.jpg')
                try:
                    # urllib.request.urlretrieve(tinfo[3], tempfname)
                    with open(tempfname, 'wb') as w:
                        w.write(requests.get(tinfo[3]).content)
                except:
                    templog.append(x)
            f.seek(0)
            f.writelines(templog)
            f.truncate()


def listbook():
    with open(catalog, 'r', encoding="utf-8") as f:
        books = json.load(f)
    for bk in books:
        print(books.index(bk), bk['bookname'])
    bkid = int(input('Which one to download:\n'))
    if bkid == 0:
        exit()
    if bkid < 1 or bkid >= len(books):
        print('fuck\n')
        bkid = int(input('Which one to download:\n'))
    global bookname, homepage, bookfolder, booklist, downloadlog, errorlog
    bookname = books[bkid]['bookname']
    homepage = books[bkid]['homepage']  # Hunter * Hunter
    bookfolder = os.path.join(os.path.abspath('.'), 'output', bookname)
    booklist = os.path.join(bookfolder, bookname+'.json')
    downloadlog = os.path.join(bookfolder, 'dlog.txt')
    errorlog = os.path.join(bookfolder, 'error.txt')    


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='shutdown system')
    parser.add_argument('-r', action='store_true',
                        help='down again from error log')
    parser.add_argument('-f', action='store_true', help='force update')
    parser.add_argument('-l', action='store_true', help='list book')
    return parser.parse_args()


def initx():
    if not os.path.exists(bookfolder):
        os.mkdir(bookfolder)
    if not os.path.exists(downloadlog):
        open(downloadlog, "w+")
    if not os.path.exists(errorlog):
        open(errorlog, "w+")


def main():
    args = parse_args()
    initx()  # prepare necessary folder and files

    if args.l:
        listbook()
    # create vols's url > json.
    if not os.path.exists(booklist) or args.f:
        get_vol()

    # download in order
    if args.r:
        rdepages()
    else:
        access_vol()

    # -s to shutdown
    if args.s:
        os.system("shutdown /s /f /t 1")


if __name__ == '__main__':
    main()
