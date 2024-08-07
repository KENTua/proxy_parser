#!/usr/bin/python3
from requests import get,post
from bs4 import BeautifulSoup as bs
from re import findall
from rich import print

#,proxies={'http':'socks5://127.0.0.1:9050'} 34

html=get('https://www.proxy-list.download/api/v1/get?type=socks4',timeout=5).text
print(html)

exit()
soup = bs(html, 'lxml')
htmlText = soup.find('body').get_text()

parsed = []
parsedRaw = findall(r'((\d{1,3}\.){3}\d{1,3}:\d{2,5})', htmlText)
print(html)
for proxy in parsedRaw:
  parsed.append(proxy[0])
  print(proxy[0])

#print(parsed)
