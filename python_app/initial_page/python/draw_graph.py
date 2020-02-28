"""
2020.2.26
Riku Noguchi
グラフを作成して保存
"""

from initial_page.python import penman
from initial_page.python import weather
import pandas as pd
import numpy as np
from datetime import datetime,date,timedelta
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

def draw_graph_pollen(data, pollen_data, save_dir):
    """

    :param data: 各時間帯の気象データ list
    :param save_dir: 保存ディレクトリ str
    """

    #グラフの縦軸横軸の宣言
    x = []
    y_pollen = []
    if len(data) == 11:
        y = []
    else:
        y = [0]

    #花粉データの処理
    day_count = 0
    for pdt in pollen_data:
        if pdt[6] == '非常に多い':
            ppoint = 0.001
            y_pollen.append(ppoint)
        elif pdt[6] == '多い':
            ppoint = 0.00075
            y_pollen.append(ppoint)
        elif pdt[6] == 'やや多い':
            ppoint = 0.0005
            y_pollen.append(ppoint)
        elif pdt[6] == '少ない':
            ppoint = 0.00025
            y_pollen.append(ppoint)
        else:
            ppoint = 0
            y_pollen.append(ppoint)
        if day_count == 6:
            break
        day_count += 1

    # x軸の設定
    now = datetime.today()
    x = [str(now.month)+"/"+str(now.day)]
    next_day = now + timedelta(1)
    for i in range(6):
        x.append(str(next_day.month)+"/"+str(next_day.day)+"\n"+data[i][1]+"\n"+pollen_data[i][6])
        next_day = next_day +timedelta(1)


    #朝昼夜の見分け
    if data[0][0] == "06-12":
        type_of_graph = "morning"
    elif data[0][0] == "12-18":
        type_of_graph = "noon"
    elif data[0][0] == "18-24":
        type_of_graph = "night"
    else:
        exit(1)

    # 日射量を推定するために天気の判定をする．
    for n in data:
        tenki = n[1]

        if data[0][0] == "18-24":
            insolation = 1
        elif tenki == "晴":
            insolation = 15
        elif tenki == "晴のち雲" or tenki == "雲のち晴":
            insolation = 10
        elif tenki == "曇":
            insolation = 5
        elif tenki == "雨" or tenki == "雪":
            insolation = 1
        else:
            insolation = 1


        # ペンマン式
        y.append(1/penman.penman(int(n[2]),int(n[4][:-1]),int(n[5][:-3]),insolation))

    fig = plt.figure()

    # matplotlibの設定
    plt.rcParams["font.size"] = 12
    plt.ylim([0,0.002])
    plt.tick_params(left=False)
    plt.yticks([])
    plt.bar(x,y[:7])
    plt.plot(x, y_pollen, color='r')
    plt.subplots_adjust(left=0.125, right=0.9, bottom=0.15, top=0.9)

    #plt.show()
    fig.savefig(str(save_dir+type_of_graph+"_pollen.png"))
    plt.close(fig)
    plt.clf()

#グラフ1枚を描画
def draw_graph(data, save_dir):
    """

    :param data: 各時間帯の気象データ list
    :param save_dir: 保存ディレクトリ str
    """

    #グラフの縦軸横軸の宣言
    x = []
    if len(data) == 11:
        y = []
    else:
        y = [0]

    # x軸の設定
    now = datetime.today()
    x = [str(now.month)+"/"+str(now.day)]
    next_day = now + timedelta(1)
    for i in range(6):
        x.append(str(next_day.month)+"/"+str(next_day.day)+"\n"+data[i][1])
        next_day = next_day +timedelta(1)

    #朝昼夜の見分け
    if data[0][0] == "06-12":
        type_of_graph = "morning"
    elif data[0][0] == "12-18":
        type_of_graph = "noon"
    elif data[0][0] == "18-24":
        type_of_graph = "night"
    else:
        exit(1)

    # 日射量を推定するために天気の判定をする．
    for n in data:
        tenki = n[1]

        if data[0][0] == "18-24":
            insolation = 1
        elif tenki == "晴":
            insolation = 15
        elif tenki == "晴のち雲" or tenki == "雲のち晴":
            insolation = 10
        elif tenki == "曇":
            insolation = 5
        elif tenki == "雨" or tenki == "雪":
            insolation = 1
        else:
            insolation = 1


        # ペンマン式
        y.append(1/penman.penman(int(n[2]),int(n[4][:-1]),int(n[5][:-3]),insolation))

    fig = plt.figure()

    # matplotlibの設定
    plt.rcParams["font.size"] = 12
    plt.ylim([0,0.002])
    plt.tick_params(left=False)
    plt.yticks([])
    plt.bar(x,y[:7])
    #plt.show()
    fig.savefig(str(save_dir+type_of_graph+".png"))
    plt.close(fig)

    plt.clf()
#朝昼夜のグラフを作成する
def time_sep_and_draw_graph(postnumber,save_dir):
    """

    :param postnumber:郵便番号 ハイフン無し str
    :param save_dir:  保存ディレクトリ str
    """
    time_of_day = ["morning","noon","night"]
    weather_data = weather.tenki_jp(False,postnumber)
    weather_data_pollen = weather.tenki_jp(True,postnumber)

    #朝昼夜の配列を用意
    morning = []
    noon = []
    night = []
    for i in range(len(weather_data)):
        time = weather_data[i][0]
        weather_element = weather_data[i][:]

        if time == "06-12":
            morning.append(weather_element)

        elif time == "12-18":
            noon.append(weather_element)

        elif time == "18-24":
            night.append(weather_element)

    draw_graph(morning,save_dir)
    draw_graph_pollen(morning, weather_data_pollen, save_dir)
    draw_graph(noon, save_dir)
    draw_graph_pollen(noon, weather_data_pollen, save_dir)
    draw_graph(night, save_dir)
    draw_graph_pollen(night, weather_data_pollen, save_dir)


if __name__ == "__main__":
    pass
    #time_sep_and_draw_graph("2520027","")
