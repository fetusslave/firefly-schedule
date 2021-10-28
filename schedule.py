import requests
from requests import Session
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime

s = Session()

s.headers.update({'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Content-Length': '59',
'Content-Type': 'application/x-www-form-urlencoded',
'Host': 'dcspd.fireflycloud.net.cn',
'Origin': 'https://dcspd.fireflycloud.net.cn',
'Referer': 'https://dcspd.fireflycloud.net.cn/login/login.aspx?prelogin=https%3a%2f%2fdcspd.fireflycloud.net.cn%2f&kr=Cloud:Cloud',
'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
'sec-ch-ua-mobile': '?0',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
                  })

with open('credidentials.txt', 'r') as a:
    username = a.readline().strip('\n')
    password = a.readline().strip('\n')

params = {
'prelogin': '/',
'kr': 'Cloud:Cloud'
}

res = s.post('https://dcspd.fireflycloud.net.cn/login/login.aspx?prelogin=/&kr=Cloud:Cloud', data={'username': username, 'password': password})

res = s.get('https://dcspd.fireflycloud.net.cn/planner/week', data={'username': username, 'password': password})

soup = BeautifulSoup(res.content, 'html.parser')

script = soup.find_all('script')[10].string

w = eval(script[29:])['events']

cal = Calendar()

for i in w:
    event = Event()
    event['summary'] = i['subject']
    event.add('dtstart', datetime.strptime(i['isostartdate'], "%Y-%m-%dT%H:%M:%S"))
    event.add('dtend', datetime.strptime(i['isoenddate'], "%Y-%m-%dT%H:%M:%S"))
    cal.add_component(event)

path = '/'

with open(path, 'wb') as a:
    a.write(cal.to_ical())
