# Pollen scattering
# coding by: Wataru Hamanishi
# !/usr/bin/python
# -*- encoding: utf-8  -*-

import requests
from bs4 import BeautifulSoup

def main():
    area = "関東地域"

    if area == "関東地域":
        next_page = 'OpenSaisinHyou(03)'

    target_url = 'http://kafun.taiki.go.jp/#' # 環境省花粉観測システム（愛称：はなこさん）
    request_page = requests.get(target_url)
    #print(request_page)

    soup = BeautifulSoup(request_page.text, "html.parser")
    #print(soup)

    links = soup.findAll('a')
    for link in links:
        if link.get('onclick') == next_page:
            area_code = link.get('onclick')
            area_code = area_code[15:17]
            next_link = "http://kafun.taiki.go.jp/HyouSaisin0.aspx?Area=" + area_code
            request_page = requests.get(next_link)

    soup = BeautifulSoup(request_page.text, "html.parser")
    #print(soup)

    table = soup.findAll("table", {"class":"bun"})
    rows = table.findAll("tr")
    print(rows)




if __name__ == '__main__':
    main()
