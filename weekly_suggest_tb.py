#Create weekly suggest table
#Yusuke Aonuma
# -*- encoding: utf-8  -*-

import Penman
from weather_10days import tenki_jp_All
from weather_1day import tenki_jp_day
import numpy as np
import pandas


def createPenmanArray(postnumber):
    #1時〜0時
    #晴れ　2020/2/25 9:00:00、座標：35.40N 137.00E
    isola_sunny = [0.00001,0.00001,0.00001,0.00001,0.00001,0.00001,0.09,0.75,1.44,2.01,2.42,2.64,2.66,2.47,2.09,1.54,0.86,0.16,0.00001,0.00001,0.00001,0.00001,0.00001,0.00001]
    #曇り　2020/2/25 9:00:00、座標：40.20N 141.00E
    isola_cloudy = [0.00001,0.00001,0.00001,0.00001,0.00001,0.00001,0.08,0.32,0.48,0.65,0.88,1.05,1.05,0.99,0.82,0.53,0.23,0.01,0.00001,0.00001,0.00001,0.00001,0.00001,0.00001]
    #雨
    isola_rainy = 0.00001

    date = []
    week = []
    #当日のデータ
    week.append(tenki_jp_day(postnumber))

    #翌日以降のデータ取得
    bgn_index = 0
    data = tenki_jp_All(postnumber)
    maxtime_date2date = 6
    for i in range(1, maxtime_date2date):
        if (('月' in data[i])&('日' in data[i])):
            break
        bgn_index += 1

    for i in range(bgn_index, len(data), 5):
        week.append([ data[i], data[i + 1], data[i + 2], data[i + 3]])


    print(week)
    return week

def weekly_penman():


    return weekly

if __name__ == "__main__":
    postnum = "2591206"
    createPenmanArray(postnum)