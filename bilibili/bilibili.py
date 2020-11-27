import requests
import time

url = 'https://api.live.bilibili.com/ajax/msg'
dat = {
    'roomid':'213',
    'token'	:'',
    'csrf_token':''
}

html = requests.post(url , data = dat)
asd = list(map(lambda ii:html.json()['data']['room'][ii]['text'],range(1)))
print(asd)