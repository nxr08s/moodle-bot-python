from requests import get
from re import findall
from time import sleep
import datetime

logfile = 'log.log'

url = 'https://moodle.kubsu.ru/report/usersessions/user.php'
headers = {
	'Accept':'text/html',
	'Cookie':'SSESS793f6acd2def245c1081d4d3a4cdf6fc=X8cwF6iiO2yAVP5CFSvL9g1O_rKbvCtOKuUBgpX7q6A; MoodleSession=r18t4iobuur67r13j7m4reurm8',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}

print("Bot started on {}".format(datetime.datetime.now()))
while(True):
	r = get(url, headers=headers)
	match = findall(r'<td class="cell c\d" style="text-align:left;">([^<][\s\S]*?|<a.*>[.\d]+</a>)</td>', r.text)
	if (len(match) > 3):
		# remove all rats
		exitUrl = findall(r'<a href="([^"]+delete[^"]+)">Выход</a>', r.text)[0];
		get(exitUrl.replace('&amp;', '&'), headers=headers)
		
		# log in file
		file = open(logfile, 'a')
		i = 0;
		file.write(str(datetime.datetime.now()) + '\n')
		while (i < len(match)):
			if (match[i + 1] != 'Текущая сессия'):
				ip = findall(r'>([\d.]+)<', match[i + 2])[0]
				file.write(match[i] + ' ' + match[i + 1] + ' ' + ip + '\n')
			i += 3
		file.write(' -----------------------------------------\n')
		file.close()
		
		# log in console
		i = 0;
		print( '==============',datetime.datetime.now(),'==================')
		while (i < len(match)):
			ip = findall(r'>([\d.]+)<', match[i+2])[0]
			print(match[i], match[i+1], ip, sep='\t')
			i += 3
		print('============================================================')
	sleep(5)