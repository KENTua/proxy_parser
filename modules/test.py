#!/usr/bin/python3
import aiohttp
import asyncio

from aiohttp_socks import ProxyConnector
from bs4 import BeautifulSoup as bs
from re import findall
from rich import print
TIMEOUT =2
#asyncio_loop=asyncio.get_running_loop()


#,proxies={'http':'socks5://127.0.0.1:9050'} 34

async def check(proxy:str,session)->str:
    result='error'
    resp=await session.get('https://ident.me',timeout=TIMEOUT)
    #text=await resp.text
    result='https://'+proxy
    return result


async def create_task(proxy:str):
  conn=ProxyConnector.from_url('socks4://127.0.0.1:9050')
  tasks=[]
  print(conn)
  async with aiohttp.ClientSession(connector=conn) as session:
    tasks.append(asyncio.create_task(check(proxy,session)))
    return await asyncio.gather(*tasks)

async def main():
    proxies=['127.0.0.1:9050']
    for proxy in proxies:
        print(await create_task(proxy))


asyncio.run(main())