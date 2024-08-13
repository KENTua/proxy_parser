from requests import get
from rich.console import Console
from os import cpu_count
from multiprocessing.dummy import Pool

pool = Pool(60)#cpu_count()*2)  # threads count
console=Console()
TIMEOUT =2
with open('proxies.txt','r') as f:
    proxies = f.read().rstrip('\n').split('\n')


def check(proxy:str)->str:
    result='error'
    try:
        get('https://ident.me',proxies={'https':'https://'+proxy},timeout=TIMEOUT)
        #text=await resp.text
        result='https://'+proxy
    except:
        try:
            get('https://ident.me',proxies={'https':'socks4://'+proxy},timeout=TIMEOUT)
            #text=await resp.text
            result='socks4://'+proxy
        except:
            pass
    return result


def main():
    goods=[]
    print('to check:',len(proxies))
    results = pool.map(check, proxies)
    pool.close()
    pool.join()
    for result in results:
        if result!='error':
            style='bold green'
            goods.append(result)
        else:
            style='bold red'
        #console.print(result,style=style)
    with open('checked.txt', 'w') as f:
        f.write('\n'.join(goods))
        

if __name__=='__main__':
    main()