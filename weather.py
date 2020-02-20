import requests, bs4
import re
import time

res = requests.get('https://tenki.jp/forecast/3/17/4610/14203/10days.html')
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
print(soup.title)

#指定タグから余計なものを排除
for script in soup(["script", "style"]):
    script.decompose()
text =soup.get_text()
lines= [line.strip() for line in text.splitlines()]

i = 0
index = []
index_time = []

#月と日から日にちを抽出
for data in lines: 
	if(('月' in data) & ('日' in data)|('00-06' in data) | ('06-12' in data ) | ('12-18' in data ) | ('18-24' in data )):
		index.append(i)
	i += 1	#カウントしてインデックスを求める



for n in range(len(index) -1):
	temp = lines[index[n]+2].split('℃')	#最高気温と最低気温が同じ配列なので分解
	#テキスト出力
	if("月" in lines[index[n]]):
		print(lines[index[n]] + ' 天気：' + lines[index[n]+1] + ' 最高気温：' + temp[0] + "℃" + ' 最低気温：' + temp[1] + "℃" + ' 降水確率：' + lines[index[n]+3] + '　' + lines[index[n]+6] + '　' + lines[index[n]+7])
	else:
		print(lines[index[n]] + ' 天気：' + lines[index[n]+1] + ' 最高気温：' + temp[0] + "℃" + ' 最低気温：' + temp[1] + "℃" + ' 降水確率：' + lines[index[n]+3] + '　湿度：' + lines[index[n]+5] + '　風速：' + lines[index[n]+6])


