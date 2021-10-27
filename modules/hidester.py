from json import loads

def parse(html):
  parsed = []
  obj = loads(html)
  proxysRaw = obj
  for proxyRaw in proxysRaw:
      parsed.append(proxyRaw['IP']+':'+str(proxyRaw['PORT']))
  return parsed
