#!/usr/bin/python3

from colorama import Fore, init
from requests import get
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from os import cpu_count
from sys import path
from  modules import *
from multiprocessing.dummy import Pool

init(autoreset=True)

parsed = []
pool = Pool( cpu_count()*2)  # threads count. 30
urls = set()
with open(path[0]+'/proxyDelivers.txt', 'r') as f:
  urlsRaw = f.read().rstrip('\n').split('\n')
for urlRaw in urlsRaw:  # delete empty strings, "/" from end of url and dublicates
  if urlRaw != '':
    if urlRaw[-1] == '/':
      urls.add(urlRaw[:-1])
    else:
      urls.add(urlRaw)


def main(url):
  global parsed
  urlClear = url.replace('https://', '').replace('http://', '').replace('www.', '').split('/')[0]
  if urlClear == 'hidester.com':
    headers = {'user-agent': UserAgent().random, 'accept-encoding': 'gzip, deflate, br','Referer': 'https://hidester.com/proxylist/'}
  else:
    headers = {'user-agent': UserAgent().random, 'accept-encoding': 'gzip, deflate, br'}
  try:
    if urlClear=='aliveproxy.com':
      html=get(url, headers=headers,timeout=5,proxies={'http':'socks5://127.0.0.1:9050'}).text
    else:
      html = get(url, headers=headers,timeout=5).text
    soup = bs(html, 'lxml')
    htmlText = soup.find('body').get_text()
    if urlClear == 'api.foxtools.ru':
      parsedRaw = foxtools.parse(htmlText)
    elif urlClear == 'proxylist.geonode.com':
      parsedRaw = genode.parse(htmlText)
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
