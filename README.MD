## How to run
```
# modify constants.py last 2 line, then run
python commic.py

# modify catalog.json, then run, then pick the id.
python commic.py -l

```

## Commic.py
New version.

## Update
* Old version is not supported, sicne the page url was replaced by js. New version use selenium instead.
* Add "download from last stop page"
* Add "retry the failed page"
* Add "shutdown Windows system after completed"
* Modify "find_element"
## Tips

* Find dictionary matching value in list
```
# sub = {'name':'a'}, vols = [sub1, sub2...]
tempinfo = next((sub for sub in vols if sub['name'] == lastinfo[1]), None)
```

* Jump to page by click the drop down list
```
if startpage > 1:
    browser.find_element_by_xpath('//*[@id="page-selector"]/option['+str(startpage)+']').click()
```            

* Read and overwrite file
```
# errorlog will be overwriten by tenmplog[]
with open(errorlog, 'r+', encoding='utf-8') as f:
    templog = []
    for x in f:
        try:
            whatever
        except:
            templog.append(x)
    f.seek(0) # jump to line 1
    f.writelines(templog) # insert new lines
    f.truncate() # clean the rest lines
```

* Boolean arguments 
```
# python x.py -s -r
...
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', help='shutdown system')
    parser.add_argument('-r', action='store_true', help='down again from error log')
    return parser.parse_args()
...
if args.r:
    whatever
...    
```

* Shutdown system, Windows
```
os.system("shutdown /s /f /t 1")
```

* How to cralwler when js is found.

<https://www.k0rz3n.com/2019/03/05/%E7%88%AC%E8%99%AB%E7%88%AC%E5%8F%96%E5%8A%A8%E6%80%81%E7%BD%91%E9%A1%B5%E7%9A%84%E4%B8%89%E7%A7%8D%E6%96%B9%E5%BC%8F%E7%AE%80%E4%BB%8B/>