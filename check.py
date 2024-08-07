from requests import get

with open('proxies.txt','r') as f:
    proxies = f.read().rstrip('\n').split('\n')


for proxy in proxies:
    print(proxy)
    try:
        resp=get('https://ident.me',proxies={'https':'https://'+proxy}).text
        print(resp)
    except:
        pass
