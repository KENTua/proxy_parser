from json import loads

def parse(html):
  parsed = []
  obj = loads(html)
  proxysRaw = obj['response']['items']
  for proxyRaw in proxysRaw:
      parsed.append(proxyRaw['ip']+':'+str(proxyRaw['port']))
  return parsed
