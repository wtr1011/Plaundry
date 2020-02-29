#Create weekly suggest table
#Yusuke Aonuma
# -*- encoding: utf-8  -*-

from initial_page.python import penman
from initial_page.python.weather_10days import tenki_jp_All
from initial_page.python.weather_1day import tenki_jp_day
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors

def createPenmanArray(postnumber, startTime, endTime):
    #1時〜0時
    #晴れ　2020/2/25 9:00:00、座標：35.40N 137.00E
    isola_sunny = [0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.09,0.75,1.44,2.01,2.42,2.64,2.66,2.47,2.09,1.54,0.86,0.16,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001]
    #曇り　2020/2/25 9:00:00、座標：40.20N 141.00E
    isola_cloudy = [0.000001,0.000001,0.000001,0.000001,0.000001,0.000001,0.08,0.32,0.48,0.65,0.88,1.05,1.05,0.99,0.82,0.53,0.23,0.01,0.000001,0.000001,0.000001,0.000001,0.000001,0.000001]
    #雨
    isola_rainy = 0.000001

    day = []
    date_colum = []
    week = []
    penmanArray = []
    time_index = []
    worktime = workTimeArray(startTime, endTime)

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

    #当日の日付
    date_colum.append(data[0][0].replace('月', '/')[:-4] )
    #5個飛ばしで先頭（0-6）を探す
    for i in range(bgn_index, len(data)-21, 5):
        week.append([ data[i + 1], data[i + 2], data[i + 3], data[i + 4]])
        #翌日以降の日付
        date_colum.append(data[i][0].replace('月', '/')[:-4] )
        #print(data[i][0])

    #当日
    maxtime = 24    #24時間
    for j in range(maxtime):
        if ( ('晴れ' in week[0][j][1]) & ( week[0][j][0] not in worktime ) ):
            day.append( round(10000 / penman.penman(float(week[0][j][2]), float(week[0][j][5]), float(week[0][j][7]), isola_sunny[j]), 3))
        elif ( ('曇り' in week[0][j][1]) & ( week[0][j][0] not in worktime )  ):
            day.append( round(10000 / penman.penman(float(week[0][j][2]), float(week[0][j][5]), float(week[0][j][7]), isola_cloudy[j]), 3))
        elif week[0][j][0] in worktime:
            day.append(-1)
        else:
            day.append( round(10000 / penman.penman(float(week[0][j][2]), 100, float(week[0][j][7]), isola_rainy), 3))
        time_index.append(week[0][j][0])
    penmanArray.append(day)
    day = []

    #翌日以降
    isola_index = 0
    for i in range(1, 7):           #6日間
        for j in range(4):          #4区切り(6時間毎)
            for n in range(6):      #1区切りに6個のデータ
                if ( ('晴' == week[i][j][1]) & (week[0][isola_index][0] not in worktime )):
                    day.append( round(10000 / penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_sunny[isola_index]), 3))
                elif ( ('曇' == week[i][j][1]) & (week[0][isola_index][0] not in worktime )):
                    day.append( round(10000 / penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_cloudy[isola_index]), 3))
                elif ( ('晴のち曇' == week[i][j][1]) & (week[0][isola_index][0] not in worktime )):
                    day.append( round(10000 / penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_cloudy[isola_index]), 3))
                elif ( ('曇のち晴' == week[i][j][1]) & (week[0][isola_index][0] not in worktime )):
                    day.append( round(10000 / penman.penman(float(week[i][j][2]), float(week[i][j][4]), float(week[i][j][5]), isola_sunny[isola_index]), 3))
                elif week[0][isola_index][0]  in worktime:
                    day.append(-1)
                else:
                    day.append( round(10000 / penman.penman(float(week[i][j][2]), 100, float(week[i][j][5]), isola_rainy), 3))
                isola_index += 1
        isola_index = 0
        penmanArray.append(day)
        day = []

    return penmanArray, time_index, date_colum


#テーブル作成
def createTable(array, time_index, date_colum):
    array_t = np.array(array).T
    df = pd.DataFrame(array_t, index=time_index, columns=date_colum)

    fig, ax = plt.subplots(figsize=(10,10))
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values,
             colLabels=df.columns,
             rowLabels=df.index,
             cellColours=coloring(array_t),
             loc='center',
             bbox=[0,0,1,1])

    plt.savefig('./static/table.png')
    plt.clf()

    df_max_week_index = df.idxmax()
    Dict = {
        df[df_max_week_index.index[0]][df_max_week_index.values[0]]:[df_max_week_index.index[0], df_max_week_index.values[0]],
        df[df_max_week_index.index[1]][df_max_week_index.values[1]]:[df_max_week_index.index[1], df_max_week_index.values[1]],
        df[df_max_week_index.index[2]][df_max_week_index.values[2]]:[df_max_week_index.index[2], df_max_week_index.values[2]],
        df[df_max_week_index.index[3]][df_max_week_index.values[3]]:[df_max_week_index.index[3], df_max_week_index.values[3]],
        df[df_max_week_index.index[4]][df_max_week_index.values[4]]:[df_max_week_index.index[4], df_max_week_index.values[4]],
        df[df_max_week_index.index[5]][df_max_week_index.values[5]]:[df_max_week_index.index[5], df_max_week_index.values[5]],
        df[df_max_week_index.index[6]][df_max_week_index.values[6]]:[df_max_week_index.index[6], df_max_week_index.values[6]]
    }
    sortedDict = sorted(Dict.items())
    max_3rank = [sortedDict[-1], sortedDict[-2], sortedDict[-3]]
    
    return max_3rank

def workTimeArray(startTime, endTime):
    #文字処理
    startTime = startTime.split(':')[0]
    endTime = endTime.split(':')[0]

    workTime = []

    timeDict = {
        '00':0,
        '01':1,
        '02':2,
        '03':3,
        '04':4,
        '05':5,
        '06':6,
        '07':7,
        '08':8,
        '09':9,
        '10':10,
        '11':11,
        '12':12,
        '13':13,
        '14':14,
        '15':15,
        '16':16,
        '17':17,
        '18':18,
        '19':19,
        '20':20,
        '21':21,
        '22':22,
        '23':23
    }

    time_range = timeDict[endTime] - timeDict[startTime]

    for i in range(timeDict[startTime], timeDict[endTime]+1):
        keys = [k for k, v in timeDict.items() if v == i]
        workTime.append(keys[0])
    
    print(workTime)
    return workTime

def executeCreateTable(postnumber, startTime, endTime):
    data, time, date = createPenmanArray(postnumber, startTime, endTime)

    return createTable(data, time, date)

    #color list array
def coloring(data):
    color_data = np.full((24, 7), '1111111')

    level = data.max()
    i, j = 0, 0
    for day in data:
        for val in day:
            if ( level*(3/4) < val <=  level ):
                color_data[i][j] = '#F08080'
            elif ( level*(2/4) < val <=  level*(3/4) ) :
                color_data[i][j] = '#FFDEAD' #orangered
            elif ( level*(1/4) < val <=  level*(2/4) ) :
                color_data[i, j] = '#48D1CC'
            elif ( 0 <= val <=  level*(1/4) ) :
                color_data[i][j] = '#6495ED' #dodgerblue
            else:
                color_data[i][j] = '#708090' #slategray
            j += 1
        j = 0
        i += 1

 
    return color_data

if __name__ == "__main__":
    #executeCreateTable('2591206')
    pass
