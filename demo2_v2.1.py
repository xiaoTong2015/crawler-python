import requests
import json
from pymongo import MongoClient

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
}

# 读取json文件
def load_json():
    with open('data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data[2]

#发请求
def sendRequest(url):
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    resp.encoding = resp.apparent_encoding
    strs = resp.text
    strt = strs.replace('false', 'False')
    strt1 = strt.replace('true', 'True')
    strt2 = strt1.replace('null', "'null'")
    py_obj = eval(strt2)
    return py_obj

#获取数据库连接
def get_dbclient():
    client = MongoClient('mongodb://11.203.0.194:27017/')
    return client


# 将数据保存到数据库中
def save_db(keylist, vallilst, name):
    json_list = []
    for list in vallilst:
        #print(dict(zip(keylist, list)))
        json_list.append(dict(zip(keylist, list)))
    client = get_dbclient()
    db = client.Test
    col = db.col
    #print({'name':'test','data':json_list})
    if json_list:
        col.insert({'name':name, 'data':json_list})
    return True


# 读取配置文件
config = load_json()
# 数据内容名称
data_name = config['name']
# 机构列表url请求地址
url = config['requireURL']
py_obj = sendRequest(url)
# 机构列表
comcode_list = py_obj['returndata'][0]['nodes']
# 表头
zb_data = config['tbHead']
# 数据内容
sj_data_list = []
# 表头 + 数据
data = []
for comcode in comcode_list:
    plates_url = []
    obj_list = []
    for index, plate in enumerate(config['plates']):
        plates_url.append(config['nextURL'][0] % (comcode['code'], plate['platecode']))
    for index, url in enumerate(plates_url):
        obj = sendRequest(url)
        obj_list.append(obj)

    # 输出当前机构
    print(comcode['code'])
    if not data:
        data.append(','.join(zb_data))
    sj_data = []
    # 添加机构名称
    sj_data.append(comcode['name'])
    for index, obj in enumerate(obj_list):
        sj_list = obj['returndata']['datanodes']
        fieldlist = config['fields'][index]['fieldcode'].split(',')
        for fieldcode in fieldlist:
            for i in sj_list:
                if config['fields'][index]['dateYear'] in i['code'] and fieldcode in i['code']:
                    sj_data.append(str(i['data']['data']))

    sj_data_list.append(sj_data)
    data.append(','.join(sj_data))

# 将数据写入到文件中（可选）
# file_csv = open(config['output_file'], 'w')
# for i in data:
#     file_csv.write(i+'\n')
# file_csv.close()

# 将数据写入到数据库中（可选）
insertResult = save_db(zb_data, sj_data_list, data_name)
if insertResult:
    print("数据插入成功！")
else:
    print("数据插入失败！")

