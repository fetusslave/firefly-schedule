from requests import Session
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta

# amount of weeks to get schedule of
weeks = 10

# path of .ics file
path = ''

url = 'https://dcspd.fireflycloud.net.cn/planner/week'

cal = Calendar()

s = Session()

s.headers.update({
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '59',
    'Content-Type': 'application/x-www-form-urlencoded',
    #'Cookie': 'ASP.NET_SessionId=rnihgriwa2edzovo4x3cy30d; AWSELB=ADCDC31F0453FE7D4F8FCE13573EF235BC61CB3CFD62DE9E2BD8AFCF2B0FDC7CD3F784EFC7334034BB56C6DB1A6C852B016D215BB9968E5A1F02B0F4BD20C0FB9C027B5724; AWSELBCORS=ADCDC31F0453FE7D4F8FCE13573EF235BC61CB3CFD62DE9E2BD8AFCF2B0FDC7CD3F784EFC7334034BB56C6DB1A6C852B016D215BB9968E5A1F02B0F4BD20C0FB9C027B5724; FireflyNETLoggedIn=yes; SessionSecureA=r0s8eG3gU3s3QVW5TWnA9H2qexnhI4sCpUy+dmz0AMe3iUIgBza1zyOMrt3Qe/4n2EM=; SessionSecureB=poPzRwcI55hEObWzEcNhmT6bOANNzTZtRcdXf5Cp2KUbtrv6GBEguRFWUHH8Eo0O3gc=',
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

with open('w.txt', 'r') as a:
    username = a.readline().strip('\n')
    password = a.readline().strip('\n')

#https://dcspd.fireflycloud.net.cn/login/login.aspx?prelogin=/&kr=Cloud:Cloud
res = s.post('https://dcspd.fireflycloud.net.cn/login/login.aspx?prelogin=/&kr=Cloud:Cloud', data={'username': username, 'password': password})

print(res.status_code)

now = datetime.now()

current = now.replace(second=0, microsecond=0)-timedelta(days=now.weekday())

def get_schedule(date):
    global username, password, s
    res = s.get(f"{url}/{date.strftime('%Y-%m-%d')}", data={'username': username, 'password': password})

    print(res.status_code)

    soup = BeautifulSoup(res.content, 'html.parser')

    script = soup.find_all('script')

    w = eval(script[10].string[29:])['events']

    for i in w:
        event = Event()
        event['summary'] = i['subject']
        event.add('dtstart', datetime.strptime(i['isostartdate'], "%Y-%m-%dT%H:%M:%S"))
        event.add('dtend', datetime.strptime(i['isoenddate'], "%Y-%m-%dT%H:%M:%S"))
        cal.add_component(event)

for i in range(weeks):
    get_schedule(current)
    current += timedelta(days=7)

with open(path, 'wb') as a:
    a.write(cal.to_ical())
