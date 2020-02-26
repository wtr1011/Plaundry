#Output result from penman equation and weather_1day
#Weather solar_radio form http://www.amecs.co.jp/solar/index.html

#Yusuke Aonuma
# -*- encoding: utf-8  -*-

import weather_1day
import Penman
import numpy as np
import matplotlib.pyplot as plt

#戻り値：乾やすさが一番高い時間帯　幅：1時間
#＋グラフの生成
#
#引数：郵便番号
#
def output_time(postnumber):
    drytime = []
    time = []
    maxtime = 24 #[h]
    data_point = 8

     #1時〜0時
    #晴れ　2020/2/25 9:00:00、座標：35.40N 137.00E
    isola_sunny = [0.00001,0.00001,0.00001,0.00001,0.00001,0.00001,0.09,0.75,1.44,2.01,2.42,2.64,2.66,2.47,2.09,1.54,0.86,0.16,0.00001,0.00001,0.00001,0.00001,0.00001,0.00001]

    #曇り　2020/2/25 9:00:00、座標：40.20N 141.00E
    isola_cloudy = [0.00001,0.00001,0.00001,0.00001,0.00001,0.00001,0.08,0.32,0.48,0.65,0.88,1.05,1.05,0.99,0.82,0.53,0.23,0.01,0.00001,0.00001,0.00001,0.00001,0.00001,0.00001]

    #雨
    isola_rainy = 0.00001

    data = weather_1day.tenki_jp_day(postnumber)

    for i in range(1, maxtime + 1):
        if '晴れ' in data[i][1]:
            drytime.append(1/Penman.penman(float(data[i][2]), float(data[i][5]), float(data[i][7]), isola_sunny[i-1]))
            print('晴れ' + str(isola_sunny[i-1]))
        elif '曇り' in data[i][1]:
            drytime.append(1/Penman.penman(float(data[i][2]), float(data[i][5]), float(data[i][7]), isola_cloudy[i-1]))
            print('曇り' + str(isola_cloudy[i-1]))
        else:
            drytime.append(1/Penman.penman(float(data[i][2]), 100, float(data[i][7]), isola_rainy))
            print('雨')

        time.append(int(data[i][0]))

    plt.bar(time, drytime)
    #plt.savefig('day.png')
    plt.show()

    penman_max_index = np.argmax(drytime)
    time_result = data[penman_max_index][0]
    
    return time_result

if __name__ == "__main__":
    pass
    #example
    print(output_time("2591206"))