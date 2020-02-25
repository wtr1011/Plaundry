#Weather Scraping from 'tenki.jp'
#Yusuke Aonuma
# -*- encoding: utf-8  -*-


import requests, bs4
import re
import time

def tenki_jp_day(postnumber):
#返り値(リストインリスト）　
#	引数  			    |
#	(郵便番号(string) ) |	0:時間 1:天気 2:気温 3:降水確率 4:降水量 5:湿度 6:風向 7:風速(m/s)
#

    #郵便番号から場所特定、市町区村に対応
    search_url = requests.get("https://tenki.jp/search/?keyword=" + postnumber)
    search_url.raise_for_status()
    soup = bs4.BeautifulSoup(search_url.text, "html.parser")
    for a in soup.p.find_all('a'):
        place = a.get('href')

    url = 'https://tenki.jp' + place + '1hour.html'
    res = requests.get(url)
    search_soup = bs4.BeautifulSoup(res.text, "html.parser")

    #a day weather table
    table = search_soup.findAll("table", {"class":"forecast-point-1h"})[0]

    hour = extractVal(table, "hour")
    weather = extractVal(table, "weather")
    temperature = extractVal(table, "temperature")
    prob_precip = extractVal(table, "prob-precip")
    precipitation = extractVal(table, "precipitation")
    humidity = extractVal(table, "humidity")
    wind_blow = extractVal(table, "wind-blow")
    wind_speed = extractVal(table, "wind-speed")
    output_data = []

    for i in range(len(hour)):
        output_data.append([
            hour[i],
            weather[i],
            temperature[i],
            prob_precip[i],
            precipitation[i],
            humidity[i],
            wind_blow[i],
            wind_speed[i],
        ])

    return output_data

def extractVal(table, class_name):
    #get rows from table
    rows = table.findAll("tr", {"class":class_name})
    for row in rows:
        data = row.text.splitlines()
    return data

if __name__ == "__main__":
    #max iterate
    time = 24 #[h]
    data_point = 8

    #example
    data = tenki_jp_day("2591206")
    for i in range(time + 1):
        for j in range(data_point):
            print(data[i][j])
