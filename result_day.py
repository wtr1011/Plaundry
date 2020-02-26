#Output result from penman equation and weather_1day
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

    isola = 10.08#

    data = weather_1day.tenki_jp_day(postnumber)

    for i in range(1, maxtime + 1):
        drytime.append(1/Penman.penman(float(data[i][2]), float(data[i][5]), float(data[i][7]), isola))
        time.append(int(data[i][0]))

    plt.bar(time, drytime)
    plt.savefig('day.png')

    penman_max_index = np.argmax(drytime)
    time_result = data[penman_max_index][0]
    
    return time_result

if __name__ == "__main__":
    pass
    #example
    #print(output_time("2591206"))