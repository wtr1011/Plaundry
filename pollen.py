# Pollen scattering
# coding by: Wataru Hamanishi
# !/usr/bin/python
# -*- encoding: utf-8  -*-

import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

def page_detector(area, id):
    if area == "北海道地域":
        next_page = 'OpenSaisinHyou(01)'
        add_url = "1/"
    elif area == "東北地域":
        next_page = 'OpenSaisinHyou(02)'
        add_url = "2/"
    elif area == "関東地域":
        next_page = 'OpenSaisinHyou(03)'
        add_url = "3/"
    elif area == "北陸地域":
        next_page = 'OpenSaisinHyou(05)'
        add_url = "4/"
    elif area == "東海地域":
        next_page = 'OpenSaisinHyou(05)'
        add_url = "5/"
    elif area == "関西地域":
        next_page = 'OpenSaisinHyou(06)'
        add_url = "6/"
    elif area == "中国地域":
        next_page = 'OpenSaisinHyou(07)'
        add_url = "7/"
    elif area == "四国地域":
        next_page = 'OpenSaisinHyou(07)'
        add_url = "8/"
    elif area == "九州地域":
        next_page = 'OpenSaisinHyou(08)'
        add_url = "9/"

    if id == 1:
        return next_page
    elif id == 2:
        return add_url

def time2name():
    # 現在時刻の取得
<<<<<<< HEAD
    now     = datetime.datetime.now()
    year     = now.strftime("%Y")
    month  = now.strftime("%m")
    day      =  now.strftime("%d")
    hour     = now.hour
    minute  = now.minute
=======
    now    = datetime.datetime.now()
    year   = now.strftime("%Y")
    month  = now.strftime("%m")
    day    =  now.strftime("%d")
    hour   = now.hour
    minute = now.minute
>>>>>>> upstream/master

    # 毎時35分データ更新対策
    if minute < 35:
        hour = hour - 1
        hour = str(hour)
    elif minute >= 35:
        hour = str(hour)

    file_name = year + month + day + hour

    return file_name

def split_list(list, num):
    for index in range(0, len(list), num):
        yield list[index:index+num]

def pollen_forcast(area):
    target_url = 'https://tenki.jp/pollen/week/'
<<<<<<< HEAD
    #data = pd.read_html(target_url, header=0, encoding="shift-jis")
    request_page = requests.get(target_url)
    soup = BeautifulSoup(request_page.content, "html.parser")

    #print(rows)

    add_url = page_detector(area, 2)
    next_link = target_url + add_url

    request_page = requests.get(next_link)
    soup = BeautifulSoup(request_page.content, "html.parser")
    table = soup.findAll('table', {'class':'week-index-table'})[0]
    rows = table.findAll('td')
=======
    
    request_page = requests.get(target_url)
    soup         = BeautifulSoup(request_page.content, "html.parser")

    add_url   = page_detector(area, 2)
    next_link = target_url + add_url

    request_page = requests.get(next_link)
    soup         = BeautifulSoup(request_page.content, "html.parser")
    table        = soup.findAll('table', {'class':'week-index-table'})[0]
    rows         = table.findAll('td')
>>>>>>> upstream/master

    data = []
    for row in rows:
        data.append(row.get_text())

    data = list(split_list(data, 8))
    print(data)
<<<<<<< HEAD
=======

>>>>>>> upstream/master
    return data

def pollen_now(area):
    target_url = 'http://kafun.taiki.go.jp/#' # 環境省花粉観測システム（愛称：はなこさん）
<<<<<<< HEAD
    request_page = requests.get(target_url)

    soup = BeautifulSoup(request_page.text, "html.parser")

    next_page = page_detector(area,1)
    links = soup.findAll('a')
=======
    
    request_page = requests.get(target_url)
    soup         = BeautifulSoup(request_page.text, "html.parser")

    next_page = page_detector(area,1)
    links     = soup.findAll('a')
    
>>>>>>> upstream/master
    for link in links:
        if link.get('onclick') == next_page:
            area_code = link.get('onclick')
            area_code = area_code[15:17]
            next_link = "http://kafun.taiki.go.jp/HyouSaisin0.aspx?Area=" + area_code
<<<<<<< HEAD
            request_page = requests.get(next_link)

    soup = BeautifulSoup(request_page.content, "html.parser")
=======
           
            request_page = requests.get(next_link)

    soup  = BeautifulSoup(request_page.content, "html.parser")
>>>>>>> upstream/master
    links = soup.findAll('frame')

    file_name = time2name()
    for link in links:
        if link.get('name') == 'main':
            next_link = "http://kafun.taiki.go.jp/Gazou/Hyou/AllMst/ha" + \
                file_name + area_code + ".html"
            print(next_link)
            request_page = requests.get(next_link)

    data = pd.read_html(next_link, header=0)
    data = data[1]
    print(data)

def pollen():
    area = "関東地域" # inputデータのarea情報

<<<<<<< HEAD
    now_data      = pollen_now(area)
=======
    now_data     = pollen_now(area)
>>>>>>> upstream/master
    forcast_data = pollen_forcast(area)

if __name__ == '__main__':
    pollen()
