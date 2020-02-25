import math


def penman(temperature,humidity,wind,insolation):

    """

    :param temperature:気温
    :param humidity: 相対湿度
    :param wind: 風速
    :param insolation:日射量
    :return: Tシャツが乾くまでの時間(s)
    """

    kelvin = temperature + 273
    e_a = math.exp(21.07 - (5336 / kelvin))
    delta = e_a * 5336 / (kelvin * kelvin)
    delta = delta * 0.1333
    lam = 2.501 - 0.002361 * (kelvin-273)
    gamma = (0.0016286 * 101.3) / lam
    #print(gamma)
    d = (1 - humidity/100) * e_a
    evaporation_rate = (delta * insolation + gamma * (6.43 * (1 + 0.536 * wind) * d)) / (lam * (delta + gamma))
    #print(evaporation_rate)
    time2dry = 0.075 / (0.5 * evaporation_rate / 86400)

    return time2dry


if __name__ == "__main__":
    pass
    #temp = 13
    #humi = 87
    #win = 0
    #isola = 10.08
    #t = penman(temp,humi,win,isola)
    #print(t)
