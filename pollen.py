# Pollen scattering
# coding by: Wataru Hamanishi
# !/usr/bin/python
# -*- encoding: utf-8  -*-

import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

def page_detector(area):

    if area == "北海道地域":
        next_page = 'OpenSaisinHyou(01)'
    elif area == "東北地域":
        next_page = 'OpenSaisinHyou(02)'
    elif area == "関東地域":
        next_page = 'OpenSaisinHyou(03)'
    elif area == "中部地域":
        next_page = 'OpenSaisinHyou(05)'
    elif area == "関西地域":
        next_page = 'OpenSaisinHyou(06)'
    elif area == "中国・四国地域":
        next_page = 'OpenSaisinHyou(07)'
    elif area == "九州地域":
        next_page = 'OpenSaisinHyou(08)'

    return next_page

def time2name():
    # 現在時刻の取得
    now     = datetime.datetime.now()
    year     = now.strftime("%Y")
    month  = now.strftime("%m")
    day      =  now.strftime("%d")
    hour     = now.hour
    minute  = now.minute

    # 毎時35分データ更新対策
    if minute < 35:
        hour = hour - 1
        hour = str(hour)
    elif minute >= 35:
        hour = str(hour)

    file_name = year + month + day + hour

    return file_name

def pollen():
    area = "中国・四国地域" # inputデータのarea情報

    target_url = 'http://kafun.taiki.go.jp/#' # 環境省花粉観測システム（愛称：はなこさん）
    request_page = requests.get(target_url)

    soup = BeautifulSoup(request_page.text, "html.parser")

    next_page = page_detector(area)
    links = soup.findAll('a')
    for link in links:
        if link.get('onclick') == next_page:
            area_code = link.get('onclick')
            area_code = area_code[15:17]
            next_link = "http://kafun.taiki.go.jp/HyouSaisin0.aspx?Area=" + area_code
            request_page = requests.get(next_link)

    soup = BeautifulSoup(request_page.content, "html.parser")
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

if __name__ == '__main__':
    pollen()
