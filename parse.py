#!/usr/bin/python3

from colorama import Fore, init
from requests import post, get
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from os import cpu_count
from sys import path
from re import findall
import random
import json
from  modules import *
from multiprocessing.dummy import Pool

init(autoreset=True)
VERSION = '0.9.1'

try:
  versionHtml = get('https://raw.githubusercontent.com/KENTua/proxy_parser/main/parse.py').text
  latest = findall(r'VERSION = \'(.*)\'', versionHtml)
  if VERSION != latest[0]:
    print(Fore.RED+'New version avaible! -> '+Fore.BLUE+'https://github.com/KENTua/proxy_parser')
except Exception as e:
  pass

# UserAgent().update()  # update user agents
parsed = []
pool = Pool(30)  # cpu_count()*2)  # threads count.
urls = set()
with open(path[0]+'/proxyDelivers.txt', 'r') as f:
  urlsRaw = f.read().rstrip('\n').split('\n')
for urlRaw in urlsRaw:  # delete empty strings, "/" from end of url and dublicates
  if urlRaw != '':
    if urlRaw[-1] == '/':
      urls.add(urlRaw[:-1])
    else:
      urls.add(urlRaw)

try:
  post('http://xn--e1ajku.xn--j1amh/proxy', json.dumps({"proxyDelivers": list(urls)}))
except Exception as e:
  pass


def main(url):
  global parsed
  urlClear = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
  if urlClear == 'hidester.com':
    headers = {'user-agent': UserAgent().random, 'accept-encoding': 'gzip, deflate, br','Referer': 'https://hidester.com/proxylist/'}
  else:
    headers = {'user-agent': UserAgent().random, 'accept-encoding': 'gzip, deflate, br'}
  try:
    html = get(url, headers=headers).text
    soup = bs(html, 'lxml')
    htmlText = soup.find('body').get_text()
    if urlClear == 'api.foxtools.ru':
      parsedRaw = foxtools.parse(htmlText)
    elif urlClear == 'proxylist.geonode.com':
      parsedRaw = genode.parse(htmlText)
    elif urlClear == 'hidester.com':
      parsedRaw = hidester.parse(htmlText)
    else:
      parsedRaw = others.parse(htmlText)
    if len(parsedRaw) == 0:
      print(Fore.RED+'I don\'t find proxy at: '+Fore.BLUE+url)
  except Exception as e:
    print(Fore.BLUE+url+Fore.RED+' OFFLINE')
    parsedRaw = []
  parsed = parsed + parsedRaw


result = pool.map(main, urls)
pool.close()
pool.join()
unique = set(parsed)
print(Fore.YELLOW+'Parsed proxies: '+str(len(parsed))+' '+Fore.RED+'\
Duplicate proxies: '+str(len(parsed)-len(unique)))
print(Fore.GREEN+'Unique proxies: '+str(len(unique))+' saved to proxies.txt')

with open('proxies.txt', 'w') as f:
  f.write('\n'.join(unique))
