# ppproxy

## what is this?

it maintained an usable proxy list, which can be used in your project.

## how to use it?
import and it will start 

``` python
from ppproxy import getProxy

with getProxy() as proxy:
    r = requests.get(url, headers=headers, timeout=5, proxies={'http : 'http://' + proxy})
    print r.content

```

## where are ip from?

http://www.kuaidaili.com/free/inha/

http://www.site-digger.com/html/articles/20110516/proxieslist.html



