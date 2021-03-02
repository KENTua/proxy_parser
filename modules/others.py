from re import findall

def parse(html):
  parsed = []
  parsedRaw = findall(r'((\d{1,3}\.){3}\d{1,3}:\d{2,5})', html)
  for proxy in parsedRaw:
    parsed.append(proxy[0])
  #print(parsed)
  return parsed
