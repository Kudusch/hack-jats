import xml
import requests
import feedparser


test_url = "http://academic.oup.com/rss/site_6088/OpenAccess.xml"

#GET /rss/site_6088/OpenAccess.xml HTTP/1.

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "SaneID=DKX0DdzPkbe-cbK0AYL; _ga=GA1.2.626144651.1615302341; OUP_SessionId=e2iiqyuayrfmkzqyrn51ytg5; Oxford_AcademicMachineID=637890703085116346",
    "Host": "academic.oup.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS"
}

cookies={'OUP_SessionId':'hpxgd0fuq2hbzrsycie1c4ci', 'Oxford_AcademicMachineID':'637890699747887954', 'KEY':"1370909*1484969:1978426888:1561096246:1"}

cookies = {"SaneID":"DKX0DdzPkbe-cbK0AYL", "_ga":"GA1.2.626144651.1615302341", "OUP_SessionId":"e2iiqyuayrfmkzqyrn51ytg5", "Oxford_AcademicMachineID":"637890703085116346"}

headers = {'Host':'academic.oup.com',
           'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
           'Accept-Language':'en-US,en;q=0.5',
           'Accept-Encoding':'gzip, deflate, br',
           'Cache-Control': 'no-cache',
           'If-None-Match': None,
           'Pragma': 'no-cache',
           'DNT': '1',
           'Connection': 'keep-alive',
           'Sec-Fetch-Dest': 'empty',
           'Sec-Fetch-Mode':'cors',
           'Sec-Fetch-Site': 'same-origin',
           'sec-ch-ua-platform': "Linux"
           }


cookies = {"SaneID":"DKX0DdzPkbe-cbK0AYL", "_ga":"GA1.2.626144651.1615302341", "OUP_SessionId":"e2iiqyuayrfmkzqyrn51ytg5", "Oxford_AcademicMachineID":"637890703085116346"}


import requests
cookies = {"SaneID":"DKX0DdzPkbe-cbK0AYL", "_ga":"GA1.2.626144651.1615302341", "OUP_SessionId":"0ybai15txtgb1dyiszocdbuh", "Oxford_AcademicMachineID":"637286288694795633"}
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "SaneID=DKX0DdzPkbe-cbK0AYL; _ga=GA1.2.626144651.1615302341; OUP_SessionId=e2iiqyuayrfmkzqyrn51ytg5; Oxford_AcademicMachineID=637890703085116346",
    "Host": "academic.oup.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS"
}
u = "https://academic.oup.com/rss/site_6088/OpenAccess.xml"
r = requests.get(url=u, cookies=cookies, headers=headers)
print(r.content)

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,de;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "Cookie: Oxford_AcademicMachineID=637286288694795633; oup-cookie=1_25-2-2022; OUP_SessionId=0ybai15txtgb1dyiszocdbuh; KEY=1080847*1181681:285799632:971700251:1"
    "Host": "academic.oup.com",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "sec-ch-ua": "' Not A;Brand';v='99', 'Chromium';v='101', 'Google Chrome';v='101'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS"
}

u = "https://academic.oup.com/rss/site_6088/OpenAccess.xml"

r = requests.get(url=u, cookies=cookies, headers=headers)


# headers = {
#     'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
#     'From': 'nathante@uw.edu'  # This is another valid field
# }


def get_rss_url(url):
    try:
        req = requests.get(url, headers=headers, cookies=cookies)
        feedparser.parse(url)

    except Error as _:
    
