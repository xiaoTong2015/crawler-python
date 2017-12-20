#!coding:utf-8
import paramiko
from wxpy import *
import time
import datetime

#bot = Bot()
#tuling = Tuling(api_key='346d12f61bd14b9ca0ecd5a6538fb69e')

#my_group = bot.groups().search('新生代')[0]
#my_friend = bot.friends().search('饼干')[0]

#command = "/hexport-runtar-1.0.0/activemq/scripts/test2.sh"
#cmd = "echo `free | grep + | awk '{print $3}'`;echo `free | grep + | awk '{print $4}'`"

# def get_history():
#     with open('./history.txt', 'r') as file:
#         for line in file:
#             if line:
#                 return str(line).split(',')
#             else:
#                 return []


# def write_history(message_str):
#     with open('./history.txt', 'w') as file:
#         file.write(message_str)

command = "free | grep +|awk '{print 100*$3/($3+$4)}'"

#echo "`free | grep + | awk '{print $3}'` `free | grep + | awk '{print $4}'`" | awk '{printf "%.2f\n",$1/($1+$2)}'

def send_hello():
    for i in range(1,  3):
        my_group.send('hello world')
        time.sleep(20)


watch_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect('10.133.217.4', 22, username='weblogic', password='7QAZ6WSX', timeout=4)
stdin, stdout, stderr = client.exec_command(command)
arr = [i[:-3] for i in stdout]
print(arr)



# while True:
#     watch_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#     time_str = time.strftime('%Y%m%d', time.localtime(time.time()))
#     client = paramiko.SSHClient()
#     client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     client.connect('node3', 22, username='root', password='1q2w3e!', timeout=4)
#     stdin, stdout, stderr = client.exec_command('ls /data/total/badfile | grep %s' % time_str)
#     arr = [i.replace('\n', '') for i in stdout]

#     tar_client = paramiko.SSHClient()
#     tar_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     tar_client.connect('node20', 22, username='root', password='1q2w3e!', timeout=4)
#     tar_stdin, tar_stdout, tar_stderr = tar_client.exec_command(command)

#     i = 0
#     he = [i for i in tar_stdout]
#     b = time.localtime(time.time())
#     nowdate = datetime.datetime(*b[:5])
#     tar_massage = ''
    
#     history_arr = get_history()
#     message_arr = [i for i in arr if i not in history_arr]
#     if message_arr:
#         message = 'have bad file: ' + ','.join(message_arr)
#         try:
#             my_group.send(message)
#         except Exception:
#             print('error : 网络异常！邮件发送异常，message记录在note.txt中')
#             with open('./note.txt', 'a') as note_file:
#                 message = watch_time + message + '\n'
#                 note_file.write(message)

#         write_history(','.join(arr))
#     else:
#         print('%s 正常' % watch_time)

#     client.close()
#     tar_client.close()
#     time.sleep(600)




