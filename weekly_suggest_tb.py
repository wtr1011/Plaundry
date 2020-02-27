#Create weekly suggest table
#Yusuke Aonuma
# -*- encoding: utf-8  -*-

import Penman
from weather_10days import tenki_jp_All
from weather_1day import tenki_jp_day
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

def createPenmanArray(postnumber):
    #1時〜0時
    #晴れ　2020/2/25 9:00:00、座標：35.40N 137.00E
    isola_sunny = [0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.09,0.75,1.44,2.01,2.42,2.64,2.66,2.47,2.09,1.54,0.86,0.16,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001]
    #曇り　2020/2/25 9:00:00、座標：40.20N 141.00E
    isola_cloudy = [0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.08,0.32,0.48,0.65,0.88,1.05,1.05,0.99,0.82,0.53,0.23,0.01,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001]
    #雨
    isola_rainy = 0.000001

    day = []
    date = []
    week = []
    penmanArray = []

    #当日のデータ
    week.append(tenki_jp_day(postnumber))

    #翌日以降のデータ取得
    bgn_index = 0
    data = tenki_jp_All(postnumber)
    maxtime_date2date = 5

    #翌日の先頭を探す
    for i in range(1, maxtime_date2date):
        if (('月' in data[i][0])|('日' in data[i][0])):
            bgn_index = i
            break

    #5個飛ばしで先頭（0-6）を探す
    for i in range(bgn_index, len(data)-1, 5):
        week.append([ data[i + 1], data[i + 2], data[i + 3], data[i + 4]])

    #当日
    maxtime = 24    #24時間
    for j in range(maxtime):
        if '晴れ' in week[0][j][1]:
            day.append( round(1 / Penman.penman(float(week[0][j][2]), float(week[0][j][5]), float(week[0][j][7]), isola_sunny[j]), 3))
        elif '曇り' in week[0][j][1]:
            day.append( round(1 / Penman.penman(float(week[0][j][2]), float(week[0][j][5]), float(week[0][j][7]), isola_cloudy[j]), 3))
        else:
            day.append( round(1 / Penman.penman(float(week[0][j][2]), 100, float(week[0][j][7]), isola_rainy), 3))
    penmanArray.append(day)
    day = []

    #翌日以降
    isola_index = 0
    for i in range(1, 7):           #6日間
        for j in range(4):          #4区切り(6時間毎)
            for n in range(6):      #1区切りに6個のデータ
                if '晴' == week[i][j][1]:
                    day.append( round(1 / Penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_sunny[isola_index]), 3))
                elif '曇' == week[i][j][1]:
                    day.append( round(1 / Penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_cloudy[isola_index]), 3))
                elif '晴のち曇' == week[i][j][1]:
                    day.append( round(1 / Penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_cloudy[isola_index]), 3))
                elif '曇のち晴' == week[i][j][1]:
                    day.append( round(1 / Penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_sunny[isola_index]), 3))
                else:
                    day.append( round(1 / Penman.penman(float(week[i][j][2]), 100, float(week[i][j][5]), isola_rainy), 3))
                isola_index += 1
        isola_index = 0
        penmanArray.append(day)
        day = []

    return penmanArray

def weekly_penman():


    return weekly

def createTable(array):
    df = pd.DataFrame(array)

    """
    cm = sns.light_palette("red", as_cmap=True)
    df.style.background_gradient(cmap=cm)
    fig, ax = plt.subplots(figsize=(2,2))
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values,
             colLabels=df.columns,
             loc='center',
             bbox=[0,0,1,1])

    plt.show()
    #plt.savefig('table.png')
    """
    #テーブルの作成
    fig = go.Figure(data=[go.Table(
        columnwidth =  [10, 20, 30, 40], #カラム幅の変更
        header=dict(values=df.columns, align='center', font_size=20),
        cells=dict(values=df.values.T, align='center', font_size=10)
        )])
    fig.update_layout(title={'text': "sample_table",'y':0.85,'x':0.5,'xanchor': 'center'})#タイトル位置の調整
    fig.layout.title.font.size= 24 #タイトルフォントサイズの変更
    #fig.write_image("sample_table.jpg")#,height=600, width=800)
    #fig.write_image("sample_table.jpg",height=600, width=800) #デーブルのサイズ変更
    fig.show()

if __name__ == "__main__":
    postnum = "2591206"
    data = createPenmanArray(postnum)
    createTable(data)