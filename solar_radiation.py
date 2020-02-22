#Weather Scraping from 'tenki.jp'
#Yusuke Aonuma
# -*- encoding: utf-8  -*-

import requests, bs4
import re
import time

def solar_radio():

    res = requests.get('https://solar-radiation.info/')
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    print(soup.title)
    lines = soup.find_all('info')
    print(lines)

if __name__ == "__main__":
    solar_radio()