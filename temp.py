import requests
import json
import sys
import urllib
from bs4 import BeautifulSoup

a=[]
a.append({'a':'a','b':'b'})
a.append({'a1':'a1','b1':'b1'})
print(repr(a))
a[0].update({'c':'c'})
print(repr(a))