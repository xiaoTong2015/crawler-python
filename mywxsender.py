#!coding:utf-8
import paramiko
from wxpy import *
import time
import datetime
import io
import sys

bot = Bot(cache_path=True)
#tuling = Tuling(api_key='346d12f61bd14b9ca0ecd5a6538fb69e')

my_group = bot.groups().search('新生代')[0]
# my_friend = bot.friends().search('饼干')[0]
def get_history():
	with open('./history.txt', 'r') as file:
		for line in file:
			if line:
				return str(line).split(',')
			else:
				return []

def write_history(message_str):
	with open('./history.txt', 'w') as file:
		file.write(message_str)

nodeList = ['10.133.250.72']


while True:
	watch_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
	watch_hour = time.strftime('%H', time.localtime(time.time()))
	for node in nodeList:
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(node, 22, username='root', password='1q2w3e!', timeout=60)
		stdin, stdout, stderr = client.exec_command("cat /data/tyc/mymq/wxinfo.log")
		message = [i.replace('\n', '') for i in stdout]
		history_arr = get_history()
		history_arr = ','.join(history_arr)
		if history_arr:
			message_arr = [m for m in message if m not in history_arr]
		else:
			message_arr = [m for m in message]
		if message_arr:
			for m in message_arr:
				try:
				 	print(m)	
				 	my_group.send(message)
				except Exception:
				 	print('网络错误！内容追加至note.txt！')
				 	with open('./note.txt', 'a') as note_file:
				 		mess_note = watch_time + m + '\n'
				 		note_file.write(mess_note)
			write_history(','.join(message_arr))
		else:
			print("no info update")
		client.close()
		time.sleep(10)
