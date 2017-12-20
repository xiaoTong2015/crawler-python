#!coding:utf-8
import paramiko
from wxpy import *
import time
import datetime
import io
import sys

bot = Bot(cache_path=True)
#tuling = Tuling(api_key='346d12f61bd14b9ca0ecd5a6538fb69e')
#groups = bot.groups()
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
# for group in groups:
#     print(group)

my_group = bot.groups().search('新生代')[0]
# my_friend = bot.friends().search('饼干')[0]


# nodeList = ['10.133.217.3','10.133.217.4','10.133.217.5']


# cmd = "free | grep +|awk '{print 100*$3/($3+$4)}'"

# while True:
# 	for node in nodeList:
# 		watch_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
# 		client = paramiko.SSHClient()
# 		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 		client.connect(node, 22, username='weblogic', password='7QAZ6WSX', timeout=4)
# 		stdin, stdout, stderr = client.exec_command(cmd)
# 		usedbuffer = float([i[:-3] for i in stdout][0])
# 		if usedbuffer >= 80:
# 			message = "%s 请注意：服务器 %s 当前内存使用率为 %.2f%% 超过80%%"%(watch_time,node,usedbuffer)
# 			print (message)
# 			try:
# 				my_friend.send(message)
# 			except Exception:
# 				print('网络错误！')
# 		else:
# 			print("%s 服务器 %s 当前内存使用率为 %.2f%% 安全"%(watch_time,node,usedbuffer))
# 		client.close()
# 	time.sleep(3600)