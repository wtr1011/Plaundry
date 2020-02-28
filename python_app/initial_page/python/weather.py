#Weather Scraping from 'tenki.jp'
#Yusuke Aonuma
#

import requests, bs4
import re
import time

def tenki_jp(arg, postnumber):
#返り値(リストインリスト）　
#	引数  			           |
#	(True ,　郵便番号(string) ) |	0:日付 1:天気 2:最高気温 3:最低気温 4:降水確率 5:紫外線量(5段階) 6:花粉量(5段階)
#	(False,　郵便番号(string) ) |	0:6時間毎 1:天気 2:気温 3:降水確率 4:湿度 5:風速
#
	place = 0
	#郵便番号から場所特定、市町区村に対応
	search_url = requests.get("https://tenki.jp/search/?keyword=" + postnumber)
	search_url.raise_for_status()
	soup = bs4.BeautifulSoup(search_url.text, "html.parser")
	for a in soup.p.find_all('a'):
		place = a.get('href')

	res = requests.get('https://tenki.jp' + place + '10days.html')
	res.raise_for_status()
	soup = bs4.BeautifulSoup(res.text, "html.parser")
	#print(soup.title)


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

	buf = []
	output = []
	output2 = []

	for n in range(len(index) -1):
		temp = lines[index[n]+2].split('℃')	#最高気温と最低気温が同じ配列なので分解
		#テキスト出力
		if("月" in lines[index[n]]):
			buf = [lines[index[n]], lines[index[n]+1], temp[0], temp[1], lines[index[n]+3], lines[index[n]+6], lines[index[n]+7].strip('花粉：')]
			output.append(buf)
			buf = []
			#print(lines[index[n]] + ' 天気：' + lines[index[n]+1] + ' 最高気温：' + temp[0] + "℃" + ' 最低気温：' + temp[1] + "℃" + ' 降水確率：' + lines[index[n]+3] + '　' + lines[index[n]+6] + '　' + lines[index[n]+7])
		else:
			buf = [lines[index[n]], lines[index[n]+1], temp[0], lines[index[n]+3], lines[index[n]+5], lines[index[n]+6]]
			output2.append(buf)
			buf = []
			#print(lines[index[n]] + ' 天気：' + lines[index[n]+1] + ' 気温：' + temp[0] + "℃" + ' 降水確率：' + lines[index[n]+3] + '　湿度：' + lines[index[n]+5] + '　風速：' + lines[index[n]+6])

	return output if arg else output2

if __name__ == "__main__":
	pass

	#example
	#true
	#data_point = 7
	#false
	#data_point = 6
	#data = tenki_jp(True,"2591206")
	#for i in range(len(data)):
		#for j in range(data_point):
	#	print(data[i][0])