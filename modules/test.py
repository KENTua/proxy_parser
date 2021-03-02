#!/usr/bin/python3
from requests import get
from bs4 import BeautifulSoup as bs
from re import findall

html = get('https://www.sslproxies.org').text

soup = bs(html, 'lxml')
htmlText = soup.find('body').get_text()

parsed = []
parsedRaw = findall(r'((\d{1,3}\.){3}\d{1,3}:\d{2,5})', htmlText)
print(html)
for proxy in parsedRaw:
  parsed.append(proxy[0])
  print(proxy[0])

#print(parsed)
